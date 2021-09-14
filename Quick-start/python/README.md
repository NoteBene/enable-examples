# 物联使能 SaaS 托管 Python 示例

## 第 1 步：编写基础应用

创建名为 `helloworld-python` 的新目录，并转到此目录中：

```sh
mkdir helloworld-python
cd helloworld-python
```

创建名为 `main.py` 的文件，并将以下代码粘贴到其中：

```python
import os

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)
```

以上代码会创建一个基本的 Web 服务器，并监听 `80` 端口。

## 第 2 步：将应用容器化

在项目根目录下，创建一个名为 `Dockerfile` 的文件，内容如下：

```docker
# 使用官方 Python 轻量级镜像
# https://hub.docker.com/_/python
FROM python:3.8-slim

# 将本地代码拷贝到容器内
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# 安装依赖
RUN pip install Flask gunicorn

# 启动 Web 服务
# 这里我们使用了 gunicorn 作为 Server，1 个 worker 和 8 个线程
# 如果您的容器实例拥有多个 CPU 核心，我们推荐您把线程数设置为与 CPU 核心数一致
CMD exec gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 main:app
```

添加一个 `.dockerignore` 文件，以从容器映像中排除文件：

```undefined
Dockerfile
README.md
*.pyc
*.pyo
*.pyd
__pycache__
.pytest_cache
```

## 第 3 步：本地构建镜像

如果您本地已经安装了 Docker，可以运行以下命令，在本地构建 Docker 镜像：

```sh
docker build -t helloworld-python .
```

构建成功后，运行 `docker images`，可以看到构建出的镜像：

```undefined
REPOSITORY          TAG       IMAGE ID         CREATED            SIZE
helloworld-python   latest    1c8dfb88c823     8 seconds ago      123MB
```

随后您可以将此镜像上传至您的镜像仓库。

## 第 4 步：新建 SaaS 托管自研节点

参考 [新建服务](https://cloud.tencent.com/document/product/1081/50044)，完成 SaaS 托管自研节点的构建。

## 第 5 步：部署 SaaS 托管自研节点服务

参考 [部署服务](https://cloud.tencent.com/document/product/1081/50045)，完成 SaaS 托管自研节点服务的构建。

## 第 6 步：访问服务

完成上述步骤后，单击【服务配置】进入服务配置页面，点击【公网访问地址】的跳转链接，即可访问 SaaS 的前端页面。

<img src="https://main.qcloudimg.com/raw/9e3dabf221344c2c1d70f6d01f946871.jpg" alt="" style="" />

