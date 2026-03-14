#!/usr/bin/env python3
"""
MutiPaw 多智能体状态监控
提供实时监控、健康检查、状态展示功能
"""

import os
import time
import json
import docker
import threading
from datetime import datetime
from typing import Dict, List, Optional
from flask import Flask, render_template, jsonify
from docker.errors import DockerException, NotFound


class MutiPawMonitor:
    """MutiPaw 监控器"""
    
    def __init__(self, config_path: str = "config.toml"):
        self.config_path = config_path
        self.docker_client = docker.from_env()
        self.monitoring_data = {}
        self.monitoring_thread = None
        self.is_monitoring = False
        
    def read_config(self) -> Dict:
        """读取配置文件"""
        try:
            import pytomlpp
            with open(self.config_path, "r", encoding="utf-8") as f:
                return pytomlpp.loads(f.read())
        except Exception as e:
            print(f"❌ 读取配置失败: {e}")
            return {}
    
    def get_container_info(self, container_name: str) -> Dict:
        """获取单个容器信息"""
        try:
            container = self.docker_client.containers.get(container_name)
            stats = container.stats(stream=False)
            
            # 计算CPU使用率
            cpu_delta = stats['cpu_stats']['cpu_usage']['total_usage'] - stats['precpu_stats']['cpu_usage']['total_usage']
            system_delta = stats['cpu_stats']['system_cpu_usage'] - stats['precpu_stats']['system_cpu_usage']
            cpu_percent = (cpu_delta / system_delta) * 100 if system_delta > 0 else 0
            
            # 计算内存使用率
            memory_usage = stats['memory_stats']['usage']
            memory_limit = stats['memory_stats']['limit']
            memory_percent = (memory_usage / memory_limit) * 100 if memory_limit > 0 else 0
            
            return {
                'id': container.id[:12],
                'name': container.name,
                'status': container.status,
                'state': container.attrs['State'],
                'created': container.attrs['Created'],
                'cpu_percent': round(cpu_percent, 2),
                'memory_usage': memory_usage,
                'memory_limit': memory_limit,
                'memory_percent': round(memory_percent, 2),
                'network_rx': stats['networks']['eth0']['rx_bytes'] if 'networks' in stats else 0,
                'network_tx': stats['networks']['eth0']['tx_bytes'] if 'networks' in stats else 0,
                'last_updated': datetime.now().isoformat()
            }
            
        except NotFound:
            return {
                'name': container_name,
                'status': 'not_found',
                'error': '容器不存在',
                'last_updated': datetime.now().isoformat()
            }
        except DockerException as e:
            return {
                'name': container_name,
                'status': 'error',
                'error': str(e),
                'last_updated': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'name': container_name,
                'status': 'unknown',
                'error': str(e),
                'last_updated': datetime.now().isoformat()
            }
    
    def get_all_containers_info(self) -> Dict:
        """获取所有容器信息"""
        config = self.read_config()
        if not config:
            return {}
        
        paws_list = config.get("mutipaws", [])
        containers_info = []
        
        for paw in paws_list:
            container_name = paw.get("CONTAINER_NAME", "")
            if container_name:
                info = self.get_container_info(container_name)
                info['port'] = paw.get("PORT", "")
                info['network_mode'] = paw.get("NETWORK_MODE", "bridge")
                containers_info.append(info)
        
        return {
            'containers': containers_info,
            'total_count': len(containers_info),
            'running_count': len([c for c in containers_info if c.get('status') == 'running']),
            'stopped_count': len([c for c in containers_info if c.get('status') == 'exited']),
            'error_count': len([c for c in containers_info if c.get('status') in ['error', 'not_found', 'unknown']]),
            'last_updated': datetime.now().isoformat()
        }
    
    def start_monitoring(self, interval: int = 5):
        """启动监控"""
        if self.is_monitoring:
            return
        
        self.is_monitoring = True
        
        def monitor_loop():
            while self.is_monitoring:
                try:
                    self.monitoring_data = self.get_all_containers_info()
                    time.sleep(interval)
                except Exception as e:
                    print(f"❌ 监控循环错误: {e}")
                    time.sleep(interval)
        
        self.monitoring_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitoring_thread.start()
        print("✅ 监控已启动")
    
    def stop_monitoring(self):
        """停止监控"""
        self.is_monitoring = False
        if self.monitoring_thread:
            self.monitoring_thread.join(timeout=2)
        print("🛑 监控已停止")
    
    def get_status(self) -> Dict:
        """获取当前状态"""
        return self.monitoring_data


# Flask 应用
app = Flask(__name__,
            template_folder='templates',
            static_folder='static')
app.config['SECRET_KEY'] = 'mutipaw-monitor-secret-key'

# 静态资源路由
@app.route('/monitoring/static/<path:filename>')
def static_files(filename):
    """提供静态资源文件"""
    return app.send_static_file(filename)

monitor = MutiPawMonitor()

@app.route('/')
def index():
    """监控主页面"""
    return render_template('monitor.html')

@app.route('/api/status')
def api_status():
    """状态API"""
    return jsonify(monitor.get_status())

@app.route('/api/health')
def api_health():
    """健康检查API"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'monitoring': monitor.is_monitoring
    })

@app.route('/api/start_monitoring')
def start_monitoring():
    """启动监控API"""
    monitor.start_monitoring()
    return jsonify({'status': 'started'})

@app.route('/api/stop_monitoring')
def stop_monitoring():
    """停止监控API"""
    monitor.stop_monitoring()
    return jsonify({'status': 'stopped'})

if __name__ == '__main__':
    # 启动监控
    monitor.start_monitoring()
    
    # 启动Web服务
    print("🚀 启动 MutiPaw 监控服务...")
    print("🌐 访问地址: http://localhost:8090")
    app.run(host='0.0.0.0', port=8090, debug=False)