---
layout:     post
title:      "Celery + RabbitMQ实现异步队列"
subtitle:   ""
date:       2019-06-27
categories: backend
tags:
    - Python
    - RabbbitMQ
---

- [参考资料](#参考资料)
- [启动broker](#启动broker)
- [安装Celery](#安装Celery)
- [Celery应用](#celery应用)
- [启动celery worker](#启动celery-worker)
- [触发任务](#触发任务)
- [测试](#测试)


### 参考资料

[用celery和rabbitmq做异步任务调度](https://vosamo.github.io/2016/05/celery-rabbitmq/)  
[celery官方文档](http://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html)  
[任务队列在 Web 服务里的应用](http://blog.csdn.net/nicajonh/article/details/53224783)

### 启动broker

- 常规启动RabbitMQ

    环境：macOS10.13
    ```
    $ brew install rabbitmq
    ==> Summary
    🍺  /usr/local/Cellar/rabbitmq/3.7.4: 232 files, 12.6MB, built in 2 seconds
    ```
    可以看到安装的路径是`/usr/local/Cellar/rabbitmq/3.7.4`，需要将此路径加入到环境变量里，这样才能直接输入rabbitmq-server启动，而不用输入全部路径，将下面的内容添加到`.zshrc`里（注：不用的shell不同的文件，这里以zsh为例）：
    ```
    PATH=$PATH:/usr/local/Cellar/rabbitmq/3.7.4/sbin
    ```
    启动
    ```shell
    # 守护进程启动服务
    $ sudo rabbitmq-server -detached
    ```

### 安装Celery

```
$ pip install celery
```
如果出现import error的情况，可能是安装的路径不在本机python的路径下，那么按照下面的命令来安装
```
$ python -m pip install celery
```

### Celery应用

创建一个celery应用application, 这个app是入口, 可以创建任务, 管理worker等等
我在Django项目下, 在app目录下创建一个tasks.py文件, 代码示例如下:

```python
from celery import Celery

app = Celery('tasks', broker='pyamqp://guest@localhost//')

@app.task
def add(x, y):
    return x + y
```

### 启动Celery worker

```shell
$ celery -A tasks worker --loglevel=info


celery@bogon v4.2.1 (windowlicker)

Darwin-17.7.0-x86_64-i386-64bit 2019-06-27 11:21:57

[config]
.> app:         tasks:0x10fc01668
.> transport:   amqp://guest:**@localhost:5672//
.> results:     disabled://
.> concurrency: 4 (prefork)
.> task events: OFF (enable -E to monitor tasks in this worker)

[queues]
.> celery           exchange=celery(direct) key=celery


[tasks]
  . mmflowproject.tasks.add

[2019-06-27 11:21:57,401: INFO/MainProcess] Connected to amqp://guest:**@127.0.0.1:5672//
[2019-06-27 11:21:57,428: INFO/MainProcess] mingle: searching for neighbors
[2019-06-27 11:21:58,467: INFO/MainProcess] mingle: all alone
[2019-06-27 11:21:58,487: INFO/MainProcess] celery@bogon ready.
```

`-A`指的是APP，就是当前的tasks.py，如果在某个路径下, 则输入完整路径, 例如`mmflowproject.tasks`, worker后面可以加-c 2制定worker数量
如果要守护进程运行, 需要用到supervisord, 暂且不表

### 触发任务
进入python shell：
```
>>> from tasks import add
>>> add.delay(1, 2)
<AsyncResult: 8d1b69e5-dd51-4194-9d9e-4e5f68a94d81>
```
我们在celery worker下面也会看到日志:
```shell
...
[2019-06-27 11:37:14,038: INFO/MainProcess] Received task: mmflowproject.tasks.add[d4ab8105-d267-4deb-9957-505d8810cddc]
[2019-06-27 11:37:14,047: INFO/ForkPoolWorker-2] Task mmflowproject.tasks.add[d4ab8105-d267-4deb-9957-505d8810cddc] succeeded in 0.0011335039999949004s: 3
```
这样就是一个基本的Celery+RabbitMQ的一个基本的过程

### 测试
测试采用mock的方式, task函数单独测试, 参照官方文档<https://docs.celeryproject.org/en/latest/userguide/testing.html>
