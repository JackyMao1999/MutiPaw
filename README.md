# MutiPaw

MutiPaw 是一个基于 [CoPaw](https://github.com/agentscope-ai/CoPaw) 项目扩展的工具，旨在提供启动和管理多个 Paw 智能体（Agent）的能力。

## 项目简介

CoPaw 是一个功能强大的个人 AI 助手框架，支持多种聊天渠道（如钉钉、飞书、QQ、Discord 等）并具有高度的可扩展性。MutiPaw 在此基础上，专注于**多实例、多角色**的部署场景，让用户能够更方便地在同一套环境下运行多个相互独立或协同工作的智能体。

## 核心功能

- **多智能体启动**：通过 Docker Compose 轻松管理多个智能体实例，每个实例可以有独立的配置和存储。
- **配置隔离**：每个智能体拥有独立的数据目录 (`copaw-data`) 和密钥目录 (`copaw-secrets`)。
- **高性能运行**：基于 ARM64 优化的镜像，适合在 Orange Pi 等嵌入式设备上流畅运行。

## 快速开始

### 1. 环境准备

确保您的系统中已安装 Docker 和 Docker Compose。

### 2. 启动多个智能体

要启动多个智能体，您可以在 `docker-compose.yml` 中定义多个服务，或使用 Docker Compose 的 `scale` 功能（如果配置允许）。

#### 示例：在 `docker-compose.yml` 中手动添加多个服务

```yaml
services:
  agent1:
    image: swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/agentscope/copaw:v0.0.5-linuxarm64
    container_name: copaw-1
    volumes:
      - copaw-data-1:/app/working
      - copaw-secrets-1:/app/working.secret
    # ... 其他配置
  
  agent2:
    image: swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/agentscope/copaw:v0.0.5-linuxarm64
    container_name: copaw-2
    volumes:
      - copaw-data-2:/app/working
      - copaw-secrets-2:/app/working.secret
    # ... 其他配置
```

### 3. 运行项目

```bash
docker-compose up -d
```

## 项目结构

- `docker-compose.yml`: Docker 编排文件，定义了服务和卷挂载。
- `mutipaw.py`: (开发中) 用于管理多智能体生命周期的 Python 脚本。
- `start_up.sh`: 项目启动入口脚本。
- `.venv/`: Python 虚拟环境。

## 后续计划

- [ ] 实现 `mutipaw.py` 以支持更复杂的动态多智能体管理。
- [ ] 提供更多预设的智能体角色模板。
- [ ] 优化多智能体之间的通信与协同逻辑。

---

## 致谢

感谢 [CoPaw](https://github.com/agentscope-ai/CoPaw) 团队提供的优秀框架支持。
