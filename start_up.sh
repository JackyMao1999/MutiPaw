#!/bin/bash
# MutiPaw 启动脚本

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
PAW_NAME=$1

# 检查是否在正确的目录
if [[ ! -f "${SCRIPT_DIR}/mutipaw.py" ]]; then
    echo "❌ 错误: 请在 MutiPaw 项目根目录运行此脚本"
    exit 1
fi

# 1. 初始化环境
echo "🔧 初始化环境..."
if ! dpkg -s python3-dev &>/dev/null; then
    echo "📦 安装 python3-dev..."
    sudo apt install -y python3-dev
fi

if ! dpkg -s python3-venv &>/dev/null; then
    echo "📦 安装 python3-venv..."
    sudo apt install -y python3-venv
fi

# 2. 创建虚拟环境
if [[ ! -d ${SCRIPT_DIR}/.venv ]]; then
    echo "🔧 创建 Python 虚拟环境..."
    python3 -m venv .venv
fi

# 3. 进入虚拟环境并安装依赖
echo "📦 安装依赖..."
source .venv/bin/activate
pip3 install -r requirements.txt

# 4. 启动程序
if [[ "x${PAW_NAME}" != "x" ]]; then
    echo "🚀 启动单个智能体: ${PAW_NAME}"
    python3 mutipaw.py --option="start" --paw=${PAW_NAME}
else
    echo "🚀 启动所有智能体"
    python3 mutipaw.py --option="start"
fi
