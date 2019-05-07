---
layout:     post
title:      "SQLAlchemy使用"
subtitle:   ""
date:       2017-08-04 14:40:00
author:     "alvy"
header-img: "img/post-bg-sqlalchemy.jpg"
header-mask: 0.3
catalog:    true
tags:
    - Python
    - MySQL
---

##### 问题汇总

- in_查询批量更新时报错

  参考资料：<https://stackoverflow.com/questions/33703070/using-sqlalchemy-result-set-for-update>

  代码示例：

  ```python
  session.query(cls).filter(cls.id.in_(ids)).update({"password": new_password})
  ```

  查询时采用`in_`时，update会报错，错误信息如下:

  ```shell
  InvalidRequestError: Could not evaluate current criteria in Python. Specify 'fetch' or False for the synchronize_session parameter.
  ```

  设置synchronize_session的值为False或者fetch即可

  ```python
  session.query(cls).filter_by(id=id).update({"password": new_password}, synchronize_session=False)
  ```

  官方文档参照：<http://docs.sqlalchemy.org/en/latest/orm/query.html?highlight=query.update#sqlalchemy.orm.query.Query.update.params.synchronize_session>

