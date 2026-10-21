# 09｜BindCraft：记录尝试数，读懂接受结果

**method ID：**`bindcraft`。**本例：**受体条件蛋白／迷你蛋白 binder，长度 65—150 aa。**状态：**教学文档完成；未安装或运行 BindCraft，完整 advanced/filter、环境和实际资源待核查。

## 阶段一：完整示范

### 本例要解决什么问题

使用官方 `example/PDL1.pdb` 和 `settings_target/PDL1.json`。靶标是 **PD-L1** 工作构建体，链 A，热点 56。原例要求得到 100 个接受候选，本例改为 1 个，便于学习配置和结果解释。但“接受 1 个”并不保证只尝试一次，实际耗时仍未知。

先按工作文件核对结构状态、裁剪、组分和编号。“PD-L1”这个名称不能说明糖基化是否完整，也不能证明候选有 blocking 活性。本例设计 65—150 aa 蛋白 binder，与短线性肽需要的条件不同。

| 步骤 | 本例怎样做 | 为什么 |
|---|---|---|
| 1 目标 | 在声明区域提出蛋白 binder 计算候选 | 先说明当前是计算设计和选择，不是实测抑制 |
| 2 输入确认 | 核查 PDL1 工作文件、A 链、56 位点及构建体 | 来源热点须落在实际使用输入上 |
| 3 设置条件 | basic 填目标和长度，另选完整 advanced 与 filters | 三种文件各有用途，几个 basic 字段不能替代完整预设 |
| 4 原生运行 | 使用三文件入口，记录实际尝试数和时间 | 想得到几个候选，不能代替计算预算 |
| 5 审阅结果 | 对照轨迹、MPNN 和最终表，保留拒绝及各条序列 | 只看最终表会遗漏未接受的尝试 |
| 6 决定下一步 | 根据记录继续、修复或停止 | 零接受时仍可分析原因并作出决定 |

### 原生配置与步骤

以下是修改了路径与接受数量的 **原生 basic JSON 教学例**；路径待填，未在本服务器执行：

```json
{
  "design_path": "/path/to/course/bindcraft-output/",
  "binder_name": "PDL1_course",
  "starting_pdb": "/path/to/tools/BindCraft/example/PDL1.pdb",
  "chains": "A",
  "target_hotspot_residues": "56",
  "lengths": [65, 150],
  "number_of_final_designs": 1
}
```

从固定版上游选择完整的蛋白 binder advanced/filter 预设，再按[原生配置准备](../../../configs/bindcraft/README.md)填写自己的工作副本。环境、AlphaFold/PyRosetta 等资产与实际运行额度先由教师核查，不在这里执行安装。

```bash
python -u bindcraft.py \
  --settings /path/to/course/bindcraft-basic.json \
  --filters /path/to/course/bindcraft-filters.json \
  --advanced /path/to/course/bindcraft-advanced.json
```

advanced 中的 `max_trajectories` 只统计保存到 `Trajectory/Relaxed/` 的轨迹，可能漏掉早期失败。因此要另记总尝试数和最长运行时间。原生 CLI 没有 `--seed`。资源和停止条件确定前，运行状态保持待执行。

### 修改指南

| 分类 | 字段／操作 | 自己项目怎样改 |
|---|---|---|
| 必须修改 | `starting_pdb`、`chains`、热点、`design_path`、名称 | 真实靶标构建体、链和输出轮次 |
| 可以调整 | `lengths`、接受目标和完整 advanced/filter | 按设计对象解释；短肽需要相应原生预设 |
| 必须另记 | 实际尝试、早期失败、停止时间 | 总尝试数包括未保存的失败，不能只数接受者或已保存轨迹 |
| 不能照抄 | PD-L1 热点、100 个接受、Colab 路径 | 都不是自己问题与服务器的默认事实 |

### 合成教学记录：怎样审阅

人工构造：记录了 8 次实际尝试，3 次早期失败；余下 5 条有 relaxed 轨迹，其中 1 条进入最终接受表。假设流程记录完整且本轮没有实测结合。

分别报告：目标接受数 1，实际尝试数 8，已保存轨迹数 5。1/8 是这次软件接受比例，不能称为 binder 实验命中率；最终表的一行也不表示只尝试了一次。

下一步先检查接受者所用输入、准备过程、序列来源和几何，再决定是否做后续比较。扩大采样前，还应解释早期失败的原因。

**自我解释：**为什么接受目标 1 不保证一次尝试？为什么原生 max_trajectories 不能覆盖所有失败？为什么同一骨架的多 MPNN 序列不能作为多个独立骨架验证？

## 阶段二：补全练习

**练习 1｜最后决定。**上述计数和审阅已给出。你会先做哪一次比较，或为什么停止？说明它要解决什么问题。

**练习 2｜审阅与决定。**配置和流程记录已给。合成批次有 6 次有效尝试、0 接受，均被同一个几何规则拒绝；按相同方式准备的已知兼容对照也被拒绝。请完成步骤 5—6：怎样检查规则是否适用？保存哪些失败记录？若用该对照调过规则，为什么不能再算独立验证？

**练习 3｜配置及后续。**已给另一受体工作文件、链和有来源的热点。请完成步骤 3—6：修改 basic，解释完整预设的选择，安排计算预算、运行记录和结果审阅。尚无运行数据时，不承诺得到候选的时间。

## 阶段三：独立迁移

1. 为另一个公开蛋白受体编写 binder 设计卡，解释蛋白/迷你蛋白与短肽预设的差异，并说明怎样记录总尝试数和各阶段数量。
2. 用自己的课题填写[任务卡](../common/research-task-card.md)和[迁移模板](../common/project-transfer.md)。若想与 BindCraft2 比较，明确方法、长度、输入、预算和过滤不同，不能直接按最终数量排优劣。

能分清早期失败、保存轨迹和接受数后，可进入迁移任务；仍混淆时，先补做一组计数。

## 来源与后续验收

- [固定上游](https://github.com/martinpacesa/BindCraft/tree/b971db42ba6e091afab63ccb30ae02215150a990)、[官方 PD-L1 basic](https://github.com/martinpacesa/BindCraft/blob/b971db42ba6e091afab63ccb30ae02215150a990/settings_target/PDL1.json)、[方法说明](../../methods/bindcraft.md)。
- 原生产物包括 PDB、`trajectory_stats.csv`、`mpnn_design_stats.csv`、`final_design_stats.csv`；需与实际原始记录关联。
- 待验收：输入/资产/环境、完整预设、真实停止额度、最小轨迹和输出解析。尚无本服务器候选或成功率。

[教师参考答案](../teacher-guide.md#bindcraft) · [返回教学导航](../README.md)
