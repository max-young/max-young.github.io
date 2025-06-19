---
layout: post
title: "Celery Config"
date: 2025-06-19
categories: Backend
tags:
  - Python
  - RabbbitMQ
  - Celery
---

start celery command is like this:

```shell
celery -A app.celery worker -c 4 --loglevel=info
```

-c is the number of concurrent processes.  
there is another option `-P` to specify the pool implementation. The default value is `prefork`, which is a process-based pool.  
If you use command `ps aux | grep celery`, you can see 4 processes are started.  
This prefork pool is suitable for CPU-bound tasks.  

If your tasks is IO-bound, you can use `gevent` as the pool implementation and can set more concurrent processes.  
for example, the tasks in my projects contains many rsync and ssh operations, which are IO-bound, then I can use `gevent` to handle more concurrent tasks.
```shell
pip install gevent
celery -A app.celery worker -c 20 -P gevent --loglevel=info
```