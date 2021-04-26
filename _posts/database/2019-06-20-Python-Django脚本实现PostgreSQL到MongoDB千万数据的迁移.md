---
layout:     post
title:      "Python-Django脚本实现PostgreSQL到MongoDB千万数据的迁移"
subtitle:   ""
date:       2019-06-19
categories: Backend
tags:
    - Python
    - Database
---

Python-Django脚本实现PostgreSQL到MongoDB千万数据的迁移

- [需求](#需求)
- [实现](#实现)
- [总结](#总结)

### 需求

从PostgreSQL的一张表OrderRaw(电商订单的原始数据)查询出所有数据, 组织成财务需要的格式存入MongoDB, 这张表有四千万多万条数据

### 实现

需求很简单哈, 查出来所有的数据, for循环, 一条条处理, 然后存入MongoDB即可, 如下所示:

```python
# MongoDBClient
mdb = MongoService.get_client()
# 获取所有OrderRaw的数据
order_raws = OrderRaw.objects.values('id', 'ptype', 'raw').all()
for order_raw in order_raws:
    # 转换成财务数据
    finance_data = finance_data(order_raw)
    # 存入MongoDB
    client.hermes.order_raw.insert(insert_data)
```

可能不用运行都会发现问题, 我们把问题列出来, 然后挨个去解决

- 取出所有数据会不会内存不够用?

  答案是会, 参照这篇文章: [Using Django querysets effectively](https://blog.etianen.com/blog/2013/06/08/django-querysets/), 而且有可能导致运行的程序宕掉

  怎么办? Django queryset有[iterator](https://docs.djangoproject.com/en/2.1/ref/models/querysets/#iterator)的功能, 迭代器, 分片去取, 而不是一次全部取出来

  > queryset有很多"学问", 参照这篇文章可以学到很多

  那么代码变成这样:

  ```python
  # MongoDBClient
  mdb = MongoService.get_client()
  # 获取所有OrderRaw的数据
  order_raws = OrderRaw.objects.values('id', 'ptype', 'raw')
  for order_raw in order_raws.iterator():
      # 转换成财务数据
      finance_data = finance_data(order_raw)
      # 存入MongoDB
      client.hermes.order_raw.insert(insert_data)
  ```

  这样我们运行看看, 我们会发现执行后"没有反应", 大概能够猜到数据量太大, 可能会运行很长时间, 到底需要运行多长时间呢? 我们不知道

- 运行时间未知, 没有任何输出

  我们可以采用进度条第三方包[progressbar](https://progressbar-2.readthedocs.io/en/latest/), 来输出时间和进度, 代码变成:

  ```python
  import progressbar
  
  # MongoDBClient
  mdb = MongoService.get_client()
  # 获取所有OrderRaw的数据
  order_raws = OrderRaw.objects.values('id', 'ptype', 'raw')
  with progressbar.ProgressBar(max_value=order_raws.count()) as bar:
      count = 0
      for order_raw in order_raws.iterator():
          count += 1
          # 转换成财务数据
          finance_data = finance_data(order_raw)
          # 存入MongoDB
          client.hermes.order_raw.insert(insert_data)
          bar.update(count)
  ```

  这样运行之后, 我们就能看到运行的进度和大概的时间了, 但是我们会发现大概会运行好几十个小时才能完成.

  我们怎样优化呢? 

- 运行时间太长, 如何优化

  优化首先要做的是定位性能问题在哪里, Python有自己的性能分析工具[cProfile](#https://docs.python.org/3.7/library/profile.html), 我们可以查询出一定数量的数据来进行测试, 代码变成这样:

  ```python
  import cProfile
  import progressbar
  
  pr = cProfile.Profile()
  pr.enable()
  
  # MongoDBClient
  mdb = MongoService.get_client()
  # 获取所有OrderRaw的数据
  order_raws = OrderRaw.objects.filter(id__gte=80000, id__lte=90000).values('id', 'ptype', 'raw')
  with progressbar.ProgressBar(max_value=order_raws.count()) as bar:
      count = 0
      for order_raw in order_raws.iterator():
          count += 1
          # 转换成财务数据
          finance_data = finance_data(order_raw)
          # 存入MongoDB
          client.hermes.order_raw.insert(insert_data)
          bar.update(count)
  
  pr.disable()
  # python3.6不兼容
  #  sortby = SortKey.TIME
  #  ps = pstats.Stats(pr).sort_stats(sortby)
  ps = pstats.Stats(pr).sort_stats('time')
  ps.print_stats(10)
  ```

  运行之后我们能看到输出, 显示往MongoDB插入数据的时间最久, 如何解决这个问题?

- 往MongoDB写入数据的时间太久

  现在是一条一条数据插入, 我们能批量插入吗? 我们一千条存入一次试试:

  ```python
  import cProfile
  import progressbar
  
  pr = cProfile.Profile()
  pr.enable()
  
  # MongoDBClient
  mdb = MongoService.get_client()
  # 获取所有OrderRaw的数据
  order_raws = OrderRaw.objects.filter(id__gte=80000, id__lte=90000).values('id', 'ptype', 'raw')
  with progressbar.ProgressBar(max_value=order_raws.count()) as bar:
      count = 0
      insert_data = []
      for order_raw in order_raws.iterator():
          count += 1
          # 转换成财务数据
          finance_data = finance_data(order_raw)
          insert_data.append(finance_data)
          if count % 1000 == 0:
              # 存入MongoDB
              client.hermes.order_raw.insert_many(insert_data)
              insert_data.clear()
          bar.update(count)
  
  pr.disable()
  # python3.6不兼容
  #  sortby = SortKey.TIME
  #  ps = pstats.Stats(pr).sort_stats(sortby)
  ps = pstats.Stats(pr).sort_stats('time')
  ps.print_stats(10)
  ```

  我们还可以调试一次存入的数量, 最后发现2000条是正合适的.

  最后我记得一个多小时执行完毕.

### 总结

细小的工作也有很多隐藏的知识, 上面知识列举了主要的东西, 其中还有很多细节, 我还有用多线程去做, 实现起来有一些复杂, 且销量也没有很大提升, 所以作罢

总结还是: 细节! 深入!
