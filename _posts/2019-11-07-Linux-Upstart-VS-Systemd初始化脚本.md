---
layout:     post
title:      "Linux Upstart VS Systemd初始化脚本"
subtitle:   ""
date:       2019-11-07
categories: Linux
tags:
    - Linux
---

Linux启动时会执行进程, 我们可以自定义.

Ubuntu15.04之前用的是Upstart, 之后用Systemd

他们之间的差别参照这里: <https://wiki.ubuntu.com/SystemdForUpstartUsers>

我们以开机启动Gunicorn为例来说明

#### 文件地址和格式

Upstart是创建`/etc/init/$job.conf`文件, 后缀为`.conf`
Systemd是创建`/lib/systemd/system/$job.service`文件, 后缀为`.service`

#### 文件内容

文件内容格式参见上面提到的文档, 举个例子, Upstart的conf文件是这样的:
```
description "Gunicorn server for mm.mmflow.online"

start on net-device-up
stop on shutdown

respawn

setuid max
chdir /home/max/sites/mm.mmflow.online/source

exec ../virtualenv/bin/gunicorn --bind unix:/tmp/mm.mmflow.online.socket superlists.wsgi:application
```
Systemd的service文件应该这么写:
```service
[Unit]
Description=Gunicorn server for mm.mmflow.online
Wants=net-device-up
Conflicts=shutdown

[Service]
Restart=on-failure
User=max
WorkingDirectory=/home/max/sites/mm.mmflow.online/source
ExecStart=/home/max/sites/mm.mmflow.online/virtualenv/bin/gunicorn --bind unix:/tmp/mm.mmflow.online.socket superlists.wsgi:application
```
#### 运行命令
Upstart的命令是:
```shell
sudo start $job
```
Systemd的命令是:
```shell
systemctl start $job
```
