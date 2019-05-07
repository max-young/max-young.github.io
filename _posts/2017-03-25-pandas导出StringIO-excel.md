---
layout:     post
title:      "pandas导出StringIO excel"
subtitle:   ""
date:       2017-03-25 18:46:00
author:     "alvy"
header-img: "img/post-bg-blue-jasmine.jpg"
header-mask: 0.3
catalog:    true
tags:
    - Python
    - pandas
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