# 115cli OpenClaw Skill

[中文](#中文) | [English](#english)

---

## 中文

### 简介

JavDB 搜索 + 115网盘云下载 CLI 工具。一键搜索日本影片并自动添加到115网盘离线下载。

### 功能

- 🔍 **JavDB搜索** - 按番号/关键词搜索，获取磁力链接
- ☁️ **115云下载** - 添加磁力链接到115网盘离线下载
- 📂 **文件管理** - 浏览目录、搜索文件、移动文件
- 🚀 **一键下载** - 搜索→选择→下载一条龙

### 安装

```bash
# 克隆仓库
git clone https://github.com/championeer/115cli-openclaw-skill.git
cd 115cli-openclaw-skill

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 使用

#### 1. 登录115网盘

从浏览器获取Cookie（参见 [Cookie获取指南](references/cookie-guide.md)），然后：

```bash
scripts/115cli login --cookie 'CID=xxx; UID=xxx; SEID=xxx; ...'
```

#### 2. 一键下载（推荐）

```bash
scripts/jav115 download "START-451"    # 搜索并下载
scripts/jav115 download "SSIS-917" -w  # 等待下载完成
```

#### 3. 分步操作

```bash
scripts/jav115 search "关键词"    # 搜索
scripts/jav115 magnet "番号"      # 获取磁力链接
scripts/jav115 tasks              # 查看云下载任务
scripts/jav115 ls /               # 浏览115目录
```

### 作为 OpenClaw Skill 使用

本项目遵循 [OpenClaw](https://github.com/openclaw/openclaw) Skill 规范，可直接作为 OpenClaw Agent 的技能使用。

### 依赖

- [p115client](https://github.com/ChenyangGao/p115client) - 115网盘Python客户端
- [click](https://click.palletsprojects.com/) - CLI框架
- [rich](https://rich.readthedocs.io/) - 终端美化

### 注意事项

- ⚠️ 115 Cookie 会过期，需定期更新
- ⚠️ JavDB 首次访问会自动确认年龄验证
- ⚠️ 云下载速度取决于资源热度

### 许可证

MIT License

### 免责声明

本工具仅供学习交流使用，请遵守当地法律法规。

---

## English

### Introduction

JavDB Search + 115 Cloud Download CLI Tool. One-click search for Japanese videos and automatically add to 115 cloud offline download.

### Features

- 🔍 **JavDB Search** - Search by code/keyword, get magnet links
- ☁️ **115 Cloud Download** - Add magnet links to 115 cloud offline download
- 📂 **File Management** - Browse directories, search files, move files
- 🚀 **One-click Download** - Search → Select → Download in one go

### Installation

```bash
# Clone repository
git clone https://github.com/championeer/115cli-openclaw-skill.git
cd 115cli-openclaw-skill

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Usage

#### 1. Login to 115

Get Cookie from browser (see [Cookie Guide](references/cookie-guide.md)), then:

```bash
scripts/115cli login --cookie 'CID=xxx; UID=xxx; SEID=xxx; ...'
```

#### 2. One-click Download (Recommended)

```bash
scripts/jav115 download "START-451"    # Search and download
scripts/jav115 download "SSIS-917" -w  # Wait for completion
```

#### 3. Step by Step

```bash
scripts/jav115 search "keyword"   # Search
scripts/jav115 magnet "code"      # Get magnet link
scripts/jav115 tasks              # View download tasks
scripts/jav115 ls /               # Browse 115 directory
```

### Use as OpenClaw Skill

This project follows the [OpenClaw](https://github.com/openclaw/openclaw) Skill specification and can be used directly as a skill for OpenClaw Agent.

### Dependencies

- [p115client](https://github.com/ChenyangGao/p115client) - 115 Cloud Python Client
- [click](https://click.palletsprojects.com/) - CLI Framework
- [rich](https://rich.readthedocs.io/) - Terminal Beautification

### Notes

- ⚠️ 115 Cookie expires periodically, needs regular update
- ⚠️ JavDB auto-confirms age verification on first visit
- ⚠️ Cloud download speed depends on resource popularity

### License

MIT License

### Disclaimer

This tool is for educational purposes only. Please comply with local laws and regulations.
