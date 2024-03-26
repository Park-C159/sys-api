# 使用官方Python 3.10镜像作为基础镜像
FROM python:3.10

# 设置工作目录。容器中的命令将从此目录运行
WORKDIR /app

# 使容器在启动后保持运行状态，不会退出
CMD ["tail", "-f", "/dev/null"]

