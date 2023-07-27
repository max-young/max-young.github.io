---
layout: post
title: "Python PIP"
date: 2023-07-27
categories: Python
tags:
  - Python
---

- [参考资料：](#参考资料)
- [环境](#环境)
- [安装](#安装)
- [错误解决办法](#错误解决办法)
- [使用方法](#使用方法)
- [problems](#problems)

#### 参考资料：

<https://pip.pypa.io/en/stable/installing/#do-i-need-to-install-pip>

#### 环境

CentOS 7

#### 安装

[How to Install Pip on CentOS 7](https://www.liquidweb.com/kb/how-to-install-pip-on-centos-7/)

1. 添加 EPEL 仓库

   Pip 是 Extra Packages for Enterprise Linux (EPEL)的一部分，EPEL 是 RHEL 版本的非标准包仓库，安装命令是：

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

#### 错误解决办法

1. UnicodeDecodeError

   ```shell
   UnicodeDecodeError: 'utf8' codec can't decode byte 0xd5 in position 24: invalid continuation byte
   ```

   <http://stackoverflow.com/questions/25036897/pip-install-unicodedecodeerror>

   解决办法：

   ```shell
   $ export LC_ALL="en_US.UTF-8"
   ```

#### 使用方法

```shell
# 生成需求文件
$ pip freeze >requirements.txt
# 从需求文件安装
$ pip install -r requirements.txt
```

#### problems

- specify a version

  ```shell
  $ pip install "your python packet"==1.0.0
  ```

- PIL

  ```shell
  $ pip install Pillow
  ```

- TypeError: **call**() takes exactly 2 arguments (1 given)

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
  ```

  or

  ```shell
  $ pip install pandas -i https://pypi.tuna.tsinghua.edu.cn/simple
  ```

  or you can add above args to the `requirements.txt` like this:

  ```txt
  -i http://pypi.douban.com/simple
  --trusted-host pypi.douban.com
  gunicorn==20.1.0
  pandas==1.4.4
  ...
  ```

  aliyun mirror is more update than douban mirror, so you can use it:

  ```txt
  -i http://mirrors.aliyun.com/pypi/simple/
  --trusted-host mirrors.aliyun.com
  ...
  ```

- mysqlclient

  error:

  ```log
  No matching distribution found for mysqlclient==2.1.1
  OSError: mysql_config not found
  ERROR: Command errored out with exit status 1: python setup.py egg_info Check the logs for full command output.
  ```

````

need to install libmysqlclient-dev

```bash
sudo apt-get install libmysqlclient-dev
```

- Specify the installation path

  ```bash
  pip install --target=/usr/local/lib/python2.7/dist-packages/ gevent
  ```
````
