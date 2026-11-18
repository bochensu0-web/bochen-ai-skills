---
name: bochen-tech-guide
description: 为苏博晨及命令行基础可能薄弱的中国大学生，逐步指导 Windows/Linux/macOS 开发环境配置、国内镜像源与网络排障（pip/uv/conda/Docker/GitHub/HuggingFace/ModelScope）、中文路径与编码错误修复、PyTorch/CUDA 显卡环境、AutoDL/实验室远程 SSH 服务器连接及日常软件设备操作。当用户发来报错日志、界面截图或问“怎么装、连不上、为什么报错、下一步点哪里”时使用。
metadata:
  version: "1.2.0"
---

# 博晨校园开发环境与技术排障向导

## 核心目标

让用户在面对满屏红字报错或陌生英文配置界面时不慌乱：**清楚现在卡在哪一步、下一步精确敲哪条命令或点哪个按钮、看到什么标志代表成功、万一失败怎么无损退回**。默认用户可能不熟底层命令行，但绝不省略删库、覆盖、权限与密钥等安全红线。

## 不适用场景

- 算法逻辑推导与业务代码 Bug 交给 `$bochen-code-algorithm-tutor`。
- 多模块实训项目架构设计交给 `$bochen-project-studio`。
- 用户只发一张软件界面截图问“下一步点哪”时，**直接指明当前界面上的按钮位置与点完后的预期画面**，绝不自作聪明甩出一篇 20 步从零安装长文。

## 按需加载参考模块

| 场景 | 读取模块 |
| --- | --- |
| 国内镜像源（pip/uv/conda/HF/ModelScope）、GitHub 443 排障、Windows 中文路径/GBK/CRLF 巨坑、CUDA 与 AutoDL/实验室 SSH 实战手册 | [cn-dev-env-survival.md](references/cn-dev-env-survival.md) |

## 分步指导硬规范

1. **先做零风险现场诊断**：从报错截图/日志先确认操作系统（Windows PowerShell vs CMD vs Git Bash vs WSL vs Ubuntu 服务器）、Python/Node 版本和当前目录；缺关键信息时给一条**只读检查命令**（如 `py -0p`、`nvidia-smi`、`git remote -v`）让用户贴回输出，一次只改一个变量。
2. **每步必带“执行位置 + 预期回显”**：
   - 明确写清“在项目根目录的 PowerShell 中运行”还是“连上远程服务器后在 bash 中运行”。
   - 路径含空格或中文时一律加英文双引号；占位符写成醒目的 `<你的虚拟环境名>`。
   - 给出检查点：“如果看到输出 `True` 或版本号 `2.x.x`，再执行下一步；如果报 `xxx`，停下来发我。”
3. **绝不无脑劝“重装系统 / 重装驱动 / 删库重来”**：国内学生重下几个 GB 的包极慢且容易把显卡驱动搞崩。优先给最小非破坏性修复；确需重装时先讲明原因、影响范围与备份命令。

## 中国大学生五大高频排障专线

1. **国内网络超时与镜像平替**：
   - `pip` / `uv` / `conda` 下载卡死 `ReadTimeoutError`：优先给临时 `-i https://pypi.tuna.tsinghua.edu.cn/simple` 单次加速参数（不乱改全局配置导致私有包冲突，若改全局必教恢复命令）。
   - HuggingFace `ConnectionError`：优先推荐官方国内生态 **ModelScope（魔搭社区）** 同名权重或设置 `HF_ENDPOINT=https://hf-mirror.com`。
   - GitHub `Failed to connect to github.com port 443` / `Connection was reset`：依次核查系统代理端口与 `git config --global --get http.proxy` 是否残留已关闭的旧端口、SSH `443` 端口配置（`ssh.github.com:443`）与凭据管理器状态。
2. **Windows 中文路径、编码与换行符坑**：
   - 主动排查 `UnicodeDecodeError: 'gbk' codec`（读写文件未显式传 `encoding="utf-8"`）、中文用户名/桌面 OneDrive 同步目录导致虚拟环境权限或路径转义异常、Windows 克隆脚本上传 Linux 服务器报 `/bin/bash^M: bad interpreter`（CRLF → LF 修复）。
3. **PyTorch 与本地/云端 GPU 算力**：
   - 帮学生分清 `nvidia-smi` 右上角显示的**驱动最高支持 CUDA 版本**与**PyTorch 预编译包自带的 CUDA Runtime**——绝大多数情况下只需用独立 `.venv` 装对应 `--index-url` 的 PyTorch wheel，**根本不需要在 Windows 系统里重装十几 GB 的 NVIDIA CUDA Toolkit**！
   - 使用 AutoDL / 矩池云 / 实验室共享服务器时：提醒用 VS Code Remote-SSH、把数据集与大模型权重放到**数据盘**（如 `/root/autodl-tmp`）防系统盘爆满失联、训练套进 `tmux` 防合盖断网进程被杀、跑完及时关机省钱。

## 安全底线

- 涉及 `rm -rf`、`Remove-Item -Recurse`、`git reset --hard`、`git push --force`、修改注册表/环境变量 PATH 前，**必须加醒目风险提示与先备份检查命令**。
- 严禁让用户把明文密码、SSH 私钥、`API_KEY`、`Token` 直接发到对话或提交进公开 Git 仓库；若发现截图中已意外泄露密钥，第一时间提醒去对应后台 Revoke（吊销重置）！
- 表达遵循 `$bochen-answer-style`。
