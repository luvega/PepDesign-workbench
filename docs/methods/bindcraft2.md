# BindCraft2

独立方法条目。本工作台提供其线性 L 肽与头尾 cyclic L 肽原生配置；不将 D / mixed 设计能力视为已建立。

官方来源：[PacesaLab/BindCraft2](https://github.com/PacesaLab/BindCraft2/tree/a8d0f2002df373842b86a3c20c5a060c5cfdf980)。代码采用 [Source-Available Hosting-Restricted](https://github.com/PacesaLab/BindCraft2/blob/a8d0f2002df373842b86a3c20c5a060c5cfdf980/LICENSE) 条款，独立于 BindCraft 的 MIT；托管功能与命名等条件以原文为准。

## 独立环境

固定来源要求 Python ≥3.12，JAX ≥0.11 且 <0.12。按官方指南选择 GPU / CUDA 安装方向；以下仅展示不自动下载参数的安装选项：

```bash
bash install.sh cuda13 --no-weights
source .venv/bin/activate
```

GPU 较旧时查官方 CUDA 12 选项。已有合法取得的 AlphaFold 参数可通过 `BINDCRAFT_AF2_PARAMS` 指定目录。不要复用 BindCraft 的 Conda 环境或 advanced JSON。

## 两个原生 campaign

[线性模板](../../configs/bindcraft2/linear.template.json)使用 `modality: peptide`；[环肽模板](../../configs/bindcraft2/cyclic.template.json)使用 `modality: cyclic_peptide`。固定来源预设的实际长度范围分别是 12–25 与 7–16，可按任务修改。

```bash
python -m bindcraft.cli design /path/to/jobs/bindcraft2-linear.json
python -m bindcraft.cli design /path/to/jobs/bindcraft2-cyclic.json
```

模板限制轨迹、worker 和 GPU 范围；`number_of_final_designs` 与 `max_trajectories` 分别表示期望接受数量与最多尝试数量。原生过滤可能得到零接受候选。没有文档化的独立 `bindcraft preflight` CLI，不要猜造该命令。

输出位于 `1_Trajectories/`、`2_Refolded/`、`3_Ranked/`，包含 mmCIF、CSV 和 `campaign_metadata.json`。环肽尤其核对闭环几何；固定来源默认 closure filter 不设置有限接受阈值，原生通过不能替代闭环检查。

[BindCraft](bindcraft.md)仍独立提供蛋白 / 迷你蛋白与线性肽预设入口。
