# 10｜BindCraft2：针对受体设计环肽并检查闭环

**method ID：**`bindcraft2`。**本例：**hPD-L1 条件下的 cyclic L 肽设计。**状态：**教学文档完成；独立环境、模型与真实 campaign 未验收。BindCraft2 与 BindCraft 的输入格式、依赖和许可分别维护。

## 阶段一：完整示范

### 本例要解决什么问题

采用上游 `settings/target/structures/hPDL1.pdb` 及对应目标定义：人 PD-L1，A 链，热点 **54、56、66、115**。这些热点来自该工作构建体；不能直接搬到任意另一份 PD-L1 编号。

本例针对 hPD-L1 设计头尾环化的 L 肽，使用 `modality="cyclic_peptide"` 选择原生路线。生成后还要检查闭环、L 手性及其他要求。这里有受体，与 AfCycDesign 无受体 fixbb 例回答的问题不同。

| 步骤 | 本例怎样做 | 为什么 |
|---|---|---|
| 1 目标 | 在该 hPD-L1 表面设计 cyclic L 肽 | 环肽设置、输出几何和实测结合需分别判断 |
| 2 输入确认 | 核对实际目标文件、A 链和四个热点 | 相同蛋白名不保证相同构建体/编号 |
| 3 设置条件 | 从最小 cyclic preset 开始，设置小规模 campaign | 旧的详细配置可能覆盖 preset，合并前要逐项核对 |
| 4 原生运行 | 用独立 `bindcraft.cli design` 接收 campaign JSON | 不复用 BindCraft 的三文件格式 |
| 5 审阅结果 | 对照轨迹、refold、rank，并检查闭环原子 | 原生过滤未必检查了题目要求的全部性质 |
| 6 决定下一步 | 先补闭环检查或修复，再决定是否继续 | 软件接受不能给出实验亲和力 |

### 原生 campaign 教学例

下面用官方 hPDL1 输入填写现有 cyclic 模板。路径、设备和模型文件待教师配置，长度范围沿用所引 cyclic preset；其他方法的范围含义需另查。

```json
{
  "modality": "cyclic_peptide",
  "targets": [
    {
      "name": "hPDL1_course",
      "target_path": "/path/to/tools/BindCraft2/settings/target/structures/hPDL1.pdb",
      "chains": "A",
      "hotspots": "54,56,66,115"
    }
  ],
  "binder_lengths": [7, 16],
  "campaign_seed": 42,
  "number_of_final_designs": 1,
  "max_trajectories": 1,
  "resume": false,
  "auto_multi_gpu": false,
  "design_workers": 1,
  "gpu_ids": [0],
  "project_folder": "/path/to/course/bindcraft2-cyclic"
}
```

在已准备的独立环境与固定源码目录运行原生入口：

```bash
python -m bindcraft.cli design /path/to/course/bindcraft2-cyclic.json
```

本阶段尚未安装、获取权重或运行设计。该版本没有文档化的独立 `bindcraft preflight` CLI。后续需将 `campaign_seed` 连同模型、环境和全部结果一起记录；仅有 seed 不足以证明可复现或稳定。

### 修改指南

| 分类 | 字段／操作 | 自己项目怎样改 |
|---|---|---|
| 必须修改 | `targets`、链/热点、`project_folder` | 真实构建体与全新轮次目录 |
| 可以调整 | `binder_lengths`、采样与接受目标 | 明确目的与资源；接受数可能为零 |
| 分别记录 | `number_of_final_designs` 与 `max_trajectories` | 前者是期望接受数，后者是最多轨迹数，都不是实测成功率 |
| 输出后检查 | modality 与实际产物闭环/手性 | 当前模板尚未建立 D/mixed 支持 |
| 不能照抄 | BindCraft 的 `starting_pdb`、`design_path`、advanced/filter 文件 | 本方法使用独立 campaign 格式 |

本版本默认 closure filter 没有设置有限的接受阈值。因此，候选进入 ranked 后仍要检查头尾连接和局部几何，注明规则来源及涉及的原子，不能自行填一个“通用阈值”。最多 1 条轨迹只是教学规模，可能零接受，耗时也尚未确定。

### 合成教学记录：怎样审阅

人工给定：某次独立教学批次中 A 被原生接受，但闭环几何尚未检查；B 因一个已声明的原生筛选项拒绝，保留原拒绝原因。没有真实文件或结果。

A 应先补原子检查，目前闭环状态为“未检查”。B 则要按拒绝原因决定修复、少量探索或停止，不能因为软件拒绝就认定实测不结合。

若 1 条轨迹最终零接受，就报告 1 条轨迹、0 接受。“期望得到 1 个”只是设置，不是结果。

**自我解释：**为何 cyclic modality 不等于闭环检查完成？为什么不能把 BindCraft 的 basic JSON 直接换成这里的输入？为什么不同长度/预算/过滤下的接受数量不能直接比较方法优越性？

## 阶段二：补全练习

**练习 1｜最后决定。**A/B 的检查范围已给。请选一项后续操作，说明它能改变什么判断。

**练习 2｜审阅与决定。**配置和目标已核实。合成记录中，首轮 1 次轨迹、0 接受；第二轮改了过滤规则，1 次轨迹、1 接受。请完成步骤 5—6：保存哪些记录？为什么不能直接称为成功率提高或独立验证？两轮还能怎样比较？

**练习 3｜配置及后续。**用相同 hPDL1 工作输入比较线性肽和环肽。请完成步骤 3—6：分别设置原生 modality，匹配长度和预算，或解释差异；列出原生过滤之外还要做的性质检查。更改文件名不能替代路线设置。

## 阶段三：独立迁移

1. 选另一个公开受体，填写 target 和长度，并安排产物检查。没有热点时，说明是有意不限定位置，还是尚缺资料。
2. 将自己的项目填入[任务卡](../common/research-task-card.md)和[迁移模板](../common/project-transfer.md)。保留线性/环肽或原生/重设计分支，在得到相应证据前不声称满足全部功能条件。

能分清“改了筛选规则”和“产物性质改变”后，可进入迁移任务。决定可以与教师不同，但要说明理由。

## 来源与后续验收

- [固定上游](https://github.com/PacesaLab/BindCraft2/tree/a8d0f2002df373842b86a3c20c5a060c5cfdf980)、[hPDL1 目标](https://github.com/PacesaLab/BindCraft2/blob/a8d0f2002df373842b86a3c20c5a060c5cfdf980/settings/target/hPDL1.json)、[线性/环肽原生示例](https://github.com/PacesaLab/BindCraft2/blob/a8d0f2002df373842b86a3c20c5a060c5cfdf980/examples/README.md)、[方法说明](../../methods/bindcraft2.md)。
- 预期原生产物在 `1_Trajectories/`、`2_Refolded/`、`3_Ranked/`，含 mmCIF、CSV 与 `campaign_metadata.json`；不能由目录名字推断所有候选均已跑完 refold。
- 待验收：独立环境/资产、target 映射、最小 campaign、实际分母和闭环/手性检查。没有本机模型结果。

[教师参考答案](../teacher-guide.md#bindcraft2) · [返回教学导航](../README.md)
