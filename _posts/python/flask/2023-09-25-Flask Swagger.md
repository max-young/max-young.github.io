---
layout: post
title: "Flask Swagger"
date: 2023-09-25
categories: Python
tags:
  - Flask
  - swagger
---

- [install](#install)
- [usage](#usage)
- [POST example](#post-example)
- [get example](#get-example)


we can use [flasgger](https://github.com/flasgger/flasgger)

### install

```vash
pip install flasgger
```

### usage

use flasgger in flask like this:

```python
from flasgger import Swagger
from flask import Flask

app = Flask(__name__)

Swagger(app,
        template={
            "info": {
                "title": "Surge数据平台API",
                "version": "1.0.0"
            },
        })
```

after run flask, we can see swagger ui in http://[host]:[port]/apidocs/

### POST example

this is a example for post json api:

```python
@bp.route("/analyse/", methods=["POST"])
def analyse_api():
    """拉取车辆自动驾驶数据接口
    ---
    tags:
        - 车辆数据
    parameters:
      - in: body
        name: body
        schema:
          required:
            - carId
            - beginTime
            - endTime
            - analyseType
          properties:
            carId:
              type: integer
              description: "车辆id"
              example: 13
            beginTime:
              type: string
              description: "开始时间, 格式: %Y-%m-%d %H:%M:%S"
              example: "2021-08-03 10:00:00"
            endTime:
              type: string
              description: "开始时间, 格式: %Y-%m-%d %H:%M:%S"
              example: "2021-08-03 10:00:30"
            analyseType:
              type: string
              description: "分析类型: <br> video: 视频 <br> simple: 小S <br> complete: 全量 <br> latency: 时延 <br>\
                  collision: 碰撞 <br> perception: 感知 <br> control: 控制 <br> general: 速度坐标等数据"
              enum: ["video", "simple", "complete", "latency", "collision", "perception", "control", "general"]
              example: "video"
    responses:
        200:
            description: 拉取数据成功
            schema:
                type: object
                properties:
                    status:
                        type: integer
                        example: 1
                    message:
                        type: string
                        example: "异步拉取数据任务已开始"
                    file_id:
                        type: integer
                        description: "文件id"
                        example: 1
        400:
            description: 拉取数据失败
            schema:
                type: object
                properties:
                    status:
                        type: integer
                        example: 2
                    message:
                        type: string
                        example: "拉取数据失败"

    """
    ...
```

### get example

this is a example for get:

```python
@bp.route('/<int:file_id>', methods=['GET'])
def vehicle_pilot_file_view(file_id):
    """车辆自动驾驶文件接口
    ---
    tags:
      - 车辆数据
    parameters:
      - name: file_id
        in: path
        type: integer
        required: true
        description: 文件id
    responses:
      200:
        description: 文件信息
        schema:
          properties:
            car_id:
              type: string
              description: 车辆id
              example: 001
            begin_time:
              type: string
              description: 开始时间
              example: 2019-01-01 00:00:00
            begin_time:
              type: string
              description: 结束时间
              example: 2019-01-01 00:00:30
            file_type:
              type: string
              description: "分析类型: <br> video: 视频 <br> simple: 小S <br> complete: 全量 <br> latency: 时延 <br>\
                collision: 碰撞 <br> perception: 感知 <br> control: 控制 <br> general: 速度坐标等数据"
              enum: ["video", "simple", "complete", "latency", "collision", "perception", "control", \
                "general"]
            data_path:
              type: string
              description: 文件路径
              example: "/data5/surge/data_coll_box_store/20230323/white-rhino-018/
white-rhino-018.20230323.collbox.1679536799.1679536801"
            data_status:
              type: integer
              description: "文件状态: <br> 0: 初始状态 <br> 1: 正在拉取 <br> 2: 拉取完成 <br> 3: 拉取失败"
              enum: [0, 1, 2, 3]
      404:
        description: 文件不存在
    """
    ...
```
