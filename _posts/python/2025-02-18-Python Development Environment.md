---
layout:     post
title:      "Python Development Environment"
subtitle:   ""
date:       2025-02-28
categories: Python
tags:
    - Python
---

<!-- TOC -->

- [Python版本问题](#python版本问题)
- [VSCode](#vscode)
  - [import could not be resolved](#import-could-not-be-resolved)
  - [code style检查](#code-style检查)
- [上下键乱码](#上下键乱码)

<!-- /TOC -->

<a id="markdown-python版本问题" name="python版本问题"></a>
#### Python版本问题

pyenv 安装参照: https://github.com/pyenv/pyenv-installer

<a id="markdown-vscode" name="vscode"></a>
#### VSCode

<a id="markdown-import-could-not-be-resolved" name="import-could-not-be-resolved"></a>
##### import could not be resolved

import可能会显示could not be resolved pylance之类的内容, 无法跳转, 这是因为python的路径没有设置正确.  
`ctrl + shift + p`搜索`Python: Select Interpreter`选择正确的python路径即可.  
例如我用的pyenv, 所以我选择pyenv下的python路径.

<a id="markdown-code-style检查" name="code-style检查"></a>
##### code style检查

参照: <https://code.visualstudio.com/docs/python/linting>

open the Command Palette (Ctrl+Shift+P) and select the Python: Select Linter.  
例如我们选择pylint, 如果没有安装就会自动安装. 之后就会提示代码的格式等问题了.

#### 上下键乱码

`pip install readline`

if install error in Ubuntu, then install gnureadline:

`pip install gnureadline`