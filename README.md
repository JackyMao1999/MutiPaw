# MutiPaw

MutiPaw 是一个基于 [CoPaw](https://github.com/agentscope-ai/CoPaw) 项目扩展的工具，旨在提供启动和管理多个 Paw 智能体（Agent）的能力。

## 项目简介

CoPaw 是一个功能强大的个人 AI 助手框架，支持多种聊天渠道（如钉钉、飞书、QQ、Discord 等）并具有高度的可扩展性。MutiPaw 在此基础上，专注于**多实例、多角色**的部署场景，让用户能够更方便地在同一套环境下运行多个相互独立或协同工作的智能体。

## 核心功能

- **多智能体启动**：通过 Docker Compose 轻松管理多个智能体实例，每个实例可以有独立的配置和存储。
- **配置隔离**：每个智能体拥有独立的数据目录 (`copaw-data`) 和密钥目录 (`copaw-secrets`)。
- **精细化控制**：支持启动/停止单个容器或全部容器。
- **网络模式灵活**：支持 host 和 bridge 网络模式。
- **高性能运行**：基于 ARM64 优化的镜像，适合在 Orange Pi 等嵌入式设备上流畅运行。

## 快速开始

### 1. 环境准备

确保您的系统中已安装：
- Docker
- Docker Compose
- Python 3.6+

### 2. 克隆项目

```bash
git clone https://github.com/JackyMao1999/MutiPaw.git
cd MutiPaw
```

### 3. 配置智能体

编辑 `config.toml` 文件，配置您需要的智能体实例：

```toml
IMAGE = "swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/agentscope/copaw:v0.0.7-linuxarm64"

[[mutipaws]]
CONTAINER_NAME = "copaw"      # 容器名称
PORT = "8088"                 # 映射端口
NETWORK_MODE = "host"         # 网络模式：host 或 bridge

[[mutipaws]]
CONTAINER_NAME = "copaw2"
PORT = "8089"
NETWORK_MODE = "bridge"

[[mutipaws]]
CONTAINER_NAME = "copaw3"
PORT = "8090"
NETWORK_MODE = "bridge"
```

### 4. 启动智能体

#### 启动所有智能体
```bash
./start_up.sh
```

#### 启动指定智能体
```bash
./start_up.sh copaw2
```

### 5. 停止智能体

#### 停止所有智能体
```bash
./stop.sh
```

#### 停止指定智能体
```bash
./stop.sh copaw2
```

## 详细使用方法

### 配置说明

#### config.toml 参数

| 参数 | 描述 | 示例值 |
|------|------|--------|
| `IMAGE` | 容器镜像地址 | `swr.cn-north-4.myhuaweicloud.com/ddn-k8s/docker.io/agentscope/copaw:v0.0.7-linuxarm64` |
| `CONTAINER_NAME` | 容器名称 | `copaw`, `copaw2`, `copaw3` |
| `PORT` | 端口映射 | `8088`, `8089`, `8090` |
| `NETWORK_MODE` | 网络模式 | `host` 或 `bridge` |

#### 网络模式说明

- **host 模式**：容器使用主机网络，性能更好，但端口冲突风险较高
- **bridge 模式**：容器使用桥接网络，更安全，适合多实例部署

### 管理命令

#### 查看所有容器状态
```bash
docker ps -a | grep copaw
```

#### 查看容器日志
```bash
docker logs copaw
```

#### 进入容器
```bash
docker exec -it copaw bash
```

#### 查看端口映射
```bash
netstat -tlnp | grep 8088
```

### 项目结构

```
MutiPaw/
├── config.toml          # 配置文件
├── docker-compose.yml   # Docker 编排文件
├── mutipaw.py          # 多智能体管理核心脚本
├── start_up.sh         # 启动脚本
├── stop.sh             # 停止脚本
├── requirements.txt    # Python 依赖
├── README.md          # 项目文档
└── .venv/             # Python 虚拟环境
```

#### 文件说明

- **`config.toml`**: 配置智能体参数，支持多个实例定义
- **`mutipaw.py`**: 核心管理脚本，支持批量和单个容器操作
- **`start_up.sh`**: 启动入口，自动创建虚拟环境并安装依赖
- **`stop.sh`**: 停止脚本，支持停止单个或全部容器
- **`docker-compose.yml`**: Docker 编排文件，支持动态配置

### 使用场景示例

#### 场景1：部署3个智能体

1. 配置 `config.toml` 定义3个实例
2. 运行 `./start_up.sh` 启动全部
3. 访问：
   - copaw: http://localhost:8088
   - copaw2: http://localhost:8089
   - copaw3: http://localhost:8090

#### 场景2：调试单个智能体

1. 停止所有容器：`./stop.sh`
2. 启动单个容器：`./start_up.sh copaw2`
3. 查看日志：`docker logs copaw2`

#### 场景3：动态调整配置

1. 修改 `config.toml` 添加新实例
2. 重新运行 `./start_up.sh`
3. 新实例将自动创建

## 后续计划

- [x] 实现精细化容器管理（单个启动/停止）
- [x] 支持网络模式配置
- [ ] 提供更多预设的智能体角色模板
- [ ] 优化多智能体之间的通信与协同逻辑
- [ ] 添加健康检查和自动恢复功能
- [ ] 支持动态配置热加载

---

## 致谢

感谢 [CoPaw](https://github.com/agentscope-ai/CoPaw) 团队提供的优秀框架支持。
