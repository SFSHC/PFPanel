# PFPanel  [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

<!-- 项目 Logo (可选) -->
<!-- ![Project Logo](path/to/logo.png) -->

### ✨ 效果预览 ✨ （板块可单击展开）

![Polyfield Server Panel 预览](https://github.com/user-attachments/assets/244dc01d-d030-46bc-9737-d95e2b2bfa90)

## 🎉 欢迎使用 PFPanel！ 🎉

您好！感谢您使用 **PFPanel** —— 由 **SFSHC** 简单搓的 **Polyfield** 游戏服务器 Web 控制面板。告别繁琐的命令行，拥抱简洁、直观的 Web 界面，让服务器管理变得轻松愉悦！

**PFPanel 能为您做什么？**

*   🚀 **一键启停：** 告别繁琐指令，鼠标轻点，服务器即刻响应。
*   📊 **实时监控：** CPU、内存、网络状态，尽在掌握，了如指掌。
*   📈 **流量洞察：** 实时网速、累计流量，一目了然，心中有数。
*   🗓️ **每日流量：** 精细记录，助您优化资源，精打细算。
*   ⚙️ **在线配置：** 无需 SSH，网页端轻松修改服务器参数。
*   🗺️ **地图管理：** 上传、解压、删除，地图管理从未如此简单。
*   📁 **文件管理：** 浏览、重命名、删除，文件操作便捷高效。

**PFPanel - 开源、共享、共进步！** 遵循 **GNU GPLv3 许可证**，期待您的参与和贡献！

## ✨ 功能亮点 ✨

*   🌈 **美观易用：** 基于 Bootstrap 4，界面清爽，响应式设计，完美适配各种设备。
*   🏠 **实时数据：** 服务器状态、网络流量，实时更新，一览无余。
*   📝 **配置无忧：** Web 界面修改配置，告别繁琐的手动编辑。
*   🗺️ **地图掌控：** 轻松上传、解压、删除地图，打造您的专属世界。
*   🗂️ **文件便捷：** 常用文件操作，触手可及，高效管理。
*   🔒 **安全登录：** 密码保护，保障您的控制面板安全无虞。
*   🗂️ **日志详尽：** 记录所有操作，问题追溯有迹可循。
*   📊 **流量统计：** 每日流量数据，助您精细化管理服务器。

## 🚀 快速上手 🚀

PFPanel 提供两种启动方式，任您选择：

### 🛠️ 方式一：源码启动 (推荐开发者)

如果您是开发者，或者希望深入了解和定制 PFPanel，推荐使用源码启动。

#### 🚧 准备工作

*   ✅ **Linux 服务器 (VPS):** 推荐 Ubuntu 或 Debian。
*   ✅ **Polyfield 服务端:** 确保已安装。
*   ✅ **Python 3.6+:** 推荐 Python 3.8+。
*   ✅ **pip:** Python 包管理器。
*   ✅ **网络畅通:** 下载依赖包。
*   ✅ **防火墙端口:** 开放程序所需端口。
*   ✅ **Polyfield 服务端部署:** [中文安装文档](https://github.com/SFSHC/PFPanel/blob/main/%E6%9C%8D%E5%8A%A1%E7%AB%AF%E5%AE%89%E8%A3%85%E6%96%87%E6%A1%A3%E4%B8%AD%E6%96%87)

#### 🕹️ 安装步骤

1.  **SSH 登录服务器。**
2.  **下载源码:**

    ```bash
    git clone https://github.com/SFSHC/PFPanel.git
    cd PFPanel
    ```

3.  **创建并激活虚拟环境 (强烈推荐):**

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # Linux/macOS
    # 或
    venv\Scripts\activate  # Windows (CMD)
    # 或
    venv\Scripts\Activate.ps1 # Windows (PowerShell)
    ```

4.  **安装依赖:**

    ```bash
    pip install -r requirements.txt
    ```

5.  **配置 `server_config.ini` (务必修改密码!):**

    ```bash
    cp server_config.ini.template server_config.ini
    nano server_config.ini # 或 vim server_config.ini
    ```

6.  **启动 PFPanel:**

    ```bash
    python3 pfpanel.py
    ```

7.  **浏览器访问:** `http://您的服务器IP地址:9999`

### 🚀 方式二：可执行文件启动 (快速体验)

如果您希望快速体验 PFPanel，或不熟悉 Python 环境，推荐使用预编译的可执行文件。

#### 📥 下载 & 启动

1.  前往 [Releases](https://github.com/SFSHC/PFPanel/releases) 下载 `pfpanel-linux-x64`。
2.  上传至服务器，并赋予执行权限：

    ```bash
    chmod +x pfpanel-linux-x64
    ```
3. **直接运行 或 使用 `screen` 后台运行:**
   *   **直接运行:**  
      ```bash
         ./pfpanel-linux-x64
      ```
   *   **后台运行:**  

        ```bash
        screen -S pfpanel  # 创建 screen 会话
        ./pfpanel-linux-x64 # 运行 PFPanel
        # 按 Ctrl + A, 然后按 D, 分离会话
        ```

4.  **浏览器访问:** `http://您的服务器IP地址:9999`

**注意:**  可执行文件启动时，`server_config.ini` 需与可执行文件同目录。首次运行请手动创建 (复制 `server_config.ini.template` 并修改)。

### ⚙️ Polyfield 服务端配置 [中文文档](https://github.com/SFSHC/PFPanel/blob/main/%E6%9C%8D%E5%8A%A1%E7%AB%AF%E5%AE%89%E8%A3%85%E6%96%87%E6%A1%A3%E4%B8%AD%E6%96%87)

PFPanel 仅为控制面板，不包含 Polyfield 服务端程序。请参考 [Polyfield 官方文档](https://www.polyfield.net/builds/%23README.txt) 配置服务端。

**简要步骤：** 下载、解压、授权、运行 (Screen)。

## 🔄 升级指南

*   **源码:** `cd PFPanel && git pull && pip install --upgrade -r requirements.txt && restart`
*   **可执行文件:** 下载新版本，替换旧文件，重启。

## ⚠️ 安全警示

*   🔑 **强密码！** 首次使用务必修改 `server_config.ini` 中的默认密码。
*   🛡️ **避免公网暴露！** 建议内网使用，或配置防火墙、VPN、HTTPS。
*   🔒 **保护 `server_config.ini`!** 包含敏感信息，请妥善保管。
*   📅 **及时更新！** 关注项目更新，获取最新功能和安全修复。

## 🐞 待办事项 & 欢迎贡献

*   [ ] 🔒 安全性增强 (HTTPS, 更强认证)
*   [ ] ⚠️ 错误处理优化
*   [ ] 🛠️ 功能扩展 (RCON, 玩家管理等)
*   [ ] 📝 编码兼容性改进
*   [ ] 📝 文档完善

当前版本：**v1.5.0**

**您的反馈和贡献，是 PFPanel 不断进步的动力！**

## 🤝 如何贡献

*   🐛 提交 Bug 报告 (GitHub Issues)
*   💡 提出功能建议 (GitHub Issues)
*   💻 贡献代码 (Pull Request)
*   📝 改进文档 (Pull Request)
*   🌍 翻译支持

## 📜 开源协议

本项目遵循 **GNU General Public License v3.0 (GPLv3)**。

[**GPLv3 许可证全文 (English)**](https://www.gnu.org/licenses/gpl-3.0)

完整许可证文本位于项目根目录 `LICENSE` 文件。

## 📞 联系方式

*   作者: SFSHC
*   项目主页: [https://github.com/SFSHC/PFPanel](https://github.com/SFSHC/PFPanel)
*   GitHub: [https://github.com/SFSHC](https://github.com/SFSHC)
*   Polyfield 官网: [https://www.polyfield.net/](https://www.polyfield.net/)
*   Bilibili: [Bilibili](https://space.bilibili.com/1635006043)
*   邮箱: sfshc@haudio.us.kg

**感谢您的使用和支持！**
##此readme总体由gemini AI完成，SFSHC简单修改

---

🛠️ **SFSHC 制作** 🛠️ (v1.5.0) © 2024-2025 SFSHC AVD. 保留所有权利.
