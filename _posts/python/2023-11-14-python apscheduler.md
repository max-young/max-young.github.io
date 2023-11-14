---
layout: post
title: "Python APScheduler"
date: 2023-11-14
categories: Backend
tags:
  - Python
---

we can use celery to implement scheduled tasks, but it's too heavy.  
[APScheduler](https://github.com/agronholm/apscheduler) is a lightweight alternative.
it's more advanced than sched and scheduler library.

```python
from apscheduler.schedulers.blocking import BlockingScheduler

from docker_utils.script import update_docker_container

scheduler = BlockingScheduler()

scheduler.add_job(update_docker_container, 'cron', hour=1)

scheduler.start()
```
