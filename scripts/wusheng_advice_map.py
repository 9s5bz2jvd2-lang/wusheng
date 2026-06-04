#!/usr/bin/env python3
"""
万物生 · 多角度建议图生成器
Radial advice map: angle nodes around the final output, each carrying a concrete suggestion.
"""

import argparse
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

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

PRIORITY_COLORS = {
    '高': '#E74C3C',
    '中': '#F39C12',
    '低': '#3498DB',
}

CONFIDENCE_MARKERS = {
    '实推': 'o',
    '类比': 's',
    '猜想': '^',
}

DEFAULT_ANGLES = [
    {
        'angle': '用户价值',
        'suggestion': '把最能让用户立刻受益的一步写成最小可试动作。',
        'priority': '高',
        'confidence': '实推',
        'next_action': '定义 1 个可观察的用户收益指标。',
        'risk_note': '避免只讲宏大理论而没有行动入口。',
    },
    {
        'angle': '证据/事实',
        'suggestion': '把事实、类比、猜想分层，硬结论先过证据门。',
        'priority': '高',
        'confidence': '实推',
        'next_action': '列出需要核验的事实清单。',
        'risk_note': '不要把跨学科灵感包装成已证实结论。',
    },
    {
        'angle': '工程落地',
        'suggestion': '把成型理论拆成数据、流程、界面、评测四个可实现模块。',
        'priority': '中',
        'confidence': '类比',
        'next_action': '做一个低保真原型或脚本。',
        'risk_note': '避免一次性做全系统。',
    },
    {
        'angle': '叙事/传播',
        'suggestion': '提炼一个能让普通人听懂的隐喻，但保留边界说明。',
        'priority': '中',
        'confidence': '类比',
        'next_action': '写 3 句不同版本的解释。',
        'risk_note': '隐喻不能替代定义和证据。',
    },
]


def load_data(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def truncate(text, max_len=30):
    text = str(text or '')
    if len(text) <= max_len:
        return text
    return text[:max_len - 2] + '…'


def get_recommendations(data):
    final = data.get('final_output', {})
    recs = final.get('angle_recommendations') or final.get('recommendations_by_angle')
    if isinstance(recs, list) and recs:
        return recs
    return DEFAULT_ANGLES


def draw_advice_map(data, output_path):
    recs = get_recommendations(data)
    n = max(len(recs), 1)

    fig, ax = plt.subplots(1, 1, figsize=(16, 12), subplot_kw={'aspect': 'equal'})
    fig.patch.set_facecolor('#FAFAFA')
    ax.set_facecolor('#FAFAFA')

    final = data.get('final_output', {})
    input_summary = data.get('input', {}).get('summary', '输入')
    theory = final.get('theory') or final.get('summary') or '成型产物'

    # central body
    center_box = dict(boxstyle='round,pad=0.8', facecolor='#2C3E50', edgecolor='#2C3E50', alpha=0.95)
    ax.text(0, 0.28, f"主题：{truncate(input_summary, 24)}", ha='center', va='center', fontsize=13,
            color='white', fontweight='bold', bbox=center_box)
    ax.text(0, -0.50, f"成型产物：{truncate(theory, 42)}", ha='center', va='center', fontsize=10,
            color='#2C3E50', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.45', facecolor='#FDEBD0', edgecolor='#E67E22', linewidth=2))

    radius = 4.2
    label_radius = 5.15
    for idx, rec in enumerate(recs):
        angle_rad = math.radians(90 - idx * 360 / n)
        x = radius * math.cos(angle_rad)
        y = radius * math.sin(angle_rad)
        lx = label_radius * math.cos(angle_rad)
        ly = label_radius * math.sin(angle_rad)

        angle_name = rec.get('angle') or rec.get('perspective') or f'角度{idx+1}'
        suggestion = rec.get('suggestion') or rec.get('advice') or ''
        priority = rec.get('priority', '中')
        confidence = rec.get('confidence', '类比')
        next_action = rec.get('next_action') or rec.get('action') or ''
        risk_note = rec.get('risk_note') or rec.get('risk') or ''

        color = PRIORITY_COLORS.get(priority, '#95A5A6')
        marker = CONFIDENCE_MARKERS.get(confidence, 'o')

        ax.plot(x, y, marker=marker, color=color, markersize=18,
                markeredgecolor='white', markeredgewidth=2, zorder=6)
        arrow = FancyArrowPatch((0, 0), (x * 0.92, y * 0.92),
                                arrowstyle='-|>', mutation_scale=12,
                                linewidth=1.8, color=color, alpha=0.55)
        ax.add_patch(arrow)

        ha = 'left' if lx >= 0 else 'right'
        text = f"角度：{angle_name}\n建议：{truncate(suggestion, 34)}"
        if next_action:
            text += f"\n下一步：{truncate(next_action, 30)}"
        if risk_note:
            text += f"\n边界：{truncate(risk_note, 28)}"
        text += f"\n优先级：{priority}｜置信：{confidence}"

        ax.text(lx, ly, text, fontsize=9, ha=ha, va='center', color='#2C3E50',
                bbox=dict(boxstyle='round,pad=0.45', facecolor='white', edgecolor=color,
                          linewidth=1.8, alpha=0.92))

    # outer ring
    ring = plt.Circle((0, 0), radius, fill=False, linestyle='--', linewidth=1.2, color='#BDC3C7', alpha=0.8)
    ax.add_patch(ring)

    legend = []
    for priority, color in PRIORITY_COLORS.items():
        legend.append(mpatches.Patch(color=color, label=f'优先级：{priority}'))
    for confidence, marker in CONFIDENCE_MARKERS.items():
        legend.append(plt.Line2D([0], [0], marker=marker, color='w', label=f'置信：{confidence}',
                                 markerfacecolor='#7F8C8D', markeredgecolor='white', markersize=10))
    ax.legend(handles=legend, loc='lower left', fontsize=9, framealpha=0.92)

    ax.set_xlim(-7.2, 7.2)
    ax.set_ylim(-6.4, 6.4)
    ax.axis('off')
    ax.set_title('万物生 · 多角度建议图\n从成型产物回到可行动的下一步', fontsize=17,
                 fontweight='bold', color='#2C3E50', pad=20)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f'✅ 多角度建议图已生成: {output_path}')


def main():
    parser = argparse.ArgumentParser(description='万物生·多角度建议图生成器')
    parser.add_argument('--input', required=True, help='碰撞JSON数据文件路径')
    parser.add_argument('--output', default='wusheng_advice_map.png', help='输出图片路径')
    args = parser.parse_args()
    draw_advice_map(load_data(args.input), args.output)


if __name__ == '__main__':
    main()
