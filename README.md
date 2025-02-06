# Polyfield Server Panel  [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

# 效果预览
![image](https://github.com/user-attachments/assets/244dc01d-d030-46bc-9737-d95e2b2bfa90)


## 🎉 欢迎使用 Polyfield Server Panel！ 🎉

您好！欢迎来到 **Polyfield Server Panel**，这是一个由 **SFSHC from AVD战队** 倾力打造的开源项目，旨在让您轻松管理和监控心爱的 [**Polyfield**](https://www.polyfield.net/) 游戏服务器。  我们深知搭建和维护游戏服务器的繁琐，因此开发了这款简洁、直观的 Web 控制面板，希望能帮助您摆脱命令行，享受更愉悦的服务器管理体验。

使用 Polyfield Server Panel，您可以：

*   🚀 一键启停服务器:  告别复杂的命令，轻松启动和停止您的 Polyfield 服务器进程。
*   📊 实时监控服务器状态:  CPU、内存占用一目了然，服务器运行状况尽在掌握。
*   📈  网络流量尽收眼底:  实时监控上传下载速度，累计流量清晰可见。
*   🗓️  每日流量精细记录:  每日流量使用情况一览无余，优化服务器资源更高效。
*   ⚙️  在线配置服务器参数:  无需 SSH 登录，直接在网页上编辑和保存 Polyfield 服务器配置文件 (`ServerConfig.txt`)。
*   🗺️  地图管理轻松搞定:  上传、解压、删除地图文件，管理地图从未如此简单。
*   📁  文件管理触手可及:  便捷浏览服务器文件，重命名、删除文件/文件夹，一切尽在指尖。

本项目完全开源，并采用 **GNU GPLv3 许可证**，我们衷心希望它能为 Polyfield 社区带来便利。如果您喜欢这个项目，欢迎 Star 和贡献！

## ✨ 功能亮点 ✨

*   🌈  美观易用:  基于 Bootstrap 4 框架精心设计，界面清新友好，响应式布局，各种设备完美适配。
*   🏠  实时数据呈现:  服务器资源和网络流量数据实时更新，状态一目了然。
*   📝  在线配置编辑:  通过 Web 界面轻松修改服务器配置，告别繁琐的手动编辑。
*   🗺️  便捷地图管理:  上传、解压、删除地图，管理 Polyfield 世界更方便。
*   🗂️  文件操作触手可及:  基本的文件管理功能，满足日常管理需求。
*   🔒  安全登录认证:  简单的密码登录，保护您的控制面板安全。
*   🗂️  详细操作日志:  记录服务器和面板操作日志，方便问题排查和审计。
*   📊  每日流量统计:  记录每日流量数据，帮助您合理规划和使用服务器资源。

## 🚀 快速上手指南 🚀

以下步骤将引导您快速安装和运行 Polyfield Server Panel。请务必仔细阅读，确保每一步都正确执行。

### 🚧  准备工作 🚧

在开始安装之前，请确保您已满足以下条件：

*   ✅  拥有 Linux 服务器 (VPS):  您需要一台运行 Linux 操作系统的服务器 (推荐 Ubuntu 或 Debian)。
*   ✅  安装了 Polyfield 游戏服务器:**  Polyfield 游戏服务器程序需要预先下载并准备好在您的服务器上运行。
*   ✅  安装了 Python 3.6+:**  服务器需要安装 Python 3.6 或更高版本 (推荐 Python 3.8+)。
*   ✅  安装了 pip:**  pip 是 Python 的包管理工具，通常 Python 3.x 会自带 pip。
*   ✅  网络连接畅通:**  服务器需要能够访问互联网以下载依赖包和资源。
*   # 注意：若未满足请自己搜索或询问AI

### 🛠️  安装步骤 (详细教程) 🛠️

**Step 1: 登录您的 Linux 服务器**

使用 SSH 客户端 (如 PuTTY, Termius 等) 登录您的 Linux 服务器。

**Step 2: 下载 Polyfield Server Panel 代码**

在您希望安装控制面板的目录下，使用 `git clone` 命令克隆代码仓库：

```bash
git clone https://github.com/SFSHC/Polyfield-Server-Panel.git  # 或者您创建的仓库地址
cd Polyfield-Server-Panel
```

**Step 3: 创建并激活 Python 虚拟环境 (推荐)**

为了隔离项目依赖，我们强烈建议您创建并激活 Python 虚拟环境：

```bash
python3 -m venv venv   # 创建名为 "venv" 的虚拟环境
source venv/bin/activate  # 激活虚拟环境 (Linux/macOS)
# 或者
venv\Scripts\activate  # 激活虚拟环境 (Windows 命令提示符)
# 或者
venv\Scripts\Activate.ps1 # 激活虚拟环境 (Windows PowerShell)
```

激活虚拟环境后，您的终端提示符前会显示 `(venv)`，表示您已进入虚拟环境。

**Step 4: 安装 Python 依赖包**

在虚拟环境中，使用 `pip` 安装项目所需的 Python 依赖包：

```bash
pip install -r requirements.txt
```

**Step 5: 配置 `server_config.ini` 文件**

*   **复制配置文件模板:**  复制项目根目录下的 `server_config.ini.template` 文件，并重命名为 `server_config.ini`：

    ```bash
    cp server_config.ini.template server_config.ini
    ```

*   **编辑配置文件:**  使用文本编辑器 (如 `nano` 或 `vim`) 打开 `server_config.ini` 文件，并根据您的服务器环境进行配置：

    ```bash
    nano server_config.ini  # 或者 vim server_config.ini
    ```

    您需要配置以下关键参数：

    *   **`config_file_path`**:  **Polyfield 服务器配置文件路径:**  填写您的 `ServerConfig.txt` 文件的完整路径。根据 Polyfield 官方文档，默认路径为：`/root/.config/unity3d/Mohammad Alizade/Polyfield/ServerConfig.txt`
    *   **`server_executable`**:  **Polyfield 服务器可执行文件路径:**  填写 Polyfield 服务器可执行文件的完整路径。例如：`/root/pf/Polyfield_v0.6_Linux.x86_64` (请根据您的实际版本和安装位置修改)。
    *   **`upload_folder`**:  **地图上传文件夹路径:**  通常为 Polyfield 服务器安装目录下的 `editor` 文件夹。例如：`/root/.config/unity3d/Mohammad Alizade/Polyfield/editor`
    *   **`secret_password`**:  **管理员登录密码:**  **请务必修改默认密码 `your_default_password` 为您自己的强密码！** 这是您登录控制面板的密码，请妥善保管。

    其他配置项 (如端口号、日志级别等) 可以根据您的需求进行修改。  **配置完成后，保存并关闭 `server_config.ini` 文件。**

**Step 6: 运行 Polyfield Server Panel**

在项目根目录下，运行 `pfpanel.py` (或 `web.py`) 启动控制面板：

```bash
python3 pfpanel.py  # 或者 python web.py
```

您应该看到类似 `* Running on http://0.0.0.0:9999/` 的信息，表示控制面板已成功启动，并监听在 `9999` 端口 (默认端口)。

**Step 7: 访问控制面板**

打开您的浏览器，访问 `http://您的服务器IP地址:9999` (请将 `您的服务器IP地址` 替换为您的服务器公网 IP 地址)。

您应该看到 Polyfield Server Panel 的登录页面。使用您在 `server_config.ini` 文件中设置的 `secret_password` 进行登录。

**恭喜！您已成功安装并启动 Polyfield Server Panel！ 🎉**  现在您可以开始使用控制面板管理您的 Polyfield 服务器了。

### ⚙️  服务端配置 (Polyfield Server)  [查看详细配置步骤 (中文翻译)](https://translate.google.com/translate?sl=en&tl=zh-CN&u=https://polyfield.net/builds/%2523README.txt)

Polyfield Server Panel 本身并不包含 Polyfield 服务器程序，您需要单独下载和配置 Polyfield 服务器。  以下步骤概述了如何配置 Polyfield 服务器 (详细步骤请参考 [Polyfield 官方 #README.txt 文档](https://polyfield.net/builds/%23README.txt) 的 [中文翻译版本](https://translate.google.com/translate?sl=en&tl=zh-CN&u=https://polyfield.net/builds/%2523README.txt))：

1.  下载 Polyfield 服务器程序 (Polyfield_v0.6_Linux.zip)。
2.  解压 zip 文件。
3.  给予执行权限 (chmod +x Polyfield_v0.6_Linux.x86_64)。
4.  创建 screen 会话并运行服务器程序。

### 💡  保持服务器后台运行 (使用 screen)**

为了使 Polyfield Server Panel 在您关闭 SSH 终端后仍然保持运行，我们推荐使用 `screen` 工具。

*   **安装 screen (如果尚未安装):**

    ```bash
    sudo apt-get update  # Debian/Ubuntu
    sudo apt-get install screen
    # 或者
    sudo yum update   # CentOS/RHEL
    sudo yum install screen
    ```

*   **创建 screen 会话并运行控制面板:**

    ```bash
    screen -S pfpanel  # 创建名为 "pfpanel" 的 screen 会话
    python3 pfpanel.py  # 在 screen 会话中运行控制面板
    ```

*   **分离 screen 会话:**  按下 **`Ctrl + A`** 键，然后按下 **`D`** 键。  终端会显示 `[detached from ****.pfpanel]`，表示您已成功分离 screen 会话，控制面板将在后台继续运行。

*   **重新连接 screen 会话:**  要重新查看控制面板的运行状态，可以使用以下命令重新连接到 screen 会话：

    ```bash
    screen -r pfpanel
    ```

*   **退出 screen 会话 (并停止控制面板):**  在连接到 screen 会话的状态下，按下 **`Ctrl + C`** 键可以停止控制面板程序，然后输入 `exit` 命令退出 screen 会话。

## 🔄  升级指南 🔄

如果您需要将 Polyfield Server Panel 更新到最新版本，请按照以下简单步骤操作：

1.  **进入项目目录:**

    ```bash
    cd Polyfield-Server-Panel
    ```

2.  **拉取最新代码:**

    ```bash
    git pull origin main  # 或者 git pull origin master，取决于您的远程分支名称
    ```

3.  **更新 Python 依赖 (如果 `requirements.txt` 文件有更新):**

    ```bash
    pip install --upgrade -r requirements.txt
    ```

4.  **重启控制面板:**  停止当前运行的 Polyfield Server Panel，并重新运行 `pfpanel.py` (或 `web.py`)。

## ⚠️  重要安全提示 ⚠️

*   🔑  修改默认密码:**  **请务必在首次使用时修改 `server_config.ini` 文件中的默认密码 `your_default_password` 为您自己的强密码！**  这是保护您的控制面板安全的第一步，也是最重要的一步。
*   🛡️  不要暴露在公网:**  **强烈建议不要将此控制面板直接暴露在公网环境下。**  当前版本仅实现了简单的密码登录认证，安全性相对较低。  如果必须对外提供访问，请务必采取额外的安全措施，例如配置防火墙、使用 VPN、启用 HTTPS 等。
*   🔒  妥善保管 `server_config.ini`:**  `server_config.ini` 文件包含您的管理员密码和服务器配置信息，请妥善保管，避免泄露。
*   📅  定期更新:**  请关注项目更新，及时更新到最新版本，以获取最新的功能和安全修复。

## 🐞  已知问题与待改进 🐞

*   🔒  安全性待增强:**  当前版本登录认证较为简单，未来版本可能会考虑引入更安全的认证机制，例如 HTTPS 协议、更复杂的权限管理等。
*   ⚠️  错误处理需完善:**  部分错误处理机制可能不够健壮，在某些异常情况下，可能会显示不友好的错误信息或导致程序崩溃。  欢迎您提交 Issue 报告您遇到的 Bug。
*   🛠️  功能仍需丰富:**  例如，服务器配置项的编辑功能目前较为基础，未来可以考虑开发更友好的表单界面，并增加配置项验证功能。  更多高级的服务器管理功能 (如 RCON 控制、玩家管理、Ban 列表管理等)  也在规划中，欢迎社区贡献代码。
*   📝  编码兼容性:**  在处理 zip 文件解压时，我们已尽力尝试检测和处理文件名编码问题，但可能仍然存在部分兼容性问题，尤其是在非 UTF-8 环境下。  如果您遇到解压乱码问题，请尝试将 zip 文件名编码转换为 UTF-8 格式。
*   📝  文档待完善:**  本项目文档仍在持续完善中，如果您在使用过程中遇到任何疑惑，或发现文档不足之处，欢迎提出建议。

当前版本: **v1.5.0**

## 🤝  贡献与协作 🤝

Polyfield Server Panel 是一个开源项目，我们非常欢迎社区的贡献和协作！  如果您有任何想法或建议，欢迎通过以下方式参与项目：

*   🐛  Bug 报告:**  如果您在使用过程中发现了任何 Bug，请在 GitHub Issues 中提交详细的 Bug 报告，包括复现步骤、错误信息、您的环境配置等，这将帮助我们更快地定位和修复问题。
*   💡  功能建议:**  如果您对 Polyfield Server Panel 有任何新的功能想法或改进建议，欢迎在 GitHub Issues 中提出 Feature Request。  您的建议将帮助我们更好地完善项目。
*   💻  代码贡献:**  如果您具备开发能力，并希望为 Polyfield Server Panel 贡献代码，修复 Bug 或实现新功能，我们非常欢迎您提交 Pull Request (PR)。  在提交 PR 之前，请先创建一个 Feature 分支，并在 PR 中清晰地描述您的修改内容和目的。
*   📝  文档改进:**  如果您发现 `README.md` 文档或其他文档存在不足或错误之处，欢迎帮助我们改进文档，使其更加清晰易懂。
*   🌍  翻译支持:**  如果您精通其他语言，欢迎帮助我们将控制面板界面和文档翻译成更多语言，让更多用户受益。

## 📜  许可证信息 📜

本项目使用 **GNU General Public License v3.0 (GPLv3)** 开源。

GPLv3 是一个强大的 **Copyleft 许可证**，它确保了用户拥有运行、复制、修改和分发软件的自由。  **请务必仔细阅读 GPLv3 许可证全文，了解其条款和约束。  尤其需要注意的是，基于本项目修改和衍生的作品也必须使用相同的 GPLv3 许可证开源。**

[**GNU General Public License v3.0 (GPLv3) 许可证全文 (英文原文)**](https://www.gnu.org/licenses/gpl-3.0)

您可以在项目根目录下的 `LICENSE` 文件中找到完整的许可证文本。

## 📞  联系我们 📞

*   作者: SFSHC from AVD战队
*   项目主页: [https://github.com/SFSHC/Polyfield-Server-Panel](https://github.com/SFSHC/Polyfield-Server-Panel)  (请替换为您实际的仓库地址)
*   GitHub: [https://github.com/SFSHC](https://github.com/SFSHC)
*   Polyfield 官网: [https://www.polyfield.net/](https://www.polyfield.net/)
*   Bilibili: [Bilibili](https://space.bilibili.com/1635006043)
*   邮箱 : sfshc@haudio.us.kg
**再次感谢您使用 Polyfield Server Panel!**  我们衷心希望这款控制面板能帮助您更好地管理您的 Polyfield 服务器，享受更畅快的游戏体验！  如有任何问题或建议，欢迎随时通过 GitHub Issues 与我们交流。

---
🛠️ **SFSHC from AVD战队 开发** 🛠️  (版本 v1.5.0)  © 2024-2025 SFSHC from AVD战队.  保留所有权利。
