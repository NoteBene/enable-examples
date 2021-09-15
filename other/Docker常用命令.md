# Docker 常用命令

### 使用 Dockerfile 创建镜像 build

**docker build** 命令用于使用 Dockerfile 创建镜像。

```bash
docker build -t PATH .
```

OPTIONS说明：

> **-t:** 镜像的名字及标签，通常 name:tag 或者 name 格式；可以在一次构建中为一个镜像设置多个标签。
> **-f :**指定要使用的Dockerfile路径，若只输入 . 则代表使用当前目录作为Dockerfile路径；

### 查看镜像 images

查看本地镜像列表

```bash
docker images
```

输出信息实例：

> REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
> ubuntu              latest              d70eaf7277ea        5 days ago          72.9MB

### 拉取镜像 pull

拉取镜像到本地 **images_name**为容器名称，如 ubuntu

```bash
docker pull [images_name]
```

搜索某个需要的镜像，如 ubuntu，则可能有多个版本，此时就可以选择特定的，然后拉取

```bash
docker search [image_name]
```



镜像重命名

```bash
# 具体关于参数，如 IMAGE ID，TAG 等，可以参考“查看本地镜像列表所列出的输出信息”
sudo docker tag [ IMAGE ID]  [REPOSITORY]:[TAG]（仓库：标签）
```

### 查看容器 ps

查看正在运行的容器进程

```bash
sudo docker ps [options]
```

OPTIONS说明：

> -a :显示所有的容器，包括未运行的。
>
> -f :根据条件过滤显示的内容。
>
> --format :指定返回值的模板文件。
>
> -l :显示最近创建的容器。
>
> -n :列出最近创建的n个容器。
>
> --no-trunc :不截断输出。
>
> -q :静默模式，只显示容器编号。
>
> -s :显示总的文件大小。

通常采用的是 -a 参数，示例如下：

```bash
docker ps -a
```

输出信息如下：

> CONTAINER ID        IMAGE        COMMAND        CREATED             STATUS                                     PORTS            NAMES
> 46da53eebf60        ubuntu      "bash"               18 hours ago        Exited (0) 15 hours ago                                jupyterhub

列出所有容器

```bash
sudo docker container ls -a 

# 输出信息
CONTAINER ID        IMAGE        COMMAND        CREATED             STATUS                                     PORTS            NAMES
46da53eebf60        ubuntu      "bash"               18 hours ago        Exited (0) 15 hours ago                                jupyterhub
```

### 运行镜像 run

run 命令可以将“镜像”变成运行状态，它会创建一个容器，然后再进入运行状态，此时就可以使用 docker ps 的命令去判断容器有没有正在运行。

```bash
docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
# 注意：其中的 options 将会决定该容器的运行方式，也可以配置容器的各种环境和执行方式
```

示例：
```bash
sudo docker run -itd -e LANG=C.UTF-8 -v /home:/hosts/home --name=所要定义的容器名称 --privileged=true ubuntu bash
```

privileged=true 的作用是，让容器获得宿主机的 root 权限，这在执行需要 root 权限的命令时将非常有用

最后的 **ubuntu bash** 指的是 镜像名称 以及 执行该镜像下的何种 Shell

注意，镜像是拉取的，可以参考 docker images，所返回的 **REPOSITORY**  即是镜像的名称，通常也翻译成“仓库”，如果有多个重名的镜像，则需要写成这样：REPOSITORY:TAG  即镜像名加上标签。

如：**ubuntu:latest**  bash

注：bash 也可以更换成该容器内的 shell 目录，如 /xxx/bash OR /xxx/zsh

sudo docker run -itd -e LANG=C.UTF-8 -v /home:/hosts/home --name=jupyter_gpu --privileged=true 2a1a442c2ae2  bash

- **run 命令的 OPTIONS 的效用**

```bash
# -a stdin: 指定标准输入输出内容类型，可选 STDIN/STDOUT/STDERR 三项；

#-d: 后台运行容器，并返回容器ID；

# -i: 以交互模式运行容器，通常与 -t 同时使用；

#-P: 随机端口映射，容器内部端口随机映射到主机的端口

# -p: 指定端口映射，格式为：主机(宿主)端口:容器端口

# -t: 为容器重新分配一个伪输入终端，通常与 -i 同时使用；

# --name="nginx-lb": 为容器指定一个名称；

# --dns 8.8.8.8: 指定容器使用的DNS服务器，默认和宿主一致；

# --dns-search example.com: 指定容器DNS搜索域名，默认和宿主一致；

# -h "mars": 指定容器的hostname；

# -e username="ritchie": 设置环境变量；

# --env-file=[]: 从指定文件读入环境变量；

# --cpuset="0-2" or --cpuset="0,1,2": 绑定容器到指定CPU运行；

# -m :设置容器使用内存最大值；

# --net="bridge": 指定容器的网络连接类型，支持 bridge/host/none/container: 四种类型；

# --link=[]: 添加链接到另一个容器；

# --expose=[]: 开放一个端口或一组端口；

# --volume , -v: 绑定一个卷

# --privileged=true 让该容器获取宿主机的 root 权限
```

注意：执行此命令相当于利用了镜像生成了一个容器并进入运行态，如果只是直接 run 而不加上其它指令，比如端口映射规则：-p 80:8080 ，那么新创建的容器是不具备端口映射的功能的，即便访问了 80 端口也无法进入到容器的 8080 服务内容。

当然也包括上述的参数，也就是说，**创建的时候也配置了 docker 容器**，而且不可改动（其实可以，但不一定生效），所以，执行时需要充分考虑此容器未来的情况。



- **修改容器配置**

> Tips：此方案不一定生效

docker 需要一些目录来存放配置信息以及容器数据，以方便再下次启动时使用。

所以我们可以先停止 docker 服务，再找到对应的容器配置，而后改动它的配置文件，再重启即可。

首先查看 docker 的长ID，因为目录名是以长ID为存放的

/var/lib/docker/containers/**[hash_of_the_container]**/hostconfig.json

[hash_of_the_container] 指的是容器的长 ID，而 json 文件则是配置文件了，修改时先停掉相关容器：

```bash
sudo docker stop [container]
# 或者停掉 Docker 服务
sudo service stop docker
```

而后就可以改动此文件了，但是详细配置在此不赘述。

```bash
sudo vim hostconfig.json
```

之后，重新启动容器或服务即可

### 启动容器 start

```bash
sudo docker start [options]
```



### 进入容器 exec

通常情况，当容器启动后，进入到一个容器执行命令是：

```bash
sudo docker exec -it [container] bash
```

> -d :分离模式: 在后台运行
>
> -i :即使没有附加也保持STDIN 打开
>
> -t :分配一个伪终端
>
> bash：表示终端 bash 或者可指定执行的文件等，如 java -jar /xxx.jar。

docker exec -it 71d8e948a96d   bash

### 退出容器 exit



### 文件传入 cp

当需要将本地文件传递给容器时，需要以下命令：

```bash
docker cp [本地文件路径]  ID:容器路径
```

示例  ID 为长ID

```bash
docker cp /home/myfile.zip  46dsfhs....saff:/home
```



### 创建镜像 commit

> 当容器内部的环境、配置等都搭建好了，包括服务也已经正常启动，那么就可以将其打包成一个镜像，将其传到任意环境都可以直接运行了，而不必担心配置或环境问题。

创建之前，先停止掉该容器：

```bash
docker stop [container]
```

提交创建请求，将其创建成一个镜像：

```bash
docker commit [container] [new_image]:[tag]
```

这样，容器就打包成一个镜像了，可以在 docker images 中看见新创建的镜像，容器大小越大，创建的速度也就越慢。



### 导出镜像 save

通过下述代码将镜像保存为压缩包

```bash
docker save -o test.tar 镜像id/name
```

直接生成的压缩包是没有执行权限的，可以通过下述代码赋予权限：

```
chmod 777 test.tar
```

其他权限说明：

> **-rw------- (600) 只有所有者才有读和写的权限**
>
> **-rw-r--r-- (644) 只有所有者才有读和写的权限，组群和其他人只有读的权限**
>
> **-rwx------ (700) 只有所有者才有读，写，执行的权限**
>
> **-rwxr-xr-x (755) 只有所有者才有读，写，执行的权限，组群和其他人只有读和执行的权限**
>
> **-rwx--x--x (711) 只有所有者才有读，写，执行的权限，组群和其他人只有执行的权限**
>
> **-rw-rw-rw- (666) 每个人都有读写的权限**
>
> **-rwxrwxrwx (777) 每个人都有读写和执行的权限**



### 导出容器 export

导出为tar压缩包

```
docker export 容器id/name >文件名.tar
```

导出为二进制文件img

```
docker export -o 文件名.img 容器id/name
```



### 导入镜像 load

```
docker load --input /文件名.tar
```

### 导入容器 import

```
docker import 文件名.img 镜像name
```



**load与import的区别**

- docker load用来载入镜像包，docker import用来载入容器包，但两者都会恢复为镜像；

- docker load不能对载入的镜像重命名，而docker import可以为镜像指定新名称。

注意

> 如果是save导出的镜像, 使用import 导入, 会报 Error: No command specified 错误, 所以使用save导出, 尽量使用load导入, 虽然不能重命名, 但是也比报错强。



### 删除容器/镜像 rm/rmi

- **删除容器**

> 必须先停止运行该容器，才可以删除容器。
>
> ```bash
> docker stop [container]
> ```

删除docker中的容器可以使用如下命令：

```bash
docker rm 容器id
```

- **删除镜像**

> 必须先删除镜像所产生的容器，才可以删除镜像。

删除docker中的镜像，我们可以使用如下命令：

```bash
docker rmi 镜像id
```





