---
layout: post
title: "SQLAlchemy Can’t reconnect until or mysql server has gone away"
subtitle: ""
date: 2023-09-22
categories: Python
tags:
  - Python
  - Database
  - MySQL
  - ORM
---

在 Python 项目里使用 SQLAlchemy 的时候, 经常会报错, 错误信息是:

```log
StatementError: (sqlalchemy.exc.InvalidRequestError) Can’t reconnect until invalid transaction is rolled back [SQL: ]
```

或者是

```log
raised unexpected: OperationalError(“(_mysql_exceptions.OperationalError) (2006, ‘MySQL server has gone away’)”,)
```

### solve in Django

在 Django 的 settings 文件里是这样配置的:

```python
DATABASES = {
    'base_data': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('BASE_DATA_DB_NAME'),
        'USER': config('BASE_DATA_DB_USER'),
        'PASSWORD': config('BASE_DATA_DB_PASSWORD'),
        'HOST': config('BASE_DATA_DB_HOST'),
        'PORT': config('BASE_DATA_DB_PORT')
    }
}

BASE_DB_CONF = DATABASES.get('base_data')
BASE_DB_ENGINE = create_engine('mysql://{user}:{password}@{host}:{port}/{name}?charset=utf8&autocommit=true'.format(
    user=BASE_DB_CONF.get('USER'), password=BASE_DB_CONF.get('PASSWORD'), host=BASE_DB_CONF.get('HOST'),
    port=BASE_DB_CONF.get('PORT'), name=BASE_DB_CONF.get('NAME')))
BASE_DB_SESSION_MAKER = sessionmaker(bind=BASE_DB_ENGINE)
BASE_DB_SESSION = BASE_DB_SESSION_MAKER()
```

然后在业务代码里面这样执行查询:

```python
from django.conf import settings

settings.BASE_DB_SESSION.execute(activity_sql).fetchall()
```

经过各种 google, 大概查出来原因大概是这样的:

我这样配置的话, 这个 web 应用所有的数据库事务都是用的同一个 session 连接, 且使用的是连接池管理(默认).  
连接池管理意味着就算手动 session.close()也是没有用的, 因为管理权限已经交给了连接池.  
mysql 有 interactive_timeout 参数, 查询到数值是 7200, 也就是 2 小时, 当一个连接空闲超过 2 小时时, 连接就会被回收.  
被回收之后, 这个 session 是错误状态, 没有 rolledback, committed, 或者 closed, 再次使用此 session 来进行操作时, 就会报上面的错误

在 sqlalchemy 的文档里是这样说的:

> 1. As a general rule, keep the lifecycle of the session separate and external from functions and objects that access and/or manipulate database data. This will greatly help with achieving a predictable and consistent transactional scope.
> 2. Make sure you have a clear notion of where transactions begin and end, and keep transactions short, meaning, they end at the series of a sequence of operations, instead of being held open indefinitely.

简单的说, 我们需要掌控 session 的 lifecysle, 不要让 session 一直是 open 的状态

那么我就知道上面的代码最大的问题就是: 在整个 web 项目中, 我使用的都是同一个 session, 用于所有的 web 请求和逻辑模块中, 且一直是 open 的状态, 一直到数据库会收到连接池.

那么我们应该怎么处理呢, 有 3 种方法:

1. 增加重连参数配置

   增加`pool_recycle`, 把这个时间设置小于数据库的`interactive_timeout`时间, 在空闲时间 timeout 之前, 就断开重连, 不要让数据库回收.
   例如:

   ```python
   from sqlalchemy import create_engine
   e = create_engine("mysql://scott:tiger@localhost/test", pool_recycle=3600)
   ```

   查询数据库`interactive_timeout`参数可以在 MySQL shell 里使用命令`SHOW SESSION VARIABLES LIKE "%timeout%";`

2. 搞清楚 session 的 scope 范围

   在 web 项目中这个范围很好确定, 就是一个 request 请求, 或者一个逻辑模块, 在开始阶段

3. 代码如何实现呢

   举个例子, 我们在 class 里实例化 session, class 里的所有数据库操作都用这个 session, 这是一个逻辑单元

   ```python
   from django.conf import settings


   class BasicReport:

   def __init__(self):
       self._session = settings.BASE_DB_SESSION_MAKER()

   def _query_activity_data(self)
       activity_sql = f'''
       select * from sale_item_activity
       '''
       activity_data = self._session.execute(activity_sql).fetchall()
       ...
   ```

   在调用这个 class 的函数里, 手动 close 这个 class 的 session

   ```python
   def export_report():
       ......
       report_instance = BasicReport()
       ...
       report_instance._session.close()
       ...
   ```

### solve in flask


```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(app.config.get("SQLALCHEMY_DATABASE_URI"),
                       pool_pre_ping=True)
SessionFactory = sessionmaker(bind=engine)

session = SessionFactory()
session.query(Model).first()
session.close()
```

in flask document, it recommend use celery as this:

```python
def make_celery(app):
    """celery app
    """
    celery = Celery(app.import_name)
    celery.conf.update(app.config["CELERY_CONFIG"])

    class ContextTask(celery.Task):

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
```
if we use SessionFactory, please remove flask app context, else it will raise exception when task complete, because in flask app context, it will close session, but the session may be have closed in your task code.


参考资料:

<https://docs.sqlalchemy.org/en/13/orm/session_basics.html>
<https://docs.sqlalchemy.org/en/13/core/connections.html>
<https://docs.djangoproject.com/en/2.2/topics/db/sql/>
<https://laucyun.com/e246f190cb33e80f18278189722bb633.html>
<http://einverne.github.io/post/2017/05/sqlalchemy-session.html>
<https://djangostars.com/blog/merging-django-orm-with-sqlalchemy-for-easier-data-analysis/>
<https://farer.org/2017/10/28/sqlalchemy_scoped_session/>
