---
layout: post
title: Django REST Framework单元测试以及Gitlab CI(持续集成)
subtitle:   ""
date:       2019-07-10
categories: Backend
tags: 
    - Python
    - Django
---

- [单元测试](#单元测试)
  - [基本单元测试](#基本单元测试)
  - [使用已有数据库进行测试](#使用已有数据库进行测试)
  - [mock第三方API接口](#mock第三方api接口)
  - [测试覆盖率](#测试覆盖率)
- [集成测试](#集成测试)
- [消费者驱动契约测试CDCT](#消费者驱动契约测试cdct)
  - [CDCT的概念和原理](#cdct的概念和原理)
  - [CDCT的具体实现](#cdct的具体实现)
- [持续集成](#持续集成)
  - [Gitlab持续集成配置文件](#gitlab持续集成配置文件)
  - [Docker自定义命令EntryPoint](#docker自定义命令entrypoint)
- [参考资料](#参考资料)

## 单元测试

### 基本单元测试

> 单元测试（英语：Unit Testing）又称为模块测试，是针对程序模块（软件设计的最小单位）来进行正确性检验的测试工作。程序单元是应用的最小可测试部件。在过程化编程中，一个单元就是单个程序、函数、过程等；对于面向对象编程，最小单元就是方法，包括基类（超类）、抽象类、或者派生类（子类）中的方法。

单元测试的代码可以写在app下的`tests.py`文件里, 如果测试代码很多, 要分为好几个文件, 则在app里新建一个`tests`文件夹, 在文件夹里写测试代码(文件夹里需要有`__init__.py`文件)

以测试Django REST Framework的viewset的其中一个接口为例:

```python
import json

from django.contrib.auth.models import User
from rest_framework.reverse import reverse
from rest_framework.test import (APIRequestFactory, APITestCase,
                                 force_authenticate)


class CSVoucherTestCase(APITestCase):
    """CSVoucherViewSet测试
    """

    def setUp(cls):
        cls.factory = APIRequestFactory()
        cls.User = User.objects.get(username='max')

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

  一个TestCase类可包括多个测试函数, setUp和tearDown是每个测试函数执行之前和之后执行, setUpClass和tearDownClass是TestCase是测试类运行之前和之后会执行, 也就是说多个测试函数, 只会执行一次. 例如测试类里的多个测试函数都需要新订单, 只需要创建一个新订单, 不需要重复创建, 所以把创建订单的代码写入到setUpClass里(备注: setUpClass和tearDownClass是必须成对出现, 不能只写setUpClass而不写tearDownClass)

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
  # router的basename和viewset的函数名称用-连接,需要注意的是函数名称如有有下划线_, 需要改成连接线-, 如果detai=True, 需要加上args, 下面的123代表CSVoucher的pk
  url = reverse('csvoucher-list')
  url = reverse('csvoucher-custom-func', args=[123])
  ```

- APIRequestFactory的json数据请求和强制认证

  示例如下:
  ```python
  request= APIRequestFactory.post(url, json.dumps(request_data), content_type='application/json')
  force_authenticate(request, user)
  ```

### 使用已有数据库进行测试

写完测试代码之后, 就可以执行`./manage.py test`命令来进行测试了, 参照文档<https://docs.djangoproject.com/en/2.1/topics/testing/overview/#running-tests>

Django的测试会新创建一个空的测试数据库, 测试完成之后, 测试数据库会自动删除.

实际工作中, 我们可能需要使用已有数据库做测试, 已有数据库已经准备好了数据表结构和初始化数据, 不用重新再做. 或者我们想接管django test自动执行的创建数据库和数据表的操作.那么如何实现测试使用已有数据库呢? 两种方法:

1. 自定义admin command复写测试方法

    自定义command参照文档<https://docs.djangoproject.com/en/2.1/howto/custom-management-commands/>

    自定义测试admin command的示例代码如下:

    在app下新建`./management/commands/testcsvoucher.py`

    ```python
    import unittest
    import sys

    from django.core.management.base import BaseCommand
    from csvoucher.tests.test_views import CSVoucherTestCase


    class Command(BaseCommand):
        """测试csvoucher

        自定义command可以使用测试环境的数据库, 减少相关数据依赖的限制
        """
        help = 'test csvoucher use real database'

        def handle(self, *args, **options):
            cs_voucher_suite = unittest.TestLoader().loadTestsFromTestCase(CSVoucherTestCase)
            cs_voucher_package_suite = unittest.TestLoader().loadTestsFromTestCase(CSVoucherPackageTestCase)
            cs_voucher_result = unittest.TextTestRunner().run(cs_voucher_suite)
            cs_voucher_package_result = unittest.TextTestRunner().run(cs_voucher_package_suite)
            # 如果测试失败, 则exit, 作用见下文中的CI集成
            sys.exit(not cs_voucher_result.wasSuccessful())
            sys.exit(not cs_voucher_package_result.wasSuccessful())
    ```

    这样执行`./manage.py testcsvoucher`就会使用默认settings里的数据库来进行测试, 虽然是使用的已有数据库, 但是新创建的数据也会自动删除. 测试的时候可能用的是测试settings文件, 那么测试命令就是:

    ```sh
    $ ./manage.py testcsvoucher --settings=chronosphere.settings_test
    ```
2. 配置测试数据库名称, 指定名称为已有数据库的名称

    例如我们可以指定测试数据库和当前数据库一致:
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'USER': 'mydatabaseuser',
            'NAME': 'mydatabase',
            'TEST': {
                'NAME': 'mydatabase',
            },
        },
    }
    ```
    测试时加上`keepdb`的参数就能访问`mydatabase`数据库
    ```sh
    $ python manage.py test --keepdb
    ```

上面两种方法高下立判, 哈哈, 本人走的弯路

### mock第三方API接口

有的测试模块依赖于其他模块或接口, 在单元测试中, 理想的测试案例应独立于其他案例, 我们可以采用一些程序要模拟和隔离

例如[Python的mock库](https://docs.python.org/3/library/unittest.mock.html)

被测试的接口代码如下:

```python
from .services import RouterService

class CSVoucherViewSet(viewsets.ReadOnlyModelViewSet,
                       mixins.CreateModelMixin):
    """维权单接口
    """
   @transaction.atomic
    def create(self, request):
        """创建接口
        """
        ...
        RouterService.create_shzf_cs_vouchers(cs_voucher_detail)
        return Response(msg, status=status.HTTP_201_CREATED)
```

上面的代码中, 需要执行`RouterService.create_shzf_cs_vouchers(cs_voucher_detail)`, 这一行语句会同步数据到第三方接口, 我们只需保证这一行语句返回`True`即可, 不用关注调用的细节, 所以我们mock这一行语句

```python
@patch('csvoucher.views.RouterService.create_shzf_cs_vouchers')
def test_create_cs_voucher(self, create_shzf_cs_vouchers_mock):
    """测试创建维权单
    """
    create_shzf_cs_vouchers_mock.return_value = True

    request_data = get_order_json(new_order_sn)
    url = reverse('csvoucher-list')
    request = self.factory.post(url, json.dumps(request_data), content_type='application/json')
    force_authenticate(request, user=self.user)
    create_cs_voucher = CSVoucherViewSet.as_view({'post': 'create'})
    response = create_cs_voucher(request)
    self.assertEqual(response.status_code, 201)
```

如果调用第三方接口的代码是在更深的一层呢, 例如:

```python
class RefundVoucherViewSet(viewsets.ReadOnlyModelViewSet):

    @detail_route(methods=['POST'])
    def close(self, request, pk=None):
        """拒绝退款单
        """
        ....
        RefundService.reject_refund(self.get_object(), operation_source=RefundVoucher.PS, request=request)
        ....
        return Response(data, status=status.HTTP_200_OK)
```

调用第三方API接口的代码是在`RefundService.reject_refund`里面. 如下:

```python
from csvoucher.helpers import close_cs_voucher_in_platform

def reject_refund(cls, refund_voucher, refund_proof=None, operation_source=None, request=None):
    u"""退款被拒绝"""
    ....
    success, msg = close_cs_voucher_in_platform(
        refund_voucher.cs_voucher_detail.service_id,
        **payload
    )
    ...
```

我们需要模拟RefundService.reject_refund.close_cs_voucher_in_platform
测试代码可以这样写:

```python
@patch('csvoucher.views.RouterService.create_shzf_cs_vouchers')
@patch('csvoucher.services.csvoucher_refund.close_cs_voucher_in_platform')
def test_close_refund_voucher(self, mock_close_cs_voucher_in_platform, mock_create_shzf_cs_vouchers):
    """测试拒绝退款单
    """
    mock_create_shzf_cs_vouchers.return_value = True
    mock_close_cs_voucher_in_platform.return_value = True, None
    ....
```

注意patch的路径为`csvoucher.services.csvoucher_refund.close_cs_voucher_in_platform`, 而不能写在csvoucher_refund里导入的路径`csvoucher.helpsers.close_cs_voucher_in_platform`
(还需要注意两个patch参数的顺序)

### 测试覆盖率

写完测试代码, 还需要知道测试代码覆盖整个项目的比率, 太低了达不到测试的效果, 覆盖率详情可以采用[coverage](https://coverage.readthedocs.io/en/v4.5.x/)

```sh
# source为当前路径, 即项目下的所有文件, omit参数忽略相关文件
$ coverage run --source="." --omit="./venv/*","./*/migrations/*" manage.py testcsvoucher --settings=chronosphere.settings_test
# 覆盖率不低于5%
$ coverage report --fail-under=5
# 我们可以用`echo $?`来查看上一条命令的状态, 如果覆盖率低于5, 则状态为2, 大于等于5则为0 , 状态不为0代表异常
```

单元测试仅仅保证微服务某一方的代码是有效的，而不能保证服务之间的交互是有效的。而这恰恰是微服务的核心应用场景之一。

## 集成测试

> 整合测试又称组装测试，即对程序模块采用一次性或增值方式组装起来，对系统的接口进行正确性检验的测试工作

集成测试要保证多个模块组装起来运行通过, 那么就不能像单元测试一样模拟相关的模块和接口了, 在微服务中, 就需要真实调用其他微服务的接口.

传统的集成测试里, 需要把相关的微服务都启动起来, 本项目采用docker, 实践过程中需要注意的几点:

- 多个docker service之间如何通信

    例如我们测试微服务chronosphere的接口时, 还需要启动tether维服务, 如何在两个docker service之间通信呢? 我们可以这样做:
    ```shell
    $ docker network create test-network
    $ docker run -d --network test-network --name tether-service tether:latest
    $ docker run --network test-network chronosphere:latest test
    ```
    两个service同属于test-network下
    我们在chronosphere里面可以这样访问:
    ```python
    import requests
    r = requests.get('http://tether-service/api/api-test/')
    ```

- 数据库

    两个微服务需要连接同一个全新的数据库, chronosphere和tether需要连接postgres初始化的一个数据库

    我们自定义一个可以初始化数据库的数据库镜像, DOCKERFILE内容如下:

    ```dockerfile
    FROM postgres:latest

    LABEL maintainer="yangle@luojilab.com"

    # 初始化用户和数据库
    ENV POSTGRES_USER="******"
    ENV POSTGRES_DB="******"

    # 初始化脚本, 启动此镜像时会执行pg_init.sql脚本
    COPY pg_init.sql /docker-entrypoint-initdb.d/
    ```

    postgres docker image文档参照<https://hub.docker.com/_/postgres>

这样的集成测试有很多缺点:

- 速度慢: 构建数据库, 构建服务, 初始化数据, 等等
- 脆弱: 存在网络依赖等问题, 测试失败不一定是因为代码问题
- 定位困难: 很难确定是接口提供者的错误, 还是接口消费者的错误

## 消费者驱动契约测试CDCT

### CDCT的概念和原理

上面两节我们讲到单元测试和集成测试, 他们各有各的优缺点, 但是单元测试健壮可靠, 速度更快, 并且能够很清楚的告诉我们问题在哪. 我们我们能够改进单元测试里的服务间交互(也就是模拟的那部分), 肯定能改善我们的开发测试体验

> 消费者驱动契约测试（Consumer-Driven Contracts Testing）背后的理念是定义每个服务消费者与提供者之间的契约，然后根据该契约对消费者和提供者进行独立测试，以验证他们是否符合契约约定的事项。

我们用以下示例模型来描述这一微服务测试方法背后的概念。

![dfsa](https://ws3.sinaimg.cn/large/006tKfTcly1g1n7xhcixnj30m008w0t5.jpg)
在上图中，我们可以看到两个微服务通过REST相互通信。第一个服务是消费者（Consumer）的角色，第二个是提供者（Provider）的角色。

![](https://ws1.sinaimg.cn/large/006tKfTcly1g1n7ylsizrj30lg0a4jrq.jpg)
我们通过Mock模拟服务提供者的相关反馈，相关测试是可以通过的

![](https://ws1.sinaimg.cn/large/006tKfTcly1g1n8bq4mm4j30m00aamxo.jpg)
但是，测试时模拟的服务反馈很可能跟不上服务提供者的变化，如果提供者发生了变化, 消费者还是mock的上一个版本, 单元测试能通过, 但是实际环境会发生错误

![](https://ws3.sinaimg.cn/large/006tKfTcly1g1n8dxluu0j30kk04mt91.jpg)

在CDCT中, 服务的消费者创建一个契约，它是服务消费者和提供者之间的交互协议, 这个契约是消费者驱动的，消费者提出对提供者的期望。一旦和提供者就契约达成协议，消费者和提供者都可以获取契约的副本，并使用测试来验证它们的相应实现有没有违反契约。

消费者驱动的契约测试，通常实现方式如下：

1. 选择合适的场景，定义消费者的请求和期望的响应。

2. 使用Mock机制，为消费者提供模拟的提供者以及期望的响应。

3. 记录消费者发送的请求、提供者提供的响应以及关于场景的其它元数据，并将其记录为当前场景的契约。

4. 在提供者这一方, 模拟消费者，用契约来模拟向提供者发送请求。

5. 验证提供者的服务是否和契约一致。

能够完成CDCT任务的框架有Janus\Pact\Pacto\Spring Cloud Contract等，网上资料比较多的是PACT和Spring Cloud Contract。

我们以pact这个CDCT测试框架为例来说明:

![](https://ws2.sinaimg.cn/large/006tKfTcly1g1n8ijiw6qj30u00iodhg.jpg)
消费者通过模拟服务，将请求、响应和相关信息记录下来，成为一个Pact文件。这个文件就是消费者与提供者之间的契约。在这个过程中，服务提供者无需进行任何操作。

![](https://ws1.sinaimg.cn/large/006tKfTcly1g1n8j4l74lj30u00ghdhe.jpg)
接下来，在服务提供者一端，将消费者通过模拟服务生成的Pact文件进行回放，务提供者需要对该契约做出正确的响应。

这就是一次完整的消费者驱动契约测试的过程。

CDCT有几个优点:

1. 同mock一样, 可以在本地独立运行，速度快、可靠
2. 降低接口变化带来的风险
    提供者接口修改时, 仍然需要遵守契约, 这样无论提供者怎么修改接口都能保证消费者得到正确的信息. 除非两方重新订立契约
3. 解耦团队开发
    消费者和提供者订立契约之后, 双方就可以独立去开发和测试了

### CDCT的具体实现

pact的文档地址<https://docs.pact.io/>
pact python的github<https://github.com/pact-foundation/pact-python>

1. 消费者端

```python
import atexit
import unittest
import requests
from pact import Consumer, Provider

# 定义消费者和服务者的名称, 以及契约文件的存储路径
pact = Consumer('Translator').has_pact_with(Provider('Service'), pact_dir='./pacts')

pact.start_service()

atexit.register(pact.stop_service)


class TranslateServiceContract(unittest.TestCase):

    mock_host="http://localhost:1234"

    def _request_helper(self, path):
        return requests.get(self.mock_host + path)

    def test_get_translation_existing(self):
        path = '/translate/1'
        expected_body = {"en": "one", "de": "eins"}
        expected_status = 200

        (pact
         .given('translation for number 1')
         .upon_receiving('a request to get translation for 1')
         .with_request('get', path)
         .will_respond_with(expected_status, body=expected_body))

        pact.setup()
        # do something
        resp = self._request_helper(path)
        # do something
        pact.verify()

        self.assertEqual(resp.status_code, expected_status)
```
`pact.start_service`启动pact模拟服务, `atexit.register(pact.stop_service)`会让一次请求之后自动关闭服务, 默认host是localhost, 端口是1234, 都可以自定义配置

运行测试的时候, 会访问pact服务, 根据设置, 会返回期望的信息, 并会在指定的路径生成契约文件, 契约文件示例如下:
```json
{
  "consumer": {
    "name": "Translator"
  },
  "provider": {
    "name": "Translate Service"
  },
  "interactions": [
    {
      "description": "a request to get translation for 1",
      "providerState": "translation for number 1",
      "request": {
        "method": "get",
        "path": "/translate/1"
      },
      "response": {
        "status": 200,
        "headers": {
        },
        "body": {
          "de": "eins",
          "en": "one"
        }
      }
    }
  "metadata": {
    "pactSpecification": {
      "version": "1.0.0"
    }
  }
}
```

2. 提供者端

提供者端根据契约文件执行验证

```sh
$ pact-verifier --provider-base-url=http://localhost:5000/ --pact-url=pacts/translator-translate_service.json --provider-states-setup-url=http://localhost:5000/_pact/provider_states
```
- provide-base-url

    提供者服务地址(需要提供者启动服务)

- pact-url

    契约文件路径

- provider-states-setup-url

    可选项, 执行契约测试时需要额外执行的代码, 例如准备数据等等, 见下面的例子

```python
# provider-states-setup-url
@app.route('/_pact/provider_states', methods=['GET', 'POST'])
def states():
    data = request.get_json()
    prepare_state(data["states"][0])

    return STATUS['ok']

# 提供者被测试接口
@app.route('/translate/<number>', methods=['GET'])
def translate_number(number):
    try:
        return get_translation(200, number)
    except KeyError:
        return STATUS['not_found']
```

3. 契约分享

在上面的例子中, 契约文件是存储在本地的, 需要两个微服务在同一台开发环境下才可以, 显然不符合实际要求. 一种解决方案是讲契约存储在公共的服务上, pact提供了这样的broker<https://github.com/pact-foundation/pact_broker>

我们采用broker docker来创建一个私有化服务, 参照<https://github.com/DiUS/pact_broker-docker>

具体操作方法参照<https://github.com/DiUS/pact_broker-docker/blob/master/POSTGRESQL.md>

假如我们在本地这样启动broker服务:
```sh
$ docker run --rm --name pactbroker --link pactbroker-db:postgres -e PACT_BROKER_DATABASE_USERNAME=pactbrokeruser -e PACT_BROKER_DATABASE_PASSWORD=****** -e PACT_BROKER_DATABASE_HOST=postgres -e PACT_BROKER_DATABASE_NAME=pactbroker -p 8443:80 dius/pact-broker
```
这样broker的地址就是`http://localhost:8443`, 我们可以在浏览器上访问查看相关信息

> 在192.168.0.71上启动了一个pactbroker服务, 启动命令如下:
> ```sh
> $ docker run --rm --name pactbroker -e PACT_BROKER_DATABASE_USERNAME=****** -e PACT_BROKER_DATABASE_PASSWORD=****** -e PACT_BROKER_DATABASE_HOST=192.168.0.71 -e PACT_BROKER_DATABASE_NAME=pactbroker -d -p 8443:80 dius/pact-broker
> ```

</br>

消费者端这样生成和存储契约文件

```python
import atexit
import unittest
import requests
from pact import Consumer, Provider

# 定义消费者和服务者的名称, 以及契约文件的存储路径
pact = Consumer('Translator').has_pact_with(Provider('Service'), pact_dir='./pacts')

pact.start_service()

atexit.register(pact.stop_service)


class TranslateServiceContract(unittest.TestCase):

    mock_host="http://localhost:1234"

    def _request_helper(self, path):
        return requests.get(self.mock_host + path)

    def test_get_translation_existing(self):
        path = '/translate/1'
        expected_body = {"en": "one", "de": "eins"}
        expected_status = 200

        (pact
         .given('translation for number 1')
         .upon_receiving('a request to get translation for 1')
         .with_request('get', path)
         .will_respond_with(expected_status, body=expected_body))

        pact.setup()
        resp = self._request_helper(path)
        # 将本地pact契约文件put到broker服务
        import requests
        # 地址格式是http://localhost:8443/pacts/provider/{provider name}}/consumer/{consumer name}/version/{version}
        # provider name和consumer name必需与pact的配置一致
        broker_url = "http://localhost:8443/pacts/provider/Translator/consumer/Service/version/0.1"
        headers = {'Content-Type': 'application/json'}
        # 方法为PUT
        requests.put(broker_url, data=open('./pact/pact_verify_test.json', 'rb'), headers=headers)
        pact.verify()

        self.assertEqual(resp.status_code, expected_status)
```
> pact的python包不支持配置broker地址自动上传, 这里是先存储到本地, 然后手动上传

提供者端这样验证:
```sh
$ pact-verifier --provider-base-url=http://localhost:5000/ --pact-url=http://localhost:8443/pacts/provider/Translator/consumer/Service/latest --provider-states-setup-url=http://localhost:5000/_pact/provider_states
```

## 持续集成

### Gitlab持续集成配置文件

Gitlab持续集成在这里不在赘述, 参照文档: <https://docs.gitlab.com/ee/ci/README.html>

项目根部录下`gitlab-ci.yml`内容如下:

```yaml
image: docker:stable

stages:
  - build
  - test

before_script:
  - docker login

test:
  image: docker:dind
  stage: test
  script:
    - docker network create test-network || true
    - docker stop postgres-test || true && docker stop tether-test || true && docker stop chronosphere-test || true
    - docker run -d --rm --network test-network --name postgres-test registry.cn-beijing.aliyuncs.com/myproject/phasmatodea:45a86dbc64c4a09f9da058af04e667da9a5b47d2
    - docker run -d --rm --network test-network --name tether-test  -p 8000:8000 registry.cn-beijing.aliyuncs.com/myproject/tether:6eb9b6cd713ddf5dfc5ac68f1737ee2de0d660f6 mock
    - docker run --rm --env-file=.test-env --network test-network --name chronosphere-test $CONTAINER_IMAGE:$CI_BUILD_REF test
  tags:
    - myproject
  only:
    - test-yangle


build:
  image: docker:dind
  stage: build
  script:
    - docker pull $CONTAINER_IMAGE:$CI_COMMIT_REF_NAME || true
    - docker build --cache-from $CONTAINER_IMAGE:$CI_COMMIT_REF_NAME -t $CONTAINER_IMAGE:$CI_BUILD_REF -t $CONTAINER_IMAGE:$CI_COMMIT_REF_NAME  --build-arg GIT_COMMIT=$CI_COMMIT_SHA .
    - docker push $CONTAINER_IMAGE:$CI_BUILD_REF
    - docker push $CONTAINER_IMAGE:$CI_COMMIT_REF_NAME
```

代码push之后会依次执行build和test, build构建镜像, 并推送, 第二步test会依赖第一步的镜像, 在此镜像下执行test, test会执行5个脚本, 第1步是创建docker network, 第2步是停止若干服务, 第3步是启动postgres数据, 第4步是启动测试依赖的tether服务, 第5步是执行测试, 有几个问题:

- 为什么第1步和第2步执行的时候都会加上`|| true`?

    因为如果执行错误的话(例如network已存在, 没有运行中的service), sys会exit, 从而不会执行接下来的脚本

- 为什么`docker run`的时候要加上`--rm`

    因为加上这个参数之后, 停止服务, 容器container就会自动删除, 下次运行时就不会冲突了

### Docker自定义命令EntryPoint

docker的DockerFile的内容如下:

```
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
    python3 manage.py migrate --settings=chronosphere.settings_test
    python3 manage.py loaddata test_permission test_group test_user test_platform test_country test_company test_userprofile test_auth --settings=chronosphere.settings_test
    coverage run --source="." --omit="./venv/*","./*/migrations/*","*__init__*","./top/api/*","*/management/*" manage.py test --settings=chronosphere.settings_test --keepdb
    ret="$?"
    if [ "$ret" -ne 0 ]; then
        exit "$ret"
    fi
    coverage report --fail-under=5
    ret="$?"
    if [ "$ret" -ne 0 ]; then
        exit "$ret"
    fi
fi
```

需要注意的是在上面的代码中, 加入了两个这样的代码, 判断上一行命令的状态, 如果不等于0, 则exit:

```sh
ret="$?"
if [ "$ret" -ne 0 ]; then
    exit "$ret"
fi
```
加这行代码的目的是为了让执行测试和检查覆盖率时如果报错, 则exit, 从而CI不成功, 不加的话失败CI也会成功, 这样CI就失去意义了.
如何让自定义的django test失败的话status不是0呢? 第一节已经做了说明
备注: `coverage report --fail-under=5`这个命令如果覆盖率小于5的话status是2, 会自动exit, 但是实际上没有exit, 不知道为什么, 所以手动加上了判断代码.


## 参考资料

<https://techbeacon.com/app-dev-testing/shift-right-test-microservices-wild-tame-devops>  
<http://p.primeton.com/articles/5bd90b254be8e6087c003248>  
<https://github.com/nikoly/pact-contract-test>
