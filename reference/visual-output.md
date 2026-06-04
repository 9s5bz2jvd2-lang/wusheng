# 可视化输出规范

> **思想的形状，看得见。**

## 概述

万物生的可视化输出包含四种图形，由 Python 脚本根据碰撞 JSON 数据生成：

| 图形 | 脚本 | 表达什么 |
|------|------|---------|
| **圆图** | `scripts/wusheng_circle.py` | 三轮碰撞的同心圆结构——点→线→圆 |
| **网状图** | `scripts/wusheng_network.py` | 学科节点 + 碰撞连线 + 产物标注——万物互联 |
| **推演路径树** | `scripts/wusheng_trajectory.py` | 从输入到最终理论的推理链——来龙去脉 |
| **多角度建议图** | `scripts/wusheng_advice_map.py` | 从用户价值、证据、工程、叙事/研究等角度给行动建议 |

---

## JSON 数据格式

三轮碰撞完成后，AI须按以下格式输出 JSON，供脚本读取：

```json
{
  "input": {
    "summary": "原始输入内容的一句话概括",
    "deep_analysis": {
      "frameworks": ["框架1", "框架2"],
      "assumptions": ["假设1", "假设2"],
      "boundaries": ["边界1", "边界2"],
      "meta_patterns": ["模式1", "模式2"],
      "gaps": ["空缺1", "空缺2"]
    }
  },
  "rounds": [
    {
      "round": 1,
      "name": "天地开辟",
      "daemons": [
        {
          "daemon_id": "D1",
          "discipline": "物理学",
          "target_structure": "框架",
          "strategy": "结构对撞",
          "collision_products": [
            {
              "idea": "新想法的简短描述",
              "type": "裂缝",
              "confidence": "类比",
              "value": "高",
              "derivation": "从物理学的X框架与输入的Y框架对撞，发现..."
            }
          ],
          "return_block": {
            "reusable_patterns": ["可复用模式"],
            "gotchas": ["踩到的坑"],
            "open_questions": ["开放问题"],
            "should_promote": ["应提升到枢纽的内容"],
            "do_not_promote": ["不应提升的内容"]
          }
        }
      ],
      "hub_seeds": ["种子1描述", "种子2描述"]
    },
    {
      "round": 2,
      "name": "万物萌生",
      "daemons": [
        {
          "daemon_id": "D6",
          "discipline": "控制论",
          "target_seed": "种子1",
          "strategy": "结构对撞",
          "collision_products": [
            {
              "idea": "半成型理论片段",
              "type": "缝合",
              "confidence": "实推",
              "value": "高",
              "derivation": "..."
            }
          ],
          "return_block": {
            "reusable_patterns": [],
            "gotchas": [],
            "open_questions": [],
            "should_promote": [],
            "do_not_promote": []
          }
        }
      ],
      "hub_semi_products": ["半成品1描述", "半成品2描述"]
    },
    {
      "round": 3,
      "name": "三角定圆",
      "daemons": [
        {
          "daemon_id": "D9",
          "discipline": "佛学",
          "target_semi_product": "半成品1",
          "strategy": "假设对撞",
          "collision_products": [
            {
              "idea": "验证结果",
              "type": "矛盾",
              "confidence": "猜想",
              "value": "中",
              "derivation": "..."
            }
          ],
          "return_block": {
            "reusable_patterns": [],
            "gotchas": [],
            "open_questions": [],
            "should_promote": [],
            "do_not_promote": []
          }
        }
      ],
      "final_judgments": [
        {
          "semi_product": "半成品1",
          "verdict": "成型",
          "reasoning": "..."
        }
      ]
    }
  ],
  "final_output": {
    "theory": "成型理论的完整描述",
    "derivation_path": "推演路径的文字描述",
    "open_questions": ["未解决问题1", "未解决问题2"],
    "confidence_overall": "类比",
    "valuable_failures": ["有价值的失败1"],
    "angle_recommendations": [
      {
        "angle": "用户价值|证据/事实|工程落地|叙事传播|研究问题|商业模式|伦理安全",
        "suggestion": "从该角度提出的一条具体建议",
        "priority": "高|中|低",
        "confidence": "实推|类比|猜想",
        "next_action": "下一步可执行动作",
        "risk_note": "边界、风险或必须核验处"
      }
    ]
  }
}
```

---

## 三种可视化详细说明

### 1. 圆图（wusheng_circle.py）

**视觉设计**：
- 三个同心圆，从内到外 = 第1轮→第2轮→第3轮
- 中心点 = 原始输入（黑色实心大圆点）
- 每个圆上分布该轮碰撞的学科节点（彩色圆点，大类同色）
- 圆之间有连线：某学科碰撞产物传递到下一轮（弧线，颜色=策略类型）
- 产物节点：圆之间的连线上标注新想法（小圆点，颜色=置信度）

**颜色方案**：
| 元素 | 颜色 |
|------|------|
| 中心输入点 | #2C3E50（深灰） |
| 自然科学节点 | #3498DB（蓝） |
| 社会科学节点 | #E74C3C（红） |
| 人文学科节点 | #9B59B6（紫） |
| 艺术节点 | #F39C12（橙） |
| 工程节点 | #1ABC9C（青） |
| 东方智慧节点 | #E67E22（棕橙） |
| 实推置信 | #27AE60（绿） |
| 类比置信 | #F1C40F（黄） |
| 猜想置信 | #E74C3C（红） |

**输出**：PNG，12×12 inch，300dpi

### 2. 网状图（wusheng_network.py）

**视觉设计**：
- 中心大节点 = 原始输入
- 中节点 = 学科（按大类着色）
- 小节点 = 碰撞产物（按置信度着色）
- 实线 = 学科与输入的连接（灰色）
- 彩色虚线 = 碰撞产生的连线（颜色=策略类型）
- 小节点旁标注新想法的简短文字

**布局**：spring layout（力导向布局），同类学科聚簇

**输出**：PNG，16×12 inch，300dpi

**字体注意**：若中文字体显示为方框，先安装或启用 PingFang / Hiragino Sans GB / Arial Unicode MS / Noto Sans CJK / Microsoft YaHei / SimHei 等 CJK 字体；脚本已按此顺序设置 fallback。

### 3. 推演路径树（wusheng_trajectory.py）

**视觉设计**：
- 根节点 = 原始输入
- 第1层分支 = 第1轮碰撞维度
- 第2层分支 = 第1轮产物 → 第2轮碰撞
- 第3层分支 = 第2轮产物 → 第3轮验证
- 叶节点 = 最终成型理论
- 每条边标注：策略 + 置信度
- 节点颜色：成型=绿，失败=红，可修=黄

**输出**：PNG，18×10 inch，300dpi

### 4. 多角度建议图（wusheng_advice_map.py）

**何时必须生成**：
- 用户说“还要输出一个图”“从不同角度给建议”“给我一张建议图/路线图/角度图”。
- 输出对象不只是思想路径，还需要转成下一步行动。

**视觉设计**：
- 中心 = 原始输入 + 成型产物。
- 外圈 = 不同建议角度：用户价值、证据/事实、工程落地、叙事传播、研究问题、商业模式、伦理安全等。
- 每个角度节点包含：建议、下一步、风险边界、优先级、置信度。
- 颜色 = 优先级（高/中/低）；形状 = 置信度（实推/类比/猜想）。

**建议角度选择法**：
1. **用户价值**：谁会受益？最小可见收益是什么？
2. **证据/事实**：哪些是事实，哪些是类比，哪些是猜想？哪些必须核验？
3. **工程落地**：能否拆成数据、流程、界面、评测、脚本或原型？
4. **叙事传播**：普通人怎么听懂？隐喻是否安全？
5. **研究问题**：哪些猜想可以变成可检验问题？
6. **伦理安全**：会不会误导、越权、制造羞耻或过度承诺？

**输出**：PNG，16×12 inch，300dpi

**字体注意**：若中文字体显示为方框，先安装或启用 PingFang / Hiragino Sans GB / Arial Unicode MS / Noto Sans CJK / Microsoft YaHei / SimHei 等 CJK 字体；脚本已按此顺序设置 fallback。

---

## 使用方式

```bash
# 安装依赖
pip3 install matplotlib networkx numpy

# 生成圆图
python3 scripts/wusheng_circle.py --input collision_data.json --output circle.png

# 生成网状图
python3 scripts/wusheng_network.py --input collision_data.json --output network.png

# 生成推演路径树
python3 scripts/wusheng_trajectory.py --input collision_data.json --output trajectory.png

# 生成多角度建议图
python3 scripts/wusheng_advice_map.py --input collision_data.json --output advice_map.png

# 一键生成全部四种图
python3 scripts/wusheng_circle.py --input collision_data.json --output circle.png --all
```
