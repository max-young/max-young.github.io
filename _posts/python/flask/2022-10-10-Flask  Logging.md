---
layout:     post
title:      "Flask Logging"
date:       2022-10-10
categories: Python
tags:
    - Flask
---

Flask + Gunicorn logging如何配置

```python
gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.INFO)
```

gunicorn有配置log的文件路径, 会写在这个里面.

使用时, 可以这样:
```python
import app
app.logger.info("message")
```
如果不想通过app, 事实上可能会遇到`import app`出现循环import的错误, 那么可以这样:
```python
import logging
logger = logging.getLogger("gunicorn.error")
logger.info("message")
```
