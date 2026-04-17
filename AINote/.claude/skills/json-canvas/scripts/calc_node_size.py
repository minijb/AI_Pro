#!/usr/bin/env python3
"""
JSON Canvas 节点动态尺寸计算器（Obsidian 校准版）

根据文本内容计算 Obsidian JSON Canvas 节点的理想宽高，
使节点能完整展示所有内容，无需滚动。

特性：
- Obsidian 实际渲染校准的字符像素宽度
- Markdown 标题检测（##/### 使用更大字号和行高）
- 自动换行检测（两遍算法）
- 列表缩进、代码块等特殊处理
- --fix 模式：自动修复 canvas 文件中的节点尺寸

用法:
    python calc_node_size.py --text "文本内容"
    python calc_node_size.py --path canvas.canvas
    python calc_node_size.py --path canvas.canvas --fix
"""

import re
import sys
import json
import math
import argparse
from pathlib import Path

# Windows 控制台 UTF-8 输出
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# ---------------------------------------------------------------------------
# 字符分类正则
# ---------------------------------------------------------------------------

# CJK 统一汉字 + 日文假名 + 韩文
CJK_RE = re.compile(
    r'[\u4e00-\u9fff'       # CJK 统一汉字
    r'\u3400-\u4dbf'        # CJK 统一汉字扩展 A
    r'\u3040-\u309f'        # 平假名
    r'\u30a0-\u30ff'        # 片假名
    r'\uac00-\ud7af]'       # 韩文音节
)

# CJK 全角标点和符号（与汉字等宽渲染）
CJK_PUNCT_RE = re.compile(
    r'[\u3000-\u303f'       # CJK 符号和标点（「」『』〈〉等）
    r'\uff00-\uff60'        # 全角 ASCII 变体
    r'\uffe0-\uffef]'       # 全角符号
)

# Emoji（宽字符）
EMOJI_RE = re.compile(
    r'[\U0001F300-\U0001F9FF'
    r'\U0001FA00-\U0001FA6F'
    r'\U0001FA70-\U0001FAFF'
    r'\u2600-\u26FF'
    r'\u2700-\u27BF]'
)

# 装饰性箭头符号
ARROW_CHARS = frozenset(('↓', '→', '←', '↑', '↔', '•', '○', '◇', '▸'))

# Unicode 变体选择符（零宽，不占空间）
VARIATION_SELECTORS = frozenset(('\ufe0e', '\ufe0f'))

# ---------------------------------------------------------------------------
# 像素常数（Obsidian Canvas 校准 v2 — 基于实际渲染截图修正）
# ---------------------------------------------------------------------------

# 字符像素宽度（正常文本，~16px 字号）
PX_CJK = 20          # CJK 字符
PX_CJK_PUNCT = 20    # CJK 全角标点「」（）
PX_EMOJI = 28        # Emoji（canvas 中渲染较大）
PX_ALPHA = 11        # 英文字母/数字
PX_SPACE = 5         # 空格
PX_PUNCT_HALF = 7    # 半角标点 , . ; : ! ?
PX_PATH = 9          # 路径符号 . / - _ :
PX_MONO = 10         # 等宽字体（代码块内）

# 标题字符缩放系数（Obsidian ## 标题用更大字号渲染）
HEADING_SCALE = {
    1: 2.0,   # # Heading 1
    2: 1.75,  # ## Heading 2
    3: 1.45,  # ### Heading 3
    4: 1.25,  # #### Heading 4
}

# 行高（px）— 含行间距和 margin
LH_NORMAL = 34       # 普通文本行
LH_H1 = 64           # # 标题（含上下 margin）
LH_H2 = 56           # ## 标题
LH_H3 = 46           # ### 标题
LH_H4 = 38           # #### 标题
LH_EMPTY = 18        # 空行
LH_CODE = 28         # 代码块行
LH_FENCE = 28        # 代码围栏行 ```

# 节点参数
DEFAULT_MIN_W = 220
DEFAULT_MAX_W = 800   # 允许更宽的节点以避免标题换行
DEFAULT_PAD = 24      # 节点内边距（每侧，Obsidian 实测约 20-24px）
GRID_SIZE = 20        # 尺寸对齐网格

# 列表缩进像素
LIST_INDENT_PX = 28


# ---------------------------------------------------------------------------
# 字符像素宽度
# ---------------------------------------------------------------------------

def char_px(ch: str) -> float:
    """根据字符类型返回像素宽度（正常文本字号）。"""
    if ch in VARIATION_SELECTORS:
        return 0  # 变体选择符不占宽度
    if CJK_RE.match(ch):
        return PX_CJK
    if CJK_PUNCT_RE.match(ch):
        return PX_CJK_PUNCT
    if EMOJI_RE.match(ch):
        return PX_EMOJI
    if ch == ' ':
        return PX_SPACE
    if ch in './-_:':
        return PX_PATH
    if ch.isalnum():
        return PX_ALPHA
    return PX_PUNCT_HALF


# ---------------------------------------------------------------------------
# Markdown 解析辅助
# ---------------------------------------------------------------------------

def detect_heading_level(raw_line: str) -> int:
    """检测标题级别。返回 1-4 或 0（非标题）。"""
    stripped = raw_line.strip()
    if stripped.startswith('#### '):
        return 4
    if stripped.startswith('### '):
        return 3
    if stripped.startswith('## '):
        return 2
    if stripped.startswith('# '):
        return 1
    return 0


def line_height(raw_line: str, in_code_block: bool = False) -> int:
    """根据行类型返回行高（px）。"""
    if in_code_block:
        return LH_CODE

    stripped = raw_line.strip()
    if stripped == '':
        return LH_EMPTY
    if stripped.startswith('```'):
        return LH_FENCE

    level = detect_heading_level(raw_line)
    if level == 1:
        return LH_H1
    if level == 2:
        return LH_H2
    if level == 3:
        return LH_H3
    if level == 4:
        return LH_H4

    return LH_NORMAL


def strip_markdown_for_width(line: str) -> tuple[str, int]:
    """
    移除 Markdown 语法，保留可见字符，返回 (visible_text, extra_indent_px)。

    extra_indent_px 用于列表项缩进等额外宽度。
    """
    text = line
    indent_px = 0

    # 移除行首标题标记 (# ## ### ####)
    text = re.sub(r'^#{1,6}\s+', '', text)

    # 列表前缀：记录缩进，移除标记
    m = re.match(r'^(\s*)([-*+]|\d+\.)\s', text)
    if m:
        indent_px = LIST_INDENT_PX
        text = text[m.end():]

    # 块引用前缀
    text = re.sub(r'^>\s*', '', text)

    # Wikilinks: [[display|target]] → display, [[target]] → target
    text = re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]', r'\1', text)
    text = re.sub(r'\[\[([^\]]+)\]\]', r'\1', text)

    # Markdown links: [text](url) → text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)

    # 粗体/斜体包裹（保留内容）
    text = re.sub(r'\*{1,3}(.+?)\*{1,3}', r'\1', text)
    text = re.sub(r'_{1,3}(.+?)_{1,3}', r'\1', text)

    # 删除线
    text = re.sub(r'~~(.+?)~~', r'\1', text)

    # 行内代码：保留内容
    text = re.sub(r'`(.+?)`', r'\1', text)

    # HTML 标签
    text = re.sub(r'<[^>]+>', '', text)

    return text.strip(), indent_px


# ---------------------------------------------------------------------------
# 装饰箭头检测
# ---------------------------------------------------------------------------

def is_decorative_arrow(text: str) -> bool:
    """
    判断是否为装饰性箭头节点。
    这类节点使用单字符或短箭头，应保持小尺寸。
    """
    stripped = text.strip()
    if stripped in ARROW_CHARS:
        return True
    # 短箭头标签，如 "↓ 有"、"→ 无"
    if len(stripped) <= 6 and any(stripped.startswith(a) for a in ('↓', '→', '←', '↑')):
        return True
    return False


# ---------------------------------------------------------------------------
# 网格对齐
# ---------------------------------------------------------------------------

def snap_to_grid(value: float, grid: int = GRID_SIZE) -> int:
    """将值向上取整到 grid 的倍数。"""
    v = int(value)
    return ((v + grid - 1) // grid) * grid


# ---------------------------------------------------------------------------
# 核心尺寸计算
# ---------------------------------------------------------------------------

def calc_line_px(raw_line: str, heading_level: int = 0,
                 in_code_block: bool = False) -> float:
    """计算单行的像素宽度。"""
    visible, indent_px = strip_markdown_for_width(raw_line)

    if in_code_block:
        # 等宽字体
        px = sum(PX_MONO for _ in visible)
    else:
        px = sum(char_px(c) for c in visible)
        # 标题缩放
        if heading_level > 0:
            scale = HEADING_SCALE.get(heading_level, 1.0)
            px *= scale

    return px + indent_px


def calc_node_size(
    text: str,
    min_w: int = DEFAULT_MIN_W,
    max_w: int = DEFAULT_MAX_W,
    pad: int = DEFAULT_PAD,
) -> tuple[int, int]:
    """
    根据文本内容计算节点尺寸（px）。

    参数:
        text: 节点的完整文本内容（包含 Markdown）
        min_w: 最小宽度，默认 220px
        max_w: 最大宽度，默认 600px
        pad: 节点内边距，默认 20px（每侧）

    返回:
        (width, height) 元组，单位 px，均为 GRID_SIZE 的倍数
    """
    if is_decorative_arrow(text):
        return (60, 60)

    lines = text.split('\n')
    in_code_block = False

    # ---------------------------------------------------------------
    # Pass 1: 计算自然宽度（从最长行决定）
    # ---------------------------------------------------------------
    max_line_px = 0.0

    for raw_line in lines:
        stripped = raw_line.strip()
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            continue

        heading_level = 0 if in_code_block else detect_heading_level(raw_line)
        px = calc_line_px(raw_line, heading_level, in_code_block)
        max_line_px = max(max_line_px, px)

    width = max(min_w, int(max_line_px) + pad * 2)
    width = snap_to_grid(width)
    width = min(width, max_w)

    # ---------------------------------------------------------------
    # Pass 2: 计算高度（含自动换行检测）
    # ---------------------------------------------------------------
    content_w = width - pad * 2
    total_h = 0.0
    in_code_block = False

    for raw_line in lines:
        stripped = raw_line.strip()

        if stripped.startswith('```'):
            in_code_block = not in_code_block
            total_h += LH_FENCE
            continue

        lh = line_height(raw_line, in_code_block)

        # 空行直接加高度
        if stripped == '':
            total_h += LH_EMPTY
            continue

        heading_level = 0 if in_code_block else detect_heading_level(raw_line)
        px = calc_line_px(raw_line, heading_level, in_code_block)

        # 自动换行检测
        if px > content_w and content_w > 0:
            wrapped_lines = math.ceil(px / content_w)
            total_h += wrapped_lines * lh
        else:
            total_h += lh

    height = int(total_h) + pad * 2
    height = snap_to_grid(height)

    return width, height


# ---------------------------------------------------------------------------
# Canvas 文件检查
# ---------------------------------------------------------------------------

def check_canvas(path: str | Path) -> list[dict]:
    """
    检查 canvas 文件中所有 text 节点的尺寸是否足够。

    返回:
        节点检查结果列表，每项包含 id, text, current, ideal, needs_fix, is_decorative
    """
    path = Path(path)
    with open(path, encoding='utf-8') as f:
        data = json.load(f)

    results = []
    for node in data.get('nodes', []):
        if node.get('type') != 'text' or 'text' not in node:
            continue

        text = node['text']
        cur_w = node.get('width', 0)
        cur_h = node.get('height', 0)
        ideal_w, ideal_h = calc_node_size(text)
        decorative = is_decorative_arrow(text)

        needs_fix = (cur_w < ideal_w or cur_h < ideal_h) and not decorative

        results.append({
            'id': node['id'],
            'text': text[:60],
            'width': cur_w,
            'height': cur_h,
            'ideal_width': ideal_w,
            'ideal_height': ideal_h,
            'needs_fix': needs_fix,
            'is_decorative': decorative,
        })

    return results


def fix_canvas(path: str | Path, output: str | Path | None = None) -> list[dict]:
    """
    修复 canvas 文件中所有 text 节点的尺寸。

    只增大尺寸，不缩小（保留用户手动调大的节点）。

    参数:
        path: 输入 canvas 文件路径
        output: 输出路径（默认原地修改）

    返回:
        修改记录列表
    """
    path = Path(path)
    with open(path, encoding='utf-8') as f:
        data = json.load(f)

    changes = []
    for node in data.get('nodes', []):
        if node.get('type') != 'text' or 'text' not in node:
            continue

        text = node['text']
        if is_decorative_arrow(text):
            continue

        cur_w = node.get('width', 0)
        cur_h = node.get('height', 0)
        ideal_w, ideal_h = calc_node_size(text)

        new_w = max(cur_w, ideal_w)
        new_h = max(cur_h, ideal_h)

        if new_w != cur_w or new_h != cur_h:
            changes.append({
                'id': node['id'],
                'text': text[:60],
                'old': f'{cur_w}x{cur_h}',
                'new': f'{new_w}x{new_h}',
            })
            node['width'] = new_w
            node['height'] = new_h

    out_path = Path(output) if output else path
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent='\t')

    return changes


# ---------------------------------------------------------------------------
# 报告输出
# ---------------------------------------------------------------------------

def print_report(results: list[dict]) -> None:
    """打印检查报告。"""
    needs_fix = [r for r in results if r['needs_fix']]
    decorative = [r for r in results if r['is_decorative']]
    ok = [r for r in results if not r['needs_fix'] and not r['is_decorative']]

    print(f"  总计: {len(results)} 个 text 节点")
    print(f"  正常: {len(ok)}  需修复: {len(needs_fix)}  装饰: {len(decorative)}\n")

    if needs_fix:
        print(f"  ⚠ {len(needs_fix)} 个节点尺寸不足:\n")
        print(f"    {'ID':<28} {'当前':<12} {'理想':<12} {'状态'}")
        print(f"    {'-'*28} {'-'*12} {'-'*12} {'-'*6}")
        for r in needs_fix:
            print(
                f"    {r['id']:<28} "
                f"{r['width']}x{r['height']:<8} "
                f"{r['ideal_width']}x{r['ideal_height']:<8} "
                f"← TOO SMALL"
            )
        print()

    if decorative:
        print(f"  • {len(decorative)} 个装饰节点（保持小尺寸）")
        print()


def print_fix_report(changes: list[dict], out_path: Path) -> None:
    """打印修复报告。"""
    if not changes:
        print("  ✓ 所有节点尺寸已足够，无需修复。")
        return

    print(f"  ✓ 已修复 {len(changes)} 个节点:\n")
    print(f"    {'ID':<28} {'旧尺寸':<12} {'新尺寸':<12}")
    print(f"    {'-'*28} {'-'*12} {'-'*12}")
    for c in changes:
        print(f"    {c['id']:<28} {c['old']:<12} {c['new']:<12}")
    print(f"\n  → 已保存到 {out_path}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description='JSON Canvas 节点动态尺寸计算器（Obsidian 校准版）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python calc_node_size.py --text "## 标题\\n\\n内容内容"
  python calc_node_size.py --path canvas.canvas
  python calc_node_size.py --path canvas.canvas --fix
  python calc_node_size.py --path canvas.canvas --fix -o fixed.canvas
        ''',
    )
    parser.add_argument('--text', type=str, help='计算单条文本的尺寸')
    parser.add_argument('--path', type=str, help='检查/修复 canvas 文件')
    parser.add_argument('--fix', action='store_true', help='修复节点尺寸（只增大不缩小）')
    parser.add_argument('-o', '--output', type=str, help='输出文件路径（默认原地修改）')
    parser.add_argument('--verbose', '-v', action='store_true', help='显示详细信息')
    args = parser.parse_args()

    if args.text:
        w, h = calc_node_size(args.text)
        print(f"  文本: {args.text!r}")
        print(f"  尺寸: {w} x {h} px")
        if args.verbose:
            lines = args.text.split('\n')
            in_code = False
            print(f"  行数: {len(lines)}")
            for i, raw_line in enumerate(lines, 1):
                stripped = raw_line.strip()
                if stripped.startswith('```'):
                    in_code = not in_code
                hl = 0 if in_code else detect_heading_level(raw_line)
                px = calc_line_px(raw_line, hl, in_code)
                lh = line_height(raw_line, in_code)
                visible, indent = strip_markdown_for_width(raw_line)
                print(f"    L{i}: {px:.0f}px (lh={lh}) → {visible[:50]!r}"
                      f"{f' +indent={indent}' if indent else ''}")

    elif args.path:
        print(f"\n  文件: {args.path}\n")

        if args.fix:
            changes = fix_canvas(args.path, args.output)
            out = Path(args.output) if args.output else Path(args.path)
            print_fix_report(changes, out)
        else:
            results = check_canvas(args.path)
            print_report(results)

            if args.verbose:
                needs_fix = [r for r in results if r['needs_fix']]
                if needs_fix:
                    print("  JSON 修复建议:")
                    fixes = {r['id']: {'width': r['ideal_width'], 'height': r['ideal_height']}
                             for r in needs_fix}
                    print(f"  {json.dumps(fixes, indent=2)}")
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
