@echo off
# 指定编码，预防中文乱码
chcp 65001 > nul
echo 正在运行 Python 脚本...
python main.py

if errorlevel 1 (
    echo 脚本执行出错！
) else (
    echo 脚本执行完成！
)

pause
