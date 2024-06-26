---
layout: post
title: "Python version manage"
date: 2024-04-19
categories: Python
tags:
  - Python
---

- [pyenv](#pyenv)
  - [installation](#installation)
  - [problems](#problems)
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
   or use this command, replace `2.7.6` with your version:

   ```shell
   $ export v=3.8.10; wget https://registry.npmmirror.com/-/binary/python/$v/Python-$v.tar.xz -P ~/.pyenv/cache/; ~/.pyenv/bin/pyenv install $v
   ```

2. install error

   your build environment need some packages, see: <https://github.com/pyenv/pyenv/wiki#suggested-build-environment>  
    in ubuntu, execute this command:

   ```shell
   sudo apt update; sudo apt install build-essential libssl-dev zlib1g-dev \
   libbz2-dev libreadline-dev libsqlite3-dev curl \
   libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
   ```

### python-is-python3

In Ubuntu 20, the default Python version is 3.8.10, not supporting Python2, entering Python Shell is to enter `python3`, `Python` is an invalid command. how to alias python to python3?  
we can use `alias python=python3` to alias python to python3, add this line to `~/.bashrc` to make it permanent.  
another solution is install `python-is-python3`:

```bash
 sudo apt install python-is-python3
```

<https://askubuntu.com/questions/320996/how-to-make-python-program-command-execute-python-3>
