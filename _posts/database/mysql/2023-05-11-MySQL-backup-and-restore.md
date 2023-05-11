---
layout: post
title: "MySQL backup and restore"
date: 2023-05-11
categories: DataBase
tags:
  - MySQL
---

- [环境](#环境)
- [物理备份与还原](#物理备份与还原)
- [mysqldump 备份与还原](#mysqldump-备份与还原)
  - [单个数据库备份](#单个数据库备份)

### 环境

MySQL 5.6

### 物理备份与还原

将原有数据全部打包复制到新的路径，下面以将数据库复制到另外一个服务器为例:  
原服务器:

```shell
# 打包数据文件，路径为MySQL的数据路径，位置参照配置文件/etc/my.cnf
$ ls
auto.cnf  ibdata1  ib_logfile0  ib_logfile1  ib_logfile2  ksxing  mysql  performance_schema  ruiyi.pid
$ tar cvf backup_data.tar /data
# scp到新的服务器
```

新服务器:

```shell
# 新服务器创建好空的数据路径，启动mysqld服务
$ service mysqld start
#清空数据路径下的内容，然后将原有数据内容复制进去
$ rm data/*
$ cp -r backip_data/* data/
# 重新启动mysqld服务
$ service mysqld restart
```

启动可能会出现错误，查看 mysql.err 日志:

```text
2017-03-06 11:47:11 25868 [ERROR] InnoDB: auto-extending data file ./ibdata1 is of a different size 4864 pages (rounded down to MB) than specified in the .cnf file: initial 6400 pages, max 0 (relevant if non-zero) pages!
2017-03-06 11:47:11 25868 [ERROR] InnoDB: Could not open or create the system tablespace. If you tried to add new data files to the system tablespace, and it failed here, you should now edit innodb_data_file_path in my.cnf back to what it was, and remove the new ibdata files InnoDB created in this failed attempt. InnoDB only wrote those files full of zeros, but did not yet use them in any way. But be careful: do not remove old data files which contain your precious data!
2017-03-06 11:47:11 25868 [ERROR] Plugin 'InnoDB' init function returned error.
2017-03-06 11:47:11 25868 [ERROR] Plugin 'InnoDB' registration as a STORAGE ENGINE failed.
2017-03-06 11:47:11 25868 [ERROR] Unknown/unsupported storage engine: INNODB
2017-03-06 11:47:11 25868 [ERROR] Aborting
```

修改配置文件`/etc/my.cnf`，增加或修改为：

```text
# 大小要小于等于实际的ibdata的大小
innodb_data_file_path = ibdata1:76M:autoextend
```

重新启动 mysqld 服务，进入 mysql 查看数据是否存在

### mysqldump 备份与还原

参考资料：<https://dev.mysql.com/doc/refman/5.6/en/mysqldump-sql-format.html>

<https://dev.mysql.com/doc/refman/5.6/en/mysqldump.html>

- 原服务器备份

  下面的例子是备份 ksxing 数据库的表结构

  ```shell
  $ mysqldump --user root --password --no-data --databases ksxing > mysqldump_ksxing_structure_20170331.sql
  ```

  参数说明：

  |    参数     |             描述             |
  | :---------: | :--------------------------: |
  |   --user    |            用户名            |
  | --password  |             密码             |
  |  --no-data  |       不备份数据表内容       |
  | --databases | 数据库名称，可以写多个数据库 |

- 新服务器还原

  参考资料：<https://dev.mysql.com/doc/refman/5.6/en/reloading-sql-format-dumps.html>

  首先将上面备份的 sql 文件 scp 到新服务器，再进行还原

  ```shell
  $ mysql < mysqldump_ksxing_structure_20170331.sql
  ```

#### 单个数据库备份

导出 kevin 库

```shell
[root@Mysql-node1 ~]# mysqldump -uroot -hlocalhost -p123456 kevin > /opt/kevin.sql
Warning: Using a password on the command line interface can be insecure.
```

导入 kevin 库（前提是 kevin 库要存在，如果没有，在导入前先创建 kevin 空库）

```shell
[root@Mysql-node1 ~]# mysql -uroot -hlocalhost -p123456 kevin < /opt/kevin.sql
Warning: Using a password on the command line interface can be insecure.
```

或者

```shell
mysql> use kevin；
mysql> source /opt/all.sql;
```
