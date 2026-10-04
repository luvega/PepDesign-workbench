# PepDesign Workbench

A configuration and documentation workbench for peptide design: choose a method, prepare its environment and model assets, run its native workflow, and inspect the outputs.

[中文主页](README.md) · [Getting started](docs/getting-started.md) · [Method directory](docs/methods/README.md)

![Generic platform workflow](docs/assets/platform-overview.png)

## Methods

PepMLM · DiffPepBuilder · PepGLAD · Mirror-Peptidizer · PepMirror · AfCycDesign / ColabDesign · DexDesign / OSPREY3 · RFdiffusion + ProteinMPNN · **BindCraft** · **BindCraft2**.

BindCraft and BindCraft2 are separate integrations, with separate documentation, configurations, source references, environments and licensing notes. This workbench documents linear L-peptide and cyclic L-peptide workflows for BindCraft2.

The workbench provides native configuration templates and usage guidance. Compute is performed by the upstream tools in their own environments. Input sequences, structures and model weights are supplied by the user.

## Workflow

1. Choose a method by input type and required output.
2. Check its official source and license; create an isolated environment.
3. Obtain the required model assets and prepare your inputs.
4. Adapt the native settings and launch from the method's source directory.
5. Retain raw outputs and inspect sequence identity, geometry, connectivity, topology and chirality.

Sequence-only outputs, backbone models and full-atom complexes require different checks. Record L, D, mixed and unknown chirality explicitly; computational outputs still require experimental assessment of their biological properties.

## Repository checks

```bash
python scripts/check_public_tree.py
python -m unittest discover -s tests -v
```

These checks use only the Python standard library. They validate documentation, configuration and publication structure without running a design model.

See [setup and weights](docs/environments.md), [native templates](configs/README.md), [output checks](docs/quality-checks.md) and [licenses](docs/licenses.md). Upstream software and model licenses remain separate.
