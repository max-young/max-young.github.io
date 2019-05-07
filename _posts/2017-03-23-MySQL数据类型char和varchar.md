---
layout:     post
title:      "MySQL数据类型char和varchar"
subtitle:   ""
date:       2017-03-23 00:00:00
author:     "alvy"
header-img: "img/post-bg-database.jpg"
header-mask: 0.3
catalog:    true
tags:
    - database
    - MySQL
---
##### 背景

数据库里有一张users表，存储用户信息，我们需要增加5个字段filed1～field5，作为用户自定义字段    
那么我们应该选择什么数据类型呢？应该是char还是varchar呢？
##### 解决方案

我们先看char和varchar的区别，可以参照此链接：
[MySQL数据库中CHAR与VARCHAR之争](http://www.chinaz.com/program/2011/0503/176896.shtml)    
大概意思是说表面上varchar是变长字符串，有更大的灵活度，但是也会有副作用，同时在实际应用中我发现性能上会有很大问题：    
我刚开始设置的数据类型是varchar(5)（为什么设置成这个，当时脑子不清醒），后来我意识到5太短了，所以我想更改数据表的列类型，用下面的命令：    
`alter table users midify filed1 varchar(60)`
单身悲剧发生了，服务器io激增，导致服务器瘫痪了！！！！为什么呢？参照这里：    
> MySQL’s ALTER TABLE performance can become a problem with very large tables. MySQL performs most alterations by making an empty table with the desired new structure, inserting all the data from the old table into the new one, and deleting the old table. This can take a very long time, especially if you’re short on memory and the table is large and has lots of indexes. Many people have experience with ALTER TABLE operations that have taken hours or days to complete.    

而且数据表里有好几十万条数据    
经过此事件之后，我觉得有必要搞清楚char和varchar的区别了。经过比较之后我决定选用char，那么长度怎么确定呢？我们在MySql的shell里输入下面的语句：    
`> select length("考试星");`    
得到的结果是9，也就是说一个中文字符的长度是3。    
字段的属性大概不会超过20，所以我选择char(60),  执行修改命令：    
`> alter table users modify filed1 char(60);`
几秒钟之后，修改成功，没有导致服务器瘫痪，虽然io有短暂的升高，可见char在性能上应该是优于varchar的
