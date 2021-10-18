# CI/CD-使用CODING实现SaaS托管自动化部署

## 概述

[物联使能 IoT Enable](https://cloud.tencent.com/product/iotenable) 可以为物联网 SaaS 提供高效、低成本的托管服务。但我们每次在部署服务的时候都需要进行镜像构建、上传，再通过控制台手动更新版本，这些工作是相对机械化，易出错的。为何不将这部分工作交给机器来做呢？仅需要轻点鼠标，起身泡杯咖啡，将部署与发布的事宜交由持续集成，把时间花在更有价值的事物上。

[CODING](https://coding.net/) 持续集成便是专门为此工作流而设计的得力功能。通过对每次提交的代码进行自动化的代码检查、单元测试、编译构建、甚至自动部署与发布，能够大大降低开发人员的工作负担，减少许多不必要的重复劳动，持续提升代码质量与开发效率。

> ### CODING DevOps 是什么
>
> CODING DevOps 是面向软件研发团队的一站式研发协作管理平台，提供从需求到设计、开发、构建、测试、发布到部署的全流程协同及研发工具支撑。CODING 解决方案可助力企业实现代码的统一安全管控，并快速实践敏捷开发与 DevOps，提升软件交付质量与速度，降低企业研发成本，实现研发效能升级。
>
> 更多信息请参考 [CODING DevOps 产品介绍](https://help.coding.net/docs/start/new.html)。
>
> ![](https://help-assets.codehub.cn/enterprise/20210727110654.png)

## 前置条件

在创建自动化部署计划之前，我们需要先在 [CODING](https://coding.net/) 中创建团队及项目。

- [创建或加入CODING团队](https://help.coding.net/docs/start/register-invite.html)
- [新建CODING项目](https://help.coding.net/docs/start/project.html)

同时也需要在 [物联网开发平台控制台](https://console.cloud.tencent.com/iotexplorer) 创建 SaaS 托管的自研节点服务。

- [新建服务](https://cloud.tencent.com/document/product/1081/50044)

## 实施步骤

接下来我们将通过以下三个步骤完成 SaaS 托管自动化部署计划的构建。

- 步骤1：创建计划

- 步骤2：配置工作流

- 步骤3：配置触发规则

### 步骤1：创建计划

1. 打开 [CODING 首页](https://coding.net/)，进入已创建的项目，从左侧导航栏选择「持续集成」-> 「构建计划」。
2. 在「构建计划」页面，点击右上角「创建构建计划」。![img](https://help-assets.codehub.cn/enterprise/20210730105117.png)

3. 选择构建计划模板。本例中选择「构建镜像并推送至 TCR 个人版（容器服务-镜像仓库）」。

   ![image-20211015191821753](https://main.qcloudimg.com/raw/47b54cd3a75583fa77d260d2af0496d2.png)

4. 指定构建计划名称，设置代码仓库与环境变量。

   - 代码仓库

     支持CODING、GitHub、GitLab等多种代码仓库。使用前需要将业务代码及 Dockerfile 存储在代码仓库中。

   - 环境变量

     绑定指定 TCR 镜像仓库，初次使用需要使用腾讯云账号授权。完成绑定后将自动获取镜像仓库的信息作为该项目的环境变量。

     > 建议绑定 SaaS 托管中自研节点服务所对应的镜像仓库。进入自研节点详情页，选择「镜像」-> 「访问镜像仓库」后既能查看对应镜像仓库。

   ![image-20211015192620224](https://main.qcloudimg.com/raw/075fe778e5402f471c81ae9c301d1698.png)

   完成设置后点击「确定」即可创建构建计划。

构建计划创建完成之后，会显示该计划的配置详情页面。您可直接[启动创建并查看构建结果](https://help.coding.net/docs/start/ci.html#start)，确保能够通过代码仓库构建镜像至镜像仓库。

![image-20211015194056068](https://main.qcloudimg.com/raw/f6b83f929ceb656ec79fada2b67a38db.png)

在下一步中，我们将在该计划的基础上继续编排工作流，使其能够实现 SaaS 托管服务的自动化部署。

### 步骤2：配置工作流

1. 进入已创建的项目，从左侧导航栏选择「持续集成」-> 「构建计划」。

2. 在「构建计划」页面，点击构建计划的名称或点击更多图标选择「设置」进入其设置页面。

   ![img](https://help-assets.codehub.cn/enterprise/20210730112311.png)

3. 在「流程配置」页签，点击「3-1 推送镜像」后的「+ 增加阶段」，即可添加新的阶段。

   ![image-20211015194334065](https://main.qcloudimg.com/raw/e75c63e14bc9e6f365881688a44db0c9.png)

4. 在所添加的阶段下点击蓝色 ➕ 加号，点击添加「Python 脚本」任务。

![image-20211015194416912](https://main.qcloudimg.com/raw/2782218c7f62d1989273cfa49f31c109.png)

5. 在脚本内容输入如下 Python 脚本：

   ```python
   import json
   import os
   from tencentcloud.common import credential
   from tencentcloud.common.profile.client_profile import ClientProfile
   from tencentcloud.common.profile.http_profile import HttpProfile
   from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
   from tencentcloud.tcb.v20180608 import tcb_client, models
   try:
       cred = credential.Credential(os.getenv('SecretId'), os.getenv('SecretKey'))
       httpProfile = HttpProfile()
       httpProfile.endpoint = "tcb.tencentcloudapi.com"
   
       clientProfile = ClientProfile()
       clientProfile.httpProfile = httpProfile
       client = tcb_client.TcbClient(cred, "", clientProfile)
   
       req = models.CreateCloudBaseRunServerVersionRequest()
       params = {
           "EnvId": os.getenv('EnvId'),
           "UploadType": "image",
           "FlowRatio": 0,
           "Cpu": 0.25,
           "Mem": 0.5,
           "MinNum": 0,
           "MaxNum": 50,
           "PolicyType": "cpu",
           "PolicyThreshold": 60,
           "ContainerPort": 80,
           "ServerName": os.getenv('ServerName'),
           "ImageInfo": {
               "RepositoryName": os.getenv('DOCKER_REPOSITORY_NAME'),
               "IsPublic": False,
               "TagName": os.getenv('DOCKER_IMAGE_NAME'),
               "ServerAddr": os.getenv('DOCKER_REGISTRY_HOSTNAME'),
               "ImageUrl": os.getenv('DOCKER_REPOSITORY_NAME')+":"+os.getenv('DOCKER_IMAGE_NAME')
           }
       }
       req.from_json_string(json.dumps(params))
   
       resp = client.CreateCloudBaseRunServerVersion(req)
       print(resp.to_json_string())
   
   except TencentCloudSDKException as err:
       print(err)
   ```

   > 上述脚本将调用 SaaS 托管的创建服务版本 API，从而在指定服务中部署0.25核 CPU、0.5 GB 内存的版本，API 详情可参考 [创建服务版本](https://cloud.tencent.com/document/product/876/49627)，可根据需要修改该 Python 脚本。

   接着点击「显示高级选项」，在「requirements.txt」输入框中输入`tencentcloud-sdk-python`。这样在执行该阶段时将自动 pip 安装`tencentcloud-sdk-python`，使得 Python 脚本能够正常执行。

   ![image-20211015200619747](https://main.qcloudimg.com/raw/339755ad76a2a106c5ac5f2d74047a75.png)

6. 在上一步中我们完成了 Python 脚本，但其中的环境变量还没完全定义。

   点击「环境变量」，配置如下环境变量：

   - EnvId：SaaS 的环境 ID。可于自研节点控制台查看。

   - ServerName：自研节点的服务名称。可于自研节点控制台查看。

     ![image-20211018104308091](https://main.qcloudimg.com/raw/2c565955642d5e958a648c13f73fef0e.png)

   - SecretId：通过腾讯云官网获取的 [云 API 密钥](https://console.cloud.tencent.com/cam/capi)。

   - SecretKey：通过腾讯云官网获取的 [云 API 密钥](https://console.cloud.tencent.com/cam/capi)。

   ![image-20211015201207599](https://main.qcloudimg.com/raw/d47e48fae2e3db65bc5cbad7fdd7243e.png)

7. 完成 Python 脚本与环境变量的定义后，点击「保存」，即可点击「立即构建」启动构建并查看构建结果。若配置无误，则可在自研节点控制台查看到有新的版本已创建。

### 步骤3：配置触发规则

完成工作流的创建后，我们还可以根据需要修改触发规则。

1. 进入已创建的项目，从左侧导航栏选择「持续集成」-> 「构建计划」。
2. 在「构建计划」页面，点击构建计划的名称或点击更多图标选择「设置」进入其设置页面。

3. 在「流程配置」页签，即可配置触发规则。CODING 持续集成支持通过多种方式来触发构建计划，可以 [查看完整帮助文档](https://help.coding.net/docs/devops/ci/trigger.html?_ga=2.250869058.533339527.1634267546-1945533476.1632312923)，根据需要进行修改。

   ![image-20211018104915679](https://main.qcloudimg.com/raw/1c9c1850e7143fdeb53151c6d4bd95d9.png)

## MORE

至此，我们已经完整构建了 SaaS 托管的自动化部署工作流，在每次更新代码的时候实现自动更新版本。

当然，本例只是最简单的一个案例，在正式的开发流程中我们还要根据自身业务需求调整该工作流，例如规范发布分支、添加人工确认环境、添加检查脚本、优化部署脚本、优化构建节点等等，使得该工作流能够胜任业务的要求，能够让开发团队流畅协同开发。更多内容可持续关注 [CODING](https://coding.net/) 。

![image-20211018113325209](https://main.qcloudimg.com/raw/e0b7279594e86e53b51e08b13675955e.png)
