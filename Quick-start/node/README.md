# 物联使能 SaaS 托管 Node.js 示例

## 第 1 步：编写基础应用

创建名为 `helloworld` 的新目录，并转到此目录中：

```sh
mkdir helloworld
cd helloworld
```

创建一个包含以下内容的 `package.json` 文件：

```json
{
  "name": "helloworld",
  "description": "Simple hello world sample in Node",
  "version": "1.0.0",
  "main": "index.js",
  "scripts": {
    "start": "node index.js"
  },
  "author": "Tencent CloudBase",
  "license": "Apache-2.0",
  "dependencies": {
    "express": "^4.17.1"
  }
}
```

在同一目录中，创建一个 `index.js` 文件，并将以下代码行复制到其中：

```js
const express = require("express");
const app = express();

app.get("/", (req, res) => {
  res.send(`Hello World!`);
});

const port = 80;
app.listen(port, () => {
  console.log(`helloworld: listening on port ${port}`);
});
```

此代码会创建一个基本的 Web 服务器，侦听 `80` 端口。

## 第 2 步：将应用容器化

在项目根目录下，创建一个名为 `Dockerfile` 的文件，内容如下：

```docker
# 使用官方 Node.js 12 轻量级镜像.
# https://hub.docker.com/_/node
FROM node:12-slim

# 定义工作目录
WORKDIR /usr/src/app

# 将依赖定义文件拷贝到工作目录下
COPY package*.json ./

# 以 production 形式安装依赖
RUN npm install --only=production

# 将本地代码复制到工作目录内
COPY . ./

# 启动服务
CMD [ "node", "index.js" ]
```

添加一个 `.dockerignore` 文件，以从容器映像中排除文件：

```undefined
Dockerfile
.dockerignore
node_modules
npm-debug.log
```

## 第 3 步：本地构建镜像

如果您本地已经安装了 Docker，可以运行以下命令，在本地构建 Docker 镜像：

```sh
docker build -t helloworld .
```

构建成功后，运行 `docker images`，可以看到构建出的镜像：

```undefined
REPOSITORY     TAG       IMAGE ID         CREATED          SIZE
helloworld   latest    1c8dfb88c823     8 seconds ago      146MB
```

随后您可以将此镜像上传至您的镜像仓库。

## 第 4 步：新建 SaaS 托管自研节点

参考 [新建服务](https://cloud.tencent.com/document/product/1081/50044)，完成 SaaS 托管自研节点的构建。

## 第 5 步：部署 SaaS 托管自研节点服务

参考 [部署服务](https://cloud.tencent.com/document/product/1081/50045)，完成 SaaS 托管自研节点服务的构建。

## 第 6 步：访问服务

完成上述步骤后，单击【服务配置】进入服务配置页面，点击【公网访问地址】的跳转链接，即可访问 SaaS 的前端页面。

<img src="https://main.qcloudimg.com/raw/9e3dabf221344c2c1d70f6d01f946871.jpg" alt="" style="" />

