# /bin/bash
# 这是一个启动程序

# 1. 初始化环境
if ! command -v python3-dev &>/dev/null; then
    sudo apt install python3-dev
fi

if ! command -v python3-venv &>/dev/null; then
    sudo apt install python3-venv
fi
# 2. 如果没有虚拟环境，创建一个虚拟环境
python3 -m venv .venv

# 3. 进入虚拟环境之后安装requirements
source .venv/bin/activate
pip3 install -r requirements.txt

# 4. 启动程序
python3 mutipaw.py --option="start"
