---
layout: post
title: "Python Plotly"
date: 2023-08-07
categories: Python
tags:
  - Python
---

we can use plotly to draw figure or table.

```python
import io

import plotly.graph_objects as go


json_data = [
    {
        "Name": "lc11111",
        "Age": 30,
        "City": "cy"
    },
    {
        "Name": "hd",
        "Age": 25,
        "City": "hd"
    },
    {
        "Name": "杨乐",
        "Age": 35,
        "City": "cy"
    },
]

headers = list(json_data[0].keys())
data = [list(row.values()) for row in json_data]
table_fig = go.Figure(
    data=[go.Table(header=dict(values=headers), cells=dict(values=data))])

# solve chinese display problem
# sudo apt-get update
# sudo apt-get install fonts-wqy-microhei fonts-wqy-zenhei
font_name = "文泉驿微米黑"
table_fig.update_layout(font=dict(family=font_name))

# 保存到本地
table_fig.write_image("table_image.png")

# or 转换为buffer, buffer可以用于post请求上传
image_bytes = table_fig.to_image(format="png")
buffer = io.BytesIO(image_bytes)
```
