---
name: 115cli
description: JavDB搜索 + 115网盘云下载CLI。用于搜索日本影片番号获取磁力链接，并自动添加到115网盘离线下载。当用户提到下载番号、115网盘、javdb搜索、磁力下载时使用此skill。
---

# 115cli

从javdb.com搜索影片并自动添加到115网盘云下载。

## 安装

首次使用需初始化虚拟环境：

```bash
cd <skill_dir>
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 登录115网盘

从浏览器复制cookie后运行：

```bash
scripts/115cli login --cookie 'CID=xxx; UID=xxx; SEID=xxx; ...'
```

Cookie存储在 `~/.115cli/cookie.txt`。

## 命令

### 一键下载（推荐）

```bash
scripts/jav115 download "番号"      # 搜索并下载
scripts/jav115 download "番号" -w   # 等待下载完成
```

### 分步操作

```bash
scripts/jav115 search "关键词"      # 搜索
scripts/jav115 magnet "番号"        # 获取磁力链接
scripts/jav115 tasks                # 查看云下载任务
scripts/jav115 ls /                 # 浏览115目录
```

### 115cli直接使用

```bash
scripts/115cli download "magnet:?..." # 添加磁力下载
scripts/115cli tasks                  # 任务列表
scripts/115cli ls 目录ID              # 列出目录
scripts/115cli mv 文件ID 目录ID       # 移动文件
scripts/115cli search "关键词"        # 搜索文件
```

## 注意事项

- 115 cookie会过期，需定期更新
- javdb首次访问自动确认年龄验证
- 云下载速度取决于资源热度
