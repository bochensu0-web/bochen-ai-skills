# Bochen AI Skills

[![CI](https://github.com/bochensu0-web/bochen-ai-skills/actions/workflows/ci.yml/badge.svg)](https://github.com/bochensu0-web/bochen-ai-skills/actions/workflows/ci.yml)

为苏博晨及中国大陆计算机/AI/工科大学生深度定制的模块化个人 Agent Skill 系统（v1.2），完整覆盖**大学四年全场景**：公共与专业课程学习、OJ/CSP/蓝桥杯机试算法、AI 数学与 PyTorch 机制、期末步骤分冲刺、课程综合实训与大创/数模竞赛、英文顶会论文精读与组会汇报、实验报告与本科毕业论文、保研套磁与技术实习求职、双语一手资料核验及国内开发环境排障。

## 核心设计特点

- **架构解耦，按需加载（Progressive Disclosure）**：1 个全局中文表达底座 + 12 个职责正交的专项 Skill；所有主 `SKILL.md` 保持精悍（约 75–135 行），教材记号对照表、OJ 防坑清单、组会汇报骨架、国内镜像命令等高密度资料下沉至一层 `references/` 模块按需读取。
- **深度本土化适配**：原生对接同济高数/线代、浙大概统、严蔚敏数据结构、408 四大件、西瓜书/统计学习方法、PTA/洛谷/蓝桥杯/CCF CSP、大创/数学建模、北交大本科毕设规范、现行国标（GB/T 7713.1—2025 / GB/T 7714—2025）、保研夏令营/预推免、国内技术实习面与 AutoDL/魔搭/国内镜像环境。
- **严守真实与可核验红线**：学术与论文严禁编造文献与实验数据；实训拒绝伪造在线模型推理结果；简历坚持“声明 vs 证据”分离，防面试深挖翻车；检索强制穿透营销号直查一手源。
- **多客户端即装即用**：兼容 **Antigravity**（`~/.gemini/config/skills` / `.agents/skills`）、**Codex**（`~/.codex/skills`）、**Claude Code**（`~/.claude/skills`）。

## 目录结构（7 层 13 Skill）

```text
bochen-ai-skills/
├── core/
│   └── bochen-answer-style/           # 全局中文表达、中英术语规范与低 AI 腔底座
├── learning/
│   ├── bochen-learning-tutor/         # 通用大学课程预习/补基（含高数/线代/概统/408 教材记号衔接）
│   ├── bochen-code-algorithm-tutor/   # C++/Python、数据结构与 LeetCode/PTA/洛谷/CSP/蓝桥杯算法排错
│   ├── bochen-ai-math-tutor/          # 工科数学 → 西瓜书/李航 → PyTorch/Transformer/LLM 公式与张量推导
│   └── bochen-exam-master/            # 期末复习排期、往年卷槽位拆解、主观/大题步骤分抢分与开卷速查表
├── engineering/
│   └── bochen-project-studio/         # 课程设计、多人综合实训接口契约、现场演示离线兜底与大创/数模竞赛
├── academic/
│   ├── bochen-paper-reader/           # 英文顶会论文精读、消融水分审视、公式—源码映射、外文翻译与组会汇报
│   ├── bochen-academic-writer/        # 理工科实验/上机报告、课程论文、文献综述与中英摘要润色
│   └── bochen-cn-engineering-paper/   # 中国工科本科毕设全生命周期（含北交大基线与 4 个只读审计脚本）
├── career/
│   └── bochen-career-grad-advisor/    # 技术实习/校招 JD 拆解、简历证据链防追问审查、保研套磁信与复试模拟
├── research/
│   └── bochen-research-verifier/      # 中英双轨检索、防营销号/搬运帖污染、高校届别通知/国标/模型参数核验
├── utility/
│   └── bochen-tech-guide/             # 国内镜像源、GitHub/HF/魔搭网络、Windows 中文路径/GBK、CUDA 与远程服务器排障
├── meta/
│   └── bochen-skill-builder/          # 模块化 Skill 边界设计、渐进式披露拆分、正负向评测与打包维护
├── scripts/                           # 跨客户端一键安装脚本与无污染确定性打包脚本
├── evals/                             # 全部 13 个 Skill 的真实场景与近邻负样本评测集 + 触发矩阵
├── examples/                          # 大学四年 11 类高频组合调用示例
├── docs/                              # 设计调研、架构取舍与本土化演进说明
└── tests/                             # 全仓结构、UTF-8、链接可达性、评测集与打包完整性测试
```

## Skill 快速选择表

| 当你遇到什么校园场景 | 启用哪个专项 Skill | 不负责什么（转交谁） |
| --- | --- | --- |
| 日常问答、方案对比、统一输出语感 | `bochen-answer-style` | 具体学科/工程工作流（叠加下方专项） |
| 高数/线代/概统/408 课上没听懂、教材定义太抽象 | `bochen-learning-tutor` | OJ 代码调试（`code-algorithm-tutor`） |
| 刷 PTA/洛谷/LeetCode/CSP、代码 WA/TLE/段错误 | `bochen-code-algorithm-tutor` | 深度学习张量求导（`ai-math-tutor`） |
| 看懂西瓜书/Transformer/LoRA 公式与 PyTorch `shape` | `bochen-ai-math-tutor` | 显卡驱动安装排错（`tech-guide`） |
| 期末剩 2 天救命、刷高 GPA、拆往年卷、做一页开卷纸 | `bochen-exam-master` | 无考试期限的系统学习（`learning-tutor`） |
| 3 人组队做课程综合实训、写大创立项结题、打数模比赛 | `bochen-project-studio` | 大四个人本科毕业论文（`cn-engineering-paper`） |
| 精读英文顶会论文、对照开源代码、准备周五组会 PPT | `bochen-paper-reader` | 撰写自己的实验报告（`academic-writer`） |
| 写/改专业课实验报告、课程小论文、修正英文摘要 Chinglish | `bochen-academic-writer` | 本科毕设全流程与抽检终审（`cn-engineering-paper`） |
| 推进本科毕业设计（选题→开题→实验→引用图表审计→答辩） | `bochen-cn-engineering-paper` | 日常短篇课程作业（`academic-writer`） |
| 拆解实习/秋招 JD、改简历防面试深挖、写保研预推免套磁信 | `bochen-career-grad-advisor` | 期末课程复习（`exam-master`） |
| 查当届高校政策、现行国标版本、核实文献真伪与最新模型定价 | `bochen-research-verifier` | 润色已有段落（`academic-writer`） |
| 配环境换源、GitHub 443、Windows 编码报错、连 AutoDL 算力机 | `bochen-tech-guide` | 算法逻辑推导（`code-algorithm-tutor`） |
| 新建、合并、打磨或审查个人 Skill 套件 | `bochen-skill-builder` | 一次性短提示词 |

## 黄金组合配方

- **日常课程与刷题**：`answer-style + learning-tutor`（或 `code-algorithm-tutor` / `ai-math-tutor`）
- **期末高效冲刺**：`answer-style + exam-master` + 对应学科导师（`learning` / `code` / `ai-math`）
- **课程实训与大创竞赛**：`answer-style + project-studio + tech-guide`
- **进组科研与组会**：`answer-style + paper-reader + ai-math-tutor`
- **本科毕业设计**：`answer-style + cn-engineering-paper + paper-reader / research-verifier`
- **保研夏令营与技术实习**：`answer-style + career-grad-advisor + research-verifier`

具体提示词示范见 [`examples/COMBINATIONS.md`](examples/COMBINATIONS.md)，设计依据见 [`docs/DESIGN-RESEARCH.md`](docs/DESIGN-RESEARCH.md)。

## 安装方式

### 一键脚本安装（支持全量或按场景预设安装）

```bash
# 查看全部 13 个 Skill 与预设包（all / daily-study / research-thesis / project-career）
python scripts/install_skills.py --list

# 全量安装到 Antigravity / Codex / Claude Code
python scripts/install_skills.py --client antigravity
python scripts/install_skills.py --client codex
python scripts/install_skills.py --client claude

# 仅安装某一场景预设（如科研毕设包或实训求职包）
python scripts/install_skills.py --client antigravity --preset research-thesis
python scripts/install_skills.py --client antigravity --preset project-career
```

### 手动复制安装

将任意单个 Skill 目录复制到客户端对应的 `skills/` 目录下即可独立工作（务必连同子目录 `references/`、`scripts/`、`agents/` 一并复制）。

## 自动化测试与重新打包

```bash
# 全仓 13 个 Skill 结构、UTF-8、references 双向链接、触发矩阵与 56+ 条评测集校验
python -m unittest discover -s tests -p "test_*.py" -v

# 中国工科本科论文 Skill 四个确定性审计脚本与场景测试
python -m unittest discover -s academic/bochen-cn-engineering-paper/tests -p "test_*.py" -v

# 重新生成不含 .git / 缓存文件的 14 个干净发行 ZIP
python scripts/package_skills.py
```

## License

MIT — 见 [`LICENSE`](LICENSE)。
