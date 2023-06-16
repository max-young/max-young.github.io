---
layout: post
title: "Python version manage"
date: 2023-06-16
categories: Python
tags:
  - Python
---

- [pyenv](#pyenv)
- [python-is-python3](#python-is-python3)

### pyenv

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

### python-is-python3

In Ubuntu 20, the default Python version is 3.8.10, not supporting Python2, entering Python Shell is to enter `python3`, `Python` is an invalid command. how to alias python to python3?  
we can use `alias python=python3` to alias python to python3, add this line to `~/.bashrc` to make it permanent.  
another solution is install `python-is-python3`:

```bash
 sudo apt install python-is-python3
```

<https://askubuntu.com/questions/320996/how-to-make-python-program-command-execute-python-3>
