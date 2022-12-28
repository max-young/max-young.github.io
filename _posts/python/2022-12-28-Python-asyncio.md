---
layout: post
title: "Python asyncio"
subtitle: ""
date: 2022-12-28
categories: Python
tags:
  - Python
---

场景是这样的:\
我需要导出合同数据的 excel 文件,合同有一项数据叫"优惠分摊比",需要从另外一个微服务来获取\
如果我循环从这个微服务来获取,每次请求的耗时在 0.5 秒左右,如果我要导出一百条合同数据,那么请求的时间就需要 0.5s\*100=50s 的时间,再加上其他写入 excel 的时间,耗时太久,用户体验很差,也会超时\
所以我们考虑通过 asyncio 来协程请求,这样能大大缩短请求获取数据的时间, 具体代码实现是这样的

```python
import asyncio
import aiohttp

from common.exceptions import CommonError


async def get_discount_apportionment_from_tether_by_aiohttp(contract_sn_discount_dict, contract_sn):
    """通过aiohttp从tether获取优惠分摊比
    """
    target_url = '{}{}'.format(api_root_url, f'contract/')
    headers = {'Authorization': 'Token 5dfas3465fs46fds54',
               'Content-Type': 'application/json'}
    params = {'sn': contract_sn}
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(target_url, params=params) as response:
                tether_info = await response.json()
                response.close()
    except Exception:
        raise CommonError('micro_service_connect_error', message_params='tether')
    ......
    contract_sn_discount_dict[contract_sn] = discount_info
    return True

async def asynchronous_contract_discount_data(contract_sn_data_dict, contract_instances):
    """协程从tether获取我方优惠分摊比数据
    """
    futures = [MicroServiceUtils.get_discount_apportionment_from_tether_by_aiohttp(
        contract_sn_data_dict, i.sn) for i in contract_instances]
    for i, future in enumerate(asyncio.as_completed(futures)):
        await future

def contract_list_excel(contract_instances):
    """导出合同数据excel
    """
    # 创建数据表
    wb = Workbook()
    # 创建sheet
    ws1 = wb.active
    # 获取合同sn对应的我方优惠分摊比数据
    contract_sn_data_dict = {}
    ioloop = asyncio.new_event_loop()
    asyncio.set_event_loop(ioloop)
    ioloop.run_until_complete(cls.asynchronous_contract_discount_data(contract_sn_data_dict, contract_instances))
    ioloop.close()
    # 将合同数据写入excel
    for contract_instance in contract_instances:
        ...
    return wb
```
