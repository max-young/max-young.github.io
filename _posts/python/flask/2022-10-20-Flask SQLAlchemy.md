---
layout:     post
title:      "Flask SQLAlchemy"
date:       2022-10-20
categories: Python
tags:
    - Flask
    - Database
    - SQLAlchemy
---

##### lost connection

在flask项目里有时候会碰到这样的现象:
1. lost connection to MySQL server
2. MySQL server has gone away

可以在配置里加上:
```python
SQLALCHEMY_ENGINE_OPTIONS={
    "pool_size": 100,
    "max_overflow": 20,
    "pool_pre_ping": True,
    "pool_recycle": 3600
}
```

lost connection和pool_pre_ping相关  
server has gone away和pool_recycle相关, 相当于一个小时请求一次mysql server看看server是否正常

##### NameError: name '_mysql' is not defined

对于Ubuntu来是, 需要安装
```shell
sudo apt-get install libmysqlclient-dev
```