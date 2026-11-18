# bochen-skill-builder

用于按 Agent Skills 标准设计、打磨、验证和打包个人模块化 Skill 套件的元构建器（兼容 Antigravity、Codex、Claude Code）。

- **核心特点**：强制正交职责边界与渐进式披露分层（`SKILL.md` + 一层按需 `references/` + 确定性 `scripts/`）；要求配套真实场景与近邻负样本 `evals/`；通过自动化测试守护结构、链接与干净打包。

示例：`使用 $bochen-skill-builder，审查我新写的 Skill 是否与现有 13 个 Skill 职责重叠，并帮我把冗余细节拆进按需加载的 references 模块。`
