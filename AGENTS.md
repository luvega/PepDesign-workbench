# PepDesign Workbench maintenance

This repository contains the public peptide-design workbench: generic documentation, native configuration templates, method-source metadata and explanatory images.

- Keep BindCraft and BindCraft2 as independent method IDs, directories, source references and environments.
- Use Chinese reader-facing documentation by default; keep native commands and method names unchanged.
- Publish only generic configuration and usage material. Keep user inputs, sequences, structures, run logs, study plans and computed outputs outside this repository.
- Do not vendor upstream code, dependencies, weights or credentials. Link to official sources and retain their separate licensing requirements.
- Verify native parameters against the referenced upstream revision. Identify notebook/API workflows explicitly; do not invent a unified design CLI.
- Treat source references as configuration references, not installation or scientific validation claims.
- Use grilling for new scope decisions. Confirm material scope changes; continue ordinary work within confirmed scope without repeat approval.
- Do not run installs, asset downloads or design calculations merely to validate the documentation.
- Check `python scripts/check_public_tree.py`, `python -m unittest discover -s tests -v` and `git diff --check` before publication.
