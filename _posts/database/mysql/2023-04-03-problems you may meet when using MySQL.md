---
layout: post
title: "problems you may meet when using MySQL"
date: 2023-04-03
categories: Database
tags:
  - Database
  - MySQL
---

- [MySQL too many connections error](#mysql-too-many-connections-error)
- [MySQL server has gone away long byte](#mysql-server-has-gone-away-long-byte)

### MySQL too many connections error

参考资料：  
[http://dba.stackexchange.com/questions/1558/how-long-is-too-long-for-mysql-connections-to-sleep](http://dba.stackexchange.com/questions/1558/how-long-is-too-long-for-mysql-connections-to-sleep)  
[http://stackoverflow.com/questions/19822558/how-to-set-max-connections-in-mysql-programmatically](http://stackoverflow.com/questions/19822558/how-to-set-max-connections-in-mysql-programmatically)  
[http://blog.csdn.net/vip_linux/article/details/9209485](http://blog.csdn.net/vip_linux/article/details/9209485)  
运行 python web 程序时时出现此错误  
而且进 mysql shell 时也进不去，出现此错误

我们用这个命令查询到都有哪些连接：

```shell
show processlist
```

发现有 200 多个 sleep 进程
然后用`SHOW VARIABLES LIKE "max_connections";`查询到只有 214，所以会出现此错误
我们可以修改 mysql 的三个配置

- max_connections
- interactive_timeout
- wait_timetout

分别用下面两个命令可以查询到具体配置:

```shell
show global variables like '%timeout';
SHOW VARIABLES LIKE "max_connections";
```

然后我们可以在不重启 mysql 的情况下，修改这些配置：

```shell
mysql> SET GLOBAL max_connections = 2048;
Query OK, 0 rows affected (0.00 sec)
mysql> SET GLOBAL interactive_timeout = 7200;
Query OK, 0 rows affected (0.00 sec)
mysql> SET GLOBAL wait_timeout = 7200;
Query OK, 0 rows affected (0.00 sec)
```

### MySQL server has gone away long byte

if size of data you want to save in mysql is too large, it will get this error.  
you can query the current size in mysql shell:  
`show variables like '%max_allowed_packet%'`

then change the max_allowed_packet in my.cnf and reatart mysql server.

    ```shell
    [mysqld]
    max_allowed_packet=64M
    ```

or set it in mysql shell:

    ```shell
    mysql> set global max_allowed_packet=64*1024*1024;
    ```
