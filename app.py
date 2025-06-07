#!/usr/bin/env python3
"""
Windows紧急响应系统 - 主应用
专为Windows设计的紧急响应系统，集成文档分析、应急技巧和用户管理
"""

import os
import sys
from pathlib import Path

# 添加当前目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from enhanced_windows_analyzer import app, analyzer
from flask import render_template

# 添加主页路由
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/health')
def health_check():
    """健康检查端点"""
    return {
        'status': 'healthy',
        'service': 'Windows Emergency Response System',
        'version': '1.0.0'
    }

if __name__ == '__main__':
    print("=" * 60)
    print("🛡️  Windows紧急响应系统启动中...")
    print("=" * 60)
    print(f"📊 已加载 {len(analyzer.rules)} 条安全规则")
    print(f"📚 已加载 {len(analyzer.guide.get_all_categories())} 个命令分类")
    print("🌐 Web界面地址: http://localhost:12000")
    print("👤 测试账户: admin/admin123 或 analyst/analyst123")
    print("=" * 60)
    
    # 确保所有必要的目录存在
    for folder in ['uploads', 'logs', 'exports', 'static', 'templates']:
        os.makedirs(folder, exist_ok=True)
    
    app.run(host='0.0.0.0', port=12000, debug=False)