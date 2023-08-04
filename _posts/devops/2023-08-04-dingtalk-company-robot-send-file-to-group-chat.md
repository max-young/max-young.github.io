---
layout: post
title: "dingtalk company robot send file to group chat"
date: 2023-08-04
categories: DevOps
tags:
  - ali
  - DingTalk
---

```python
import sys

from typing import List
import json

from alibabacloud_dingtalk.robot_1_0.client import Client as dingtalkrobot_1_0Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_dingtalk.robot_1_0 import models as dingtalkrobot__1__0_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient


class Sample:

    def __init__(self):
        pass

    @staticmethod
    def create_client() -> dingtalkrobot_1_0Client:
        """
        使用 Token 初始化账号Client
        @return: Client
        @throws Exception
        """
        config = open_api_models.Config()
        config.protocol = 'https'
        config.region_id = 'central'
        return dingtalkrobot_1_0Client(config)

    @staticmethod
    def main(args: List[str], ) -> None:
        client = Sample.create_client()
        org_group_send_headers = dingtalkrobot__1__0_models.OrgGroupSendHeaders(
        )
        # token和图片的media id的获取可以参考上一篇文章: /blog/dingtalk-upload-file-and-send-to-group-chat.html
        org_group_send_headers.x_acs_dingtalk_access_token = '026688673ceb39cb9359817123443240940dbb8'
        msg_param = {
            "text": "text",
            "title": "fdsafds",
            "picUrl": "@lALYH8_u_2ND2NAfTNArw",
            "messageUrl": "@lALYaH8_u_2NDNAffTNArw"
        }
        msg_key = "sampleLink"
        msg_param = {"photoURL": "@lALPDfYH8_u_2NDNAfTNArw"}
        msg_key = 'sampleImageMsg'
        msg_param = {
            "title": "测试标题",
            "text": "内容测试",
            "singleTitle": "查看详情",
            "messageUrl": "@lALPDfYH8_u_2NDNAfTNArw"
        }
        msg_key = "sampleActionCard"
        # open_concersion_id 是指群的id, 可以通过开发者平台调用接口获取: https://open.dingtalk.com/tools/explorer/jsapi?id=10301
        # robot code是指你创建的钉钉应用, 打开消息推送后, 获得的robotcode
        org_group_send_request = dingtalkrobot__1__0_models.OrgGroupSendRequest(
            msg_param=json.dumps(msg_param),
            msg_key=msg_key,
            open_conversation_id='cidl8sInTnpwgOeREIM9qRh3w==',
            robot_code='dingzsi8issmws8aukox',
        )
        try:
            client.org_group_send_with_options(org_group_send_request,
                                               org_group_send_headers,
                                               util_models.RuntimeOptions())
        except Exception as err:
            print(err)
            if not UtilClient.empty(err.code) and not UtilClient.empty(
                    err.message):
                # err 中含有 code 和 message 属性，可帮助开发定位问题
                pass


if __name__ == '__main__':
    Sample.main(sys.argv[1:])
```
