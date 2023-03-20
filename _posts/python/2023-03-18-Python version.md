---
layout: post
title: "Python version manage"
date: 2023-03-18
categories: Python
tags:
  - Python
---

[pyenv](https://github.com/pyenv/pyenv)可在一台机器上安装不同版本的 python.  
安后可以在当前目录或者全局设置不同的 python 版本:

```bash
# 列出所有python版本
pvenv versions
# 全局切换到version版本
pyenv global <version>
# 当前路径切换到version版本
pyenv local <version>
# list all python versions
Pyenv install -l
```
