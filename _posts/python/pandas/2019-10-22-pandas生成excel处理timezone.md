---
layout:     post
title:      "pandas生成excel处理timezone"
subtitle:   ""
date:       2019-10-22
categories: Python
tags:
    - Python
    - Pandas
---

panda生成excel示例如下:
```python
import datetime
import io

import pandas as pd
import pytz

# Create a Pandas dataframe from the data.
df = pd.DataFrame({'date': [datetime.datetime(2011, 8, 15, 8, 15, 12, 0, tzinfo=pytz.timezone('Asia/Shanghai'))]})

output = io.BytesIO()

# Use the BytesIO object as the filehandle.
writer = pd.ExcelWriter(output, engine='xlsxwriter')

# Write the data frame to the BytesIO object.
df.to_excel(writer, sheet_name='Sheet1')

writer.save()
xlsx_data = output.getvalue()
```
dataframe的数据是一个包含timezone的datetime, 运行的话会报错:
```shell
......
ValueError: Excel does not support datetimes with timezones. Please ensure that datetimes are timezone unaware before writing to Excel.
```
我们可以把datetiem去掉timezone
```python
dt=datetime.datetime(2011, 8, 15, 8, 15, 12, 0, tzinfo=pytz.timezone('Asia/Shanghai'))
unaware_dt = dt.replace(tzinfo=None)
```
但是这样直接去掉timezone的话, 时间有可能不对, 比如数据库存的是UTC时间, 我们要显示的是当地时间, 所以我们需要做时区转换, 再去掉时区
```python
dt=datetime.datetime(2011, 8, 15, 8, 15, 12, 0, tzinfo=pytz.timezone('UTC'))
local_dt = dt.astimezone(pytz.timezone('Asia/Shanghai'))
unaware_dt = local_dt.replace('tzinfo=None')
```
这样pandas导出excel的时候就不报错了

但是新的问题来了, dataframe的一列数据都是带有时区的datetime, 应该怎么处理呢, 我们可以这样做, 先定义一个函数, 然后再做批量处理, 代码变成这样:
```python
import datetime
import io

import pandas as pd
import pytz
from pandas import Timestamp


def unaware_datetime(dt, tz):
    """将带有时区的datetime转换为不带时区的当地时间

    Args:
        dt: aware datetime
        tz: string, 例如Asia/Shanghai
    """
    local_dt = dt.astimezone(pytz.timezone(tz))
    return local_dt.replace(tzinfo=None)


# Create a Pandas dataframe from the data.
df = pd.DataFrame({'date': [datetime.datetime(2011, 8, 15, 8, 15, 12, 0, tzinfo=pytz.timezone('UTC'))]})

# 去掉时区
df.date = df.date.apply(lambda x: unaware_datetime(x, 'Asia/Shanghai') if type(x) == Timestamp else '')

output = io.BytesIO()

# Use the BytesIO object as the filehandle.
writer = pd.ExcelWriter(output, engine='xlsxwriter')

# Write the data frame to the BytesIO object.
df.to_excel(writer, sheet_name='Sheet1')

writer.save()
xlsx_data = output.getvalue()
```

备注:

在网上有看到这样的解决方式, ExcelWriter增加option选项:
```python
writer = pandas.ExcelWriter(string_io, engine='xlsxwriter', options={'remove_timezone': True})
```
本人测试并没有奏效
