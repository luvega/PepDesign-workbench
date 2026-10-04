# 环境与模型资产

每个方法使用独立环境。首先固定源码参考，再按该版本的官方安装文件核对依赖；不把不同方法的 Python、JAX、PyTorch 和 CUDA 配置合并到一个环境中。

| 方法 | 配置方向 | 模型资产入口 |
| :--- | :--- | :--- |
| PepMLM | 官方 Python / Transformers 环境 | 官方链接的 Hugging Face 模型 |
| DiffPepBuilder | 官方 Conda 与 PyTorch 配置 | 设计 checkpoint、ESM2 预处理参数与默认 SSbuilder 构象库 |
| PepGLAD | 官方依赖与 PyTorch 配置 | API 的 `codesign.ckpt` / `fixseq.ckpt`；训练资产按官方流程另行准备 |
| Mirror-Peptidizer | Python 3.10、Chroma、ProteinMPNN、结构修复依赖 | 需要授权的 Chroma 参数；ProteinMPNN 权重 |
| PepMirror | 官方 `environment.yaml`；结构处理依赖另行配置 | 官方 Zenodo checkpoint，匹配轴向特征设置 |
| AfCycDesign / ColabDesign | 独立 ColabDesign / JAX 环境或官方 notebook | AlphaFold 参数，按官方流程获取 |
| DexDesign / OSPREY3 | 官方引擎、JVM、Python bridge 与结构准备工具 | 构象库、力场与准备好的搜索输入；无神经网络 checkpoint |
| RFdiffusion + ProteinMPNN | 两个原生软件及对应 PyTorch 依赖 | RFdiffusion 与 ProteinMPNN 各自权重 |
| BindCraft | 官方 Python 3.10 Conda 安装流程；JAX、ColabDesign、PyRosetta | AlphaFold 参数与原生序列设计资产 |
| BindCraft2 | 独立 Python ≥3.12 环境，参考版 JAX ≥0.11 且 <0.12 | 官方 AlphaFold 参数目录，可通过 `BINDCRAFT_AF2_PARAMS` 指定 |

完整入口在[各方法说明](methods/README.md)。这是一份配置指南，不是面向所有硬件的环境锁文件；驱动和 GPU 架构应以各方法固定版本的安装指南为准。

## 分层核对

1. 检查源码和许可证，记录 commit。
2. 核对 Python、驱动、CUDA 与框架版本。
3. 按官方来源获取权重，记录文件名、版本与 SHA256。
4. 检查原生配置字段和输入路径。
5. 需要计算时，再调用该方法的原生流程。

GPU 初始化、载入权重和运行模型均可能使用计算资源，不能算作纯文档检查。安装脚本也可能自动下载参数；执行前先查看上游脚本。

## 凭据与保存位置

Chroma 的参数访问遵循 [Chroma 官方说明](https://github.com/generatebio/chroma)。凭据配置在本机私有环境或上游 `.env` 中，不写入文档、模板或 Git。权重、模型缓存和第三方源码保存在工作台目录之外。

BindCraft 和 BindCraft2 分别安装；前者的 Conda 环境和 advanced/filter JSON 不直接用于后者的 campaign 或 `.venv`。
