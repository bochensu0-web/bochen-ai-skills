# 触发测试矩阵

| Skill | 应触发 | 不应单独触发 |
| --- | --- | --- |
| `bochen-answer-style` | “直接告诉我哪个好，别写套话” | “一步步教我动态规划” |
| `bochen-learning-tutor` | “我没懂傅里叶变换，举例教我” | “这段 Python 为什么报 IndexError” |
| `bochen-code-algorithm-tutor` | “这道图论题怎么从暴力想到 Dijkstra” | “解释交叉熵在分类里的数学意义” |
| `bochen-ai-math-tutor` | “用数字例子和 PyTorch 讲 batch norm” | “帮我安装 CUDA” |
| `bochen-exam-master` | “三天后考试，按得分效率排计划” | “我想长期系统学概率论” |
| `bochen-academic-writer` | “审阅我的课程论文并保留原意修改” | “帮我规划北交大本科毕设开题与实验” |
| `bochen-cn-engineering-paper` | “评估我的 AI 本科毕设选题、实验方案与北交大终稿规范” | “只帮我润色课程作业的一段摘要” |
| `bochen-research-verifier` | “查官方来源核验这个模型价格” | “把这段话写得更自然” |
| `bochen-tech-guide` | “看截图告诉我 VS Code 下一步点哪” | “证明贪心算法为什么正确” |
| `bochen-skill-builder` | “把长期工作流做成可测试 Skill” | “给这一条问题写一个临时提示词” |

组合测试还应确认：`bochen-answer-style` 不抢专项任务；`bochen-learning-tutor` 不替代代码调试；`bochen-exam-master` 只在明确考试目标时加入；`bochen-academic-writer` 与 `bochen-cn-engineering-paper` 按课程短文 vs 本科毕设全周期清晰分流，并能与 `bochen-research-verifier` 顺序协作。
