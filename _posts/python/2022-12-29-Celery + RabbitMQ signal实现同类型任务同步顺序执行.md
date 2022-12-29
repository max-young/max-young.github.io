---
layout: post
title: "2022-12-29-Celery + RabbitMQ signal实现同类型任务同步顺序执行"
subtitle: ""
date: 2022-12-29
categories: Backend
tags:
  - Python
  - RabbbitMQ
  - Celery
---

task.py 代码如下:

```python
"""
celery appp
"""
import time

from celery import Celery
from celery.signals import before_task_publish

app = Celery('tasks', broker='pyamqp://guest@localhost//')


@before_task_publish.connect
def handler(sender=None, headers=None, body=None, **kwargs):
    task_id = headers["id"]
    x = body[0][0]
    websocket_key = headers.get("websocket_key")
    while True:
        ai = app.control.inspect()
        active_tasks = ai.active().get("celery@yangle-legion")
        idle = True
        for t in active_tasks:
            if t["args"][0] == x and t["id"] != task_id:
                idle = False
        if idle:
            return
        time.sleep(2)


@app.task
def add(x, y):
    """add async task
    """
    print(f"{x} {y} task start")
    for i in range(10):
        time.sleep(1)
        print(f"{x} {y} {i}")
    print(f"result is {x + y}")
    return x + y
```

启动 celery worker:

```bash
celery -A tasks worker --loglevel=INFO --concurrency=10 --logfile=celery.log -D
```

启动 task

```bash
>>> from tasks import add
>>> add.delay(1, 2)
>>> add.delay(1, 3)
```

这两个函数的第一个参数相同, 按照上面的逻辑, 第一个 task 执行完之后, 第二个 task 才会执行  
可以通过日志看到效果:

```bash
tail -f celery.log
```
