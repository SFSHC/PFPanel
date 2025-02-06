# PFPanel  [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

### 效果预览

![image](https://github.com/user-attachments/assets/244dc01d-d030-46bc-9737-d95e2b2bfa90)

## 🎉 欢迎来到 PFPanel！ 🎉

您好！ 感谢您选择 **PFPanel**！

这是由 **SFSHC from AVD战队** 倾力打造的开源 Web 控制面板，旨在化繁为简，让您轻松掌控 **Polyfield** 游戏服务器。告别繁琐的命令行操作，享受前所未有的服务器管理体验！

**PFPanel，您的服务器管理利器：**

*   🚀 **一键启停:**  服务器控制，尽在指尖。
*   📊 **状态监控:**  CPU、内存，实时掌握服务器脉搏。
*   📈 **流量监控:**  网络上传下载，清晰呈现。
*   🗓️ **每日流量:**  精细记录，优化资源配置。
*   ⚙️ **在线配置:**  告别 SSH，网页轻松编辑。
*   🗺️ **地图管理:**  上传、解压、删除，地图尽在掌控。
*   📁 **文件管理:**  文件浏览、重命名、删除，便捷高效。

**开源，共享，共进步！**  本项目遵循 **GNU GPLv3 许可证**，我们真诚希望它能为 Polyfield 社区贡献一份力量。 如果您喜欢，请点亮 Star，欢迎加入贡献！

## ✨ 功能亮点 ✨

*   🌈 **界面友好:**  Bootstrap 4 倾力呈现，美观、简洁、响应式。
*   🏠 **实时监控:**  服务器状态、网络数据，实时更新。
*   📝 **在线配置:**  告别繁琐，配置修改一触即达。
*   🗺️ **地图管理:**  上传、解压、删除，轻松管理游戏世界。
*   🗂️ **文件管理:**  常用文件操作，便捷高效。
*   🔒 **安全登录:**  密码认证，保障面板安全。
*   🗂️ **详细日志:**  操作记录，问题追溯有据可依。
*   📊 **流量统计:**  每日数据，优化运营决策。

## 🚀 快速上手 - 多种启动方式 🚀

PFPanel 为您提供多种启动方式，选择适合您的即可：

### 🛠️ 方式一： 源码启动 (推荐开发者) 🛠️

如果您是开发者，或希望深入了解和定制 Panel，推荐使用源码启动：

#### 🚧 准备工作

*   ✅ **Linux 服务器 (VPS):**  推荐 Ubuntu 或 Debian。
*   ✅ **Polyfield 服务端:**  确保已安装。
*   ✅ **Python 3.6+:**  推荐 Python 3.8+。
*   ✅ **pip:**  Python 包管理器。
*   ✅ **网络畅通:**  用于下载依赖。
*   ✅ **防火墙端口:**  确保已开放程序端口。
*   ✅ **Polyfield 服务端部署:**  [Polyfield 服务端文档 (微软翻译)](https://www.microsofttranslator.com/bv.aspx?to=zh-CN&ref= SERP&url=https://polyfield.net/builds/%2523README.txt)

#### 🕹️ 详细步骤

1.  **登录服务器:**  SSH 连接您的 Linux 服务器。
2.  **下载源码:**

    ```bash
    git clone https://github.com/SFSHC/PFPanel.git
    cd PFPanel
    ```

3.  **创建虚拟环境 (推荐):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # 或 venv\Scripts\activate (Windows)
    ```

4.  **安装依赖:**

    ```bash
    pip install -r requirements.txt
    ```

5.  **配置 `server_config.ini`:**  **务必修改密码！**

    ```bash
    cp server_config.ini.template server_config.ini
    nano server_config.ini  # 或 vim server_config.ini
    ```

6.  **启动 Panel:**

    ```bash
    python3 pfpanel.py  # 或 python web.py
    ```

7.  **访问 Panel:**  浏览器打开 `http://您的服务器IP地址:9999`。

### 🚀 方式二： 可执行文件启动 (快速体验) 🚀

如果您希望快速体验 Panel 功能，或不熟悉 Python 环境，推荐使用预编译的可执行文件：

#### 📥 下载 Release

前往 [Releases](https://github.com/SFSHC/PFPanel/releases) 页面，下载最新版本的 `pfpanel-linux-x64` 文件。

#### 🏃‍♂️ 启动 Panel

1.  **上传文件:**  将 `pfpanel-linux-x64` 文件上传到您的 Linux 服务器 (任意目录)。
2.  **给予权限:**

    ```bash
    chmod +x pfpanel-linux-x64
    ```

3.  **运行 Panel:**

    ```bash
    ./pfpanel-linux-x64
    ```

4.  **后台运行 (推荐):**  使用 `screen` 命令，保持 PFPanel 在后台稳定运行：

    ```bash
    screen -S pfpanel  # 创建名为 "pfpanel" 的 screen 会话
    ./pfpanel-linux-x64 # 在 screen 会话中运行 PFPanel
    ```
    按下 `Ctrl + A`，再按下 `D` 键，即可分离 screen 会话，PFPanel 将在后台持续运行。

5.  **访问 Panel:**  浏览器打开 `http://您的服务器IP地址:9999`。

**注意:**  可执行文件启动方式，配置文件 `server_config.ini` 和 HTML 模板文件将与可执行文件位于同一目录。首次运行，请手动创建 `server_config.ini` 文件 (复制 `server_config.ini.template` 并修改)。

### ⚙️  服务端配置 (Polyfield Server)  [中文文档 (微软翻译)](https://www.microsofttranslator.com/bv.aspx?to=zh-CN&ref= SERP&url=https://polyfield.net/builds/%2523README.txt)

PFPanel 仅为控制面板，不包含 Polyfield 服务端程序。  请务必参考 [Polyfield 官方文档](https://www.polyfield.net/builds/%23README.txt)  配置 Polyfield 服务端。

**简要步骤:**

1.  下载 Polyfield 服务端程序。
2.  解压服务端程序。
3.  授权执行权限。
4.  创建 Screen 会话并运行服务端。

### 💡  后台运行 (Screen)**

推荐使用 `screen` 保持 Panel 后台运行，即使 SSH 断开连接，Panel 也能持续提供服务。  使用方法请参考 **快速上手指南** 中的说明。

## 🔄  升级 - 保持 Panel 常新 🔄

*   **源码升级:**  `cd PFPanel && git pull && pip install --upgrade -r requirements.txt && 重启 Panel`
*   **可执行文件升级:**  重新下载最新 Release 版本可执行文件，替换旧文件并重启 Panel。

## ⚠️  安全警示 - 安全第一 ⚠️

*   🔑 **密码安全:**  **牢记修改默认密码！**  强密码是安全之基。
*   🛡️ **公网风险:**  **请勿直接暴露公网！**  建议内网使用，或配置额外安全措施 (防火墙、VPN、HTTPS)。
*   🔒 **配置安全:**  `server_config.ini` 包含敏感信息，请妥善保管。
*   📅 **及时更新:**  请关注项目更新，及时升级，安全无忧。

## 🐞  问题反馈 & 功能建议 🐞

*   🔒 **安全性待增强**
*   ⚠️ **错误处理待完善**
*   🛠️ **功能持续丰富**
*   📝 **编码兼容性待优化**
*   📝 **文档持续完善**

当前版本: **v1.5.0**

**您的反馈是项目进步的源泉！**  欢迎通过 GitHub Issues 提交 Bug 报告、功能建议，或参与代码贡献，共同打造更强大的 PFPanel！

## 🤝  开源协作 - 期待您的加入 🤝

*   🐛 **Bug Report**
*   💡 **Feature Request**
*   💻 **Code Contribution**
*   📝 **Documentation Improvement**
*   🌍 **Translation Support**

## 📜  开源协议 - GPLv3 📜

本项目基于 **GNU General Public License v3.0** 开源。  **Copyleft 许可证，自由与责任并存。**  衍生作品须遵循相同协议开源。

[**GPLv3 许可证全文 (English)**](https://www.gnu.org/licenses/gpl-3.0)

项目根目录下 `LICENSE` 文件包含完整许可证文本。

## 📞  联系我们 - 期待您的声音 📞

*   作者: SFSHC from AVD战队
*   项目主页: [https://github.com/SFSHC/PFPanel](https://github.com/SFSHC/PFPanel)
*   GitHub: [https://github.com/SFSHC](https://github.com/SFSHC)
*   Polyfield 官网: [https://www.polyfield.net/](https://www.polyfield.net/)
*   Bilibili: [Bilibili](https://space.bilibili.com/1635006043)
*   邮箱 : sfshc@haudio.us.kg

**感谢您的使用和支持！**  PFPanel 与您一同成长！

---

🛠️ **SFSHC from AVD战队 开发** 🛠️  (版本 v1.5.0)  © 2024-2025 SFSHC from AVD战队.  保留所有权利。
