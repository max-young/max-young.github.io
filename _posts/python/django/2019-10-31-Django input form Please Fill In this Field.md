---
layout:     post
title:      "Django input form Please Fill In this Field"
subtitle:   ""
date:       2019-10-31
categories: Python
tags:
    - Python
    - Django
    - HTML
---

用Django form生成的input form里, 我们不输入内容直接回车的话, 会出现popup, 内容是:Please Fill In this Field

不能定制, 影响业务逻辑, 比如后台有validate, 然后再返回给前端错误信息, 这个机制就不起作用了.

那么我们怎么能去掉这个popup呢? 只需在form里加入`novalidate`即可

```html
<form method="POST" novalidate>
	{{ form.text }}
</form>
```
