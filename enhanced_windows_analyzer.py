#!/usr/bin/env python3
"""
Windows紧急响应系统 - 增强版分析引擎
支持多种文档格式，自动编码检测，深度分析
"""

import os
import re
import json
import yaml
import hashlib
import datetime
import logging
import chardet
# import pandas as pd  # 暂时移除pandas依赖
from pathlib import Path
from collections import defaultdict, Counter
from flask import Flask, request, jsonify, render_template_string, send_from_directory, session
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import psutil
import csv
from io import StringIO
from windows_emergency_guide import WindowsEmergencyGuide

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/emergency_response.log'),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)
app.secret_key = 'windows_emergency_response_2024'
CORS(app, origins=["http://localhost:*", "https://*.prod-runtime.all-hands.dev"])

# 配置文件上传
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'log', 'csv', 'json', 'xml', 'evtx'}
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# 确保目录存在
for folder in ['uploads', 'logs', 'exports']:
    os.makedirs(folder, exist_ok=True)

# 简单的用户管理（生产环境应使用数据库）
USERS = {
    'admin': generate_password_hash('admin123'),
    'analyst': generate_password_hash('analyst123')
}

USER_ROLES = {
    'admin': ['read', 'write', 'execute', 'admin'],
    'analyst': ['read', 'write']
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def detect_encoding(file_path):
    """自动检测文件编码"""
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read(10000)  # 读取前10KB检测编码
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            confidence = result['confidence']
            
            logging.info(f"Detected encoding: {encoding} (confidence: {confidence:.2f})")
            
            # 如果检测置信度低，尝试常见编码
            if confidence < 0.7:
                for enc in ['utf-8', 'gbk', 'gb2312', 'utf-16', 'ascii']:
                    try:
                        with open(file_path, 'r', encoding=enc) as test_file:
                            test_file.read(1000)
                        logging.info(f"Successfully read with encoding: {enc}")
                        return enc
                    except:
                        continue
            
            return encoding or 'utf-8'
    except Exception as e:
        logging.error(f"Error detecting encoding: {str(e)}")
        return 'utf-8'

def parse_document(file_path):
    """解析不同格式的文档"""
    file_ext = Path(file_path).suffix.lower()
    
    try:
        if file_ext == '.json':
            encoding = detect_encoding(file_path)
            with open(file_path, 'r', encoding=encoding) as f:
                return json.load(f)
        
        elif file_ext == '.csv':
            encoding = detect_encoding(file_path)
            data = {}
            with open(file_path, 'r', encoding=encoding) as f:
                csv_reader = csv.DictReader(f)
                rows = list(csv_reader)
                data['csv_data'] = rows
                data['content'] = '\n'.join([str(row) for row in rows])
            return data
        
        elif file_ext in ['.txt', '.log']:
            encoding = detect_encoding(file_path)
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            
            # 尝试解析结构化内容
            parsed_data = parse_structured_text(content)
            return parsed_data
        
        else:
            # 默认按文本处理
            encoding = detect_encoding(file_path)
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            return {'content': content}
            
    except Exception as e:
        logging.error(f"Error parsing document {file_path}: {str(e)}")
        return {'content': '', 'error': str(e)}

def parse_structured_text(content):
    """解析结构化文本内容"""
    data = {'content': content}
    
    # 解析Windows应急响应报告格式
    sections = {}
    current_section = None
    current_subsection = None
    current_content = []
    
    lines = content.split('\n')
    
    for line in lines:
        line = line.strip()
        
        # 检测主要部分标题
        if line.startswith('===== ') and line.endswith(' ====='):
            if current_section and current_subsection:
                if current_section not in sections:
                    sections[current_section] = {}
                sections[current_section][current_subsection] = '\n'.join(current_content)
            
            current_section = line.replace('=', '').strip().lower().replace(' ', '_')
            current_subsection = None
            current_content = []
            
        # 检测子部分标题
        elif line.startswith('----- ') and line.endswith(' -----'):
            if current_section and current_subsection:
                if current_section not in sections:
                    sections[current_section] = {}
                sections[current_section][current_subsection] = '\n'.join(current_content)
            
            current_subsection = line.replace('-', '').strip().lower().replace(' ', '_')
            current_content = []
            
        else:
            if line:  # 忽略空行
                current_content.append(line)
    
    # 处理最后一个部分
    if current_section and current_subsection:
        if current_section not in sections:
            sections[current_section] = {}
        sections[current_section][current_subsection] = '\n'.join(current_content)
    
    data.update(sections)
    return data

class EnhancedWindowsAnalyzer:
    def __init__(self):
        self.rules = self.load_rules()
        self.guide = WindowsEmergencyGuide()
        self.analysis_stats = defaultdict(int)
        
    def load_rules(self):
        """加载规则文件"""
        rules_dir = Path(__file__).parent / 'rules'
        rules = {}
        loaded_files = 0
        
        for rule_file in rules_dir.rglob('*.yml'):
            try:
                with open(rule_file, 'r', encoding='utf-8') as f:
                    rule_data = yaml.safe_load(f)
                    if isinstance(rule_data, list):
                        for rule in rule_data:
                            if isinstance(rule, dict) and 'id' in rule:
                                rules[rule['id']] = rule
                                loaded_files += 1
                    elif isinstance(rule_data, dict) and 'id' in rule_data:
                        rules[rule_data['id']] = rule_data
                        loaded_files += 1
            except Exception as e:
                logging.error(f"Error loading rule file {rule_file}: {str(e)}")
                
        logging.info(f"Loaded {loaded_files} rules from {len(list(rules_dir.rglob('*.yml')))} files")
        return rules

    def evaluate_rule(self, rule, data):
        """评估规则"""
        try:
            if 'pattern' not in rule:
                return False
                
            pattern = re.compile(rule['pattern'], re.I if rule.get('case_insensitive', True) else 0)
            
            # 确定搜索目标
            target_section = rule.get('target_section', 'content')
            content = ''
            
            if target_section == 'content':
                content = data.get('content', '')
            elif target_section in data:
                if isinstance(data[target_section], dict):
                    content = '\n'.join([str(v) for v in data[target_section].values()])
                else:
                    content = str(data[target_section])
            else:
                # 在所有数据中搜索
                for key, value in data.items():
                    if isinstance(value, dict):
                        content += '\n'.join([str(v) for v in value.values()])
                    else:
                        content += str(value)
            
            if not content:
                return False
                
            matches = list(pattern.finditer(content))
            if matches:
                findings = []
                for match in matches:
                    findings.append({
                        'start': match.start(),
                        'end': match.end(),
                        'matched_text': match.group(0),
                        'line_number': content[:match.start()].count('\n') + 1,
                        'context': self.get_context(content, match.start(), match.end())
                    })
                
                return {
                    'rule_id': rule['id'],
                    'name': rule.get('name', rule['id']),
                    'level': rule.get('level', 'medium'),
                    'description': rule.get('description', ''),
                    'findings': findings,
                    'recommendation': rule.get('recommendation', '建议进一步调查此问题'),
                    'count': len(findings)
                }
        except Exception as e:
            logging.error(f"Rule evaluation error for {rule.get('id', 'unknown')}: {str(e)}")
        return False

    def get_context(self, content, start, end, context_size=100):
        """获取匹配内容的上下文"""
        context_start = max(0, start - context_size)
        context_end = min(len(content), end + context_size)
        return content[context_start:context_end]

    def generate_statistics(self, report_data):
        """生成详细统计分析"""
        stats = {
            'system_overview': {},
            'security_summary': {},
            'risk_assessment': {},
            'recommendations': [],
            'network_analysis': {},
            'process_analysis': {},
            'user_analysis': {}
        }
        
        # 系统概览
        if 'system_information' in report_data:
            sys_info = report_data['system_information']
            if 'system_details' in sys_info:
                content = sys_info['system_details']
                # 提取系统信息
                os_match = re.search(r'OS Name:\s*(.+)', content)
                version_match = re.search(r'OS Version:\s*(.+)', content)
                if os_match:
                    stats['system_overview']['os_name'] = os_match.group(1).strip()
                if version_match:
                    stats['system_overview']['os_version'] = version_match.group(1).strip()
        
        # 网络分析
        if 'network_information' in report_data:
            net_info = report_data['network_information']
            if 'network_connections' in net_info:
                connections = net_info['network_connections']
                # 统计连接状态
                established_count = len(re.findall(r'ESTABLISHED', connections))
                listening_count = len(re.findall(r'LISTENING', connections))
                stats['network_analysis'] = {
                    'established_connections': established_count,
                    'listening_ports': listening_count,
                    'total_connections': established_count + listening_count
                }
                
                # 分析可疑端口
                suspicious_ports = ['4444', '5555', '6666', '7777', '8888', '9999']
                for port in suspicious_ports:
                    if port in connections:
                        stats['recommendations'].append({
                            'level': 'high',
                            'title': f'发现可疑端口 {port}',
                            'description': f'检测到端口 {port} 的网络活动，这通常与恶意软件相关',
                            'action': f'检查使用端口 {port} 的进程，确认其合法性'
                        })
        
        # 进程分析
        if 'process_information' in report_data:
            proc_info = report_data['process_information']
            if 'running_processes' in proc_info:
                processes = proc_info['running_processes']
                process_lines = [line for line in processes.split('\n') if line.strip()]
                stats['process_analysis']['total_processes'] = len(process_lines)
                
                # 检查可疑进程
                suspicious_processes = ['cmd.exe', 'powershell.exe', 'wscript.exe', 'cscript.exe']
                for proc in suspicious_processes:
                    count = len(re.findall(proc, processes, re.I))
                    if count > 0:
                        stats['process_analysis'][f'{proc}_count'] = count
        
        # 用户分析
        if 'user_and_security_information' in report_data:
            user_info = report_data['user_and_security_information']
            if 'all_users' in user_info:
                users = user_info['all_users']
                user_lines = [line for line in users.split('\n') if line.strip() and not line.startswith('User accounts')]
                stats['user_analysis']['total_users'] = len(user_lines)
                
            # 检查管理员组
            if 'administrators_group' in user_info:
                admins = user_info['administrators_group']
                admin_lines = [line for line in admins.split('\n') if line.strip() and not line.startswith('Alias name') and not line.startswith('Comment')]
                stats['user_analysis']['admin_count'] = len(admin_lines)
        
        # 服务分析
        if 'service_information' in report_data:
            svc_info = report_data['service_information']
            if 'running_services' in svc_info:
                services = svc_info['running_services']
                running_services = len(re.findall(r'RUNNING', services))
                stats['system_overview']['running_services'] = running_services
        
        return stats

    def analyze_document(self, file_path):
        """分析文档"""
        try:
            # 解析文档
            report_data = parse_document(file_path)
            
            if 'error' in report_data:
                return {
                    'error': report_data['error'],
                    'success': False
                }
            
            results = {
                'critical': [],
                'high': [],
                'medium': [],
                'low': [],
                'statistics': {},
                'summary': {},
                'file_info': {
                    'name': Path(file_path).name,
                    'size': os.path.getsize(file_path),
                    'modified': datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()
                }
            }
            
            # 生成统计信息
            results['statistics'] = self.generate_statistics(report_data)
            
            # 规则匹配分析
            total_rules_checked = 0
            total_matches = 0
            
            for rule in self.rules.values():
                total_rules_checked += 1
                result = self.evaluate_rule(rule, report_data)
                if result:
                    total_matches += 1
                    level = result['level']
                    if level in results:
                        results[level].append(result)
            
            # 生成总结
            results['summary'] = {
                'total_rules_checked': total_rules_checked,
                'total_matches': total_matches,
                'critical_count': len(results['critical']),
                'high_risk_count': len(results['high']),
                'medium_risk_count': len(results['medium']),
                'low_risk_count': len(results['low']),
                'analysis_time': datetime.datetime.now().isoformat(),
                'overall_risk_level': self.calculate_overall_risk(results),
                'risk_score': self.calculate_risk_score(results)
            }
            
            # 记录分析统计
            self.analysis_stats['total_analyses'] += 1
            self.analysis_stats['total_alerts'] += total_matches
            
            logging.info(f"Analysis completed: {total_matches} alerts found from {total_rules_checked} rule checks")
            
            return results
            
        except Exception as e:
            logging.error(f"Error analyzing document {file_path}: {str(e)}")
            return {
                'error': str(e),
                'success': False
            }

    def calculate_overall_risk(self, results):
        """计算整体风险等级"""
        critical_count = len(results['critical'])
        high_count = len(results['high'])
        medium_count = len(results['medium'])
        low_count = len(results['low'])
        
        if critical_count > 0:
            return 'CRITICAL'
        elif high_count > 0:
            return 'HIGH'
        elif medium_count > 3:
            return 'MEDIUM'
        elif medium_count > 0 or low_count > 5:
            return 'LOW'
        else:
            return 'NORMAL'

    def calculate_risk_score(self, results):
        """计算风险评分（0-100）"""
        critical_count = len(results['critical'])
        high_count = len(results['high'])
        medium_count = len(results['medium'])
        low_count = len(results['low'])
        
        score = (critical_count * 25) + (high_count * 15) + (medium_count * 8) + (low_count * 3)
        return min(100, score)

    def export_results(self, results, format='json'):
        """导出分析结果"""
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format == 'json':
            filename = f'analysis_report_{timestamp}.json'
            filepath = os.path.join('exports', filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
        
        elif format == 'csv':
            filename = f'analysis_report_{timestamp}.csv'
            filepath = os.path.join('exports', filename)
            
            # 创建CSV格式的报告
            csv_data = []
            for level in ['critical', 'high', 'medium', 'low']:
                for alert in results.get(level, []):
                    csv_data.append({
                        'Level': level.upper(),
                        'Rule ID': alert['rule_id'],
                        'Name': alert['name'],
                        'Description': alert['description'],
                        'Count': alert['count'],
                        'Recommendation': alert['recommendation']
                    })
            
            # 使用标准库写入CSV
            import csv
            with open(filepath, 'w', newline='', encoding='utf-8-sig') as csvfile:
                if csv_data:
                    fieldnames = csv_data[0].keys()
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(csv_data)
        
        return filepath

# 创建分析器实例
analyzer = EnhancedWindowsAnalyzer()

# 认证装饰器
def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def permission_required(permission):
    def decorator(f):
        def decorated_function(*args, **kwargs):
            if 'username' not in session:
                return jsonify({'error': 'Authentication required'}), 401
            
            username = session['username']
            user_permissions = USER_ROLES.get(username, [])
            
            if permission not in user_permissions:
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            return f(*args, **kwargs)
        decorated_function.__name__ = f.__name__
        return decorated_function
    return decorator

# API路由
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if username in USERS and check_password_hash(USERS[username], password):
        session['username'] = username
        logging.info(f"User {username} logged in successfully")
        return jsonify({
            'success': True,
            'username': username,
            'permissions': USER_ROLES.get(username, [])
        })
    else:
        logging.warning(f"Failed login attempt for user {username}")
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    username = session.get('username')
    session.clear()
    logging.info(f"User {username} logged out")
    return jsonify({'success': True})

@app.route('/api/upload', methods=['POST'])
@login_required
@permission_required('write')
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        try:
            file.save(filepath)
            logging.info(f"File uploaded: {filename} by user {session['username']}")
            return jsonify({
                'success': True,
                'filename': filename,
                'filepath': filepath
            })
        except Exception as e:
            logging.error(f"Error saving file: {str(e)}")
            return jsonify({'error': 'Failed to save file'}), 500
    else:
        return jsonify({'error': 'Invalid file type'}), 400

@app.route('/api/analyze', methods=['POST'])
@login_required
@permission_required('read')
def analyze_file():
    data = request.get_json()
    filename = data.get('filename')
    
    if not filename:
        return jsonify({'error': 'No filename provided'}), 400
    
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    
    try:
        results = analyzer.analyze_document(filepath)
        logging.info(f"Analysis completed for {filename} by user {session['username']}")
        return jsonify(results)
    except Exception as e:
        logging.error(f"Error analyzing file {filename}: {str(e)}")
        return jsonify({'error': 'Analysis failed'}), 500

@app.route('/api/export', methods=['POST'])
@login_required
@permission_required('write')
def export_results():
    data = request.get_json()
    results = data.get('results')
    format_type = data.get('format', 'json')
    
    if not results:
        return jsonify({'error': 'No results provided'}), 400
    
    try:
        filepath = analyzer.export_results(results, format_type)
        logging.info(f"Results exported to {filepath} by user {session['username']}")
        return jsonify({
            'success': True,
            'filepath': filepath,
            'download_url': f'/api/download/{os.path.basename(filepath)}'
        })
    except Exception as e:
        logging.error(f"Error exporting results: {str(e)}")
        return jsonify({'error': 'Export failed'}), 500

@app.route('/api/download/<filename>')
@login_required
def download_file(filename):
    try:
        return send_from_directory('exports', filename, as_attachment=True)
    except Exception as e:
        logging.error(f"Error downloading file {filename}: {str(e)}")
        return jsonify({'error': 'File not found'}), 404

@app.route('/api/guide/<category>')
@login_required
def get_guide(category):
    guide_data = analyzer.guide.get_command_by_category(category)
    if guide_data:
        return jsonify(guide_data)
    else:
        return jsonify({'error': 'Category not found'}), 404

@app.route('/api/guide/search')
@login_required
def search_guide():
    keyword = request.args.get('q', '')
    if not keyword:
        return jsonify({'error': 'No search keyword provided'}), 400
    
    results = analyzer.guide.search_commands(keyword)
    return jsonify(results)

@app.route('/api/guide/categories')
@login_required
def get_categories():
    categories = analyzer.guide.get_all_categories()
    return jsonify(categories)

@app.route('/api/guide/checklist')
@login_required
def get_checklist():
    checklist = analyzer.guide.get_emergency_checklist()
    return jsonify(checklist)

@app.route('/api/stats')
@login_required
def get_stats():
    return jsonify(dict(analyzer.analysis_stats))

if __name__ == '__main__':
    logging.info("Starting Windows Emergency Response System")
    app.run(host='0.0.0.0', port=12000, debug=True)