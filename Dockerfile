# 导入python 镜像
FROM python:3.12 as requirements-stage

# 设置工作目录
WORKDIR /tmp

# 安装 Poetry
RUN pip install poetry

# 将 pyproject.toml 和 poetry.lock 文件复制到工作目录
COPY ./pyproject.toml ./poetry.lock* /tmp/

# 导出poetry 依赖
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# 导入python 镜像
FROM python:3.12

# 设置工作目录
WORKDIR /code

# 复制requirements.txt
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

# 安装包 
RUN pip install --upgrade -r /code/requirements.txt --retries 3 --timeout 30

# 将应用程序复制到工作目录
COPY  ./src /code/app

# 暴露端口（根据FASTAPI应用程序进行调整）
EXPOSE 8080

# 设置工作目录
WORKDIR /code/app

# 使用 Poetry 运行 FastAPI 应用程序
CMD ["uvicorn", "app:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8080"]
