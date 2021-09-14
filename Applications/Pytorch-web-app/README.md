# Python示例 - 部署PyTorch模型

本示例引至博文: https://imadelhanafi.com/posts/train_deploy_ml_model/

最终效果：

![alt text](https://imadelhanafi.com/data/draft/capture_app_elhanafi.gif)

---



## 第 1 步：本地构建镜像

创建名为 `flaskml` 的新目录，下载文件到此目录中。

如果您本地已经安装了 Docker，可以运行以下命令，在本地构建 Docker 镜像：

```
docker build -t flaskml .
```

构建成功后，运行 `docker images`，可以看到构建出的镜像：

```undefined
REPOSITORY       TAG       IMAGE ID         CREATED            SIZE
flaskml          latest    0a477027a038     8 seconds ago      136MB
```

随后您可以将此镜像上传至您的镜像仓库。

## 第 2 步：新建 SaaS 托管自研节点

参考 [新建服务](https://cloud.tencent.com/document/product/1081/50044)，完成 SaaS 托管自研节点的构建。

## 第 3 步：部署 SaaS 托管自研节点服务

参考 [部署服务](https://cloud.tencent.com/document/product/1081/50045)，完成 SaaS 托管自研节点服务的构建。

其中服务端口设置为80。
