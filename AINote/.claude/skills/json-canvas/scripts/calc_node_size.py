#!/usr/bin/env python3
"""
JSON Canvas 节点动态尺寸计算器

根据文本内容计算 Obsidian JSON Canvas 节点的理想宽高，
使节点能完整展示所有内容，无需滚动。

用法:
    python calc_node_size.py --text "文本内容"
    python calc_node_size.py --path canvas.canvas
"""

import re
import json
import argparse
from pathlib import Path

# Unicode 字符范围
CJK_RE = re.compile(r'[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af]')
EMOJI_RE = re.compile(r'[\U0001F300-\U0001F9FF]')
# 装饰性箭头符号
ARROW_CHARS = frozenset(('↓', '→', '←', '↑', '↔', '•', '○', '◇', '▸'))


def char_px(ch: str) -> int:
    """根据字符类型返回像素宽度。"""
    if CJK_RE.match(ch):
        return 8   # 中文/日文/韩文
    if EMOJI_RE.match(ch):
        return 14   # Emoji
    if ch.isalnum() or ch in './-_:':
        return 6    # 英文/数字/路径符号
    return 3        # 标点符号


def strip_markdown(text: str) -> str:
    """移除 Markdown 和 HTML 语法，只保留可见字符。"""
    # 移除 Markdown 标记
    text = re.sub(r'[#*_`\[\]()>\-\|]', '', text)
    # 移除 HTML 标签（包括 <br/>, <sub>, </sub> 等）
    text = re.sub(r'<[^>]+>', '', text)
    # 规范化空格
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def is_decorative_arrow(text: str) -> bool:
    """
    判断是否为装饰性箭头节点。
    这类节点使用单字符或短箭头，应保持小尺寸，不受算法约束。
    """
    stripped = text.strip()
    if stripped in ARROW_CHARS:
        return True
    # 短箭头标签，如 "↓ 有"、"→ 无"
    if len(stripped) <= 6 and any(stripped.startswith(a) for a in ('↓', '→', '←', '↑')):
        return True
    return False


def calc_node_size(
    text: str,
    min_w: int = 220,
    max_w: int = 500,
    pad: int = 20,
    lh: int = 20,
) -> tuple[int, int]:
    """
    根据文本内容计算节点尺寸（px）。

    参数:
        text: 节点的完整文本内容（包含 Markdown）
        min_w: 最小宽度，默认 220px
        max_w: 最大宽度，默认 500px
        pad: 节点内边距，默认 20px（左右各 20px）
        lh: 行高，默认 20px

    返回:
        (width, height) 元组，单位 px，均为 20 的倍数
    """
    if is_decorative_arrow(text):
        # 装饰性箭头：保持小尺寸
        return (60, 60)

    lines = text.strip().split('\n')
    max_px = 0

    for line in lines:
        stripped = strip_markdown(line)
        px = sum(char_px(c) for c in stripped)
        max_px = max(max_px, px)

    # 宽度：最长行像素 + 左右 padding，取整到 20 的倍数
    width = max(min_w, max_px + pad * 2)
    width = (width + 19) // 20 * 20
    width = min(width, max_w)

    # 高度：行数 × 行高 + 上下 padding，取整到 20 的倍数
    height = len(lines) * lh + pad * 2
    height = (height + 19) // 20 * 20

    return width, height


def check_canvas(path: str | Path) -> list[dict]:
    """
    检查 canvas 文件中所有节点的尺寸是否合适。

    返回:
        问题节点列表，每项包含 id, text, current, ideal, is_decorative
    """
    path = Path(path)
    with open(path, encoding='utf-8') as f:
        data = json.load(f)

    issues = []
    for node in data.get('nodes', []):
        if node.get('type') != 'text' or 'text' not in node:
            continue

        text = node['text']
        cur_w = node.get('width')
        cur_h = node.get('height')
        ideal_w, ideal_h = calc_node_size(text)
        decorative = is_decorative_arrow(text)

        # 判断是否需要修复
        needs_fix = (cur_w < ideal_w or cur_h < ideal_h) and not decorative

        issues.append({
            'id': node['id'],
            'text': text[:60],
            'width': cur_w,
            'height': cur_h,
            'ideal_width': ideal_w,
            'ideal_height': ideal_h,
            'needs_fix': needs_fix,
            'is_decorative': decorative,
        })

    return issues


def print_report(issues: list[dict]) -> None:
    """打印检查报告。"""
    needs_fix = [i for i in issues if i['needs_fix']]
    decorative = [i for i in issues if i['is_decorative']]

    if not needs_fix and not decorative:
        print("✓ 所有节点尺寸正确，无问题。")
        return

    if needs_fix:
        print(f"⚠   {len(needs_fix)} 个节点需要修复:\n")
        print(f"  {'ID':<28} {'当前尺寸':<14} {'理想尺寸':<14} {'状态'}")
        print(f"  {'-'*28} {'-'*14} {'-'*14} {'-'*8}")
        for node in needs_fix:
            print(
                f"  {node['id']:<28} "
                f"{node['width']}x{node['height']:<10} "
                f"{node['ideal_width']}x{node['ideal_height']:<10} "
                f"← 需修复"
            )
        print()

    if decorative:
        print(f"•  {len(decorative)} 个装饰性节点（保持小尺寸）:\n")
        for node in decorative:
            print(f"  {node['id']:<28} {node['width']}x{node['height']} (保持)")
        print()


def main():
    parser = argparse.ArgumentParser(
        description='计算 JSON Canvas 节点动态尺寸',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python calc_node_size.py --text "## 标题\\n\\n内容内容"
  python calc_node_size.py --path ../wiki_workflow-ingest.canvas
  python calc_node_size.py --text "↓" --verbose
        ''',
    )
    parser.add_argument('--text', type=str, help='直接计算单条文本的尺寸')
    parser.add_argument('--path', type=str, help='检查 canvas 文件中的所有节点')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细算法信息')
    args = parser.parse_args()

    if args.text:
        w, h = calc_node_size(args.text)
        print(f"文本: {args.text!r}")
        print(f"尺寸: {w} x {h} px")
        if args.verbose:
            lines = args.text.strip().split('\n')
            print(f"行数: {len(lines)}")
            for i, line in enumerate(lines, 1):
                stripped = strip_markdown(line)
                px = sum(char_px(c) for c in stripped)
                print(f"  第{i}行: {px}px  →  {stripped[:50]!r}")

    elif args.path:
        issues = check_canvas(args.path)
        print(f"文件: {args.path}\n")
        print_report(issues)

        # 输出 JSON 格式供脚本调用
        needs_fix = [i for i in issues if i['needs_fix']]
        if needs_fix and args.verbose:
            print("\nJSON 输出（可被外部脚本解析）:")
            print(json.dumps({n['id']: {'width': n['ideal_width'], 'height': n['ideal_height']} for n in needs_fix}, indent=2))
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
