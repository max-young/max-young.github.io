---
layout:     post
title:      "Python flask.Request模块"
subtitle:   ""
date:       2017-04-11 14:45:00
author:     "alvy"
header-img: "img/post-bg-nextgen-web-pwa.jpg"
header-mask: 0.3
catalog:    true
tags:
    - Python
    - Flask
---

- Flask 怎样获取当前页面的相对路径

  参考资料：

  <http://flask.pocoo.org/docs/0.10/api/#incoming-request-data>

  Provides different ways to look at the current URL. Imagine your application is listening on the following URL:

  ```
  http://www.example.com/myapplication

  ```

  And a user requests the following URL:

  ```
  http://www.example.com/myapplication/page.html?x=y

  ```

  In this case the values of the above mentioned attributes would be the following:

  | path        | `/page.html`                             |
  | ----------- | ---------------------------------------- |
  | script_root | `/myapplication`                         |
  | base_url    | `http://www.example.com/myapplication/page.html` |
  | url         | `http://www.example.com/myapplication/page.html?x=y` |
  | url_root    | `http://www.example.com/myapplication/`  |

  ​