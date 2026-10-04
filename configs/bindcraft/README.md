# BindCraft 原生设置

[basic.template.json](basic.template.json)是原生 basic 设置；受体路径、链、长度与输出路径须由用户填写。

advanced 与 filters 使用完整官方预设。蛋白 binder 可以从 `settings_advanced/` 和 `settings_filters/` 选择适用文件；线性肽可参考固定来源中的 `peptide_3stage_multimer.json` 与 `peptide_filters.json`，并将 basic 长度调整为任务要求。

要限制原生已保存的 relaxed 轨迹数量，复制官方完整 advanced JSON，然后修改该文件中的 `max_trajectories`。例如在上游目录运行以下配置操作，不启动模型：

```python
import json
from pathlib import Path

preset = Path("settings_advanced/peptide_3stage_multimer.json")
advanced = json.loads(preset.read_text())
advanced["max_trajectories"] = 1
Path("/path/to/jobs/bindcraft-advanced.json").write_text(
    json.dumps(advanced, indent=2) + "\n"
)
```

basic 的接受数量不限制尝试数；`max_trajectories` 也不统计未留下 relaxed PDB 的早期失败。实际尝试数与墙钟时间需要另行监督。原生入口和环境见 [BindCraft](../../docs/methods/bindcraft.md)。[BindCraft2 的 campaign](../bindcraft2/README.md)是另一种配置格式。
