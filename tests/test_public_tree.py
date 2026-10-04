from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("public_check", ROOT / "scripts/check_public_tree.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)


class PublicTreeChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name) / "workbench"
        self.root.mkdir()
        for name in json.loads((ROOT / "registry/public_files.json").read_text())["files"]:
            target = self.root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)
        self.addCleanup(self.temp.cleanup)

    def test_complete_public_tree(self):
        self.assertEqual(checker.check_tree(self.root), [])

    def test_unlisted_file_is_rejected(self):
        (self.root / "user-notes.json").write_text("{}")
        self.assertTrue(any("unlisted" in e for e in checker.check_tree(self.root)))

    def test_link_to_unpublished_input_is_rejected(self):
        p = self.root / "README.md"
        p.write_text(p.read_text() + "\n[Input](inputs/structure.pdb)\n")
        self.assertTrue(any("link target not published" in e for e in checker.check_tree(self.root)))

    def test_symlink_is_rejected(self):
        path = self.root / "README.en.md"
        path.unlink()
        path.symlink_to(self.root / "README.md")
        self.assertTrue(any("unsafe public path" in e for e in checker.check_tree(self.root)))

    def test_bindcraft2_must_stay_separate(self):
        path = self.root / "registry/methods.json"
        data = json.loads(path.read_text())
        original = next(m for m in data["methods"] if m["id"] == "bindcraft")
        newer = next(m for m in data["methods"] if m["id"] == "bindcraft2")
        newer["sources"] = original["sources"]
        newer["documentation"] = original["documentation"]
        path.write_text(json.dumps(data))
        self.assertTrue(any("separate sources" in e for e in checker.check_tree(self.root)))

    def test_bindcraft_fields_do_not_enter_campaign(self):
        path = self.root / "configs/bindcraft2/linear.template.json"
        data = json.loads(path.read_text())
        data["starting_pdb"] = "/path/to/inputs/receptor.pdb"
        path.write_text(json.dumps(data))
        self.assertTrue(any("mixed into" in e for e in checker.check_tree(self.root)))

    def test_missing_source_pin_is_rejected(self):
        path = self.root / "registry/methods.json"
        data = json.loads(path.read_text())
        data["methods"][0]["sources"][0]["commit"] = "main"
        path.write_text(json.dumps(data))
        self.assertTrue(any("full commit" in e for e in checker.check_tree(self.root)))

    def test_path_escape_in_allowlist_is_rejected(self):
        path = self.root / "registry/public_files.json"
        data = json.loads(path.read_text())
        data["files"].append("../private.json")
        path.write_text(json.dumps(data))
        self.assertEqual(checker.check_tree(self.root), ["invalid public file allowlist"])


if __name__ == "__main__":
    unittest.main()
