---
layout: post
title: 'Celery + RabbitMQ实现异步队列'
subtitle: ""
date: 2022-11-24T00:00:00.000Z
categories: Backend
tags:
    - Python
    - RabbbitMQ
---  
  
  
- [参考资料](#参考资料 )
- [启动 broker](#启动-broker )
  - [环境：macOS10.13](#环境macos1013 )
  - [Ubuntu](#ubuntu )
  - [创建用户密码和 virtual host](#创建用户密码和-virtual-host )
- [安装 Celery](#安装-celery )
- [Celery 应用](#celery-应用 )
- [启动 Celery worker](#启动-celery-worker )
- [触发任务](#触发任务 )
- [测试](#测试 )
- [其他](#其他 )
  - [自定义 task id](#自定义-task-id )
  - [根据 id 获取 task](#根据-id-获取-task )
  - [更新 state](#更新-state )
  - [前端获取进度](#前端获取进度 )
  
###  参考资料
  
  
[用 celery 和 rabbitmq 做异步任务调度](https://vosamo.github.io/2016/05/celery-rabbitmq/ )  
[celery 官方文档](http://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html )  
[任务队列在 Web 服务里的应用](http://blog.csdn.net/nicajonh/article/details/53224783 )
  
###  启动 broker
  
  
####  环境：macOS10.13
  
  
```
$ brew install rabbitmq
==> Summary
🍺  /usr/local/Cellar/rabbitmq/3.7.4: 232 files, 12.6MB, built in 2 seconds
```
  
可以看到安装的路径是`/usr/local/Cellar/rabbitmq/3.7.4`，需要将此路径加入到环境变量里，这样才能直接输入 rabbitmq-server 启动，而不用输入全部路径，将下面的内容添加到`.zshrc`里（注：不用的 shell 不同的文件，这里以 zsh 为例）：
  
```
PATH=$PATH:/usr/local/Cellar/rabbitmq/3.7.4/sbin
```
  
启动
  
```shell
# 守护进程启动服务
$ sudo rabbitmq-server -detached
```
  
####  Ubuntu
  
  
```shell
sudo apt-get install rabbitmq-server
```
  
安装之后就自动启动了  
可以用这个命令来看状态
  
```shell
systemctl status rabbitmq-server
```
  
也可以停止和重启
  
####  创建用户密码和 virtual host
  
  
<https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/rabbitmq.html>
  
我们在服务器上运行了 rabbitmq, 可能要供多个应用使用, 那么我们可以给不同应用创建不同的用户和 virtual host:
  
```shell
sudo rabbitmqctl add_user myuser mypassword
sudo rabbitmqctl add_vhost myvhost
sudo rabbitmqctl set_permissions -p myvhost myuser ".*" ".*" ".*"
```
  
之后在应用里的配置需要用到, 上面的文档里也有讲到  
virtual host 的理解: <https://www.cnblogs.com/jxxblogs/p/12260029.html>
  
###  安装 Celery
  
  
```shell
$ pip install celery
```
  
###  Celery 应用
  
  
创建一个 celery 应用 application, 这个 app 是入口, 可以创建任务, 管理 worker 等等
我在 Django 项目下, 在 app 目录下创建一个 tasks.py 文件, 代码示例如下:
  
```python
from celery import Celery
  
app = Celery('tasks', broker='pyamqp://guest@localhost//')
  
@app.task
def add(x, y):
    return x + y
```
  
在 Flask application 里, 可以这么写:
  
```python
from celery import Celery
from celery.schedules import crontab
  
from . import create_app
  
  
def make_celery(flask_app):
    """celery factory
    """
    celery = Celery(flask_app.import_name)
    celery.conf.update(flask_app.config["CELERY_CONFIG"])
  
    class ContextTask(celery.Task):
        """celery task context
        """
  
        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return self.run(*args, **kwargs)
  
    celery.Task = ContextTask
    return celery
  
  
app = make_celery(create_app())
  
app.conf.beat_schedule = {
    'cal_everyday': {
        'task': 'surge.tasks.my_task',
        'schedule': crontab(hour=1),
    },
}
app.conf.timezone = 'Asia/Shanghai'
  
  
@app.task
def cal_task():
    add.delay(1, 2)
  
  
@app.task
def add(x, y):
  print(x + y)
```
  
###  启动 Celery worker
  
  
```shell
celery -A tasks worker --loglevel=info
```
  
`-A`指的是 APP，就是当前的 tasks.py，如果在某个路径下, 则输入完整路径, 例如`mmflowproject.tasks`, worker 后面可以加-c 2 制定 worker 数量
如果要守护进程运行, 需要用到 supervisord, 暂且不表
  
> 在 Django 里面可以加上配置
> `DJANGO_SETTINGS_MODULE='fsp.settings_env' celery -A fsp -l info worker`
  
###  启动 celery beat
  
  
对于定时任务, 如上面的例子, 可以用 celery beat 来启动, 代码示例如下:
  
```shell
celery -A surge.tasks beat
```
  
###  触发任务
  
  
进入 python shell：
  
```shell
>>> from tasks import add
>>> add.delay(1, 2)
<AsyncResult: 8d1b69e5-dd51-4194-9d9e-4e5f68a94d81>
```
  
我们在 celery worker 下面也会看到日志:
  
```shell
...
[2019-06-27 11:37:14,038: INFO/MainProcess] Received task: mmflowproject.tasks.add[d4ab8105-d267-4deb-9957-505d8810cddc]
[2019-06-27 11:37:14,047: INFO/ForkPoolWorker-2] Task mmflowproject.tasks.add[d4ab8105-d267-4deb-9957-505d8810cddc] succeeded in 0.0011335039999949004s: 3
```
  
这样就是一个基本的 Celery+RabbitMQ 的一个基本的过程
  
###  测试
  
  
测试采用 mock 的方式, task 函数单独测试, 参照官方文档<https://docs.celeryproject.org/en/latest/userguide/testing.html>
  
###  其他
  
  
####  自定义 task id
  
  
```python
add.apply_async(args, kwargs, task_id=i)
add.apply_async((1, 4), task_id=i)
```
  
####  根据 id 获取 task
  
  
```python
from celery.result import AsyncResult
from cel.tasks import app
  
task = app.AsyncResult('432890aa-4f02-437d-aaca-1999b70efe8d')
task.state
```
  
####  更新 state
  
  
<https://docs.celeryq.dev/en/latest/userguide/tasks.html#custom-states>
  
根据 id 获取的 task, 如果这个 task 不存在, task 的 state 是 PENDING, 如果 task 还在执行中, state 也是 PENDING, 如何区分呢?  
我们可以更新 task 的 state:
  
```python
@celery.task(bind=True)
def push_version(self, token, task_id, version_name, car_id):
    """往车上推送版本
    """
    self.update_state(state="PROGRESS", meta={"current": 1, "total": 100})
    return
```
  
meta 信息可以通过 task.result 获取
  
####  前端获取进度
  
  
<https://buildwithdjango.com/blog/post/celery-progress-bars/>
  