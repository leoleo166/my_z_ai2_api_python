# 使用官方的 Python 3.12 slim 版本作为基础镜像
FROM python:3.12-slim

# 设置工作目录为 /app
WORKDIR /app

# 1. 仅复制依赖文件
# 这样做可以利用 Docker 的层缓存机制。只要 requirements.txt 不变，
# 下面的 RUN 指令就不会重新执行，从而加快后续构建速度。
COPY requirements.txt .

# 2. 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 3. 复制项目所有文件到工作目录
# 这里我们将 `..` 修改为 `.`，表示复制构建上下文中的所有内容
# （配合 .dockerignore 效果更佳，见下文优化建议）
COPY . .

EXPOSE 7860

# 4. 指定容器启动时要执行的命令
CMD ["python", "main.py", "--host", "0.0.0.0", "--port", "7860"]
