# PepMLM

输入受体序列与肽长，生成多肽序列和原生 pseudo-perplexity。它不直接生成骨架或三维复合物。

官方来源：[programmablebio/pepmlm](https://github.com/programmablebio/pepmlm/tree/3169c4920f8c383948e0a5d3a7c8f87e5e7d2436)。模型入口：[TianlaiChen/PepMLM-650M](https://huggingface.co/TianlaiChen/PepMLM-650M)。源码参考见[登记](../../registry/methods.json)。该源码参考未提供仓库级 LICENSE；模型许可另核对官方 model card。

## 环境与原生入口

需要 PyTorch、Transformers、NumPy 和 pandas。按官方说明加载 `AutoTokenizer` 和 `AutoModelForMaskedLM`，可将权重保存到用户自己的模型目录。

原生 `scripts/generation.py` 定义函数，未提供完整命令行程序。接入时需初始化它使用的 globals：

```python
from pathlib import Path
import numpy as np
import pandas as pd
import torch
from torch.distributions import Categorical
from transformers import AutoTokenizer, AutoModelForMaskedLM
from scripts import generation

model_dir = "/path/to/models/PepMLM-650M"
generation.tokenizer = AutoTokenizer.from_pretrained(model_dir)
generation.model = AutoModelForMaskedLM.from_pretrained(model_dir).eval()
generation.torch, generation.np = torch, np
generation.pd, generation.Categorical = pd, Categorical
# 单条用户自备 FASTA；多条输入应分别解析为 list[str]。
lines = Path("/path/to/inputs/receptor.fasta").read_text().splitlines()
assert sum(line.startswith(">") for line in lines) == 1
sequence = "".join(line.strip() for line in lines if not line.startswith(">")).upper()
assert sequence and all(c in "ACDEFGHIKLMNPQRSTVWY" for c in sequence)
result = generation.generate_peptide(sequence, peptide_length=15, top_k=3, num_binders=1)
result.to_csv("/path/to/outputs/peptides.csv", index=False)
```

这是原生函数的初始化示意，不是新增统一 CLI。输出目录须先建立；GPU 使用需由用户配置模型设备。生成原样保留，检查长度、字符和重复；不能从字母序列推断 D 肽构象。pseudo-perplexity 表示模型序列兼容性，不是亲和力。
