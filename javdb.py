#!/usr/bin/env python3
"""
javdb-search - 从javdb.com搜索影片并获取magnet链接
"""

import click
import re
import json
import subprocess
from urllib.parse import quote
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()

COOKIE_FILE = Path.home() / ".115cli" / "javdb_cookie.txt"

def get_html(url: str) -> str:
    """获取页面HTML，自动处理年龄验证"""
    
    # 检查是否有cookie文件
    cookie_args = []
    if COOKIE_FILE.exists():
        cookie_args = ['-b', str(COOKIE_FILE)]
    
    # 先尝试直接访问
    result = subprocess.run(
        ['curl', '-s', '-L', '-A', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
         '-c', str(COOKIE_FILE)] + cookie_args + [url],
        capture_output=True,
        text=True,
        timeout=30
    )
    
    html = result.stdout
    
    # 如果遇到年龄验证页面，先确认年龄
    if 'over18-modal' in html or '您必須已達您當地的法定年齡' in html:
        # 提取确认链接
        confirm_match = re.search(r'href="(/over18\?respond=1[^"]*)"', html)
        if confirm_match:
            confirm_url = f"https://javdb.com{confirm_match.group(1)}"
            # 确认年龄
            subprocess.run(
                ['curl', '-s', '-L', '-A', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                 '-c', str(COOKIE_FILE), '-b', str(COOKIE_FILE), confirm_url],
                capture_output=True,
                text=True,
                timeout=30
            )
            # 重新访问
            result = subprocess.run(
                ['curl', '-s', '-L', '-A', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                 '-b', str(COOKIE_FILE), url],
                capture_output=True,
                text=True,
                timeout=30
            )
            html = result.stdout
    
    return html

def search_javdb(keyword: str, limit: int = 10) -> list:
    """
    搜索javdb并返回结果列表
    返回: [{'code': 'ABC-123', 'title': '...', 'url': '...', 'date': '...'}, ...]
    """
    search_url = f"https://javdb.com/search?q={quote(keyword)}&f=all"
    html = get_html(search_url)
    
    items = []
    
    # 新的解析模式 - 匹配 item div 块
    # <a href="/v/4DxWwZ" class="box" title="...">
    #   <div class="video-title"><strong>HEYZO-3797</strong> 标题</div>
    #   <div class="meta">2026-01-29</div>
    
    item_pattern = r'<a href="(/v/[^"]+)" class="box"[^>]*>.*?<div class="video-title"[^>]*>\s*<strong>([^<]+)</strong>\s*([^<]*)</div>.*?<div class="meta">\s*(\d{4}-\d{2}-\d{2})\s*</div>'
    
    matches = re.findall(item_pattern, html, re.DOTALL)
    
    for match in matches[:limit]:
        url_path, code, title, date = match
        items.append({
            'code': code.strip(),
            'title': title.strip(),
            'url': f"https://javdb.com{url_path}",
            'date': date.strip()
        })
    
    return items

def get_magnets(detail_url: str) -> list:
    """
    从详情页获取magnet链接
    返回: [{'name': '...', 'size': '...', 'magnet': 'magnet:?...'}, ...]
    """
    html = get_html(detail_url)
    magnets = []
    
    # 匹配磁链 - 在 data-clipboard-text 属性中
    # 以及对应的大小标签
    
    # 方法1: 找所有包含magnet的行
    row_pattern = r'<tr[^>]*>.*?data-clipboard-text="(magnet:\?xt=urn:btih:[^"]+)".*?<span[^>]*class="tag[^"]*"[^>]*>([^<]+)</span>.*?</tr>'
    rows = re.findall(row_pattern, html, re.DOTALL)
    
    if rows:
        for magnet, size in rows:
            magnets.append({
                'magnet': magnet.strip(),
                'size': size.strip(),
            })
    else:
        # 方法2: 直接提取所有magnet链接
        simple_pattern = r'data-clipboard-text="(magnet:\?xt=urn:btih:[^"]+)"'
        simple_magnets = re.findall(simple_pattern, html)
        
        # 尝试匹配大小
        size_pattern = r'<span class="tag[^"]*is-success[^"]*">([^<]+)</span>'
        sizes = re.findall(size_pattern, html)
        
        for i, m in enumerate(simple_magnets):
            size = sizes[i] if i < len(sizes) else 'N/A'
            magnets.append({
                'magnet': m.strip(),
                'size': size.strip(),
            })
    
    return magnets

@click.group()
def cli():
    """javdb.com 搜索工具"""
    pass

@cli.command()
@click.argument('keyword')
@click.option('--limit', '-n', default=10, help='结果数量')
@click.option('--json-output', '-j', is_flag=True, help='JSON输出')
def search(keyword, limit, json_output):
    """搜索影片"""
    if not json_output:
        console.print(f"[cyan]搜索: {keyword}[/cyan]")
    
    try:
        results = search_javdb(keyword, limit)
        
        if not results:
            if not json_output:
                console.print("[yellow]未找到结果[/yellow]")
            else:
                print("[]")
            return
        
        if json_output:
            print(json.dumps(results, indent=2, ensure_ascii=False))
        else:
            table = Table(title=f"搜索结果: {keyword}")
            table.add_column("#", style="dim", width=3)
            table.add_column("番号", style="cyan")
            table.add_column("标题", max_width=40)
            table.add_column("日期", style="blue")
            
            for i, item in enumerate(results, 1):
                table.add_row(
                    str(i),
                    item['code'],
                    item['title'][:40],
                    item['date']
                )
            
            console.print(table)
            console.print(f"\n使用 [cyan]javdb magnet <番号>[/cyan] 获取磁力链接")
    except Exception as e:
        console.print(f"[red]搜索失败: {e}[/red]")

@cli.command()
@click.argument('code')
@click.option('--json-output', '-j', is_flag=True, help='JSON输出')
@click.option('--first', '-1', is_flag=True, help='只返回第一个磁力链接')
def magnet(code, json_output, first):
    """获取指定番号的磁力链接"""
    if not json_output and not first:
        console.print(f"[cyan]获取磁力链接: {code}[/cyan]")
    
    try:
        # 先搜索获取详情页URL
        results = search_javdb(code, 1)
        
        if not results:
            if not json_output and not first:
                console.print("[yellow]未找到该番号[/yellow]")
            return
        
        detail_url = results[0]['url']
        if not json_output and not first:
            console.print(f"[dim]详情页: {detail_url}[/dim]")
        
        magnets_list = get_magnets(detail_url)
        
        if not magnets_list:
            if not json_output and not first:
                console.print("[yellow]未找到磁力链接（可能需要登录）[/yellow]")
            return
        
        if first:
            # 只输出第一个magnet链接（方便管道使用）
            print(magnets_list[0]['magnet'])
            return
        
        if json_output:
            print(json.dumps(magnets_list, indent=2, ensure_ascii=False))
        else:
            table = Table(title=f"磁力链接: {code}")
            table.add_column("#", style="dim", width=3)
            table.add_column("大小", style="green", width=12)
            table.add_column("磁力链接", max_width=60)
            
            for i, m in enumerate(magnets_list, 1):
                table.add_row(
                    str(i),
                    m['size'],
                    m['magnet'][:60] + '...' if len(m['magnet']) > 60 else m['magnet']
                )
            
            console.print(table)
    except Exception as e:
        console.print(f"[red]获取失败: {e}[/red]")

if __name__ == '__main__':
    cli()
