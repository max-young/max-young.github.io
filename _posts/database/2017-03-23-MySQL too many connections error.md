---
layout:     post
title:      "MySQL too many connections error"
subtitle:   ""
date:       2017-03-23 00:00:00
author:     "alvy"
header-img: "img/post-bg-database1.jpg"
header-mask: 0.3
catalog:    true
tags:
    - database
    - MySQL
---
参考资料：    
[http://dba.stackexchange.com/questions/1558/how-long-is-too-long-for-mysql-connections-to-sleep](http://dba.stackexchange.com/questions/1558/how-long-is-too-long-for-mysql-connections-to-sleep)    
[http://stackoverflow.com/questions/19822558/how-to-set-max-connections-in-mysql-programmatically](http://stackoverflow.com/questions/19822558/how-to-set-max-connections-in-mysql-programmatically)    
[http://blog.csdn.net/vip_linux/article/details/9209485](http://blog.csdn.net/vip_linux/article/details/9209485)    
运行python web程序时时出现此错误    
而且进mysql shell时也进不去，出现此错误

我们用这个命令查询到都有哪些连接：    
```shell
show processlist
```
发现有200多个sleep进程
然后用`SHOW VARIABLES LIKE "max_connections";`查询到只有214，所以会出现此错误 
我们可以修改mysql的三个配置
- max_connections
- interactive_timeout
- wait_timetout    

分别用下面两个命令可以查询到具体配置:    
```shell
show global variables like '%timeout'; 
SHOW VARIABLES LIKE "max_connections";
```
然后我们可以在不重启mysql的情况下，修改这些配置：
```shell
mysql> SET GLOBAL max_connections = 2048;
Query OK, 0 rows affected (0.00 sec)
mysql> SET GLOBAL interactive_timeout = 7200;
Query OK, 0 rows affected (0.00 sec)
mysql> SET GLOBAL wait_timeout = 7200;
Query OK, 0 rows affected (0.00 sec)
```
