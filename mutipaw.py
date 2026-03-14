import os
import time
import docker
import argparse
import subprocess
import pytomlpp
import logging
from typing import Dict, List, Optional
from docker.errors import ContainerNotFound, DockerException

def read_toml_file(file_path: str) -> Dict:
    """读取toml配置文件

    Args:
        file_path: 配置文件路径

    Returns:
        配置数据的字典格式

    Raises:
        FileNotFoundError: 文件不存在时抛出
        Exception: 文件读取或解析错误时抛出
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"配置文件 {file_path} 不存在")
    
    try:
        with open(file_path, "r", encoding="utf-8") as config:
            config_data = pytomlpp.loads(config.read())
            return config_data
    except Exception as e:
        raise Exception(f"读取配置文件失败: {str(e)}")

def start_paws() -> None:
    """启动config配置中的所有容器
    
    Raises:
        Exception: 配置文件读取或容器启动失败时抛出
    """
    try:
        print("🚀 开始启动 MutiPaw 智能体...")
        file = read_toml_file("config.toml")
        env = os.environ.copy()
        env["IMAGE"] = file["IMAGE"]
        paws_list = file["mutipaws"]
        
        success_count = 0
        for i, paw in enumerate(paws_list, 1):
            try:
                print(f"📦 [{i}/{len(paws_list)}] 启动容器: {paw['CONTAINER_NAME']}")
                
                env["CONTAINER_NAME"] = paw["CONTAINER_NAME"] 
                env["PORT"] = paw["PORT"]
                env["COMPOSE_PROJECT_NAME"] = paw["CONTAINER_NAME"]
                if "NETWORK_MODE" in paw:
                    env["NETWORK_MODE"] = paw["NETWORK_MODE"]
                
                result = subprocess.run(
                    ["docker", "compose", "up", "-d"],
                    env=env,
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    print(f"✅ {paw['CONTAINER_NAME']} 启动成功")
                    print(f"   端口: {paw['PORT']}, 网络: {paw.get('NETWORK_MODE', 'bridge')}")
                    success_count += 1
                else:
                    print(f"❌ {paw['CONTAINER_NAME']} 启动失败")
                    print(f"错误: {result.stderr}")
                
            except Exception as e:
                print(f"❌ {paw['CONTAINER_NAME']} 启动异常: {str(e)}")
            
            time.sleep(1)
        
        print(f"\n📊 启动完成: {success_count}/{len(paws_list)} 个容器启动成功")
        
    except Exception as e:
        print(f"❌ 启动 MutiPaw 失败: {str(e)}")
        raise

def stop_paws() -> None:
    """停止config配置中的所有容器
    
    Raises:
        Exception: 配置文件读取或容器停止失败时抛出
    """
    try:
        print("🛑 开始停止 MutiPaw 智能体...")
        file = read_toml_file("config.toml")
        paws_list = file["mutipaws"]
        
        success_count = 0
        for i, paw in enumerate(paws_list, 1):
            container_name = paw["CONTAINER_NAME"]
            try:
                print(f"📦 [{i}/{len(paws_list)}] 停止容器: {container_name}")
                
                # 初始化Docker客户端
                client = docker.from_env()
                
                # 1. 获取容器对象
                container = client.containers.get(container_name)
                
                # 2. 停止容器（如果容器正在运行）
                if container.status == 'running':
                    container.stop()
                    print(f"   ✅ 容器 {container.name} 已停止")
                
                # 3. 删除容器
                container.remove(force=True)
                print(f"   ✅ 容器 {container.name} 已删除")
                success_count += 1
                
            except ContainerNotFound:
                print(f"   ⚠️  容器 {container_name} 不存在，跳过")
            except DockerException as e:
                print(f"   ❌ Docker操作失败: {str(e)}")
            except Exception as e:
                print(f"   ❌ 停止容器异常: {str(e)}")
            
            time.sleep(1)
        
        print(f"\n📊 停止完成: {success_count}/{len(paws_list)} 个容器已停止")
        
    except Exception as e:
        print(f"❌ 停止 MutiPaw 失败: {str(e)}")
        raise

def start_single_paw(paw_name: str) -> bool:
    """启动其中一个指定的容器
    
    Args:
        paw_name: 要启动的容器名称
        
    Returns:
        bool: 启动成功返回True，否则返回False
    """
    try:
        print(f"🚀 启动单个智能体: {paw_name}")
        file = read_toml_file("config.toml")
        paws_list = file["mutipaws"]
        
        for paw in paws_list:
            if paw["CONTAINER_NAME"] == paw_name:
                env = os.environ.copy()
                env["CONTAINER_NAME"] = paw["CONTAINER_NAME"] 
                env["PORT"] = paw["PORT"]
                env["COMPOSE_PROJECT_NAME"] = paw["CONTAINER_NAME"]
                if "NETWORK_MODE" in paw:
                    env["NETWORK_MODE"] = paw["NETWORK_MODE"]
                
                print(f"📋 配置信息:")
                print(f"   容器名: {paw['CONTAINER_NAME']}")
                print(f"   端口: {paw['PORT']}")
                print(f"   网络模式: {paw.get('NETWORK_MODE', 'bridge')}")
                
                result = subprocess.run(
                    ["docker", "compose", "up", "-d"],
                    env=env,
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    print(f"✅ {paw_name} 启动成功")
                    return True
                else:
                    print(f"❌ {paw_name} 启动失败")
                    print(f"错误: {result.stderr}")
                    return False
        
        print(f"❌ 未找到容器配置: {paw_name}")
        return False
        
    except Exception as e:
        print(f"❌ 启动 {paw_name} 失败: {str(e)}")
        return False

def stop_single_paw(paw_name: str) -> bool:
    """停止其中一个指定的容器
    
    Args:
        paw_name: 要停止的容器名称
        
    Returns:
        bool: 停止成功返回True，否则返回False
    """
    try:
        print(f"🛑 停止单个智能体: {paw_name}")
        
        # 初始化Docker客户端
        client = docker.from_env()
        
        # 1. 获取容器对象
        container = client.containers.get(paw_name)
        
        # 2. 停止容器（如果容器正在运行）
        if container.status == 'running':
            container.stop()
            print(f"✅ 容器 {container.name} 已停止")
        
        # 3. 删除容器
        container.remove(force=True)
        print(f"✅ 容器 {container.name} 已删除")
        
        return True
        
    except ContainerNotFound:
        print(f"⚠️  容器 {paw_name} 不存在，无需停止")
        return True
    except DockerException as e:
        print(f"❌ Docker操作失败: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ 停止容器异常: {str(e)}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MutiPaw 多智能体管理工具")
    parser.add_argument("--option", type=str, choices=["start", "stop"], 
                       help="操作类型: start-启动, stop-停止")
    parser.add_argument("--paw", default="all", type=str,
                       help="容器名称，不指定则操作全部")
    args = parser.parse_args()
    
    option = args.option
    paw_name = args.paw
    
    if option == "start":
        if paw_name == "all":
            start_paws()
        else:
            start_single_paw(paw_name)
    elif option == "stop":
        if paw_name == "all":
            stop_paws()
        else:
            stop_single_paw(paw_name)
    else:
        parser.print_help()
