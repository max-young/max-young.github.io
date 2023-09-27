---
layout: post
title: "SQLAlchemy"
date: 2023-09-27
categories: Database
tags:
  - Python
  - SQLAlchemy
---

- [查询](#查询)
- [listen event](#listen-event)
- [问题汇总](#问题汇总)
  - [in\_查询批量更新时报错](#in_查询批量更新时报错)
  - [server\_default 和 default](#server_default-和-default)



#### 查询

```python
query = db.session.query(
    CollectionCase.id, CollectionCase.label, CollectionCase.remark,
    CollectionCase.case_time, VehiclePilotFile.file_type,
    VehiclePilotFile.begin_time, VehiclePilotFile.end_time,
    VehiclePilotFile.vehicle_id).join(VehiclePilotFile).join(User).filter(
        User.username == username).slice((page - 1) * per_page,
                                          page * per_page).all()
```

#### listen event

```python
from sqlalchemy.event import listen

assoc_version_vehicle = Table(
    'version_vehicle',
    Model.metadata,
    Column('id',
           Integer,
           Sequence("version_vehicle_aid_seq", start=1, increment=1),
           primary_key=True),
    Column('version_id', Integer, ForeignKey('version.id')),
    Column('vehicle_id', Integer, ForeignKey('vehicle.id')),
)

class Vehicle(Model):
    """车辆
    """

    id = Column(Integer,
               Sequence("vehicle_aid_seq", start=1, increment=1),
               primary_key=True)
    ...

class Version(Model):
    """车辆自动驾驶版本
    """
    id = Column(Integer,
                Sequence("version_aid_seq", start=1, increment=1),
                primary_key=True)
    ...

    vehicles = relationship('Vehicle',
                            secondary=assoc_version_vehicle,
                            backref='version')

def push_version_after_version_create_or_update_listener(
        mapper, connection, target):
    """push version after create version
    """
    from app.utils import request_car_drive_mode
    version_name = target.name
    for car in target.vehicles:
        if request_car_drive_mode(car.carid) == "ready":
            threading.Thread(target=push_version_by_name_and_carid,
                             args=(version_name, car.carid)).start()

def push_version_after_vesion_append_vehicle_listener(mapper, connection,
                                                      target):
    """push version after create assoc_version_vehicle
    """
    print(target)

    from app.tasks import push_version_by_name_and_carid
    version_name = mapper.name
    car = connection
    threading.Thread(target=push_version_by_name_and_carid,
                     args=(version_name, car.carid, True)).start()


# listen Version 的 after_insert 和 after_update 事件
listen(Version, 'after_insert',
       push_version_after_version_create_or_update_listener)
listen(Version, 'after_update',
       push_version_after_version_create_or_update_listener)

# listen Version 添加 vehicle 事件
listen(Version.vehicles, 'append',
       push_version_after_vesion_append_vehicle_listener)
```


#### 问题汇总


##### in\_查询批量更新时报错

参考资料：<https://stackoverflow.com/questions/33703070/using-sqlalchemy-result-set-for-update>

代码示例：

```python
session.query(cls).filter(cls.id.in_(ids)).update({"password": ******})
```

查询时采用`in_`时，update 会报错，错误信息如下:

```shell
InvalidRequestError: Could not evaluate current criteria in Python. Specify 'fetch' or False for the synchronize_session parameter.
```

设置 synchronize_session 的值为 False 或者 fetch 即可

```python
session.query(cls).filter_by(id=id).update({"password": ******}, synchronize_session=False)
```

官方文档参照：<http://docs.sqlalchemy.org/en/latest/orm/query.html?highlight=query.update#sqlalchemy.orm.query.Query.update.params.synchronize_session>


##### server_default 和 default

看这个代码:

```python
from sqlalchemy.sql import func
class Version(Model):
    ...
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
```

为什么 time_created 用 server_default，time_updated 用 default?  
server_default 会更新已有数据, default 不会
