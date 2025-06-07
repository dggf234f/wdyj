#!/usr/bin/env python3
"""
Windows应急技巧和教程库
专为Windows环境设计，优先使用cmd命令
"""

class WindowsEmergencyGuide:
    def __init__(self):
        self.commands = {
            "system_info": {
                "name": "系统信息查询",
                "description": "获取系统详细信息和配置",
                "commands": [
                    {
                        "command": "systeminfo",
                        "description": "显示计算机及其操作系统的详细配置信息",
                        "usage": "systeminfo",
                        "example": "systeminfo | findstr /C:\"OS Name\" /C:\"OS Version\"",
                        "parameters": {
                            "/s": "指定远程计算机名称或IP地址",
                            "/u": "指定用户账户",
                            "/p": "指定用户密码"
                        },
                        "output_example": "OS Name: Microsoft Windows 10 Pro\nOS Version: 10.0.19041 N/A Build 19041",
                        "troubleshooting": "如果命令执行缓慢，可能是WMI服务问题，尝试重启WMI服务"
                    },
                    {
                        "command": "ver",
                        "description": "显示Windows版本号",
                        "usage": "ver",
                        "example": "ver",
                        "output_example": "Microsoft Windows [Version 10.0.19041.1052]",
                        "troubleshooting": "此命令很少出错，如果无输出检查命令提示符是否正常"
                    },
                    {
                        "command": "hostname",
                        "description": "显示计算机名称",
                        "usage": "hostname",
                        "example": "hostname",
                        "output_example": "DESKTOP-ABC123",
                        "troubleshooting": "如果显示错误的主机名，检查网络配置"
                    }
                ]
            },
            "network_diagnostics": {
                "name": "网络诊断",
                "description": "网络连接和配置诊断工具",
                "commands": [
                    {
                        "command": "ipconfig",
                        "description": "显示和配置网络接口信息",
                        "usage": "ipconfig [/all] [/release] [/renew] [/flushdns]",
                        "example": "ipconfig /all",
                        "parameters": {
                            "/all": "显示所有网络适配器的详细信息",
                            "/release": "释放指定适配器的IP地址",
                            "/renew": "更新指定适配器的IP地址",
                            "/flushdns": "清除DNS解析程序缓存",
                            "/displaydns": "显示DNS解析程序缓存的内容"
                        },
                        "output_example": "Windows IP Configuration\nEthernet adapter Local Area Connection:\nIP Address: 192.168.1.100",
                        "troubleshooting": "如果显示'Media disconnected'，检查网线连接；如果无法获取IP，检查DHCP服务"
                    },
                    {
                        "command": "ping",
                        "description": "测试网络连接性",
                        "usage": "ping [-t] [-n count] target",
                        "example": "ping -n 4 8.8.8.8",
                        "parameters": {
                            "-t": "持续ping直到停止",
                            "-n": "指定发送的回显请求数",
                            "-l": "指定数据包大小",
                            "-w": "指定超时时间（毫秒）"
                        },
                        "output_example": "Reply from 8.8.8.8: bytes=32 time=20ms TTL=64",
                        "troubleshooting": "如果显示'Request timed out'，检查网络连接和防火墙设置"
                    },
                    {
                        "command": "tracert",
                        "description": "跟踪数据包到目标的路由路径",
                        "usage": "tracert [-h maximum_hops] target",
                        "example": "tracert google.com",
                        "parameters": {
                            "-h": "指定最大跳数",
                            "-w": "指定每次回复的超时时间"
                        },
                        "output_example": "1    1 ms    1 ms    1 ms  192.168.1.1\n2   20 ms   19 ms   20 ms  10.0.0.1",
                        "troubleshooting": "如果某跳显示'Request timed out'，可能是路由器配置了不响应ICMP"
                    },
                    {
                        "command": "netstat",
                        "description": "显示网络连接、路由表和网络接口统计",
                        "usage": "netstat [-a] [-n] [-o] [-p protocol]",
                        "example": "netstat -ano",
                        "parameters": {
                            "-a": "显示所有连接和监听端口",
                            "-n": "以数字形式显示地址和端口",
                            "-o": "显示拥有的进程ID",
                            "-p": "显示指定协议的连接",
                            "-r": "显示路由表"
                        },
                        "output_example": "TCP    127.0.0.1:135         0.0.0.0:0              LISTENING       1234",
                        "troubleshooting": "如果看到大量CLOSE_WAIT状态，可能是应用程序没有正确关闭连接"
                    },
                    {
                        "command": "nslookup",
                        "description": "查询DNS信息",
                        "usage": "nslookup [domain] [dns_server]",
                        "example": "nslookup google.com 8.8.8.8",
                        "output_example": "Name:    google.com\nAddress:  172.217.164.110",
                        "troubleshooting": "如果查询失败，检查DNS服务器设置或尝试其他DNS服务器"
                    },
                    {
                        "command": "arp",
                        "description": "显示和修改ARP缓存表",
                        "usage": "arp [-a] [-d ip_address] [-s ip_address mac_address]",
                        "example": "arp -a",
                        "parameters": {
                            "-a": "显示所有ARP条目",
                            "-d": "删除指定IP的ARP条目",
                            "-s": "添加静态ARP条目"
                        },
                        "output_example": "192.168.1.1           00-1a-2b-3c-4d-5e     dynamic",
                        "troubleshooting": "如果ARP表异常，可能存在ARP欺骗攻击"
                    }
                ]
            },
            "process_management": {
                "name": "进程管理",
                "description": "进程查看、管理和故障排除",
                "commands": [
                    {
                        "command": "tasklist",
                        "description": "显示当前运行的进程列表",
                        "usage": "tasklist [/fi filter] [/fo format] [/v]",
                        "example": "tasklist /v",
                        "parameters": {
                            "/fi": "应用筛选器",
                            "/fo": "指定输出格式(table, list, csv)",
                            "/v": "显示详细信息",
                            "/s": "指定远程计算机",
                            "/m": "显示模块信息"
                        },
                        "output_example": "notepad.exe                   1234 Console                    1     12,345 K",
                        "troubleshooting": "如果进程列表不完整，可能需要管理员权限"
                    },
                    {
                        "command": "taskkill",
                        "description": "终止进程",
                        "usage": "taskkill [/f] [/im imagename | /pid processid]",
                        "example": "taskkill /f /im notepad.exe",
                        "parameters": {
                            "/f": "强制终止进程",
                            "/im": "指定进程映像名称",
                            "/pid": "指定进程ID",
                            "/t": "终止进程及其子进程"
                        },
                        "output_example": "SUCCESS: The process \"notepad.exe\" with PID 1234 has been terminated.",
                        "troubleshooting": "如果无法终止进程，尝试使用/f参数强制终止"
                    },
                    {
                        "command": "wmic process",
                        "description": "通过WMI管理进程",
                        "usage": "wmic process [where condition] [get properties] [call method]",
                        "example": "wmic process where name=\"notepad.exe\" get ProcessId,CommandLine",
                        "parameters": {
                            "where": "指定筛选条件",
                            "get": "获取指定属性",
                            "call terminate": "终止进程"
                        },
                        "output_example": "CommandLine                    ProcessId\nC:\\Windows\\notepad.exe         1234",
                        "troubleshooting": "如果WMI命令失败，检查WMI服务是否正常运行"
                    }
                ]
            },
            "file_operations": {
                "name": "文件和目录操作",
                "description": "文件系统操作和管理",
                "commands": [
                    {
                        "command": "dir",
                        "description": "列出目录内容",
                        "usage": "dir [path] [/a] [/s] [/b] [/o]",
                        "example": "dir C:\\Windows\\System32 /a /s",
                        "parameters": {
                            "/a": "显示所有文件（包括隐藏文件）",
                            "/s": "递归显示子目录",
                            "/b": "简洁格式",
                            "/o": "排序选项",
                            "/q": "显示文件所有者"
                        },
                        "output_example": "2021/01/01  12:00    <DIR>          .",
                        "troubleshooting": "如果提示'Access denied'，需要管理员权限"
                    },
                    {
                        "command": "copy",
                        "description": "复制文件",
                        "usage": "copy source destination [/y] [/v]",
                        "example": "copy C:\\temp\\file.txt D:\\backup\\",
                        "parameters": {
                            "/y": "不提示确认覆盖",
                            "/v": "验证复制的文件",
                            "/a": "ASCII文本文件",
                            "/b": "二进制文件"
                        },
                        "output_example": "1 file(s) copied.",
                        "troubleshooting": "如果复制失败，检查目标路径是否存在和权限"
                    },
                    {
                        "command": "del",
                        "description": "删除文件",
                        "usage": "del [/f] [/q] [/s] filename",
                        "example": "del /f /q C:\\temp\\*.tmp",
                        "parameters": {
                            "/f": "强制删除只读文件",
                            "/q": "安静模式，不提示确认",
                            "/s": "删除子目录中的文件",
                            "/a": "根据属性删除文件"
                        },
                        "output_example": "删除成功或无输出",
                        "troubleshooting": "如果无法删除，检查文件是否被占用或需要管理员权限"
                    },
                    {
                        "command": "mkdir",
                        "description": "创建目录",
                        "usage": "mkdir directory_name",
                        "example": "mkdir C:\\temp\\new_folder",
                        "output_example": "目录创建成功或无输出",
                        "troubleshooting": "如果创建失败，检查父目录是否存在和权限"
                    },
                    {
                        "command": "ren",
                        "description": "重命名文件或目录",
                        "usage": "ren old_name new_name",
                        "example": "ren old_file.txt new_file.txt",
                        "output_example": "重命名成功或无输出",
                        "troubleshooting": "如果重命名失败，检查文件是否被占用"
                    }
                ]
            },
            "registry_operations": {
                "name": "注册表操作",
                "description": "Windows注册表查询和修改",
                "commands": [
                    {
                        "command": "reg query",
                        "description": "查询注册表项",
                        "usage": "reg query keyname [/v valuename] [/s]",
                        "example": "reg query \"HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run\"",
                        "parameters": {
                            "/v": "查询特定值",
                            "/s": "递归查询子项",
                            "/f": "搜索数据",
                            "/t": "指定数据类型"
                        },
                        "output_example": "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run\n    Program    REG_SZ    C:\\Program Files\\App\\app.exe",
                        "troubleshooting": "如果提示访问被拒绝，需要管理员权限"
                    },
                    {
                        "command": "reg add",
                        "description": "添加注册表项或值",
                        "usage": "reg add keyname [/v valuename] [/t type] [/d data] [/f]",
                        "example": "reg add \"HKCU\\Software\\Test\" /v \"TestValue\" /t REG_SZ /d \"TestData\" /f",
                        "parameters": {
                            "/v": "值名称",
                            "/t": "数据类型(REG_SZ, REG_DWORD等)",
                            "/d": "数据",
                            "/f": "强制覆盖"
                        },
                        "output_example": "The operation completed successfully.",
                        "troubleshooting": "修改系统注册表项需要管理员权限，建议先备份"
                    },
                    {
                        "command": "reg delete",
                        "description": "删除注册表项或值",
                        "usage": "reg delete keyname [/v valuename] [/f]",
                        "example": "reg delete \"HKCU\\Software\\Test\" /v \"TestValue\" /f",
                        "parameters": {
                            "/v": "要删除的值名称",
                            "/f": "强制删除不提示"
                        },
                        "output_example": "The operation completed successfully.",
                        "troubleshooting": "删除重要注册表项前务必备份，错误删除可能导致系统问题"
                    }
                ]
            },
            "security_management": {
                "name": "安全和权限管理",
                "description": "用户权限和安全管理",
                "commands": [
                    {
                        "command": "whoami",
                        "description": "显示当前用户信息",
                        "usage": "whoami [/user] [/groups] [/priv] [/all]",
                        "example": "whoami /priv",
                        "parameters": {
                            "/user": "显示用户名和SID",
                            "/groups": "显示用户组",
                            "/priv": "显示用户权限",
                            "/all": "显示所有信息"
                        },
                        "output_example": "DOMAIN\\username\nPrivilege Name                Description                    State\nSeShutdownPrivilege          Shut down the system          Disabled",
                        "troubleshooting": "此命令很少出错，如果无输出检查命令提示符"
                    },
                    {
                        "command": "net user",
                        "description": "管理用户账户",
                        "usage": "net user [username] [password] [/add] [/delete] [/active]",
                        "example": "net user testuser /add",
                        "parameters": {
                            "/add": "添加用户",
                            "/delete": "删除用户",
                            "/active:yes|no": "激活或禁用用户",
                            "/expires": "设置账户过期时间"
                        },
                        "output_example": "User accounts for \\\\COMPUTERNAME\nadministrator            guest                    testuser",
                        "troubleshooting": "管理用户需要管理员权限"
                    },
                    {
                        "command": "net localgroup",
                        "description": "管理本地组",
                        "usage": "net localgroup [groupname] [username] [/add] [/delete]",
                        "example": "net localgroup administrators",
                        "parameters": {
                            "/add": "添加用户到组",
                            "/delete": "从组中删除用户"
                        },
                        "output_example": "Alias name     administrators\nComment        Administrators have complete and unrestricted access\nMembers\nadministrator",
                        "troubleshooting": "修改管理员组需要管理员权限"
                    },
                    {
                        "command": "icacls",
                        "description": "管理文件和目录权限",
                        "usage": "icacls filename [/grant user:permission] [/deny user:permission]",
                        "example": "icacls C:\\temp /grant everyone:F",
                        "parameters": {
                            "/grant": "授予权限",
                            "/deny": "拒绝权限",
                            "/remove": "移除权限",
                            "/inheritance": "设置继承"
                        },
                        "output_example": "processed file: C:\\temp\nSuccessfully processed 1 files; Failed processing 0 files",
                        "troubleshooting": "修改系统文件权限需要管理员权限"
                    },
                    {
                        "command": "takeown",
                        "description": "取得文件或目录的所有权",
                        "usage": "takeown /f filename [/r] [/d]",
                        "example": "takeown /f C:\\temp\\file.txt",
                        "parameters": {
                            "/f": "指定文件或目录",
                            "/r": "递归操作",
                            "/d": "默认答案"
                        },
                        "output_example": "SUCCESS: The file (or folder): \"C:\\temp\\file.txt\" now owned by user \"DOMAIN\\username\".",
                        "troubleshooting": "需要管理员权限，谨慎使用避免破坏系统文件权限"
                    }
                ]
            },
            "performance_monitoring": {
                "name": "性能监控",
                "description": "系统性能监控和诊断",
                "commands": [
                    {
                        "command": "perfmon",
                        "description": "启动性能监视器",
                        "usage": "perfmon [/res] [/report]",
                        "example": "perfmon /res",
                        "parameters": {
                            "/res": "启动资源监视器",
                            "/report": "生成系统诊断报告"
                        },
                        "output_example": "启动图形界面工具",
                        "troubleshooting": "如果无法启动，检查性能计数器服务是否运行"
                    },
                    {
                        "command": "resmon",
                        "description": "启动资源监视器",
                        "usage": "resmon",
                        "example": "resmon",
                        "output_example": "启动图形界面工具",
                        "troubleshooting": "如果无法启动，尝试以管理员身份运行"
                    },
                    {
                        "command": "wmic cpu",
                        "description": "查询CPU信息",
                        "usage": "wmic cpu get property",
                        "example": "wmic cpu get Name,NumberOfCores,MaxClockSpeed",
                        "output_example": "MaxClockSpeed  Name                           NumberOfCores\n2400          Intel(R) Core(TM) i5-8250U     4",
                        "troubleshooting": "如果WMI查询失败，重启WMI服务"
                    },
                    {
                        "command": "wmic memorychip",
                        "description": "查询内存信息",
                        "usage": "wmic memorychip get property",
                        "example": "wmic memorychip get Capacity,Speed,Manufacturer",
                        "output_example": "Capacity     Manufacturer  Speed\n8589934592   Samsung       2400",
                        "troubleshooting": "如果显示不完整，可能是内存模块识别问题"
                    }
                ]
            },
            "disk_management": {
                "name": "磁盘管理",
                "description": "磁盘和文件系统管理",
                "commands": [
                    {
                        "command": "chkdsk",
                        "description": "检查和修复磁盘错误",
                        "usage": "chkdsk [drive:] [/f] [/r] [/x]",
                        "example": "chkdsk C: /f /r",
                        "parameters": {
                            "/f": "修复错误",
                            "/r": "定位坏扇区并恢复可读信息",
                            "/x": "强制卸载卷",
                            "/v": "显示详细信息"
                        },
                        "output_example": "Windows has checked the file system and found no problems.",
                        "troubleshooting": "系统盘检查需要重启，数据盘可能需要卸载"
                    },
                    {
                        "command": "diskpart",
                        "description": "磁盘分区管理工具",
                        "usage": "diskpart",
                        "example": "diskpart\nlist disk\nselect disk 0\nlist partition",
                        "note": "这是一个交互式工具，需要管理员权限",
                        "output_example": "Microsoft DiskPart version 10.0.19041.1\nDISKPART>",
                        "troubleshooting": "使用前务必确认操作对象，错误操作可能导致数据丢失"
                    },
                    {
                        "command": "fsutil",
                        "description": "文件系统实用工具",
                        "usage": "fsutil [command] [parameters]",
                        "example": "fsutil volume diskfree C:",
                        "parameters": {
                            "volume": "卷管理",
                            "file": "文件管理",
                            "fsinfo": "文件系统信息"
                        },
                        "output_example": "Total # of free bytes        : 123456789012\nTotal # of bytes             : 234567890123",
                        "troubleshooting": "需要管理员权限，某些功能可能需要特定文件系统"
                    },
                    {
                        "command": "defrag",
                        "description": "磁盘碎片整理",
                        "usage": "defrag [drive:] [/a] [/x] [/o]",
                        "example": "defrag C: /a",
                        "parameters": {
                            "/a": "分析碎片",
                            "/x": "执行可用空间整理",
                            "/o": "执行完整优化"
                        },
                        "output_example": "The operation completed successfully.",
                        "troubleshooting": "SSD不建议进行传统碎片整理，使用/o参数优化"
                    }
                ]
            },
            "service_management": {
                "name": "服务管理",
                "description": "Windows服务管理和故障排除",
                "commands": [
                    {
                        "command": "sc query",
                        "description": "查询服务状态",
                        "usage": "sc query [service_name] [state]",
                        "example": "sc query state= running",
                        "parameters": {
                            "state=": "按状态筛选(running, stopped等)",
                            "type=": "按类型筛选"
                        },
                        "output_example": "SERVICE_NAME: Spooler\nTYPE               : 110  WIN32_OWN_PROCESS\nSTATE              : 4  RUNNING",
                        "troubleshooting": "如果服务列表不完整，可能需要管理员权限"
                    },
                    {
                        "command": "net start",
                        "description": "启动服务",
                        "usage": "net start service_name",
                        "example": "net start spooler",
                        "output_example": "The Print Spooler service is starting.\nThe Print Spooler service was started successfully.",
                        "troubleshooting": "如果启动失败，检查服务依赖和权限"
                    },
                    {
                        "command": "net stop",
                        "description": "停止服务",
                        "usage": "net stop service_name",
                        "example": "net stop spooler",
                        "output_example": "The Print Spooler service is stopping.\nThe Print Spooler service was stopped successfully.",
                        "troubleshooting": "某些系统服务可能无法停止或需要特殊权限"
                    },
                    {
                        "command": "wmic service",
                        "description": "通过WMI管理服务",
                        "usage": "wmic service [where condition] [get properties] [call method]",
                        "example": "wmic service where name=\"spooler\" get State,StartMode",
                        "output_example": "StartMode  State\nAuto       Running",
                        "troubleshooting": "如果WMI命令失败，检查WMI服务状态"
                    }
                ]
            },
            "event_logs": {
                "name": "事件日志",
                "description": "Windows事件日志查看和分析",
                "commands": [
                    {
                        "command": "wevtutil qe",
                        "description": "查询事件日志",
                        "usage": "wevtutil qe log_name [/c:count] [/rd:true] [/f:format]",
                        "example": "wevtutil qe System /c:10 /rd:true /f:text",
                        "parameters": {
                            "/c:": "指定事件数量",
                            "/rd:": "反向读取(最新的在前)",
                            "/f:": "输出格式(text, xml)",
                            "/q:": "XPath查询"
                        },
                        "output_example": "Event[1]:\n  Log Name: System\n  Source: Service Control Manager\n  Event ID: 7036",
                        "troubleshooting": "如果无法访问某些日志，需要管理员权限"
                    },
                    {
                        "command": "eventvwr",
                        "description": "打开事件查看器",
                        "usage": "eventvwr [/l:log_file]",
                        "example": "eventvwr",
                        "parameters": {
                            "/l:": "打开指定的日志文件"
                        },
                        "output_example": "启动图形界面工具",
                        "troubleshooting": "如果无法启动，检查事件日志服务是否运行"
                    }
                ]
            },
            "powershell_when_needed": {
                "name": "PowerShell命令（必要时使用）",
                "description": "当cmd无法完成任务时使用的PowerShell命令",
                "note": "仅在cmd命令无法满足需求时使用",
                "commands": [
                    {
                        "command": "Get-Process",
                        "description": "获取详细的进程信息（当tasklist信息不足时使用）",
                        "usage": "powershell \"Get-Process | Select-Object Name,Id,CPU,WorkingSet\"",
                        "when_to_use": "需要获取进程的CPU使用率、内存详细信息时",
                        "cmd_alternative": "tasklist /v（但信息较少）"
                    },
                    {
                        "command": "Get-EventLog",
                        "description": "高级事件日志查询（当wevtutil不够用时）",
                        "usage": "powershell \"Get-EventLog -LogName System -Newest 10\"",
                        "when_to_use": "需要复杂的事件日志筛选和分析时",
                        "cmd_alternative": "wevtutil qe（功能较基础）"
                    },
                    {
                        "command": "Get-WmiObject",
                        "description": "高级WMI查询（当wmic语法复杂时）",
                        "usage": "powershell \"Get-WmiObject Win32_Process | Where-Object {$_.Name -eq 'notepad.exe'}\"",
                        "when_to_use": "需要复杂的WMI查询和对象操作时",
                        "cmd_alternative": "wmic（但语法较复杂）"
                    },
                    {
                        "command": "Test-NetConnection",
                        "description": "高级网络连接测试（当基础网络命令不够时）",
                        "usage": "powershell \"Test-NetConnection -ComputerName google.com -Port 443\"",
                        "when_to_use": "需要测试特定端口连接或获取详细网络信息时",
                        "cmd_alternative": "telnet（但功能有限）"
                    }
                ]
            }
        }
    
    def get_command_by_category(self, category):
        """根据分类获取命令"""
        return self.commands.get(category, {})
    
    def search_commands(self, keyword):
        """搜索包含关键词的命令"""
        results = []
        for category, data in self.commands.items():
            if 'commands' in data:
                for cmd in data['commands']:
                    if (keyword.lower() in cmd['command'].lower() or 
                        keyword.lower() in cmd['description'].lower()):
                        results.append({
                            'category': category,
                            'command': cmd
                        })
        return results
    
    def get_all_categories(self):
        """获取所有命令分类"""
        return {k: v.get('name', k) for k, v in self.commands.items()}
    
    def get_emergency_checklist(self):
        """获取应急响应检查清单"""
        return {
            "immediate_response": [
                "1. 隔离受影响系统 - 断开网络连接但保持电源",
                "2. 保存易失性数据 - 运行内存转储和进程列表",
                "3. 记录当前状态 - 截图和日志记录",
                "4. 通知相关人员 - 安全团队和管理层"
            ],
            "data_collection": [
                "1. 运行 windows_emergency_response.bat 收集系统信息",
                "2. 导出关键事件日志",
                "3. 收集网络连接信息",
                "4. 备份可疑文件（不要直接删除）"
            ],
            "analysis_steps": [
                "1. 上传收集的数据到分析平台",
                "2. 查看高危告警和建议",
                "3. 分析网络连接和进程",
                "4. 检查用户账户和权限变化"
            ],
            "containment": [
                "1. 禁用可疑用户账户",
                "2. 停止可疑服务和进程",
                "3. 阻断恶意网络连接",
                "4. 隔离受感染文件"
            ],
            "recovery": [
                "1. 清理恶意文件和注册表项",
                "2. 重置受影响账户密码",
                "3. 更新安全策略",
                "4. 恢复正常网络连接"
            ]
        }