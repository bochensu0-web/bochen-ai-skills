# 工科数学 → 西瓜书/李航 → PyTorch/LLM 记号与张量桥接表

国内本科生从大一公共数学进入《机器学习》（周志华“西瓜书”）、《统计学习方法》（李航）和 PyTorch 代码时，90% 的困惑来自**记号惯例打架**与**批量维度隐式广播**。讲解时按需对照本表。

---

## 1. 记号体系三方对照（防转置绕晕）

| 概念 | 大一同济线代/浙大概统 | 西瓜书 / 统计学习方法 | PyTorch / 深度学习代码 | 讲解避坑提醒 |
| --- | --- | --- | --- | --- |
| 单样本特征 | 列向量 $x = (x_1, \dots, x_d)^\top$ | 列向量 $\boldsymbol{x} \in \mathbb{R}^d$ | 1D 张量 `[D]` 或带 batch `[1, D]` | 数学推导默认**列向量**，代码里一行是一个样本！ |
| 数据集矩阵 $X$ | 常按列拼或按方程组写 | 西瓜书 $\mathbf{X} \in \mathbb{R}^{m \times d}$（每行一个样本，$\boldsymbol{x}_i^\top$） | `X: [B, D]`（Batch 在第 0 维） | 教材写 $f(\boldsymbol{x}) = \boldsymbol{w}^\top \boldsymbol{x} + b$，对应 `nn.Linear` 内部存 `weight: [out, in]`，计算 `X @ W.T + b`！ |
| 梯度方向 $\nabla_{\boldsymbol{w}} L$ | 偏导数组成的向量 | 与 $\boldsymbol{w}$ 同维度的列向量（分母布局） | `w.grad` 与 `w.shape` **严格同形状** | 教学生求矩阵导数时，最稳妥的方法是**标量展开/微分迹技巧 + 形状匹配检查**：导数形状永远等于被求导参数的形状！ |
| 对数底数 $\log$ | $\ln x$（自然对数）vs $\lg x$（以 10 为底） | 信息论常取 $\log_2$（单位 bit），优化推导常取 $\ln$ | `torch.log` 默认是自然对数 $\ln$（单位 nat） | 只差常数倍 $\ln 2$，不改变极值点位置，但手算决策树信息增益作业题时必须用 $\log_2$！ |
| 期望与指示函数 | $E(X)$，无统一指示函数记号 | $\mathbb{E}[\cdot]$，$\mathbb{I}(\text{条件})$（真为 1，假为 0） | `.mean(dim=...)`，`(cond).float()` | 看到求和 $\frac{1}{m}\sum_{i=1}^m$ 就对应代码里的 `.mean(dim=0)`。 |

---

## 2. PyTorch 高频张量维度与静默 Bug 清单

1. **`[B, 1]` 与 `[B]` 的致命广播陷阱**：
   - 若 `pred` 形状为 `[B, 1]`，`target` 形状为 `[B]`，手写 `((pred - target) ** 2).mean()` 会触发广播变成 `[B, B]` 两两相减矩阵，训练不报错但模型完全学废！修复：统一 `.squeeze(-1)` 或显式 `assert pred.shape == target.shape`。
2. **`CrossEntropyLoss` 不要重复套 `Softmax`**：
   - `nn.CrossEntropyLoss()` 内部包含 `LogSoftmax + NLLLoss`（数值稳定防 `exp` 上溢），输入必须是未归一化的原始 `logits: [B, C]`（LLM 下常展平为 `[B*L, V]`），标签为 `int64` 类别索引 `[B]`。
3. **BatchNorm vs LayerNorm vs RMSNorm 归一化轴对比**：
   - 输入特征 `[B, L, D]`（Batch、序列长、隐藏维）：
   - `BatchNorm`：跨 `B` 统计每个通道均值方差 → 依赖大 batch，维护 `running_mean/var`，训练与 `eval()` 行为不同。
   - `LayerNorm`：对**单个 token 自身**的 `D` 维求均值方差并重缩放 → 与 batch 大小和序列长度无关，NLP/Transformer 标配。
   - `RMSNorm`：去掉减均值中心化，只除均方根 $\text{RMS}(\boldsymbol{x}) = \sqrt{\frac{1}{D}\sum x_i^2 + \epsilon}$ 再乘可学习缩放 $\gamma$ → LLaMA/Qwen 等现代大模型标配。
4. **Transformer / LLM 显存与 KV Cache 心算公式**：
   - 单层 Multi-Head Attention：`X: [B, L, D]`，拆头后 `Q, K, V: [B, H, L, d_h]`（其中 $H \times d_h = D$），注意力矩阵 `[B, H, L, L]`（复杂度 $O(L^2)$ 来源）。
   - FP16/BF16（每参数 `2 Bytes`）下：模型权重显存 $\approx 2 \times \text{参数量}$；AdamW 混合精度全参训练（权重 + 梯度 + FP32 主权重 + 一二阶动量）显存约需 **$16 \sim 18 \times \text{参数量}$**，因此消费级单卡（如 16G/24G）常需配合 LoRA / QLoRA + Gradient Checkpointing。
