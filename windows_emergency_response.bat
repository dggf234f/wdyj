@echo off
REM Windows Emergency Response Data Collection Script
REM 专为Windows设计的紧急响应数据收集脚本
REM 优先使用cmd命令，必要时使用PowerShell

setlocal enabledelayedexpansion
set "REPORT_FILE=emergency_report_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%.txt"
set "REPORT_FILE=%REPORT_FILE: =0%"

echo =============================================== > "%REPORT_FILE%"
echo Windows Emergency Response Report >> "%REPORT_FILE%"
echo Generated: %date% %time% >> "%REPORT_FILE%"
echo =============================================== >> "%REPORT_FILE%"
echo. >> "%REPORT_FILE%"

echo [INFO] Starting Windows Emergency Response Data Collection...
echo [INFO] Report will be saved as: %REPORT_FILE%

REM ===== 系统信息查询 =====
echo [INFO] Collecting system information...
echo ===== SYSTEM INFORMATION ===== >> "%REPORT_FILE%"
echo. >> "%REPORT_FILE%"

echo ----- System Details ----- >> "%REPORT_FILE%"
systeminfo >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

echo ----- Windows Version ----- >> "%REPORT_FILE%"
ver >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

echo ----- Hostname ----- >> "%REPORT_FILE%"
hostname >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

echo ----- Environment Variables ----- >> "%REPORT_FILE%"
set >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

REM ===== 网络配置和诊断 =====
echo [INFO] Collecting network information...
echo ===== NETWORK INFORMATION ===== >> "%REPORT_FILE%"
echo. >> "%REPORT_FILE%"

echo ----- Network Configuration ----- >> "%REPORT_FILE%"
ipconfig /all >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

echo ----- Network Connections ----- >> "%REPORT_FILE%"
netstat -an >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

echo ----- Listening Ports ----- >> "%REPORT_FILE%"
netstat -an | findstr LISTENING >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

echo ----- ARP Table ----- >> "%REPORT_FILE%"
arp -a >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

echo ----- Routing Table ----- >> "%REPORT_FILE%"
route print >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

echo ----- DNS Cache ----- >> "%REPORT_FILE%"
ipconfig /displaydns >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

REM ===== 进程管理 =====
echo [INFO] Collecting process information...
echo ===== PROCESS INFORMATION ===== >> "%REPORT_FILE%"
echo. >> "%REPORT_FILE%"

echo ----- Running Processes ----- >> "%REPORT_FILE%"
tasklist /v >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

echo ----- Process Tree ----- >> "%REPORT_FILE%"
wmic process get Name,ProcessId,ParentProcessId,CommandLine /format:csv >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

echo ----- Suspicious Processes ----- >> "%REPORT_FILE%"
wmic process where "name like '%%cmd%%' or name like '%%powershell%%' or name like '%%wscript%%' or name like '%%cscript%%'" get Name,ProcessId,CommandLine /format:csv >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

REM ===== 用户和权限管理 =====
echo [INFO] Collecting user and security information...
echo ===== USER AND SECURITY INFORMATION ===== >> "%REPORT_FILE%"
echo. >> "%REPORT_FILE%"

echo ----- Current User ----- >> "%REPORT_FILE%"
whoami >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

echo ----- Current User Privileges ----- >> "%REPORT_FILE%"
whoami /priv >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

echo ----- Current User Groups ----- >> "%REPORT_FILE%"
whoami /groups >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

echo ----- All Users ----- >> "%REPORT_FILE%"
net user >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

echo ----- Local Groups ----- >> "%REPORT_FILE%"
net localgroup >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

echo ----- Administrators Group ----- >> "%REPORT_FILE%"
net localgroup administrators >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

echo ----- Remote Desktop Users ----- >> "%REPORT_FILE%"
net localgroup "Remote Desktop Users" >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

REM ===== 服务管理 =====
echo [INFO] Collecting service information...
echo ===== SERVICE INFORMATION ===== >> "%REPORT_FILE%"
echo. >> "%REPORT_FILE%"

echo ----- All Services ----- >> "%REPORT_FILE%"
sc query >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

echo ----- Running Services ----- >> "%REPORT_FILE%"
sc query state= running >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

echo ----- Service Details via WMIC ----- >> "%REPORT_FILE%"
wmic service get Name,State,StartMode,PathName /format:csv >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

REM ===== 启动项和计划任务 =====
echo [INFO] Collecting startup and scheduled tasks...
echo ===== STARTUP AND SCHEDULED TASKS ===== >> "%REPORT_FILE%"
echo. >> "%REPORT_FILE%"

echo ----- Startup Programs ----- >> "%REPORT_FILE%"
wmic startup get Caption,Command,Location /format:csv >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

echo ----- Scheduled Tasks ----- >> "%REPORT_FILE%"
schtasks /query /fo csv /v >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

REM ===== 文件系统信息 =====
echo [INFO] Collecting filesystem information...
echo ===== FILESYSTEM INFORMATION ===== >> "%REPORT_FILE%"
echo. >> "%REPORT_FILE%"

echo ----- Disk Usage ----- >> "%REPORT_FILE%"
wmic logicaldisk get Size,FreeSpace,Caption /format:csv >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

echo ----- System Files ----- >> "%REPORT_FILE%"
dir C:\Windows\System32\*.exe /s /b >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

echo ----- Temp Files ----- >> "%REPORT_FILE%"
dir %TEMP% >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

echo ----- Recent Files ----- >> "%REPORT_FILE%"
dir "%USERPROFILE%\Recent" >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

REM ===== 注册表关键信息 =====
echo [INFO] Collecting registry information...
echo ===== REGISTRY INFORMATION ===== >> "%REPORT_FILE%"
echo. >> "%REPORT_FILE%"

echo ----- Run Keys ----- >> "%REPORT_FILE%"
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" >> "%REPORT_FILE%" 2>&1
reg query "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run" >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

echo ----- RunOnce Keys ----- >> "%REPORT_FILE%"
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce" >> "%REPORT_FILE%" 2>&1
reg query "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\RunOnce" >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

echo ----- Installed Programs ----- >> "%REPORT_FILE%"
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall" /s >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

REM ===== 事件日志 =====
echo [INFO] Collecting event logs...
echo ===== EVENT LOGS ===== >> "%REPORT_FILE%"
echo. >> "%REPORT_FILE%"

echo ----- System Event Log (Last 50 entries) ----- >> "%REPORT_FILE%"
wevtutil qe System /c:50 /rd:true /f:text >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

echo ----- Security Event Log (Last 50 entries) ----- >> "%REPORT_FILE%"
wevtutil qe Security /c:50 /rd:true /f:text >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

echo ----- Application Event Log (Last 50 entries) ----- >> "%REPORT_FILE%"
wevtutil qe Application /c:50 /rd:true /f:text >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

REM ===== 性能和硬件信息 =====
echo [INFO] Collecting performance and hardware information...
echo ===== PERFORMANCE AND HARDWARE ===== >> "%REPORT_FILE%"
echo. >> "%REPORT_FILE%"

echo ----- CPU Information ----- >> "%REPORT_FILE%"
wmic cpu get Name,NumberOfCores,NumberOfLogicalProcessors,MaxClockSpeed /format:csv >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

echo ----- Memory Information ----- >> "%REPORT_FILE%"
wmic memorychip get Capacity,Speed,Manufacturer /format:csv >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

echo ----- System Performance ----- >> "%REPORT_FILE%"
wmic os get TotalVisibleMemorySize,FreePhysicalMemory /format:csv >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

REM ===== 网络安全检查 =====
echo [INFO] Collecting network security information...
echo ===== NETWORK SECURITY ===== >> "%REPORT_FILE%"
echo. >> "%REPORT_FILE%"

echo ----- Firewall Status ----- >> "%REPORT_FILE%"
netsh advfirewall show allprofiles >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

echo ----- Firewall Rules ----- >> "%REPORT_FILE%"
netsh advfirewall firewall show rule name=all >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

echo ----- Network Shares ----- >> "%REPORT_FILE%"
net share >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

echo ----- Network Sessions ----- >> "%REPORT_FILE%"
net session >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

REM ===== PowerShell执行策略和历史 =====
echo [INFO] Collecting PowerShell information...
echo ===== POWERSHELL INFORMATION ===== >> "%REPORT_FILE%"
echo. >> "%REPORT_FILE%"

echo ----- PowerShell Execution Policy ----- >> "%REPORT_FILE%"
powershell -Command "Get-ExecutionPolicy -List" >> "%REPORT_FILE%" 2>&1
echo. >> "%REPORT_FILE%"

echo ----- PowerShell History ----- >> "%REPORT_FILE%"
if exist "%USERPROFILE%\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt" (
    type "%USERPROFILE%\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt" >> "%REPORT_FILE%" 2>&1
)
echo. >> "%REPORT_FILE%"

echo =============================================== >> "%REPORT_FILE%"
echo Report Generation Completed: %date% %time% >> "%REPORT_FILE%"
echo =============================================== >> "%REPORT_FILE%"

echo [INFO] Data collection completed successfully!
echo [INFO] Report saved as: %REPORT_FILE%
echo [INFO] You can now upload this file to the web interface for analysis.

pause