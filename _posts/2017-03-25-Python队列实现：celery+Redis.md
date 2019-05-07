---
layout:     post
title:      "Python队列实现：celery+Redis"
subtitle:   ""
date:       2017-03-25 11:22:00
author:     "alvy"
header-img: "img/post-bg-nextgen-web-pwa.jpg"
header-mask: 0.3
catalog:    true
tags:
    - Python
    - cache
    - Redis
---

##### redis

1. redis服务安装

   [http://redis.io/download](http://redis.io/download)

   一般安装路径放在`/usr/local/`下

   启动服务之后，进入客户端，发现没有反应，那么请参照这里

   [http://unix.stackexchange.com/questions/103731/run-a-command-without-making-me-wait](http://unix.stackexchange.com/questions/103731/run-a-command-without-making-me-wait)

   启动服务的命令是    
   `/usr/local/redis/src/redis-server`

   CTRL+Z之后输入bg，让服务在后台运行

   然后就可以进去客户端了,命令是    
   `/usr/local/redis/src/redis-cli`    
   可以加上`-h <i> -p <port>`

2. Redis配置

   上面的服务启动命令是以默认的配置启动，我们也可以以自己的配置来启动，配置设置的含义可以参照这里

   [http://www.runoob.com/redis/redis-conf.html](http://www.runoob.com/redis/redis-conf.html)

   官网也有配置示例，可在`/etc/`下创建redis.conf文件，然后将示例粘贴进去，在此基础上修改

   我将守护进程开启，并绑定本机的内网地址  

3. 在Flask应用里配置Redis

   我们采用python的redis包，参照[https://pypi.python.org/pypi/redis](https://pypi.python.org/pypi/redis)

   配置文件：

   ```python
   REDIS_HOST = "10.174.93.111"
   REDIS_PORT = 6379
   REDIS_DATABASE = 0
   ```
   创建redis实例

   ```python
   redis_celery_conn = redis.StrictRedis(host=config.REDIS_HOST,port=config.REDIS_PORT,db=config.REDIS_DATABASE)
   ```
   运行测试：
   ```shell
   >>> from ksxing.store import redis_celery_conn as redis_clr
   >>> redis_clr.set('foo','bar')
   True
   >>> redis_clr.get('foo')
   'bar'
   ```
    import redis实例时可能会出现错误

   `redis.exceptions.ResponseError: DENIED Redis is running in protected mode because protected mode is enabled`

   原因参照这里：[http://www.cnblogs.com/leolztang/p/5542747.html](http://www.cnblogs.com/leolztang/p/5542747.html)

   简单的说有两个原因：1. 没有设置密码；2. 没有绑定ip

   只需改动其一重新运行redis服务即可

   我们在配置文件里配置bind ip

   然后先关闭redis服务

   进入客户端`/usr/local/redis/src/redis-cli`

   输入`shutdown`

   退出客户端，输入`ps aux|grep redis`，发现服务已关闭

   然后重新用配置文件启动redis

   `/usr/local/redis-3.2.3/src/redis-server /etc/redis.conf`

   重新测试，发现没有问题
   进入客户端需要加上ip    
   `/usr/local/redis-3.2.3/src/redis-cli -h 10.174.93.111`

   备注：redis服务重启可参照    
   [http://stackoverflow.com/questions/6910378/how-can-i-stop-redis-server](http://stackoverflow.com/questions/6910378/how-can-i-stop-redis-server)

***

##### celery

1. 安装

    因为我们采用redis，安装参照
    [http://docs.jinkan.org/docs/celery/getting-started/brokers/redis.html#broker-redis](http://docs.jinkan.org/docs/celery/getting-started/brokers/redis.html#broker-redis)

2. 创建celery实例，我们创建一个celery_app.py文件，内容如下：

   ```python
   from celery import Celery
   from config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND
   celery = Celery("ksxing", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

   @celery.task
   def export_all_results(exam_info_id, all_users=0):
       pass
   ```

3. 运行worker

   根据官方文档    
   [http://docs.celeryproject.org/en/latest/userguide/workers.html](http://docs.celeryproject.org/en/latest/userguide/workers.html)

   运行的命令是`$ celery -A proj worker -l info`

   celery_app.py的路径是`/home/work/ksxing/ksxing/`

   我们当前的路径是`/home/work/ksxing`    

   所以我们运行的命令是`$ celery -A ksxing.celery_app worker -l info`    

   测试导出成绩成功，但是官方worker的启动不支持守护进程启动，也就是说运行上面的命令之后，我们关掉终端，worker就停止了。

4. 守护进程启动celery worker    
    官方文档在此：    
    [Running the worker as a daemon](http://docs.celeryproject.org/en/latest/tutorials/daemonizing.html)    
    我们参照第一种推荐方法
    - 创建celeryd脚本    
      路径：/etc/init.d/celeryd    
      内容从官方文档里面复制
      运行的命令是：    
      `/etc/init.d/celeryd {start|stop|restart|status}`
        > 运行此命令时可能会出现command not found或者permission denied的错误，我们需要下面的命令，来改变此脚本的权限和用户组，因为根据官方文档的说法，此脚本只能是root下运行，命令如下：    
        > ```
        > sudo chmod 755 /etc/init.d/celeryd
        > sudo chown root:root /etc/init.d/celeryd
        > ```
        > 解释如下：The first line changes the permissions to -rwxr-xr-x, and the second line ensures that the owner and group owner of the file is root.    

    - 配置文件    
      路径： /etc/default/celeryd
      创建之后，从官方文档里粘贴配置示例进行修改    
        ```
        # Names of nodes to start
        #   most people will only start one node:
        CELERYD_NODES="worker1"
        #   but you can also start multiple and configure settings
        #   for each in CELERYD_OPTS (see `celery multi --help` for examples):
        #CELERYD_NODES="worker1 worker2 worker3"
        #   alternatively, you can specify the number of nodes to start:
        # 可采取这种方式，只有一个worker可能会引起阻塞，任务不执行，血泪教训
        #CELERYD_NODES=10
        
        # Absolute or relative path to the 'celery' command:
        CELERY_BIN="/usr/bin/celery"
        #CELERY_BIN="/virtualenvs/def/bin/celery"
        # App instance to use
        # comment out this line if you don't use an app
        CELERY_APP="ksxing.celery_app"
        # or fully qualified:
        #CELERY_APP="proj.tasks:app"
        
        # Where to chdir at start.
        CELERYD_CHDIR="/home/yangle/ksxing/"
        
        # Extra command-line arguments to the worker
        CELERYD_OPTS="--time-limit=300 --concurrency=8"
        
        # %N will be replaced with the first part of the nodename.
        CELERYD_LOG_FILE="/var/log/celery/%N.log"
        CELERYD_PID_FILE="/var/run/celery/%N.pid"
        
        # Workers should run as an unprivileged user.
        #   You need to create this user manually (or you can choose
        #   a user/group combination that already exists, e.g. nobody).
        CELERYD_USER="yangle"
        CELERYD_GROUP="yangle"
        
        # If enabled pid and log directories will be created if missing,
        # and owned by the userid/group configured.
        CELERY_CREATE_DIRS=1
        ```

        需要注意的有如下几点：    
        > CELERY_BIN="/usr/bin/celery"    
        > celery的安装路径，可用`whereis celery`获取    
        > CELERY_APP="ksxing.celery_app"
        > CELERYD_CHDIR="/home/yangle/ksxing/"    
        > 我的celery实例是写在/home/yangle/ksxing/ksxing/celery_app.py里面，所以这两个配置是这样写，不能把CELERYD_CHDIR写成"/home/yangle/ksxing/ksxing/",CELERY_APP写成"celery_app",因为这样路径环境在`/ksxing/ksxing/`下，celery_app.py文件里面如果要import路径`/home/work/ksxing`下的包，就会出错，task装饰的函数不可避免的要引用ksxing下的各种函数和模型等等。
        > CELERYD_USER="yangle"    
        > CELERYD_GROUP="yangle"    
        > 用户和用户组，我是在yangle用户下测试，所以需要设置成yangle，而且上面的两个配置CELERY_LOG_FILE和CELERY_PID_FILE，首先需要创建路径（里面的log和pid不用创建，是自动生成的），然后需要将用户和用户组修改成yangle，命令是：`chown -R yangle:yangle /var/log/celery/`，如果是正式环境，再修改成正式的work用户组    

    - daemon运行    
      `$ /usr/init.d/celeryd {start|stop|restart|status}`    
      或者    
      `$ service celeryd {start|stop|restart|status}`    
      运行之后我们查看status，正常情况下是：
        ```
        celery init v10.1.
        Using config script: /etc/default/celeryd
        celeryd (node worker1) (pid 13705) is up...
        ```
        如果是`not pidfiles found`，则没有运行成功，检查上面步骤是否有问题    
        运行任务测试