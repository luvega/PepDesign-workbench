# BindCraft

独立的受体条件 binder 设计方法，组合 AlphaFold 优化、序列设计和结构过滤，提供蛋白 / 迷你蛋白及线性肽预设。

官方来源：[martinpacesa/BindCraft](https://github.com/martinpacesa/BindCraft/tree/b971db42ba6e091afab63ccb30ae02215150a990)，代码 MIT。PyRosetta、AlphaFold 参数和其他依赖条款分别核对。

## 环境与设置

按固定版本的 `install_bindcraft.sh` 安装独立 Python 3.10 Conda 环境。安装会配置依赖并获取参数，应先查看脚本和 CUDA 选项：

```bash
bash install_bindcraft.sh --cuda '12.4' --pkg_manager 'conda'
```

配置由 basic、advanced 和 filter 三部分组成：[basic 模板](../../configs/bindcraft/basic.template.json)请求蛋白 binder 的长度范围；原生线性肽可选择 peptide advanced / filter 预设并调整 basic 长度。

## 原生入口

```bash
python -u bindcraft.py \
  --settings /path/to/jobs/bindcraft-basic.json \
  --filters /path/to/jobs/bindcraft-filters.json \
  --advanced /path/to/jobs/bindcraft-advanced.json
```

advanced 和 filters 应基于完整的官方预设填写，不能只写几项就假设它们是完整配置。`max_trajectories` 在 advanced 中，统计已保存到 `Trajectory/Relaxed/` 的轨迹；早期失败可能不计入，实际尝试数与墙钟预算需要另行监督。原生 CLI 没有 `--seed`。详见[配置准备](../../configs/bindcraft/README.md)。

输出包括 PDB、`trajectory_stats.csv`、`mpnn_design_stats.csv` 和 `final_design_stats.csv`。保留接受和拒绝记录，分别检查序列、结构与原生过滤状态。不将 L 体系设置直接解释为 D / mixed 设计支持。

[BindCraft2](bindcraft2.md)使用另一个源码、环境、campaign 格式与许可证。
