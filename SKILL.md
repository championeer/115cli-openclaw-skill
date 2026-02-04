# 115cli Skill - JavDB搜索 + 115网盘云下载

从javdb.com搜索影片并自动添加到115网盘云下载。

## 安装

首次使用需要初始化虚拟环境：

```bash
cd /Users/dev/.openclaw/workspace/115cli
python3 -m venv venv
source venv/bin/activate
pip install p115client click rich
```

## 登录115网盘

使用cookie登录（从浏览器复制）：

```bash
./115cli login --cookie 'CID=xxx; UID=xxx; ...'
```

## 使用

### 一键下载（推荐）

```bash
# 搜索并添加到云下载
./jav115 download "番号或关键词"

# 指定保存目录
./jav115 download "SSIS-917" -s 目录ID

# 等待下载完成
./jav115 download "SSIS-917" -w
```

### 分步操作

```bash
# 仅搜索
./jav115 search "关键词"

# 获取磁力链接
./jav115 magnet "SSIS-917"

# 查看云下载任务
./jav115 tasks

# 浏览115目录
./jav115 ls /
./jav115 ls 目录ID
```

### 115cli单独使用

```bash
# 登录
./115cli login --cookie 'cookie字符串'

# 添加磁力云下载
./115cli download "magnet:?xt=urn:btih:..."

# 查看任务
./115cli tasks

# 列出目录
./115cli ls /

# 搜索文件
./115cli search "关键词"

# 移动文件
./115cli mv 文件ID 目标目录ID
```

## 工作流程

1. 用户提供番号/关键词
2. 搜索javdb.com获取影片列表
3. 用户选择目标影片
4. 获取磁力链接
5. 添加到115云下载
6. （可选）等待下载完成后移动到指定目录

## 文件结构

```
115cli/
├── 115cli          # 115网盘CLI wrapper
├── cli.py          # 115网盘CLI主程序
├── javdb.py        # JavDB搜索工具
├── jav115          # 一键下载wrapper
├── jav115.py       # 一键下载主程序
├── venv/           # Python虚拟环境
└── SKILL.md        # 本文件
```

## 注意事项

- 115 cookie会过期，需要定期更新
- javdb搜索首次访问会自动确认年龄验证
- 云下载速度取决于115网盘资源热度
