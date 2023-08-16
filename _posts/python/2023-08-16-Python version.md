---
layout: post
title: "Python version manage"
date: 2023-08-16
categories: Python
tags:
  - Python
---

- [pyenv](#pyenv)
- [python-is-python3](#python-is-python3)

### pyenv

pyenv's installation refer to pyenv homepage.  
if your network is not good, you can use gitee, clone reporitory to `~/.pyenv` and edit your `~/.bashrc`:

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

#### installation

如果网络不好, 可以用克隆[gitee 仓库](https://gitee.com/mirrors/pyenv)到`~/.pyenv`目录:

```shell
git clone https://gitee.com/mirrors/pyenv.git ~/.pyenv
```

然后往`~/.bashrc`添加内容, 可以用命令行添加:

```bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
```

#### problems

1. install very slow

   `pyenv install <version>` may very slow and fail eventually, we can download the `.tar` file manually and put it in the `~/.pyenv/cache` folder, then run `pyenv install <version>` again.  
   donwload link: <https://www.python.org/ftp/python/>  
   if `~/.pyenv/cache` directory not exist, create it manually.

2. ModuleNotFoundError: No module named '\_lzma'  
   `sudo apt install liblzma-dev`
3. ModuleNotFoundError: No module named '\_sqlite3'  
   `sudo apt install libsqlite3-dev`
4. ModuleNotFoundError: No module named '\_ctypes'  
   `sudo apt-get install libffi-dev`
5. ModuleNotFoundError: No module named '\_bz2'  
   `sudo apt-get install libbz2-dev`
6. ModuleNotFoundError: No module named '\_curses'
   `sudo apt-get install libncurses5 libncurses5-dev libncursesw5`
7. ModuleNotFoundError: No module named 'readline'  
   `sudo apt-get install libreadline-dev`

### python-is-python3

In Ubuntu 20, the default Python version is 3.8.10, not supporting Python2, entering Python Shell is to enter `python3`, `Python` is an invalid command. how to alias python to python3?  
we can use `alias python=python3` to alias python to python3, add this line to `~/.bashrc` to make it permanent.  
another solution is install `python-is-python3`:

```bash
 sudo apt install python-is-python3
```

<https://askubuntu.com/questions/320996/how-to-make-python-program-command-execute-python-3>
