---
layout:     post
title:      "Python logging自定义handler存储数据库"
subtitle:   ""
date:       2019-11-14
categories: Python
tags:
    - Python
    - Django
---

### 需求

web微服务项目中需要将用户操作记录存储到数据库里

### 方案

最初的方案是在其中一个微服务中提供一个公共的API接口, 其它服务在需要记录用户操作记录的地方, 比如某一个view里面, 将用户操作记录POST请求公共接口, 公共接口处理数据存储到数据库.

这样做的弊端是:

1. 接口可能不稳定, 也可能会影响到正常的业务, 比如接口报错, 接口请求延迟, 虽然可以做相应的处理, 但是这样就复杂了
2. 代码比较复杂, 其他服务需要额外增加的代码比较多, 手写request代码, 或者用公共的装饰器, 都比较复杂

细想一下, 这个需求跟日志很像, 只是日志一般是打印到终端, 或者是存储到日志文件里, 这个需求是存储到数据库.

我看了一下Python logging的文档, 日志如何处理是由handler来控制的, logging自带的handler有fileHandler, streamHandler等, 那么我们可不可以自定义一个handler, 来把日志存储到数据库呢?

这样的话, 在需要记录用户操作记录的地方, 只需按照logging的方式, 一行代码就可以了:`logging.info('xxxxxxxxxx')`

### 实现

我是在Django里面来实现的

1. 用户操作记录数据表模型

   ```python
   from django.db import models


   class AuditLog(models.Model):
       ACTION_CHOICES = (
           ('INSERT', '添加'),
           ('UPDATE', '更新'),
           ('DELETE', '删除'),
           ('SEARCH', '搜索'),
           ('EXPORT', '导出')
       )
       system = models.CharField("服务名称", max_length=20, default='')
       user_id = models.IntegerField("操作人用户ID", default=0)
       action = models.CharField("操作动作", max_length=10, choices=ACTION_CHOICES, default='')
       keyword = models.CharField("业务关键词", max_length=20, default='')
       key = models.IntegerField("操作对象ID", null=True, blank=True)
       extra = models.CharField("额外信息", max_length=100, default='')
       time = models.DateTimeField(auto_now_add=True)

       class Meta:
           indexes = [
               models.Index(fields=['system'], name='system_idx'),
               models.Index(fields=['user_id'], name='user_id_idx'),
               models.Index(fields=['time'], name='time_idx'),
           ]
   ```

2. 自定义Handler和公共logger实例

   ```python
   import logging

   from .models import AuditLog


   class AuditLoggingHandler(logging.Handler):
       """自定义handler

       将日志存入数据库
       """

       def __init__(self):
           # 设置hander的level, 只有level高于INFO的log才能处理
           super().__init__(level=logging.INFO)

       def emit(self, record):
           # 处理日志, emit函数是handler的默认处理日志的函数
           try:
               # 这里需要用到record.args和record.msg, 在下面使用方法里就能看到这两个属性是什么意思了
               args = record.args
               action = args.get('action')
               key = args.get('key')
               log = AuditLog(
                   system=args.get('system'),
                   user_id=args.get('user_id'),
                   action=args.get('action'),
                   keyword=args.get('keyword'),
                   key=args.get('key'),
                   extra=record.msg)
               log.full_clean()
               log.save()
           except Exception:
               # 处理错误, 为了不影响正常业务
               self.handleError(record)

   def audit_logger():
	   # 实例化logger, 其他服务引入此logger来记录
	   logger = logging.getLogger('audit')
	   # 设置handler
	   logger.addHandler(AuditLoggingHandler())
	   # 设置level
	   logger.setLevel(logging.INFO)
   ```

3. 使用

   上面的代码放在一个公共的包si里面, 在其他微服务里就可以直接来使用了

   ```python
   from si.audit import audit_logger

   # 第一个参数'导出报表'就是record.msg, 第二个字典参数就是record.args
   ...
   audit_logger().info('导出报表', {'system': 'fsp', 'user_id': request.user.id, 'action': 'EXPORT', 'keyword': '报表'})
   ...
   ```
