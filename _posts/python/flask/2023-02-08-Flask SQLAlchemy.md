---
layout: post
title: "Flask SQLAlchemy"
date: 2023-02-08
categories: Python
tags:
  - Flask
  - Database
  - SQLAlchemy
---

- [lost connection](#lost-connection)
- [NameError: name '\_mysql' is not defined](#nameerror-name-_mysql-is-not-defined)
- [multi database](#multi-database)

#### lost connection

在 flask 项目里有时候会碰到这样的现象:

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

lost connection 和 pool_pre_ping 相关  
server has gone away 和 pool_recycle 相关, 相当于一个小时请求一次 mysql server 看看 server 是否正常

#### NameError: name '\_mysql' is not defined

对于 Ubuntu 来是, 需要安装

```shell
sudo apt-get install libmysqlclient-dev
```

#### multi database

flask app need to connect to multiple databases, how to do it?
config can be like this:

```python
SQLALCHEMY_DATABASE_URI = 'mysql://user:password@host:port/databasename?charset=utf8mb4'
SQLALCHEMY_BINDS = {
    'another_database': 'mysql://user:password@host:port/badass?charset=utf8mb4',
}
```

db is `db = SQLAlchemy()`, if we execute `db.session.execute(sql)`, it connect to the default database: `SQLALCHEMY_DATABASE_URI`.  
if we want execute sql on another database, we need to use ` db.get_engine(create_app(), "another_database").execute(sql).all()`
