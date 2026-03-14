// MutiPaw 监控面板工具函数

/**
 * 格式化时间戳
 * @param {string} timestamp - ISO 时间戳字符串
 * @returns {string} - 格式化后的时间字符串
 */
function formatTimestamp(timestamp) {
    if (!timestamp) return '--';
    try {
        const date = new Date(timestamp);
        return date.toLocaleString('zh-CN');
    } catch (e) {
        return '--';
    }
}

/**
 * 格式化字节数
 * @param {number} bytes - 字节数
 * @returns {string} - 格式化后的字节数
 */
function formatBytes(bytes) {
    if (!bytes || isNaN(bytes)) return '0 B';

    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(1024));

    return `${(bytes / Math.pow(1024, i)).toFixed(2)} ${sizes[i]}`;
}

/**
 * 格式化百分比
 * @param {number} percent - 百分比数值
 * @returns {string} - 格式化后的百分比字符串
 */
function formatPercent(percent) {
    if (!percent || isNaN(percent)) return '0.0%';
    return `${parseFloat(percent).toFixed(1)}%`;
}

/**
 * 获取状态图标
 * @param {string} status - 容器状态
 * @returns {string} - HTML 图标字符串
 */
function getStatusIcon(status) {
    switch (status) {
        case 'running':
            return '🟢';
        case 'exited':
            return '🔴';
        case 'error':
        case 'unknown':
            return '❌';
        default:
            return '❓';
    }
}

/**
 * 获取状态文本
 * @param {string} status - 容器状态
 * @returns {string} - 状态对应的中文文本
 */
function getStatusText(status) {
    switch (status) {
        case 'running': return '运行中';
        case 'exited': return '已停止';
        case 'restarting': return '重启中';
        case 'paused': return '暂停';
        case 'error':
        case 'unknown': return '异常';
        case 'created': return '已创建';
        case 'removing': return '移除中';
        default: return status;
    }
}

/**
 * 显示消息提示
 * @param {string} message - 消息内容
 * @param {string} type - 消息类型 ('success', 'error', 'warning', 'info')
 * @param {number} duration - 显示时长（毫秒）
 */
function showToast(message, type = 'info', duration = 3000) {
    // 创建提示元素
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.innerHTML = `
        <div class="toast-content">
            <span class="toast-icon">${getToastIcon(type)}</span>
            <span class="toast-message">${message}</span>
        </div>
    `;

    // 添加到页面
    document.body.appendChild(toast);

    // 显示动画
    setTimeout(() => {
        toast.classList.add('show');
    }, 10);

    // 自动移除
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => {
            if (document.body.contains(toast)) {
                document.body.removeChild(toast);
            }
        }, 300);
    }, duration);
}

/**
 * 获取提示图标
 * @param {string} type - 消息类型
 * @returns {string} - 对应类型的图标
 */
function getToastIcon(type) {
    switch (type) {
        case 'success': return '✅';
        case 'error': return '❌';
        case 'warning': return '⚠️';
        case 'info': return 'ℹ️';
        default: return '📢';
    }
}

/**
 * 节流函数
 * @param {Function} func - 要节流的函数
 * @param {number} delay - 延迟时间（毫秒）
 * @returns {Function} - 节流后的函数
 */
function throttle(func, delay) {
    let timeoutId;
    return function(...args) {
        if (!timeoutId) {
            timeoutId = setTimeout(() => {
                func.apply(this, args);
                timeoutId = null;
            }, delay);
        }
    };
}

/**
 * 防抖函数
 * @param {Function} func - 要防抖的函数
 * @param {number} delay - 延迟时间（毫秒）
 * @returns {Function} - 防抖后的函数
 */
function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => {
            func.apply(this, args);
        }, delay);
    };
}

/**
 * 深拷贝对象
 * @param {any} obj - 要拷贝的对象
 * @returns {any} - 拷贝后的对象
 */
function deepClone(obj) {
    if (obj === null || typeof obj !== 'object') {
        return obj;
    }

    if (obj instanceof Date) {
        return new Date(obj.getTime());
    }

    if (obj instanceof Array) {
        return obj.map(item => deepClone(item));
    }

    if (typeof obj === 'object') {
        const clonedObj = {};
        for (let key in obj) {
            if (obj.hasOwnProperty(key)) {
                clonedObj[key] = deepClone(obj[key]);
            }
        }
        return clonedObj;
    }
}

/**
 * 生成随机ID
 * @returns {string} - 随机ID
 */
function generateId() {
    return Math.random().toString(36).substr(2, 9);
}

/**
 * 检查是否为有效的URL
 * @param {string} url - URL字符串
 * @returns {boolean} - 是否为有效URL
 */
function isValidUrl(url) {
    try {
        new URL(url);
        return true;
    } catch (e) {
        return false;
    }
}

/**
 * 格式化文件大小
 * @param {number} bytes - 字节数
 * @returns {string} - 格式化后的文件大小
 */
function formatFileSize(bytes) {
    return formatBytes(bytes);
}

/**
 * 格式化网络流量
 * @param {Object} networkStats - 网络统计对象
 * @returns {Object} - 格式化后的网络统计
 */
function formatNetworkStats(networkStats) {
    if (!networkStats) return { rx: '0 B', tx: '0 B' };

    return {
        rx: formatBytes(networkStats.rx_bytes),
        tx: formatBytes(networkStats.tx_bytes)
    };
}

export {
    formatTimestamp,
    formatBytes,
    formatPercent,
    getStatusIcon,
    getStatusText,
    showToast,
    getToastIcon,
    throttle,
    debounce,
    deepClone,
    generateId,
    isValidUrl,
    formatFileSize,
    formatNetworkStats
};