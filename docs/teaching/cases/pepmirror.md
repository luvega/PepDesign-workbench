# 05｜PepMirror：从参考复合物定义口袋，核对模板与模型

**method ID：**`pepmirror`。**任务：**用参考复合物和原生线性肽模板生成候选，后续可扩展 D 肽镜像设计。**状态：**教材已编写，环境、checkpoint、镜像处理和生成流程尚未在本项目验收。

## 阶段一：完整示范

### 本例要解决什么问题

采用官方 `api/demo/7mdp_chothia.pdb`。**7MDP** 是 KRAS G12C 复合物，A 链为 KRAS，H/I 为参考抗体重/轻链。原生示例 `tgt_chains: [A]`、`lig_chains: [HI]` 用参考 Fab 定义区域；这里的 ligand 并非一条天然短肽。

使用的是 Chothia 处理后的工作文件，编号未必与原始 PDB 相同。本例在参考区域生成线性肽候选；新肽是否具有原抗体或其他配体的活性和作用机制，仍需研究。

| 步骤 | 本例怎样做 | 为什么 |
|---|---|---|
| 1 目标 | 在参考区域提出 10—11 aa 线性肽 | 对应原生 `size_max` 排除上限，不是 10—12 aa |
| 2 输入确认 | 核查实际 A/H/I 工作链及参考角色 | 抗体用于口袋条件，不是新候选，也不能凭空补链 |
| 3 设置条件 | 使用原生 `LinearPeptide`，填写 axial 配置 | 特征设置须与 checkpoint 匹配 |
| 4 原生运行 | 将 YAML 交给 `api.generate` | 此处 YAML 是程序配置 |
| 5 审阅结果 | 检查长度、位置、手性、几何和产物类型 | 拓扑和手性要由实际输出确认 |
| 6 决定下一步 | 先查配置与模型是否匹配，再比较候选 | 错配模型的分数不能直接比较 |

### 原生配置与调用

下面将官方 demo 缩为单样本，并指定与所选模型对应的轴向设置。这是原生 YAML 配置；文件路径、模型文件及兼容性仍待服务器检查。

```yaml
dataset:
  pdb_paths:
    - /path/to/course/7mdp_chothia.pdb
  tgt_chains:
    - A
  lig_chains:
    - HI
templates:
  - class: LinearPeptide
    size_min: 10
    size_max: 12
batch_size: 1
n_samples: 1
axial_type: commutator
axial_position: Both
```

本例 `HI` 表示参考链 H 和 I 的集合，并非一条名为 HI 的 PDB 链。保留该版本解析器要求的写法，不改成其他多复合物列表格式。环境就绪后，在源码目录调用：

```bash
python -m api.generate \
  --config /path/to/course/pepmirror.yaml \
  --save_dir /path/to/course/pepmirror-output \
  --gpu 0 \
  --ckpt /path/to/models/pepmirror_commutator_both_v1.ckpt
```

权重路径目前是占位符，后续要核对文件及其特征配置。详见[原生方法](../../methods/pepmirror.md)和[通用模板](../../../configs/pepmirror/linear.template.yaml)。

### 修改指南

| 分类 | 原生表达 | 自己项目怎样改 |
|---|---|---|
| 必须修改 | `pdb_paths`、`tgt_chains`、`lig_chains`、输出路径 | 对应自己的真实复合物与口袋来源 |
| 可以调整 | `size_min`、`size_max`、`n_samples`、`batch_size` | 固定长度 L 用 L 与 L+1，规模需资源依据 |
| 必须匹配 | `axial_type`、`axial_position` 与 `--ckpt` | 读取模型实际配置，不只改 checkpoint 名称 |
| 不能照抄 | H/I 参考链、Chothia 编号、`LinearPeptide` | 没有参考 ligand 的受体需另行定义口袋，不虚构链 |

扩展 D 肽设计时，用原生 `scripts/mirror_pdb.py` 准备镜像输入；生成后将整个复合物镜像返回，再检查最终受体和候选。L、D、mixed 或 unknown 要根据坐标判断。环化也需要实际处理，重命名文件不会改变线性产物。

### 合成教学记录：怎样审阅

教学给定：A 使用本例匹配特征，产生长度 10 的候选摘要；B 的 YAML 改成另一种 axial 设置，但仍加载原 checkpoint，得到更好看的原生数值。没有真实输出。

先查 B 的设置是被接口拒绝、忽略，还是被错误使用。确认前，它的分数不能说明优于 A。

A 可保留探索，但只有摘要时，手性和几何仍为“未检查”。落在参考 Fab 定义的区域，也不能证明新肽具有抗体的结合或抑制作用。

**自我解释：**为什么参考 H/I 与候选链不能混同？为什么 `[10,12)` 只含两个整数长度？为什么只换文件名不能切换到环肽或 D 肽？

## 阶段二：补全练习

**练习 1｜最后决定。**A/B 的问题已找到。修复 B 前后应保存哪些记录？之后先做什么，为什么？

**练习 2｜审阅与决定。**配置和模型已匹配。合成摘要称候选落在参考 Fab 定义的区域，但 D 肽扩展流程缺少整个复合物镜像返回后的文件。请完成步骤 5—6：目前能确认什么？还缺什么？怎样补回文件和记录？

**练习 3｜配置及后续。**另一份复合物中，target 为 A，参考 ligand 为 B。要求固定 13 aa。请完成步骤 3—6：填写链和长度，核对模型匹配，安排结果审阅。参考链按新文件填写；口袋条件不能当作实测亲和力。

## 阶段三：独立迁移

1. 对一个只有受体、没有参考 ligand 的公开对象，提出有依据的口袋准备途径，说明哪项原生输入需要另行准备；不要补一条假参考链。
2. 将自己的项目填入[任务卡](../common/research-task-card.md)和[迁移模板](../common/project-transfer.md)。若使用镜像或改变拓扑，另列新增操作和检查。

能说明输入、模型和最终坐标的来源后，可进入迁移任务；只会复制 YAML 还不够。

## 来源与后续验收

- [固定上游](https://github.com/YZY010418/PepMirror/tree/41cb31f3974d91e1a2ca88f0db060405833e4a9c)、[原生 demo 配置](https://github.com/YZY010418/PepMirror/blob/41cb31f3974d91e1a2ca88f0db060405833e4a9c/api/demo/config.yaml)、[7MDP 身份](https://www.rcsb.org/structure/7MDP)。
- 待验收：实际工作 PDB/链、特征与 checkpoint、原生 parser、生成与后处理、镜像扩展及最终坐标检查。

[教师参考答案](../teacher-guide.md#pepmirror) · [返回教学导航](../README.md)
