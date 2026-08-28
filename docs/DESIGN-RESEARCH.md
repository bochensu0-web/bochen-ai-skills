# 设计调研与取舍

本套装在定稿前对标了官方 Agent Skills 规范、官方示例和多个公开同类 Skill。目标是提炼可靠模式，不复制第三方文本。

## 主要参考

- [Agent Skills specification](https://github.com/agentskills/agentskills)：采用标准 `SKILL.md`、触发描述与渐进式披露。
- [Anthropic skills / skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator)：吸收真实任务 eval、触发正负样本和迭代验证方法。
- [Anthropic K-12 teacher skills](https://github.com/anthropics/k12-teacher-skills)：参考分层教学、可观察学习目标和评估思路。
- [agent-teacher](https://github.com/JackyYang258/agent-teacher)：参考“先判断是否真的是教学任务”、直觉—例子—陷阱—检查的紧凑课程骨架。
- [socrates-skill](https://github.com/RoundTable02/socrates-skill)：吸收逐步提问、根据回答调难度和最后复述；没有采用“永远不直接回答”的极端规则。
- [learn-codebase](https://github.com/ktaletsk/learn-codebase)：参考预测后揭示、主动回忆和掌握度跟踪。
- [exam-prep-learning-plan-builder](https://github.com/microsoft/cat-agent-skills/tree/main/submissions/exam-prep-learning-plan-builder)：参考按日期、可用时间、材料和信心动态调整计划。
- [Academic Research Agent Skill](https://github.com/ngtiendong/Academic-Research-Agent-Skill)：参考证据、推断和研究假设分离，以及人类保留最终判断。
- [researcher_agent research skill](https://github.com/drader/researcher_agent/tree/main/skills/research)：参考多种研究模式、明确 in-scope/out-of-scope 和来源核验。
- [GOV.UK style skill](https://github.com/lelouvincx/agent-skills/tree/main/skills/govuk-style)：参考结论前置、具体用词、一句一意和删除无信息内容。
- [general-writing](https://github.com/msimchowitz/writing-skills/tree/main/for-agents/general-writing)：参考保留作者原意与个人声音、做最小有效修改。
- [skill-forge](https://github.com/bm629/agent-skills/tree/main/skills/skill-forge)：参考先寻找现有 Skill、核验来源，再合成和迭代。
- [PaperCraft](https://github.com/Kimogrant/PaperCraft)：为工科毕业论文 Skill 参考主文件路由、渐进式模块和诚信停止门槛。
- [WenyuChiou academic research and writing skills](https://github.com/WenyuChiou/academic-research-and-writing-skills)：参考研究问题、证据驱动写作、双向对齐和多轮终审。
- [北京交通大学本科毕业设计（论文）规范与质量抽检办法](https://sse.bjtu.edu.cn/cms/item/1031.html)：用于 `bochen-cn-engineering-paper` 的 2024 校级基线，并明确当届学院/导师要求优先。
- [国家标准全文公开系统](https://openstd.samr.gov.cn/bzgk/std/std_list?p.p1=0&p.p2=GBT7713&p.p90=circulation_date&p.p91=desc)：核对 2026 年现行学位论文和参考文献标准，避免沿用已废止版本。

## 吸收的设计

1. **触发靠描述，不靠正文标题**：frontmatter 同时写清能力、典型任务和用户常用说法。
2. **先判任务类型**：理解概念、修复代码、备考、写作和核验不能混成同一流程。
3. **主动学习而非答案倾倒**：先给必要解释，再让用户预测、补全、手算或复述。
4. **提示逐步撤掉**：从完整例题过渡到半开放和独立练习。
5. **说明不适用场景**：通过 near-miss eval 避免多个 Skill 抢同一任务。
6. **计划动态重排**：考试时间、范围或掌握度变化时重新计算优先级。
7. **研究可审计**：区分已检查证据、来源中的说法、综合推断和未知项。
8. **短核心 + 按需资源**：当前规则规模足够小，不添加无实际用途的脚本或大参考库。

## 有意没有采用

- 不采用“永远只提问不回答”，因为基础薄弱时可能造成额外挫败。
- 不采用几十个角色或多 Agent 流程，避免简单本科任务被过度工程化。
- 不把“减少 AI 味”写成规避检测器；只通过真实证据、个人判断和自然表达改善质量。
- 不为每个 Skill 重复全局语言规则；统一交给 `bochen-answer-style`。
- 不使用单一固定输出模板；根据任务复杂度选择最小结构。

## 后续迭代方法

使用 `evals/` 中的真实任务和相邻领域负样本测试触发与输出。每次更新只针对观察到的问题修改，记录触发准确性、解释完整性、篇幅、可执行性和事实可靠性。
