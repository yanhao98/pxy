# 使用官方的 Python 镜像作为基础镜像
FROM python:3-slim

# 设置工作目录
WORKDIR /app

# 将当前目录的内容复制到工作目录
COPY . /app

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE 8787

# 使用 Gunicorn 启动 Flask 应用，并配置日志
CMD ["gunicorn", "--bind", "0.0.0.0:8787", "app:app", "--access-logfile", "-", "--error-logfile", "-", "--log-level", "debug", "--timeout", "0"]
