# 设计调研记录

## 调研目标

在编写本 Skill 前，比较公开的论文研究/写作 Skills、官方 Agent Skills 规范和北京交通大学现行要求。只吸收工作流思想，不复制第三方表述。

调研与核验日期：2026-08-28。

## 同类 Skill 对比

### Academic Research Agent Skill

来源：[ngtiendong/Academic-Research-Agent-Skill](https://github.com/ngtiendong/Academic-Research-Agent-Skill)

值得吸收：研究范围、创新性、试验可行性、主张证据和审稿模拟等阶段门槛；强调人类保留最终判断。未直接采用其偏研究发表的复杂多 Agent 结构，因为本科毕设需要更紧凑的导师协作和院校流程。

### PaperCraft

来源：[Kimogrant/PaperCraft](https://github.com/Kimogrant/PaperCraft)

值得吸收：主文件负责路由、参考模块渐进式加载；对引文可核验与学术诚信设置停止门槛；覆盖中文论文。未采用其大量模块和复杂命令系统，避免简单局部任务上下文过重。

### Research Writing Skill

来源：[zLanqing/research-writing-skill](https://github.com/zLanqing/research-writing-skill)

值得吸收：保留事实、公式和引文；区分来源材料、确认事实、推断和建议扩展；先论证骨架后成文。本 Skill 将其扩展为五种证据状态和论文契约。

### WenyuChiou Academic Research & Writing Skills

来源：[WenyuChiou/academic-research-and-writing-skills](https://github.com/WenyuChiou/academic-research-and-writing-skills)

值得吸收：从问题定义到证据驱动写作、双向对齐、多轮审查和投稿/答辩的完整生命周期。结合本科场景后，转化为“任务书—研究问题—方法—结果—结论”的闭环检查。

## Agent Skills 规范

- [Agent Skills specification](https://agentskills.io/specification)：采用 `SKILL.md`、`name`/`description` frontmatter、64 字符名称限制和渐进式披露。
- [OpenAI Skills](https://github.com/openai/skills)：参考官方 skill-creator 的初始化、验证和 UI 元数据做法。
- [Anthropic Skills](https://github.com/anthropics/skills/tree/main/skills/skill-creator)：参考触发描述、真实任务 eval、按观察迭代和不要把所有知识塞入主文件。

## 北京交通大学与国家规范

- 北京交通大学软件学院，2024-09-20：[本科毕业设计（论文）规范与质量抽检办法](https://sse.bjtu.edu.cn/cms/item/1031.html)
- 校级办法 [PDF](https://rjxy.bjtu.edu.cn/media/attachments/2024/10/20241012161205.pdf)
- 北京交通大学本科生院，2024-05-10：[2024 届工作推进会](https://bksy.bjtu.edu.cn/news/638509558889536169.html)
- 教育部：[本科毕业论文（设计）抽检办法（试行）](https://www.moe.gov.cn/srcsite/A11/s7057/202101/t20210107_509019.html)
- 国家标准全文公开系统：[GB/T 7713.1—2025、GB/T 7713.2—2022 检索](https://openstd.samr.gov.cn/bzgk/std/std_list?p.p1=0&p.p2=GBT7713&p.p90=circulation_date&p.p91=desc)
- 国家标准全文公开系统：[GB/T 7714—2025](https://openstd.samr.gov.cn/bzgk/std/newGbInfo?hcno=C6CE52E55AC09B9C79A20AEA77CEDD14)

关键发现：2026 年现行国家标准已发生变化，`GB/T 7713.1—2025` 和 `GB/T 7714—2025` 均已实施，而很多旧模板和公开教程仍引用旧版。因此本 Skill 不把通用旧格式写死，强制按来源层级和日期核验。

## 最终架构取舍

1. `SKILL.md` 只保留触发、边界、论文契约、来源优先级、阶段路由和硬门槛。
2. 12 个参考模块按任务加载，避免每次都注入院校细节和完整方法库。
3. 四个脚本只做可解释的确定性审计，不充当查重、AI 检测或事实判定器。
4. 与 `bochen-academic-writer` 分工：一般写作归后者，中国工科本科毕设全生命周期归本 Skill。
5. 不设置固定“万能论文模板”，而是按成果类型选择章节功能并服从学校/学院模板。
6. 不用文献数量、语言流畅度或检测分数替代研究真实性和证据链。

## 后续维护

每届毕设开始前核验北交大本科生院和用户所在学院通知；国家标准状态至少每年核验一次。观察真实任务中是否出现触发冲突、过度提问、模块遗漏或脚本误报，再以小版本更新，不无依据扩张文件。
