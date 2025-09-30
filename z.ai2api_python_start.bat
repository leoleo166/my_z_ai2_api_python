@echo off
echo 正在运行 Python 脚本...
python main.py

if errorlevel 1 (
    echo 脚本执行出错！
) else (
    echo 脚本执行完成！
)

pause
