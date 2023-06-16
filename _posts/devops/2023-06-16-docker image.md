---
layout: post
title: "docker image"
date: 2023-06-16
categories: Devops
tags:
  - docker
---

### how to install docker in dockerfile

```dockerfile
FROM ubuntu:20.04
USER root
RUN apt update
RUN apt install docker.io -y
```
