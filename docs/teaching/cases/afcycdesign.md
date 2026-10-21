# 06｜AfCycDesign：单体环肽骨架上的序列设计

**method ID：**`afcycdesign`。**任务：**为无受体的单体环肽骨架设计序列。**状态：**教材已编写；服务器 Notebook/API、AlphaFold 参数和生成流程待验收，目前没有可直接使用的一键 CLI。

## 阶段一：完整示范

### 本例要解决什么问题

固定版 `af_cyc_design.ipynb` 的 fixbb 例使用 **7M28 A 链**。RCSB 将其登记为 PawL-derived peptide PLP-22，是 7 aa 环肽的溶液 NMR 结构。本例为这条骨架设计相容序列，没有受体，因此只讨论单体结构，不能判断受体结合。

准备 NMR 输入时，要选择并记录 model、链和原子。固定骨架的长度由输入决定；改动 `binder_len` 不能把本例变成受体结合设计。

| 步骤 | 本例怎样做 | 为什么 |
|---|---|---|
| 1 目标 | 在 7M28 的选定 A 链骨架上做序列设计 | 这是 fixbb 问题，尚无靶标结合终点 |
| 2 输入确认 | 保留本地副本、NMR model 与 A 链，核查 7 个残基 | 不把数据库条目、多构象和工作文件视为同一对象 |
| 3 设置条件 | 选 `protocol="fixbb"`，加入 `add_cyclic_offset` | 这会改变模型中的相对位置表示，不能证明已形成化学键 |
| 4 原生运行 | 在已准备的 Notebook/API 环境进行优化并导出序列/PDB | notebook 含安装和下载单元，需先适配服务器 |
| 5 审阅结果 | 检查序列、骨架变化、头尾原子、闭环和几何 | pLDDT 等模型指标不能代替头尾原子检查 |
| 6 决定下一步 | 几何合理时继续研究单体构象；异常先查输入和表示 | 单体结果不能证明结合或合成成功 |

### 原生操作与输入准备

教师需先准备固定版 ColabDesign、本地参数和同版 notebook 中的 `add_cyclic_offset`。原始 setup 包含安装、参数下载、Colab 上传和联网获取 PDB，本阶段**尚未执行这些单元**。服务器适配和辅助运行代码留待后续。

下面的 API 片段需要先配置 `model_data_root`、`pdb_path` 和 `output_pdb`，并载入固定 notebook 中的 `add_cyclic_offset`，不能独立运行：

```python
af_model = mk_afdesign_model(protocol="fixbb", data_dir=model_data_root)
af_model.prep_inputs(pdb_filename=pdb_path, chain="A")
add_cyclic_offset(af_model, offset_type=2)
af_model.restart()
af_model.design_3stage()
af_model.save_pdb(output_pdb)
seqs = af_model.get_seqs()
```

实际运行时再记录优化次数、模型和资源。详见[方法说明](../../methods/afcycdesign.md)。[notebook 输入 JSON](../../../configs/afcycdesign/notebook-inputs.template.json)供人工填写，并不是传给 `afcycdesign.py` 的原生配置。

### 修改指南

| 分类 | 原生设置／操作 | 迁移时怎样处理 |
|---|---|---|
| 必须修改 | PDB、链、选定构象、参数与输出位置 | 从自己环肽骨架取得真实输入 |
| 可以调整 | 优化策略与采样 | 说明改变的科学问题与预算，保留全部相关结果 |
| 不能照抄 | 7M28 的链、长度与 model 选择 | 其他骨架不保证也为 7 aa 或相同化学拓扑 |
| 需另做准备 | 针对受体设计环肽 | 需要接入并验证 binder API、受体和对应 cyclic offset，不能直接套用本例 fixbb |

同一 notebook 还有无靶标从头生成的 hallucination 分支，固定版示例长 13 aa。它与固定骨架设计使用不同协议，长度和排除残基等条件要按各自协议填写。

### 合成教学记录：怎样审阅

人工给定：A 的模型 confidence 较好，但导出的头尾邻接原子不完整，无法检查闭环；B 的模型 confidence 稍低，教学条件给定其原子完整且声明的闭环几何检查通过。无真实序列、坐标或检查数值。

A 的闭环状态应写“未检查”，先查导出过程和原子完整性。较高 confidence 不能补足缺失的原子。

B 可继续用于单体几何研究，但还不能判断溶液中各构象的比例、可合成性或结合。记录检查时，要说明涉及哪些原子、采用什么规则；本题给定的结果不能记作自己的测量。

**自我解释：**为什么本例不需要受体？为什么 cyclic offset 不是化学键的实验确认？改变 fixbb 长度需要重新考虑什么输入，而非只改一个数字？

## 阶段二：补全练习

**练习 1｜最后决定。**A/B 前五步已给出。请选一次后续检查并解释理由，说明它能解决什么问题。高 confidence 不能替代缺失检查。

**练习 2｜审阅与决定。**配置和输入已核对。合成导出记录称链长 7，但末端有多余封闭基团，现有检查只看 Cα 是否邻近。请完成步骤 5—6：这些检查能说明什么？还要查看哪些原子、连接和化学处理？

**练习 3｜配置及后续。**已给一份明确的 9 aa 单体环肽骨架。请完成步骤 3—6：选择 protocol 和固定来源的 cyclic offset，安排产物检查并决定下一步。保持无受体设定，不能用 `binder_len=9` 代替 fixbb 骨架输入。

## 阶段三：独立迁移

1. 为一个新的公开单体环肽骨架写固定骨架设计方案，说明构象选择、环化类型和输出核查；与无靶标从头生成作概念比较。
2. 用自己的课题填写[任务卡](../common/research-task-card.md)和[迁移模板](../common/project-transfer.md)。如果真正终点是受体结合，说明需新增哪些任务或为何改选 BindCraft2 等适用路线。

能分清单体几何、受体结合和实测闭环后，可进入自己的项目；分不清时，先重新说明本例输入和 protocol 的作用。

## 来源与后续验收

- [固定环肽 notebook](https://github.com/sokrypton/ColabDesign/blob/e31a56fe1d9b4de25c8697f3a28b75892941cc72/af/examples/af_cyc_design.ipynb)、[独立 binder notebook](https://github.com/sokrypton/ColabDesign/blob/e31a56fe1d9b4de25c8697f3a28b75892941cc72/af/examples/peptide_binder_design.ipynb)、[7M28 身份](https://www.rcsb.org/structure/7M28)。
- 待验收：实际 ColabDesign/API 与参数版本一致性、本地输入、服务器适配、最小优化、最终原子/闭环/手性检查。

[教师参考答案](../teacher-guide.md#afcycdesign) · [返回教学导航](../README.md)
