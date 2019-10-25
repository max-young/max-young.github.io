---
layout:     post
title:      "SQLAlchemy Can’t reconnect until invalid transaction is rolled back问题"
subtitle:   ""
date:       2019-10-25
categories: Python
tags:
    - Python
    - Database
    - MySQL
    - ORM
---

在一个Django项目里使用SQLAlchemy的时候, 经常会报错, 错误信息是:
```log
StatementError: (sqlalchemy.exc.InvalidRequestError) Can’t reconnect until invalid transaction is rolled back [SQL: ]
```
或者是
```log
raised unexpected: OperationalError(“(_mysql_exceptions.OperationalError) (2006, ‘MySQL server has gone away’)”,)
```
在Django的settings文件里是这样配置的:
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
经过各种google, 大概查出来原因大概是这样的:

我这样配置的话, 这个web应用所有的数据库事务都是用的同一个session连接, 且使用的是连接池管理(默认)
连接池管理意味着就算手动session.close()也是没有用的, 因为管理权限已经交给了连接池
mysql有interactive_timeout参数, 查询到数值是7200, 也就是2小时, 当一个连接空闲超过2小时时, 连接就会被回收
被回收之后, 这个session是错误状态, 再次使用此session来进行操作时, 就会报上面的错误

那么我们应该怎么处理呢, 有3种方法:

1. 不使用连接池管理

    在create_engine里增加`poolclass=NullPool`的配置, 示例如下:
    ```python
    from sqlalchemy.pool import NullPool
    engine = create_engine(
              'postgresql+psycopg2://scott:tiger@localhost/test',
              poolclass=NullPool)
    ```
    但是这样的话我们就需要手动干预, 每次执行完事务之后都执行session.close(), 以免再次空闲时间过长, 导致上面的错误
    但是这样增加了太多业务代码, 且容易出错

2. 增加重连参数配置

    增加`pool_recycle`, 把这个时间设置小于数据库的`interactive_timeout`时间, 在空闲时间timeout之前, 就断开重连

    好像很完美的解决了这个问题, 但是这样的话, 我们还是只用到了一个session, 没用充分利用到数据库的连接池

    如果手动再去创建多个session来用的话, 也增加了业务代码复杂度

3. 交给Django去处理

    我们交给Django去处理岂不是更好, 框架已经提供了完整的session管理机制, 我们就不用手动去做管理了.
    之所以我的代码里会手写session, 一是因为我的Django项目里没有写model, 连接是别的项目的数据库, 二是因为还是学艺不精, 对Django不熟啊!! 那么怎样不依赖model来执行数据库事务呢, 示例如下:
    ```python
    from django.db import connections
    with connections['base_data'].cursor() as cursor:
        cursor.execute('select * from sale limit 1')
        row = cursor.fetchone()
    ```
    用with的话执行完之后会自动执行cursor.close()

嗯, 学艺不精的情况下, 还是相信框架吧

参考资料:

<https://docs.sqlalchemy.org/en/13/core/connections.html>  
<https://docs.djangoproject.com/en/2.2/topics/db/sql/>  
<https://laucyun.com/e246f190cb33e80f18278189722bb633.html>  
<http://einverne.github.io/post/2017/05/sqlalchemy-session.html>  
<https://djangostars.com/blog/merging-django-orm-with-sqlalchemy-for-easier-data-analysis/>  
<https://farer.org/2017/10/28/sqlalchemy_scoped_session/>
