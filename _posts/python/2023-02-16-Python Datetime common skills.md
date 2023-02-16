---
layout: post
title: "Python Datetime common skills"
subtitle: ""
date: 2023-02-16
categories: Python
tags:
  - Python
---

- [date 转换为 datetime](#date-转换为-datetime)
- [计算昨天日期](#计算昨天日期)
- [local datetime string to utc string](#local-datetime-string-to-utc-string)

#### date 转换为 datetime

```python
from datetime import date
from datetime import datetime

dt = datetime.combine(date.today(), datetime.min.time())
```

#### 计算昨天日期

```python
from datetime import date, timedelta
(date.today - timedelta(days=1)).strftime("%Y-%m-%d")
```

#### local datetime string to utc string

for example, convert beijing time "2023-02-16 10:00:00" to utc time "2023-02-16T02:00:00Z"

```python
from datetime import datetime, timezone
end_time_utc = datetime.strptime(
    self.end_time + " +0800", "%Y-%m-%d %H:%M:%S %z").astimezone(
        timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
```
