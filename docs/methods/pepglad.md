# PepGLAD

以几何潜空间扩散生成全原子多肽，输入受体结构与口袋索引，原生 CLI 可进行序列 / 结构联合设计。

官方来源：[THUNLP-MT/PepGLAD](https://github.com/THUNLP-MT/PepGLAD/tree/bad015ca50c312a89482adb5220c3d907f13df5c)。代码许可 MIT，依赖和参数条款独立。按官方环境配置安装，权重见[官方 v1.0 release](https://github.com/THUNLP-MT/PepGLAD/releases/tag/v1.0)。该 API 联合设计入口读取源码目录的 `checkpoints/codesign.ckpt`。

## 原生配置

复制[口袋格式模板](../../configs/pepglad/pocket.template.json)，用实际链和 author residue number 替换。未使用插入码时保留单个空格 `" "`，不要改成空字符串。若已有参考复合物，也可用原生 `api.detect_pocket` 提取口袋。

```bash
python -m api.run --mode codesign \
  --pdb /path/to/inputs/receptor.pdb \
  --pocket /path/to/jobs/pocket.json \
  --out_dir /path/to/outputs/pepglad \
  --length_min 15 --length_max 16 --n_samples 1 --gpu 0
```

`length_max` 是不包含的上限，以上设置请求长度 15。此原生 API 不提供 `--seed` 或 `--ckpt` 参数，不要把其他脚本的选项直接传入。

输出包括 PDB 与 `summary.jsonl`，原生流程含 OpenMM relax。分别保留和检查可获得的生成 / 修复结构，关注手性、骨架连通性、末端几何和碰撞；全原子输出不自动代表化学或生物学有效。
