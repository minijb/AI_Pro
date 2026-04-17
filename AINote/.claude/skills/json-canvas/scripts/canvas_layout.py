#!/usr/bin/env python3
"""
JSON Canvas 布局对齐工具

自动检测 canvas 布局类型，对不同宽高的节点应用智能对齐，
消除因节点尺寸不一致造成的锯齿排版。

支持的布局类型：
- vertical_flow：垂直流（同列节点中心对齐 x）
- horizontal_flow：水平流（同行节点中心对齐 y）
- tree：树形（子节点组居中于父节点，同层顶部对齐）
- mindmap：思维导图（右分支左对齐，左分支右对齐）
- grid：网格/看板（列内左对齐，跨列顶部对齐）

用法:
    python canvas_layout.py input.canvas                    # 检测 + 报告
    python canvas_layout.py input.canvas --fix              # 修复对齐
    python canvas_layout.py input.canvas --fix --fix-sizes  # 修复尺寸 + 对齐
    python canvas_layout.py input.canvas --layout tree      # 指定布局类型
"""

import sys
import json
import argparse
from pathlib import Path
from collections import defaultdict

# Windows 控制台 UTF-8 输出
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# 导入尺寸计算模块
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from calc_node_size import calc_node_size, is_decorative_arrow

# ---------------------------------------------------------------------------
# 常数
# ---------------------------------------------------------------------------

MIN_GAP = 60          # 节点之间最小间隙 (px)（含边距的宽松检测）
GRID = 20             # 坐标对齐网格
HORIZONTAL_SPACING = 180  # 分支节点水平间距
CHILD_GAP = 60        # 树形布局子节点间距
VERTICAL_GAP = 80     # 垂直流节点间距


def snap_pos(value: float, grid: int = 10) -> int:
    """将坐标 snap 到最近的 grid 倍数（四舍五入，用于位置）。
    使用 10px 网格（而非 20px）以获得更精确的中心对齐。"""
    return round(value / grid) * grid


# ---------------------------------------------------------------------------
# 节点分类
# ---------------------------------------------------------------------------

def separate_nodes(nodes: list[dict]) -> tuple[list, list, list]:
    """
    将节点分为三类：group、decorative arrow、content。

    返回: (group_nodes, arrow_nodes, content_nodes)
    """
    groups = []
    arrows = []
    content = []

    for node in nodes:
        if node.get('type') == 'group':
            groups.append(node)
        elif node.get('type') == 'text' and is_decorative_arrow(node.get('text', '')):
            arrows.append(node)
        else:
            content.append(node)

    return groups, arrows, content


# ---------------------------------------------------------------------------
# 布局检测
# ---------------------------------------------------------------------------

def detect_layout(content_nodes: list[dict], edges: list[dict],
                  all_nodes: list[dict] | None = None) -> str:
    """
    从 edge 拓扑自动检测布局类型。

    返回: 'vertical_flow' | 'horizontal_flow' | 'tree' | 'mindmap' | 'grid' | 'unknown'
    """
    if not edges:
        return 'unknown'

    content_ids = {n['id'] for n in content_nodes}
    has_groups = any(n.get('type') == 'group' for n in (all_nodes or []))

    # 统计 edge 方向
    bottom_top = 0
    right_left = 0
    left_right = 0

    for edge in edges:
        fs = edge.get('fromSide', '')
        ts = edge.get('toSide', '')
        # 只统计连接 content 节点的边
        if edge.get('fromNode') not in content_ids and edge.get('toNode') not in content_ids:
            continue
        if fs == 'bottom' and ts == 'top':
            bottom_top += 1
        elif fs == 'right' and ts == 'left':
            right_left += 1
        elif fs == 'left' and ts == 'right':
            left_right += 1

    total = bottom_top + right_left + left_right
    if total == 0:
        return 'grid' if has_groups else 'unknown'

    # 有 group 节点且边方向不是压倒性的某个方向 → grid
    if has_groups and max(bottom_top, right_left, left_right) / total < 0.8:
        return 'grid'

    # 同时有 left→right 和 right→left → 可能是 flowchart 或 mindmap
    if left_right > 0 and right_left > 0:
        # 有明显主列（≥3 条 bottom→top）→ flowchart，否则 → mindmap
        if bottom_top >= 3:
            return 'flowchart'
        return 'mindmap'

    # 垂直流：>60% 的边是 bottom→top
    if bottom_top / total > 0.6:
        # 有分叉 → tree，否则 → vertical_flow
        parent_children: dict[str, int] = {}
        for edge in edges:
            if edge.get('fromSide') == 'bottom' and edge.get('toSide') == 'top':
                parent = edge['fromNode']
                parent_children[parent] = parent_children.get(parent, 0) + 1
        has_branching = any(c > 1 for c in parent_children.values())
        return 'tree' if has_branching else 'vertical_flow'

    # 水平流：>60% 的边是 right→left
    if right_left > 0 and right_left / total > 0.6:
        return 'horizontal_flow'

    return 'unknown'


# ---------------------------------------------------------------------------
# 列/行检测
# ---------------------------------------------------------------------------

def detect_columns(content_nodes: list[dict], edges: list[dict]) -> list[list[str]]:
    """
    垂直流：追踪 bottom→top edge 链识别独立列。
    每列是一组由 edge 串联的节点 ID。
    """
    # 建立 parent→children 邻接表（只看 bottom→top 边）
    children_of: dict[str, list[str]] = defaultdict(list)
    all_children: set[str] = set()
    content_ids = {n['id'] for n in content_nodes}

    for edge in edges:
        if edge.get('fromSide') == 'bottom' and edge.get('toSide') == 'top':
            parent = edge['fromNode']
            child = edge['toNode']
            if parent in content_ids and child in content_ids:
                children_of[parent].append(child)
                all_children.add(child)

    # 找根节点（无入边的 content 节点）
    roots = [nid for nid in content_ids if nid not in all_children]

    # 如果没有根节点，用 y 最小的节点作为根
    if not roots:
        node_map = {n['id']: n for n in content_nodes}
        roots = [min(content_ids, key=lambda nid: node_map[nid]['y'])]

    # BFS 从每个根收集列成员
    columns: list[list[str]] = []
    visited: set[str] = set()

    for root in sorted(roots):
        if root in visited:
            continue
        column: list[str] = []
        queue = [root]
        while queue:
            nid = queue.pop(0)
            if nid in visited:
                continue
            visited.add(nid)
            column.append(nid)
            for child in children_of.get(nid, []):
                queue.append(child)
        if column:
            columns.append(column)

    # 把未被追踪到的孤立节点也加入（每个独立成列）
    for n in content_nodes:
        if n['id'] not in visited:
            columns.append([n['id']])
            visited.add(n['id'])

    return columns


def detect_rows(content_nodes: list[dict], edges: list[dict]) -> list[list[str]]:
    """
    水平流：追踪 right→left edge 链识别独立行。
    """
    children_of: dict[str, list[str]] = defaultdict(list)
    all_children: set[str] = set()
    content_ids = {n['id'] for n in content_nodes}

    for edge in edges:
        if edge.get('fromSide') == 'right' and edge.get('toSide') == 'left':
            parent = edge['fromNode']
            child = edge['toNode']
            if parent in content_ids and child in content_ids:
                children_of[parent].append(child)
                all_children.add(child)

    roots = [nid for nid in content_ids if nid not in all_children]
    if not roots:
        node_map = {n['id']: n for n in content_nodes}
        roots = [min(content_ids, key=lambda nid: node_map[nid]['x'])]

    rows: list[list[str]] = []
    visited: set[str] = set()

    for root in sorted(roots):
        if root in visited:
            continue
        row: list[str] = []
        queue = [root]
        while queue:
            nid = queue.pop(0)
            if nid in visited:
                continue
            visited.add(nid)
            row.append(nid)
            for child in children_of.get(nid, []):
                queue.append(child)
        if row:
            rows.append(row)

    for n in content_nodes:
        if n['id'] not in visited:
            rows.append([n['id']])
            visited.add(n['id'])

    return rows


def group_by_y_band(nodes: list[dict], tolerance: int = 60) -> list[list[dict]]:
    """按 y 坐标中心点分组（中心点差 <= tolerance 的归为同一行）。"""
    if not nodes:
        return []

    sorted_nodes = sorted(nodes, key=lambda n: n['y'] + n['height'] / 2)
    groups: list[list[dict]] = []
    current_group = [sorted_nodes[0]]
    current_center = sorted_nodes[0]['y'] + sorted_nodes[0]['height'] / 2

    for node in sorted_nodes[1:]:
        center = node['y'] + node['height'] / 2
        if abs(center - current_center) <= tolerance:
            current_group.append(node)
        else:
            groups.append(current_group)
            current_group = [node]
            current_center = center

    groups.append(current_group)
    return groups


# ---------------------------------------------------------------------------
# 对齐函数
# ---------------------------------------------------------------------------

def align_column_center_x(node_ids: list[str], node_map: dict[str, dict]) -> int:
    """
    垂直流列：所有节点共享同一 center_x（中心对齐）。
    返回使用的 center_x。
    """
    nodes = [node_map[nid] for nid in node_ids if nid in node_map]
    if not nodes:
        return 0

    widest = max(nodes, key=lambda n: n['width'])
    target_cx = widest['x'] + widest['width'] / 2

    for node in nodes:
        new_x = target_cx - node['width'] / 2
        node['x'] = snap_pos(new_x)

    return int(target_cx)

def _detect_sibling_groups(children_of: dict, edge_info: dict,
                          node_map: dict[str, dict]) -> list[tuple[str, list[tuple[str, str]]]]:
    """
    识别"分支组"：同一父节点的多个子节点，fromSide 不同（left/bottom/right 各一个）。
    这些子节点应作为水平兄弟排列在同一行。

    返回: [(parent_id, [(child_id, fromSide)])] 列表
    """
    groups = []
    for parent_id, children in children_of.items():
        child_sides = []
        for child_id in children:
            fs = edge_info.get((parent_id, child_id), ('', ''))[0]
            if fs in ('left', 'right', 'bottom'):
                child_sides.append((child_id, fs))

        # 至少 2 个来自不同 fromSide → 分支组
        if len(child_sides) >= 2:
            sides = set(cs[1] for cs in child_sides)
            if len(sides) >= 2:
                groups.append((parent_id, child_sides))

    return groups


def _resolve_y_topo(content_nodes: list[dict], edges: list[dict],
                    node_map: dict[str, dict],
                    children_of: dict, parents_of: dict) -> dict[str, int]:
    """
    Phase 1: 按拓扑层级（max ancestor depth）分批处理 y 坐标。

    算法：
    1. 计算每个节点的最长路径深度（从根）
    2. 按深度分层：先处理深度 0，再处理深度 1……确保深层节点在其所有祖先之后处理
    3. 每层内按 x 坐标排序（从左到右）

    y(node) = max(所有父节点底部) + VERTICAL_GAP

    返回 node_id -> y 值的映射。
    """
    content_ids = {n['id'] for n in content_nodes}

    # 计算最长路径深度（DFS）
    def max_depth(nid: str, visited: set[str]) -> int:
        if nid in visited:
            return 0
        parents = parents_of.get(nid, [])
        if not parents:
            return 0
        return 1 + max(max_depth(p, visited | {nid}) for p in parents)

    depth: dict[str, int] = {}
    for nid in content_ids:
        depth[nid] = max_depth(nid, set())

    # 收集所有根节点（无父节点）
    roots = [nid for nid in content_ids if not parents_of.get(nid)]
    if not roots:
        roots = [min(content_ids, key=lambda nid: node_map[nid]['y'])]

    # 计算每个节点的 x 中心（用于同层内从左到右排序）
    x_of: dict[str, float] = {}
    for n in content_nodes:
        x_of[n['id']] = n['x'] + n['width'] / 2

    # 按层级处理：BFS 逐层
    y_map: dict[str, int] = {}
    start_y = node_map[roots[0]]['y']

    def process_batch(batch: list[str]) -> None:
        """处理一批节点（同一深度层级）。"""
        # 按 x 从小到大排序（从左到右）
        batch.sort(key=lambda nid: x_of.get(nid, 0))

        for nid in batch:
            node = node_map[nid]
            # 找所有已放置的父节点
            placed_parents = [p for p in parents_of.get(nid, []) if p in y_map]
            if not placed_parents:
                y_map[nid] = start_y
            else:
                max_bottom = max(y_map[p] + node_map[p]['height'] for p in placed_parents)
                y_map[nid] = snap_pos(max_bottom + VERTICAL_GAP)

    # 收集所有节点
    remaining = set(content_ids)
    current_batch = list(roots)

    while current_batch:
        process_batch(current_batch)
        remaining -= set(current_batch)

        # 收集下一层：当前批次节点的子节点（且其所有父节点已在 y_map 中）
        next_batch = []
        for nid in current_batch:
            for child in children_of.get(nid, []):
                if child in remaining:
                    # 检查所有父节点是否都已放置
                    all_parents_placed = all(p in y_map for p in parents_of.get(child, []))
                    if all_parents_placed and child not in next_batch:
                        next_batch.append(child)

        current_batch = next_batch

    # 处理可能遗漏的孤立节点（兜底）
    for nid in remaining:
        if nid not in y_map:
            y_map[nid] = start_y

    return y_map


def _detect_side_branches(content_nodes: list[dict], edges: list[dict],
                          node_map: dict[str, dict],
                          children_of: dict) -> tuple[set[str], str, float]:
    """
    检测侧边分支。

    返回: (side_branch_ids, direction, side_extent)
    direction: 'left' | 'right' | 'none'
    side_extent: 侧边分支最左/最右边缘的 x 坐标
    """
    # 收集所有侧边子节点（fromSide 为 left 或 right）
    left_children: set[str] = set()
    right_children: set[str] = set()

    for edge in edges:
        fn, tn = edge.get('fromNode', ''), edge.get('toNode', '')
        fs = edge.get('fromSide', '')
        if fn not in node_map or tn not in node_map:
            continue
        if fs == 'left':
            left_children.add(tn)
        elif fs == 'right':
            right_children.add(tn)

    side_ids = left_children | right_children

    # 收集这些节点的实际内容节点（排除 group）
    actual_side_ids: set[str] = set()
    for nid in side_ids:
        node = node_map.get(nid)
        if node and node.get('type') != 'group':
            actual_side_ids.add(nid)

    if not actual_side_ids:
        return set(), 'none', 0.0

    # 确定方向：看哪个方向的节点多
    left_actual = {nid for nid in left_children if nid in node_map and node_map[nid].get('type') != 'group'}
    right_actual = {nid for nid in right_children if nid in node_map and node_map[nid].get('type') != 'group'}

    if len(left_actual) >= len(right_actual):
        direction = 'left'
        side_extent = min(node_map[nid]['x'] for nid in left_actual)
    else:
        direction = 'right'
        side_extent = max(node_map[nid]['x'] + node_map[nid]['width'] for nid in right_actual)

    return actual_side_ids, direction, side_extent


def _resolve_x_column(content_nodes: list[dict], node_map: dict[str, dict],
                      children_of: dict, parents_of: dict,
                      edge_info: dict,
                      sibling_groups: list,
                      y_map: dict[str, int],
                      side_branch_ids: set[str] | None = None,
                      side_direction: str = 'none',
                      side_extent: float = 0.0) -> None:
    """
    Phase 2: x 坐标确定。

    1. 以画布中最宽深度 0 节点（入口节点）的中心为基准 x
    2. 所有主流程节点以基准 x 居中（保持相对位置）
    3. 分支组内的子节点以父节点中心水平排列（left → bottom → right）
    4. 分支节点水平方向与主列冲突时，偏移分支组以避免碰撞
    """
    content_ids = {n['id'] for n in content_nodes}

    # 收集所有分支组子节点（和其父节点）
    branch_children: set[str] = set()
    for (_, siblings) in sibling_groups:
        for child_id, _ in siblings:
            branch_children.add(child_id)

    # 找深度 0 的根节点中最宽者，以此为画布 x 基准
    # 深度 0 = 无父节点（roots）
    roots = [n['id'] for n in content_nodes if not parents_of.get(n['id'])]
    if not roots:
        roots = [min(content_ids, key=lambda nid: y_map.get(nid, 0))]
    root_widest = max(roots, key=lambda nid: node_map[nid]['width'])
    root_node = node_map[root_widest]
    root_width = root_node['width']

    # 计算基础基准 x（根节点居中位置）
    base_cx = root_node['x'] + root_width / 2

    # 侧边面板偏移：如果主列附近有侧边面板节点，将主列偏移到远离方向
    # 最小间隙 = 侧边节点最右/最左边缘 + 100px 额外间距
    SIDE_GAP = 100
    if side_branch_ids and side_direction in ('left', 'right'):
        side_x = float(side_extent)
        root_left = base_cx - root_width / 2  # 根节点左边缘

        if side_direction == 'left':
            # 左侧有面板 → 将主列向右移
            # 需要确保根节点左边缘 >= side_x + SIDE_GAP
            needed_left = side_x + SIDE_GAP
            if root_left < needed_left:
                shift = needed_left - root_left
                base_cx += shift
        else:  # right
            # 右侧有面板 → 将主列向左移
            root_right = base_cx + root_width / 2
            needed_right = side_x - SIDE_GAP
            if root_right > needed_right:
                shift = root_right - needed_right
                base_cx -= shift

    # 主流程节点以基准 x 居中对齐（排除分支组的子节点）
    # 记录主列的 x 范围（用于碰撞检测）
    main_col_xs = {}  # node_id -> x
    for nid in content_ids:
        if nid in branch_children:
            continue
        node = node_map[nid]
        nx = snap_pos(base_cx - node['width'] / 2)
        node['x'] = nx
        main_col_xs[nid] = (nx, nx + node['width'])  # left, right

    # 分支组水平排列，同时检测与主列的水平碰撞
    for (parent_id, siblings) in sibling_groups:
        parent = node_map[parent_id]
        parent_cx = parent['x'] + parent['width'] / 2
        parent_y = y_map.get(parent_id, parent['y'])
        parent_bottom = parent_y + parent['height']

        # 按 left=0, bottom=1, right=2 排序
        SIDE_ORDER = {'left': 0, 'bottom': 1, 'right': 2}
        sorted_siblings = sorted(siblings, key=lambda x: SIDE_ORDER.get(x[1], 9))

        # 计算总宽度
        total_w = sum(node_map[c]['width'] for c, _ in sorted_siblings)
        total_w += VERTICAL_GAP * max(0, len(sorted_siblings) - 1)

        # 以 parent_cx 为中心，从左到右排列
        current_x = snap_pos(parent_cx - total_w / 2)

        for child_id, side in sorted_siblings:
            child = node_map[child_id]
            child_top = y_map.get(child_id, child['y'])
            child_bottom = child_top + child['height']

            # 检测与主列的水平碰撞（垂直方向有交集时检查 x 方向）
            if main_col_xs and side in ('left', 'right'):
                for main_id, (main_left, main_right) in main_col_xs.items():
                    main_y = y_map.get(main_id, node_map[main_id]['y'])
                    main_bottom = main_y + node_map[main_id]['height']
                    # 垂直方向有交集
                    if not (child_bottom <= main_y or child_top >= main_bottom):
                        # x 方向有重叠
                        if not (current_x + child['width'] <= main_left or current_x >= main_right):
                            if side == 'left':
                                # 分支在左边 → 不能与主列重叠，确保左分支右边缘 <= 主列左边缘 - MIN_GAP
                                needed_right = main_left - MIN_GAP
                                if current_x + child['width'] > needed_right:
                                    current_x = snap_pos(needed_right - child['width'])
                            elif side == 'right':
                                # 分支在右边 → 不能与主列重叠，确保右分支左边缘 >= 主列右边缘 + MIN_GAP
                                needed_left = main_right + MIN_GAP
                                if current_x < needed_left:
                                    current_x = snap_pos(needed_left)

            child['x'] = snap_pos(current_x)
            # y 已在 Phase 1 确定，无需调整
            current_x += child['width'] + VERTICAL_GAP


def layout_vertical_flow(content_nodes: list[dict], edges: list[dict],
                         node_map: dict[str, dict]) -> None:
    """
    垂直流布局（完整重写，支持分支/合并节点）。

    流程：
    1. 建立邻接表和父子关系
    2. Phase 1: 拓扑排序确定 y 坐标（每个节点 y = max(父节点底部) + GAP）
    3. Phase 2: x 坐标（分支组水平排列，其余主列居中）
    4. 将计算结果写入节点
    """
    content_ids = {n['id'] for n in content_nodes}

    # 建立邻接表
    children_of: dict[str, list[str]] = defaultdict(list)
    parents_of: dict[str, list[str]] = defaultdict(list)
    edge_info: dict[tuple[str, str], tuple[str, str]] = {}

    for edge in edges:
        fn = edge.get('fromNode', '')
        tn = edge.get('toNode', '')
        if fn not in content_ids or tn not in content_ids:
            continue
        children_of[fn].append(tn)
        parents_of[tn].append(fn)
        edge_info[(fn, tn)] = (edge.get('fromSide', ''), edge.get('toSide', ''))

    # Phase 1: y 坐标
    y_map = _resolve_y_topo(content_nodes, edges, node_map, children_of, parents_of)

    # 检测侧边分支，用于后续 x 坐标偏移
    side_ids, side_dir, side_extent = _detect_side_branches(
        content_nodes, edges, node_map, children_of)

    # Phase 2: x 坐标（含侧边面板偏移）
    sibling_groups = _detect_sibling_groups(children_of, edge_info, node_map)
    _resolve_x_column(content_nodes, node_map, children_of, parents_of, edge_info,
                     sibling_groups, y_map,
                     side_branch_ids=side_ids,
                     side_direction=side_dir,
                     side_extent=side_extent)

    # 写回节点
    for nid, y in y_map.items():
        if nid in node_map:
            node_map[nid]['y'] = y


def align_row_center_y(node_ids: list[str], node_map: dict[str, dict]) -> int:
    """
    水平流行：所有节点共享同一 center_y（中心对齐）。
    返回使用的 center_y。
    """
    nodes = [node_map[nid] for nid in node_ids if nid in node_map]
    if not nodes:
        return 0

    tallest = max(nodes, key=lambda n: n['height'])
    target_cy = tallest['y'] + tallest['height'] / 2

    for node in nodes:
        new_y = target_cy - node['height'] / 2
        node['y'] = snap_pos(new_y)

    return int(target_cy)


def align_tree(content_nodes: list[dict], edges: list[dict],
               node_map: dict[str, dict]) -> None:
    """
    树形布局：
    1. 同层子节点顶部对齐（共享 y）
    2. 子节点组居中于父节点下方
    """
    # 建立 parent→children
    children_of: dict[str, list[str]] = defaultdict(list)
    all_children: set[str] = set()
    content_ids = {n['id'] for n in content_nodes}

    for edge in edges:
        if edge.get('fromSide') == 'bottom' and edge.get('toSide') == 'top':
            p, c = edge['fromNode'], edge['toNode']
            if p in content_ids and c in content_ids:
                children_of[p].append(c)
                all_children.add(c)

    # 找根
    roots = [nid for nid in content_ids if nid not in all_children]

    # 按层级分组 (BFS)
    levels: list[list[str]] = []
    visited: set[str] = set()
    current_level = roots[:]

    while current_level:
        level_nodes = []
        next_level = []
        for nid in current_level:
            if nid in visited:
                continue
            visited.add(nid)
            level_nodes.append(nid)
            next_level.extend(children_of.get(nid, []))
        if level_nodes:
            levels.append(level_nodes)
        current_level = next_level

    # 对每层同层节点顶部对齐
    for level_nids in levels:
        if len(level_nids) <= 1:
            continue
        nodes_in_level = [node_map[nid] for nid in level_nids if nid in node_map]
        if not nodes_in_level:
            continue
        # 使用中位数 y 作为参考（避免极端值拉偏）
        ys = sorted(n['y'] for n in nodes_in_level)
        target_y = ys[len(ys) // 2]
        target_y = snap_pos(target_y)
        for node in nodes_in_level:
            node['y'] = target_y

    # 对每个父节点，将其子节点组居中
    for parent_id, child_ids in children_of.items():
        if parent_id not in node_map or len(child_ids) < 2:
            continue
        parent = node_map[parent_id]
        parent_cx = parent['x'] + parent['width'] / 2

        children = [node_map[cid] for cid in child_ids if cid in node_map]
        if not children:
            continue

        # 按当前 x 排序
        children.sort(key=lambda n: n['x'])

        # 计算总宽度（含间距）
        total_w = sum(c['width'] for c in children) + CHILD_GAP * (len(children) - 1)

        # 从 parent_cx 居中分配
        start_x = parent_cx - total_w / 2
        for child in children:
            child['x'] = snap_pos(start_x)
            start_x += child['width'] + CHILD_GAP


def align_mindmap(content_nodes: list[dict], edges: list[dict],
                  node_map: dict[str, dict]) -> None:
    """
    思维导图布局：
    - 右侧分支：左对齐（共享 x）
    - 左侧分支：右对齐（共享 x + width）
    """
    # 找中心节点（被最多 edge 引用的 fromNode）
    from_counts: dict[str, int] = defaultdict(int)
    content_ids = {n['id'] for n in content_nodes}
    for edge in edges:
        fn = edge.get('fromNode', '')
        if fn in content_ids:
            from_counts[fn] += 1

    if not from_counts:
        return

    center_id = max(from_counts, key=from_counts.get)
    center = node_map.get(center_id)
    if not center:
        return

    center_cx = center['x'] + center['width'] / 2

    # 分组：右侧分支和左侧分支
    right_branches: list[str] = []
    left_branches: list[str] = []

    for edge in edges:
        fn = edge.get('fromNode', '')
        tn = edge.get('toNode', '')
        fs = edge.get('fromSide', '')

        if fn == center_id and tn in content_ids:
            target = node_map.get(tn)
            if target:
                target_cx = target['x'] + target['width'] / 2
                if target_cx > center_cx or fs == 'right':
                    right_branches.append(tn)
                else:
                    left_branches.append(tn)

    # 递归收集子节点
    def collect_descendants(parent_id: str, side: str) -> list[str]:
        result = []
        for edge in edges:
            if edge.get('fromNode') == parent_id:
                child = edge.get('toNode', '')
                if child in content_ids and child != center_id:
                    result.append(child)
                    result.extend(collect_descendants(child, side))
        return result

    all_right = set(right_branches)
    for nid in list(right_branches):
        all_right.update(collect_descendants(nid, 'right'))

    all_left = set(left_branches)
    for nid in list(left_branches):
        all_left.update(collect_descendants(nid, 'left'))

    # 按层级分组
    def group_by_depth(node_ids: set[str]) -> dict[int, list[str]]:
        by_x: dict[int, list[str]] = defaultdict(list)
        for nid in node_ids:
            n = node_map.get(nid)
            if n:
                # 按 x 位置粗分层（每 300px 为一层）
                layer = round(abs(n['x'] - center['x']) / 300)
                by_x[layer].append(nid)
        return by_x

    # 右侧分支：同层左对齐
    right_layers = group_by_depth(all_right)
    for layer_nodes in right_layers.values():
        if len(layer_nodes) <= 1:
            continue
        # 左对齐：共享 x
        target_x = min(node_map[nid]['x'] for nid in layer_nodes if nid in node_map)
        target_x = snap_pos(target_x)
        for nid in layer_nodes:
            if nid in node_map:
                node_map[nid]['x'] = target_x

    # 左侧分支：同层右对齐
    left_layers = group_by_depth(all_left)
    for layer_nodes in left_layers.values():
        if len(layer_nodes) <= 1:
            continue
        # 右对齐：共享 x + width
        target_right = max(
            node_map[nid]['x'] + node_map[nid]['width']
            for nid in layer_nodes if nid in node_map
        )
        target_right = snap_pos(target_right)
        for nid in layer_nodes:
            if nid in node_map:
                node_map[nid]['x'] = snap_pos(target_right - node_map[nid]['width'])


def align_flowchart(content_nodes: list[dict], edges: list[dict],
                     node_map: dict[str, dict]) -> None:
    """
    流程图布局：主流程（垂直）+ 侧边分支（水平）。

    算法：
    1. 建立邻接表，区分主列节点（bottom→top 链）和分支节点（left/right fromSide）
    2. 主列节点按拓扑排序分层，y 按 max(父节点底部) + GAP
    3. 主列 x 居中（以最宽节点中心为基准）
    4. 分支节点按 fromSide 水平排列在主列两侧（left → 左侧，right → 右侧）
    5. 检测并解决分支节点与主列的水平碰撞
    """
    content_ids = {n['id'] for n in content_nodes}

    # 建立邻接表
    children_of: dict[str, list[str]] = defaultdict(list)
    parents_of: dict[str, list[str]] = defaultdict(list)
    edge_info: dict[tuple[str, str], tuple[str, str]] = {}  # (from, to) -> (fromSide, toSide)
    edge_sides: dict[tuple[str, str], str] = {}  # (from, to) -> fromSide

    for edge in edges:
        fn = edge.get('fromNode', '')
        tn = edge.get('toNode', '')
        if fn not in content_ids or tn not in content_ids:
            continue
        fs = edge.get('fromSide', '')
        ts = edge.get('toSide', '')
        children_of[fn].append(tn)
        parents_of[tn].append(fn)
        edge_info[(fn, tn)] = (fs, ts)
        edge_sides[(fn, tn)] = fs

    # 分类节点：主列（bottom→top）vs 分支（left/right）
    # 根节点（无父节点）属于主列
    roots = [n['id'] for n in content_nodes if not parents_of.get(n['id'])]
    if not roots:
        roots = [min(content_ids, key=lambda nid: node_map[nid]['y'] + node_map[nid]['height'] / 2)]

    # BFS 确定主列：沿 bottom→top 边前进的节点
    main_col: set[str] = set(roots)
    frontier = list(roots)
    visited_main = set(roots)

    while frontier:
        next_frontier = []
        for parent in frontier:
            for child in children_of.get(parent, []):
                if child in visited_main:
                    continue
                # 只跟随 bottom→top 边加入主列
                side = edge_sides.get((parent, child), '')
                if side == 'bottom':
                    main_col.add(child)
                    visited_main.add(child)
                    next_frontier.append(child)
        frontier = next_frontier

    # 其余节点（left/right fromSide 的子节点）为分支
    branch_ids: set[str] = content_ids - main_col

    # Phase 1: 确定 y 坐标（全局拓扑分层）
    # 计算最长路径深度
    def max_depth(nid: str, visited: set[str]) -> int:
        if nid in visited:
            return 0
        parents = parents_of.get(nid, [])
        if not parents:
            return 0
        return 1 + max(max_depth(p, visited | {nid}) for p in parents)

    depth_map: dict[str, int] = {}
    for nid in content_ids:
        depth_map[nid] = max_depth(nid, set())

    max_depth_val = max(depth_map.values()) if depth_map else 0

    # 按深度分层，每层 y 相同
    depth_groups: dict[int, list[str]] = defaultdict(list)
    for nid, d in depth_map.items():
        depth_groups[d].append(nid)

    # 确定主列基准 x（以最宽的根节点中心为准）
    root_widest = max(roots, key=lambda nid: node_map[nid]['width'])
    base_cx = node_map[root_widest]['x'] + node_map[root_widest]['width'] / 2

    # 计算主列的 x 范围
    main_col_xs = {}
    for nid in main_col:
        n = node_map[nid]
        nx = snap_pos(base_cx - n['width'] / 2)
        n['x'] = nx
        main_col_xs[nid] = (nx, nx + n['width'])

    # 分支节点 x：left 分支放在主列左侧，right 分支放在主列右侧
    # 收集每个深度的分支节点，按 fromSide 分组
    for depth, nids in depth_groups.items():
        branch_left: list[tuple[str, str]] = []  # [(node_id, fromSide)]
        branch_right: list[tuple[str, str]] = []

        for nid in nids:
            if nid in main_col:
                continue
            # 确定这个节点是 left 还是 right 分支
            # 查找它的 fromSide（从哪个父节点的哪侧来）
            from_sides = set()
            for parent in parents_of.get(nid, []):
                side = edge_sides.get((parent, nid), '')
                if side in ('left', 'right'):
                    from_sides.add(side)

            if 'left' in from_sides:
                branch_left.append((nid, 'left'))
            elif 'right' in from_sides:
                branch_right.append((nid, 'right'))
            else:
                # 没有明确的 left/right 方向，默认放在右侧
                branch_right.append((nid, 'right'))

        # 计算 y 坐标：与同深度主列节点对齐（共用 y）
        if nids:
            target_y = min(node_map[nid]['y'] for nid in nids if nid in node_map)
            target_y = snap_pos(target_y)
            for nid in nids:
                if nid in node_map and nid not in main_col:
                    node_map[nid]['y'] = target_y

        # 左侧分支：水平排列，最左边缘对齐
        if branch_left:
            branch_left.sort(key=lambda x: node_map[x[0]]['x'])
            total_w = sum(node_map[nid]['width'] + HORIZONTAL_SPACING
                          for nid, _ in branch_left) - HORIZONTAL_SPACING
            total_w = max(total_w, 0)
            # 以主列左边缘为基准，向左排列
            if main_col_xs:
                main_left = min(l for l, r in main_col_xs.values())
            else:
                main_left = base_cx - 200
            start_x = snap_pos(main_left - total_w)
            for nid, side in branch_left:
                node_map[nid]['x'] = start_x
                start_x += node_map[nid]['width'] + HORIZONTAL_SPACING

                # 检测与主列的水平碰撞
                if main_col_xs:
                    child = node_map[nid]
                    child_right = start_x  # after placement
                    child_left = start_x - node_map[nid]['width']
                    for main_id, (main_l, main_r) in main_col_xs.items():
                        main_n = node_map[main_id]
                        # 垂直方向有交集
                        if not (child['y'] + child['height'] <= main_n['y']
                                or child['y'] >= main_n['y'] + main_n['height']):
                            # x 方向有重叠
                            if not (child_right <= main_l or child_left >= main_r):
                                # 移向左
                                new_left = snap_pos(main_l - MIN_GAP - node_map[nid]['width'])
                                if node_map[nid]['x'] > new_left:
                                    node_map[nid]['x'] = new_left

        # 右侧分支：水平排列
        if branch_right:
            branch_right.sort(key=lambda x: node_map[x[0]]['x'])
            total_w = sum(node_map[nid]['width'] + HORIZONTAL_SPACING
                          for nid, _ in branch_right) - HORIZONTAL_SPACING
            total_w = max(total_w, 0)
            # 以主列右边缘为基准，向右排列
            if main_col_xs:
                main_right = max(r for l, r in main_col_xs.values())
            else:
                main_right = base_cx + 200
            start_x = snap_pos(main_right + MIN_GAP)
            for nid, side in branch_right:
                node_map[nid]['x'] = start_x
                start_x += node_map[nid]['width'] + HORIZONTAL_SPACING


def align_grid(content_nodes: list[dict], group_nodes: list[dict],
               node_map: dict[str, dict]) -> None:
    """
    网格/看板布局：
    - 列内：左对齐
    - 跨列同行：顶部对齐
    """
    if not group_nodes:
        # 无 group 节点，按 y-band 分行，center-align y
        rows = group_by_y_band(content_nodes)
        for row in rows:
            if len(row) <= 1:
                continue
            row_ids = [n['id'] for n in row]
            align_row_center_y(row_ids, node_map)
        return

    # 有 group 节点：按 group 分列
    for group in group_nodes:
        gx = group['x']
        gy = group['y']
        gw = group['width']
        gh = group['height']

        # 找 group 内的 content 节点
        inside = []
        for node in content_nodes:
            nx, ny = node['x'], node['y']
            if gx <= nx <= gx + gw and gy <= ny <= gy + gh:
                inside.append(node)

        if len(inside) <= 1:
            continue

        # 列内左对齐：所有节点共享 x
        target_x = min(n['x'] for n in inside)
        target_x = snap_pos(target_x)
        for node in inside:
            node['x'] = target_x


def align_horizontal_flow(content_nodes: list[dict], edges: list[dict],
                          node_map: dict[str, dict]) -> None:
    """水平流：同行节点中心对齐 y。"""
    rows = detect_rows(content_nodes, edges)
    for row_ids in rows:
        if len(row_ids) <= 1:
            continue
        align_row_center_y(row_ids, node_map)


# ---------------------------------------------------------------------------
# 装饰箭头重定位
# ---------------------------------------------------------------------------

def reposition_arrows(arrow_nodes: list[dict], content_nodes: list[dict],
                      node_map: dict[str, dict]) -> None:
    """
    将装饰箭头节点重新定位到相邻内容节点之间的中心位置。
    """
    if not arrow_nodes or not content_nodes:
        return

    # 按 y 排序的内容节点
    sorted_content = sorted(content_nodes, key=lambda n: n['y'])

    for arrow in arrow_nodes:
        arrow_cy = arrow['y'] + arrow['height'] / 2

        # 找最近的上方和下方内容节点
        above = None
        below = None

        for n in sorted_content:
            n_bottom = n['y'] + n['height']
            n_top = n['y']

            if n_bottom <= arrow_cy:
                if above is None or n_bottom > (above['y'] + above['height']):
                    above = n
            elif n_top >= arrow_cy:
                if below is None or n_top < below['y']:
                    below = n

        if above and below:
            # x：居中于上下节点的平均 center_x
            above_cx = above['x'] + above['width'] / 2
            below_cx = below['x'] + below['width'] / 2
            avg_cx = (above_cx + below_cx) / 2
            arrow['x'] = snap_pos(avg_cx - arrow['width'] / 2)

            # y：居中于上节点底部和下节点顶部之间
            gap_center = (above['y'] + above['height'] + below['y']) / 2
            arrow['y'] = snap_pos(gap_center - arrow['height'] / 2)
        elif above:
            # 只有上方节点：放在其下方
            above_cx = above['x'] + above['width'] / 2
            arrow['x'] = snap_pos(above_cx - arrow['width'] / 2)
        elif below:
            # 只有下方节点：放在其上方
            below_cx = below['x'] + below['width'] / 2
            arrow['x'] = snap_pos(below_cx - arrow['width'] / 2)


# ---------------------------------------------------------------------------
# 碰撞检测与解决
# ---------------------------------------------------------------------------

def rects_overlap(a: dict, b: dict, gap: int = MIN_GAP) -> bool:
    """检查两个节点矩形是否重叠（含间隙）。"""
    return not (
        a['x'] + a['width'] + gap <= b['x'] or
        b['x'] + b['width'] + gap <= a['x'] or
        a['y'] + a['height'] + gap <= b['y'] or
        b['y'] + b['height'] + gap <= a['y']
    )


def detect_collisions(nodes: list[dict]) -> list[tuple[str, str]]:
    """检测所有碰撞的节点对（排除 group 和 decorative arrow 节点）。"""
    collisions = []
    # 只检测 content 节点之间的碰撞
    check_nodes = [n for n in nodes
                   if n.get('type') != 'group'
                   and not (n.get('type') == 'text' and is_decorative_arrow(n.get('text', '')))]
    for i, a in enumerate(check_nodes):
        for b in check_nodes[i + 1:]:
            if rects_overlap(a, b):
                collisions.append((a['id'], b['id']))
    return collisions


def resolve_collisions(nodes: list[dict], node_map: dict[str, dict]) -> int:
    """
    解决碰撞：将重叠的节点向下偏移。
    返回解决的碰撞数。
    """
    # 只处理 content 节点（排除 group 和 arrow）
    content = [n for n in nodes
               if n.get('type') != 'group'
               and not (n.get('type') == 'text' and is_decorative_arrow(n.get('text', '')))]
    resolved = 0
    max_iterations = 20

    for _ in range(max_iterations):
        collisions = detect_collisions(content)
        if not collisions:
            break

        for aid, bid in collisions:
            a = node_map.get(aid)
            b = node_map.get(bid)
            if not a or not b:
                continue

            # 将 y 更大的节点向下偏移
            if a['y'] <= b['y']:
                upper, lower = a, b
            else:
                upper, lower = b, a

            overlap_y = (upper['y'] + upper['height'] + MIN_GAP) - lower['y']
            if overlap_y > 0:
                lower['y'] = snap_pos(lower['y'] + overlap_y)
                resolved += 1

    return resolved


# ---------------------------------------------------------------------------
# 主处理流程
# ---------------------------------------------------------------------------

def fix_node_sizes(nodes: list[dict]) -> int:
    """修复所有 text 节点的尺寸。返回修复数量。"""
    fixed = 0
    for node in nodes:
        if node.get('type') != 'text' or 'text' not in node:
            continue
        if is_decorative_arrow(node['text']):
            continue

        ideal_w, ideal_h = calc_node_size(node['text'])
        changed = False
        if node['width'] < ideal_w:
            node['width'] = ideal_w
            changed = True
        if node['height'] < ideal_h:
            node['height'] = ideal_h
            changed = True
        if changed:
            fixed += 1
    return fixed


def process_canvas(path: str | Path,
                   layout_override: str | None = None,
                   fix_sizes: bool = False,
                   remove_arrows: bool = True) -> dict:
    """
    处理 canvas 文件：检测布局、应用对齐。

    参数:
        path: canvas 文件路径
        layout_override: 强制指定布局类型
        fix_sizes: 是否修复节点尺寸
        remove_arrows: 是否移除装饰性箭头节点（默认 True）

    返回:
        {
            'data': canvas JSON 数据,
            'layout': 检测到的布局类型,
            'sizes_fixed': 修复的尺寸数,
            'arrows_removed': 移除的箭头数,
            'alignment_applied': bool,
        }
    """
    path = Path(path)
    with open(path, encoding='utf-8') as f:
        data = json.load(f)

    nodes = data.get('nodes', [])
    edges = data.get('edges', [])
    node_map = {n['id']: n for n in nodes}

    result = {
        'data': data,
        'layout': 'unknown',
        'sizes_fixed': 0,
        'arrows_removed': 0,
        'alignment_applied': False,
    }

    # Step 1: 可选修复尺寸
    if fix_sizes:
        result['sizes_fixed'] = fix_node_sizes(nodes)

    # Step 2: 分离节点类型
    groups, arrows, content = separate_nodes(nodes)

    # Step 3: 移除装饰箭头节点（已有 edge 连线，箭头文本节点冗余）
    if remove_arrows and arrows:
        result['arrows_removed'] = len(arrows)
        arrow_ids = {a['id'] for a in arrows}
        data['nodes'] = [n for n in nodes if n['id'] not in arrow_ids]
        # 也移除引用箭头节点的 edge
        data['edges'] = [e for e in edges if
                         e.get('fromNode') not in arrow_ids and
                         e.get('toNode') not in arrow_ids]
        nodes = data['nodes']
        edges = data['edges']
        node_map = {n['id']: n for n in nodes}
        # 重新分离
        groups, arrows, content = separate_nodes(nodes)

    if not content:
        return result

    # Step 4: 检测布局
    layout = layout_override or detect_layout(content, edges, nodes)
    if layout == 'unknown' and groups:
        layout = 'grid'
    result['layout'] = layout

    # Step 5: 按布局类型对齐
    if layout == 'vertical_flow':
        layout_vertical_flow(content, edges, node_map)
        result['alignment_applied'] = True

    elif layout == 'horizontal_flow':
        align_horizontal_flow(content, edges, node_map)
        result['alignment_applied'] = True

    elif layout == 'tree':
        align_tree(content, edges, node_map)
        result['alignment_applied'] = True

    elif layout == 'mindmap':
        align_mindmap(content, edges, node_map)
        result['alignment_applied'] = True

    elif layout == 'grid':
        align_grid(content, groups, node_map)
        result['alignment_applied'] = True

    elif layout == 'flowchart':
        align_flowchart(content, edges, node_map)
        result['alignment_applied'] = True

    # Step 5b: 碰撞检测与解决
    collisions = detect_collisions(nodes)
    if collisions:
        resolved = resolve_collisions(nodes, node_map)
        if resolved > 0:
            result['collisions_resolved'] = resolved

    # Step 6: snap 所有坐标到网格
    for node in nodes:
        node['x'] = snap_pos(node['x'])
        node['y'] = snap_pos(node['y'])

    return result


def save_canvas(data: dict, path: str | Path) -> None:
    """保存 canvas 数据到文件。"""
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent='\t')


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description='JSON Canvas 布局对齐工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例:
  python canvas_layout.py input.canvas                       # 检测 + 报告
  python canvas_layout.py input.canvas --fix                 # 修复对齐
  python canvas_layout.py input.canvas --fix --fix-sizes     # 修复尺寸 + 对齐
  python canvas_layout.py input.canvas --layout tree --fix   # 指定布局类型
  python canvas_layout.py input.canvas --fix -o output.canvas
        ''',
    )
    parser.add_argument('canvas', help='Canvas 文件路径')
    parser.add_argument('--fix', action='store_true', help='修复对齐（写入文件）')
    parser.add_argument('--fix-sizes', action='store_true', help='同时修复节点尺寸')
    parser.add_argument('--layout', choices=[
        'vertical_flow', 'horizontal_flow', 'tree', 'mindmap', 'grid', 'flowchart'
    ], help='强制指定布局类型（默认自动检测）')
    parser.add_argument('-o', '--output', type=str, help='输出文件路径（默认原地修改）')
    args = parser.parse_args()

    path = Path(args.canvas)
    if not path.exists():
        print(f"  错误: 文件不存在: {path}")
        sys.exit(1)

    print(f"\n  文件: {path}\n")

    result = process_canvas(
        path,
        layout_override=args.layout,
        fix_sizes=args.fix_sizes,
    )

    layout = result['layout']
    sizes_fixed = result['sizes_fixed']
    arrows_removed = result['arrows_removed']
    aligned = result['alignment_applied']

    # 输出报告
    layout_names = {
        'vertical_flow': '垂直流（Vertical Flow）',
        'flowchart': '流程图（Flowchart）',
        'horizontal_flow': '水平流（Horizontal Flow）',
        'tree': '树形（Tree）',
        'mindmap': '思维导图（MindMap）',
        'grid': '网格（Grid）',
        'unknown': '未知',
    }
    print(f"  布局类型: {layout_names.get(layout, layout)}")

    alignment_desc = {
        'vertical_flow': '同列节点中心对齐 x',
        'flowchart': '主列居中，分支节点水平展开到两侧',
        'horizontal_flow': '同行节点中心对齐 y',
        'tree': '子节点组居中于父节点，同层顶部对齐',
        'mindmap': '右分支左对齐，左分支右对齐',
        'grid': '列内左对齐，跨列顶部对齐',
        'unknown': '无对齐（未识别布局）',
    }
    print(f"  对齐策略: {alignment_desc.get(layout, '-')}")

    if sizes_fixed:
        print(f"  尺寸修复: {sizes_fixed} 个节点")
    if arrows_removed:
        print(f"  箭头移除: {arrows_removed} 个装饰箭头节点")
    if aligned:
        print(f"  对齐状态: ✓ 已对齐")
    else:
        print(f"  对齐状态: - 未应用")

    # 碰撞报告（使用同一文件的数据）
    all_nodes = result['data'].get('nodes', [])
    cmap = {n['id']: n for n in all_nodes}
    cols = detect_collisions(all_nodes)
    if cols:
        resolved = resolve_collisions(all_nodes, cmap)
        print(f"  碰撞: {len(cols)} 个 → 解决 {resolved} 个")
        for a, b in cols[:3]:
            print(f"    {a} ↔ {b}")
    else:
        print(f"  碰撞: 0 个 ✓")

    # 保存
    if args.fix:
        out_path = Path(args.output) if args.output else path
        save_canvas(result['data'], out_path)
        print(f"\n  → 已保存到 {out_path}")
    else:
        print(f"\n  提示: 使用 --fix 写入修复结果")

    print()


if __name__ == '__main__':
    main()
