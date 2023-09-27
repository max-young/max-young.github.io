---
layout:     post
title:      "baidu apollo"
date:       2023-09-27
categories: autonomous driving
tags:  
  -  apollo
---

### installation

[安装说明](https://apollo.baidu.com/community/Apollo-Homepage-Document/Apollo_Doc_CN_8_0?doc=%2F%25E5%25AE%2589%25E8%25A3%2585%25E8%25AF%25B4%25E6%2598%258E%2F%25E8%25BD%25AF%25E4%25BB%25B6%25E5%258C%2585%25E5%25AE%2589%25E8%25A3%2585%2F%25E8%25BD%25AF%25E4%25BB%25B6%25E5%258C%2585%25E5%25AE%2589%25E8%25A3%2585%2F)

you may account for some problems when installing apollo, such as:

- `Failed to pull docker image : registry.baidubce.com/apollo/apollo-env-gpu:latest` when you execute `aem start`

	it's related to your docker permission, execute this:
	```shell
	sudo chmod 777 /var/run/docker.sock
	```