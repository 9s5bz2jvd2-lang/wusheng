#!/usr/bin/env python3
"""
万物生 · 推演路径树生成器
Derivation path from input to final theory
"""

import json
import argparse
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# 中文字体支持
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK JP', 'Noto Serif CJK JP', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# ===== 颜色方案 =====
VERDICT_COLORS = {
    '成型': '#27AE60',
    '可修': '#F1C40F',
    '失败': '#E74C3C',
}

ROUND_COLORS = {
    1: '#3498DB',
    2: '#9B59B6',
    3: '#E67E22',
}

STRATEGY_COLORS = {
    '结构对撞': '#8E44AD',
    '假设对撞': '#2980B9',
    '边界缝合': '#16A085',
    '逆向复制': '#D35400',
    '尺度跳跃': '#C0392B',
    '缺失注入': '#27AE60',
}

CONFIDENCE_COLORS = {
    '实推': '#27AE60',
    '类比': '#F1C40F',
    '猜想': '#E74C3C',
}


def load_data(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def truncate(text, max_len=25):
    if len(text) > max_len:
        return text[:max_len - 2] + '...'
    return text


def draw_trajectory(data, output_path):
    """
    手动绘制树形结构，不依赖 graphviz
    """
    fig, ax = plt.subplots(1, 1, figsize=(20, 12))
    fig.patch.set_facecolor('#FAFAFA')
    ax.set_facecolor('#FAFAFA')

    # 收集树形数据
    # Level 0: 输入
    # Level 1: 第1轮各学科
    # Level 2: 第1轮碰撞产物 → 第2轮学科
    # Level 3: 第2轮产物 → 第3轮学科
    # Level 4: 最终理论

    input_summary = data.get('input', {}).get('summary', '输入')

    # 构建树
    tree = {
        'label': truncate(input_summary, 30),
        'color': '#2C3E50',
        'level': 0,
        'children': []
    }

    for round_data in data.get('rounds', []):
        round_idx = round_data['round']
        for daemon in round_data.get('daemons', []):
            discipline = daemon.get('discipline', '未知')
            strategy = daemon.get('strategy', '结构对撞')
            strat_color = STRATEGY_COLORS.get(strategy, '#95A5A6')

            # 学科节点
            disc_node = {
                'label': f'R{round_idx}:{discipline}\n[{strategy}]',
                'color': ROUND_COLORS.get(round_idx, '#95A5A6'),
                'level': round_idx,
                'edge_color': strat_color,
                'edge_label': strategy,
                'children': []
            }

            # 碰撞产物
            for prod in daemon.get('collision_products', []):
                idea = prod.get('idea', '新想法')
                conf = prod.get('confidence', '类比')
                val = prod.get('value', '中')
                prod_type = prod.get('type', '裂缝')
                conf_color = CONFIDENCE_COLORS.get(conf, '#95A5A6')

                prod_node = {
                    'label': truncate(f'{idea}', 20),
                    'color': conf_color,
                    'level': round_idx + 0.5,
                    'edge_color': conf_color,
                    'edge_label': f'{prod_type}({conf})',
                    'children': []
                }
                disc_node['children'].append(prod_node)

            tree['children'].append(disc_node)

    # 最终理论
    final = data.get('final_output', {})
    theory = final.get('theory', '')
    if theory:
        tree['children'].append({
            'label': f'★ {truncate(theory, 35)}',
            'color': '#E67E22',
            'level': 3.5,
            'edge_color': '#E67E22',
            'edge_label': '成型理论',
            'children': []
        })

    # 手动布局
    def count_leaves(node):
        if not node.get('children'):
            return 1
        return sum(count_leaves(c) for c in node['children'])

    total_leaves = max(count_leaves(tree), 1)
    x_unit = 1.0 / total_leaves

    positions = {}  # node_id -> (x, y)
    node_id = [0]

    def assign_positions(node, x_start, x_end, y_level):
        nid = node_id[0]
        node_id[0] += 1

        if not node.get('children'):
            x = (x_start + x_end) / 2
            positions[nid] = (x, -y_level, node)
            return nid, x

        # 递归分配子节点
        child_leaves = [count_leaves(c) for c in node['children']]
        total = sum(child_leaves)

        child_ids = []
        cx = x_start
        for i, child in enumerate(node['children']):
            cx_end = cx + (x_end - x_start) * child_leaves[i] / total
            cid, child_x = assign_positions(child, cx, cx_end, y_level + 1)
            child_ids.append((cid, child, child_x))
            cx = cx_end

        # 父节点在子节点中心
        x = sum(cx for _, _, cx in child_ids) / len(child_ids)
        positions[nid] = (x, -y_level, node)

        return nid, x

    root_id, _ = assign_positions(tree, 0.05, 0.95, 0)

    # 重新遍历建立边
    edges = []
    node_id2 = [0]

    def collect_edges(node, parent_nid):
        nid = node_id2[0]
        node_id2[0] += 1

        for child in node.get('children', []):
            child_nid = node_id2[0]
            collect_edges(child, nid)

        if parent_nid is not None:
            edges.append((parent_nid, nid, node.get('edge_color', '#BDC3C7'),
                         node.get('edge_label', '')))

    node_id2[0] = 0
    collect_edges(tree, None)

    # 绘制
    for nid, (x, y, node) in positions.items():
        label = node.get('label', '')
        color = node.get('color', '#95A5A6')
        level = node.get('level', 0)

        # 节点大小根据层级
        if level == 0:
            box_size = dict(boxstyle='round,pad=0.5', facecolor=color, alpha=0.9)
            fontsize = 12
            text_color = 'white'
        elif level <= 3:
            box_size = dict(boxstyle='round,pad=0.3', facecolor=color, alpha=0.15,
                          edgecolor=color, linewidth=2)
            fontsize = 9
            text_color = color
        else:
            box_size = dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8,
                          edgecolor=color, linewidth=1.5)
            fontsize = 7.5
            text_color = '#555555'

        ax.text(x, y, label, fontsize=fontsize, ha='center', va='center',
               color=text_color, fontweight='bold', bbox=box_size)

    # 绘制边
    id_list = [0]
    def remap_ids(node):
        nid = id_list[0]
        id_list[0] += 1
        result = {nid: node}
        for child in node.get('children', []):
            result.update(remap_ids(child))
        return result

    id_list = [0]
    node_map = remap_ids(tree)

    # 简化：直接用positions画边
    # 用另一种方式：按positions的顺序重新建边
    # 由于node_id和node_id2的遍历顺序一致，可以直接用
    id_list2 = [0]
    edge_data = []

    def collect_edges2(node, parent_key):
        nid = id_list2[0]
        id_list2[0] += 1

        if parent_key is not None:
            edge_data.append((parent_key, nid, node.get('edge_color', '#BDC3C7'),
                            node.get('edge_label', '')))

        for child in node.get('children', []):
            collect_edges2(child, nid)

    id_list2 = [0]
    collect_edges2(tree, None)

    for parent_nid, child_nid, edge_color, edge_label in edge_data:
        if parent_nid in positions and child_nid in positions:
            px, py, _ = positions[parent_nid]
            cx, cy, _ = positions[child_nid]

            # 画线
            ax.annotate('', xy=(cx, cy), xytext=(px, py),
                       arrowprops=dict(arrowstyle='->', color=edge_color,
                                      lw=1.5, connectionstyle='arc3,rad=0.1'))

            # 边标签
            if edge_label:
                mid_x = (px + cx) / 2
                mid_y = (py + cy) / 2
                ax.text(mid_x, mid_y + 0.15, edge_label, fontsize=6.5,
                       ha='center', va='bottom', color=edge_color,
                       bbox=dict(boxstyle='round,pad=0.1', facecolor='white',
                                alpha=0.8, edgecolor=edge_color, linewidth=0.5))

    # 图例
    legend_elements = []
    for r, color in ROUND_COLORS.items():
        names = {1: '第1轮·天地开辟', 2: '第2轮·万物萌生', 3: '第3轮·三角定圆'}
        legend_elements.append(mpatches.Patch(color=color, label=names[r]))
    for conf, color in CONFIDENCE_COLORS.items():
        legend_elements.append(mpatches.Patch(color=color, label=f'置信: {conf}'))
    for strat, color in STRATEGY_COLORS.items():
        legend_elements.append(mpatches.Patch(color=color, label=strat))

    ax.legend(handles=legend_elements, loc='lower left', fontsize=8,
             framealpha=0.9, edgecolor='#BDC3C7', ncol=2)

    ax.set_xlim(-0.05, 1.05)
    y_vals = [y for _, (_, y, _) in positions.items()]
    if y_vals:
        ax.set_ylim(min(y_vals) - 0.5, max(y_vals) + 0.5)
    ax.axis('off')
    ax.set_title('万物生 · 推演路径树\n来龙去脉，步步可溯', fontsize=16,
                fontweight='bold', color='#2C3E50', pad=20)

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight',
               facecolor=fig.get_facecolor())
    plt.close()
    print(f'✅ 推演路径树已生成: {output_path}')


def main():
    parser = argparse.ArgumentParser(description='万物生·推演路径树生成器')
    parser.add_argument('--input', required=True, help='碰撞JSON数据文件路径')
    parser.add_argument('--output', default='wusheng_trajectory.png', help='输出图片路径')
    args = parser.parse_args()

    data = load_data(args.input)
    draw_trajectory(data, args.output)


if __name__ == '__main__':
    main()
