# 03｜PepGLAD：从参考复合物提取口袋，再联合设计序列和结构

**method ID：**`pepglad`。**产物：**全原子肽及复合物、原生摘要。**状态：**教学文档完成；未在本项目运行口袋提取、生成或 OpenMM relax，环境与 checkpoint 待核查。

## 阶段一：完整示范

### 本例要解决什么问题

本例使用官方 `assets/1ssc_A_B.pdb`。**1SSC** 是半合成 RNase A 结构：A 链为 112 aa 片段，B 链为 11 aa 片段。我们用 A 作 target，用参考 ligand B 定义口袋。这个片段体系适合学习复合物输入和联合设计；换成完整独立受体时，要重新判断是否适用。

本例选择生成 15 aa 新肽，长度不同于原 B 链，也不能据此认为新肽保留酶功能。这里使用 codesign，同时设计序列与结构；固定序列后生成构象是另一种任务。

| 步骤 | 本例怎样做 | 为什么 |
|---|---|---|
| 1 目标 | 在参考 B 定义的区域设计 15 aa 新肽 | B 用于定位，新肽才是待研究候选 |
| 2 输入确认 | 核对上游 A/B 工作文件及实际编号，保存参考 B | 参考 ligand 可定义位点，不是生成结果 |
| 3 设置条件 | 生成 pocket JSON，设 `length_min=15,length_max=16` | 本 API 不包含长度上限，15/16 才表示固定 15 aa |
| 4 原生运行 | `api.detect_pocket` 后调用 `api.run --mode codesign` | 方法需要实际口袋索引和对应 checkpoint |
| 5 审阅结果 | 对照 `summary.jsonl` 和 PDB，检查序列、原子、手性及修复前后变化 | 全原子文件仍可能存在化学问题 |
| 6 决定下一步 | 先处理输入或几何异常，再决定是否增加样本或比较结构 | 生成概率和几何只能提供计算证据 |

### 原生配置与操作

以下命令在已准备的固定版源码目录执行；路径为待替换占位，不代表文件已存在：

```bash
python -m api.detect_pocket \
  --pdb /path/to/course/1ssc_A_B.pdb \
  --target_chains A --ligand_chains B \
  --out /path/to/course/1ssc-pocket.json
python -m api.run --mode codesign \
  --pdb /path/to/course/1ssc_A_B.pdb \
  --pocket /path/to/course/1ssc-pocket.json \
  --out_dir /path/to/course/pepglad-output \
  --length_min 15 --length_max 16 --n_samples 1 --gpu 0
```

固定版按其默认 Cβ 距离规则提取口袋，记录时注明这是该方法的规则，不将它用作通用物理阈值。JSON 中的残基按 author residue number 和插入码表示，不是从 1 开始的数组下标；没有插入码时保留一个空格。口袋残基应由实际结构取得。

[原生方法说明](../../methods/pepglad.md)中，该入口读取 `checkpoints/codesign.ckpt`，没有 `--seed` 或 `--ckpt` 选项。原生流程包含 relax，运行时要记录其耗时和结构变化。

### 修改指南

| 分类 | 字段／操作 | 迁移时的检查 |
|---|---|---|
| 必须修改 | `--pdb`、`--target_chains`、`--ligand_chains`、`--pocket`、`--out_dir` | 新受体、真实参考 ligand 与实际编号 |
| 可以调整 | `--length_min`、`--length_max`、`--n_samples` | 上限排除；固定长度 L 用 L 与 L+1 |
| 不能照抄 | 1SSC A/B 角色、默认口袋范围 | 自己的参考链必须真实存在，角色由问题决定 |
| 需另核实 | 固定序列构象模式、非标准化学要求 | 不把 codesign 的输入和产物默认等同其他模式 |

### 合成教学记录：怎样审阅

另设一个两候选练习批次。A、B 均有 PDB 和摘要，长度都是 15。A 在 relax 后有一个位点的坐标手性不符合要求。练习给定 B 的手性和骨架连通性符合要求，但尚未比较不同输入准备方式下是否稳定。这些条件为人工设定，没有真实坐标或检查报告。

先定位 A 的异常残基，对照生成和修复前后的文件，查明问题来自生成、残基对应还是 relax，并保留原件。

B 可保留做小规模探索。题目给定的几何检查不构成实测结合或独立结构验证。处理自己的项目时，如果只有摘要而没有坐标，应把手性和几何记为“未检查”。

**自我解释：**为什么 `15/16` 请求的是长度 15？参考 B 的作用与新设计肽有什么不同？为什么一次 relax 后的好分数不能取代原子检查？

## 阶段二：补全练习

**练习 1｜最后决定。**前五步及 A/B 审阅已给出。你会先补哪一次检查？什么结果会改变你的判断？

**练习 2｜审阅与决定。**要求固定 12 aa，配置为 `length_min=12,length_max=13`。合成摘要写长度 12，但 PDB 只能对应到 11 个残基。请完成步骤 5—6：核对哪些原始记录、怎样计数、暂时无法确认哪些性质？

**练习 3｜配置及后续。**另一份参考复合物的 A/B 链已核实。请为固定 12 aa 设计完成步骤 3—6：提取 pocket、填写长度参数、安排输出检查，再决定怎样继续。参数须来自本接口，不能增加 `--seed`。

## 阶段三：独立迁移

1. 选另一个有参考肽的公开受体复合物，说明怎样用参考链定义口袋，怎样分清参考肽和新输出，以及怎样记录实际得到的产物类型。
2. 将自己的课题写进[任务卡](../common/research-task-card.md)和[迁移模板](../common/project-transfer.md)。没有参考 ligand 时，另行提出有依据的 pocket 定义，说明其假设与检查。

能独立完成这些检查后，可进入自己的项目。若仍混淆残基编号和数组序号，先练习将口袋记录与 PDB 逐项对应。

## 来源与后续验收

- [固定上游与使用例](https://github.com/THUNLP-MT/PepGLAD/tree/bad015ca50c312a89482adb5220c3d907f13df5c)、[口袋脚本](https://github.com/THUNLP-MT/PepGLAD/blob/bad015ca50c312a89482adb5220c3d907f13df5c/api/detect_pocket.py)、[1SSC 结构身份](https://www.rcsb.org/structure/1SSC)。
- 待验收：工作文件、口袋结果、checkpoint 实际路径、环境、relax、最小调用与真实原子级检查。

[教师参考答案](../teacher-guide.md#pepglad) · [返回教学导航](../README.md)
