#!/usr/bin/env python3
"""
115cli - 115网盘命令行工具
支持：登录、云下载、文件管理
"""

import os
import json
import click
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
import time

console = Console()

CONFIG_DIR = Path.home() / ".115cli"
COOKIE_FILE = CONFIG_DIR / "cookie.txt"

def get_client():
    """获取已认证的115客户端"""
    from p115client import P115Client
    
    if not COOKIE_FILE.exists():
        console.print("[red]未登录！请先运行: 115cli login[/red]")
        raise SystemExit(1)
    
    cookie = COOKIE_FILE.read_text().strip()
    return P115Client(cookie)

@click.group()
def cli():
    """115网盘命令行工具"""
    CONFIG_DIR.mkdir(exist_ok=True)

@cli.command()
@click.option('--cookie', '-c', help='直接传入cookie字符串')
def login(cookie):
    """登录115网盘（使用cookie）"""
    if cookie:
        # 直接使用传入的cookie
        COOKIE_FILE.write_text(cookie)
        console.print("[green]Cookie已保存！[/green]")
    else:
        # 显示QR码登录
        from p115client import P115Client
        
        console.print("正在生成登录二维码...")
        
        try:
            # 尝试二维码登录
            client = P115Client.login_with_qrcode()
            COOKIE_FILE.write_text(client.cookie)
            console.print("[green]登录成功！Cookie已保存。[/green]")
        except Exception as e:
            console.print(f"[red]登录失败: {e}[/red]")
            console.print("\n[yellow]备选方案：从浏览器复制cookie后运行：[/yellow]")
            console.print("115cli login --cookie 'YOUR_COOKIE_STRING'")
            raise SystemExit(1)
    
    # 验证登录
    try:
        client = get_client()
        user_info = client.user_info()
        console.print(f"[green]欢迎, {user_info.get('user_name', '用户')}！[/green]")
    except Exception as e:
        console.print(f"[yellow]Cookie已保存，但验证失败: {e}[/yellow]")

@cli.command()
def whoami():
    """显示当前登录用户信息"""
    client = get_client()
    try:
        info = client.user_info()
        console.print(f"用户名: {info.get('user_name', 'N/A')}")
        console.print(f"用户ID: {info.get('user_id', 'N/A')}")
    except Exception as e:
        console.print(f"[red]获取用户信息失败: {e}[/red]")

@cli.command()
@click.argument('magnet')
@click.option('--save-path', '-s', default='/', help='保存路径（目录ID或路径）')
def download(magnet, save_path):
    """添加磁力链接到云下载"""
    client = get_client()
    
    console.print(f"[cyan]添加云下载任务...[/cyan]")
    console.print(f"链接: {magnet[:60]}...")
    
    try:
        # 添加离线下载任务
        result = client.offline_add_url(magnet, save_path)
        
        if result.get('state'):
            info_hash = result.get('info_hash', 'N/A')
            console.print(f"[green]✓ 任务添加成功！[/green]")
            console.print(f"Info Hash: {info_hash}")
            return info_hash
        else:
            error = result.get('error_msg', '未知错误')
            console.print(f"[red]✗ 添加失败: {error}[/red]")
            raise SystemExit(1)
    except Exception as e:
        console.print(f"[red]错误: {e}[/red]")
        raise SystemExit(1)

@cli.command()
@click.option('--limit', '-n', default=20, help='显示数量')
def tasks(limit):
    """查看云下载任务列表"""
    client = get_client()
    
    try:
        result = client.offline_list()
        task_list = result.get('tasks', [])
        
        if not task_list:
            console.print("[yellow]没有云下载任务[/yellow]")
            return
        
        table = Table(title="云下载任务")
        table.add_column("状态", style="cyan")
        table.add_column("名称", max_width=50)
        table.add_column("进度", style="green")
        table.add_column("大小", style="blue")
        
        for task in task_list[:limit]:
            status_map = {
                0: "⏳ 等待",
                1: "⬇️ 下载中",
                2: "✅ 完成",
                -1: "❌ 失败"
            }
            status = status_map.get(task.get('status', 0), "❓ 未知")
            name = task.get('name', 'N/A')[:50]
            percent = f"{task.get('percent_done', 0)}%"
            size = format_size(task.get('size', 0))
            
            table.add_row(status, name, percent, size)
        
        console.print(table)
    except Exception as e:
        console.print(f"[red]获取任务列表失败: {e}[/red]")

@cli.command()
@click.argument('path', default='/')
@click.option('--limit', '-n', default=30, help='显示数量')
def ls(path, limit):
    """列出目录内容"""
    client = get_client()
    
    try:
        # 如果是数字，当作目录ID
        if path.isdigit():
            cid = int(path)
        else:
            # 路径转ID
            cid = 0  # 根目录
            if path != '/':
                # 简单实现：只支持根目录或目录ID
                console.print("[yellow]提示：路径导航暂只支持目录ID，根目录请用 / 或 0[/yellow]")
        
        result = client.fs_files(cid, limit=limit)
        files = result.get('data', [])
        
        if not files:
            console.print("[yellow]目录为空[/yellow]")
            return
        
        table = Table(title=f"目录内容 (cid={cid})")
        table.add_column("类型", style="cyan", width=4)
        table.add_column("名称", max_width=50)
        table.add_column("大小", style="blue", justify="right")
        table.add_column("ID", style="dim")
        
        for f in files:
            ftype = "📁" if f.get('fid') is None else "📄"
            name = f.get('n', 'N/A')[:50]
            size = format_size(f.get('s', 0)) if f.get('fid') else '-'
            fid = str(f.get('cid') or f.get('fid', 'N/A'))
            
            table.add_row(ftype, name, size, fid)
        
        console.print(table)
    except Exception as e:
        console.print(f"[red]获取目录失败: {e}[/red]")

@cli.command()
@click.argument('file_id')
@click.argument('target_dir_id')
def mv(file_id, target_dir_id):
    """移动文件到指定目录"""
    client = get_client()
    
    try:
        result = client.fs_move([int(file_id)], int(target_dir_id))
        if result.get('state'):
            console.print(f"[green]✓ 文件已移动到目录 {target_dir_id}[/green]")
        else:
            console.print(f"[red]移动失败: {result}[/red]")
    except Exception as e:
        console.print(f"[red]错误: {e}[/red]")

@cli.command()
@click.argument('keyword')
@click.option('--limit', '-n', default=20, help='结果数量')
def search(keyword, limit):
    """搜索文件"""
    client = get_client()
    
    try:
        result = client.fs_search(keyword, limit=limit)
        files = result.get('data', [])
        
        if not files:
            console.print(f"[yellow]未找到 '{keyword}' 相关文件[/yellow]")
            return
        
        table = Table(title=f"搜索结果: {keyword}")
        table.add_column("类型", style="cyan", width=4)
        table.add_column("名称", max_width=50)
        table.add_column("大小", style="blue", justify="right")
        table.add_column("ID", style="dim")
        
        for f in files:
            ftype = "📁" if f.get('fid') is None else "📄"
            name = f.get('n', 'N/A')[:50]
            size = format_size(f.get('s', 0)) if f.get('fid') else '-'
            fid = str(f.get('cid') or f.get('fid', 'N/A'))
            
            table.add_row(ftype, name, size, fid)
        
        console.print(table)
    except Exception as e:
        console.print(f"[red]搜索失败: {e}[/red]")

@cli.command()
@click.argument('info_hash')
@click.option('--wait', '-w', is_flag=True, help='等待下载完成')
@click.option('--timeout', '-t', default=600, help='等待超时（秒）')
def status(info_hash, wait, timeout):
    """查询云下载任务状态"""
    client = get_client()
    
    def check_status():
        result = client.offline_list()
        for task in result.get('tasks', []):
            if task.get('info_hash', '').lower() == info_hash.lower():
                return task
        return None
    
    if wait:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("等待下载完成...", total=None)
            start = time.time()
            
            while time.time() - start < timeout:
                info = check_status()
                if info is None:
                    console.print("[yellow]任务不存在[/yellow]")
                    return
                
                status_val = info.get('status', 0)
                percent = info.get('percent_done', 0)
                
                progress.update(task, description=f"下载中... {percent}%")
                
                if status_val == 2:  # 完成
                    console.print(f"[green]✓ 下载完成: {info.get('name')}[/green]")
                    console.print(f"文件ID: {info.get('file_id', 'N/A')}")
                    return info
                elif status_val == -1:  # 失败
                    console.print(f"[red]✗ 下载失败: {info.get('name')}[/red]")
                    return info
                
                time.sleep(5)
            
            console.print("[yellow]等待超时[/yellow]")
    else:
        info = check_status()
        if info:
            console.print(json.dumps(info, indent=2, ensure_ascii=False))
        else:
            console.print("[yellow]任务不存在[/yellow]")

def format_size(size_bytes):
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f}{unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f}PB"

if __name__ == '__main__':
    cli()
