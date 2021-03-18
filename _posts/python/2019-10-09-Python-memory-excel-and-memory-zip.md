---
layout:     post
title:      "Python memory excel and memory zip"
subtitle:   ""
date:       2019-10-09
categories: Python
tags:
    - Python
    - Pandas
---

常见的场景是将本地磁盘文件压缩成一个zip文件并保存到磁盘, 但是在web服务中, 更常见的场景是在内存中生成二进制文件, 返回给客户端, 或者上传到云存储, 而没必要存储文件到磁盘中.
下面的例子里就是生成BytesIO的excel文件, 并压缩, 可以将压缩文件存储到本地, 也可以生成BytesIO的压缩数据.
```python
import zipfile
from io import BytesIO

import pandas as pd


def generate_zip_memory(files):
    mem_zip = BytesIO()

    with zipfile.ZipFile(mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.writestr(f[0], f[1])
    return mem_zip.getvalue()


def generate_zip(files):
    mem_zip = "./test.zip"

    with zipfile.ZipFile(mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for f in files:
            zf.writestr(f[0], f[1])
    return zf


def generate_excel(data):
    output = BytesIO()
    df = pd.DataFrame(data, columns=[1, 'aaaa', 'field1', 'field2'])
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False, header=['aaaa', 'bbbbbb', 'cccc', 'dddddd'])
    writer.save()
    excel = output.getvalue()
    output.close()
    return excel


def main():
    excel_data = [
        [{'field1': 'a1', 'field2': 'a2', 1: '1', 'aaaa': 'a3'},
         {'field1': 'b1', 'field2': 'b2', 'aaaa': 'b3', 1: 2}],
        [{'field1': '2a1', 'field2': '2a2', 1: '21', 'aaaa': '2a3'},
         {'field1': '2b1', 'field2': '2b2', 'aaaa': '2b3', 1: 2}]
    ]
    excel_files = []

    for i, data in enumerate(excel_data):
        excel = generate_excel(data)
        excel_files.append((f'excel{i}.xlsx', excel))

    zip_memory = generate_zip_memory(excel_files)
    print(zip_memory)
    zip_memory = generate_zip(excel_files)
    print(zip_memory)


if __name__ == "__main__":
    main()
```


