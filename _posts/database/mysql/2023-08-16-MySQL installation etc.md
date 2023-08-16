---
layout: post
title: "MySQL installation etc"
date: 2023-08-16
categories: Database
tags:
  - MySQL
---

- [安装与卸载](#安装与卸载)
  - [CentOS 7](#centos-7)
    - [卸载 MySQL](#卸载-mysql)
    - [Yum 源安装](#yum-源安装)
    - [启动](#启动)
  - [MacOS](#macos)
    - [安装](#安装)
    - [启动](#启动-1)
    - [shell](#shell)
  - [Ubuntu](#ubuntu)
    - [卸载](#卸载)
    - [安装](#安装-1)
    - [安装 mysql workbench](#安装-mysql-workbench)
- [配置](#配置)
- [QA](#qa)

## 安装与卸载

### CentOS 7

#### 卸载 MySQL

<https://tecadmin.net/remove-mysql-completely-from-linux-system/#>

- 卸载

  `$ yum remove mysql mysql-server`

- 备份或者删除原数据

  如果新安装的 mysql 的数据路径和之前一致, 请确保备货或者删除此路径的数据, 不然启动时可能报错
  `$ mv /var/lib/mysql /var/lib/mysql_old_backup`

- 卸载原有 MySQL 源

  查看是否有安装过：

  ```shell
  $ yum list installed | grep mysql
  mysql-community-client.x86_64           5.7.17-1.el7               @mysql57-community
  mysql-community-common.x86_64           5.7.17-1.el7               @mysql57-community
  mysql-community-libs.x86_64             5.7.17-1.el7               @mysql57-community
  mysql-community-server.x86_64           5.7.17-1.el7               @mysql57-community
  mysql57-community-release.noarch        el7-9                      installed
  ```

  依次卸载：

  ```shell
  $ yum -y remove mysql-community-client.x86_64
  $ yum -y remove mysql-community-common.x86_64
  ```

#### Yum 源安装

> 参考资料：
>
> https://dev.mysql.com/doc/refman/5.6/en/linux-installation-yum-repo.html
>
> https://yq.aliyun.com/articles/47237
>
> http://idroot.net/tutorials/completely-removing-mysql-server-centos/

1. 添加 MySQL Yum 源
   a. 访问 MySQL 官方源页面<http://dev.mysql.com/downloads/repo/yum/>
   b. 下载对应的包
   根据服务器 Linux 内核版本来下载不同的源，例如内核版本是 Linux 3.10.0-327.el7.x86_64，那么我们下载 Red Hat Enterprise Linux 7 / Oracle Linux 7 (Architecture Independent), RPM Package(mysql57-community-release-el7-9.noarch.rpm)，可以通过网页下载，也可以通过 wget 命令下载，下载的地址通过查看网页下载按钮的地址属性即可获得：

   ```shell
   # 下载地址可从页面链接右键获取
   $ wget https://dev.mysql.com/get/mysql57-community-release-el7-10.noarch.rpm
   ```

   c. 安装

   ```shell
   $ yum localinstall mysql57-community-release-el7-10.noarch.rpm
   ```

2. 选择版本
   MySQL Yum 源默认是 MySQL 的最新版本（现在是 5.7），其他版本的源是默认关闭的。我们通过下面的命令查看所有版本的源：
   ```shell
   $ yum repolist all | grep mysql
   mysql-cluster-7.5-community/x86_64 MySQL Cluster 7.5 Community    disabled
   mysql-cluster-7.5-community-source MySQL Cluster 7.5 Community -  disabled
   mysql-connectors-community/x86_64  MySQL Connectors Community     enabled:    30
   mysql-connectors-community-source  MySQL Connectors Community - S disabled
   mysql-tools-community/x86_64       MySQL Tools Community          enabled:    47
   mysql-tools-community-source       MySQL Tools Community - Source disabled
   mysql-tools-preview/x86_64         MySQL Tools Preview            disabled
   mysql-tools-preview-source         MySQL Tools Preview - Source   disabled
   mysql55-community/x86_64           MySQL 5.5 Community Server     disabled
   mysql55-community-source           MySQL 5.5 Community Server - S disabled
   mysql56-community/x86_64           MySQL 5.6 Community Server     disabled
   mysql56-community-source           MySQL 5.6 Community Server - S disabled
   mysql57-community/x86_64           MySQL 5.7 Community Server     enabled:   187
   mysql57-community-source           MySQL 5.7 Community Server - S disabled
   mysql80-community/x86_64           MySQL 8.0 Community Server     disabled
   mysql80-community-source           MySQL 8.0 Community Server - S disabled
   ```
   我们可以看到 5.7enable，其他都是 disable，如果我们需要安装 5.6 版本，可以用下面的命令来关闭 5.7，启用 5.6：
   ```shell
   $ yum-config-manager --disable mysql57-community
   $ yum-config-manager --enable mysql56-community
   ```
3. 安装 Mysql
   ```shell
   $ yum install mysql-community-server
   ```
   插曲：如果是 CentOS6，安装了 el7 包，安装会报错：
   requieres:libc.so.6(glibc_2.17)
   需要安装 el6 包，还要更新包
   $ yum update
   $ yum clean all
   CentOS6 安装 Mysql5.6 参照这里：
   http://www.jianshu.com/p/5a2e4e0b6eda

#### 启动

    $ service mysqld start

<a id="markdown-macos" name="macos"></a>

### MacOS

<a id="markdown-安装" name="安装"></a>

#### 安装

去官网下载 dmg 安装包安装即可, 安装过程中会给'root'@'localhost'用户生成一个密码, 需要记住

<a id="markdown-启动-1" name="启动-1"></a>

#### 启动

在 system preferences 启动  
也可以用命令行启动:  
`$ /usr/local/mysql-5.7.26-macos10.14-x86_64/support-files/mysql.server start`

<a id="markdown-shell" name="shell"></a>

#### shell

mysql 的路径在`/usr/local/`下, 进 shell 的命令是:

```shell
$ /usr/local/mysql-5.7.26-macos10.14-x86_64/bin/mysql -u root -p
```

输入安装时生成的密码即可

<a id="markdown-ubuntu" name="ubuntu"></a>

### Ubuntu

#### 卸载

<https://askubuntu.com/questions/172514/how-do-i-uninstall-mysql>

```shell
sudo systemctl stop mysql
sudo apt-get purge mysql-server mysql-client mysql-common mysql-server-core-* mysql-client-core-*
sudo rm -rf /etc/mysql /var/lib/mysql
sudo apt autoremove
sudo apt autoclean
```

#### 安装

<https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04>

```shell
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql.service
```

之后就可以用 root 登陆了

```shell
sudo mysql
```

这里没有密码, 我们可以设置密码

```sql
> ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
> FLUSH PRIVILEGES;
> SELECT user,authentication_string,plugin,host FROM mysql.user;
```

退出, 重新进入就需要输入密码了

```shell
sudo mysql -p
```

进入之后可以添加用户:

```sql
> CREATE USER 'sammy'@'localhost' IDENTIFIED BY 'password';
> GRANT ALL PRIVILEGES ON *.* TO 'sammy'@'localhost' WITH GRANT OPTION;
```

user consists of username and host, host means where the user can login from, `localhost` means only from localhost, `%` means from anywhere

<a id="markdown-安装mysql-workbench" name="安装mysql-workbench"></a>

#### 安装 mysql workbench

```shell
sudo apt-get install mysql-workbench
```

## 配置

默认配置里数据和日志的路径都是在系统盘，实际工作中我们可能需要放在另外的路径下，如下面的配置文件所示：

```text
[mysqld]
datadir=/mnt/data/mysql/data
socket=/mnt/data/mysql/mysql.sock

symbolic-links=0

sql_mode=NO_ENGINE_SUBSTITUTION

[mysqld_safe]
log-error=/mnt/data/mysql/log/mysqld.log
pid-file=/mnt/data/mysql/mysqld/mysqld.pid
```

我们需要在对应的路径下创建相应路径，在这里我们需要在/mnt/data 下创建 mysql 路径，在 mysql 下创建 log,data,mysqld 等路径，并且需要把整个/mnt/data/mysql 路径的用户组改成 mysql：

```shell
$ chown -R mysql:mysql /mnt/data/mysql
```

## QA

用户不同的环境, 不同的安装方法, 等等都可能导致启动时报错, 要解决这些错误, 首先要定位到错误是什么, 错误信息我们看错误日志就好了, MySQL 的错误日志默认是在`/var/log/mysqld.log`里, 看配置文件`/etc/my.cnf`就知道错误信息时什么

- 没有反应，相应路径也没日志文件和数据文件生成

  - 检查路径所有者，如果不是 mysql，则更改，参照上一部
  - 切换到 mysql 用户，是否能访问数据路径，如果是 Permission Denied，则需要修改路径的权限
    参照：http://unix.stackexchange.com/questions/320011/permission-denied-cd-into-directory
    `$ sudo chmod go+rx /home/work/mysql`
    如果 su - mysql 出现错误 This account is currently not available，则执行下面的语句解决:
    `$ usermod -s /bin/bash mysql`
  - 如果还不行，可以设置 SELinux
    `    vi /etc/selinux/config
set SELINUX=disabled`
    重启服务器

- Fatal error: Can't open and lock privilege tables: Table 'mysql.host' doesn't exist

  查看日志，看到上面的错误信息。一般是由于默认配置文件启动之后，又修改配置文件启动导致，需要初始化数据库
  参照：<http://stackoverflow.com/questions/9083408/fatal-error-cant-open-and-lock-privilege-tables-table-mysql-host-doesnt-ex>

  ```shell
  $ mysql_install_db --user=mysql -ldata=/data/mysql/data
  # 重新启动MySQL服务
  $ service mysqld restart
  ```

- socket

  ```shell
  $ mysql
  ERROR 2002 (HY000): Can't connect to local MySQL server through socket '/var/lib/mysql/mysql.sock' (2)
  ```

  我们发现 socket 的路径还是原有默认路径。因为我们只是修改了服务端的 socket 路径，而没有配置客户端的 socket 路径，修改配置文件，加上客户端 socket 路径，并重新启动 MySQL 服务：
  修改配置文件之后，客户端的 socket 还是原来默认路径的 socket，在配置文件里加上客户端 socket 配置即可：

  ```text
  [client]
  socket=/mnt/data/mysql/mysql.sock
  ```

- InnoDB: space header page consists of zero bytes in data file ./ibdata1

  <http://www.weicot.com/mysql-5-6-%E5%AE%89%E8%A3%85-%E5%90%AF%E7%94%A8-%E5%92%8C%E9%85%8D%E7%BD%AE-innodb-%E7%AD%89/>

  ```shell
  # 切换到数据路径
  $ cd /data
  # 删除下面的文件
  $ rm -rf ibdata1 && rm -rf ib_logfile
  # 初始化
  $ mysql_install_db --user=mysql -ldata=/data/mysql/data
  ```

- Cannot allocate memory for the buffer pool

  ```text
  [ERROR] [MY-012681] [InnoDB] mmap(137428992 bytes) failed; errno 12
  [ERROR] [MY-012956] [InnoDB] Cannot allocate memory for the buffer pool
  ```

  看字面意思是内存不够, 我们查看一下:

  ```shell
  [root@host log]# free -m
                total        used        free      shared  buff/cache   available
  Mem:            503         131         212           1         160         336
  Swap:           131         131           0
  ```

  果然 swap 已用尽, 怎么解决呢, 参照这里:
  <https://stackoverflow.com/questions/10284532/amazon-ec2-mysql-aborting-start-because-innodb-mmap-x-bytes-failed-errno-12>

  Steps below show how to make a swap space for your Micro instance. I assume you have AWS Account with a Micro instance running.

  Run `dd if=/dev/zero of=/swapfile bs=1M count=1024`  
   Run `mkswap /swapfile`  
   Run `swapon /swapfile`  
   Add this line `/swapfile swap swap defaults 0 0` to `/etc/fstab`  
   Step 4 is needed if you would like to automatically enable swap file after each reboot.

- 首次登陆客户端时密码

  首次登陆时, 默认用户是'root'@'localhost', 那么密码是多少呢? 用下面的命令即可获得

  ```shell
  [root@host ~]# sudo grep 'temporary password' /var/log/mysqld.log
  2018-12-23T15:19:10.153004Z 5 [Note] [MY-010454] [Server] A temporary password is generated for root@localhost: BO80Vw0NfI%u
  ```

  登陆进去之后我们可以修改密码:

  ```shell
  mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'Gdfs123';
  ```

  如果新密码强度不够高, 会修改不成功, 提示`ERROR 1820 (HY000): You must reset your password using ALTER USER statement before executing this statement.`
  我们需要修改密码强度:

  ```sql
  mysql> SET GLOBAL validate_password_policy=LOW;
  ```
