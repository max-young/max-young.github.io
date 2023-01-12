---
layout: post
title: "my Docker manual"
date: 2023-01-12
categories: Docker
tags:
  - Docker
---

- [安装](#安装)
- [参考资料](#参考资料)
- [DEMO](#demo)
- [Docker Achitecture](#docker-achitecture)
- [基本命令](#基本命令)
- [创建自定义镜像](#创建自定义镜像)
  - [Dockerfile](#dockerfile)
    - [基本格式](#基本格式)
    - [Parser directives](#parser-directives)
    - [Environment replacement](#environment-replacement)
    - [.dockerignore file](#dockerignore-file)
    - [FROM](#from)
    - [RUN](#run)
    - [CMD 和 ENTRYPOINT 的区别](#cmd-和-entrypoint-的区别)
    - [LABEL](#label)
    - [MAINTAINER](#maintainer)
    - [EXPOSE](#expose)
    - [ENV](#env)
    - [ADD 和 COPY](#add-和-copy)
    - [VOLUME](#volume)
    - [USER](#user)
    - [WORKDIR](#workdir)
- [使用 Docker 构建服务](#使用-docker-构建服务)
- [Docker 编配](#docker-编配)
  - [Docker Compose](#docker-compose)
    - [简单的例子](#简单的例子)
    - [docker compose mysql](#docker-compose-mysql)
    - [docker compose 的基本命令](#docker-compose-的基本命令)

# 初印象

## 安装

<https://docs.docker.com/desktop/install/linux-install/>

## 参考资料

[官方文档](https://docs.docker.com/desktop/)  
[第一本 Docker 书](https://book.douban.com/subject/26285268/)

## DEMO

- Django 应用

  1. demo  
     <https://docs.docker.com/compose/django/#create-a-django-project>
  2. PostgreSQL  
     <https://hub.docker.com/_/postgres/>
  3. 在 docker 里面启动终端运行相关命令  
     How do you perform Django database migrations when using Docker-Compose?
     ```shell
     # 先启动Django应用，可用-d来守护进程启动
     $ docker-compose up
     # 查询到django的container id
     $ docker ps
     # 启动bash
     $ docker exec -i -t 9ff9184c2182 bash
     ```
  4. 连接 PostgreSQL
     ```shell
     $ psql -h postgres -U clm
     ```
     host 默认是 postgres  
     username 和 password 看 docker-compose.yml 里面的配置  
     如果没有安装 psql，则通过`apt-get install postgresql-client`来安装

## Docker Achitecture

image is a read-only template with instructions for creating a Docker container.

## command

- build image

  ```shell
  $ docker build -t my_image .
  ```

  `.` means current path, `-t` means tag, we can use `my_image:tag` to tag image

  if current path has a directory contain large fail, build will be very slow, message is: `build context to Docker daemon 3.314GB`.  
  we can add `.dockerignore` file to ignore some directory

- start a container

  ```shell
  $ docker run --name my_container --rm -it -v host_path:docker_path centos
  ```

  `--name`参数可以为容器命名，也可以不加此参数，命名必需唯一
  `it`参数可以理解为进入命令行界面  
  `-i` support stdin, `-t` support tty bash
  如果本地没有 centos 镜像则会从官方镜像里下载，命令后面还可以加进入容器后的命令，比如`/bin/bash`，`ls`等等，看看效果吧

  `--rm` means auto remove container after exit
  `-v` means mount host path to docker path, we can add third parameter to set permission, for example, `host_path:docker_path:ro` means host_path will mount in docker container docker_path, host_path is sync with docker_path, if we add a file in docker_path in docker container, it will also add in host_path. but we add `:ro`, we cann't do that, we can only read file in docker_path.

- 查看容器

  ```shell
  # 查看运行中的容器
  $ docker ps
  # 查看所有容器
  $ docker ps -a
  ```

  可以查看到容器的信息，比如 id，名称，等等

- 重新启动一个容器

  ```shell
  $ docker restart my_container
  ```

  后面可以加容器的名称，或者容器的 id

- 附着到容器上

  以上面的 centos 容器为例，`docker start`重新启动之后，是守护进程启动，如果我们要进入命令行，可以用附着命令：

  ```shell
  # 可以使容器名称也可以是id
  $ docker attach my_container
  ```

  进入命令行之后 exit，容器也会关闭  
  这里只适用于 centos、ubuntu 这种 linux 镜像  
  如果我们用`docker exec -it my_container bash`进入命令行，exit 后容器不会关闭，下面会讲到

- 查看日志

  守护进程启动 Django 应用，我们可以用下面的命令来查看日志

  ```shell
  # 后面可加上容器名称或者id
  $ docker logs my_container
  # 查看日志实时更新
  $ docker logs -f my_container
  ```

- 查看容器内的进程

  `$ docker top my_container`

- 查看容器的统计信息

  `$ docker stats my_container1 my_container2`

- 在容器内运行进程

  用 docker exec 来实现

  - 在容器内运行后台任务  
    `$ docker exec -d my_container touch /etc/new_file`

  - run command in container
    `$ docker exec -it my_container <command>`
    add `-it` args is better, if not, command standout will not display corrently: Inappropriate ioctl for device

- 停止守护容器

  `$ docker stop my_container`

- 查看容器的详细信息

  `$ docker inspect my_container`

- 删除容器

  `$ docker rm my_container`

- 容器和主机之间复制文件

  `$ docker cp <containerId>:/file/path/within/container /host/path/target`

---

## 创建自定义镜像

镜像可以从官方获取，比如我们以 centos 镜像启动一个仓库，命令是：

```shell
$ docker run -it centos bash
```

docker 会先看本地有没有 docker 镜像，如果没有则从官方获取 centos:latest 镜像

可以指定 centos 的版本，不指定的话默认 latest

进入 bash 之后是一个空的 centos 系统，可以通过`yum install vim`来安装 vim

我们不想每次都安装 vim，可不可以将安装 vim 后的仓库生成一个自定义的镜像呢，这样下次就不用安装 vim 了

这就是自定义镜像的由来，创建自定义镜像的方式有两种，一种是 commit，一种是 Dockerfile, 不推荐 commit 这种方法，具体使用参照文档

### Dockerfile

用 Dockerfile 的方式创建镜像，基本的命令是：

```shell
$ docker build -t max/test .
```

`-t`是指定镜像的仓库和名称，之后是指定 Dockerfile 的路径，这里假定 Dockerfile 是在当前路径

所以用 Dockerfile 的方式创建镜像的步骤是：

```shell
# 创建一个存放Dockerfile的路径
$ mkdir test && cd test
# 创建一个Dockerfile文件
$ vim Dockerfile
# 创建镜像
$ docker build -t max/test .
```

Dockerfile 的内容和规范参照文档<https://docs.docker.com/engine/reference/builder/>

另外, 强烈推荐这个实操文档<https://docs.docker.com/develop/develop-images/dockerfile_best-practices/>

格式说明:

#### 基本格式

```dockerfile
# Comment
INSTRUCTION arguments
```

`#`代表注释  
instruction 可以大小写, 但是为了与 arguments 区分, 最好是大写  
FROM 是必须的, 代表从哪个基本镜像开始构建

#### Parser directives

这个代表如何解析命令, 这个是可选的, 需要在文件的最上面标注, 现在支持两种: syntax 和 escape  
syntax 指定 dockfile 的镜像版本, 一般用不上  
escape 有的时候能用到, 例如默认的 escape 是右下划线\, 我们在 Dockfile 里写入:

```dockerfile
FROM microsoft/nanoserver
COPY testfile.txt c:\\
RUN dir c:\
```

因为默认的 escape 是\\, 所以执行时会报错:

```shell
PS C:\John> docker build -t cmd .
Sending build context to Docker daemon 3.072 kB
Step 1/2 : FROM microsoft/nanoserver
 ---> 22738ff49c6d
Step 2/2 : COPY testfile.txt c:\RUN dir c:
GetFileAttributesEx c:RUN: The system cannot find the file specified.
PS C:\John>
```

如果我们首行记上自定义 escape 的 parser directive 注释, 则会避免这个问题

```dockerfile
# escape=`

FROM microsoft/nanoserver
COPY testfile.txt c:\
RUN dir c:\
```

运行结果是:

```shell
PS C:\John> docker build -t succeeds --no-cache=true .
Sending build context to Docker daemon 3.072 kB
Step 1/3 : FROM microsoft/nanoserver
 ---> 22738ff49c6d
Step 2/3 : COPY testfile.txt c:\
 ---> 96655de338de
Removing intermediate container 4db9acbb1682
Step 3/3 : RUN dir c:\
 ---> Running in a2c157f842f5
 Volume in drive C has no label.
 Volume Serial Number is 7E6D-E0F7

 Directory of c:\

10/05/2016  05:04 PM             1,894 License.txt
10/05/2016  02:22 PM    <DIR>          Program Files
10/05/2016  02:14 PM    <DIR>          Program Files (x86)
10/28/2016  11:18 AM                62 testfile.txt
10/28/2016  11:20 AM    <DIR>          Users
10/28/2016  11:20 AM    <DIR>          Windows
           2 File(s)          1,956 bytes
           4 Dir(s)  21,259,096,064 bytes free
 ---> 01c7f3bef04f
Removing intermediate container a2c157f842f5
Successfully built 01c7f3bef04f
PS C:\John>
```

#### Environment replacement

环境变量替换, 基本用法:

```shell
FROM busybox
ENV foo /bar
WORKDIR ${foo}   # WORKDIR /bar
ADD . $foo       # ADD . /bar
COPY \$foo /quux # COPY $foo /quux
```

上面定义了 foo 这个环境变量的值`/bar`, 在下面就可以使用了, 两种用法`${foo}`和`$foo`都可以, 但是加上 escape 则失效了, 环境变量在下面这些 instruction 里可以使用:

- ADD
- COPY
- ENV
- EXPOSE
- FROM
- LABEL
- STOPSIGNAL
- USER
- VOLUME
- WORKDIR
  如果我们重复定义了同一个环境变量会怎么样呢:

```shell
ENV abc=hello
ENV abc=bye def=$abc
ENV ghi=$abc
```

def 的值会是 hello, ghi 的值会是 bye

#### .dockerignore file

在 Dockerfile 在一个路径下可以定义`.dockerignore`这个文件, 这个文件可以使`ADD`和`COPY`时忽略这个文件里面的内容, `.dockerignore`的内容格式如下:

```shell
# comment
*/temp*
*/*/temp*
temp?
```

#### FROM

是基础镜像, 必需配置, 使用示例:

```shell
ARG  CODE_VERSION=latest
FROM base:${CODE_VERSION}
CMD  /code/run-app

FROM extras:${CODE_VERSION}
CMD  /code/run-extras
```

在 FROM 前面可以配置 ARG 指定镜像版本, 如果没有版本, 则默认 latest

#### RUN

在基础镜像上执行命令, 用于之后的操作, 示例:

```shell
RUN <command>
RUN ["executable", "param1", "param2"]
```

#### CMD 和 ENTRYPOINT 的区别

Dockerfile 里只能有一个 CMD，如果有多个，则执行最后一个 CMD,  
CMD 的主要作用是运行容器时的默认命令, docker run 会执行 CMD，比如 Dockerfile 里有下面的指令：

```shell
CMD [ "/bin/bash" ]
```

运行`docker run -i -t max/test`时，就执行了 CMD 指令进入了 bash  
但是如果我们在 run 里加入命令，比如`docker run -i -t max/test /bin/ps`,则`ps`命令会覆盖掉`bash`命令，不会进入 bash

CMD 有三种格式:

- CMD ["executable","param1","param2"] (exec form, this is the preferred form)
- CMD ["param1","param2"] (as default parameters to ENTRYPOINT)
- CMD command param1 param2 (shell form)

如果是第二种作为 ENTRYPOINT 的参数, 则都需要是这种格式  
如果是第一种, 注意需要是双引号
第三种 shell form 模式默认是在`/bin/sh -c`下执行(sh 是默认的 shell)  
array form is preferred

we can not use CMD in Dockerfile, because we can use CMD in compose.yaml.

如果想每次运行容器时都运行同一个命令, 推荐使用 Entrypoint + CMD 的方式.

我们再来说 ENTRYPOINT  
我们举一个同时使用 ENTRYPOINT 和 CMD 的例子，Dockerfile 包含下面的内容：

```docker
ENTRYPOINT [ "/usr/sbin/nginx" ]
CMD [ "-h" ]
```

docker run 里可以为 ENTRYPOINT 的指令加参数，比如我们运行：

```shell
$ docker run -t -i max/test -g "daemon off;"
```

则会把后面的参数`-g "daemon off";`加到 ENTRYPOINT 的指令`/usr/sbin/nginx`后面  
如果没有加参数，则会把 CMD 里的参数`-h`加到 ENTRYPOINT 的指令后面

官方文档很好的解释了`CMD`和`ENTRYPOINT`的区别:
`CMD`和`ENTYYPOINT`都可以定义启动容器室执行的命令. 两者之间会遵循一些规则:

1. Dockerfile 至少定义两者其中的一个
2. ENTRYPOINT should be defined when using the container as an executable.(这个我没理解)
3. `CMD`可作为`ENTRYPOINT`执行的参数
4. `CMD`在运行容器附加参数时被覆盖掉

当两者结合时的运行规则是这样的:

| No ENTRYPOINT              | ENTRYPOINT                 | exec_entry p1_entry            | ENTRYPOINT [“exec_entry”, “p1_entry”]          |
| -------------------------- | -------------------------- | ------------------------------ | ---------------------------------------------- |
| No CMD                     | error, not allowed         | /bin/sh -c exec_entry p1_entry | exec_entry p1_entry                            |
| CMD [“exec_cmd”, “p1_cmd”] | exec_cmd p1_cmd            | /bin/sh -c exec_entry p1_entry | exec_entry p1_entry exec_cmd p1_cmd            |
| CMD [“p1_cmd”, “p2_cmd”]   | p1_cmd p2_cmd              | /bin/sh -c exec_entry p1_entry | exec_entry p1_entry p1_cmd p2_cmd              |
| CMD exec_cmd p1_cmd        | /bin/sh -c exec_cmd p1_cmd | /bin/sh -c exec_entry p1_entry | exec_entry p1_entry /bin/sh -c exec_cmd p1_cmd |

#### LABEL

给镜像加元数据, 也就是属性, 例如:

```shell
LABEL "com.example.vendor"="ACME Incorporated"
LABEL com.example.label-with-value="foo"
LABEL version="1.0"
LABEL description="This text illustrates \
that label-values can span multiple lines."
```

可以通过`docker inspect`来查看

#### MAINTAINER

镜像拥有者创建者, 这个已过期, 可用 label 替代, 例如:

```shell
LABEL maintainer="SvenDowideit@home.org.au"
```

#### EXPOSE

定义端口去公开, 默认是 TCP 协议, 也可自定义 UDP

#### ENV

环境变量, 两种方式

```docker
ENV key value
ENV key1=value1 key2=value2
```

可以通过`docker inspect`来查看, `docker run --env     key=value`能够改变环境变量

#### ADD 和 COPY

`ADD`和`COPY`功能类似, 都是讲文件添加到容器中, 官方更推荐`COPY`. `COPY`更简单易懂. `ADD`支持一些别的功能, 比如压缩文件添加到容器中时会自动解压缩, 还支持 URL(其实这个功能可以用`RUN curl`来解决)

#### VOLUME

新加卷, 可以存放数据文件, 新加卷的内容会存放到 host 机器上, 用`docker inspect`能查看到位置, 删除容器不会删除 volume 在 host 机器上的文件. `RUN mkdir`这个就不行, 删除容器之后这个路径文件也会没了

VOLUME config in Dockerfile file only create a volume in container, not specify the host path. when you run `docker run` this image and create a container, if you don't use `-v` option to specify the host path, docker will create a directory in host machine, we use `docker inspect [container name]` to check the host path.

#### USER

创建用户和用户组

```docker
USER <user>[:<group>] or
USER <UID>[:<GID>]
```

不指定的话默认 root

#### WORKDIR

`WORKDIR`指定了`RUN`, `CMD`, `ENTRYPOINT`, `COPY`, `ADD`执行的路径, 用法示例:

```shell
WORKDIR /a
WORKDIR b
WORKDIR c
RUN pwd
```

结果会是`/a/b/c`  
在`WORKDIR`里也可使用环境变量

```
ENV DIRPATH /path
WORKDIR $DIRPATH/$DIRNAME
RUN pwd
```

结果会是`/path/$DIRNAME`

## 使用 Docker 构建服务

- 构建 Flask web 应用

  <http://containertutorials.com/docker-compose/flask-simple-app.html>

- 构建 Redis 集群

  参照[《第一本 Docker 书》](https://book.douban.com/subject/26285268/)里面的例子

## Docker 编配

编配（orchestration）是一个没有严格定义的概念。这个概念大概描述了自动配置、协作和管理服务的过程。在 Docker 的世界里，编配用来描述一组实践过程，这个过程会管理运行多个 Docker 容器内的应用，而这些 Docker 容器有可能运行在多个宿主机上。

### Docker Compose

使用 Docker Compose，可以用一个 YAML 文件定义一组要启动的容器，以及运行时的属性，使这些容器能够交互。

#### 简单的例子

下面是一个 Flask web 应用和 Redis 结合的例子：

1.  create flask application

    当前的工作路径是`/composeapp`  
    此路径下新建一个 Flask 应用的 app.py 文件，代码如下所示：

    ```Python
    from flask import Flask
    from redis import Redis

    app = Flask(__name__)
    redis = Redis(host="redis", port=6379)


    @app.route('/')
    def hello():
        redis.incr('hits')
        return 'Hello Docker Book reader!I have been seen {} times'.format(
            int(redis.get('hits')))


    if __name__ == '__main__':
        app.run(host='0.0.0.0', debug=True)
    ```

    可以打看到代码里 web 应用需要连接 Redis，刷新一次主页，计数增加一次
    那么我们应该怎么办呢，单独启动两个容器，一个 Flask 容器，一个 Redis，然后连接起来？手动来做好像太麻烦了，而且中间不知道会遇到什么问题，这个时候就该 docker-compose 登场了

2.  继续新建依赖包文件 requirements.txt

    ```txt
    Flask==2.2.2
    redis==4.4.0
    ```

3.  新建 Dockerfile 用来构建基础镜像，内容如下：

    ```dockerfile
    FROM python:3.9.16
    ADD . /composeapp
    WORKDIR /composeapp
    RUN pip install -r requirements.txt
    ```

    基础镜像是 Python，然后将代码路径加入到镜像里，并安装相关依赖包

4.  创建镜像

    ```shell
    $ docker build --pull --rm -f "Dockerfile" -t composeapp:latest "."
    ```

5.  创建 docker compose 的 yaml 文件 compose.yaml

    内容如下：

    ```yaml
    services:
      web:
        image: composeapp
        command: python app.py
        ports:
          - "5000:5000"
        links:
          - redis
      redis:
        image: redis
    ```

6.  启动服务

    ```shell
    $ docker-compose up
    ```

wo can see the effect with http://localhost:5000/ in the browser

#### docker compose mysql

```yaml
services:
  backend:
    image: <image name>
    ...
    links:
      - database
  database:
    image: mysql:5.7.40
    environment:
      - MYSQL_ROOT_PASSWORD=dockermysql
    ports:
      - 3307:3306
```

mysql environment MYSQL_ROOT_PASSWORD is required.  
we configed ports. wo we can connect the mysql in the container:

```bash
mysql -u root -h 127.0.0.1 -P 3307 -p
```

input the password enter mysql client shell

#### docker compose 的基本命令

- 启动  
   `docker compose up`  
   可以加`-d`后台启动
- 查看进程  
   `docker compose ps`
- 查看日志  
   `docker compose logs`  
   可以加`-f`实时查看
- 停止服务  
   `docker compose stop`
