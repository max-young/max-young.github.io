---
layout:     post
title:      "Pandas导出StringIO excel"
subtitle:   ""
date:       2019-08-21
categories: Database
tags:
    - Python
    - Pandas
---

从数据库取出数据，并用pandas导出到excel，但是我们需要将文件上传到七牛，如果将文件保存到本地，再上传，太浪费资源了，所以我们先要将excel存储为StringIO，再将之上传。方法参考如下：
<https://xlsxwriter.readthedocs.io/working_with_pandas.html#saving-the-dataframe-output-to-a-string>

```python
import pandas as pd
import io

# Create a Pandas dataframe from the data.
df = pd.DataFrame({'Data': [10, 20, 30, 20, 15, 30, 45]})

output = io.BytesIO()

# Use the BytesIO object as the filehandle.
writer = pd.ExcelWriter(output, engine='xlsxwriter')

# Write the data frame to the BytesIO object.
df.to_excel(writer, sheet_name='Sheet1')

writer.save()
xlsx_data = output.getvalue()

# Do something with the data...
```
