# PFPanel  [![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

[**中文**](./README.md) | **English**

## ✨ Preview ✨

<img width="1730" height="1040" alt="image" src="https://github.com/user-attachments/assets/b24640b6-1c8e-40cb-8c82-d2cc88d61733" />
<img width="1026" height="974" alt="image" src="https://github.com/user-attachments/assets/dfa99f57-fa7c-45e8-b471-ad18f2fd40fe" />


## 🎉 Welcome to PFPanel! 🎉

**PFPanel** — A Web control panel for **Polyfield** game server developed by **SFSHC**. Say goodbye to tedious command lines and embrace a clean, intuitive web interface for effortless server management!

**Core Features:**

*   🚀 **One-Click Control** - Start/stop server with a single click
*   📊 **Real-time Monitoring** - CPU, memory, network status at a glance
*   📈 **Traffic Statistics** - Real-time speed, total traffic, daily records
*   ⚙️ **Online Configuration** - Modify server settings via web interface
*   🗺️ **Map Management** - Upload, extract, delete maps easily
*   📁 **File Management** - Browse, rename, delete files conveniently
*   🌍 **Multi-language** - Support Chinese and English switching

## 🎨 UI Design

PFPanel features a modern UI design:

*   🌙 **Dark Theme** - Eye-friendly dark background for extended use
*   ✨ **Glass Morphism** - Semi-transparent cards with layered visual depth
*   🎯 **Gradient Colors** - Elegant purple-blue gradient as primary color
*   📱 **Responsive Layout** - Perfect adaptation for desktop and mobile
*   🔄 **Smooth Animations** - Seamless transition effects for fluid interaction
*   📊 **Data Visualization** - Progress bars and status cards for clear insights
*   🎛️ **Sidebar Navigation** - Clear functional sections for intuitive operation

## 🚀 Quick Start

### Requirements

*   Linux server (Ubuntu/Debian recommended)
*   Polyfield server deployed
*   Python 3.8+
*   Port 9999 open

### Installation

```bash
# Clone repository
git clone https://github.com/SFSHC/PFPanel.git
cd PFPanel

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start panel
python3 web.py
```

Access via browser: `http://YOUR_SERVER_IP:9999`

### Using Executable

1. Download from [Releases](https://github.com/SFSHC/PFPanel/releases)
2. Grant permission and run:

```bash
chmod +x pfpanel-linux-x64
./pfpanel-linux-x64
```

## ⚙️ Configuration

In v1.6.0, configuration files are located in the game directory:

```
/root/pf/
├── ServerConfig.txt    # Server configuration
├── editor/             # Map files directory
└── ...
```

## 🔄 Upgrade Guide

```bash
cd PFPanel
git pull
pip install --upgrade -r requirements.txt
# Restart panel
```

## ⚠️ Security Tips

*   🔑 Change default password on first use
*   🛡️ Use in internal network or configure firewall
*   🔒 Do not expose panel port to public network

## 📋 TODO

*   [ ] HTTPS support
*   [ ] RCON integration
*   [ ] Player management
*   [ ] More themes

## 🤝 Contributing

Welcome to submit bug reports, feature suggestions and code contributions!

*   🐛 [Submit Issue](https://github.com/SFSHC/PFPanel/issues)
*   💻 [Submit PR](https://github.com/SFSHC/PFPanel/pulls)

## 📜 License

This project is licensed under [GNU GPLv3](https://www.gnu.org/licenses/gpl-3.0).

## 📞 Contact

*   Author: SFSHC
*   GitHub: [https://github.com/SFSHC](https://github.com/SFSHC)
*   Project: [https://github.com/SFSHC/PFPanel](https://github.com/SFSHC/PFPanel)

---

🛠️ **Made by SFSHC** (v1.6.0) © 2024-2026 SFSHC. All rights reserved.
