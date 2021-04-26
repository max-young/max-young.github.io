---
layout:     post
title:      "Docker创建MongoDB replicaset实例"
subtitle:   ""
date:       2019-06-24
categories: Database
tags:
    - Docker
    - MongoDB
---

在本地开发做测试时, 有时候需要MongoDB replicaset, 但是安装MongoDB再启动应用在配置很繁琐
用Docker就可以很方便的实现, 如下所示:

1. 启动MongoDB实例

    ```shell
    # pull the official mongo docker container
    $ docker pull mongo

    # create network
    $ docker network create my-mongo-cluster

    # create mongos
    $ docker run -d --rm --net my-mongo-cluster -p 27017:27017 --name mongo1 mongo mongod --replSet my-mongo-set --port 27017
    $ docker run -d --rm --net my-mongo-cluster -p 27018:27018 --name mongo2 mongo mongod --replSet my-mongo-set --port 27018
    $ docker run -d --rm --net my-mongo-cluster -p 27019:27019 --name mongo3 mongo mongod --replSet my-mongo-set --port 27019
    ```

2. 修改host

    在`/etc/hosts`里添加如下内容:
    ```
    127.0.0.1       mongo1 mongo2 mongo3
    ```

3. 配置replicaset

    - 进入mongo shell
    ```shell
    # setup replica set
    $ docker exec -it mongo1 mongo
    ```
    - 在mongo shell里执行
    ```mongodb
    >> db = (new Mongo('localhost:27017')).getDB('test')
    >> config={"_id":"my-mongo-set","members":[{"_id":0,"host":"mongo1:27017"},{"_id":1,"host":"mongo2:27018"},{"_id":2,"host":"mongo3:27019"}]}
    rs.initiate(config)
    ```

4. 连接mongo服务

    经过上面的操作replicaset就配置好了, 就可以通过下面的命令连接mongo服务了
    ```shell
    # connection URI
    $ mongo "mongodb://localhost:27017,localhost:27018,localhost:27019/{db}?replicaSet=my-mongo-set"
    ```
    在应用程序里就可以按照对应的配置来进行测试了
