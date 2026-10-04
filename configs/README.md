# 通用原生配置

模板只包含通用路径和参数。复制到仓库外的任务目录后，按自己的输入填写；命令从对应上游源码目录执行。

| 方法 | 配置入口 | 用法 |
| :--- | :--- | :--- |
| PepMLM | [函数输入记录](pepmlm/function-inputs.template.json) | 人工记录；按[原生函数说明](../docs/methods/pepmlm.md)加载模型和调用 |
| DiffPepBuilder | [受体 JSON](diffpepbuilder/receptor.template.json) | 用户改写 residue / hotspot 后交给原生预处理 |
| PepGLAD | [口袋 JSON](pepglad/pocket.template.json) | 填写实际链、编号与插入码，再交给原生 API |
| Mirror-Peptidizer | [CLI 参数记录](mirror-peptidizer/cli-inputs.template.json) | 人工记录；使用[原生 run_design.py](../docs/methods/mirror-peptidizer.md) |
| PepMirror | [线性 YAML](pepmirror/linear.template.yaml) | 填写真实复合物和匹配的 checkpoint，传给原生 API |
| AfCycDesign | [notebook 参数记录](afcycdesign/notebook-inputs.template.json) | 人工记录；按[notebook/API 路线](../docs/methods/afcycdesign.md)接入 |
| DexDesign / OSPREY3 | [搜索准备记录](dexdesign/search-inputs.template.json) | 人工记录；原生脚本需要自己的 prepared complex 与引擎配置 |
| RFdiffusion + ProteinMPNN | [两阶段输入记录](rfdiffusion-proteinmpnn/stages.template.json) | 人工记录；对应[两阶段原生命令](../docs/methods/rfdiffusion-proteinmpnn.md) |
| BindCraft | [basic 与预设准备](bindcraft/README.md) | basic / advanced / filters 三个原生文件 |
| BindCraft2 | [两个 campaign](bindcraft2/README.md) | 线性与 cyclic 两个独立原生 JSON |

标注“人工记录”的 JSON 不是原生程序输入，也不被平台执行。[任务记录](run-record.template.json)可用于保存用户任务的源码、资产摘要、环境与输出状态。

不要直接执行尚未填写的模板。原生安装、下载和计算均在用户自己的方法环境中进行。
