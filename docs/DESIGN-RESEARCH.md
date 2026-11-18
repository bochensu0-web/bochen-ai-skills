# 设计调研与架构取舍

本套装在设计、首版发布与 v1.2 中国大学生全场景升级过程中，系统对标了官方 Agent Skills 规范、主流客户端定制机制（Antigravity / Codex / Claude Code）以及公开高星同类 Skill。核心原则是**提炼可验证的工作流结构与中国高校本土化经验，绝不复制第三方文本或堆砌无效空话**。

## 主要参考基线

- [Agent Skills specification](https://agentskills.io/specification)：采用标准 `SKILL.md`、高区分度 frontmatter `description` 触发与一层深度渐进式披露。
- [Anthropic skills / skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator)：吸收真实任务 eval、相邻领域近邻负样本（near-miss）与基于观察的小步迭代方法。
- [Anthropic K-12 teacher skills](https://github.com/anthropics/k12-teacher-skills) & [agent-teacher](https://github.com/JackyYang258/agent-teacher)：参考分层教学目标与“直觉—例子—陷阱—理解检查”紧凑闭环。
- [socrates-skill](https://github.com/RoundTable02/socrates-skill) & [learn-codebase](https://github.com/ktaletsk/learn-codebase)：吸收主动回忆与预测后揭示，但明确拒绝“永远只反问不解释”的教条，防止基础薄弱学生受挫。
- [exam-prep-learning-plan-builder](https://github.com/microsoft/cat-agent-skills/tree/main/submissions/exam-prep-learning-plan-builder)：参考按考试日期、材料与掌握度动态重算优先级。
- [PaperCraft](https://github.com/Kimogrant/PaperCraft) & [WenyuChiou academic research skills](https://github.com/WenyuChiou/academic-research-and-writing-skills)：参考主文件路由、按需加载 `references/` 模块、双向引用对齐与学术诚信硬门槛。
- [北京交通大学本科毕业设计（论文）规范与质量抽检办法](https://sse.bjtu.edu.cn/cms/item/1031.html) 与 [国家标准全文公开系统](https://openstd.samr.gov.cn/bzgk/std/std_list?p.p1=0&p.p2=GBT7713&p.p90=circulation_date&p.p91=desc)：确立“当届导师/学院模板 > 校级基线 > 现行国标（如 GB/T 7713.1—2025、GB/T 7714—2025）> 通用惯例”的规范优先级。

## 中国大学生全周期本土化适配（v1.2 核心升级）

通用英文 Skill 在中国高校场景下经常“水土不服”——不懂同济线代/严蔚敏数据结构记号痛点、不区分 LeetCode 核心代码模式与 PTA/蓝桥杯/CSP 的 ACM 标准流模式、不了解大创/综合实训课堂断网演示风险、不熟悉国内镜像网络与 AutoDL 算力环境，也缺少针对保研夏令营/预推免套磁与国内技术面“深挖简历”的防护。

因此本套件围绕中国 AI/计算机本科生四年完整成长链路构建 **7 大层 13 个正交 Skill**：

1. **教材与记号本土对齐**：在 `learning-tutor` 与 `ai-math-tutor` 中显式桥接同济高数/线代、浙大概统、408 核心课、西瓜书/统计学习方法与 PyTorch 张量维度。
2. **国内编程与考试生态全覆盖**：在 `code-algorithm-tutor` 与 `exam-master` 中内建 PTA 行末格式、CSP 子任务部分分、蓝桥杯 OI 赛制对拍、平时分核算与期末大题采分点步骤分模板。
3. **补齐实训竞赛、英文论文精读与升学求职三大断层**：
   - 新增 `bochen-project-studio`：承接课程设计、多人综合实训接口契约、课堂演示离线兜底与大创/数模/挑战杯。
   - 新增 `bochen-paper-reader`：承接顶会英文论文三遍精读、消融水分审计、Paper-to-Code 源码映射、毕设外文文献翻译纠错与实验室组会 8 页汇报骨架。
   - 新增 `bochen-career-grad-advisor`：承接日常/暑期实习与秋招 JD 拆解、四级证据阶梯简历审查（防 `Resume Attack` 穿帮）、以及保研夏令营/预推免定制套磁信与复试模拟。
4. **国内网络与信息去噪专治**：`tech-guide` 内建 `pip`/`uv`/ModelScope/HF-Mirror、GitHub 443 代理排障、Windows 中文路径/GBK/CRLF 与远程服务器 `tmux` 保活；`research-verifier` 强制穿透营销号与 CSDN 搬运帖，核对高校“届别 vs 自然年”与现行国标。
5. **全仓渐进式披露**：所有主 `SKILL.md` 控制在约 75–135 行，高密度细则下沉至各自 `references/*.md`（仅在命中对应子场景时按需读取），做到既深且轻。

## 有意坚持的“四不做”

- **不做“纯反问不给解释”**：基础薄弱时先给足直觉与最小算例，再用轻量检查题验证掌握度。
- **不做虚构与代造假**：严禁编造文献、DOI、实验数值、实习经历、并发指标或导师论文细节。
- **不做规避检测器噱头**：通过真实实验记录、具体工程权衡与自然中文表达消除空话，不搞同义词乱替。
- **不做跨文件重复规则**：公共中文语感与中英术语规范集中于 `bochen-answer-style`，专项 Skill 零重复。

## 持续验证机制

通过 `tests/test_suite_integrity.py` 与 `academic/bochen-cn-engineering-paper/tests/` 守护全部 13 个 Skill 的 frontmatter、UTF-8 编码、一层 `references/` 双向可达性、56+ 条正负向 `evals/*.json` 场景与无 `.git` 污染的确定性打包。
