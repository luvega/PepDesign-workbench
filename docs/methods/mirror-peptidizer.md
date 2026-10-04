# Mirror-Peptidizer

镜像设计路线结合 Chroma 骨架生成、ProteinMPNN 序列设计及结构处理，面向 L 受体的 D 肽设计。

官方来源：[dahuilangda/Mirror-Peptidizer](https://github.com/dahuilangda/Mirror-Peptidizer/tree/a517c8fb6711649284116135c2fe2c7e1719870b)。代码许可 Apache-2.0；Chroma 参数按其独立授权条款获取，不由本工作台分发。

## 环境与资产

按官方安装说明建立 Python 3.10 环境，配置 Chroma、ProteinMPNN、Biopython 与结构修复工具。官方 `.env` 使用 `CHROMA_KEY`、`CHROMA_WEIGHTS_DIR` 和可选 `ProteinMPNN_CHECKPOINT`。凭据仅保存在私有本机配置中。

[Chroma 官方项目](https://github.com/generatebio/chroma)提供参数访问说明。ProteinMPNN 默认使用 `vanilla_model_weights/v_48_020.pt`；不要把不同模型 prior 的 checkpoint 当作同一资产。

## 原生命令

```bash
python run_design.py \
  --receptor /path/to/inputs/receptor.pdb \
  --output /path/to/outputs/mirror-peptidizer \
  --len_binder 15 --num_poses 1 --num_seqs_per_pose 1 \
  --temperature 0.1 --gpu 0 --bo_rounds 0
```

这是初始设计入口；Bayesian optimization 是另一个可配置阶段。以上关闭 BO，不依赖额外 embedding 服务。

原生输出包含序列记录与镜像 / 返回后的结构。检查最终受体与肽链手性，保留反射和修复记录；D 肽设计意图与输出实际手性分别记载，mixed 产物按实际结构评估。
