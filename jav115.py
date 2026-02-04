#!/usr/bin/env python3
"""
jav115 - 一键搜索javdb并添加到115云下载
"""

import click
import re
import json
import subprocess
from urllib.parse import quote
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.table import Table
import time

console = Console()

SCRIPT_DIR = Path(__file__).parent
CLI_115 = SCRIPT_DIR / "115cli"
JAVDB_PY = SCRIPT_DIR / "javdb.py"
VENV_PYTHON = SCRIPT_DIR / "venv" / "bin" / "python"

def run_115cli(*args):
    """运行115cli命令"""
    result = subprocess.run(
        [str(CLI_115)] + list(args),
        capture_output=True,
        text=True
    )
    return result.stdout, result.returncode

def run_javdb(*args):
    """运行javdb命令"""
    result = subprocess.run(
        [str(VENV_PYTHON), str(JAVDB_PY)] + list(args),
        capture_output=True,
        text=True
    )
    return result.stdout, result.returncode

def search_and_get_magnet(keyword: str) -> str | None:
    """搜索并获取magnet链接"""
    # 搜索
    console.print(f"[cyan]🔍 搜索: {keyword}[/cyan]")
    output, code = run_javdb("search", keyword, "-j")
    
    if code != 0 or not output.strip():
        console.print("[red]搜索失败[/red]")
        return None
    
    try:
        results = json.loads(output)
    except:
        console.print("[red]解析搜索结果失败[/red]")
        return None
    
    if not results:
        console.print("[yellow]未找到结果[/yellow]")
        return None
    
    # 显示搜索结果
    table = Table(title="搜索结果")
    table.add_column("#", style="dim", width=3)
    table.add_column("番号", style="cyan")
    table.add_column("标题", max_width=45)
    table.add_column("日期", style="blue")
    
    for i, item in enumerate(results, 1):
        table.add_row(
            str(i),
            item['code'],
            item['title'][:45] if item['title'] else '',
            item['date']
        )
    
    console.print(table)
    
    # 选择
    if len(results) == 1:
        choice = 1
    else:
        choice = IntPrompt.ask("选择", default=1)
    
    if choice < 1 or choice > len(results):
        console.print("[red]无效选择[/red]")
        return None
    
    selected = results[choice - 1]
    console.print(f"[green]选择: {selected['code']}[/green]")
    
    # 获取magnet
    console.print("[cyan]🔗 获取磁力链接...[/cyan]")
    output, code = run_javdb("magnet", selected['code'], "-1")
    
    if code != 0 or not output.strip():
        console.print("[red]获取磁力链接失败[/red]")
        return None
    
    magnet = output.strip()
    console.print(f"[dim]{magnet[:60]}...[/dim]")
    return magnet

@click.group()
def cli():
    """JavDB + 115网盘 一键下载工具"""
    pass

@cli.command()
@click.argument('keyword')
@click.option('--save-path', '-s', default='/', help='115保存路径（目录ID）')
@click.option('--move-to', '-m', help='下载完成后移动到的目录ID')
@click.option('--wait', '-w', is_flag=True, help='等待下载完成')
def download(keyword, save_path, move_to, wait):
    """搜索并下载到115"""
    
    # 1. 搜索并获取magnet
    magnet = search_and_get_magnet(keyword)
    if not magnet:
        return
    
    # 2. 添加到115云下载
    console.print("[cyan]☁️ 添加到115云下载...[/cyan]")
    output, code = run_115cli("download", magnet, "-s", save_path)
    console.print(output)
    
    if code != 0:
        console.print("[red]添加云下载失败[/red]")
        return
    
    # 提取info_hash
    hash_match = re.search(r'btih:([a-fA-F0-9]+)', magnet)
    if not hash_match:
        console.print("[yellow]无法提取hash[/yellow]")
        return
    
    info_hash = hash_match.group(1)
    
    # 3. 等待下载完成（可选）
    if wait:
        console.print("[cyan]⏳ 等待下载完成...[/cyan]")
        output, code = run_115cli("status", info_hash, "--wait")
        console.print(output)
        
        # 4. 移动文件（可选）
        if move_to and code == 0:
            console.print(f"[cyan]📂 移动文件到目录 {move_to}...[/cyan]")
            # 需要从status输出中提取file_id
            # 这部分需要115cli支持返回文件ID
            console.print("[yellow]文件移动功能待完善[/yellow]")
    
    console.print("[green]✓ 完成！[/green]")

@cli.command()
@click.argument('keyword')
def search(keyword):
    """仅搜索，不下载"""
    run_javdb("search", keyword)

@cli.command()
@click.argument('code')
def magnet(code):
    """获取指定番号的磁力链接"""
    output, _ = run_javdb("magnet", code)
    console.print(output)

@cli.command()
def tasks():
    """查看115云下载任务"""
    output, _ = run_115cli("tasks")
    console.print(output)

@cli.command()
@click.argument('path', default='/')
def ls(path):
    """列出115目录"""
    output, _ = run_115cli("ls", path)
    console.print(output)

if __name__ == '__main__':
    cli()
