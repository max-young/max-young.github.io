---
layout:     post
title:      "Django测试Celery"
subtitle:   ""
date:       2019-10-21
categories: Python
tags:
    - Python
    - Django
    - Celery
    - 测试
---

如果我们想测试celery任务是否执行正确, 我们可以把任务函数当作普通函数来测试, 但是还有一种情况是测试接口, 接口调用celery任务, 这样应该怎么测试呢?

如果我们启动临时的broker和worker, 天啦, 这样太麻烦了, 怎么可以不启动服务, 还能测试celery任务是否正确呢?

在Django里可以这样做:
在测试函数里加上装饰器`@override_settings(task_always_eager=True)`
这样运行测试的时候就会直接执行任务, 而不需要启动celery服务

```python
from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from rest_framework.test import APIClient


class ReportTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        user = User.objects.first()
        self.client.force_authenticate(user=user)

    @override_settings(task_always_eager=True)
    def test_stock_daily_summary_report(self):
        post_data = {
            "company_id": 5,
            "report_name": "stock_daily_summary_detail",
            "query_params": {"date_from": "2019-08-27", "date_to": "2019-08-27"}
        }
        response = self.client.post('/api/report/tasks/', post_data, format='json')
        self.assertContains(response, '备注')
```
