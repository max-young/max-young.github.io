---
layout:     post
title:      "SQLAlchemy Model field value related to another column"
date:       2022-08-15
categories: Database
tags:
    - Python
    - MySQL
    - SQLAlchemy
---

有这样的一个model:
```Python
class Version(Model):
    name = Column(String(50), unique=True, nullable=False)
    detail = Column(String(250))
```
name是版本名称, 规则是`\d+\.\d+\.\d+$`, 三个数字用两个点相连, 需要按照版本名称排序, 例如:
```text
1.2.3
1.2.1
0.1.2
0.1.0
```
如果就按照name字段排序, 咋一看好像没问题, 但是我们会发现, 1.2.0会排在1.12.0之前, 所以我想到一个解决方案, 根据name计算出一个数值, 然后存到另一个字段name_value中, 计算规则是:
```python
name_spilit = name.split('.')
# 版本的三个数字最大为999, 相当于3位的1000进制数
name_value = int(name_spilit[0]) * 1000000 + int(name_spilit[1]) * 1000 + int(name_spilit[2])
```
model就变成:
```python
class Version(Model):
    name = Column(String(50), unique=True, nullable=False)
    detail = Column(String(250))
    name_value = Column(Integer)
```
计算规则有了, 怎么实现这个model在创建和更新的时候自动计算这个name_value呢? sqlalchemy给column提供了default和onupdate两个属性, 可以设置默认值和更新时计算的值, model的创建时间和更新时间就可以通过这两个属性来实现:
```python
from sqlalchemy.sql import func
class Version(Model):
    ...
    time_created = Column(DateTime(timezone=True), default=func.now())
    time_updated = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
```
创建时会调用default函数, 编辑时会调用onupdate函数.  
但是现在的情况是name_value需要和其他column name关联, 而不是独立的计算, 怎么实现呢? 
```python
def version_name_value(context):
    """计算版本名称的值用于排序

    Args:
        context: sqlalchemy context
    Returns:
        value: int
    """
    version_name = context.get_current_parameters()["name"]
    version_split = version_name.split(".")
    value = int(version_split[0]) * 1000000 + int(version_split[1]) * 1000 + int(version_split[2])
    return value

class Version(Model):
    name = Column(String(50), unique=True, nullable=False)
    name_value = Column(Integer,
                        default=version_name_value,
                        onupdate=version_name_value,
                        comment="版本名称的计算数值, 用于排序")
    detail = Column(String(250))
```
version_name_value函数的参数是context, context是sqlalchemy的上下文, 它能获取到你在创建和更新的时候传入的name值.  
that's it. 等等, 我们看函数里的这一条语句: `version_name = context.get_current_parameters()["name"]`  
我们能保证`context.get_current_parameters()`里一定有`name`这个key吗? 这样写不会报错吗?  
如果我们认真测试, 会发现如果我们编辑一条数据, 只修改其他数据, 例如detail字段, 不修改name, 那么就是会报错, 不存在name这个key.    
如果修改name则没有问题, 创建时因为name是必填的, 所以也没有问题.  
怎么解决? 如何获取已存在但是不需要修改的name值, context能获得吗? 很遗憾, 我尝试了很多方法, 但是都没有解决.  
这条路好像不通, 看看有没有其他方法, 中间的艰辛略去不表.  
最后的解决方案是, 采用sqlalchemy的event listen方法:
```Python
def version_name_value(version_name):
    """计算版本名称的值用于排序

    Args:
        version_name: string, Version.name, 版本名称
    Returns:
        value: int
    """
    version_split = version_name.split(".")
    value = int(version_split[0]) * 1000000 + int(version_split[1]) * 1000 + int(version_split[2])
    return value


def update_version_name_value(target, version_name, old_version_name,
                              initiator):
    """Version.name变化时, 更新Version.name_value

    Args:
        target: Version, 版本对象
        version_name: string, Version.name, 新的版本名称
        old_version_name: string, Version.name, 旧的版本名称
        initiator: sqlalchemy.orm.attributes.AttributeEvent object, 暂时不用
    Returns:
        None
    """
    if version_name != old_version_name:
        target.name_value = version_name_value(version_name)


# 监听Version.name变化, 调用update_version_name_value函数, retval=False代表update_version_name_value函数不用返回值
listen(Version.name, 'set', update_version_name_value, retval=False)
```
name_value也不需要default和onupdate了:
```python
class Version(Model):
    name = Column(String(50), unique=True, nullable=False)
    name_value = Column(Integer, comment="版本名称的计算数值, 用于排序")
    detail = Column(String(250))
```
