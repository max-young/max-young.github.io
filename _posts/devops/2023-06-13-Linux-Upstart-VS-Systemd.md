---
layout: post
title: "Linux Upstart VS Systemd"
subtitle: ""
date: 2023-06-13
categories: Linux
tags:
  - Linux
---

- [文件地址和格式](#文件地址和格式)
- [文件内容](#文件内容)
- [运行命令](#运行命令)
- [log](#log)

Linux 启动时会执行进程, 我们可以自定义.

Ubuntu15.04 之前用的是 Upstart, 之后用 Systemd

他们之间的差别参照这里: <https://wiki.ubuntu.com/SystemdForUpstartUsers>

我们以开机启动 Gunicorn 为例来说明

#### 文件地址和格式

Upstart 是创建`/etc/init/$job.conf`文件, 后缀为`.conf`

Systemd 是创建`/lib/systemd/system/$job.service`文件, 后缀为`.service`  
系统范围的服务单元文件：/lib/systemd/system/  
用户范围的服务单元文件：/etc/systemd/system/

#### 文件内容

文件内容格式参见上面提到的文档, 举个例子, Upstart 的 conf 文件是这样的:

```text
description "Gunicorn server for mm.mmflow.online"

start on net-device-up
stop on shutdown

respawn

setuid max
chdir /home/max/sites/mm.mmflow.online/source

exec ../virtualenv/bin/gunicorn --bind unix:/tmp/mm.mmflow.online.socket superlists.wsgi:application
```

Systemd 的 service 文件应该这么写:

```text
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

Upstart 的命令是:

```shell
sudo start $job
```

Systemd 的命令是:

```shell
systemctl start $job
```

#### log

```shell
journalctl -u $job
```
