import os
import time
import subprocess
import pytomlpp
import json

def read_toml_file(file_path) -> json:
    """ 读toml文件

    Returns:
        返回json格式的配置参数
    """
    # 判断文件是否存在
    if os.path.exists(file_path):
        read_state = "r+"
    else:
        read_state = "w+"
    config = open(file_path, read_state, encoding="utf-8")
    config_data = pytomlpp.loads(config.read())
    return config_data


if __name__ == "__main__":
    print("Start MutiPaw.")
    file = read_toml_file("config.toml")
    env = os.environ.copy()
    env["IMAGE"] = file["IMAGE"]
    paws_list = file["mutipaws"]
    for paw in paws_list:
        env["CONTAINER_NAME"] = paw["CONTAINER_NAME"] 
        env["DATA_VOLUME"] = paw["DATA_VOLUME"]
        env["PORT"] = paw["PORT"]
        env["COMPOSE_PROJECT_NAME"] = paw["CONTAINER_NAME"]
        print("============Paw info============")
        print(paw)
        result = subprocess.run(
                ["docker", "compose", "up", "-d"],
                env=env,
                capture_output=True,
                text=True
        )
        if result.returncode == 0:
            print("Successed.")
            print(result.stdout)
        else:
            print("Failed.")
            print(result.stdout)
            print(result.stderr)
        
        print("================================")
        time.sleep(1)
    print("Start Mutipaw ending.")
