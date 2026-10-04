# AfCycDesign / ColabDesign

使用 AlphaFold / ColabDesign 的设计 API，通过 cyclic offset 表达环肽拓扑。

官方来源：[sokrypton/ColabDesign](https://github.com/sokrypton/ColabDesign/tree/e31a56fe1d9b4de25c8697f3a28b75892941cc72)。此源码的 `LICENSE.txt` 为 Beer-Ware Revision 42，AlphaFold 参数和依赖条款分别核对。按固定版本安装 ColabDesign，并将官方 AlphaFold 参数放在独立模型目录的 `params/` 下。

## notebook / API 入口

原生入口是 `af/examples/af_cyc_design.ipynb`，其中定义 `add_cyclic_offset`；受体条件 peptide binder API 见 `af/examples/peptide_binder_design.ipynb`。没有独立官方 `afcycdesign.py` CLI。

受体条件环肽接入需要组合两个 notebook 的逻辑：

1. 使用 `mk_afdesign_model(protocol="binder", data_dir=...)`。
2. 通过 `prep_inputs(pdb_filename=..., chain=..., binder_len=..., hotspot=...)`准备自己的受体输入。
3. 将固定版环肽 notebook 的 `add_cyclic_offset` 逻辑应用于 binder model。
4. 调用原生 `design_3stage` 等优化 API，使用 `get_seqs()`、`save_pdb()` 导出。

上述是接入路线说明，需要用户准备 notebook / API 适配；本工作台没有声称存在现成的一键官方 CLI。[参数记录模板](../../configs/afcycdesign/notebook-inputs.template.json)仅用于填写输入，不是原生程序可直接读取的配置。

不同 notebook 可能安装不同 ColabDesign 版本，应固定实际使用的源码并核对 API。输出主要是 L 肽体系中的环化设计模型；检查头尾闭合几何、原子完整性与实际手性。cyclic offset 不能证明合成闭环或实验构象。
