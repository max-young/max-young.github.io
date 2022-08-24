---
layout: post
title: "shell script"
date: 2022-08-24
categories: Linux
tags:
  - shell
---

#### shift

删除参数

一个`run.sh`脚本:

```bash
#!/bin/bash
while [ $# != 0 ];do
echo "第一个参数为：$1,参数个数为：$#"
shift
done
```

执行`run.sh a b c d e f`
结果是

```shell
第一个参数为：a,参数个数为：6
第一个参数为：b,参数个数为：5
第一个参数为：c,参数个数为：4
第一个参数为：d,参数个数为：3
第一个参数为：e,参数个数为：2
第一个参数为：f,参数个数为：1
```

从上可知`shift(shift 1)`命令每执行一次, 变量的个数`$#`减一(之前的`$1`变量被销毁, 之后的`$2`就变成了`$1`), 而变量值提前一位.
