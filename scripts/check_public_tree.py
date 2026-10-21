#!/usr/bin/env python3
"""Check publishable files, local links and native configuration references.

Uses only the standard library. Does not import or execute design software.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
from urllib.parse import unquote, urlsplit

METHOD_IDS = {
    "pepmlm", "diffpepbuilder", "pepglad", "mirror-peptidizer", "pepmirror",
    "afcycdesign", "dexdesign", "rfdiffusion-proteinmpnn", "bindcraft", "bindcraft2",
}
TEXT_SUFFIXES = {".md", ".json", ".py", ".yaml", ".yml"}
ROOT_TEXT_FILES = {".gitignore", "LICENSE"}
MAX_FILE_BYTES = 15 * 1024 * 1024


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def safe_relative(value: str) -> bool:
    p = PurePosixPath(value)
    return bool(value) and not p.is_absolute() and ".." not in p.parts and "\\" not in value


def publishable_paths(root: Path) -> list[str]:
    if (root / ".git").exists():
        result = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-co", "--exclude-standard", "-z"],
            capture_output=True, check=True,
        )
        return sorted(set(x.decode("utf-8") for x in result.stdout.split(b"\0") if x))
    return sorted(
        p.relative_to(root).as_posix() for p in root.rglob("*")
        if (p.is_file() or p.is_symlink()) and "__pycache__" not in p.parts
    )


def check_links(root: Path, paths: set[str]) -> list[str]:
    errors = []
    for relative in sorted(paths):
        path = root / relative
        if path.suffix != ".md" or not path.is_file() or path.is_symlink():
            continue
        content = path.read_text(encoding="utf-8")
        for match in re.finditer(r"!?\[[^\]]*\]\(([^)]+)\)", content):
            target = match.group(1).strip().strip("<>")
            parsed = urlsplit(target)
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            destination = (path.parent / unquote(parsed.path)).resolve()
            try:
                destination_relative = destination.relative_to(root.resolve()).as_posix()
            except ValueError:
                errors.append(f"link leaves repository: {relative}: {target}")
                continue
            if destination_relative not in paths:
                errors.append(f"link target not published: {relative}: {target}")
    return errors


def check_methods(root: Path, paths: set[str]) -> list[str]:
    errors = []
    try:
        registry = read_json(root / "registry/methods.json")
        methods = registry["methods"]
        ids = [m["id"] for m in methods]
        if len(ids) != len(METHOD_IDS) or set(ids) != METHOD_IDS:
            errors.append("method registry must contain ten distinct method IDs")
        for method in methods:
            if method["documentation"] not in paths:
                errors.append(f"missing method document: {method['id']}")
            for source in method["sources"]:
                if not source["url"].startswith("https://github.com/"):
                    errors.append(f"source must use official HTTPS URL: {method['id']}")
                if not re.fullmatch(r"[0-9a-f]{40}", source["commit"]):
                    errors.append(f"source needs full commit reference: {method['id']}")
        bindcraft = next(m for m in methods if m["id"] == "bindcraft")
        bindcraft2 = next(m for m in methods if m["id"] == "bindcraft2")
        if bindcraft["sources"] == bindcraft2["sources"] or bindcraft["documentation"] == bindcraft2["documentation"]:
            errors.append("BindCraft and BindCraft2 must use separate sources and documents")
    except (OSError, ValueError, TypeError, KeyError, StopIteration) as exc:
        errors.append(f"invalid method registry: {exc}")
    return errors


def check_templates(root: Path) -> list[str]:
    errors = []
    try:
        basic = read_json(root / "configs/bindcraft/basic.template.json")
        expected = {"design_path", "binder_name", "starting_pdb", "chains", "target_hotspot_residues", "lengths", "number_of_final_designs"}
        if set(basic) != expected:
            errors.append("BindCraft basic fields must follow its native format")
        for name, modality in (("linear", "peptide"), ("cyclic", "cyclic_peptide")):
            campaign = read_json(root / f"configs/bindcraft2/{name}.template.json")
            if campaign["modality"] != modality:
                errors.append(f"wrong BindCraft2 modality: {name}")
            if "starting_pdb" in campaign or "design_path" in campaign:
                errors.append(f"BindCraft settings mixed into BindCraft2: {name}")
            if "target" in campaign or "core" in campaign:
                errors.append(f"campaign must use user-supplied inputs and default core: {name}")
            if campaign["max_trajectories"] != 1 or campaign["design_workers"] != 1 or campaign["gpu_ids"] != [0]:
                errors.append(f"template must keep bounded native execution settings: {name}")
            if campaign["resume"] is not False or campaign["auto_multi_gpu"] is not False:
                errors.append(f"template must use explicit serial fresh configuration: {name}")
            for target in campaign["targets"]:
                if not target["target_path"].startswith("/path/to/"):
                    errors.append(f"campaign input must be a path placeholder: {name}")
        pocket = read_json(root / "configs/pepglad/pocket.template.json")
        if any(residue[1][1] != " " for residue in pocket):
            errors.append("PepGLAD placeholder insertion code must be a single space")
    except (OSError, ValueError, TypeError, KeyError, IndexError) as exc:
        errors.append(f"invalid native template: {exc}")
    return errors


def check_tree(root: Path) -> list[str]:
    errors = []
    try:
        manifest = read_json(root / "registry/public_files.json")
        names = manifest["files"]
        if len(names) != len(set(names)) or not all(safe_relative(n) for n in names):
            return ["invalid public file allowlist"]
        allowed = set(names)
        actual = set(publishable_paths(root))
    except (OSError, ValueError, TypeError, KeyError, subprocess.SubprocessError) as exc:
        return [f"cannot read public file allowlist: {exc}"]
    errors += [f"unlisted publishable file: {p}" for p in sorted(actual - allowed)]
    errors += [f"missing public file: {p}" for p in sorted(allowed - actual)]
    for relative in sorted(actual):
        path = root / relative
        if not safe_relative(relative) or path.is_symlink():
            errors.append(f"non-regular or unsafe public path: {relative}")
            continue
        if not path.is_file():
            errors.append(f"public path is not a file: {relative}")
            continue
        if path.stat().st_size > MAX_FILE_BYTES:
            errors.append(f"public file exceeds size limit: {relative}")
        if path.suffix == ".png" and path.parent == root / "docs/assets":
            if path.read_bytes()[:8] != b"\x89PNG\r\n\x1a\n":
                errors.append(f"invalid image signature: {relative}")
        elif path.suffix in TEXT_SUFFIXES or relative in ROOT_TEXT_FILES:
            try:
                content = path.read_text(encoding="utf-8")
                if path.suffix == ".json":
                    json.loads(content)
                if re.search(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", content):
                    errors.append(f"private key material in text: {relative}")
            except (UnicodeError, ValueError) as exc:
                errors.append(f"invalid public text: {relative}: {exc}")
        else:
            errors.append(f"unsupported public file type: {relative}")
    errors.extend(check_links(root, actual))
    errors.extend(check_methods(root, actual))
    errors.extend(check_templates(root))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = check_tree(args.root.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Public tree, local links, ten method references and independent native templates: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
