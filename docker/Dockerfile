# 使用官方Python镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制项目文件
COPY . .

# 安装依赖
RUN pip install -r requirements.txt

# 暴露Gradio应用端口
EXPOSE 7860

# 启动Gradio应用
CMD ["python", "ui/gradio_app.py"]