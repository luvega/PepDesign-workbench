# DexDesign / OSPREY3

基于 OSPREY 的 D 肽能量搜索路线，使用准备好的 D 肽 / L 受体复合物、构象库与显式搜索空间。

官方来源：[donaldlab/OSPREY3](https://github.com/donaldlab/OSPREY3/tree/3d53244851f0388db9e01b288bbd330145935aa7)。代码许可见该版本 `LICENSE.txt`（GPL v2）；计算引擎、结构准备工具与其他组件分别核对条款。配置官方引擎、JVM 和 Python bridge，无神经网络 checkpoint 下载要求。

## 原生入口

路线位于 `examples/ccs.D-peptide-L-protein/`，包括 `DL_preprocess.py`、`DL.py`、`Confspace_Combiner.py` 与 `ccsKstar.py`。

原生脚本使用文件内配置及生成的作业，不能用不存在的 `--pdb` 或 `--weights` 参数启动。工作流程是：

1. 准备符合化学和手性要求的复合物与 scaffold。
2. 按原生预处理步骤检查质子化、链与残基标识，建立 prepared-PDB 输入目录。
3. 配置 `DL.py` 中的输入路径、引擎路径、线程、内存与作业设置，建立 IAS 的构象空间。
4. 按生成的原生配置执行 K* 搜索，保留完整搜索状态、数值记录与构象 ensemble。

[搜索准备记录](../../configs/dexdesign/search-inputs.template.json)是待填写的接入清单，不是 OSPREY 原生 CLI 配置。原生脚本默认资源参数面向集群，应按自己的环境主动配置。

构象空间中的二硫键、非标准残基、D 构象库和柔性位点须显式检查。任务结束、得到数值、完整搜索收敛和结构质量是不同状态；能量结果不是实验结合常数。
