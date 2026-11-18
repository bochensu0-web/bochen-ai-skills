# 大学四年典型场景组合调用示例

通常采用 **“1 个全局表达 Skill + 1 个核心领域 Skill”**（跨场景时最多叠加第 3 个），兼顾深度与上下文精简。

---

## 1. 大一/大二公共课与 408 专业课补基
> 使用 `$bochen-answer-style` 和 `$bochen-learning-tutor`。我同济版线性代数课上跟丢了，一上来全是行列式和伴随矩阵完全没直觉。请先用二维平面变换讲清楚“矩阵的秩”到底在衡量什么，再对齐回国内教材记号带我手算一道含参方程组解的个数讨论题，最后出一道小检查题考我。

## 2. PTA / 蓝桥杯 / CCF CSP 算法与机试排错
> 使用 `$bochen-answer-style` 和 `$bochen-code-algorithm-tutor`。我在准备 CCF CSP 和期末上机，请从 $O(n^2)$ 暴力瓶颈出发推导出最长递增子序列 $O(n \log n)$ 解法是怎么想到的，给出符合 PTA 行末无多余空格要求的 C++17 ACM 模式代码，并标出多组测试与 `long long` 防坑点。

## 3. 西瓜书/统计学习方法与 PyTorch 大模型机制打通
> 使用 `$bochen-answer-style` 和 `$bochen-ai-math-tutor`。我在看西瓜书和 Transformer 代码，总是把数学列向量和 PyTorch 的 batch 张量转置搞混。请用 `B=1, L=2, d_k=2` 的具体小整数手算一遍 Scaled Dot-Product Attention，再给出逐行标明 `shape` 的 PyTorch 最小验证代码。

## 4. 期末 48 小时极限抢分与步骤分突击
> 使用 `$bochen-answer-style` 和 `$bochen-exam-master`。后天上午考《操作系统》，我平时基础一般，手头有老师最后一节课的复习提纲和两套本校往年卷。请按单位时间得分排一份 36 小时冲刺表，重点总结 PV 同步、页表地址转换和页面置换大题的“保底步骤分”书写模板。

## 5. 课程综合实训组队大作业与大创/数模竞赛
> 使用 `$bochen-answer-style` 和 `$bochen-project-studio`。我们 3 个人组队做为期 3 周的 AI 创新应用综合实训（A 做 ResNet 图像分类、B 做大模型 RAG 问答、C 做 Web 界面），教室答辩现场可能断网。请帮我们收敛第一周 MVP 边界、制定 A/B/C JSON 接口契约与离线降级防翻车方案。

## 6. 顶会英文论文精读、源码定位与实验室组会汇报
> 使用 `$bochen-answer-style` 和 `$bochen-paper-reader`。本周五实验室组会轮到我讲这篇英文论文和它的官方 PyTorch 仓库。请先帮我区分哪些是常规 Backbone、哪两个公式是作者真正的创新，审视消融实验到底靠哪一项涨点，再生成 8 页组会 PPT 提纲和导师最可能追问的 3 个问题。

## 7. 专业课实验报告修改与中英摘要去水词
> 使用 `$bochen-answer-style` 和 `$bochen-academic-writer`。这是我的计算机视觉课程实验报告草稿和英文 Abstract。请先以 Reviewer 模式抓出“只贴图没分析”和空泛套话问题，再保留我的真实实验过程做最小有效修改，不要编造任何未测过的实验指标。

## 8. 北交大工科本科毕业设计（论文）全周期推进
> 使用 `$bochen-answer-style`、`$bochen-cn-engineering-paper` 和 `$bochen-research-verifier`。我是北京交通大学人工智能专业本科生，只有 12 周和单张消费级显卡。请先按当届学院与校级规范建立论文契约，评估选题可行性与实验基线设计，并用确定性审计脚本检查文稿引用与图表编号一致性。

## 9. 大三暑期实习简历“防拷打”审查与保研预推免套磁
> 使用 `$bochen-answer-style` 和 `$bochen-career-grad-advisor`。这是我收集的 5 份大模型应用/AI 后端实习 JD 以及我目前的简历和两个课程项目说明。请按证据感知原则标出简历里会被面试官深挖穿帮的声明、指出项目里做过却漏写的高价值证据，并模拟 5 道针对我头号项目的追问题。

## 10. 高校政策 / 国家标准 / 模型参数双语核验
> 使用 `$bochen-answer-style` 和 `$bochen-research-verifier`。避开二手公众号和 CSDN 搬运帖，帮我查官方一手来源核实 `GB/T 7714` 与 `GB/T 7713.1` 现行有效版本，并对比两个主流大模型 API 当前的官方上下文窗口与计费单价，标明核验日期。

## 11. 国内镜像源、CUDA 与 AutoDL 远程算力排障
> 使用 `$bochen-answer-style` 和 `$bochen-tech-guide`。我连上 AutoDL 租的 RTX 4090 实例后拉 HuggingFace 权重一直超时，而且系统盘快满了、笔记本一合盖训练就中断。请一步步给我最稳妥的国内魔搭/镜像替代命令、数据盘缓存迁移和 `tmux` 保活操作及每步预期输出。
