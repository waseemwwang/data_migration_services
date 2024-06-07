# FastAPI Project Template

python3.12
fastapi
pymysql
sqlalchemy
docker
poetry

## 项目clone

```bash
git clone ***
```

## 安装环境

1. 本机安装

```bash
# 依赖本机python3.12版本
# 1. 安装poetry 
pip install poetry
# 2. 安装python包
poetry install
# 3. 配置config.toml 配置文件
vim src/config.toml
# 4. 启动服务
cd src && python main.py
```

2. docker部署

```bash
# 打包镜像
docker build -t xxx .

# 启动容器
# DEPLOY 环境 支持 dev test prod 支持自定义
docker run --name xxx -d -p 8080:8080 -e DEPLOY=dev xxx
```

3. 查看api

浏览器打开 [swagger](127.0.0.1:8080/docs) 即可访问swagger文档
