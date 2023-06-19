---
layout: post
title: "docker in docker"
date: 2023-06-19
categories: Devops
tags:
  - docker
---

- [how to run docker in docker container?](#how-to-run-docker-in-docker-container)

### how to run docker in docker container?

- Dockerfile

  ```dockerfile
  FROM ubuntu:20.04
  USER root
  RUN apt update
  RUN apt install docker.io -y
  ```

- build and run

  ```shell
  docker build -t docker-in-docker .
  docker run -it --rm docker-in-docker bash
  ```

- call docker in container

  ```shell
  root@6d0d4893b1ab:/# docker run hello-world
  docker: Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?.
  See 'docker run --help'.
  ```

how to fix it?

1. run dockerd in contaier  
   but I failed, I don't know why
2. mount docker.sock in container

   ```shell
   docker run -it --rm -v /var/run/docker.sock:/var/run/docker.sock docker-in-docker bash
   ```

   this solution is work.
