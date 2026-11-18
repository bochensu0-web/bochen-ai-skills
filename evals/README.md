# Evals

每个 JSON 文件包含真实任务、预期行为与易混淆场景。测试时分别运行“启用对应 Skill”和“不启用 Skill”的版本，比较：结论是否前置、机制是否清楚、篇幅是否匹配、是否出现职责越界、是否给出可验证下一步。

`TRIGGER-MATRIX.md` 用于检查 should-trigger 与 should-not-trigger，优先关注相邻 Skill 之间的误触发。
