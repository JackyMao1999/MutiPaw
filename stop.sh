#/bin/bash

source .venv/bin/activate

PAW_NAME=$1

if [[ "x${PAW_NAME}" != "x" ]]; then
    python3 mutipaw.py --option="stop" --paw=${PAW_NAME}
else
    python3 mutipaw.py --option="stop"
fi
