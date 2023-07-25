---
layout: post
title: "Python version manage"
date: 2023-07-25
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

#### problems

1. install very slow

    `pyenv install <version>` may very slow and fail eventually, we can download the `.tar` file manually and put it in the `~/.pyenv/cache` folder, then run `pyenv install <version>` again.  
    donwload link: <https://www.python.org/ftp/python/>  
    if `~/.pyenv/cache` directory not exist, create it manually.
2. ModuleNotFoundError: No module named '_lzma'  
   `sudo apt install liblzma-dev`
3. ModuleNotFoundError: No module named '_sqlite3'  
  `sudo apt install libsqlite3-dev`

### python-is-python3

In Ubuntu 20, the default Python version is 3.8.10, not supporting Python2, entering Python Shell is to enter `python3`, `Python` is an invalid command. how to alias python to python3?  
we can use `alias python=python3` to alias python to python3, add this line to `~/.bashrc` to make it permanent.  
another solution is install `python-is-python3`:

```bash
 sudo apt install python-is-python3
```

<https://askubuntu.com/questions/320996/how-to-make-python-program-command-execute-python-3>
