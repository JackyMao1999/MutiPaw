#!/bin/bash
# MutiPaw 监控面板启动脚本

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
VENV_PATH="${SCRIPT_DIR}/../.venv"

echo "🚀 启动 MutiPaw 监控面板..."

# 检查是否在正确的目录
if [[ ! -d "${VENV_PATH}" ]]; then
    echo "❌ 错误: 未找到虚拟环境，请先运行 ./start_up.sh"
    exit 1
fi

# 激活虚拟环境
source "${VENV_PATH}/bin/activate"

# 检查依赖
pip3 install -r ../requirements.txt --quiet

# 启动监控服务
echo "📊 启动监控服务..."
echo "🌐 访问地址: http://localhost:8090"
echo "⏰ 启动时间: $(date)"
echo ""

python3 monitor.py