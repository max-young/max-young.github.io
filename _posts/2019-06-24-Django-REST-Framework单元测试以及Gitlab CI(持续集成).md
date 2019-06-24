---
layout: post
title: Django REST Framework单元测试以及Gitlab CI(持续集成)
subtitle:   ""
date:       2019-06-24
categories: backend
tags: 
    - Python
---

## 单元测试

#### 单元测试

单元测试的代码可以写在app下的`tests.py`文件里, 如果测试很多很复杂, 要分为好几个文件, 则在app里新建一个`tests`文件夹, 在文件夹里写测试代码(文件夹里需要有`__init__.py`文件)

先上示例代码:

```python
import json

from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.test import (APIRequestFactory, APITestCase,
                                 force_authenticate)


class CSVoucherTestCase(APITestCase):
    """CSVoucherViewSet测试
    """
    @classmethod
    def setUpClass(cls):
        ...
        cls.factory = APIRequestFactory()
        cls.User = User.objects.get(username='max')

    @classmethod
    def tearDownClass(cls):
        print('-' * 30 + 'test csvoucher complete' + '-' * 30)

    def test_create_cs_voucher(self):
        """测试创建维权单
        """
        url = reverse('csvoucher-list')
        request = self.factory.post(url, json.dumps(request_data), content_type='application/json')
        force_authenticate(request, user=self.user)
        create_cs_voucher = CSVoucherViewSet.as_view({'post': 'create'})
        response = create_cs_voucher(request)
        self.assertEqual(response.status_code, 201)
```

Django REST framework有自己的测试库APIRequestFactory, APITestCase, 参照文档<https://www.django-rest-framework.org/api-guide/testing/>

代码实现过程中有几个需要注意的点:

- setUpClass和tearDownClass

  下面的示例代码包括setUpClass和teardownClass, 一个TestCase类可包括多个测试函数, setUp和tearDown是每个测试函数执行之前和之后都会执行, setUpClass和tearDownClass是TestCase是实例化之前和之后会执行, 也就是说多个测试函数, 只会执行一次. 在下面的示例代码中, 因为多个测试函数都需要一个新的订单数据, 只需要创建一个新订单, 不需要重复创建, 所以把这一部分代码写入到setUpClass里, setUpClass和tearDownClass是必须成对出现, 不能只写setUpClass而不写tearDownClass

- reverse

  reverse能根据view函数获取url地址, 而不用担心url配置修改, 例如:

  ViewSet如下所示, 复写了list方法, 自定义了一个custom_fun函数, detail=True: 

  ```python
  from rest_framework import mixins, viewsets
  from rest_framework.decorators import actions
  
  class CSVoucherViewSet(viewsets.ReadOnlyModelViewSet, mixins.CreateModelMixin):
      serializer_class= CSVoucherSerializer
      queryset = CSVoucher.objects.all()
      
      def list(self, request, *args, **kwargs):
          pass
      
      @actions(detail=True, methods=['POST'])
      def custom_func(self, request, pk=None):
          pass
  ```

  url配置是这样的:

  ```python
  router.register('csvoucher', csvoucher_view.CSVoucherViewSet, 'csvoucher')
  ```

  那么rever的对应写法应该是:

  ```python
  # router的basename和viewset的函数名称用-连接,需要注意的是函数名称如有有下划线_, 需要改成连接线-, 如果detai=True, 需要加上args 
  url = reverse('csvoucher-list')
  url = reverse('csvoucher-custom-func', args=[123])
  ```

- APIRequestFactory的json数据请求和强制认证

  ```python
  request= APIRequestFactory.post(url, json.dumps(request_data), content_type='application/json')
  force_authenticate(request, user)
  ```

#### 使用已有数据库

写完测试代码之后, 就可以执行`./manage.py test`命令来进行测试了, 参照文档https://docs.djangoproject.com/en/2.1/topics/testing/overview/#running-tests

Django的测试会新创建一个空的测试数据库, 测试完成之后, 测试数据库会自动删除.

实际工作中, 可能项目非常大, models非常复杂, 而且依赖很多初始化数据, 会导致测试之前的准备工作(自动测试数据库, setUp写fixture等工作)异常复杂且容易出错, 所以考虑用已有的测试数据库来进行测试, 省却了这些繁重的工作, 那么如何实现测试使用已有数据库呢? 我们需要自定义admin command来实现, 自定义command参照文档<https://docs.djangoproject.com/en/2.1/howto/custom-management-commands/>

自定义测试admin command的示例代码如下:

在app下新建`./management/commands/testcsvoucher.py`

```python
import unittest

from django.core.management.base import BaseCommand
from csvoucher.tests.test_views import CSVoucherTestCase


class Command(BaseCommand):
    """测试csvoucher

    自定义command可以使用测试环境的数据库, 减少相关数据依赖的限制
    """
    help = 'test csvoucher use real database'

    def handle(self, *args, **options):
        # load上面写的单元测试的类CSVoucherTestCase, 可以load多个, run多个
        cs_voucher_suite = unittest.TestLoader().loadTestsFromTestCase(CSVoucherTestCase)
        unittest.TextTestRunner().run(cs_voucher_suite)
```

这样执行`./manage.py testcsvoucher`就会使用默认settings里的数据库来进行测试, 虽然是使用的已有数据库, 但是新创建的数据也会自动删除. 测试的时候可能用的是测试settings文件, 那么测试命令就是:

```shell
$ ./manage.py testcsvoucher --settings=chronosphere.settings_test
```

#### 测试覆盖率

写完测试代码, 可能还需要知道测试代码覆盖整个项目的比率, 太低了达不到测试的效果, 覆盖率可以采用coverage库, 文档地址: <https://coverage.readthedocs.io/en/v4.5.x/>

安装之后, 测试命令改为:

```shell
# source为当前路径, 即项目下的所有文件, omit参数忽略相关文件
$ coverage run --source="." --omit="./venv/*","./*/migrations/*","*__init__*" manage.py testcsvoucher --settings=chronosphere.settings_test
```

运行之后查看报告

```shell
$ coverage report
```

我们可以加上检查覆盖率的参数

```shell
# 覆盖率不低于5%
$ coverage report --fail-under=5
```

以上两个命令的输出是一样的, 但是状态不一样, 我们可以用`echo $?`来查看上一条命令的状态, 如果覆盖率低于5, 则状态为2, 大于等于5则为0 , 状态不为0代表异常, 持续集成会不成功(下面会讲到)

## 持续集成

#### Gitlab持续集成配置文件

Gitlab持续集成在这里不在赘述, 参照文档: <https://docs.gitlab.com/ee/ci/README.html>

项目根部录下`gitlab-ci.yml`内容如下:

```yaml
image: docker:stable

stages:
  - build
  - test

before_script:
    # - docker info
  - docker login

test:
  services:
    - docker:dind
  stage: test
  script:
    - docker run --env-file=.test-env $CONTAINER_IMAGE:$CI_COMMIT_REF_NAME test

build:
  services:
    - docker:dind
  stage: build
  script:
    - docker build
    - docker push $CONTAINER_IMAGE:$CI_COMMIT_REF_NAME
```

代码push之后会依次执行build和test, build和test都依赖docker:stable镜像, build构建镜像, 并推送, 第二步test会依赖第一步的镜像, 在此镜像下执行test, 那么test会执行什么呢? 我们看下一步

#### Docker自定义命令EntryPoint

docker的DockerFile的内容如下:

```yml
...

ENTRYPOINT ["/entrypoint.sh"]
```

我们可以自定义命令, 命令执行的内容写在entrypoint.sh里面:

```sh
#!/bin/bash

if [ ! -z $1 ] ; then
    COMMAND=$@
fi

if [ "$COMMAND" = "test" ] ; then
    coverage run --source="." --omit="./venv/*","./*/migrations/*","*__init__*" manage.py testcsvoucher --settings=chronosphere.settings_env
    coverage report --fail-under=5
fi
```

如果是test, 则执行上一节提到的覆盖率的命令, 在这里如果覆盖率低于5, 则会报错, CI无法通过


