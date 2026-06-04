#!/usr/bin/env python3
"""
万物生 · 网状图生成器
Discipline nodes + collision edges + product annotations
"""

import json
import argparse
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
import numpy as np

# 中文字体支持：优先注册可用 CJK 字体，避免导出 PNG 时中文变方框
from matplotlib import font_manager
_CJK_FONT_PATHS = [
    '/System/Library/Fonts/PingFang.ttc',
    '/System/Library/Fonts/Hiragino Sans GB.ttc',
    '/System/Library/Fonts/STHeiti Medium.ttc',
    '/System/Library/Fonts/STHeiti Light.ttc',
    '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',
    '/Library/Fonts/Arial Unicode.ttf',
    '/System/Library/Fonts/Supplemental/Songti.ttc',
]
for _font_path in _CJK_FONT_PATHS:
    if Path(_font_path).exists():
        try:
            font_manager.fontManager.addfont(_font_path)
        except Exception:
            pass
plt.rcParams['font.sans-serif'] = [
    'PingFang HK', 'PingFang SC', 'Hiragino Sans GB', 'Hiragino Sans',
    'Arial Unicode MS', 'Heiti TC', 'Songti SC',
    'Noto Sans CJK SC', 'Noto Sans CJK JP', 'Noto Serif CJK JP',
    'Microsoft YaHei', 'SimHei', 'WenQuanYi Zen Hei', 'DejaVu Sans'
]
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['axes.unicode_minus'] = False

# ===== 颜色方案 =====
DISCIPLINE_COLORS = {
    '自然科学': '#3498DB',
    '社会科学': '#E74C3C',
    '人文学科': '#9B59B6',
    '艺术': '#F39C12',
    '工程': '#1ABC9C',
    '东方智慧': '#E67E22',
}

CONFIDENCE_COLORS = {
    '实推': '#27AE60',
    '类比': '#F1C40F',
    '猜想': '#E74C3C',
}

STRATEGY_COLORS = {
    '结构对撞': '#8E44AD',
    '假设对撞': '#2980B9',
    '边界缝合': '#16A085',
    '逆向复制': '#D35400',
    '尺度跳跃': '#C0392B',
    '缺失注入': '#27AE60',
}

DISCIPLINE_CATEGORY = {
    '物理学': '自然科学', '生物学': '自然科学', '化学': '自然科学',
    '天文学': '自然科学', '地质学': '自然科学',
    '经济学': '社会科学', '心理学': '社会科学', '社会学': '社会科学',
    '人类学': '社会科学', '语言学': '社会科学',
    '历史学': '人文学科', '文学': '人文学科', '哲学': '人文学科',
    '宗教学': '人文学科', '美学': '人文学科',
    '音乐': '艺术', '绘画': '艺术', '建筑': '艺术',
    '舞蹈': '艺术', '电影': '艺术',
    '计算机科学': '工程', '控制论': '工程', '系统工程': '工程',
    '材料科学': '工程', '信息论': '工程',
    '道家': '东方智慧', '佛学': '东方智慧', '中医': '东方智慧',
    '易经': '东方智慧', '兵法': '东方智慧',
}


def get_discipline_color(discipline):
    cat = DISCIPLINE_CATEGORY.get(discipline, '自然科学')
    return DISCIPLINE_COLORS.get(cat, '#95A5A6')


def get_category(discipline):
    return DISCIPLINE_CATEGORY.get(discipline, '其他')


def load_data(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def draw_network(data, output_path):
    G = nx.Graph()

    # 中心输入节点
    input_summary = data.get('input', {}).get('summary', '输入')
    if len(input_summary) > 15:
        input_summary = input_summary[:13] + '...'
    input_node = f'INPUT: {input_summary}'
    G.add_node(input_node, node_type='input', size=2000)

    # 遍历轮次，添加学科节点和产物节点
    product_nodes = []
    for round_data in data.get('rounds', []):
        round_idx = round_data['round']
        for daemon in round_data.get('daemons', []):
            discipline = daemon.get('discipline', '未知')
            strategy = daemon.get('strategy', '结构对撞')
            daemon_id = daemon.get('daemon_id', f'D{round_idx}')

            # 学科节点
            disc_node = f'R{round_idx}:{discipline}'
            if disc_node not in G:
                G.add_node(disc_node, node_type='discipline',
                          discipline=discipline, round=round_idx, size=800)
                # 连接到输入
                G.add_edge(input_node, disc_node, edge_type='connect',
                          color='#BDC3C7', width=1.5, style='solid')

            # 碰撞产物
            for k, prod in enumerate(daemon.get('collision_products', [])):
                idea = prod.get('idea', '新想法')
                if len(idea) > 20:
                    idea = idea[:18] + '...'
                conf = prod.get('confidence', '类比')
                val = prod.get('value', '中')
                prod_type = prod.get('type', '裂缝')
                strat_color = STRATEGY_COLORS.get(strategy, '#95A5A6')

                prod_node = f'P_{daemon_id}_{k}'
                G.add_node(prod_node, node_type='product', idea=idea,
                          confidence=conf, value=val, prod_type=prod_type,
                          size=400)
                product_nodes.append(prod_node)

                # 学科→产物连线
                G.add_edge(disc_node, prod_node, edge_type='collision',
                          color=strat_color, width=2, style='dashed',
                          strategy=strategy)

    # 跨轮次连线：如果第2轮的学科追踪第1轮的种子
    round_disciplines = {}
    for node in G.nodes():
        if G.nodes[node].get('node_type') == 'discipline':
            r = G.nodes[node].get('round', 0)
            if r not in round_disciplines:
                round_disciplines[r] = []
            round_disciplines[r].append(node)

    for r in sorted(round_disciplines.keys()):
        if r + 1 in round_disciplines:
            for n1 in round_disciplines[r]:
                for n2 in round_disciplines[r + 1]:
                    # 用浅色弧线连接相邻轮次的学科
                    G.add_edge(n1, n2, edge_type='round_transition',
                              color='#ECF0F1', width=0.8, style='dotted')

    # ===== 绘图 =====
    fig, ax = plt.subplots(1, 1, figsize=(18, 14))
    fig.patch.set_facecolor('#FAFAFA')
    ax.set_facecolor('#FAFAFA')

    # 布局
    pos = nx.spring_layout(G, k=2.5, iterations=80, seed=42)

    # 确保输入节点在中心
    if input_node in pos:
        center = np.array([0.5, 0.5])
        offset = center - pos[input_node]
        for key in pos:
            pos[key] = pos[key] + offset

    # 画边
    for u, v, edata in G.edges(data=True):
        edge_color = edata.get('color', '#BDC3C7')
        edge_width = edata.get('width', 1)
        edge_style = edata.get('style', 'solid')
        nx.draw_networkx_edges(G, pos, edgelist=[(u, v)],
                              edge_color=edge_color, width=edge_width,
                              style=edge_style, alpha=0.6, ax=ax)

    # 画节点
    for ntype in ['round_transition', 'discipline', 'product', 'input']:
        nodes = [n for n in G.nodes() if G.nodes[n].get('node_type') == ntype]
        if not nodes:
            continue

        if ntype == 'input':
            colors = ['#2C3E50']
            sizes = [2000]
        elif ntype == 'discipline':
            colors = [get_discipline_color(G.nodes[n].get('discipline', '未知')) for n in nodes]
            sizes = [800 for _ in nodes]
        elif ntype == 'product':
            colors = [CONFIDENCE_COLORS.get(G.nodes[n].get('confidence', '类比'), '#95A5A6') for n in nodes]
            sizes = [400 for _ in nodes]
        else:
            continue

        nx.draw_networkx_nodes(G, pos, nodelist=nodes,
                              node_color=colors, node_size=sizes,
                              edgecolors='white', linewidths=1.5, ax=ax)

    # 标签
    # 输入标签
    if input_node in pos:
        ax.text(pos[input_node][0], pos[input_node][1] - 0.06,
               input_summary, fontsize=10, ha='center', va='top',
               fontweight='bold', color='white',
               bbox=dict(boxstyle='round,pad=0.3', facecolor='#2C3E50', alpha=0.9))

    # 学科标签
    for node in G.nodes():
        if G.nodes[node].get('node_type') == 'discipline':
            disc = G.nodes[node].get('discipline', '')
            r = G.nodes[node].get('round', 0)
            label = f'R{r}:{disc}'
            color = get_discipline_color(disc)
            ax.text(pos[node][0], pos[node][1] - 0.04,
                   label, fontsize=8, ha='center', va='top',
                   fontweight='bold', color=color)

    # 产物标签
    for node in G.nodes():
        if G.nodes[node].get('node_type') == 'product':
            idea = G.nodes[node].get('idea', '')
            conf = G.nodes[node].get('confidence', '类比')
            conf_color = CONFIDENCE_COLORS.get(conf, '#95A5A6')
            ax.text(pos[node][0], pos[node][1] - 0.03,
                   idea, fontsize=6.5, ha='center', va='top',
                   color='#555555',
                   bbox=dict(boxstyle='round,pad=0.15',
                            facecolor='white', alpha=0.7,
                            edgecolor=conf_color, linewidth=0.8))

    # 图例
    legend_elements = []
    for cat, color in DISCIPLINE_COLORS.items():
        legend_elements.append(mpatches.Patch(color=color, label=cat))
    for conf, color in CONFIDENCE_COLORS.items():
        legend_elements.append(mpatches.Patch(color=color, label=f'置信: {conf}'))
    for strat, color in STRATEGY_COLORS.items():
        legend_elements.append(mpatches.Patch(color=color, label=strat))

    ax.legend(handles=legend_elements, loc='lower left', fontsize=8,
             framealpha=0.9, edgecolor='#BDC3C7', ncol=2)

    ax.axis('off')
    ax.set_title('万物生 · 网状图\n万物互联，碰撞生新', fontsize=16,
                fontweight='bold', color='#2C3E50', pad=20)

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight',
               facecolor=fig.get_facecolor())
    plt.close()
    print(f'✅ 网状图已生成: {output_path}')


def main():
    parser = argparse.ArgumentParser(description='万物生·网状图生成器')
    parser.add_argument('--input', required=True, help='碰撞JSON数据文件路径')
    parser.add_argument('--output', default='wusheng_network.png', help='输出图片路径')
    args = parser.parse_args()

    data = load_data(args.input)
    draw_network(data, args.output)


if __name__ == '__main__':
    main()
