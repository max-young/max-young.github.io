---
layout:     post
title:      "Python pip的安装与使用"
subtitle:   ""
date:       2017-03-31 11:53:00
author:     "alvy"
header-img: "img/post-bg-deer-hunter.jpg"
header-mask: 0.3
catalog:    true
tags:
    - Python
---

##### 参考资料：

<https://pip.pypa.io/en/stable/installing/#do-i-need-to-install-pip>

##### 环境

CentOS 7

##### 安装

[How to Install Pip on CentOS 7](https://www.liquidweb.com/kb/how-to-install-pip-on-centos-7/)

1. 添加EPEL仓库

   Pip是Extra Packages for Enterprise Linux (EPEL)的一部分，EPEL是RHEL版本的非标准包仓库，安装命令是：

   ```shell
   $ yum install epel-release
   ```

2. 安装

   ```shell
   # 建议先升级包
   $ yum -y update
   # 安装pip及相关依赖包
   $ yum -y install python-pip
   ```

##### 错误解决办法

1. UnicodeDecodeError

   ```shell
   UnicodeDecodeError: 'utf8' codec can't decode byte 0xd5 in position 24: invalid continuation byte
   ```

   <http://stackoverflow.com/questions/25036897/pip-install-unicodedecodeerror>

   解决办法：

   ```shell
   $ export LC_ALL="en_US.UTF-8"
   ```

##### 使用方法

```shell
# 生成需求文件
$ pip freeze >requirements.txt
# 从需求文件安装
$ pip install -r requirements.txt
```

##### 使用中的问题

- PIL

  ```shell
  $ pip install Pillow
  ```

- TypeError: __call__() takes exactly 2 arguments (1 given)

  参照：<http://stackoverflow.com/questions/42029545/pip-is-error-typeerror-call-takes-exactly-2-arguments-1-given>

  ```shell
  $ pip install setuptools==33.1.1
  ```

- command 'gcc' failed with exit status 1

  参照：

  <http://stackoverflow.com/questions/11094718/error-command-gcc-failed-with-exit-status-1-while-installing-eventlet>

  <http://stackoverflow.com/questions/19955775/error-command-gcc-failed-with-exit-status-1-on-centos>

  ```shell
  $ yum -y install gcc gcc-c++ kernel-devel
  $ yum -y install python-devel libxslt-devel libffi-devel openssl-devel
  $ pip install "your python packet"
  ```

- MySQLdb

  参考资料：<http://stackoverflow.com/questions/5178292/pip-install-mysql-python-fails-with-environmenterror-mysql-config-not-found>

  ```shell
  $ pip install Mysql-Python
  # 如果安装不上，则安装下面的软件
  $ yum install -y mysql-devel python-devel python-setuptools
  ```

- memcache

  ```shell
  $ pip install python-memcached
  ```

- yaml

  ```shell
  $ yum install python-yaml
  ```

- weixin.client

  ```shell
  $ pip install python-weixin
  ```

- pandas

  <http://youerning.blog.51cto.com/10513771/1711008>

  ```shell
  $ pip install pandas -i http://pypi.douban.com/simple --trusted-host pypi.douban.com
  或者
  $ pip install pandas -i https://pypi.tuna.tsinghua.edu.cn/simple
  ```

  ​

