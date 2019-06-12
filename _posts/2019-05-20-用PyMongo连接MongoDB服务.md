---
layout:     post
title:      "用PyMongo连接MongoDB服务"
subtitle:   ""
date:       2019-05-20
categories: database
tags:
    - MongoDB
    - Python
---

- [连接单点服务](#连接单点服务)
- [连接集群replica-set](#连接集群replica-set)

pymongo可以采用URI的方式连接, 也可以采用参数的方式连接, 下面说一下参数连接的配置方法

### 连接单点服务

如下所示:

`authsource`是可选的, 默认admin, 可以特殊指定, 用于认证

```python
import pymongo
client = pymongo.MongoClient(
    host="192.168.0.1",
    port=8001,
    username="user",
    password="password",
    authsource="admin")
mdb = client.get_database("my_database")
```

### 连接集群replica-set

如果是一个集群, 应该怎么连接呢? 例如集群有三个节点, 分布在3台服务器上, 不同的IP, 相同的端口

主节点是192.168.0.1:8001, 两个从节点是192.168.0.2:8001, 192.168.0.3:8001

集群的名称是`foo`, 那么我们增加一个`replicaset`参数即可:

```python
import pymongo
client = pymongo.MongoClient(
    host="192.168.0.1",
    port=8001,
    username="user",
    password="password",
    authsource="admin",
    replicset="foo")
mdb = client.get_database("my_database")
```

我们看一下client的信息:

```python
> client
MongoClient(host=['192.168.0.1:8001'], document_class=dict, tz_aware=False, connect=True, authsource='admin')
> client.nodes
frozenset({('192.168.0.1', 8001), ('192.168.0.2', 8001), ('192.168.0.3', 8001)})
> client.primary
('192.168.0.1', 8001)
> client.secondaries
{('192.168.0.2', 8001), ('192.168.0.3', 8001)}
> client.is_primary
True
```

问题来了, `host`不用指定三个ip地址吗? 我们试试, 用逗号分隔

```python
import pymongo
client = pymongo.MongoClient(
    host="192.168.0.1,192.168.0.2,192.168.0.3",
    port=8001,
    username="user",
    password="password",
    authsource="admin",
    replicset="foo")
mdb = client.get_database("my_database")
```

> 如果三个节点地址不一样, 端口不一样, 可以把端口写到host里面:
> ```python
> import pymongo
> # post还是需要配置的, 不用与三个post对应, 随便配一个参数就好
> client = pymongo.MongoClient(
>     host="192.168.0.1:8001,192.168.0.2:8002,192.168.0.3:8003",
>     port=8001,
>     username="user",
>     password="password",
>     authsource="admin",
>     replicset="foo")
> mdb = client.get_database("my_database")
> ```

再看一下client的信息

```python
> client
MongoClient(host=['192.168.0.1:8001', '192.168.0.2:8001', '192.168.0.3:8001'], document_class=dict, tz_aware=False, connect=True, authsource='admin')
> client.nodes
frozenset({('192.168.0.1', 8001), ('192.168.0.2', 8001), ('192.168.0.3', 8001)})
> client.primary
('192.168.0.1', 8001)
> client.secondaries
{('192.168.0.2', 8001), ('192.168.0.3', 8001)}
> client.is_primary
True
```

除了host不一样, 其他都一样, 可见我们只需设置一个节点的ip即可, 在[官方文档](http://api.mongodb.com/python/current/examples/high_availability.html#initializing-the-set)里面有说明:

> The addresses passed to MongoClient() are called the seeds. As long as at least one of the seeds is online, MongoClient discovers all the members in the replica set, and determines which is the current primary and which are secondaries or arbiters. Each seed must be the address of a single mongod.

寻根究底一下: 那么我们把ip地址设置成其中一个从节点可以吗? 我试了一下, 也是可以的, `client`输出信息是一样的

还有一些额外的参数, 参照这里:

```python
import pymongo
client = pymongo.MongoClient(
    host="192.168.0.1,192.168.0.2,192.168.0.3",
    port=8001,
    username="user",
    password="password",
    authsource="admin",
    replicset="foo",
    readpreference='secondaryPreferred',
    connecttimeoutms=20000,
    maxpoolsize=50)
mdb = client.get_database("my_database")
```

**结论:**

PyMongo连接MongoDB  replicaset时, 配置一个host或者所有host都是可以的, PyMongo会自动发现所有节点.

但是我们注意文档中的一句话, *As long as at least one of the seeds is online*, 如果我们只配置一个host, 但是这个host不可用, 那么连接就会失败, 所以最好是把host都加上

但是, 但是, 一个集群如果primary不可用, 那么从节点也会不可用, 所以配上主节点即可