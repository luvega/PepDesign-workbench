# 开始使用

本科生先从[十方法教学导航](teaching/README.md)选择 1—2 种方法，读示范、做练习，再改成自己的项目方案。任务卡用于说明计划，运行时仍需各方法的原生配置，并完成下面的环境和输入准备。

工作台按方法组织环境配置、原生入口和产物检查。先选择满足输入与输出要求的一种方法，再安装它的依赖。

## 选择入口

只有受体序列时，先阅读 [PepMLM](methods/pepmlm.md)。需要结构条件生成时，可阅读 [DiffPepBuilder](methods/diffpepbuilder.md)、[PepGLAD](methods/pepglad.md) 或 [RFdiffusion + ProteinMPNN](methods/rfdiffusion-proteinmpnn.md)。

D 肽路线分别见 [Mirror-Peptidizer](methods/mirror-peptidizer.md)、[PepMirror](methods/pepmirror.md) 和 [DexDesign / OSPREY3](methods/dexdesign.md)。它们的输入、模型和能量搜索要求不同。

环肽路线见 [AfCycDesign](methods/afcycdesign.md) 和 [BindCraft2](methods/bindcraft2.md)。蛋白 / 迷你蛋白 binder 和原生线性肽预设见 [BindCraft](methods/bindcraft.md)。

## 目录与环境

将工作台、上游源码、模型资产和用户任务分开，例如：

```text
workspace/
  PepDesign-workbench/    文档和通用配置
  tools/                 各方法源码与独立环境
  models/                权重与参数
  jobs/
    inputs/              用户输入
    configs/             已填写的原生设置
    outputs/             原始产物和日志
```

源码参考见[方法登记](../registry/methods.json)。按[环境指南](environments.md)核对驱动、CUDA、Python 和上游安装方式。首次安装可能下载大型资产，应预先安排存储和网络。

使用来源登记的官方 URL 和 commit 建立源码副本，例如填写下面三个 shell 变量后执行：

```bash
git clone "$OFFICIAL_SOURCE_URL" "$METHOD_SOURCE_DIR"
git -C "$METHOD_SOURCE_DIR" checkout --detach "$REFERENCE_COMMIT"
```

这些是源码准备命令；不同方法的安装入口在各自说明中列出。

## 填写配置并运行

复制所选方法的[模板](../configs/README.md)到自己的任务目录，将输入、输出和模型路径改为绝对路径。示例的链 ID 和长度是可编辑参数，应与自己的输入一致。

原生命令通常从上游源码目录执行。模板不会自动准备受体、定义口袋或获取权重；这些步骤按各方法说明完成。API 和 notebook 方法没有额外虚构的命令行入口。

任务开始前记录使用的源码 commit、依赖、权重文件和配置，并为轨迹数、输出数量和耗时安排边界。接受候选数量与尝试数量是两个不同参数。

产物检查见[质量检查指南](quality-checks.md)。保留原生过滤拒绝信息，并将运行完成与候选质量分开记录。
