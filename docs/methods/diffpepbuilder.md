# DiffPepBuilder

结构条件扩散设计，输入受体 PDB 与结合区域描述，输出多肽序列和结构。

官方来源：[YuzheWangPKU/DiffPepBuilder](https://github.com/YuzheWangPKU/DiffPepBuilder/tree/c19eb4f0cd2419d3bcc116184c0868243b6c4169)。代码许可 MIT；模型与 PyRosetta 依赖各自核对条款。环境按该版本官方配置建立，设计模型由[官方 checkpoint](https://zenodo.org/records/12794439/files/diffpepbuilder_v1.pth)获取。预处理还会获取 ESM2 模型与 contact-regression 参数；默认 SSbuilder 路线需要按官方说明解包构象库。

## 原生流程

在源码目录执行。用户受体命名为 `receptor.pdb`，其 stem 与 JSON 的 `receptor` 对应；避免文件 stem 中的下划线。先填写[受体模板](../../configs/diffpepbuilder/receptor.template.json)，其中位点编号仅作格式示意。

原生预处理会就地改写受体 PDB 和 JSON 的链标识，并清理输入目录中的部分 processed 文件。先复制一份工作输入与配置，保留原件；下面 `--pdb_dir` 指向工作副本目录。预处理载入 ESM 参数，CUDA 可用时会使用 GPU，属于计算步骤。

```bash
export BASE_PATH="/path/to/tools/DiffPepBuilder"
python experiments/process_receptor.py \
  --pdb_dir /path/to/jobs/receptors-working \
  --write_dir /path/to/jobs/processed \
  --receptor_info_path /path/to/jobs/receptor.json

python experiments/run_inference.py \
  experiment.use_ddp=false experiment.num_gpus=1 \
  data.val_csv_path=/path/to/jobs/processed/metadata_test.csv \
  experiment.eval_ckpt_path=/path/to/models/diffpepbuilder_v1.pth \
  experiment.eval_dir=/path/to/outputs/diffpepbuilder \
  inference.sampling.min_length=15 inference.sampling.max_length=15 \
  inference.sampling.samples_per_length=1 inference.seed=42
```

长度上限包含在范围内。`lig_chain`、`hotspots` 和 `motif` 是不同口袋来源；原生优先顺序为 ligand、hotspot、motif，不能不加检查地混填。后处理入口为 `experiments/run_postprocess.py`，其结构修复依赖另行安装。

保留生成与后处理前后的结构，逐残基检查手性、连通性、几何和碰撞。全流程包含受体预处理，不能只运行推理后假设口袋已正确建立。
