# 中国大学生开发环境配置与网络/编码/算力排障速查手册

指导国内网络下的包管理、GitHub 连接、Windows 编码路径、CUDA 显卡与远程 GPU 服务器操作时按需读取本文件。

---

## 1. 国内包管理与模型下载加速命令速查

### Python（优先推荐单次 `-i` 或独立 `.venv`，不污染系统全局 Python）
```powershell
# 单次使用清华源安装（最稳妥，不改全局配置）：
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# uv 虚拟环境创建与国内源加速（速度比传统 pip 快一个数量级）：
uv venv --python 3.12 .venv
uv pip install --python .venv -r requirements.txt --index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### PyTorch 带 CUDA 版本安装（防误装纯 CPU 版！）
国内镜像直接 `pip install torch` 在 Windows 上经常默认装成 `+cpu` 版本导致 `torch.cuda.is_available()` 为 `False`！
1. 先运行 `nvidia-smi` 看右上角 `CUDA Version: 12.x`（只要驱动支持的最高版本 $\ge$ PyTorch wheel 要求的版本即可，无需单独装 CUDA Toolkit）。
2. 指定官方 wheel 索引（如 `cu124`）下载，跑完立刻验证：
   ```powershell
   python -c "import torch; print(torch.__version__, 'CUDA:', torch.cuda.is_available())"
   ```

### 大模型与数据集下载（HuggingFace 超时自救）
- **首选方案**：查 **ModelScope（魔搭社区）** 是否有官方同步仓库（国内满速直连，无需任何代理）：
  ```python
  from modelscope import snapshot_download
  model_dir = snapshot_download("Qwen/Qwen2.5-7B-Instruct")
  ```
- **备选方案**：在运行脚本前设置环境变量走镜像站：
  - PowerShell：`$env:HF_ENDPOINT = "https://hf-mirror.com"`
  - Linux / macOS：`export HF_ENDPOINT=https://hf-mirror.com`

---

## 2. GitHub 连接与上传防坑清单

1. **`port 443: Timed out` 或 `Connection was reset` 排查顺序**：
   - 先查 Git 是否残留了早已关闭的旧本地代理端口：
     ```powershell
     git config --global --get http.proxy
     git config --global --get https.proxy
     ```
     若输出的端口当前并未运行代理软件，用 `git config --global --unset http.proxy` 清除；若正在使用本地代理，核对其实际监听的 HTTP 端口是否一致。
   - 若校园网屏蔽默认 SSH `22` 端口，可在 `~/.ssh/config` 中将 `github.com` 指向 `Hostname ssh.github.com` + `Port 443`。
2. **上传代码前必检三件事（防社死与防损坏）**：
   - **绝不用网页端 Upload files 拖拽多级项目文件夹**（会丢失空目录、压平嵌套路径或覆盖根目录同名 `README.md`）。
   - `git status` 检查是否误把 `.env`（含大模型 API Key）、`*.db`、`__pycache__/`、`.venv/` 或超过 `100MB` 的 `.pt` 模型权重加进暂存区（超过 100MB 会被 GitHub 服务端直接拒收且还残留在本地历史 commit 里，需 `git rm --cached` 清理）。

---

## 3. Windows 与远程 Linux GPU 服务器（AutoDL / 实验室）高频坑点

| 典型报错或症状 | 真实根因 | 一键修复方法 |
| --- | --- | --- |
| `UnicodeDecodeError: 'gbk' codec can't decode byte...` | Windows 中文系统下 Python `open()` 默认用 `cp936/gbk` 打开了 UTF-8 文件 | 所有 `open(..., encoding="utf-8")` 与 `Path.read_text(encoding="utf-8")` 显式指定编码；或设 `$env:PYTHONUTF8="1"` |
| PowerShell 运行 `.venv\Scripts\Activate.ps1` 报“在此系统上禁止运行脚本” | PowerShell 默认执行策略限制 | 运行 `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`（仅当前用户生效，安全可逆），或直接用 `.venv\Scripts\python.exe xxx.py` 免激活运行 |
| 脚本传到 Linux 报 `bash: ./start.sh: /bin/bash^M: bad interpreter` | Windows 回车换行 `\r\n`（CRLF）混入 shell 脚本 | 在仓库加 `.gitattributes`（`*.sh text eol=lf`），或在 Linux 下执行 `sed -i 's/\r$//' start.sh` |
| AutoDL / 实验室服务器连不上或 pip 报 `No space left on device` | 把缓存（`~/.cache/huggingface` / `pip`）和数据集塞爆了 30GB 系统盘 | 将 `HF_HOME`、`TORCH_HOME`、`TMPDIR` 及数据集目录全部软链或指到大容量数据盘（如 `/root/autodl-tmp`） |
| 笔记本一合盖 SSH 断开，跑了 4 小时的训练直接没了 | 进程挂在当前前台 SSH 会话下，收到 `SIGHUP` 退出 | 训练前先 `tmux new -s train` 进入持久会话再启动命令；断线重连后 `tmux attach -t train` 无缝找回输出 |
