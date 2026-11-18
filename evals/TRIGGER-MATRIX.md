# 13-Skill 触发与分流测试矩阵

| Skill | 典型应触发原话（中国大学生场景） | 相邻易混负样本（应转交右侧专项 Skill） |
| --- | --- | --- |
| `bochen-answer-style` | “直接告诉我选哪个，别写报告套话，术语别硬翻” | “从零一步步教我同济线代矩阵的秩” → `learning-tutor` |
| `bochen-learning-tutor` | “课上老师讲条件概率和独立没听懂，结合浙大教材记号举例教我” | “我的 PTA 链表题最后一个测试点段错误” → `code-algorithm-tutor` |
| `bochen-code-algorithm-tutor` | “这道蓝桥杯/洛谷图论题怎么从暴力想到正解，注意多测清空和爆 int” | “推导西瓜书里逻辑回归最大似然和交叉熵的等价性” → `ai-math-tutor` |
| `bochen-ai-math-tutor` | “用二维小数字和 PyTorch shape 讲透 Self-Attention 为什么除根号 d_k” | “我在 Windows 上装 PyTorch 为什么读不到 RTX 4060 显卡” → `tech-guide` |
| `bochen-exam-master` | “后天考操作系统，这是复习 PPT 和往年卷，按得分效率排 36 小时计划和步骤分” | “我想用整个暑假不带考试压力把概率论底子打牢” → `learning-tutor` |
| `bochen-project-studio` | “我们三人组队做 3 周综合实训大作业，怎么切分 MVP 接口并防课堂演示断网翻车” | “我是北交大四学生，帮我做 15000 字本科毕业论文终稿抽检审查” → `cn-engineering-paper` |
| `bochen-paper-reader` | “带我拆解这篇 CVPR 英文论文的消融表到底靠哪项涨点，准备 12 分钟组会 PPT” | “帮我联网核实通义千问最新 API 输入输出单价” → `research-verifier` |
| `bochen-academic-writer` | “审阅我的计算机网络实验报告草稿，指出误差分析缺口并修正英文摘要 Chinglish” | “帮我从头评估 12 周本科毕设开题与任务书风险” → `cn-engineering-paper` |
| `bochen-cn-engineering-paper` | “按北交大校级与学院规范建立论文契约，审计我毕设初稿的引用、图表与结论边界” | “只帮我润色通识课 2000 字读书报告的一段引言” → `academic-writer` |
| `bochen-career-grad-advisor` | “对照这份大模型实习 JD 审查我简历里撑不住追问的风险点，再改一封保研预推免套磁信” | “帮我把这道 LeetCode 二分查找的边界 bug 调通” → `code-algorithm-tutor` |
| `bochen-research-verifier` | “避开营销号，去官网核实今年全国大学生数学建模报名时间和 GB/T 7714 最新版次” | “把我已写好的实验结论改得更自然简练” → `academic-writer` |
| `bochen-tech-guide` | “AutoDL 系统盘满了报 No space left，而且合上笔记本训练就断，一步步教我怎么改” | “证明为什么负权图不能用 Dijkstra 算法” → `code-algorithm-tutor` |
| `bochen-skill-builder` | “把这套工作习惯拆成渐进式披露的 SKILL.md 和 references，补正负向 evals” | “给当前这一条问题写一句简短提示词” → 直接回答 |

## 组合分流原则

1. `bochen-answer-style` 只管表达质感，绝不单独吞掉需要领域工作流的任务。
2. **代码与工程三级递进**：单题/语法/OJ 归 `code-algorithm-tutor` → 课程组队大作业/大创/竞赛归 `project-studio` → 大四本科毕业论文全周期归 `cn-engineering-paper`。
3. **科研与文献三级分工**：联网查真伪与外部最新元数据归 `research-verifier` → 精读单篇已知英文论文与源码对齐归 `paper-reader` → 起草与修改自己的课程报告归 `academic-writer`。
4. **考核与出路分工**：校内课程期末/四六级/CSP 提分归 `exam-master` → 校外技术实习/秋招/保研套磁与复试深挖归 `career-grad-advisor`。
