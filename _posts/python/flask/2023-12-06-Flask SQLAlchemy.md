---
layout: post
title: "Flask SQLAlchemy"
date: 2023-12-06
categories: Python
tags:
  - Flask
  - Database
  - SQLAlchemy
---

- [lost connection](#lost-connection)
- [NameError: name '\_mysql' is not defined](#nameerror-name-_mysql-is-not-defined)
- [multi database](#multi-database)
- [migrate](#migrate)
- [how to save image in database](#how-to-save-image-in-database)

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

This question is not so simple. For details, please refer to: <https://maxyoung.fun/blog/SQLAlchemy-Can-t-reconnect-or-mysql-server-has-gone-away.html>

#### NameError: name '\_mysql' is not defined

对于 Ubuntu 来说, 需要安装

```shell
sudo apt-get install libmysqlclient-dev
```

#### multi database

flask app need to connect to multiple databases, how to do it?
config can be like this:

```python
SQLALCHEMY_DATABASE_URI = 'mysql://user:password@host:port/databasename?charset=utf8mb4'
SQLALCHEMY_BINDS = {
    'auth': 'mysql://user:password@host:port/badass?charset=utf8mb4',
}
```

db is `db = SQLAlchemy()`, if we execute `db.session.execute(sql)`, it connect to the default database: `SQLALCHEMY_DATABASE_URI`.  
if we want execute sql on another database, we need to use ` db.get_engine(create_app(), "auth").execute(sql).all()`

if above method is not working, try this:

```python
session = db.get_engine('auth').connect()
users = session.exec_driver_sql("select username from auth_user")
session.close()
```

#### migrate

use <https://flask-migrate.readthedocs.io/en/latest/>

- mo nodule named "MysqlDB"  
  `flask db init` may occur error: no module named "MysqlDB", please install `pip install mysqlclient`

- no schema change  
  `flask db migrate` may occur error: no schema changed, please add import model in migrations/env.py. see <https://github.com/miguelgrinberg/Flask-Migrate/issues/378>

- avoid drop table  
  if databse have table that not defined in model, when we migrate and upgrade, it will drop the table. how to avoid?
  in the migrations/env.py file, add this function:

  ```python
  def include_object(object, name, type_, reflected, compare_to):
    if type_ == "table" and reflected and compare_to is None:
        return False
    else:
        return True
  ```

  and modify the `run_migrations_online` function:

  ```python
  def run_migrations_online():
    ...
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            process_revision_directives=process_revision_directives,
            # new line
            include_object=include_object,
            **current_app.extensions['migrate'].configure_args)
    ...
  ```

  reference: <https://alembic.sqlalchemy.org/en/latest/cookbook.html#don-t-generate-any-drop-table-directives-with-autogenerate>

- CommandError: Can't locate revision identified by '...' when migrating using Flask-Migrate
  ```bash
  flask db revision --rev-id e39d16e62810
  flask db migrate
  flask db upgrade
  ```

- ERROR [flask_migrate] Error: Target database is not up to date.

  ```bash
  flask db stamp head
  flask db migrate
  flask db upgrade
  ```

#### how to save image in database

in rich rext editor, we can upload image, two choices:

1. upload image to server, and save image path in database
2. encode image to base64, and save base64 string in database

the second choices. the data will be a long string, so we need to increase the column length.
the String or Text field is not enough, we need to use another filed, like this:

```python
class Article(db.Model):
    ...
    analyse = db.Column(db.LargeBinary(length=(2**32) - 1), doc="分析")
    ...
```

when we save to this filed, we should encode like: `request.form['analyse'].encode('utf-8')`
when we get from this filed, we should decode like: `article.analyse.decode('utf-8')`

Correspondingly, the database needs to set the storage size limit, Refer to this [link](/blog/problems-you-may-meet-when-using-MySQL.html#mysql-server-has-gone-away-long-byte)

Although we can realize saving pictures to the database, this will bring a problem to web applications: browser load data will be very slowly. so the first choice is better.
