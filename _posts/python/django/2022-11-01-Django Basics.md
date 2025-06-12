---
layout: post
title: "Django Basics"
subtitle: ""
date: 2025-06-10
categories: Backend
tags:
  - Python
  - Django
---

- [commands](#commands)
  - [create super user](#create-super-user)
  - [dumpdata 导出数据](#dumpdata-导出数据)
  - [startapp 创建应用](#startapp-创建应用)
- [问答](#问答)
  - [如何卸载 app](#如何卸载-app)
  - [static file](#static-file)

## commands

### create super user

```shell
$ python manage.py createsuperuser
```

### dumpdata 导出数据

我们可以使用 loaddata 命令将 fixtures 里的 json 文件写入到数据库，dumpdata 是相反的过程
dumpdata 可以将数据库里的数据生成 json 文件，供 loaddata 使用
<https://coderwall.com/p/mvsoyg/django-dumpdata-and-loaddata>
举例如下：
我们要将 contract app 下的 contracttemplate 表的数据导出，那么命令是：

```
$ python manage.py dumpdata contract.contracttempalte > template.json
```

默认是 json 格式，也可以指定其他格式
为了美观，也可以加上`--indent 2`, 还可以指定 pk 来导出, 示例命令:

```shell
python manage.py dumpdata sale.orderraw --pk=875087 --indent=2 --settings=chronosphere.settings_env > csvoucher/fixtures/test_orderraw.json
```

### startapp 创建应用

```shell
$ python manage.py startapp <app name>
```

使用这个命令可以在项目下新建一个应用, Django 已帮我们生成好了基础目录结构, 我们就可以专心去开发了

## 问答

### 如何卸载 app

<https://stackoverflow.com/questions/3329773/django-how-to-completely-uninstall-a-django-app>

1. Django < 1.7 has a handy management command that will give you the necessary SQL to drop all the tables for an app. See the [sqlclear docs](http://docs.djangoproject.com/en/dev/ref/django-admin/?from=olddocs#sqlclear-appname-appname) for more information. Basically, running `./manage.py sqlclear my_app_name` gets you get the SQL statements that should be executed to get rid of all traces of the app in your DB. You still need to copy and paste (or pipe) those statements into your SQL client. For Django 1.7 and up, use `./manage.py migrate my_app_name zero` (see the [migrate](https://docs.djangoproject.com/en/2.1/ref/django-admin/#migrate) docs), which runs the database cleaning automatically.
2. To remove the app from your project, all you need to do is remove it from `INSTALLED_APPS` in your project's `settings.py`. Django will no longer load the app.
3. If you no longer want the app's files hanging around, delete the app directory from your project directory or other location on your PYTHONPATH where it resides.
4. (optional) If the app stored media files, cache files, or other temporary files somewhere, you may want to delete those as well. Also be wary of lingering session data that might be leftover from the app.
5. (optional) I would also remove any stale content types.

Like so.

```Python
from django.contrib.contenttypes.models import ContentType
for c in ContentType.objects.all():
    if not c.model_class():
        print "deleting %s"%c
        c.delete()
```

总结:

在 settings 里面的 INSTALLED_APPS 里面去掉即可, 如有必要手动删掉 APP 路径

### static file

static 存储了 css 样式, 我们部署到生产环境时, 将 debug 设为 false, 会发现 css 样式没了, 404.  
可以这样解决, 在 url 里加上这些:

```python
from django.urls import re_path
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    re_path(r'^static/(?P<path>.*)$', serve,
            {'document_root': settings.STATIC_ROOT}),
]
```

settings.STATIC_ROOT 是这样配置的:

```
STATIC_ROOT = BASE_DIR / 'static'
```

之前已经用 collectstatic 命令将 css 文件汇集到此路径下了
