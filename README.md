[README.md](https://github.com/user-attachments/files/29002087/README.md)
# PFPanel  [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

**中文** | [**English**](./README_EN.md)

## ✨ 效果预览 ✨

<img width="1730" height="1040" alt="image" src="https://github.com/user-attachments/assets/b24640b6-1c8e-40cb-8c82-d2cc88d61733" />
<img width="1026" height="974" alt="image" src="https://github.com/user-attachments/assets/dfa99f57-fa7c-45e8-b471-ad18f2fd40fe" />



## 🎉 欢迎使用 PFPanel！ 🎉

**PFPanel** —— 由 **SFSHC** 开发的 **Polyfield** 游戏服务器 Web 控制面板。告别繁琐的命令行，拥抱简洁、直观的 Web 界面，让服务器管理变得轻松愉悦！

**核心功能：**

*   🚀 **一键启停** - 鼠标轻点，服务器即刻响应
*   📊 **实时监控** - CPU、内存、网络状态，尽在掌握
*   📈 **流量统计** - 实时网速、累计流量、每日记录
*   ⚙️ **在线配置** - 网页端轻松修改服务器参数
*   🗺️ **地图管理** - 上传、解压、删除，操作简单
*   📁 **文件管理** - 浏览、重命名、删除，便捷高效
*   🌍 **中英文** - 支持中文/英文切换

## 🎨 界面设计

PFPanel 采用现代化 UI 设计理念：

*   🌙 **暗色主题** - 护眼深色背景，长时间使用不疲劳
*   ✨ **毛玻璃效果** - 半透明卡片，层次分明，视觉舒适
*   🎯 **渐变配色** - 紫蓝渐变主色调，优雅大气
*   📱 **响应式布局** - 完美适配桌面端和移动端
*   🔄 **流畅动画** - 平滑过渡效果，交互体验丝滑
*   📊 **数据可视化** - 进度条、状态卡片，数据一目了然
*   🎛️ **侧边导航** - 清晰的功能分区，操作直观便捷

## 🚀 快速上手

### 环境要求

*   Linux 服务器 (推荐 Ubuntu/Debian)
*   Python 3.8+
*   开放端口 9999

### 第一步：安装 Polyfield 服务端

> ⚠️ **开始之前！** 请确保按照 [Polyfield 官方安装说明](https://polyfield.net/builds/#README.txt) 的要求配置好服务器。

**前置要求：**
1. 确保 Ubuntu 服务器已禁用 IPv6，否则玩家无法通过服务器列表加入
2. 确保有 root 权限
3. 游戏应下载到 `/root` 目录下

**安装依赖：**
```bash
apt-get install screen unzip libc6-i386 lib32stdc++6
```

**下载并解压服务端：**
```bash
# 创建 pf 目录
mkdir -p /root/pf
cd /root/pf

# 下载服务端
wget https://polyfield.net/builds/Polyfield_v0.7.5_Linux.zip

# 解压到当前目录
unzip Polyfield_v0.7.5_Linux.zip
chmod +x Polyfield_v0.7.5_Linux.x86_64
```

**首次运行生成配置文件：**
```bash
./Polyfield_v0.7.5_Linux.x86_64
# 等待约1分钟后按 Ctrl + C 关闭
# 检查 ServerConfig.txt 是否生成
ls
```

**禁用 IPv6（重要）：**
```bash
sysctl -w net.ipv6.conf.all.disable_ipv6=1
sysctl -w net.ipv6.conf.default.disable_ipv6=1
sysctl -w net.ipv6.conf.lo.disable_ipv6=1

echo -e "net.ipv6.conf.all.disable_ipv6=1\nnet.ipv6.conf.default.disable_ipv6=1\nnet.ipv6.conf.lo.disable_ipv6=1" | sudo tee -a /etc/sysctl.conf
sysctl -p
```

**目录结构：**
```
/root/pf/
├── Polyfield_v0.7.5_Linux.x86_64  # 游戏程序
├── ServerConfig.txt                # 服务器配置
├── banned-users.txt                # 封禁列表
└── editor/                         # 地图文件夹
```

> 📖 完整安装说明请参考 [Polyfield 官方文档](https://polyfield.net/builds/#README.txt)

### 第二步：安装并启动面板

```bash
# 克隆面板
git clone https://github.com/SFSHC/PFPanel.git
cd PFPanel

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 启动面板
python3 web.py
```

浏览器访问: `http://服务器IP:9999`

首次访问会提示设置管理员密码。

### 使用可执行文件

1. 前往 [Releases](https://github.com/SFSHC/PFPanel/releases) 下载
2. 赋予执行权限并运行：

```bash
chmod +x pfpanel-linux-x64
./pfpanel-linux-x64
```

## ⚙️ 配置说明

v1.6.0 版本配置文件位于游戏目录：

```
/root/pf/
├── ServerConfig.txt    # 服务器配置
├── editor/             # 地图文件目录
└── ...
```

## 🔄 升级指南

```bash
cd PFPanel
git pull
pip install --upgrade -r requirements.txt
# 重启面板
```

## ⚠️ 安全提示

*   🔑 首次使用请修改默认密码
*   🛡️ 建议内网使用或配置防火墙
*   🔒 不要公网暴露面板端口

## 📋 TODO

*   [ ] HTTPS 支持
*   [ ] RCON 集成
*   [ ] 玩家管理
*   [ ] 更多主题

## 🤝 参与贡献

欢迎提交 Bug 报告、功能建议和代码贡献！

*   🐛 [提交 Issue](https://github.com/SFSHC/PFPanel/issues)
*   💻 [提交 PR](https://github.com/SFSHC/PFPanel/pulls)

## 📜 开源协议

本项目遵循 [GNU GPLv3](https://www.gnu.org/licenses/gpl-3.0) 协议。

## 📞 联系方式

*   作者: SFSHC
*   GitHub: [https://github.com/SFSHC](https://github.com/SFSHC)
*   项目主页: [https://github.com/SFSHC/PFPanel](https://github.com/SFSHC/PFPanel)

---

🛠️ **SFSHC 制作** (v1.6.0) © 2024-2026 SFSHC. All rights reserved.
