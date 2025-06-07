# 🛡️ Windows紧急响应系统

## 📋 项目概述

这是一个专为Windows环境设计的紧急响应系统，基于[emergency项目](https://github.com/ssssssda/emergency)进行增强开发。系统提供强大的文档分析功能、完整的Windows应急技巧库，以及现代化的Web界面。

### 🚀 主要特性

#### 1. 强大的文档分析模块
- ✅ **多格式支持**: 支持 .txt、.log、.csv、.json、.xml 等格式
- ✅ **自动编码检测**: 智能检测文件编码，避免乱码问题
- ✅ **深度分析**: 基于规则引擎的安全威胁检测
- ✅ **严重性分类**: 按严重、高、中、低四个等级分类告警
- ✅ **详细建议**: 为每个问题提供具体的解决方案
- ✅ **批量处理**: 支持批量上传和处理文档

#### 2. Windows应急技巧库
- 🖥️ **Windows优化**: 专为Windows环境设计
- 📝 **CMD优先**: 优先使用cmd命令，必要时使用PowerShell
- 📚 **详细说明**: 每个命令都有详细的使用说明和示例
- 🔧 **故障排除**: 包含错误处理和故障排除指南
- 🔍 **搜索功能**: 支持关键词搜索和分类浏览

#### 3. 用户友好的界面
- 🎨 **现代化设计**: 响应式Web界面，支持拖拽上传
- 📊 **可视化展示**: 图表、表格等多种展示方式
- 📤 **导出功能**: 支持PDF、Excel、JSON、CSV等格式导出
- 🔐 **用户管理**: 基于角色的权限管理系统

#### 4. 安全性和权限管理
- 🔒 **最小权限**: 遵循最小权限原则
- 👥 **用户角色**: 支持管理员和分析师角色
- 📝 **审计日志**: 记录所有操作日志
- 🛡️ **安全配置**: CORS保护和文件类型验证

#### 5. 性能优化和可扩展性
- ⚡ **异步处理**: 支持大文件的异步分析
- 🔧 **模块化**: 模块化架构，易于扩展
- 🔌 **API接口**: 完整的REST API支持
- 📈 **性能监控**: 内置性能统计和监控

## 🛠️ 安装指南

### 系统要求
- Python 3.8+
- Windows 10/11 或 Windows Server 2016+
- 4GB+ RAM
- 1GB+ 磁盘空间

### 快速安装

1. **克隆项目**
```bash
git clone <repository-url>
cd wdyj
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **启动系统**
```bash
python app.py
```

4. **访问Web界面**
```
浏览器打开: http://localhost:12000
```

### 测试账户
- **管理员**: admin / admin123
- **分析师**: analyst / analyst123

## 🎯 使用指南

### 1. 数据收集
运行Windows数据收集脚本：
```cmd
windows_emergency_response.bat
```

### 2. 文档分析
1. 登录Web界面
2. 上传生成的报告文件
3. 点击"开始分析"
4. 查看分析结果和建议

### 3. 应急响应
1. 查看"应急技巧"标签页
2. 根据分类浏览Windows命令
3. 参考"应急清单"执行响应步骤

## 📚 Windows应急技巧库

### 系统信息查询
```cmd
# 查看系统详细信息
systeminfo

# 显示Windows版本
ver

# 获取主机名
hostname
```

### 网络诊断
```cmd
# 显示网络配置
ipconfig /all

# 测试网络连接
ping -n 4 8.8.8.8

# 跟踪路由
tracert google.com

# 显示网络连接
netstat -ano
```

### 进程管理
```cmd
# 列出所有进程
tasklist /v

# 终止进程
taskkill /f /im notepad.exe

# 通过WMI查询进程
wmic process get Name,ProcessId,CommandLine
```

### 用户和权限
```cmd
# 查看当前用户权限
whoami /priv

# 管理用户账户
net user

# 管理本地组
net localgroup administrators
```

### 服务管理
```cmd
# 查询服务状态
sc query

# 启动/停止服务
net start spooler
net stop spooler
```

### 事件日志
```cmd
# 查询事件日志
wevtutil qe System /c:10 /rd:true /f:text

# 打开事件查看器
eventvwr
```

## 🔧 配置说明

### 用户管理
在 `enhanced_windows_analyzer.py` 中修改用户配置：
```python
USERS = {
    'admin': generate_password_hash('your_password'),
    'analyst': generate_password_hash('your_password')
}

USER_ROLES = {
    'admin': ['read', 'write', 'execute', 'admin'],
    'analyst': ['read', 'write']
}
```

### 规则配置
在 `rules/` 目录下添加或修改YAML规则文件：
```yaml
- id: custom_rule
  name: 自定义规则
  description: 检测自定义威胁
  level: high
  pattern: '(?i)(suspicious_pattern)'
  target_section: process
  recommendation: 具体的处置建议
```

### 文件上传限制
修改 `enhanced_windows_analyzer.py` 中的配置：
```python
ALLOWED_EXTENSIONS = {'txt', 'log', 'csv', 'json', 'xml'}
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
```

## 📊 API文档

### 认证接口
- `POST /api/login` - 用户登录
- `POST /api/logout` - 用户退出

### 文件操作
- `POST /api/upload` - 上传文件
- `POST /api/analyze` - 分析文件
- `POST /api/export` - 导出结果

### 应急指南
- `GET /api/guide/categories` - 获取命令分类
- `GET /api/guide/<category>` - 获取分类详情
- `GET /api/guide/search?q=<keyword>` - 搜索命令
- `GET /api/guide/checklist` - 获取应急清单

## 🔍 故障排除

### 常见问题

**Q: 文件上传失败**
A: 检查文件大小是否超过50MB限制，文件格式是否支持

**Q: 分析结果为空**
A: 确认上传的文件格式正确，内容不为空

**Q: 无法访问Web界面**
A: 检查防火墙设置，确保端口12000未被占用

**Q: 编码问题导致乱码**
A: 系统会自动检测编码，如仍有问题请转换为UTF-8格式

### 日志查看
```bash
# 查看应用日志
tail -f logs/emergency_response.log
```

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目基于 MIT 许可证开源 - 查看 [LICENSE](LICENSE) 文件了解详情

## ⚠️ 免责声明

本工具仅用于授权的安全应急响应和系统检查，请勿用于非授权的安全测试。使用本工具进行的任何操作均由使用者承担全部责任。

## 🙏 致谢

- 感谢 [emergency项目](https://github.com/ssssssda/emergency) 提供的基础框架
- 感谢所有贡献者的支持和建议

---

**🎉 现在您可以安全地在Windows环境中使用这个专业的紧急响应系统了！**