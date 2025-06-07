#!/usr/bin/env python3
"""
详细分析模块 - 提供深度分析功能
包含进程分析、网络分析、用户分析、攻击统计等
"""

import re
import json
from datetime import datetime
from collections import defaultdict, Counter
import ipaddress

class DetailedAnalyzer:
    def __init__(self):
        self.suspicious_processes = [
            'backdoor.exe', 'malware.exe', 'hack.exe', 'trojan.exe', 'virus.exe',
            'keylogger.exe', 'rootkit.exe', 'payload.exe', 'shell.exe', 'exploit.exe',
            'miner.exe', 'bot.exe', 'rat.exe', 'stealer.exe', 'ransomware.exe'
        ]
        self.admin_groups = ['Administrators', 'Domain Admins', 'Enterprise Admins', 'Schema Admins']
        self.hidden_user_indicators = ['$', 'Guest', 'DefaultAccount', 'WDAGUtilityAccount']
        
    def analyze_detailed_content(self, content, filename):
        """执行详细内容分析"""
        results = {
            'filename': filename,
            'analysis_time': datetime.now().isoformat(),
            'detailed_analysis': {
                'processes': self.analyze_processes(content),
                'network_connections': self.analyze_network_connections(content),
                'users': self.analyze_users(content),
                'services': self.analyze_services(content),
                'files': self.analyze_files(content),
                'registry': self.analyze_registry(content),
                'events': self.analyze_events(content)
            },
            'attack_statistics': self.calculate_attack_statistics(content),
            'security_summary': self.generate_security_summary(content),
            'recommendations': []
        }
        
        # 生成建议
        results['recommendations'] = self.generate_recommendations(results)
        
        return results
    
    def analyze_processes(self, content):
        """分析进程信息"""
        processes = {
            'total_count': 0,
            'suspicious_processes': [],
            'high_memory_processes': [],
            'system_processes': [],
            'user_processes': [],
            'details': []
        }
        
        # 查找进程列表部分
        process_section = self.extract_section(content, 'PROCESS INFORMATION')
        if not process_section:
            return processes
        
        # 解析tasklist输出
        lines = process_section.split('\n')
        header_found = False
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # 跳过标题行
            if 'Image Name' in line and 'PID' in line:
                header_found = True
                continue
            if '=' in line and len(line) > 20:  # 跳过分隔符行
                continue
                
            # 解析进程行
            if header_found and '.exe' in line:
                # 使用正则表达式解析固定宽度的表格
                match = re.match(r'(\S+\.exe)\s+(\d+)\s+(\S+)\s+(\d+)\s+(.+)', line)
                if match:
                    process_name = match.group(1)
                    try:
                        pid = int(match.group(2))
                        session = match.group(3)
                        session_num = int(match.group(4))
                        memory = match.group(5).strip()
                        
                        process_info = {
                            'name': process_name,
                            'pid': pid,
                            'session': session,
                            'session_number': session_num,
                            'memory_usage': memory,
                            'is_suspicious': process_name.lower() in [p.lower() for p in self.suspicious_processes],
                            'is_system': session == 'Services',
                            'memory_mb': self.parse_memory(memory)
                        }
                        
                        processes['details'].append(process_info)
                        processes['total_count'] += 1
                        
                        # 分类进程
                        if process_info['is_suspicious']:
                            processes['suspicious_processes'].append(process_info)
                        
                        if process_info['memory_mb'] > 100:  # 大于100MB
                            processes['high_memory_processes'].append(process_info)
                        
                        if process_info['is_system']:
                            processes['system_processes'].append(process_info)
                        else:
                            processes['user_processes'].append(process_info)
                            
                    except (ValueError, IndexError) as e:
                        continue
        
        return processes
    
    def analyze_network_connections(self, content):
        """分析网络连接"""
        connections = {
            'total_connections': 0,
            'established_connections': [],
            'listening_ports': [],
            'external_ips': [],
            'suspicious_connections': [],
            'port_statistics': {},
            'ip_statistics': {}
        }
        
        # 查找网络连接部分
        network_section = self.extract_section(content, 'Network Information', 'Network Connections')
        if not network_section:
            return connections
        
        lines = network_section.split('\n')
        for line in lines:
            if 'TCP' in line or 'UDP' in line:
                parts = line.split()
                if len(parts) >= 4:
                    protocol = parts[0]
                    local_addr = parts[1]
                    foreign_addr = parts[2]
                    state = parts[3] if len(parts) > 3 else 'UNKNOWN'
                    
                    conn_info = {
                        'protocol': protocol,
                        'local_address': local_addr,
                        'foreign_address': foreign_addr,
                        'state': state,
                        'is_external': self.is_external_ip(foreign_addr),
                        'is_suspicious': self.is_suspicious_connection(local_addr, foreign_addr)
                    }
                    
                    connections['total_connections'] += 1
                    
                    if state == 'ESTABLISHED':
                        connections['established_connections'].append(conn_info)
                    elif state == 'LISTENING':
                        connections['listening_ports'].append(conn_info)
                    
                    if conn_info['is_external']:
                        ip = self.extract_ip(foreign_addr)
                        if ip and ip not in connections['external_ips']:
                            connections['external_ips'].append(ip)
                    
                    if conn_info['is_suspicious']:
                        connections['suspicious_connections'].append(conn_info)
                    
                    # 统计端口
                    local_port = self.extract_port(local_addr)
                    if local_port:
                        connections['port_statistics'][local_port] = connections['port_statistics'].get(local_port, 0) + 1
                    
                    # 统计IP
                    foreign_ip = self.extract_ip(foreign_addr)
                    if foreign_ip:
                        connections['ip_statistics'][foreign_ip] = connections['ip_statistics'].get(foreign_ip, 0) + 1
        
        return connections
    
    def analyze_users(self, content):
        """分析用户信息"""
        users = {
            'total_users': 0,
            'admin_users': [],
            'regular_users': [],
            'hidden_users': [],
            'disabled_users': [],
            'recently_created': [],
            'suspicious_users': [],
            'details': []
        }
        
        # 查找用户信息部分
        user_section = self.extract_section(content, 'User Information', 'User Accounts')
        if not user_section:
            return users
        
        lines = user_section.split('\n')
        current_user = None
        
        for line in lines:
            line = line.strip()
            
            # 检测用户账户行
            if 'User name' in line:
                username = line.split('User name')[-1].strip()
                current_user = {
                    'username': username,
                    'is_admin': False,
                    'is_hidden': any(indicator in username for indicator in self.hidden_user_indicators),
                    'is_disabled': False,
                    'last_logon': None,
                    'password_last_set': None,
                    'groups': []
                }
                users['details'].append(current_user)
                users['total_users'] += 1
            
            elif current_user and 'Local Group Memberships' in line:
                groups_line = line.split('Local Group Memberships')[-1].strip()
                groups = [g.strip() for g in groups_line.split('*') if g.strip()]
                current_user['groups'] = groups
                
                # 检查是否为管理员
                if any(admin_group in groups for admin_group in self.admin_groups):
                    current_user['is_admin'] = True
                    users['admin_users'].append(current_user)
                else:
                    users['regular_users'].append(current_user)
            
            elif current_user and 'Account active' in line:
                if 'No' in line:
                    current_user['is_disabled'] = True
                    users['disabled_users'].append(current_user)
            
            elif current_user and 'Password last set' in line:
                current_user['password_last_set'] = line.split('Password last set')[-1].strip()
            
            elif current_user and 'Last logon' in line:
                current_user['last_logon'] = line.split('Last logon')[-1].strip()
        
        # 识别隐藏用户和可疑用户
        for user in users['details']:
            if user['is_hidden']:
                users['hidden_users'].append(user)
            
            # 检查可疑用户（如包含hack, admin, test等）
            suspicious_keywords = ['hack', 'admin', 'test', 'temp', 'backdoor', 'shell']
            if any(keyword in user['username'].lower() for keyword in suspicious_keywords):
                users['suspicious_users'].append(user)
        
        return users
    
    def analyze_services(self, content):
        """分析服务信息"""
        services = {
            'total_services': 0,
            'running_services': [],
            'stopped_services': [],
            'suspicious_services': [],
            'auto_start_services': [],
            'details': []
        }
        
        service_section = self.extract_section(content, 'Service Information', 'Services')
        if not service_section:
            return services
        
        lines = service_section.split('\n')
        for line in lines:
            if 'SERVICE_NAME:' in line:
                service_name = line.split('SERVICE_NAME:')[-1].strip()
                service_info = {'name': service_name, 'state': 'UNKNOWN', 'start_type': 'UNKNOWN'}
                services['details'].append(service_info)
                services['total_services'] += 1
            
            elif 'STATE' in line and services['details']:
                state = line.split()[-1] if line.split() else 'UNKNOWN'
                services['details'][-1]['state'] = state
                
                if 'RUNNING' in state:
                    services['running_services'].append(services['details'][-1])
                else:
                    services['stopped_services'].append(services['details'][-1])
            
            elif 'START_TYPE' in line and services['details']:
                start_type = line.split()[-1] if line.split() else 'UNKNOWN'
                services['details'][-1]['start_type'] = start_type
                
                if 'AUTO' in start_type:
                    services['auto_start_services'].append(services['details'][-1])
        
        return services
    
    def analyze_files(self, content):
        """分析文件信息"""
        files = {
            'suspicious_files': [],
            'temp_files': [],
            'executable_files': [],
            'recent_files': [],
            'details': []
        }
        
        # 查找文件相关信息
        file_patterns = [
            r'([A-Z]:\\[^\\]+(?:\\[^\\]+)*\\.exe)',
            r'([A-Z]:\\[^\\]+(?:\\[^\\]+)*\\.dll)',
            r'([A-Z]:\\[^\\]+(?:\\[^\\]+)*\\.bat)',
            r'([A-Z]:\\[^\\]+(?:\\[^\\]+)*\\.cmd)',
            r'([A-Z]:\\[^\\]+(?:\\[^\\]+)*\\.ps1)'
        ]
        
        for pattern in file_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                file_info = {
                    'path': match,
                    'extension': match.split('.')[-1].lower(),
                    'is_suspicious': self.is_suspicious_file(match),
                    'is_temp': 'temp' in match.lower() or 'tmp' in match.lower()
                }
                files['details'].append(file_info)
                
                if file_info['is_suspicious']:
                    files['suspicious_files'].append(file_info)
                
                if file_info['is_temp']:
                    files['temp_files'].append(file_info)
                
                if file_info['extension'] in ['exe', 'dll', 'bat', 'cmd', 'ps1']:
                    files['executable_files'].append(file_info)
        
        return files
    
    def analyze_registry(self, content):
        """分析注册表信息"""
        registry = {
            'suspicious_entries': [],
            'startup_entries': [],
            'policy_changes': [],
            'details': []
        }
        
        # 查找注册表相关信息
        reg_section = self.extract_section(content, 'Registry Information', 'Registry')
        if reg_section:
            # 分析启动项
            startup_patterns = [
                r'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run',
                r'HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run'
            ]
            
            for pattern in startup_patterns:
                if re.search(pattern, reg_section, re.IGNORECASE):
                    registry['startup_entries'].append({
                        'key': pattern,
                        'found': True,
                        'suspicious': self.is_suspicious_registry_key(pattern)
                    })
        
        return registry
    
    def analyze_events(self, content):
        """分析事件日志"""
        events = {
            'total_events': 0,
            'security_events': [],
            'system_events': [],
            'application_events': [],
            'failed_logins': [],
            'successful_logins': [],
            'privilege_escalations': [],
            'details': []
        }
        
        # 查找事件日志部分
        event_section = self.extract_section(content, 'Event Logs', 'Events')
        if not event_section:
            return events
        
        # 分析特定事件ID
        event_patterns = {
            '4624': 'successful_login',
            '4625': 'failed_login',
            '4672': 'privilege_escalation',
            '4648': 'explicit_logon',
            '4634': 'logoff'
        }
        
        for event_id, event_type in event_patterns.items():
            matches = re.findall(rf'Event ID:\s*{event_id}', event_section, re.IGNORECASE)
            count = len(matches)
            
            if count > 0:
                event_info = {
                    'event_id': event_id,
                    'type': event_type,
                    'count': count,
                    'description': self.get_event_description(event_id)
                }
                events['details'].append(event_info)
                events['total_events'] += count
                
                if event_type == 'failed_login':
                    events['failed_logins'].extend([event_info] * count)
                elif event_type == 'successful_login':
                    events['successful_logins'].extend([event_info] * count)
                elif event_type == 'privilege_escalation':
                    events['privilege_escalations'].extend([event_info] * count)
        
        return events
    
    def calculate_attack_statistics(self, content):
        """计算攻击统计信息"""
        stats = {
            'total_attacks': 0,
            'failed_logins': 0,
            'privilege_escalations': 0,
            'malware_detections': 0,
            'suspicious_processes': 0,
            'network_anomalies': 0,
            'suspicious_files': 0,
            'registry_modifications': 0,
            'attack_timeline': [],
            'attack_sources': [],
            'attack_targets': []
        }
        
        # 统计失败登录
        failed_login_matches = re.findall(r'Event ID:\s*4625', content, re.IGNORECASE)
        stats['failed_logins'] = len(failed_login_matches)
        
        # 统计权限提升
        privilege_matches = re.findall(r'Event ID:\s*4672', content, re.IGNORECASE)
        stats['privilege_escalations'] = len(privilege_matches)
        
        # 统计可疑进程
        for process in self.suspicious_processes:
            if process.lower() in content.lower():
                stats['suspicious_processes'] += content.lower().count(process.lower())
        
        # 统计恶意软件检测
        malware_indicators = ['virus', 'trojan', 'malware', 'backdoor', 'rootkit']
        for indicator in malware_indicators:
            stats['malware_detections'] += content.lower().count(indicator)
        
        # 统计网络异常
        suspicious_ports = ['4444', '5555', '6666', '7777', '8888', '9999']
        for port in suspicious_ports:
            if port in content:
                stats['network_anomalies'] += 1
        
        # 统计可疑文件
        suspicious_extensions = ['.exe', '.bat', '.cmd', '.ps1', '.vbs']
        temp_paths = ['\\temp\\', '\\tmp\\', '\\appdata\\']
        for ext in suspicious_extensions:
            for path in temp_paths:
                pattern = rf'{re.escape(path)}[^\\]*{re.escape(ext)}'
                matches = re.findall(pattern, content, re.IGNORECASE)
                stats['suspicious_files'] += len(matches)
        
        # 计算总攻击数
        stats['total_attacks'] = (
            stats['failed_logins'] + 
            stats['privilege_escalations'] + 
            stats['malware_detections'] + 
            stats['suspicious_processes'] + 
            stats['network_anomalies'] + 
            stats['suspicious_files']
        )
        
        return stats
    
    def generate_security_summary(self, content):
        """生成安全摘要"""
        summary = {
            'overall_risk': 'LOW',
            'critical_issues': [],
            'high_issues': [],
            'medium_issues': [],
            'low_issues': [],
            'system_health': 'GOOD',
            'recommendations_count': 0
        }
        
        # 评估整体风险
        risk_score = 0
        
        # 检查关键安全指标
        if re.search(r'lsass\.exe.*dump', content, re.IGNORECASE):
            summary['critical_issues'].append('检测到LSASS进程转储活动')
            risk_score += 10
        
        failed_logins = len(re.findall(r'Event ID:\s*4625', content, re.IGNORECASE))
        if failed_logins > 10:
            summary['high_issues'].append(f'检测到大量失败登录尝试 ({failed_logins}次)')
            risk_score += 5
        elif failed_logins > 5:
            summary['medium_issues'].append(f'检测到多次失败登录尝试 ({failed_logins}次)')
            risk_score += 2
        
        # 检查可疑用户
        suspicious_users = re.findall(r'User name\s*([^\n]*(?:hack|admin|test|temp)[^\n]*)', content, re.IGNORECASE)
        if suspicious_users:
            summary['medium_issues'].append(f'发现可疑用户账户: {", ".join(suspicious_users)}')
            risk_score += 3
        
        # 确定整体风险等级
        if risk_score >= 10:
            summary['overall_risk'] = 'CRITICAL'
            summary['system_health'] = 'COMPROMISED'
        elif risk_score >= 7:
            summary['overall_risk'] = 'HIGH'
            summary['system_health'] = 'AT_RISK'
        elif risk_score >= 4:
            summary['overall_risk'] = 'MEDIUM'
            summary['system_health'] = 'CONCERNING'
        elif risk_score >= 1:
            summary['overall_risk'] = 'LOW'
            summary['system_health'] = 'FAIR'
        
        summary['recommendations_count'] = len(summary['critical_issues']) + len(summary['high_issues']) + len(summary['medium_issues'])
        
        return summary
    
    def generate_recommendations(self, analysis_results):
        """生成详细建议"""
        recommendations = []
        
        # 基于攻击统计生成建议
        attack_stats = analysis_results['attack_statistics']
        
        if attack_stats['failed_logins'] > 10:
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Authentication',
                'title': '大量失败登录检测',
                'description': f'检测到{attack_stats["failed_logins"]}次失败登录尝试，可能存在暴力破解攻击',
                'action': '1. 立即检查账户锁定策略\n2. 审查失败登录的源IP\n3. 考虑启用多因素认证\n4. 监控相关用户账户'
            })
        
        if attack_stats['privilege_escalations'] > 0:
            recommendations.append({
                'priority': 'CRITICAL',
                'category': 'Privilege Escalation',
                'title': '权限提升活动检测',
                'description': f'检测到{attack_stats["privilege_escalations"]}次权限提升尝试',
                'action': '1. 立即审查提升权限的账户\n2. 检查是否为授权操作\n3. 审查管理员组成员\n4. 加强权限管理策略'
            })
        
        # 基于进程分析生成建议
        processes = analysis_results['detailed_analysis']['processes']
        if processes['suspicious_processes']:
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Process Analysis',
                'title': '可疑进程检测',
                'description': f'发现{len(processes["suspicious_processes"])}个可疑进程',
                'action': '1. 立即终止可疑进程\n2. 分析进程来源和行为\n3. 检查进程签名\n4. 隔离相关文件'
            })
        
        # 基于网络分析生成建议
        network = analysis_results['detailed_analysis']['network_connections']
        if network['suspicious_connections']:
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Network Security',
                'title': '可疑网络连接',
                'description': f'发现{len(network["suspicious_connections"])}个可疑网络连接',
                'action': '1. 阻断可疑IP连接\n2. 分析网络流量\n3. 检查防火墙规则\n4. 监控外部通信'
            })
        
        # 基于用户分析生成建议
        users = analysis_results['detailed_analysis']['users']
        if users['suspicious_users']:
            recommendations.append({
                'priority': 'MEDIUM',
                'category': 'User Management',
                'title': '可疑用户账户',
                'description': f'发现{len(users["suspicious_users"])}个可疑用户账户',
                'action': '1. 禁用可疑账户\n2. 审查账户创建历史\n3. 检查账户权限\n4. 重置相关密码'
            })
        
        return recommendations
    
    # 辅助方法
    def extract_section(self, content, *section_names):
        """提取特定部分的内容"""
        for section_name in section_names:
            # 尝试多种格式的分隔符
            patterns = [
                rf'===== {re.escape(section_name)} =====(.*?)(?=\n===== |$)',
                rf'===== {re.escape(section_name.upper())} =====(.*?)(?=\n===== |$)',
                rf'----- {re.escape(section_name)} -----(.*?)(?=\n===== |$)',
                rf'----- {re.escape(section_name.title())} -----(.*?)(?=\n===== |$)'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
                if match:
                    return match.group(1).strip()
        return ""
    
    def parse_memory(self, memory_str):
        """解析内存使用量"""
        try:
            if 'K' in memory_str:
                return float(memory_str.replace('K', '').replace(',', '')) / 1024
            elif 'M' in memory_str:
                return float(memory_str.replace('M', '').replace(',', ''))
            else:
                return float(memory_str.replace(',', '')) / 1024 / 1024
        except:
            return 0
    
    def is_external_ip(self, address):
        """检查是否为外部IP"""
        try:
            ip = self.extract_ip(address)
            if not ip:
                return False
            ip_obj = ipaddress.ip_address(ip)
            return not ip_obj.is_private
        except:
            return False
    
    def extract_ip(self, address):
        """从地址中提取IP"""
        match = re.search(r'(\d+\.\d+\.\d+\.\d+)', address)
        return match.group(1) if match else None
    
    def extract_port(self, address):
        """从地址中提取端口"""
        match = re.search(r':(\d+)$', address)
        return match.group(1) if match else None
    
    def is_suspicious_connection(self, local_addr, foreign_addr):
        """检查是否为可疑连接"""
        suspicious_ports = ['4444', '5555', '6666', '7777', '8888', '9999']
        return any(port in local_addr or port in foreign_addr for port in suspicious_ports)
    
    def is_suspicious_file(self, file_path):
        """检查是否为可疑文件"""
        suspicious_paths = ['\\temp\\', '\\tmp\\', '\\appdata\\local\\temp\\']
        suspicious_names = ['hack', 'backdoor', 'shell', 'payload', 'exploit']
        
        file_path_lower = file_path.lower()
        return (any(path in file_path_lower for path in suspicious_paths) or
                any(name in file_path_lower for name in suspicious_names))
    
    def is_suspicious_registry_key(self, key):
        """检查是否为可疑注册表项"""
        suspicious_indicators = ['temp', 'hack', 'backdoor', 'shell']
        return any(indicator in key.lower() for indicator in suspicious_indicators)
    
    def get_event_description(self, event_id):
        """获取事件描述"""
        descriptions = {
            '4624': '账户成功登录',
            '4625': '账户登录失败',
            '4672': '分配给新登录的特殊权限',
            '4648': '使用显式凭据尝试登录',
            '4634': '账户注销'
        }
        return descriptions.get(event_id, f'事件ID {event_id}')