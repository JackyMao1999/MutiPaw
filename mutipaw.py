import os
import time
import docker
import argparse
import subprocess
import pytomlpp

def read_toml_file(file_path):
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

def start_paws():
    """ 启动CoPaw的docker
    """
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

def stop_paws():
    """ 停止CoPaw的docker
    """
    print("Stop MutiPaw.")
    file = read_toml_file("config.toml")
    paws_list = file["mutipaws"]
    for paw in paws_list:
        CONTAINER_NAME = paw["CONTAINER_NAME"] 
        print("============Paw info============")
        print(paw)
        try:
            # 初始化Docker客户端
            client = docker.from_env()
            
            # 1. 获取容器对象
            container = client.containers.get(CONTAINER_NAME)
            
            # 2. 停止容器（如果容器正在运行）
            if container.status == 'running':
                container.stop()
                print(f"容器 {container.name} ({container.id[:12]}) 已停止")
            
            # 3. 删除容器（force=True 强制删除运行中的容器，可选）
            container.remove(force=True)
            print(f"容器 {container.name} ({container.id[:12]}) 已删除")
            
        except ContainerNotFound:
            print(f"错误：容器 {CONTAINER_NAME} 不存在")
        except DockerException as e:
            print(f"Docker操作失败：{str(e)}")
        
        print("================================")
        time.sleep(1)
    print("Stop Mutipaw ending.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--option", type=str)
    args = parser.parse_args()
    option = args.option
    if option == "start":
        start_paws()
    elif option == "stop":
        stop_paws()
    
