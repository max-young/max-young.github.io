---
layout:     post
title:      "SQLAlchemy使用"
date:       2022-08-15
categories: Database
tags:
    - Python
    - MySQL
    - SQLAlchemy
---

<!-- TOC -->

- [问题汇总](#问题汇总)
  - [in_查询批量更新时报错](#in_查询批量更新时报错)
  - [server_default 和 default](#server_default-和-default)

<!-- /TOC -->

<a id="markdown-问题汇总" name="问题汇总"></a>
#### 问题汇总

<a id="markdown-in_查询批量更新时报错" name="in_查询批量更新时报错"></a>
##### in_查询批量更新时报错

  参考资料：<https://stackoverflow.com/questions/33703070/using-sqlalchemy-result-set-for-update>

  代码示例：

  ```python
  session.query(cls).filter(cls.id.in_(ids)).update({"password": ******})
  ```

  查询时采用`in_`时，update会报错，错误信息如下:

  ```shell
  InvalidRequestError: Could not evaluate current criteria in Python. Specify 'fetch' or False for the synchronize_session parameter.
  ```

  设置synchronize_session的值为False或者fetch即可

  ```python
  session.query(cls).filter_by(id=id).update({"password": ******}, synchronize_session=False)
  ```

  官方文档参照：<http://docs.sqlalchemy.org/en/latest/orm/query.html?highlight=query.update#sqlalchemy.orm.query.Query.update.params.synchronize_session>

<a id="markdown-server_default-和-default" name="server_default-和-default"></a>
##### server_default 和 default

看这个代码:
```python
from sqlalchemy.sql import func
class Version(Model):
    ...
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
```
为什么time_created用server_default，time_updated用default?  
server_default会更新已有数据, default不会


