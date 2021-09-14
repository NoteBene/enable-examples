# Python示例 - IoT设备数据转发至企业微信

## 第 1 步：编写基础应用

创建名为 `http-python` 的新目录，下载文件到此目录中。

编辑`app/app.py`文件中`explorerHandle(self, body)`函数的目标地址。可设置为企业微信机器Webhook地址或其他地址。

```python
def explorerHandle(self, body):#处理数据函数
    # 设置目标地址
    url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=*********'
    headers = {"Content-Type": "application/json;charset=UTF-8"}
    d = {
        "msgtype": "text",
        "text": {
            "content": body.decode('utf-8')
        }
    }
    # 转发至目标地址
    r = requests.post(url, headers=headers, data=json.dumps(d))
```

## 第 2 步：本地构建镜像

如果您本地已经安装了 Docker，可以运行以下命令，在本地构建 Docker 镜像：

```
docker build -t webhook-python .
```

构建成功后，运行 `docker images`，可以看到构建出的镜像：

```undefined
REPOSITORY           TAG       IMAGE ID         CREATED            SIZE
webhook-python       latest    0a477027a038     8 seconds ago      136MB
```

随后您可以将此镜像上传至您的镜像仓库。

## 第 2 步：新建 SaaS 托管自研节点

参考 [新建服务](https://cloud.tencent.com/document/product/1081/50044)，完成 SaaS 托管自研节点的构建。

## 第 3 步：部署 SaaS 托管自研节点服务

参考 [部署服务](https://cloud.tencent.com/document/product/1081/50045)，完成 SaaS 托管自研节点服务的构建。

其中服务端口设置为80。

完成服务部署后，单击【服务配置】进入服务配置页面，即可获得【公网访问地址】。

<img src="https://main.qcloudimg.com/raw/9e3dabf221344c2c1d70f6d01f946871.jpg" alt="" style="" />

## 第 4 步：设置数据同步

1. 登录 [物联网开发平台控制台](https://console.cloud.tencent.com/iotexplorer) ，进入项目详情页面，单击左侧菜单的【数据同步】进入数据同步页面。

2. 在数据同步页面中，数据同步在未设置时，默认生效状态都为关闭，HTTP 服务地址为空。

   <img src="https://main.qcloudimg.com/raw/ccefb4e1667484c8362108c87f7c2206.png" alt="" style="" />

3. 选择需要设置数据同步的产品，单击设备列表中的【设置】，即可设置该产品需要同步的消息类型及 HTTP 服务 URL。其中URL需要输入上一步骤得到的默认公网访问地址，例如“https://***.ap-guangzhou.service.tcloudbase.com”。

   <img src="https://main.qcloudimg.com/raw/fd5d3496f2ecd2c2db191c5383e76baf.png" alt="" style="zoom: 80%;" />

4. 单击【保存】，跳转到列表页，可开启该产品的【生效状态】，完成该产品的数据同步配置。

本示例使用的是 [数据同步](https://cloud.tencent.com/document/product/1081/40298) 功能，若需要更精细化的数据规则定义，可通过 [数据开发](https://cloud.tencent.com/document/product/1081/40292) 配置数据流规则，并通过自定义推送模块推送至 HTTP 服务 URL。

## 第 5 步：上报设备状态数据

若在物联网开发平台的产品开发的过程中已经绑定实物设备，可直接通过控制设备实现设备状态上报。

若暂无实物设备，可通过 [虚拟设备调试](https://cloud.tencent.com/document/product/1081/34741) 功能完成设备数据上报。

1. 登录 [物联网开发平台控制台](https://console.cloud.tencent.com/iotexplorer) ，单击项目进入项目详情页面，单击【产品开发】> 选择相应产品 >【设备调试】>【虚拟设备调试】进入虚拟设备调试页面。

2. 于虚拟设备操控面板设置相应参数，单击【上报】实现设备状态数据上报。

   <img src="https://main.qcloudimg.com/raw/5dc04f19b2f5b17a23d70a0a76b68004.png" alt=""  />

若一切顺利，则能在将设备状态数据转发至指定url。

![](https://main.qcloudimg.com/raw/2d132feae5a6a1467e00fcb8b035767c.png)
