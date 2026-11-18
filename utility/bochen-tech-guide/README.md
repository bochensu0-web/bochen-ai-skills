# bochen-tech-guide

面向中国大学生的开发环境配置与技术排障向导，深度适配国内网络镜像（`pip`/`uv`/`conda`/ModelScope/HF-Mirror）、GitHub 连接、Windows 中文路径/GBK/CRLF 陷阱、本地 PyTorch-CUDA 及 AutoDL/实验室远程服务器操作。

- **核心特点**：先零风险诊断再改单个变量；每步写明终端位置、预期回显与回退方式；截图问“点哪里”只指当前一步；内置凭据防泄漏与高危命令拦截。
- **不适用**：算法与代码逻辑推导（用 `bochen-code-algorithm-tutor`）、项目架构设计（用 `bochen-project-studio`）。

示例：`使用 $bochen-tech-guide，我在 Windows 上 pip install torch 装完后 torch.cuda.is_available() 显示 False，显卡是 RTX 4060，带我一步步排查修复。`
