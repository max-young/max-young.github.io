---
layout: post
title: "Linux command"
date: 2025-04-18
categories: Linux
tags:
  - CentOS
  - Ubuntu
---

- [shell 以及 bash](#shell-以及-bash)
- [系统相关](#系统相关)
  - [查看 Linux 内核版本和 CentOS 版本](#查看-linux-内核版本和-centos-版本)
  - [User](#user)
- [网络与连接](#网络与连接)
  - [SSH](#ssh)
  - [网络 IP 相关命令](#网络-ip-相关命令)
  - [SCP 文件传输](#scp-文件传输)
  - [开通端口](#开通端口)
  - [下载文件](#下载文件)
  - [curl 请求](#curl-请求)
  - [net status](#net-status)
- [about file](#about-file)
  - [mv file](#mv-file)
  - [查找文件](#查找文件)
  - [file display](#file-display)
  - [archive \& unarchive](#archive--unarchive)
  - [路径](#路径)
  - [磁盘](#磁盘)
  - [创建随机临时文件](#创建随机临时文件)
  - [获取当前路径下某文件的完整路径](#获取当前路径下某文件的完整路径)
  - [根据文件路径获取文件名](#根据文件路径获取文件名)
  - [preview image](#preview-image)
  - [check two file is same](#check-two-file-is-same)
- [进程](#进程)
  - [查看网络状态](#查看网络状态)
  - [重新读取配置文件并重启](#重新读取配置文件并重启)
- [权限](#权限)
  - [无法 cd 到某些路径，Permission Denied](#无法-cd-到某些路径permission-denied)
  - [更改文件的用户](#更改文件的用户)
  - [文件权限](#文件权限)
- [进程](#进程-1)
  - [screen](#screen)
- [日期](#日期)
  - [时间戳转换为日期](#时间戳转换为日期)
- [bash](#bash)
- [grammar](#grammar)

### shell 以及 bash

参考书：[Linux 命令行与 shell 脚本编程大全](https://book.douban.com/subject/11589828/)

- 命令前加上`bash -x`可以输出命令的执行过程  
  [http://macshuo.com/?p=676](http://macshuo.com/?p=676)

- terminal 按 tab 补全异常  
  <https://askubuntu.com/questions/545540/terminal-autocomplete-doesnt-work-properly>

- rbash  
  受限制的 bash

- cursor move
  `Ctrl + [left/right arrow]` move cursor to previous/next word

---


### 系统相关


#### 查看 Linux 内核版本和 CentOS 版本

1. 查看 CentOS 版本

   ```shell
   $ cat /etc/centos-release
   # 或者
   $ cat /etc/redhat-release
   Red Hat Enterprise Linux Server release 7.2 (Maipo)
   ```

2. 查看内核版本

   ```shell
   $ uname -a
   Linux dscn3 3.10.0-327.el7.x86_64 #1 SMP Thu Oct 29 17:29:29 EDT 2015 x86_64 x86_64 x86_64 GNU/Linux
   ```

3. 查看 Ubuntu 版本

   ```shell
   $ lsb_release -a
   ```

4. 查看 CPU 信息

   ```bash
   $ lscpu
   Architecture:        x86_64
   CPU op-mode(s):      32-bit, 64-bit
   Byte Order:          Little Endian
   CPU(s):              8
   On-line CPU(s) list: 0-7
   Thread(s) per core:  2
   Core(s) per socket:  4
   Socket(s):           1
   NUMA node(s):        1
   Vendor ID:           GenuineIntel
   CPU family:          6
   Model:               158
   Model name:          Intel(R) Core(TM) i5-9300H CPU @ 2.40GHz
   Stepping:            10
   CPU MHz:             1144.681
   CPU max MHz:         4100.0000
   CPU min MHz:         800.0000
   BogoMIPS:            4800.00
   Virtualization:      VT-x
   L1d cache:           32K
   L1i cache:           32K
   L2 cache:            256K
   L3 cache:            8192K
   NUMA node0 CPU(s):   0-7
   ...
   ```

   我们可以根据 architecture 来确定下载软件的不同编译版本， 例如 ttyd 的 release 里有很多不同的编译版本: <https://github.com/tsl0922/ttyd/releases>

---

#### User

- 显示用户

  ```shell
  $ cat /etc/passwd
  ```

- 删除用户

  ```shell
  # remove the user’s home directory and mail spool pass the -r option to userdel
  $ userdel -r username
  ```

- add user

  ```shell
  $ sudo adduser <username>
  ```

- 修改用户密码

  ```shell
  # 修改其他用户密码
  sudo passwd <user>
  ```

- add user to the sudo group
  
  ```shell
  $ sudo usermod -aG sudo <username>
  ```

---


### 网络与连接


#### SSH

[How To Use SSH to Connect to a Remote Server in Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-use-ssh-to-connect-to-a-remote-server-in-ubuntu)

我们用`ssh`命令能登录远程服务器，例如：

```shell
$ ssh root@123.45.12.145
```

如果我们只是想测试是否能连通服务器, 用`ssh -q user@downhost exit`命令, 如果能连上那么`$?`等于 0, 否则等于 255

> 需要注意的是，ssh 的默认端口是 22，有的服务器设置的端口不是 22，那么连接的时候就需要指定端口，例如：
>
> ```shell
> $ ssh -p 2222 root@123.45.12.145
> ```

然后系统会提示输入密码，每次输入密码很麻烦，我们可以这样

```bash
$ ssh-copy-id root@123.45.12.145
```

if we not have key, it will get `no identities found error`, because `ssh-copy-id` command is copy out host key to remote server, so we need generate key first:

```bash
ssh-keygen -t rsa
```

ssh user@ip command is too long? we can set it to `~/.ssh/config`:

```bash
Host car18
    Hostname 192.168.2.43
    Port 22
    User apollo
```

if you want to connect a inner server in a bulk server which have one server have outer ip, you can config proxyjump in ssh config:

```text
Host car18
    Hostname 39.13.13.14
    Port 22
    User apollo
Host car18-inner
    Hostname 192.168.102.10
    Port 22
    User apollo
    ProxyJump car18
```

some problems:

- WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!

  参考资料：<http://stackoverflow.com/questions/20840012/ssh-remote-host-identification-has-changed>

  ```shell
  $ ssh-keygen -R <host>
  ```

- 连接不上, 没反应

  可能是 22 端口没打开, 如何打开端口, 这篇文章里有讲到

- connection refused

  probably openssh-server is not installed on remote server, use this command to check(ubuntu):

  ```shell
  dpkg -l | grep openssh-server
  ```

  if not installed, use this command to install:

  ```shell
  sudo apt install openssh-server
  ```

- avoid host authenticity check

  first ssh to remote server, it will ask you to confirm the authenticity of the host, you can use this command to avoid this check:

  ```shell
  ssh -o StrictHostKeyChecking=no
  ```

  or you can add this line to `~/.ssh/config`:

  ```shell
  Host car18
      StrictHostKeyChecking no
      UserKnownHostsFile=/dev/null
      Hostname 103.61.153.140
      Port 6018
      User apollo
  ```

#### 网络 IP 相关命令

参考资料：<http://www.cnblogs.com/kaiye/archive/2013/05/25/3099393.html>

- port occupation progress：

  ```shell
  $ lsof -i:<port>
  ```

  sometimes progress is root, it will not show, so we need sudo to run this command.

- 查看 localhost ip：

  ```shell
  $ hostname -I
  ```

#### SCP 文件传输

安装(CentOS)：

```shell
$ yum -y install openssh-clients
```

需要相互通信的服务器都要安装

#### 开通端口

Ubuntu

```shell
# 查看已经开启的端口
sudo ufw status
# 打开端口
sudo ufw allow <port>
# 开启防火墙
sudo ufw enable
# 重启防火墙
sudo ufw reload
# 再次查看端口是否已开启
sudo ufw status
```

#### 下载文件

```shell
# 下载到当前路径
wget http://www.domain.com/filename-4.0.1.zip
# 指定路径和文件名
wget -O filename.zip http://www.domain.com/filename-4.0.1.zip
```

#### curl 请求

curl post 请求

```bash
curl -X POST -H "Content-Type: application/json" -d '{"date": "2022-08-03", "car_id_list": ["white-rhino-013"]}' http://192.168.199.102:8802/api/case/
```

#### net status

nethogs command is useful:

```shell
sudo apt install nethogs
sudo nethogs -s
```

---

### about file

#### mv file

```shell
mv file1 file2
```

move and overwrite

```shell
mv -f file1 file2
```

#### 查找文件

- which 查找可执行文件，根据可执行文件的文件名。例如：

  ```shell
  $ which mysqld
  ```

- 查找路径下包含某内容的文件

  ```shell
  # 在当前路径下查找包含content的文件
  $ grep -r "content" .
  ```

- 在当前路径下根据文件名查找文件
  ```bash
  find . -name app.bundle.js
  ```

#### file display

- list file with date sort

  ```shell
  ll -t .
  ```

- 查看文件的全部内容

  ```shell
  $ cat app.py
  ```

- 如果你只想看文件的前 5 行，可以使用 head 命令，如：

  ```shell
  $ head -5 app.py
  ```

- 如果你想查看文件的后 10 行，可以使用 tail 命令，如：

  ```shell
  $ tail -20 /etc/passwd
  ```

- 参数-f 使 tail 不停地去读最新的内容，这样有实时监视的效果

  ```shell
  $ tail -f /var/log/messages
  ```

- 查看某文件是否包含特定字符串

  ```shell
  $ grep "string" /path/to/file
  $ echo $? # 0表示包含，1表示不包含
  ```

#### archive & unarchive

- tar

  [Tar Command Examples in Linux](https://www.tecmint.com/18-tar-command-examples-in-linux/)

  > The Linux “**tar**” stands for tape archive, which is used by large number of **Linux/Unix** system administrators to deal with tape drives backup. The tar command used to rip a collection of files and directories into highly compressed archive file commonly called **tarball** or **tar**, **gzip** and **bzip** in **Linux**. The tar is most widely used command to create compressed archive files and that can be moved easily from one disk to another disk or machine to machine.

  - args

    **x** – extract 释放

    **v** – Verbosely show the .tar file progress 显示解压过程

    **f** – File name type of the archive file 使用档案文件或设备，这个选项通常是必选的

    **C** – specified directory 指定路径

    **z** – if archive file is compressed with gzip, then use this argument

  - unzip

    ```shell
    # unzip to current path
    $ tar -xvf public_html-14-09-12.tar
    # unzip to specified path
    $ tar -xvf public_html-14-09-12.tar -C /home/public_html/videos/
    ```

    args:  
    `--strip-components 2` 去掉前两层路径. 例如有的压缩结果有多层文件夹, 前两层文件夹可能是无用的.

  - zip

    ```shell
    # zip file
    $ tar -zcvf public_html-14-09-12.tar.gz public_html
    ```

#### 路径

- mkdir

  ```shell
  # 创建多层级路径
  $ mkdir -p /home/work/bin/ksxing-web
  ```

- 查看路径下的全部内容，并 exclude 某路径

  ```shell
  # 查看当前路径下的所有文件，并不查看venv这个路径
  $ find . -path ./venv -prune -o -print
  ```

#### 磁盘

- 查看路径挂载在哪个磁盘下
  ```shell
  # df -h再加上路径
  $ df -h /tmp
    Filesystem      Size  Used Avail Use% Mounted on
    /dev/sde2       439G   21G  395G   6% /
  ```

#### 创建随机临时文件

```bash
# 创建临时文件
$ mktemp
/tmp/tmp.aJuVf0ftIo
# 创建临时文件夹
$ mktemp -d
/tmp/tmp.3iwExbjajN
```

#### 获取当前路径下某文件的完整路径

```bash
readlink -e <filename>
```

#### 根据文件路径获取文件名

```bash
basename <path>
```

#### preview image

feh <https://feh.finalrewind.org/>

#### check two file is same

```bash
md5sum file1.txt
md5sum file2.txt
```

---

### 进程

#### 查看网络状态

```bash
$ netstat -pln
$ netstat -pln|grep python
```

#### 重新读取配置文件并重启

一个进程, 我们修改了配置文件, 但是不想关闭它然后再启动, 想无缝重启, 那么可以用:

```bash
kill -HUP <pid>
```

pid 怎么获取呢? 可以用`ps aux | grep <name>`, 也可以去读取其 pid 文件, 例如 supervisord 的 pid 文件一般是在`/tmp`下, 那么可以:

```bash
kill -HUP `cat /tmp/supervisord.pid`
```

---

### 权限

#### 无法 cd 到某些路径，Permission Denied

[http://unix.stackexchange.com/questions/320011/permission-denied-cd-into-directory](http://unix.stackexchange.com/questions/320011/permission-denied-cd-into-directory)

```shell
$ chmod go+rx /dir
```

#### 更改文件的用户

`ll`可以看到文件的用户和组信息, 如果是 root 用户, 权限较高, 可能某些场景下会有问题.  
我们可以修改成当前用户:

```shell
sudo chown -R max:max /data/product
```

#### 文件权限

用`ll`查看文件详细信息

```shell
$ ll
-rwxrwxr-x  1 yangle yangle 5.9M 8月   7 16:51 access*
drwxr-xr-x 15 yangle yangle 4.0K 7月  21 13:52 apollo/
...
```

第一列就是文件的类型和权限信息, 第一个字符`-`代表文件, `d`代表文件夹. 后面还有 3\*3 = 9 个字符, 第一组 3 个字符是 owner 的权限, 第二组 3 个字符是 group 的权限, 第三组 3 个字符是 other 的权限. `r`代表读, `w`代表写, `x`代表执行.  
如果我们需要增加一个文件(例如上面的 access 文件)的执行权限, 可以用`chmod`命令, 如:

```shell
chmod +x access*
```

another example:

```shell
sudo chmod 600 ××× （只有所有者有读和写的权限）
sudo chmod 644 ××× （所有者有读和写的权限，组用户只有读的权限）
sudo chmod 700 ××× （只有所有者有读和写以及执行的权限）
sudo chmod 666 ××× （每个人都有读和写的权限）
sudo chmod 777 ××× （每个人都有读和写以及执行的权限）
```

### 进程

#### screen

screen 和 tmux 类似, 可以脱离 shell 运行程序, 不受 shell 退出的影响

```shell
# dmS后台运行并指定一个名字, 后面再加上命令
$ screen -dmS myscreen python -m SimpleHTTPServer 8080
```

回到这个进程可以用

```shell
$ screen -xS myscreen
```

### 日期

#### 时间戳转换为日期

```shell
$ date -d @123456789
Wed Dec 31 19:00:00 1969
```

### bash

`bash -x [command]`可以打印出命令执行的详细信息

`ldd [command]`可以查看命令依赖的库

### grammar

- `&&` and `||` and `;`

  ```bash
  $ false || echo "Oops, fail"
  Oops, fail

  $ true || echo "Will not be printed"
  $

  $ true && echo "Things went well"
  Things went well

  $ false && echo "Will not be printed"
  $

  $ false ; echo "This will always run"
  This will always run
  ```
