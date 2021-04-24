---
layout:     post
title:      "Python MySQLdb TypeError: not all arguments converted during string formatting"
subtitle:   ""
date:       2017-03-25 17:48:00
author:     "alvy"
header-img: "img/post-bg-woody-allen1.jpg"
header-mask: 0.3
catalog:    true
tags:
    - Python
    - MySQL
---

客户部署的python flask web应用出现上面的错误，调试发现：

```python
sql = "select * from Users  where id = %s"
cursor = db_conn.execute(sql, value)
```

执行上面的语句时，报此错误，google一下很多都说value这个参数应该是一个list或者tuple，改成

```python
cursor = db_conn.execute(sql, [value])
```

的确是能正常运行了，但是为什么此语句为什么以前没有报错呢，我初步猜测可能是python包的版本问题，不同版本不一样，在这里我的想法得到了印证：

[https://discuss.erpnext.com/t/typeerror-not-all-arguments-converted-during-string-formatting/1575/2](https://discuss.erpnext.com/t/typeerror-not-all-arguments-converted-during-string-formatting/1575/2)

我们查看自己的服务器的Mysql-Python版本：

```shell
[root@app3 ~]# pip show Mysql-Python
Name: MySQL-python
Version: 1.2.3
Summary: Python interface to MySQL
Home-page: http://sourceforge.net/projects/mysql-python
Author: Andy Dustman
Author-email: adustman@users.sourceforge.net
License: GPL
Location: /usr/lib64/python2.7/site-packages
Requires:
```

发现时1.2.3，而客户的版本是1.2.5

于是我们需要降低版本：

```
[exam@iZ9483m8uxyZ ~]$ sudo pip install --upgrade MySQL-python==1.2.3
[sudo] password for exam:
Collecting Mysql-Python
  Downloading http://mirrors.aliyun.com/pypi/packages/a5/e9/51b544da85a36a68debe7a7091f068d802fc515a3a202652828c73453cad/MySQL-python-1.2.5.zip (108kB)
    100% |████████████████████████████████| 112kB 1.0MB/s
    Complete output from command python setup.py egg_info:
    sh: mysql_config: command not found
    Traceback (most recent call last):
      File "<string>", line 1, in <module>
      File "/tmp/pip-build-Tgxxcw/Mysql-Python/setup.py", line 17, in <module>
        metadata, options = get_config()
      File "setup_posix.py", line 43, in get_config
        libs = mysql_config("libs_r")
      File "setup_posix.py", line 25, in mysql_config
        raise EnvironmentError("%s not found" % (mysql_config.path,))
    EnvironmentError: mysql_config not found

    ----------------------------------------
Command "python setup.py egg_info" failed with error code 1 in /tmp/pip-build-Tgxxcw/Mysql-Python/
```

安装报错，google之，[http://stackoverflow.com/questions/5178292/pip-install-mysql-python-fails-with-environmenterror-mysql-config-not-found](http://stackoverflow.com/questions/5178292/pip-install-mysql-python-fails-with-environmenterror-mysql-config-not-found)

第二个答案适用我们的情况：

```
shell> yum install -y mysql-devel python-devel python-setuptools
```

安装上面的包之后再安装Mysql-Python

搞定收工