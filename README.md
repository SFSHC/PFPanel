# Polyfield Server Panel  [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0) <!-- GPLv3 License Badge -->

<!-- 项目 Logo (可选，如果你的项目有 Logo，可以放在这里) -->
<!-- 例如： ![Project Logo](path/to/your/logo.png) -->

## 项目简介

**Polyfield Server Panel**  是一个基于 Web 的控制面板，旨在方便用户管理和监控 [**Polyfield**](https://store.steampowered.com/app/1935200/Polyfield/) 游戏服务器。 它提供了一个简洁直观的界面，允许你：

*   **服务器控制:** 启动、停止 Polyfield 服务器进程。
*   **服务器状态监控:**  实时查看 CPU 和内存使用率、服务器运行状态。
*   **网络使用情况监控:**  查看累计上传/下载流量、实时上传/下载速度。
*   **每日流量记录:**  查看每日的流量使用历史。
*   **服务器配置管理:**  在线编辑和保存 Polyfield 服务器配置文件 (`ServerConfig.txt`)。
*   **地图管理:**  上传新的地图文件 (zip 格式)、解压地图文件、删除地图文件。
*   **文件管理:**  浏览服务器文件系统 (上传地图的文件夹)，重命名和删除文件/文件夹。

本项目由 **SFSHC from AVD战队** 制作并开源，旨在为 Polyfield 社区提供一个易于使用、功能全面的服务器管理工具。  本项目使用 **GNU GPLv3 许可证** 开源，这意味着基于本项目修改和衍生的作品也必须使用相同的许可证开源 (Copyleft)。

## 功能特性

*   **简洁易用的 Web 界面:**  基于 Bootstrap 4 框架，界面美观、响应式设计，易于操作。
*   **实时服务器监控:**  即时更新服务器资源使用情况和网络流量数据。
*   **灵活的配置管理:**  在线编辑服务器配置文件，无需手动 SSH 连接服务器。
*   **便捷的地图管理:**  通过 Web 界面轻松上传和管理地图文件。
*   **基本文件管理功能:**  方便地浏览和管理服务器文件。
*   **登录认证:**  简单的密码登录保护，确保控制面板的安全性。
*   **详细的日志记录:**  记录服务器操作和 Web 应用日志，方便问题排查。
*   **每日流量统计:**  记录每日的上传和下载流量，帮助用户了解服务器流量使用情况。

## 快速开始

### 前提条件

*   **Python 3.6+**  (推荐使用 Python 3.8 或更高版本)
*   **pip** (Python 包管理工具，通常 Python 3.x 自带)
*   **Polyfield 游戏服务器**  已安装并可运行在你的服务器上。
*   **Font Awesome 图标库** (已通过 CDN 引入，无需额外安装，但需要网络连接)

### 安装步骤

1.  **克隆仓库:**

    ```bash
    git clone https://github.com/SFSHC/Polyfield-Server-Panel.git  # 或者你创建的仓库地址
    cd Polyfield-Server-Panel
    ```

2.  **创建并激活 Python 虚拟环境 (推荐):**

    ```bash
    python3 -m venv venv   # 创建虚拟环境
    source venv/bin/activate  # Linux/macOS
    venv\Scripts\activate  # Windows (命令提示符)
    venv\Scripts\Activate.ps1 # Windows (PowerShell)
    ```

3.  **安装 Python 依赖包:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **配置 `server_config.ini` 文件:**

    *   复制 `server_config.ini.template` 文件并重命名为 `server_config.ini`。
    *   编辑 `server_config.ini` 文件，根据你的服务器环境配置以下参数:
        *   `config_file_path`:  Polyfield 服务器配置文件 `ServerConfig.txt` 的完整路径。
        *   `server_executable`: Polyfield 服务器可执行文件 (`PolyfieldServer.x86_64` 或 `Polyfield_v[版本号]_Linux.x86_64`) 的完整路径。
        *   `upload_folder`: 地图上传文件夹的完整路径 (通常是 Polyfield 服务器安装目录下的 `editor` 文件夹)。
        *   `secret_password`:  **请务必修改默认密码为你自己的强密码！**  这是控制面板的登录密码。
        *   其他配置项 (端口号、日志级别等) 可以根据需要修改。

    **重要安全提示:**  请务必修改 `server_config.ini` 中的默认密码 `your_default_password` 为你自己的强密码，并妥善保管 `server_config.ini` 文件。

5.  **创建 `LICENSE` 文件并添加 GPLv3 许可证文本:**

    *   在项目根目录下创建一个名为 `LICENSE` 的文件 (无后缀名)。
    *   将 **完整的 GNU GPLv3 许可证文本** 复制粘贴到 `LICENSE` 文件中 (许可证文本请参考下面的 **步骤 2**)。

6.  **运行控制面板:**

    ```bash
    python3 pfpanel.py  # 或者 python web.py，取决于你的主程序文件名
    ```

    控制面板默认会在 `http://服务器IP地址:9999` 运行 (端口号可在 `server_config.ini` 中修改)。

7.  **登录控制面板:**
    *   在浏览器中访问 `http://服务器IP地址:9999`。
    *   使用你在 `server_config.ini` 中设置的 `secret_password` 进行登录。

### 升级步骤

如果你需要更新控制面板到最新版本，可以按照以下步骤操作：

1.  **进入项目目录:**

    ```bash
    cd Polyfield-Server-Panel
    ```

2.  **拉取最新代码:**

    ```bash
    git pull origin main  # 或者 git pull origin master，取决于你的远程分支名
    ```

3.  **更新 Python 依赖 (如果 `requirements.txt` 文件有更新):**

    ```bash
    pip install --upgrade -r requirements.txt
    ```

4.  **重启控制面板:**  停止并重新运行 `pfpanel.py` (或 `web.py`)。

## 已知问题和限制

*   **安全性:**  当前版本只实现了简单的密码登录认证，安全性相对较低。  **强烈建议不要将此控制面板直接暴露在公网环境下。**  未来版本可能会考虑增加更安全的认证方式 (例如 HTTPS、更复杂的权限管理)。
*   **错误处理:**  部分错误处理可能不够完善，某些情况下可能会显示不友好的错误信息或崩溃。  欢迎提交 Issue 报告 Bug。
*   **功能待完善:**  例如，服务器配置项的编辑功能目前是简单的文本框输入，未来可以考虑更友好的表单界面和配置项验证。  更多高级的服务器管理功能 (例如 RCON 控制、玩家管理、Ban 列表管理等)  尚未实现，欢迎贡献代码。
*   **编码问题:**  在处理 zip 文件解压时，尽力尝试检测和处理文件名编码问题，但可能仍然存在兼容性问题，尤其是在非 UTF-8 环境下。 如果遇到解压乱码问题，请尝试将 zip 文件名编码转换为 UTF-8。
*   **GPLv3 许可证限制:**  本项目使用 GNU GPLv3 许可证，请注意 GPLv3 的 "Copyleft" 特性。  **基于本项目修改和衍生的作品也必须使用相同的 GPLv3 许可证开源。**  如果你的项目计划包含闭源或商业用途的组件，请仔细评估 GPLv3 许可证的适用性。

## 贡献

欢迎任何形式的贡献，包括但不限于：

*   **提交 Bug 报告:**  如果在使用过程中发现 Bug，请在 GitHub Issues 中提交详细的 Bug 报告，包括复现步骤、错误信息等。
*   **提交功能建议:**  如果你有新的功能建议或改进意见，欢迎在 GitHub Issues 中提出。
*   **提交代码贡献 (Pull Request):**  如果你有能力修复 Bug 或实现新功能，欢迎提交 Pull Request。  提交 PR 前请先创建一个 Feature 分支，并在 PR 中清晰描述你的修改内容。
*   **完善文档:**  帮助改进 `README.md` 文档，使其更加清晰易懂。
*   **翻译:**  将控制面板界面和文档翻译成其他语言。

## License

本项目使用 **GNU General Public License v3.0 (GPLv3)** 开源。  GPLv3 是一个 Copyleft 许可证，这意味着基于本项目修改和衍生的作品也必须使用相同的许可证开源。  **请务必仔细阅读 GPLv3 许可证全文，了解其条款和约束。**

[**GNU General Public License v3.0 (GPLv3) 许可证全文**](https://www.gnu.org/licenses/gpl-3.0)

你可以在项目根目录下的 `LICENSE` 文件中找到完整的许可证文本。

## 联系方式

*   **作者:** SFSHC from AVD战队
*   **GitHub:** [https://github.com/SFSHC](https://github.com/SFSHC)
*   **Bilibili:** [YOUR_BILIBILI_PROFILE_URL]  **(请替换为你的 B 站主页链接)**
*   **邮箱 (可选):**  [你的邮箱地址 (可选)]

**感谢使用 Polyfield Server Panel!**  希望这个控制面板能帮助你更好地管理你的 Polyfield 服务器。 如果有任何问题或建议，欢迎在 GitHub Issues 中交流。

---
**SFSHC from AVD战队 制作**  (版本 v1.0.0)  © 2025 SFSHC from AVD战队. All rights reserved.
