#!/bin/bash
# MutiPaw 停止脚本

# 检查是否在正确的目录
if [[ ! -f "mutipaw.py" ]]; then
    echo "❌ 错误: 请在 MutiPaw 项目根目录运行此脚本"
    exit 1
fi

echo "🛑 进入虚拟环境..."
source .venv/bin/activate

PAW_NAME=$1

if [[ "x${PAW_NAME}" != "x" ]]; then
    echo "🛑 停止单个智能体: ${PAW_NAME}"
    python3 mutipaw.py --option="stop" --paw=${PAW_NAME}
else
    echo "🛑 停止所有智能体"
    python3 mutipaw.py --option="stop"
fi
