---
layout: post
title: "Python Datetime常用技巧"
subtitle: ""
date: 2022-11-24
categories: Python
tags:
  - Python
---

##### date 转换为 datetime

```python
from datetime import date
from datetime import datetime

dt = datetime.combine(date.today(), datetime.min.time())
```

##### 计算昨天日期

```python
from datetime import date, timedelta
(date.today - timedelta(days=1)).strftime("%Y-%m-%d")
```
