---
layout: post
title: "Python try exception with timeout"
subtitle: ""
date: 2022-12-08
categories: Python
tags:
  - Python
---

利用 signal

```python
import signal

def handler(signum, frame):
    raise Exception("timeout")

def push_version():
    import time
    while True:
        print("...")
        time.sleep(1)

signal.signal(signal.SIGALRM, handler)

signal.alarm(10)

try:
    push_version()
except Exception as e:
    if str(e) == "timeout":
        print("timeout")
    else:
        print("eeeeeeeeeee")
```
