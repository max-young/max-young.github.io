---
layout:     post
title:      "pandas导出StringIO excel"
subtitle:   ""
date:       2017-03-25
author:     "alvy"
header-img: "1nn.jpg"
header-mask: 0.3
catalog:    true
categories: Python
tags:
    - Python
    - Pandas
---

从数据库取出数据，并用pandas导出到excel，但是我们需要将文件上传到七牛，如果将文件保存到本地，再上传，太浪费资源了，所以我们先要将excel存储为StringIO，再将之上传。方法参考如下：    
[http://stackoverflow.com/questions/28058563/write-to-stringio-object-using-pandas-excelwriter](http://stackoverflow.com/questions/28058563/write-to-stringio-object-using-pandas-excelwriter)   

> Pandas expects a filename path to the ExcelWriter constructors although each of the writer engines support StringIO. Perhaps that should be raised as a bug/feature request in Pandas.    
> In the meantime here is a workaround example using the Pandas xlsxwriter engine:
> ```python
> import pandas as pd
> import StringIO
>
> io = StringIO.StringIO()
>
> # Use a temp filename to keep pandas happy.
> writer = pd.ExcelWriter('temp.xlsx', engine='xlsxwriter')
>
> # Set the filename/file handle in the xlsxwriter.workbook object.
> writer.book.filename = io
>
> # Write the data frame to the StringIO object.
> pd.DataFrame().to_excel(writer, sheet_name='Sheet1')
> writer.save()
> xlsx_data = io.getvalue()
> ```
> Update: As of Pandas 0.17 it is now possible to do this more directly:
> ```
> # Note, Python 2 example. For Python 3 use: > output = io.BytesIO().
> output = StringIO.StringIO()
>
> # Use the StringIO object as the filehandle.
> writer = pd.ExcelWriter(output, engine='xlsxwriter')
> ```
> See also [Saving the Dataframe output to a string](http://xlsxwriter.readthedocs.io/working_with_pandas.html#saving-the-dataframe-output-to-a-string) in the XlsxWriter docs.

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

导出csv
```python
header_dict = {
    "deliver_sku": "交付SKU",
    "deliver_sku_lv1_category": "交付SKU一级分类",
    "deliver_sku_lv2_category": "交付SKU二级分类",
    "deliver_sku_lv3_category": "交付SKU三级分类",
    "product_type": "得到p_type",
    "product_id": "得到p_id",
    "deliver_time": "交付时间"}
    
io = StringIO()
writer = csv.DictWriter(io, fieldnames=self.header_list)
writer.writerow(self.header_dict)
writer.writerows(rows_data)
f = ContentFile(io.getvalue().encode('utf-8-sig'))
filename = f'{self.report_name_display}_{self.task.id}.csv'
self.task.result_file_csv.save(filename, f)
```