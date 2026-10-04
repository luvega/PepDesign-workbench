# PepMirror

手性感知多肽设计，使用结构口袋、模板与相匹配的轴向特征模型。输入需要有效的受体及口袋定义。

官方来源：[YZY010418/PepMirror](https://github.com/YZY010418/PepMirror/tree/41cb31f3974d91e1a2ca88f0db060405833e4a9c)。代码许可 MIT；模型来自官方 README 的 Zenodo 路径，权重许可另查。按官方 `environment.yaml` 建立环境，PyRosetta 等后处理依赖单独配置。

## 原生配置与入口

[线性模板](../../configs/pepmirror/linear.template.yaml)使用用户自备参考复合物，链 R 定义受体、链 L 的参考 ligand 定义口袋。它们是可修改的链 ID；不能给只有受体的结构虚构 ligand 链。仅受体输入可按官方指引建立口袋中心，但应明确记录这一准备步骤。

```bash
python -m api.generate \
  --config /path/to/jobs/pepmirror.yaml \
  --save_dir /path/to/outputs/pepmirror \
  --gpu 0 \
  --ckpt /path/to/models/pepmirror_commutator_both_v1.ckpt
```

配置与 checkpoint 的 axial type / position 必须一致。模板的 `size_max` 不包含在长度范围内。原生 API 支持不同模板，不能只改文件名就把线性肽视为环肽。

D 肽镜像路线使用官方 `scripts/mirror_pdb.py`：先准备镜像输入，配置指向该输入，生成后将复合物镜像返回。最终核查受体与肽链坐标手性，而非仅凭模板或模型名判定。原始结构、镜像操作及任何 relax 产物分别保存。
