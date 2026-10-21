# 08｜RFdiffusion＋ProteinMPNN：把骨架生成和序列设计接起来

**method ID：**`rfdiffusion-proteinmpnn`。**设计对象：**70—100 aa 蛋白 binder，长度明显大于十几残基短肽。**状态：**教材已编写，两个方法的环境、模型和步骤衔接尚未在本项目实跑。

## 阶段一：完整示范

### 本例要解决什么问题

使用 RFdiffusion 固定版 `examples/input_pdbs/insulin_target.pdb` 与 `examples/design_ppi.sh`。上游将其描述为 insulin receptor PPI 示例，保留输入 A1—150，指向 A59/A83/A91，再生成长度 70—100 的独立 binder。此处不补写未核验的 PDB 编号，也不把输入裁剪片段等同完整受体。

本例先生成一个新骨架，再为它设计序列。目标是学会连接这两个步骤，现有示例不能据此给出亲和力结论。

| 步骤 | 本例怎样做 | 为什么 |
|---|---|---|
| 1 目标 | 为指定受体表面生成一个新 binder 骨架并设计一条序列 | 明确这是两个方法和两个产物阶段 |
| 2 输入确认 | 核对实际文件中 A1—150 与三个热点 | 文件名不能证明组装体、编号或构建体身份 |
| 3 设置条件 | 填写 target contig、chain break 和 binder 长度 | `/0` 后的空格有分链语义，不能删去 |
| 4 原生运行 | 先 RFdiffusion，再按输出链指定 MPNN 的设计链 | 输出可重编号，原受体 A 不等于要设计的链 |
| 5 审阅结果 | 对照 PDB/TRB、序列文件及固定和设计位置，保留对应关系 | 同一骨架产生多条序列，仍只有一个骨架 |
| 6 决定下一步 | 链对应错误时先修复；其余候选按证据继续建模 | 完成这两步还不足以确认全原子结合模型 |

### 原生步骤与参数

以下命令从 RFdiffusion 固定版源码根目录运行。输入沿用上游示例，输出路径需改成自己的私有目录。本例把上游的 10 个骨架减到 1 个，沿用零噪声设置；这组设置只用于该示例，没有被证明普遍最优：

```bash
python scripts/run_inference.py \
  inference.input_pdb=examples/input_pdbs/insulin_target.pdb \
  inference.output_prefix=/path/to/course/rf-output/design \
  'contigmap.contigs=[A1-150/0 70-100]' \
  'ppi.hotspot_res=[A59,A83,A91]' \
  inference.num_designs=1 \
  denoiser.noise_scale_ca=0 denoiser.noise_scale_frame=0
```

生成后，先核对 PDB 和 TRB，再填写输出文件及 **实际 binder 链**，不能提前猜 A 或 B。之后切换到 ProteinMPNN 环境和源码目录，填写变量并运行：

```bash
python protein_mpnn_run.py \
  --pdb_path "$GENERATED_PDB" --pdb_path_chains "$BINDER_CHAIN" \
  --out_folder "$MPNN_OUTPUT" --num_seq_per_target 1 \
  --sampling_temp 0.1 --seed 42 \
  --path_to_model_weights "$MPNN_WEIGHTS" --model_name v_48_020
```

这些变量需要在两步之间填写。`MPNN_WEIGHTS` 是存放匹配权重文件的目录。FASTA 可能同时含原始序列和新生成序列，统计时要分开。用[两阶段人工记录](../../../configs/rfdiffusion-proteinmpnn/stages.template.json)保存设置；它不能直接启动两个方法。

### 修改指南

| 分类 | 条件表达 | 迁移时的要求 |
|---|---|---|
| 必须修改 | 输入、contig 的受体链/区间、hotspot、输出目录 | 用真实结构支持，保留裁剪与映射 |
| 必须核查 | `GENERATED_PDB`、`BINDER_CHAIN` 与固定/设计位置 | 根据 RF 实际输出填写，不能照搬原链 |
| 可以调整 | binder 长度、骨架数、每骨架序列数、MPNN 温度与 seed | 分别记录两步的计算量，以及每条序列对应哪个骨架 |
| 不能照抄 | A1—150、A59/A83/A91、零噪声设置 | 来源特定配方，不是所有靶标的默认 |

### 合成教学记录：怎样审阅

教学给定：骨架 X 的输出链 A 是新 binder、B 是受体；学生却把 MPNN 设计链填为 B。另一骨架 Y 的阶段映射正确，每骨架生成两条序列，其中一条原生评分更好。以上均无真实结构或序列。

X 选错了设计链，应保留错误记录，在新轮次修复。此前的相关序列分数不能用于选择 binder。

Y 的两条序列对应同一骨架，不能算两个独立骨架。较好的 MPNN 分数只说明序列与骨架的相容性，还需检查固定位置、回折和界面。补侧链、refold 或复合物预测都属于额外计算，不能记作这两步已完成的验证；原生序列与后续重设计序列也要分别记录。

**自我解释：**为什么阶段一的 A 链不一定等于阶段二的 A 链？骨架数和序列数怎样计数？为什么已有 PDB 和 FASTA 还不能自动写“全原子复合物验证通过”？

## 阶段二：补全练习

**练习 1｜最后决定。**沿用 X/Y 的核对结果，说明先修复什么、可以保留什么，以及下一步和理由。

**练习 2｜审阅与决定。**输入和两步衔接已核实。同一骨架的三条序列原生分数很好，但后续复合物预测出现两种 pose。请完成步骤 5—6：序列分数和 pose 各回答什么问题？怎样记录分歧并提出比较？不能按三票对两票决定。

**练习 3｜配置及后续。**已给新受体可用的链区间和位点表，要求比较两种 binder 长度。请完成步骤 3—6：填写 contig，安排输出链核对，说明每骨架序列怎样计数、两组结果怎样比较。尚无输出时，只写核查办法，不猜链 ID。

## 阶段三：独立迁移

1. 用另一公开受体片段设计一份两阶段研究方案，解释为何保留/裁剪某部分、哪些位点固定，以及设计链怎样确定。
2. 将自己的问题填入[任务卡](../common/research-task-card.md)和[迁移模板](../common/project-transfer.md)。若目标是很短的环肽，先判断当前路线是否适用；缩短长度不能代替环化设置和检查。

能追踪一个骨架对应的多条序列后，可进入独立任务。若仍把受体链当作设计链，先回看 PDB/TRB 对应关系。

## 来源与后续验收

- [RF 固定 PPI 示例](https://github.com/RosettaCommons/RFdiffusion/blob/2d0c003df46b9db41d119321f15403dec3716cd9/examples/design_ppi.sh)。
- [ProteinMPNN 固定版本](https://github.com/dauparas/ProteinMPNN/tree/8907e6671bfbfc92303b5f79c4b5e6ce47cdef57)、[两阶段方法说明](../../methods/rfdiffusion-proteinmpnn.md)。
- 待验收：两个独立环境/权重、输入编号、输出链/TRB 映射、FASTA 记录解析、最小两阶段运行与后续建模能力。

[教师参考答案](../teacher-guide.md#rfdiffusion-proteinmpnn) · [返回教学导航](../README.md)
