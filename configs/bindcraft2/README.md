# BindCraft2 原生 campaign

[linear.template.json](linear.template.json)和[cyclic.template.json](cyclic.template.json)分别配置线性 L 肽与 cyclic L 肽。修改受体绝对路径、链、长度和输出目录后，传给原生 `python -m bindcraft.cli design`。

模板继承原生默认环境与 modality 预设，限制为一个 GPU、一个 worker、最多一个 trajectory。每个 campaign 使用独立输出目录。实际参数可根据任务修改；一个 trajectory 不保证一个接受候选。

两个 campaign 的 `binder_lengths` 为闭区间。固定版本的 cyclic preset 默认启用环化；仍需独立检查最终闭环几何。

环境、参数目录、原生输出和许可见 [BindCraft2](../../docs/methods/bindcraft2.md)。这些设置不传给 [BindCraft](../bindcraft/README.md)。
