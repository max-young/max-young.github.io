---
layout: post
title: "MySQL query result export CSV"
date: 2025-06-20
categories: Database
tags:
  - Database
  - MySQL
---

1. 查询语句，用到联合查询

   - 例子 1

     ```sql
     select users.user_name,users.surname,exam_results.results from users,exam_results where users.id=exam_results.user_id and exam_results.exam_info_id=19256 into outfile '/tmp/hunan15.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n'
     ```

   - 例子 2

     ```sql
     select users.surname, table2. department_name from users left outer join (select department_user.user_id as user_id,departments.name as department_name from department_user left outer join departments on department_user.department_id=departments.id) as table2 on users.id=table2.user_id limit 300001, 50000 into outfile '/var/lib/mysql-files/users7.csv' FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';
     ```

     涉及到 3 个表：users, department_user, departments。我们需要导出用户姓名和部门名称。

   - 例子 3

     ```sql
     select exam_results.user_id, user_department_info.surname, user_department_info.dep_name, exam_results.results,exam_results.start_time,exam_results.commit_time from exam_results left join  (select table1.id as user_id, table1.surname, table2.name as dep_name from (select users.id, users.surname, du.department_id from users, department_user du where users.id=du.user_id) as table1, departments table2 where table1.department_id=table2.id) as user_department_info on exam_results.user_id=user_department_info.user_id
     ```

2. 问题汇总

   - 导出路径

     导出路径是`/tmp/`，但是问题来了，导出发现 no place left,磁盘空间不足。至于不足的原因我就不知道了。那么我就换个路径导出，结果`Errcode: 13 - Permission denied`

     解决办法

     [http://stackoverflow.com/questions/11463452/where-does-mysql-on-osx-write-outfiles-by-default](http://stackoverflow.com/questions/11463452/where-does-mysql-on-osx-write-outfiles-by-default)

     新建一个路径，更改权限，导出在这里就好了

     ```shell
     $ cd /usr/local
     $ mkdir DbOutput
     $ sudo chmod -R 777 DbOutput
     ```

   - 导出文件内容不全

     查询结构有 30 多万条记录，一次导出发现只有 6 万多条，文件大小最多到 10M，只能分批导出，一次导 5W 条，加上 limit 限制条件
