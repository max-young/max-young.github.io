---
layout:     post
title:      "C++编译compile与调试debug"
subtitle:   "mac环境下"
date:       2021-09-07
author:     max
categories: C++
tags:  
  - C++
---

<!-- TOC -->

- [编译compile](#编译compile)
- [调试debug](#调试debug)

<!-- /TOC -->

<a id="markdown-编译compile" name="编译compile"></a>
### 编译compile

c++文件需要编译才能执行  
编译器有g++, clang++, 分别是gcc和llvm project支持c++的编译器  
mac下推荐使用clang++, Linux下使用g++, 可以自行搜索g++和clang++的区别  

我们对一个C++文件做编译的命令是:  
```shell
$ clang++ main.cpp -o main
```
`-o`是指输出文件  
我们可以用`main clang++`来查看clang++有哪些参数  
如果要编译多个文件, 就需要这样:  
```shell
$ clang++ main.cpp file1.cpp -o main
```
或者编译当前目录下的所有文件:
```shell
$ clang++ ./*.cpp -o main
```

下面列举一些我使用过的参数:

- -o \<fail\>  
  `-o main`
  后面接输出文件的文件名

- -I\<directory\>  
  `-I/usr/local/opt/opencv/include/opencv4`
  和-o不同, 这个直接在-I后面接一个路径  
  c++文件里有include别的文件, 有的文件不在默认的includePath里, 需要增加这个参数
  
- -std=\<standard\>  
  `-std=c++11`  
  有的代码是符合C++11标准的, 需要指定, 才不会报错

- -L\<directory\>  
  `-L/usr/local/opt/opencv/lib`  
  指定用到的库的路径

- -l\<lib\>  
  `-lopencv_photo`  
  指定用到的库

> 注: 这个编译命令: clang++ -g *.cpp -o main -std=c++17 \`pkg-config --cflags --libs opencv4\`加上了命令`pkg-config --cflags --libs opencv4`  
> 这个命令就生成了opencv的-L和-l参数`-I/usr/local/opt/opencv/include/opencv4 -L/usr/local/opt/opencv/lib -lopencv_gapi ...`, 就不用手动写了

- -Wall
  输出warning信息, 比如代码里有一个未使用的变量, 编译时就会提示, 但是不影响编译结果

- -g
  编译时加上这个命令生成的可执行文件支持debug, 否则不支持

### 调试debug

和编译一样, gcc的调试工具是gdb, LLVM的调试工具是lldb, 使用方法差不多  
在mac下推荐使用lldb, 用法就是`lldb <file>`  
如果这个可执行文件需要参数才能执行, 那么这样运行: `lldb main -- b 20 out.png`, `--`后面接了三个参数  
下面是进入debug模式之后常用的命令:  
- run: 运行
- b <num>: 在第几行加上断点
- p <var>: 打印某个变量
- n: 下一步
- q: 退出

