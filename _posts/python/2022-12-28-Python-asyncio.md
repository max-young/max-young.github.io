---
layout: post
title: "Python asyncio"
subtitle: ""
date: 2022-12-28
categories: Python
tags:
  - Python
---

- [asyncio 名词解释](#asyncio-名词解释)
- [asyncio 的基本用法:](#asyncio-的基本用法)
- [其他](#其他)
  - [RuntimeError: asyncio.run() cannot be called from a running event loop](#runtimeerror-asynciorun-cannot-be-called-from-a-running-event-loop)

#### asyncio 名词解释

asyncio 能实现 concurrent, 在一个线程里交替执行任务, 不用等一个任务完成才能执行另外一个任务, 所以特别适用于 io 高的场景

event loop: 事件循环, 用来调度协程的执行, 一个线程只能有一个事件循环

#### asyncio 的基本用法

以实际例子来说明:
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

#### 其他

##### RuntimeError: asyncio.run() cannot be called from a running event loop

```python
import asyncio

async def main():
    print('hello')
    await asyncio.sleep(1)
    print('world')

asyncio.run(main())
```

[`asyncio.run()`](https://docs.python.org/3.9/library/asyncio-task.html#asyncio.run)执行`main()`, `main`用`async`定义, 所以它是一个 coroutine, `asyncio.run()`会创建一个 event loop, 执行 coroutine main, 完成之后会关闭 loop, 但是如果线程里已经有 loop 了, 那么就会报错: `RuntimeError: asyncio.run() cannot be called from a running event loop`  
(这里需要报这个错误的简单实例, 我在实际项目中遇到了此错误, 但是场景太复杂)  
如何解决这个问题呢? 思路是获取线程里的 event loop, 如果没有则创建, 然后用这个 loop 来执行 coroutine, 代码如下:

```python
try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
task = loop.create_task(main())
loop.run_until_complete(task)
```
