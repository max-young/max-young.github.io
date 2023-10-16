---
layout:     post
title:      "baidu apollo"
date:       2023-09-27
categories: autonomous driving
tags:  
  -  apollo
---

- [installation](#installation)
- [glossary](#glossary)


### installation

[安装说明](https://apollo.baidu.com/community/Apollo-Homepage-Document/Apollo_Doc_CN_8_0?doc=%2F%25E5%25AE%2589%25E8%25A3%2585%25E8%25AF%25B4%25E6%2598%258E%2F%25E8%25BD%25AF%25E4%25BB%25B6%25E5%258C%2585%25E5%25AE%2589%25E8%25A3%2585%2F%25E8%25BD%25AF%25E4%25BB%25B6%25E5%258C%2585%25E5%25AE%2589%25E8%25A3%2585%2F)

you may account for some problems when installing apollo, such as:

- `Failed to pull docker image : registry.baidubce.com/apollo/apollo-env-gpu:latest` when you execute `aem start`

	it's related to your docker permission, execute this:
	```shell
	sudo chmod 777 /var/run/docker.sock
	```

### glossary

- RTOS
  real time operating system, 实时操作系统
- OTA
  over the air, 无线升级
- v2x
  vehicle to everything, 车联网
- cyber RT
  cyber real time, 实时通信框架
- canbus
	controller area network bus, 控制器局域网总线
	用于和车辆的各个部件(电子元器件, 传感器等硬件)进行通信, 实现控制和监控
