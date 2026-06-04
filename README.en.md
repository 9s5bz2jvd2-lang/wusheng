# 万物生 · Interdisciplinary Creativity Engine

English version translated from the existing Chinese README.

> **One gives birth to two; two gives birth to three; three gives birth to all things. I do not distill; I create.**

## What is this?

万物生 is an AI Agent Skill. After invocation, it dispatches the input across multiple disciplinary dimensions for **three rounds of collision-based exploration**. Based on a cyclic architecture from “Circle Theory” — divergence → return → renewed departure — it generates new theories, new frameworks, and new ideas.

**万物生 is not a knowledge mover. It is a knowledge chemical reactor.**

## Three Collision Modes

| Mode | Direction | Description |
|------|-----------|-------------|
| **Internal collision** | Inward decomposition | Break down and collide within the structure itself to find cracks, contradictions, and hidden patterns. |
| **External collision** | Outward collision | Bring in other disciplines for cross-domain collision and transfer to generate something new. |
| **Infinite collision** | Let things arise and perish | Release boundaries for random jumps, blank-space creation, and extreme exploration. |

Collision boundaries are defined by the user. Writing a collision guide can greatly improve precision; see `reference/collision-guide-writing.md`.

## Core Principle

| Level | Meaning | What existing distillation projects do |
|------|---------|----------------------------------------|
| Copy | Move the original over unchanged | ✅ all projects |
| Compress | Remove the rough and keep the essence | ✅ some projects |
| Translate | Express in another language | ✅ some projects |
| Reorganize | Shuffle and rearrange | ⚠️ a few projects |
| **Infer** | **Move one step forward along the rules** | ❌ none |
| **Create** | **Generate something new through cross-domain transfer** | ❌ none |

**万物生 works at levels 5 and 6.**

## Three-Round Collision Framework

```text
Input content
  → Round 1: Heaven and Earth Open (breadth) → thought seeds
  → Round 2: All Things Sprout (depth) → semi-formed theory
  → Round 3: Triangle Fixes the Circle (validation) → formed theory
  → Visual outputs: circle diagram + network graph + inference-path tree + multi-angle advice map
```

**One point opens heaven and earth; two points set direction; three points close the circle. Three rounds of collision, and all things begin to grow.**

## Six Collision Strategies

| Strategy | Core action |
|---------|-------------|
| Structural collision | Framework vs. framework → cracks generate a new framework |
| Assumption collision | Premise vs. premise → contradiction generates a new premise |
| Boundary stitching | Endpoint vs. starting point → stitching generates an interdisciplinary field |
| Reverse replication | Pattern vs. anti-pattern → reversal generates a disruptive assumption |
| Scale jump | Micro vs. macro → jumping generates scaling laws |
| Missing-part injection | What is absent vs. what exists → transfer generates a new method |

## Discipline Library

- **Preset**: 6 categories × 5 disciplines (natural sciences, social sciences, humanities, arts, engineering, Eastern wisdom).
- **Dynamic**: automatically matches the best collision disciplines based on the input.
- **Customizable**: users can add disciplines at any time.

## Visual Outputs

Four graphics are generated automatically by Python scripts:

| Graphic | Expression |
|---------|------------|
| Circle diagram | Three concentric rounds: point → line → circle |
| Network graph | Discipline nodes + collision edges + product labels |
| Inference-path tree | Input → theory, step by step and traceable |
| Multi-angle advice map | Actionable suggestions from user value, evidence, engineering, narrative/research, and safety angles |

## File Structure

```text
wusheng/
├── SKILL.md
├── reference/
│   ├── triangle-circle.md
│   ├── collision-engine.md
│   ├── collision-modes.md
│   ├── collision-guide-writing.md
│   ├── three-rounds.md
│   ├── six-strategies.md
│   ├── discipline-library.md
│   ├── return-harmony.md
│   └── visual-output.md
├── scripts/
│   ├── wusheng_circle.py
│   ├── wusheng_network.py
│   ├── wusheng_trajectory.py
│   └── wusheng_advice_map.py
├── README.md
└── install.sh
```

## Installation

```bash
bash install.sh
```

## Usage

1. Load `SKILL.md` into an AI Agent.
2. Enter content and optionally specify collision disciplines.
3. The Agent performs the three-round collision process.
4. It outputs collision JSON data.
5. Run the scripts to generate visualizations:

```bash
python3 scripts/wusheng_circle.py --input collision_data.json --output circle.png
python3 scripts/wusheng_network.py --input collision_data.json --output network.png
python3 scripts/wusheng_trajectory.py --input collision_data.json --output trajectory.png
python3 scripts/wusheng_advice_map.py --input collision_data.json --output advice_map.png
```

## Theoretical Basis

**Circle Theory** (Runyuan Wang): A net connects; a sphere becomes a body. Mind and spirit unite; my circle is as one.

万物生 applies Circle Theory’s divergence → return → unity-holding architecture to interdisciplinary creativity.

## Author

Runyuan Wang, M.S. in Nutrition and Food Hygiene, Kunming Medical University; Chinese Registered Dietitian. Built with WorkBuddy.

## License

MIT License
