#!/usr/bin/env python3
"""
万物生 · 圆图生成器
Three concentric circles: Round 1 (inner) → Round 2 (middle) → Round 3 (outer)
"""

import json
import argparse
import math
import subprocess
import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import numpy as np

# 中文字体支持
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK JP', 'Noto Serif CJK JP', 'DejaVu Sans']
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

# 学科→大类映射
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

ROUND_NAMES = {1: '天地开辟', 2: '万物萌生', 3: '三角定圆'}


def get_discipline_color(discipline):
    cat = DISCIPLINE_CATEGORY.get(discipline, '自然科学')
    return DISCIPLINE_COLORS.get(cat, '#95A5A6')


def load_data(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def draw_circle_chart(data, output_path):
    fig, ax = plt.subplots(1, 1, figsize=(14, 14), subplot_kw={'aspect': 'equal'})
    fig.patch.set_facecolor('#FAFAFA')
    ax.set_facecolor('#FAFAFA')

    center = (0, 0)
    radii = [2.0, 3.5, 5.0]  # 三轮的圆半径

    # 画同心圆（虚线）
    for i, r in enumerate(radii):
        circle = plt.Circle(center, r, fill=False, linewidth=1.5,
                          linestyle='--', color='#BDC3C7', alpha=0.6)
        ax.add_patch(circle)
        # 标注轮次名称
        angle = math.radians(90)
        label_x = r * math.cos(angle)
        label_y = r * math.sin(angle)
        ax.text(label_x + 0.1, label_y + 0.15,
                f'第{i+1}轮：{ROUND_NAMES[i+1]}',
                fontsize=11, color='#7F8C8D', ha='left', va='bottom',
                fontweight='bold')

    # 中心点（原始输入）
    ax.plot(0, 0, 'o', color='#2C3E50', markersize=18, zorder=10)
    summary = data.get('input', {}).get('summary', '输入')
    # 截断长文本
    if len(summary) > 20:
        summary = summary[:18] + '...'
    ax.text(0, -0.35, summary, fontsize=9, ha='center', va='top',
            color='#2C3E50', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

    # 收集所有学科节点
    all_nodes = []  # (round_idx, discipline, angle, products)

    for round_data in data.get('rounds', []):
        round_idx = round_data['round']
        daemons = round_data.get('daemons', [])
        n_daemons = len(daemons)
        if n_daemons == 0:
            continue

        # 均匀分布在该圆上
        angle_step = 360 / n_daemons
        start_angle = 90  # 从顶部开始

        for j, daemon in enumerate(daemons):
            discipline = daemon.get('discipline', '未知')
            angle = math.radians(start_angle + j * angle_step)
            r = radii[round_idx - 1]

            x = r * math.cos(angle)
            y = r * math.sin(angle)
            color = get_discipline_color(discipline)

            # 画学科节点
            ax.plot(x, y, 'o', color=color, markersize=14, zorder=8,
                   markeredgecolor='white', markeredgewidth=1.5)

            # 学科名称
            label_r = r + 0.5
            lx = label_r * math.cos(angle)
            ly = label_r * math.sin(angle)
            ax.text(lx, ly, discipline, fontsize=9, ha='center', va='center',
                   color=color, fontweight='bold')

            # 收集碰撞产物
            products = daemon.get('collision_products', [])
            all_nodes.append((round_idx, discipline, x, y, angle, r, products, color))

    # 画轮次之间的连线（产物传递）
    for i in range(len(all_nodes)):
        for j in range(len(all_nodes)):
            ri, disc_i, xi, yi, ai, rad_i, prods_i, col_i = all_nodes[i]
            rj, disc_j, xj, yj, aj, rad_j, prods_j, col_j = all_nodes[j]
            # 只连相邻轮次
            if rj == ri + 1:
                # 用弧线连接
                mid_x = (xi + xj) / 2
                mid_y = (yi + yj) / 2
                # 稍微弯曲
                perp_x = -(yj - yi) * 0.15
                perp_y = (xj - xi) * 0.15
                ctrl_x = mid_x + perp_x
                ctrl_y = mid_y + perp_y

                # 画曲线
                t = np.linspace(0, 1, 50)
                curve_x = (1-t)**2 * xi + 2*(1-t)*t * ctrl_x + t**2 * xj
                curve_y = (1-t)**2 * yi + 2*(1-t)*t * ctrl_y + t**2 * yj
                ax.plot(curve_x, curve_y, '-', color='#BDC3C7', alpha=0.4, linewidth=1)

                # 在连线上标注碰撞产物
                if prods_i:
                    best_prod = max(prods_i, key=lambda p: {'高': 3, '中': 2, '低': 1}.get(p.get('value', '低'), 1))
                    idea = best_prod.get('idea', '')
                    if len(idea) > 15:
                        idea = idea[:13] + '...'
                    conf = best_prod.get('confidence', '类比')
                    conf_color = CONFIDENCE_COLORS.get(conf, '#95A5A6')

                    # 产物小圆点
                    dot_x = ctrl_x
                    dot_y = ctrl_y
                    ax.plot(dot_x, dot_y, 'o', color=conf_color, markersize=8,
                           zorder=9, markeredgecolor='white', markeredgewidth=1)
                    ax.text(dot_x, dot_y - 0.25, idea, fontsize=7,
                           ha='center', va='top', color='#555555',
                           bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.7))

    # 最终理论标注
    final = data.get('final_output', {})
    theory = final.get('theory', '')
    if theory:
        if len(theory) > 60:
            theory = theory[:57] + '...'
        ax.text(0, -radii[2] - 0.8, f'★ {theory}', fontsize=11,
               ha='center', va='top', color='#2C3E50', fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='#FDEBD0',
                        edgecolor='#E67E22', linewidth=2))

    # 图例
    legend_elements = []
    for cat, color in DISCIPLINE_COLORS.items():
        legend_elements.append(mpatches.Patch(color=color, label=cat))
    for conf, color in CONFIDENCE_COLORS.items():
        legend_elements.append(mpatches.Patch(color=color, label=f'置信: {conf}'))

    ax.legend(handles=legend_elements, loc='lower left', fontsize=9,
             framealpha=0.9, edgecolor='#BDC3C7')

    ax.set_xlim(-7, 7)
    ax.set_ylim(-7, 7)
    ax.axis('off')
    ax.set_title('万物生 · 圆图\n三角定圆，万物从此生', fontsize=16,
                fontweight='bold', color='#2C3E50', pad=20)

    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight',
               facecolor=fig.get_facecolor())
    plt.close()
    print(f'✅ 圆图已生成: {output_path}')


def main():
    parser = argparse.ArgumentParser(description='万物生·圆图生成器')
    parser.add_argument('--input', required=True, help='碰撞JSON数据文件路径')
    parser.add_argument('--output', default='wusheng_circle.png', help='输出图片路径')
    parser.add_argument('--all', action='store_true', help='同时生成全部三种图')
    args = parser.parse_args()

    data = load_data(args.input)
    draw_circle_chart(data, args.output)

    if args.all:
        base = Path(args.output).stem
        outdir = Path(args.output).parent
        # 调用另外三个脚本，生成完整可视化包
        companion_scripts = [
            ('wusheng_network.py', 'network'),
            ('wusheng_trajectory.py', 'trajectory'),
            ('wusheng_advice_map.py', 'advice_map'),
        ]
        for script, suffix in companion_scripts:
            script_path = Path(__file__).parent / script
            if script_path.exists():
                out_name = base.replace('circle', suffix) if 'circle' in base else f'{base}_{suffix}'
                out_path = outdir / f'{out_name}.png'
                subprocess.run([sys.executable, str(script_path),
                              '--input', args.input, '--output', str(out_path)], check=True)


if __name__ == '__main__':
    main()
