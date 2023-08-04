---
layout: post
title: "dingtalk upload file and send to group chat"
date: 2023-08-04
categories: DevOps
tags:
  - ali
  - DingTalk
---

```python
import io

import plotly.graph_objects as go
import requests

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
        "Name": "yl",
        "Age": 35,
        "City": "cy"
    },
]

headers = list(json_data[0].keys())
data = [list(row.values()) for row in json_data]
table_fig = go.Figure(
    data=[go.Table(header=dict(values=headers), cells=dict(values=data))])

# 转换为buffer做上传
image_bytes = table_fig.to_image(format="png")
buffer = io.BytesIO(image_bytes)

# 上传文件
# 获取app key和app token, 需要在钉钉开发者后台创建一个应用, 在应用首页可以获得
get_token_request = requests.get(
    "https://oapi.dingtalk.com/gettoken?appkey=<app key>&appsecret=<app secret>"
)
token = get_token_request.json()['access_token']
upload_file_request = requests.post(
    "https://oapi.dingtalk.com/media/upload?access_token=" + token,
    files={'media': ('table_image.png', buffer, 'image/png')},
    data={'type': 'image'})
# 获取media id
media_id = upload_file_request.json()['media_id']

# 群机器人的webhook
webhook_url = 'https://oapi.dingtalk.com/robot/send?access_token=094919c2940272ec84c747f0ef0e112d0a047882bde50d3c3646d9248fb61a8b'
# text = "#### 2023-08-03运营情况\n- 总里程: 156km\n- 订单量: 156\n\n[查看详情]({})".format(media_id)
# data = {"msgtype": "markdown", "markdown": {"title": "数据指标", "text": text}}
# data = {
#     "msgtype": "actionCard",
#     "actionCard": {
#         "title": "数据指标",
#         "text": text,
#         "singleTitle": "查看详情",
#         "singleUrl": "http://www.baidu.com"
#     }
# }
data = {
    "msgtype": "link",
    "link": {
        "text": "#### 2023-08-03运营情况\n\n- 总里程: 156km\n\n- 订单量: 156\n\n",
        "title": "2023-08-03白犀牛运营数据指标",
        "picUrl": media_id,
        "messageUrl": media_id
    }
}
headers = {'Content-Type': 'application/json'}
response = requests.post(webhook_url, json=data, headers=headers)
print(response.text)
```
