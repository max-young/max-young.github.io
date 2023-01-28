---
layout: post
title: "docker image tag latest"
date: 2023-01-17
categories: Docker
tags:
  - Docker
---

参考资料: <https://medium.com/@mccode/the-misunderstood-docker-tag-latest-af3babfd6375>

我关于 docker 镜像的 latest tag 有一些误解, 按照我的第一印象 latest 应该是这个镜像的最新版本, 但是没那么简单, 我们来试验一下:

创建一个简单的 Doockerfile:

```dockerfile
FROM busybox:ubuntu-14.04

ENTRYPOINT ["echo", "version 1"]
```

构建镜像, 不加 tag:

```sh
$ docker build -t max/test .
```

运行检查一下

```sh
$ docker run --rm max/test
version 1
$ docker run --rm max/test:latest
version 1
```

> 加上`--rm`是为了停止镜像之后自动删除容器, 防止多余容器产生

推送到 docker hub

```sh
$ docker push max/test
```

我们登录到 docker hub, 会看到镜像存在, tag 是 latest, 也就是说我没有加版本号的时候, 会默认加上 latest  
我们再修改一下:

```dockerfile
FROM busybox:ubuntu-14.04

ENTRYPOINT ["echo", "version 2"]
```

这次我们构建镜像加上 tag

```sh
$ docker build -t max/test:2 .
```

我们再次运行

```sh
$ docker run --rm max/test
version 1
$ docker run --rm max/test:latest
version 1
$ docker run --rm max/test:2
version2
```

我们看到加上 tag 之后并不会更新本地的 latest  
我们再推送到 docker hub

```sh
$ docker push max/test
```

在 docker hub 上就能看到两个 tag 了: latest 和 2  
我们 pull 下来再运行试试看呢:

```sh
$ docker pull
$ docker run --rm max/test
version 1
$ docker run --rm max/test:latest
version 1
```

有点出乎意料, 我们更新了镜像, 但是 latest 还是 version 1  
不死心, 在 pull 一下 latest

```sh
$ docker pull max/test:latest
$ docker run --rm max/test
version 1
$ docker run --rm max/test:latest
version 1
```

还是一样的结果~~  
我再修改一次, 但是这次不打 tag

```dockerfile
FROM busybox:ubuntu-14.04

ENTRYPOINT ["echo", "version 3"]
```

构建

```sh
$ docker build -t max/test .
```

运行

```sh
$ docker run --rm max/test
version 3
$ docker run --rm max/test:latest
version 3
$ docker run --rm max/test:2
version 2
```

推送到 docker hub 再拉取(在这里其实我们大概就能明白了, 但是还是继续一下多此一举的动作吧)

```sh
$ docker push
$ docker pull max/test
$ docker pull max/test:2
$ docker pull max/test:latest
```

再次运行

```sh
$ docker run alvy/test
version 3
$ docker run alvy/test:latest
version 3
$ docker run alvy/test:2
version 2
```

#### 结论

latest 是最新的不加 tag 的镜像.  
如果加上了 tag, latest 和这些 tag 一样, 都是同等级的 tag, 没有关联
