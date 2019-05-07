---
layout:     post
title:      "MySQL sql_mode"
subtitle:   ""
date:       2017-03-22 00:00:00
author:     "alvy"
header-img: "img/post-bg-database.jpg"
header-mask: 0.3
catalog:    true
tags:
    - database
    - MySQL
---
在往数据库写入数据的时候，有时会出现错误Data truncate，例如：    

```shell
DataError: (DataError) (1265, "Data truncated for column 'status' at row 1") 'INSERT INTO departments (name, `pId`, company_id, status) VALUES (%s, %s, %s, %s)' ('\xe6\x96\xb0\xe5\x88\x86\xe7\xb1\xbb1', 1, 1, 0)
```

这一般是因为插入的数据格式与数据表定义的数据格式不一致导致的，比如数据表定义的格式是`enum('0', '1')`，但是插入的数据是整型1，就会导致这样的错误。    

错误的出现与代码有关，也与mysql的sql_mode有关。如果代码严格遵循数据格式，当然就能避免这样的错误。这样的严格很难做到，比如刚才的例子，我们也是能容许的，这样我们就需要修改mysql的sql_mode。

sql_mode的定义参照官方文档：[http://dev.mysql.com/doc/refman/5.7/en/sql-mode.html](http://dev.mysql.com/doc/refman/5.7/en/sql-mode.html)    

查询sql_mode的命令是（进入MySQL的shell）：

```shell
> SELECT @@GLOBAL.sql_mode;
+------------------------+
| @@global.sql_mode      |
+------------------------+
| NO_ENGINE_SUBSTITUTION |
+------------------------+
> SELECT @@SESSION.sql_mode;
+------------------------+
| @@session.sql_mode     |
+------------------------+
| NO_ENGINE_SUBSTITUTION |
+------------------------+
```

如果mode里面还包含例如`STRICT_TRANS_TABLES`、`STRICT_ALL_TABLES`，就会导致这样的错误，我们需要修改mode，只保留`NO_ENGINE_SUBSTITUTION`，修改命令如下：    

```shell
> SET GLOBAL sql_mode = 'modes';
> SET SESSION sql_mode = 'modes';
```

GLOBAL和SESSION的区别是前者是永久生效，后者临时生效。我们用前者即可。即：    

```shell
> SET GLOBAL sql_mode = 'NO_ENGINE_SUBSTITUTION';
```
