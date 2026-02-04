# 115cli

JavDB 搜索 + 115网盘云下载 CLI 工具

一键搜索日本影片并自动添加到115网盘离线下载。

## Features

- 🔍 **JavDB搜索** - 按番号/关键词搜索，获取磁力链接
- ☁️ **115云下载** - 添加磁力链接到115网盘离线下载
- 📂 **文件管理** - 浏览目录、搜索文件、移动文件
- 🚀 **一键下载** - 搜索→选择→下载一条龙

## Installation

```bash
# Clone
git clone https://github.com/YOUR_USERNAME/115cli.git
cd 115cli

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install p115client click rich
```

## Usage

### 1. Login to 115

从浏览器获取115网盘的Cookie，然后：

```bash
./115cli login --cookie 'CID=xxx; UID=xxx; SEID=xxx; ...'
```

### 2. One-click Download (推荐)

```bash
# 搜索并下载
./jav115 download "START-451"

# 指定保存目录（使用目录ID）
./jav115 download "SSIS-917" -s 1234567890

# 等待下载完成
./jav115 download "ABW-267" -w
```

### 3. Step by Step

```bash
# 搜索
./jav115 search "关键词"

# 获取磁力链接
./jav115 magnet "SSIS-917"

# 查看云下载任务
./jav115 tasks

# 浏览115目录
./jav115 ls /
```

### 4. 115cli Commands

```bash
./115cli login --cookie 'COOKIE'  # 登录
./115cli whoami                    # 查看当前用户
./115cli tasks                     # 云下载任务列表
./115cli download "magnet:?..."    # 添加磁力下载
./115cli ls /                      # 列出根目录
./115cli ls 目录ID                 # 列出指定目录
./115cli search "关键词"           # 搜索文件
./115cli mv 文件ID 目录ID          # 移动文件
./115cli status HASH --wait        # 等待下载完成
```

## How to Get 115 Cookie

1. 在浏览器中登录 [115.com](https://115.com)
2. 打开开发者工具 (F12)
3. 切换到 Network 标签
4. 刷新页面
5. 点击任意请求，找到 Request Headers 中的 `Cookie`
6. 复制完整的 Cookie 字符串

关键字段：`CID`, `UID`, `SEID`, `KID` 等

## File Structure

```
115cli/
├── 115cli          # 115网盘CLI入口
├── cli.py          # 115网盘CLI主程序
├── javdb.py        # JavDB搜索工具
├── jav115          # 一键下载入口
├── jav115.py       # 一键下载主程序
├── SKILL.md        # OpenClaw skill文档
└── README.md       # 本文件
```

## Dependencies

- [p115client](https://github.com/ChenyangGao/p115client) - 115网盘Python客户端
- [click](https://click.palletsprojects.com/) - CLI框架
- [rich](https://rich.readthedocs.io/) - 终端美化

## Notes

- ⚠️ 115 Cookie 会过期，需要定期更新
- ⚠️ JavDB 首次访问会自动确认年龄验证
- ⚠️ 云下载速度取决于资源热度

## License

MIT License

## Disclaimer

本工具仅供学习交流使用，请遵守当地法律法规。
