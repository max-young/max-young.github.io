---
layout: post
title: "run Python script in background"
date: 2023-06-06
categories: Linux
tags:
  - Python
---

- [参考资料：](#参考资料)
- [背景](#背景)
- [解决办法](#解决办法)

##### 参考资料：

<https://www.ibm.com/developerworks/cn/linux/l-cn-nohup/>

##### 背景

我需要启动一个消息队列的消费脚本，需要一直运行，脚本 HttpConsumer.py 示例如下：

```python
# encoding:utf-8
class HttpConsumer(object):
    def __init__(self):
        pass
    def process(self):
        pass
if __name__ == '__main__':
    """构造消息订阅者"""
    consumer = HttpConsumer()
    """开始启动消息订阅者"""
    consumer.process()
```

问题是：直接运行`python HttpConsumer.py`如果退出终端，python 进程也会中断，所以我们需要后台运行。

##### 解决办法

- nohup

  ```shell
  $ nohup python HttpConsumer.py > 111.txt &
  [1] 13531
  $ nohup: ignoring input and redirecting stderr to stdout
  ^C
  $ ps aux|grep HttpConsumer
  root     13531  4.6  0.3 638552 30788 pts/5    Sl   10:17   0:00 python HttpConsumer.py
  root     13585  0.0  0.0 112648   972 pts/5    S+   10:17   0:00 grep --color=auto HttpConsumer
  ```

  我们可以把 python 的日志（包括里面的 print 信息）输出到指定文件，实验成功

  `&` can be used to run any command as a background process, if you want to run a command in the background without any output to the screen you can use the following command:

  ```shell
  $ nohup python HttpConsumer.py > /dev/null 2>&1 &
  ```

- setsid

  ```shell
  $ setsid python HttpConsumer.py > log.txt &
  $ ps aux|grep HttpCon
  root     12517  1.8  0.4 638556 32832 ?        Ssl  10:01   0:00 python HttpConsumer.py
  root     12552  0.0  0.0 112648   972 pts/5    S+   10:01   0:00 grep --color=auto HttpCon
  ```

  后台运行成功，但是 log.txt 里没有内容，这里应该是把 stdout 输出到 log.txt，而不是日志，所以是空的。

比较一下，我们用 nohup 来启动更合适
