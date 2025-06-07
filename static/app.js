// Windows紧急响应系统 - 前端JavaScript

class WindowsEmergencyApp {
    constructor() {
        this.currentUser = null;
        this.currentResults = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.checkAuthStatus();
    }

    setupEventListeners() {
        // 登录表单
        document.getElementById('loginForm').addEventListener('submit', (e) => {
            e.preventDefault();
            this.login();
        });

        // 文件上传
        const fileInput = document.getElementById('fileInput');
        const uploadArea = document.getElementById('uploadArea');

        fileInput.addEventListener('change', (e) => {
            this.handleFileSelect(e.target.files[0]);
        });

        // 拖拽上传
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });

        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });

        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.handleFileSelect(files[0]);
            }
        });

        // 搜索功能
        document.getElementById('guideSearch').addEventListener('input', (e) => {
            this.searchGuide(e.target.value);
        });

        // 标签切换事件
        document.querySelectorAll('[data-bs-toggle="tab"]').forEach(tab => {
            tab.addEventListener('shown.bs.tab', (e) => {
                const target = e.target.getAttribute('data-bs-target');
                if (target === '#guide') {
                    this.loadGuideCategories();
                } else if (target === '#checklist') {
                    this.loadChecklist();
                } else if (target === '#stats') {
                    this.loadStats();
                }
            });
        });
    }

    checkAuthStatus() {
        // 检查是否已登录
        fetch('/api/stats')
            .then(response => {
                if (response.ok) {
                    this.showMainInterface();
                } else {
                    this.showLoginForm();
                }
            })
            .catch(() => {
                this.showLoginForm();
            });
    }

    async login() {
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        try {
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password })
            });

            const data = await response.json();

            if (data.success) {
                this.currentUser = data;
                this.showMainInterface();
                this.showAlert('登录成功', 'success');
            } else {
                this.showAlert('登录失败: ' + data.error, 'danger');
            }
        } catch (error) {
            this.showAlert('登录失败: ' + error.message, 'danger');
        }
    }

    async logout() {
        try {
            await fetch('/api/logout', { method: 'POST' });
            this.currentUser = null;
            this.showLoginForm();
            this.showAlert('已退出登录', 'info');
        } catch (error) {
            console.error('Logout error:', error);
        }
    }

    showLoginForm() {
        document.getElementById('loginContainer').classList.remove('hidden');
        document.getElementById('mainContainer').classList.add('hidden');
    }

    showMainInterface() {
        document.getElementById('loginContainer').classList.add('hidden');
        document.getElementById('mainContainer').classList.remove('hidden');
        
        if (this.currentUser) {
            document.getElementById('userInfo').textContent = 
                `欢迎, ${this.currentUser.username} (${this.currentUser.permissions.join(', ')})`;
        }
    }

    handleFileSelect(file) {
        if (!file) return;

        const allowedTypes = ['text/plain', 'application/json', 'text/csv', 'application/xml'];
        const maxSize = 50 * 1024 * 1024; // 50MB

        if (file.size > maxSize) {
            this.showAlert('文件大小超过50MB限制', 'danger');
            return;
        }

        // 显示文件信息
        document.getElementById('fileName').textContent = file.name;
        document.getElementById('fileInfo').classList.remove('hidden');
        
        // 上传文件
        this.uploadFile(file);
    }

    async uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/api/upload', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (data.success) {
                this.currentFilename = data.filename;
                this.showAlert('文件上传成功', 'success');
            } else {
                this.showAlert('文件上传失败: ' + data.error, 'danger');
            }
        } catch (error) {
            this.showAlert('文件上传失败: ' + error.message, 'danger');
        }
    }

    async analyzeFile() {
        if (!this.currentFilename) {
            this.showAlert('请先上传文件', 'warning');
            return;
        }

        // 显示加载动画
        document.getElementById('loadingSpinner').style.display = 'block';
        document.getElementById('analysisResults').classList.add('hidden');

        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ filename: this.currentFilename })
            });

            const data = await response.json();

            if (data.error) {
                this.showAlert('分析失败: ' + data.error, 'danger');
            } else {
                this.currentResults = data;
                this.displayResults(data);
                this.showAlert('分析完成', 'success');
            }
        } catch (error) {
            this.showAlert('分析失败: ' + error.message, 'danger');
        } finally {
            document.getElementById('loadingSpinner').style.display = 'none';
        }
    }

    displayResults(results) {
        // 显示统计卡片
        this.displayStatsCards(results.summary);
        
        // 显示攻击统计
        if (results.attack_statistics) {
            this.displayAttackStats(results.attack_statistics);
        }
        
        // 显示详细分析
        if (results.detailed_analysis) {
            this.displayDetailedAnalysis(results.detailed_analysis);
        }
        
        // 显示告警
        this.displayAlerts(results);
        
        // 显示结果区域
        document.getElementById('analysisResults').classList.remove('hidden');
    }

    displayStatsCards(summary) {
        const container = document.getElementById('statsCards');
        container.innerHTML = '';

        const stats = [
            {
                title: '风险等级',
                value: summary.overall_risk_level,
                class: `risk-${summary.overall_risk_level.toLowerCase()}`,
                icon: 'fas fa-shield-alt'
            },
            {
                title: '风险评分',
                value: summary.risk_score + '/100',
                class: summary.risk_score > 70 ? 'risk-high' : summary.risk_score > 40 ? 'risk-medium' : 'risk-low',
                icon: 'fas fa-tachometer-alt'
            },
            {
                title: '严重告警',
                value: summary.critical_count || 0,
                class: 'risk-critical',
                icon: 'fas fa-exclamation-circle'
            },
            {
                title: '高危告警',
                value: summary.high_risk_count,
                class: 'risk-high',
                icon: 'fas fa-exclamation-triangle'
            },
            {
                title: '中危告警',
                value: summary.medium_risk_count,
                class: 'risk-medium',
                icon: 'fas fa-exclamation'
            },
            {
                title: '低危告警',
                value: summary.low_risk_count,
                class: 'risk-low',
                icon: 'fas fa-info-circle'
            }
        ];

        stats.forEach(stat => {
            const card = document.createElement('div');
            card.className = 'col-md-2';
            card.innerHTML = `
                <div class="stat-card">
                    <i class="${stat.icon} fa-2x ${stat.class}"></i>
                    <div class="stat-number ${stat.class}">${stat.value}</div>
                    <div class="stat-label">${stat.title}</div>
                </div>
            `;
            container.appendChild(card);
        });
    }

    displayAttackStats(attackStats) {
        const container = document.getElementById('attackStatsContainer');
        if (!container) return;
        
        container.innerHTML = `
            <div class="attack-stats-section">
                <h5><i class="fas fa-crosshairs"></i> 攻击统计分析</h5>
                <div class="row">
                    <div class="col-md-2">
                        <div class="stat-card attack-stat">
                            <div class="stat-number text-danger">${attackStats.total_attacks}</div>
                            <div class="stat-label">总攻击次数</div>
                        </div>
                    </div>
                    <div class="col-md-2">
                        <div class="stat-card attack-stat">
                            <div class="stat-number text-warning">${attackStats.failed_logins}</div>
                            <div class="stat-label">失败登录</div>
                        </div>
                    </div>
                    <div class="col-md-2">
                        <div class="stat-card attack-stat">
                            <div class="stat-number text-danger">${attackStats.privilege_escalations}</div>
                            <div class="stat-label">权限提升</div>
                        </div>
                    </div>
                    <div class="col-md-2">
                        <div class="stat-card attack-stat">
                            <div class="stat-number text-danger">${attackStats.malware_detections}</div>
                            <div class="stat-label">恶意软件</div>
                        </div>
                    </div>
                    <div class="col-md-2">
                        <div class="stat-card attack-stat">
                            <div class="stat-number text-warning">${attackStats.suspicious_processes}</div>
                            <div class="stat-label">可疑进程</div>
                        </div>
                    </div>
                    <div class="col-md-2">
                        <div class="stat-card attack-stat">
                            <div class="stat-number text-info">${attackStats.network_anomalies}</div>
                            <div class="stat-label">网络异常</div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    displayDetailedAnalysis(detailedAnalysis) {
        const container = document.getElementById('detailedAnalysisContainer');
        if (!container) return;
        
        let html = `
            <div class="detailed-analysis-section">
                <h5><i class="fas fa-microscope"></i> 详细分析结果</h5>
                <div class="analysis-tabs">
                    <button class="tab-button active" onclick="showAnalysisTab('processes')">
                        <i class="fas fa-cogs"></i> 进程分析
                    </button>
                    <button class="tab-button" onclick="showAnalysisTab('network')">
                        <i class="fas fa-network-wired"></i> 网络分析
                    </button>
                    <button class="tab-button" onclick="showAnalysisTab('users')">
                        <i class="fas fa-users"></i> 用户分析
                    </button>
                    <button class="tab-button" onclick="showAnalysisTab('services')">
                        <i class="fas fa-server"></i> 服务分析
                    </button>
                    <button class="tab-button" onclick="showAnalysisTab('events')">
                        <i class="fas fa-list-alt"></i> 事件分析
                    </button>
                </div>
                
                <div id="processes-tab" class="tab-content active">
                    ${displayProcessAnalysis(detailedAnalysis.processes)}
                </div>
                
                <div id="network-tab" class="tab-content">
                    ${displayNetworkAnalysis(detailedAnalysis.network_connections)}
                </div>
                
                <div id="users-tab" class="tab-content">
                    ${displayUserAnalysis(detailedAnalysis.users)}
                </div>
                
                <div id="services-tab" class="tab-content">
                    ${displayServiceAnalysis(detailedAnalysis.services)}
                </div>
                
                <div id="events-tab" class="tab-content">
                    ${displayEventAnalysis(detailedAnalysis.events)}
                </div>
            </div>
        `;
        
        container.innerHTML = html;
    }

    displayAlerts(results) {
        const container = document.getElementById('alertsContainer');
        container.innerHTML = '';

        const levels = ['critical', 'high', 'medium', 'low'];
        const levelNames = {
            'critical': '严重',
            'high': '高危',
            'medium': '中危',
            'low': '低危'
        };

        levels.forEach(level => {
            const alerts = results[level] || [];
            if (alerts.length > 0) {
                const section = document.createElement('div');
                section.innerHTML = `
                    <h5 class="mt-4 mb-3">
                        <span class="badge bg-${level === 'critical' ? 'dark' : level === 'high' ? 'danger' : level === 'medium' ? 'warning' : 'info'}">
                            ${levelNames[level]} (${alerts.length})
                        </span>
                    </h5>
                `;

                alerts.forEach(alert => {
                    const alertCard = document.createElement('div');
                    alertCard.className = `alert-card alert-${level}`;
                    alertCard.innerHTML = `
                        <div class="card-body">
                            <h6 class="card-title">
                                <i class="fas fa-exclamation-triangle"></i> ${alert.name}
                            </h6>
                            <p class="card-text">${alert.description}</p>
                            <div class="alert alert-info">
                                <strong>建议措施:</strong> ${alert.recommendation}
                            </div>
                            <small class="text-muted">
                                规则ID: ${alert.rule_id} | 匹配次数: ${alert.count}
                            </small>
                        </div>
                    `;
                    section.appendChild(alertCard);
                });

                container.appendChild(section);
            }
        });

        if (container.innerHTML === '') {
            container.innerHTML = `
                <div class="alert alert-success">
                    <i class="fas fa-check-circle"></i> 未发现安全威胁，系统状态良好。
                </div>
            `;
        }
    }

    async exportResults(format) {
        if (!this.currentResults) {
            this.showAlert('没有可导出的结果', 'warning');
            return;
        }

        try {
            const response = await fetch('/api/export', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    results: this.currentResults,
                    format: format
                })
            });

            const data = await response.json();

            if (data.success) {
                // 创建下载链接
                const link = document.createElement('a');
                link.href = data.download_url;
                link.download = '';
                link.click();
                this.showAlert('导出成功', 'success');
            } else {
                this.showAlert('导出失败: ' + data.error, 'danger');
            }
        } catch (error) {
            this.showAlert('导出失败: ' + error.message, 'danger');
        }
    }

    async loadGuideCategories() {
        try {
            const response = await fetch('/api/guide/categories');
            const categories = await response.json();

            const container = document.getElementById('guideCategories');
            container.innerHTML = '';

            Object.entries(categories).forEach(([key, name]) => {
                const item = document.createElement('a');
                item.className = 'list-group-item list-group-item-action';
                item.href = '#';
                item.textContent = name;
                item.onclick = () => this.loadGuideCategory(key);
                container.appendChild(item);
            });
        } catch (error) {
            console.error('Error loading guide categories:', error);
        }
    }

    async loadGuideCategory(category) {
        try {
            const response = await fetch(`/api/guide/${category}`);
            const data = await response.json();

            this.displayGuideCategory(data);
        } catch (error) {
            console.error('Error loading guide category:', error);
        }
    }

    displayGuideCategory(data) {
        const container = document.getElementById('guideContent');
        
        let html = `
            <div class="guide-card">
                <h4><i class="fas fa-terminal"></i> ${data.name}</h4>
                <p class="text-muted">${data.description}</p>
        `;

        if (data.note) {
            html += `<div class="alert alert-warning"><strong>注意:</strong> ${data.note}</div>`;
        }

        if (data.commands) {
            data.commands.forEach(cmd => {
                html += `
                    <div class="command-item">
                        <h6><i class="fas fa-code"></i> ${cmd.command}</h6>
                        <p>${cmd.description}</p>
                        
                        <div class="row">
                            <div class="col-md-6">
                                <strong>用法:</strong>
                                <div class="command-code">${cmd.usage}</div>
                            </div>
                            <div class="col-md-6">
                                <strong>示例:</strong>
                                <div class="command-code">${cmd.example}</div>
                            </div>
                        </div>
                `;

                if (cmd.parameters) {
                    html += '<div class="mt-3"><strong>参数说明:</strong><ul>';
                    Object.entries(cmd.parameters).forEach(([param, desc]) => {
                        html += `<li><code>${param}</code>: ${desc}</li>`;
                    });
                    html += '</ul></div>';
                }

                if (cmd.output_example) {
                    html += `
                        <div class="mt-3">
                            <strong>输出示例:</strong>
                            <div class="command-code">${cmd.output_example}</div>
                        </div>
                    `;
                }

                if (cmd.troubleshooting) {
                    html += `
                        <div class="alert alert-info mt-3">
                            <strong>故障排除:</strong> ${cmd.troubleshooting}
                        </div>
                    `;
                }

                if (cmd.when_to_use) {
                    html += `
                        <div class="alert alert-warning mt-3">
                            <strong>使用场景:</strong> ${cmd.when_to_use}
                        </div>
                    `;
                }

                if (cmd.cmd_alternative) {
                    html += `
                        <div class="alert alert-secondary mt-3">
                            <strong>CMD替代:</strong> ${cmd.cmd_alternative}
                        </div>
                    `;
                }

                html += '</div>';
            });
        }

        html += '</div>';
        container.innerHTML = html;
    }

    async searchGuide(keyword) {
        if (!keyword.trim()) {
            return;
        }

        try {
            const response = await fetch(`/api/guide/search?q=${encodeURIComponent(keyword)}`);
            const results = await response.json();

            this.displaySearchResults(results);
        } catch (error) {
            console.error('Error searching guide:', error);
        }
    }

    displaySearchResults(results) {
        const container = document.getElementById('guideContent');
        
        if (results.length === 0) {
            container.innerHTML = `
                <div class="guide-card text-center">
                    <i class="fas fa-search fa-2x text-muted"></i>
                    <p class="mt-3 text-muted">未找到匹配的命令</p>
                </div>
            `;
            return;
        }

        let html = `
            <div class="guide-card">
                <h4><i class="fas fa-search"></i> 搜索结果 (${results.length})</h4>
        `;

        results.forEach(result => {
            const cmd = result.command;
            html += `
                <div class="command-item">
                    <h6><i class="fas fa-code"></i> ${cmd.command}</h6>
                    <p>${cmd.description}</p>
                    <small class="text-muted">分类: ${result.category}</small>
                </div>
            `;
        });

        html += '</div>';
        container.innerHTML = html;
    }

    async loadChecklist() {
        try {
            const response = await fetch('/api/guide/checklist');
            const checklist = await response.json();

            this.displayChecklist(checklist);
        } catch (error) {
            console.error('Error loading checklist:', error);
        }
    }

    displayChecklist(checklist) {
        const container = document.getElementById('checklistContent');
        let html = '';

        Object.entries(checklist).forEach(([category, items]) => {
            const categoryNames = {
                'immediate_response': '立即响应',
                'data_collection': '数据收集',
                'analysis_steps': '分析步骤',
                'containment': '威胁遏制',
                'recovery': '系统恢复'
            };

            html += `
                <div class="guide-card">
                    <h5><i class="fas fa-clipboard-check"></i> ${categoryNames[category] || category}</h5>
                    <ul class="list-group list-group-flush">
            `;

            items.forEach(item => {
                html += `<li class="list-group-item">${item}</li>`;
            });

            html += '</ul></div>';
        });

        container.innerHTML = html;
    }

    async loadStats() {
        try {
            const response = await fetch('/api/stats');
            const stats = await response.json();

            this.displayStats(stats);
        } catch (error) {
            console.error('Error loading stats:', error);
        }
    }

    displayStats(stats) {
        const container = document.getElementById('systemStats');
        
        let html = `
            <h5><i class="fas fa-chart-line"></i> 系统使用统计</h5>
            <div class="row">
                <div class="col-md-6">
                    <p><strong>总分析次数:</strong> ${stats.total_analyses || 0}</p>
                    <p><strong>总告警数:</strong> ${stats.total_alerts || 0}</p>
                </div>
                <div class="col-md-6">
                    <p><strong>平均告警/分析:</strong> ${stats.total_analyses ? (stats.total_alerts / stats.total_analyses).toFixed(2) : 0}</p>
                    <p><strong>系统状态:</strong> <span class="text-success">正常运行</span></p>
                </div>
            </div>
        `;

        container.innerHTML = html;
    }

    showAlert(message, type) {
        // 创建临时提示
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        alert.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(alert);
        
        // 3秒后自动消失
        setTimeout(() => {
            if (alert.parentNode) {
                alert.parentNode.removeChild(alert);
            }
        }, 3000);
    }
}

// 全局函数
function logout() {
    app.logout();
}

function analyzeFile() {
    app.analyzeFile();
}

function exportResults(format) {
    app.exportResults(format);
}

// 详细分析相关函数
function showAnalysisTab(tabName) {
    // 隐藏所有标签页内容
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // 移除所有按钮的active类
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // 显示选中的标签页
    document.getElementById(tabName + '-tab').classList.add('active');
    event.target.classList.add('active');
}

function displayProcessAnalysis(processes) {
    let html = '<div class="process-analysis">';
    html += `<h6>📊 进程统计</h6>`;
    html += `<div class="stats-row">`;
    html += `<span class="stat-badge">总进程: ${processes.total_count}</span>`;
    html += `<span class="stat-badge">可疑进程: ${processes.suspicious_processes.length}</span>`;
    html += `<span class="stat-badge">高内存进程: ${processes.high_memory_processes.length}</span>`;
    html += `<span class="stat-badge">系统进程: ${processes.system_processes.length}</span>`;
    html += `</div>`;
    
    if (processes.suspicious_processes.length > 0) {
        html += '<h6 class="mt-3">🚨 可疑进程</h6>';
        html += '<div class="table-responsive"><table class="table table-sm">';
        html += '<thead><tr><th>进程名</th><th>PID</th><th>内存使用</th><th>会话</th></tr></thead><tbody>';
        processes.suspicious_processes.forEach(proc => {
            html += `<tr><td>${proc.name}</td><td>${proc.pid}</td><td>${proc.memory_usage}</td><td>${proc.session}</td></tr>`;
        });
        html += '</tbody></table></div>';
    }
    
    if (processes.high_memory_processes.length > 0) {
        html += '<h6 class="mt-3">💾 高内存使用进程</h6>';
        html += '<div class="table-responsive"><table class="table table-sm">';
        html += '<thead><tr><th>进程名</th><th>PID</th><th>内存使用</th><th>内存(MB)</th></tr></thead><tbody>';
        processes.high_memory_processes.slice(0, 10).forEach(proc => {
            html += `<tr><td>${proc.name}</td><td>${proc.pid}</td><td>${proc.memory_usage}</td><td>${proc.memory_mb.toFixed(1)}</td></tr>`;
        });
        html += '</tbody></table></div>';
    }
    
    html += '</div>';
    return html;
}

function displayNetworkAnalysis(network) {
    let html = '<div class="network-analysis">';
    html += `<h6>🌐 网络统计</h6>`;
    html += `<div class="stats-row">`;
    html += `<span class="stat-badge">总连接: ${network.total_connections}</span>`;
    html += `<span class="stat-badge">已建立: ${network.established_connections.length}</span>`;
    html += `<span class="stat-badge">监听端口: ${network.listening_ports.length}</span>`;
    html += `<span class="stat-badge">外部IP: ${network.external_ips.length}</span>`;
    html += `<span class="stat-badge">可疑连接: ${network.suspicious_connections.length}</span>`;
    html += `</div>`;
    
    if (network.external_ips.length > 0) {
        html += '<h6 class="mt-3">🌍 外部IP连接</h6>';
        html += '<div class="ip-list">';
        network.external_ips.slice(0, 20).forEach(ip => {
            html += `<span class="ip-badge">${ip}</span>`;
        });
        html += '</div>';
    }
    
    if (network.suspicious_connections.length > 0) {
        html += '<h6 class="mt-3">⚠️ 可疑连接</h6>';
        html += '<div class="table-responsive"><table class="table table-sm">';
        html += '<thead><tr><th>协议</th><th>本地地址</th><th>远程地址</th><th>状态</th></tr></thead><tbody>';
        network.suspicious_connections.forEach(conn => {
            html += `<tr><td>${conn.protocol}</td><td>${conn.local_address}</td><td>${conn.foreign_address}</td><td>${conn.state}</td></tr>`;
        });
        html += '</tbody></table></div>';
    }
    
    if (Object.keys(network.port_statistics).length > 0) {
        html += '<h6 class="mt-3">📊 端口统计</h6>';
        html += '<div class="port-stats">';
        Object.entries(network.port_statistics).slice(0, 10).forEach(([port, count]) => {
            html += `<span class="port-badge">端口${port}: ${count}次</span>`;
        });
        html += '</div>';
    }
    
    html += '</div>';
    return html;
}

function displayUserAnalysis(users) {
    let html = '<div class="user-analysis">';
    html += `<h6>👥 用户统计</h6>`;
    html += `<div class="stats-row">`;
    html += `<span class="stat-badge">总用户: ${users.total_users}</span>`;
    html += `<span class="stat-badge">管理员: ${users.admin_users.length}</span>`;
    html += `<span class="stat-badge">普通用户: ${users.regular_users.length}</span>`;
    html += `<span class="stat-badge">隐藏用户: ${users.hidden_users.length}</span>`;
    html += `<span class="stat-badge">禁用用户: ${users.disabled_users.length}</span>`;
    html += `<span class="stat-badge">可疑用户: ${users.suspicious_users.length}</span>`;
    html += `</div>`;
    
    if (users.admin_users.length > 0) {
        html += '<h6 class="mt-3">👑 管理员用户</h6>';
        html += '<div class="user-list">';
        users.admin_users.forEach(user => {
            html += `<div class="user-item">`;
            html += `<strong>${user.username}</strong>`;
            if (user.groups && user.groups.length > 0) {
                html += ` <small>(${user.groups.join(', ')})</small>`;
            }
            html += `</div>`;
        });
        html += '</div>';
    }
    
    if (users.suspicious_users.length > 0) {
        html += '<h6 class="mt-3">⚠️ 可疑用户</h6>';
        html += '<div class="user-list">';
        users.suspicious_users.forEach(user => {
            html += `<div class="user-item suspicious">`;
            html += `<strong>${user.username}</strong>`;
            if (user.is_admin) html += ` <span class="badge bg-danger">管理员</span>`;
            if (user.is_hidden) html += ` <span class="badge bg-warning">隐藏</span>`;
            if (user.is_disabled) html += ` <span class="badge bg-secondary">禁用</span>`;
            html += `</div>`;
        });
        html += '</div>';
    }
    
    if (users.hidden_users.length > 0) {
        html += '<h6 class="mt-3">🔍 隐藏用户</h6>';
        html += '<div class="user-list">';
        users.hidden_users.forEach(user => {
            html += `<div class="user-item hidden">`;
            html += `<strong>${user.username}</strong>`;
            if (user.is_admin) html += ` <span class="badge bg-danger">管理员</span>`;
            html += `</div>`;
        });
        html += '</div>';
    }
    
    html += '</div>';
    return html;
}

function displayServiceAnalysis(services) {
    let html = '<div class="service-analysis">';
    html += `<h6>⚙️ 服务统计</h6>`;
    html += `<div class="stats-row">`;
    html += `<span class="stat-badge">总服务: ${services.total_services}</span>`;
    html += `<span class="stat-badge">运行中: ${services.running_services.length}</span>`;
    html += `<span class="stat-badge">已停止: ${services.stopped_services.length}</span>`;
    html += `<span class="stat-badge">自动启动: ${services.auto_start_services.length}</span>`;
    html += `<span class="stat-badge">可疑服务: ${services.suspicious_services.length}</span>`;
    html += `</div>`;
    
    if (services.suspicious_services.length > 0) {
        html += '<h6 class="mt-3">⚠️ 可疑服务</h6>';
        html += '<div class="table-responsive"><table class="table table-sm">';
        html += '<thead><tr><th>服务名</th><th>状态</th><th>启动类型</th></tr></thead><tbody>';
        services.suspicious_services.forEach(svc => {
            html += `<tr><td>${svc.name}</td><td>${svc.state}</td><td>${svc.start_type}</td></tr>`;
        });
        html += '</tbody></table></div>';
    }
    
    if (services.running_services.length > 0) {
        html += '<h6 class="mt-3">▶️ 运行中的服务 (前20个)</h6>';
        html += '<div class="service-list">';
        services.running_services.slice(0, 20).forEach(svc => {
            html += `<span class="service-badge running">${svc.name}</span>`;
        });
        html += '</div>';
    }
    
    html += '</div>';
    return html;
}

function displayEventAnalysis(events) {
    let html = '<div class="event-analysis">';
    html += `<h6>📋 事件统计</h6>`;
    html += `<div class="stats-row">`;
    html += `<span class="stat-badge">总事件: ${events.total_events}</span>`;
    html += `<span class="stat-badge">失败登录: ${events.failed_logins.length}</span>`;
    html += `<span class="stat-badge">成功登录: ${events.successful_logins.length}</span>`;
    html += `<span class="stat-badge">权限提升: ${events.privilege_escalations.length}</span>`;
    html += `</div>`;
    
    if (events.details.length > 0) {
        html += '<h6 class="mt-3">📊 事件详情</h6>';
        html += '<div class="table-responsive"><table class="table table-sm">';
        html += '<thead><tr><th>事件ID</th><th>类型</th><th>次数</th><th>描述</th></tr></thead><tbody>';
        events.details.forEach(event => {
            html += `<tr><td>${event.event_id}</td><td>${event.type}</td><td>${event.count}</td><td>${event.description}</td></tr>`;
        });
        html += '</tbody></table></div>';
    }
    
    html += '</div>';
    return html;
}

// 初始化应用
const app = new WindowsEmergencyApp();