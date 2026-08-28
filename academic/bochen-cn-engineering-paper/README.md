# bochen-cn-engineering-paper

面向苏博晨及中国大陆高校工科本科生的毕业设计（论文）全流程 Agent Skill，重点适配北京交通大学，尤其适合人工智能、计算机、软件工程、自动化、数据科学与算法方向。

## 什么时候用

- 评估和收敛毕业设计选题
- 写任务书、开题报告、文献综述和研究计划
- 设计算法实验、软件系统、工程验证或数据分析
- 修改论文结构、摘要、正文、图表、公式和参考文献
- 做中期检查、终稿审计、抽检准备和答辩准备

普通课程论文或只修改一小段文字，使用 `bochen-academic-writer` 更轻；需要查最新文献、政策或产品信息时，与 `bochen-research-verifier` 组合。

## 调用示例

```text
使用 $bochen-cn-engineering-paper，帮我判断这个 AI 本科毕设题目是否能在 12 周内完成。
```

```text
使用 $bochen-cn-engineering-paper，按北交大要求检查我的开题报告，先列必须修改项。
```

```text
使用 $bochen-cn-engineering-paper，审计这份算法论文的实验公平性、引用和图表一致性。
```

## 设计特点

- 用“论文契约”锁定学校、阶段、研究问题、证据、约束和本轮交付物
- 按选题、文献、方法、实施、写作、终审和答辩推进完整生命周期
- 严格区分已核验事实、用户材料、推断、待核验项和建议方案
- 绝不编造文献、DOI、数据、实验、结果、图表或导师意见
- 主文件保持紧凑，院校规范与专项方法按需加载
- 附带四个只读审计脚本、常用模板和八类真实场景评测

## 北京交通大学适配

内置 2024 年发布的《北京交通大学本科毕业设计（论文）规范与质量抽检办法》基线，同时要求每次优先采用用户提供的导师模板和当届学院通知。由于提交时间、查重阈值、学院评分和模板可能按届变化，Skill 不会把这些动态要求永久写死。

## 目录

```text
bochen-cn-engineering-paper/
├── SKILL.md
├── README.md
├── VERSION
├── agents/openai.yaml
├── references/
├── scripts/
├── examples/
└── tests/
```

## 审计脚本

```text
python scripts/reference_audit.py paper.md
python scripts/citation_consistency_check.py paper.md
python scripts/academic_style_lint.py paper.md
python scripts/figure_table_audit.py paper.md
```

这些脚本提供编号、双向引用、占位符、空泛表达、图表编号等确定性提示。它们不是查重工具、AIGC 检测器或最终学术判断。

## 版本

当前版本：`1.0.0`。设计依据、来源日期和同类 Skill 对比见 `references/design-research-note.md`。
