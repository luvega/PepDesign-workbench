# 02｜DiffPepBuilder：结构与位点条件下设计结合肽

**method ID：**`diffpepbuilder`。**任务：**根据受体结构和选定位点设计 15 aa 肽。**状态：**教材已编写，尚未在本项目执行预处理、推理或后处理；环境和模型文件待核查。

## 阶段一：完整示范

### 本例要解决什么问题

起点为官方 ALK1 例，相关结构是 **6SF1：BMP10 与 ALK1 胞外区复合物**。原始数据库中 ALK1 为 A 链；上游 `examples/receptor_data/alk1.pdb` 已是处理后的 **B 链**受体片段，含 76 个带 ATOM 的残基，起始编号 30。两份文件的链标识不能直接互换。

本例使用上游处理后的 `alk1.pdb` 及配套位点。原始 6SF1 的 B 链是 BMP10，不能把它当作 ALK1。官方热点只提供设计位置，新肽能否结合、能否产生预期药理作用仍需相应证据。

| 步骤 | 本例怎样做 | 为什么 |
|---|---|---|
| 1 目标 | 在该 ALK1 构建体表面提出 15 aa 肽 | 限定探索问题，不先宣称抑制 BMP10 信号 |
| 2 输入确认 | 保留原件；在工作副本中核查 B40、B58–59、B71–72、B87 | 位点必须属于实际工作文件 |
| 3 设置条件 | 只填热点，其他口袋来源留空 | 原生按 ligand、hotspot、motif 的顺序选来源，混填时未必采用你想要的条件 |
| 4 原生运行 | 工作副本预处理，再读取其 metadata 推理 | 预处理会改写 PDB/JSON 链信息，且涉及 ESM 计算 |
| 5 审阅结果 | 核对链和残基对应关系、长度、连续性、碰撞及修复前后变化 | 配置填对后，还要确认输出的位置和几何 |
| 6 决定下一步 | 位点对应错误时先修复；其余候选按检查结果决定是否继续 | 错位点上的高分不能支持候选选择 |

### 原生配置与步骤

下面只使用热点定义口袋，因此将官方例中的 motif 清空。把 JSON 保存在仓库外工作目录；其中编号对应上游处理后的受体，不能直接用于原始 6SF1：

```json
{
  "alk1": {
    "hotspots": "B40, B58-59, B71-72, B87",
    "motif": "",
    "lig_chain": ""
  }
}
```

在已准备的固定版本源码目录，按[原生方法说明](../../methods/diffpepbuilder.md)分两步执行。以下路径都是待配置的教学占位，不表示本机已有文件：

```bash
export BASE_PATH="/path/to/tools/DiffPepBuilder"
python experiments/process_receptor.py \
  --pdb_dir /path/to/course/alk1-working \
  --write_dir /path/to/course/alk1-processed \
  --receptor_info_path /path/to/course/alk1-working.json
python experiments/run_inference.py \
  experiment.use_ddp=false experiment.num_gpus=1 \
  data.val_csv_path=/path/to/course/alk1-processed/metadata_test.csv \
  experiment.eval_ckpt_path=/path/to/models/diffpepbuilder_v1.pth \
  experiment.eval_dir=/path/to/course/alk1-output \
  inference.sampling.min_length=15 inference.sampling.max_length=15 \
  inference.sampling.samples_per_length=1 inference.seed=42
```

工作目录只放 `alk1.pdb` 副本，并确认文件名去掉扩展名后与 JSON key 一致。原生脚本会改写输入、清理部分 processed 文件，原件要另存。

单 GPU、单样本只是教学设置，是否能运行留待服务器检查。后处理需另读 `experiments/run_postprocess.py` 并准备依赖；尚未执行时，不能把结构记为已修复。

### 修改指南

| 分类 | 原生字段／操作 | 自己项目需要改变的内容 |
|---|---|---|
| 必须修改 | `--pdb_dir`、JSON key、受体与输出路径 | 自己的受体副本、文件名（不含扩展名）和模型目录 |
| 必须重新核对 | `hotspots`／`lig_chain`／`motif` | 从自己的结构取得位点，说明实际采用哪种来源，处理后复查编号 |
| 可以调整 | `min_length`、`max_length`、`samples_per_length`、`inference.seed` | 长度上限包含；按问题选择规模 |
| 不能照抄 | ALK1 B 链编号、原生多 GPU 示例和构象库路径 | 不能当作其他受体或本服务器的事实 |

### 合成教学记录：怎样审阅

假设两次输出均为 15 aa。A 的原生综合指标较好，但预处理后热点仍引用旧链，实际设计位置不明。B 的链和残基能逐一对应，局部几何检查可解释，但尚未比较不同输入准备方式。以上为人工编写的记录，没有真实结构和分数。

A 应先修复位点对应问题，再重算相关结果。保存原件、失败记录和修改前后的配置，在新轮次确认位点后再比较。

B 可保留做小规模探索；局部几何合理尚不能说明实测结合。两次计算输出也不能算作两次独立生物学验证。

**自我解释：**为什么不能把原始 6SF1 的 A/B 标识直接换入本例？为什么预处理也要记录为计算步骤？为什么同时填 motif 与热点可能没有表达自己以为的条件？

## 阶段二：补全练习

**练习 1｜最后决定。**沿用 A/B 摘要和步骤 1—5 的检查。修复 A、保留 B 后，你会先做哪一次检查或比较？说明理由。

**练习 2｜审阅与决定。**已给输入副本、热点来源和预处理日志。合成摘要称“全蛋白 RMSD 很低，但一个热点附近发生较大局部移动”。请完成步骤 5—6：要核对哪些局部原子和接触？全局 RMSD 不能说明什么？下一步怎样查？

**练习 3｜配置及后续。**同一 ALK1 工作构建体，分别只用热点、只用 motif 设计。请完成步骤 3—6：写两份配置，保持其他条件可比；说明怎样确认程序实际用了哪种来源、怎样计数，以及何时继续。没有输出时，只写方案。

## 阶段三：独立迁移

1. 选另一个公开受体结构，提出有来源的热点或 motif，说明预处理可能改变哪些编号，以及怎样核对。
2. 把自己的项目写入[任务卡](../common/research-task-card.md)和[迁移模板](../common/project-transfer.md)。若不存在可支持的位点来源，保留未知并说明先如何定位，而不是复制本例热点。

能解释练习 2 中的局部变化后，可进入迁移任务。若仍混淆原件和工作副本，先重新核对输入。

## 来源与后续验收

- [固定上游与原生示例](https://github.com/YuzheWangPKU/DiffPepBuilder/tree/c19eb4f0cd2419d3bcc116184c0868243b6c4169)、[受体工作文件](https://github.com/YuzheWangPKU/DiffPepBuilder/blob/c19eb4f0cd2419d3bcc116184c0868243b6c4169/examples/receptor_data/alk1.pdb)、[位点配置](https://github.com/YuzheWangPKU/DiffPepBuilder/blob/c19eb4f0cd2419d3bcc116184c0868243b6c4169/examples/receptor_data/de_novo_cases.json)。
- [6SF1 原始结构身份](https://www.rcsb.org/structure/6SF1)；链差异依据原始登记与上游 ATOM 记录核对，不声称已恢复完整准备过程。
- 待验收：输入副本处理、链映射、ESM/设计资产、最小推理、后处理依赖和实际几何检查。

[教师参考答案](../teacher-guide.md#diffpepbuilder) · [返回教学导航](../README.md)
