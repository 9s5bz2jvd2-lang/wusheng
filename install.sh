#!/bin/bash
# 万物生安装脚本

echo "🔧 万物生·跨学科创造力引擎 安装中..."
echo ""

# 检测Python
if command -v python3 &> /dev/null; then
    PYTHON=python3
elif command -v python &> /dev/null; then
    PYTHON=python
else
    echo "❌ 未检测到Python，请先安装Python 3.8+"
    exit 1
fi

echo "✅ 检测到Python: $PYTHON"
$PYTHON --version

# 安装依赖
echo ""
echo "📦 安装Python依赖..."
$PYTHON -m pip install matplotlib networkx numpy --quiet

if [ $? -eq 0 ]; then
    echo "✅ 依赖安装成功"
else
    echo "❌ 依赖安装失败，请尝试手动安装："
    echo "   pip3 install matplotlib networkx numpy"
    exit 1
fi

# 验证
echo ""
echo "🧪 验证安装..."
$PYTHON -c "import matplotlib; import networkx; import numpy; print('✅ 所有依赖验证通过')"

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 万物生安装完成！"
    echo ""
    echo "使用方式："
    echo "  1. 将 SKILL.md 加载到 AI Agent"
    echo "  2. 输入内容 + 可选指定碰撞学科"
    echo "  3. Agent 执行三轮碰撞，输出 JSON"
    echo "  4. 运行可视化脚本："
    echo "     python3 scripts/wusheng_circle.py --input data.json --output circle.png"
    echo "     python3 scripts/wusheng_network.py --input data.json --output network.png"
    echo "     python3 scripts/wusheng_trajectory.py --input data.json --output trajectory.png"
else
    echo "❌ 验证失败"
    exit 1
fi
