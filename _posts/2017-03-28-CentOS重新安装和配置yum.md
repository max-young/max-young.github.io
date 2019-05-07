---
layout:     post
title:      "CentOS重新安装和配置yum"
subtitle:   ""
date:       2017-03-28 19:36:00
author:     "alvy"
header-img: "img/post-bg-linux.jpg"
header-mask: 0.3
catalog:    true
tags:
    - Linux
    - 运维
---

##### 环境

CentOS 7

##### 问题

新安装的CentOS 7系统用yum安装软件时报错：

```shell
$ yum install git-all
Loaded plugins: langpacks, product-id, search-disabled-repos, subscription-manager
This system is not registered to Red Hat Subscription Management. You can use subscription-manager to register.
There are no enabled repos.
 Run "yum repolist all" to see the repos you have.
 You can enable repos with yum-config-manager --enable <repo>
```

##### 解决办法

参考地址：

[http://tsung.blog.51cto.com/3049036/1625814](http://tsung.blog.51cto.com/3049036/1625814)

[http://fengyuzaitu.blog.51cto.com/5218690/1384796](http://fengyuzaitu.blog.51cto.com/5218690/1384796)

redhat 的更新包只对注册的用户生效，所以我们自己手动更改成CentOS 的更新包

1. 首先查看redhat 7.0系统本身所安装的那些yum 软件包：

   ```shell
   $ rpm -qa | grep yum
   yum-3.4.3-132.el7.noarch
   yum-langpacks-0.4.2-4.el7.noarch
   yum-rhn-plugin-2.0.1-5.el7.noarch
   yum-metadata-parser-1.1.4-10.el7.x86_64
   PackageKit-yum-1.0.7-5.el7.x86_64
   yum-utils-1.1.31-34.el7.noarch
   ```

2. 删除这些软件包:

   ```shell
   $ rpm -e yum-3.4.3-132.el7.noarch --nodeps
   $ rpm -e yum-langpacks-0.4.2-4.el7.noarch --nodeps
   $ rpm -e yum-rhn-plugin-2.0.1-5.el7.noarch --nodeps
   $ rpm -e yum-metadata-parser-1.1.4-10.el7.x86_64 --nodeps
   $ rpm -e PackageKit-yum-1.0.7-5.el7.x86_64 --nodeps
   $ rpm -e yum-utils-1.1.31-34.el7.noarch --nodeps
   ```

3. 进入网易镜像网站找到自己系统所对应的文件包版本更新：

   [http://mirrors.163.com/](http://mirrors.163.com/)

4. 找到自己所需要的版本然后下载：

   ```shell
   $ wget http://mirrors.163.com/centos/7/os/x86_64/Packages/yum-3.4.3-150.el7.centos.noarch.rpm
   $ wget http://mirrors.163.com/centos/7/os/x86_64/Packages/yum-metadata-parser-1.1.4-10.el7.x86_64.rpm
   $ wget http://mirrors.163.com/centos/7/os/x86_64/Packages/yum-utils-1.1.31-40.el7.noarch.rpm
   $ wget http://mirrors.163.com/centos/7/os/x86_64/Packages/yum-updateonboot-1.1.31-40.el7.noarch.rpm
   $ wget http://mirrors.163.com/centos/7/os/x86_64/Packages/yum-plugin-fastestmirror-1.1.31-40.el7.noarch.rpm
   ```

5. 安装软件包：

   ```shell
   $ rpm -ivh yum-*
   ```

   yum依赖高版本的python-urlgrabber，安装过程中可能会出现错误提示：

   ```shell
   $ rpm -ivh yum-*
   warning: yum-3.4.3-150.el7.centos.noarch.rpm: Header V3 RSA/SHA256 Signature, key ID f4a80eb5: NOKEY
   error: Failed dependencies:
   	python-urlgrabber >= 3.10-8 is needed by yum-3.4.3-150.el7.centos.noarch
   ```

   在网易镜像网站找到python-urlgrabber的安装包并下载安装：

   ```shell
   $ wget http://mirrors.163.com/centos/7/os/x86_64/Packages/python-urlgrabber-3.10-8.el7.noarch.rpm
   $ rpm -Uvh python-urlgrabber-3.10-8.el7.noarch.rpm
   warning: python-urlgrabber-3.10-8.el7.noarch.rpm: Header V3 RSA/SHA256 Signature, key ID f4a80eb5: NOKEY
   Preparing...                          ################################# [100%]
   Updating / installing...
      1:python-urlgrabber-3.10-8.el7     ################################# [ 50%]
   Cleaning up / removing...
      2:python-urlgrabber-3.10-7.el7     ################################# [100%]
   ```

   然后再安装yum包，正常安装是这样的：

   ```shell
   $ rpm -ivh yum-*
   warning: yum-3.4.3-150.el7.centos.noarch.rpm: Header V3 RSA/SHA256 Signature, key ID f4a80eb5: NOKEY
   Preparing...                          ################################# [100%]
   Updating / installing...
      1:yum-metadata-parser-1.1.4-10.el7 ################################# [ 20%]
      2:yum-plugin-fastestmirror-1.1.31-4################################# [ 40%]
      3:yum-3.4.3-150.el7.centos         ################################# [ 60%]
      4:yum-updateonboot-1.1.31-40.el7   ################################# [ 80%]
      5:yum-utils-1.1.31-40.el7          ################################# [100%]
   ```

6. 更新repo文件

   参考地址：[http://mirrors.163.com/.help/centos.html](http://mirrors.163.com/.help/centos.html)

   - 下载对应版本repo文件, 放入/etc/yum.repos.d/(操作前请做好相应备份)

   - 修改文件里的对应CentOS分发版本，本例子中将文件里的`$releasever`改成`7`，与网易镜像里的路径对应

   - 生成缓存

     ```shell
     $ yum clean all
     $ yum makecache
     ```

7. 测试安装

   例如：

   ```shell
   $ yum install git-all
   ```

   ​