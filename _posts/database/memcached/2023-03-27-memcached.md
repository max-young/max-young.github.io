---
layout: post
title: "Memcached"
date: 2023-03-27
categories: Database
tags:
  - Memcached
---

<!-- TOC -->

- [Linux](#linux)
  - [安装](#安装)
  - [安装过程中常遇到的问题](#安装过程中常遇到的问题)
  - [启动](#启动)
- [Mac](#mac)
- [docker](#docker)
- [client](#client)

<!-- /TOC -->

<a id="markdown-linux" name="linux"></a>

### Linux

<a id="markdown-安装" name="安装"></a>

#### 安装

参照官方文档[https://memcached.org/downloads](https://memcached.org/downloads)

```shell
# 一般安装在/usr/local
$ cd /usr/local
$ wget http://memcached.org/latest
$ tar -zxvf latest
$ cd memcached-1.x.x
# 下面的命令可分开来做，make test可能会出错，可跳过此命令
$ ./configure && make && make test && sudo make install
```

<a id="markdown-安装过程中常遇到的问题" name="安装过程中常遇到的问题"></a>

#### 安装过程中常遇到的问题

1. libevent

   参考资料：[http://71254468.iteye.com/blog/1871036](http://71254468.iteye.com/blog/1871036)

   如果系统没有安装 libevent，安装过程中会提 示，下面为安装 libevent 的过程:

   安装过程参照：

   [https://geeksww.com/tutorials/operating_systems/linux/installation/how_to_install_libevent_on_debianubuntucentos_linux.php](https://geeksww.com/tutorials/operating_systems/linux/installation/how_to_install_libevent_on_debianubuntucentos_linux.php)

   ```shell
   $ cd /usr/local
   # 从官网http://libevent.org/获取安装包地址（右键获取链接即可）,用wget下载
   $ wget https://github.com/libevent/libevent/releases/download/release-2.1.8-stable/libevent-2.1.8-stable.tar.gz
   $ tar xzf libevent-1.4.14b-stable.tar.gz
   $ cd libevent-1.4.14b-stable
   $ ./configure --prefix=/opt/libevent
   # hopefully, you haven't encountered any errors so far
   $ make
   # make install
   ```

   继续安装还会提示：

   ```shell
   checking for libevent directory… configure: error: libevent is required. You can get it from http://www.monkey.org/~provos/libevent/
   If it’s already installed, specify its path using –with-libevent=/dir/
   ```

   还需要安装相应的开发所用的头文件

   ```shell
   $ yum install libevent-devel
   ```

2. GCC 编译器

   运行`./configure`时出现：

   ```shell
   configure: error: no acceptable C compiler found in $PATH
   ```

   只是因为缺少 GCC 编译器，Yum 安装即可：

   ```shell
   $ yum install gcc
   ```

3. prove: Command not found

   参考资料：[http://sgq0085.iteye.com/blog/2088440](http://sgq0085.iteye.com/blog/2088440)

   错误提示：

   ```shell
   prove ./t
   make: prove: Command not found
   make: *** [test] Error 127
   ```

   需要安装 perl-Test\*

   ```
   $ yum install perl-Test*
   ```

<a id="markdown-启动" name="启动"></a>

#### 启动

```
# 守护进程启动服务，指定用户，端口，ip
$ /usr/local/bin/memcached -u root -d -m 1024 -l 127.0.0.1 -p 11211
```

<a id="markdown-mac" name="mac"></a>

### Mac

参照<https://gist.github.com/tomysmile/ba6c0ba4488ea51e6423d492985a7953>

### docker

```shell
docker run --name memcache-surge -d -p 8812:11211 -m 1024m memcached
```

### client

<https://www.shouce.ren/api/view/a/6413>
