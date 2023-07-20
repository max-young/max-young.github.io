---
layout: post
title: "MySQL Common operation commands"
subtitle: ""
date: 2023-07-20
categories: Database
tags:
  - MySQL
---

- [Basic command](#basic-command)
- [创建](#创建)
- [update](#update)
- [查询](#查询)
- [索引](#索引)
- [状态](#状态)
- [管理](#管理)

### Basic command

- create database

  `CREATE DATABASE menagerie`  
  注意字符集, 可能默认是 ladin 不支持中文, 所以创建 database 时可以指定字符集:  
  `CREATE DATABASE menagerie DEFAULT CHARACTER SET utf8`  
  如果已经创建了 database 想修改呢?  
  `ALTER DATABASE surge CHARACTER SET utf8;`  
  另外, 如果数据表已经创建了, 数据表的字符集还是原来的, 我们还需要修改表:  
  `alter table collection_case CONVERT TO CHARACTER SET utf8;`

- 进入数据库

  `USE ksxing`;

- 显示所有数据库

  `SHOW DATABASES`

- 显示数据库创建命令(数据库属性, 例如编码)

  `show create database surge`

- 显示所有表格

  `SHOW TABLES`

- 显示表的结构

  `DESC table_name`

- 查看当前数据的函数

  `SHOW FUNCTION STATUS`

- 查看表创建过程

  `SHOW CREATE TABLE table_name`

- 查看创建语句

  `-t`忽略创建表格过程

  ```shell
  $ mysqldump -h localhost -u root -P 3306 -t <database name> <table name> --where="id<=100" -p
  ```

- truncate all tables

  <https://stackoverflow.com/questions/1912813/truncate-all-tables-in-a-mysql-database-in-one-command>

  ```shell
  $ mysql -uUSER -pPASSWORD -Nse 'show tables' DATABASE_NAME | while read table; do mysql -uUSER -pPASSWORD -e "truncate table $table" DATABASE_NAME; done
  ```

- 撤销当前命令  
  在输入定界符;之前输入`\c`

<a id="markdown-创建" name="创建"></a>

### 创建

- 创建数据表

  `CREATE TABLE examinees ( *** )`

  标准的创建数据表示例，包括创建索引：

  ```sql
  create table user_login_new
  (id mediumint unsigned not null auto_increment,
  primary key (id),
  user_id mediumint unsigned,
  company_id smallint unsigned,
  login_is_succ tinyint,
  login_device tinyint,
  login_time datetime,
  login_ip varchar(20),
  index login_time_index (id,company_id,login_time))
  ```

### update

- insert row

  ```sql
  > INSERT INTO examinees (`exam_id`,`user_ids`) VALUES (1,'1,2'),(2,'2,3');
  ```

  you should use \` to quote the column name

- 修改行

  ```shell
  update *** set ***=*** where ***
  ```

- 删除表的某个字段

  ```shell
  #删除exam_dep表的is_all字段
  >ALTER TABLE exam_dep DROP COLUMN is_all;
  ```

- 删除表

  ```shell
  DROP TABLE test
  ```

- 复制一个字段的值到另一个字段 `

  ```sql
  Update {your_table} set {source_field} = {object_field} WHERE case;
  ```

- 删除某个字段的所有值

  ```shell
  # 还是用上面的命令
  > UPDATE {your_table} SET {column_field}=NULL;
  ```

- 约束条件删除部分数据

  ```shell
  > delete from exam_dep where department_id='';
  ```

- 修改列的数据类型

  ```shell
  > ALTER TABLE mytb1 MODIFY i FLOAT(5,1) DEFAULT 100;
  ```

- 增加列

  ```shell
  > ALTER TABLE ext_paper_test ADD COLUMN option_peer_score float(5,1) AFTER has_option_peer;
  ```

- 在首列增加 id 列

  ```shell
  > alter table companys_new add column id mediumint unsigned not null auto_increment primary key first;
  ```

- 修改列

  ```shell
  > alter table ext_paper_test change has_option_peer has_option_peer_score enum('1','0') default '0';
  ```

- 删除列

  ```shell
  alter table sub_admin drop column allow_modify;
  ```

- 更改某列数据

  ```shell
  update fix_paper_test set option_peer_score=0 where option_peer_score is null;
  ```

- 清空表（清空后添加数据 id 从 1 开始）

  ```shell
  truncate table ***;
  ```

  如果因为外键的原因 truncate 失败, 则需要这样操作:

  ```bash
  SET FOREIGN_KEY_CHECKS = 0;

  TRUNCATE table1;
  TRUNCATE table2;

  SET FOREIGN_KEY_CHECKS = 1;
  ```

- 将别的表的内容复制到本表

  ```shell
  > insert into [table] (valueA,valueB) select valueA,valueB from [table2]
  ```

- 删除某条数据

  ```shell
  > delete from *** where id = *
  ```

- 修改表名

  ```shell
  > alter table *** rename to ***
  ```

- 更新时间

  ```sql
  > update exam_results set end_time =date_add(end_time,interval 1 hour) where exam_info_id=20536;

  ```

  date_add 是增加时间
  date_sub 是减少时间

- truncate all tables

  ```sql
  $ mysql -Nse 'show tables' DATABASE_NAME | while read table; do mysql -e "truncate table $table" DATABASE_NAME; done

  ```

- 替换某个字段的某些字符

  [MySQL search and replace some text in a field](https://stackoverflow.com/questions/125230/mysql-search-and-replace-some-text-in-a-field)

  ```sql
  > UPDATE table_name SET field = REPLACE(field, 'foo', 'bar') WHERE INSTR(field, 'foo') > 0;
  ```

<a id="markdown-查询" name="查询"></a>

### 查询

- 查询格式化显示  
  加上`\G`  
  `select * from version where ver_map_tile_id = 2479\G;`

- 跨表查询

  ```sql
  > select a.company_id, b.company_name from user_pay as a companys_new as b where a.company_id = b.id;

  ```

- 模糊查询

  ```sql
  > select * from companys_new where domain like "%gaoxiaobang.com%";
  ```

- left join query column not in another table

  ```sql
  > select * from users left join department_user on users.id=department_user.user_id where users.company_id=949 and department_user.user_id is null;
  ```

- 检索前五行数据

  ```sql
  > SELECT * FROM examinees ORDER BY id LIMIT 5;
  ```

- 联合查询

  ```sql
  > select users.user_name,exam_results.results from users,exam_results where users.id=exam_results.user_id and exam_results.exam_info_id=19256 into outfile '/tmp/hunan15.csv';
  ```

- 联合查询 1

  ```sql
  > select companys_new.id,companys_new.company_name, max(user_login_new.login_time) from companys_new left join user_login_new on (companys_new.id=user_login_new.company_id) order by companys_new.id limit 230,10;
  ```

- 联合查询 2

  ```sql
  > select companys_new.id,companys_new.company_name,max(user_login_new.login_time) from companys_new, user_login_new where companys_new.id=user_login_new.company_id and user_login_new.login_time>="2016-07-01 00:00:00" and user_login_new.login_time<="2016-08-11 00:00:00" group by companys_new.id;
  ```

<a id="markdown-索引" name="索引"></a>

### 索引

```shell
# 单列索引
> alter table table_name add index index_name (column_list) ;
# unique索引
> alter table table_name add unique (column_list);
# primary索引
> alter table table_name add primary key (column_list);
# 全文索引
> alter table table_name add fulltext index index_name (column_list);
# 多列索引
> alter table table_name add index index_name (user, name);
# 删除索引
> DROP INDEX index_name ON tbl_name;
```

<a id="markdown-状态" name="状态"></a>

### 状态

```shell
＃查看mysql的进程，可以观察哪些查询耗时比较高
show processlist
```

<a id="markdown-管理" name="管理"></a>

### 管理

- 显示用户

  `select host, user, password from mysql.user`

- 给用户赋权限

  `grant all on database.* to 'yangle'@'%'`

- 删除用户

  `DROP USER 'jeffrey'@'localhost'`

- 查询数据路径

  `select @@datadir`

- 设置密码

  ```sql
  > SET PASSWORD FOR 'root'@'localhost' = PASSWORD('newpass');
  ```

- 查看端口

  `show global variables like 'port'`
