# Bochen AI Skills

[![CI](https://github.com/bochensu0-web/bochen-ai-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/bochensu0-web/bochen-ai-skills/actions/workflows/ci.yml)

为苏博晨长期使用而设计的模块化私人 AI Skill 系统，覆盖日常回答、大学课程、代码算法、AI 数学、考试、学术写作、毕业论文、资料核验和技术操作。

## 设计目标

- 一个全局表达 Skill，多个职责清晰的专项 Skill
- 默认自然简洁中文、结论优先、少套话和低 AI 腔
- 面向基础可能薄弱、但希望真正理解并独立完成任务的大学 AI 学生
- 简单问题简答，复杂问题按直觉、机制、例子、练习与检查逐步深入
- 可以组合使用，同时避免重复规则、触发过宽和职责冲突
- 使用标准 `SKILL.md` 与 `agents/openai.yaml`，兼容 Antigravity、Codex、Claude Code 等客户端

## 目录

```text
bochen-ai-skills/
├── core/bochen-answer-style/
├── learning/
│   ├── bochen-learning-tutor/
│   ├── bochen-code-algorithm-tutor/
│   ├── bochen-ai-math-tutor/
│   └── bochen-exam-master/
├── academic/
│   ├── bochen-academic-writer/
│   └── bochen-cn-engineering-paper/
├── research/bochen-research-verifier/
├── utility/bochen-tech-guide/
├── meta/bochen-skill-builder/
├── scripts/
│   ├── install_skills.py
│   └── package_skills.py
├── tests/
├── examples/
├── evals/
└── docs/
```

## Skill 选择

| Skill | 主职责 | 不负责 |
| --- | --- | --- |
| `bochen-answer-style` | 所有回答的语言、结构、篇幅与自然度 | 具体学科工作流 |
| `bochen-learning-tutor` | 通用知识学习、例题、练习、理解检查 | 专项算法/AI 机制、考试规划 |
| `bochen-code-algorithm-tutor` | C++、Python、数据结构、算法、LeetCode、Debug | 纯数学推导、软件安装 |
| `bochen-ai-math-tutor` | 数学与 ML/DL/NLP/CV/RL/LLM 的连接 | 一般编程语法、考试时间规划 |
| `bochen-exam-master` | 提分策略、重点、错题、模拟题、开卷资料 | 无考试目标的长期学习 |
| `bochen-academic-writer` | 论文、报告、综述的写作、审阅与核查 | 独立事实检索、工科本科毕设全流程 |
| `bochen-cn-engineering-paper` | 中国工科本科毕设的选题、研究、实验、写作、终审与答辩 | 普通课程短论文、虚构研究材料 |
| `bochen-research-verifier` | 最新资料、事实核验、模型和产品比较 | 普通稳定知识讲解 |
| `bochen-tech-guide` | 软件、设备、GitHub、IDE 和环境排障 | 算法与学术写作 |
| `bochen-skill-builder` | 新 Skill 的设计、测试、打包和维护 | 一次性短提示 |

## 推荐组合

- 日常课程：`answer-style + learning-tutor`
- 算法学习：`answer-style + learning-tutor + code-algorithm-tutor`
- AI/数学学习：`answer-style + learning-tutor + ai-math-tutor`
- 算法考试：`answer-style + code-algorithm-tutor + exam-master`
- 机器学习考试：`answer-style + ai-math-tutor + exam-master`
- 课程论文：`answer-style + academic-writer + research-verifier`
- 工科毕业论文：`answer-style + cn-engineering-paper + research-verifier`

通常只需要一个全局 Skill 和一个专项 Skill。只有任务确实跨越学习、专项内容和考试时才同时启用三个，避免上下文膨胀。

## 安装

### 一键脚本安装（推荐）

支持直接安装到 **Antigravity**（`~/.gemini/config/skills`）、**Codex**（`~/.codex/skills`）、**Claude Code**（`~/.claude/skills`）或项目级 `.agents/skills`：

```bash
# 查看全部可用 Skill
python scripts/install_skills.py --list

# 安装全部 10 个 Skill 到 Antigravity / Codex / Claude Code
python scripts/install_skills.py --client antigravity
python scripts/install_skills.py --client codex
python scripts/install_skills.py --client claude

# 只安装指定子集到自定义目录
python scripts/install_skills.py --target ./.agents/skills --skills bochen-answer-style bochen-code-algorithm-tutor
```

### 手动安装

每个 Skill 均可独立复制安装：

```text
skill-name/
├── SKILL.md
├── README.md
└── agents/openai.yaml
```

## 校验与打包

```bash
# 全套结构、编码、链接、触发矩阵与评测集校验
python -m unittest discover -s tests -p "test_*.py" -v

# 中国工科毕业论文 Skill 审计脚本与场景测试
python -m unittest discover -s academic/bochen-cn-engineering-paper/tests -p "test_*.py" -v

# 重新生成不含 .git / 缓存文件的干净发行 ZIP
python scripts/package_skills.py
```

## 质量保证

- 全部 10 个 Skill 通过目录结构、YAML frontmatter、UTF-8 编码与本地链接完整性自动化测试
- 每个 Skill 均配备 `evals/*.json` 真实任务与相邻领域负样本，以及统一的 [`evals/TRIGGER-MATRIX.md`](evals/TRIGGER-MATRIX.md)
- 触发信息集中在 frontmatter `description`；公共风格集中在 `bochen-answer-style`，专项 Skill 不重复堆叠
- 学术和研究 Skill 禁止编造文献、数据、实验与引用
- 工科论文 Skill 内置北交大规范优先级、研究证据门槛、四个确定性只读审计脚本与真实场景测试
- 技术 Skill 对删除、覆盖、权限和凭据设置安全边界

设计依据与同类 Skill 对标见 [`docs/DESIGN-RESEARCH.md`](docs/DESIGN-RESEARCH.md)，组合示例见 [`examples/COMBINATIONS.md`](examples/COMBINATIONS.md)。

## License

MIT — 见 [`LICENSE`](LICENSE)。
