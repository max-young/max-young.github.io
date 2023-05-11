---
layout: post
title: "uptime kuma"
date: 2023-05-11
categories: Linux
tags:
  - devops
---

uptime kuma is a fancy self-hosted monitoring tool. It can monitor services and websites, and send you notifications via Telegram, Discord, Slack, Email and more.

<https://github.com/louislam/uptime-kuma>

we usually deploy it with docker

here is the docker-compose.yml

```yaml
version: "1.0"

services:
  uptime-kuma:
    image: louislam/uptime-kuma:latest
    container_name: uptime-kuma
    restart: unless-stopped
    ports:
      - 3001:3001
    volumes:
      - /home/apollo/rhino-monitor/uptime-kuma/_data:/app/data
```

please note volumes config, it can prvent data loss in case of remove container.

#### how to update

<https://github.com/louislam/uptime-kuma/wiki/%F0%9F%86%99-How-to-Update>
