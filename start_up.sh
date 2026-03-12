# /bin/bash
# 这是一个启动程序
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
# 1. 初始化环境
if ! dpkg -s python3-dev &>/dev/null; then
    sudo apt install python3-dev
fi

if ! dpkg -s python3-venv &>/dev/null; then
    sudo apt install python3-venv
fi
# 2. 如果没有虚拟环境，创建一个虚拟环境
if [[ ! -d ${SCRIPT_DIR}/.venv ]]; then
    python3 -m venv .venv
fi

# 3. 进入虚拟环境之后安装requirements
source .venv/bin/activate
pip3 install -r requirements.txt

# 4. 启动程序
python3 mutipaw.py --option="start"
