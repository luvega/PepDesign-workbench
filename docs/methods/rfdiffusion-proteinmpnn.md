# RFdiffusion + ProteinMPNN

两个原生软件组成骨架生成与序列设计流程。输入受体结构和 contig / hotspot 条件；RFdiffusion 输出骨架，ProteinMPNN 为选定链设计序列。

官方来源：[RFdiffusion](https://github.com/RosettaCommons/RFdiffusion/tree/2d0c003df46b9db41d119321f15403dec3716cd9) 与 [ProteinMPNN](https://github.com/dauparas/ProteinMPNN/tree/8907e6671bfbfc92303b5f79c4b5e6ce47cdef57)。前者 BSD，后者 MIT；参数与依赖以各自来源说明为准。

## 环境与两个入口

RFdiffusion 按官方 `env/SE3nv.yml`、SE3Transformer 和 editable install 建立环境，模型放入其 `models/`。ProteinMPNN 另按官方环境配置，使用相匹配的模型权重，例如 `vanilla_model_weights/v_48_020.pt`。下面 `$MPNN_WEIGHTS` 指向包含该文件的目录，不是单个 `.pt` 文件。

从 RFdiffusion 源码目录运行；下面 shell 变量由用户填写，链和起止编号来自自己的结构：

```bash
python scripts/run_inference.py \
  "inference.input_pdb=$RECEPTOR_PDB" \
  "inference.output_prefix=$OUTPUT_PREFIX" \
  inference.num_designs=1 \
  "contigmap.contigs=[$TARGET_CHAIN$START-$END/0 $BINDER_MIN-$BINDER_MAX]"
```

`/0` 后面的空格是 contig 语法的一部分。可按官方 Hydra 格式另外指定 `ppi.hotspot_res`。

检查生成结构中的 binder 链后，从 ProteinMPNN 源码目录运行：

```bash
python protein_mpnn_run.py \
  --pdb_path "$GENERATED_PDB" --pdb_path_chains "$BINDER_CHAIN" \
  --out_folder "$MPNN_OUTPUT" --num_seq_per_target 1 \
  --sampling_temp 0.1 --seed 42 \
  --path_to_model_weights "$MPNN_WEIGHTS" --model_name v_48_020
```

RFdiffusion 可能重新分配链 ID，不能把受体原始链直接当作 MPNN 设计链。先检查 `.trb` 和输出 PDB。ProteinMPNN 的 `seqs/*.fa` 含原始序列记录与生成记录，解析时需区分。

两个步骤不会自动得到已补全侧链的全原子复合物。若另行建模、修复或 refold，应保留步骤关系并分别检查手性与几何。
