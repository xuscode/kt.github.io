@echo off
chcp 65001 >nul
REM 构建RSS文件的批处理脚本

echo 开始构建RSS文件...

REM 检查Python是否可用
D:\python_env\python-3.12.4-embed-amd64\python.exe --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误：未找到Python，请确保Python已安装并添加到环境变量
    pause
    exit /b 1
)

REM 运行构建脚本
D:\python_env\python-3.12.4-embed-amd64\python.exe build_rss.py

if %errorlevel% neq 0 (
    echo 构建失败！
    pause
    exit /b 1
)

echo 构建成功！
pause