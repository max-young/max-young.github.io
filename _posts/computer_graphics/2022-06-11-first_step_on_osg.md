---
layout:     post
title:      "First Step on OSG"
subtitle:   ""
date:       2022-06-11
categories: Computer Graphics
tags:
    - OSG
---

OSG是一个图形引擎, 全称OpenSceneGraph, 主要用在虚拟仿真领域, 不太适用于游戏开发.  
OSG的环境搭建网上资料纷繁复杂, 但是没有适合我的. 下面是我的搭建过程:

#### 环境

MacOS Montery 12.1  
VS Code

#### 安装OSG

采用`brew`安装.
```shell
$ brew install open-scene-graph
```
这样安装是没有osg相关的示例数据的, 例如OSG经典的cow的模型.  
可以去github下载:
```shell
$ git clone git@github.com:openscenegraph/OpenSceneGraph-Data.git
```
下载完之后需要配置一下环境变量, 修改`~/.zshrc`文件, 增加一行, 路径按照自己的实际情况修改:
```txt
export OSG_FILE_PATH=/Users/<username>/Documents/OpenSceneGraph-Data
```


#### VS Code Demo

VS Code新建一个project, 在project里面新建一个文件, 文件名是`main.cpp`, 内容是:
```cpp
// 加这一行是为了不显示编译时出现的OpenGL接口过期的警告
#define GL_SILENCE_DEPRECATION  

#include <osgDB/ReadFile>
#include <osgViewer/Viewer>

int main()
{
  osgViewer::Viewer viewer;
  // cow.osg这个文件在上面配置的OSG示例数据的环境变量路径下, 所以不要写其完整路径
  viewer.setSceneData(osgDB::readNodeFile("cow.osg"));
  return viewer.run();
}
```
再创建一个`CmakeLists.txt`文件, 内容是:
```cmake
cmake_minimum_required(VERSION 3.10)
project(main)

set(CMAKE_CXX_STANDARD 11)

set(CMAKE_BUILD_TYPE Debug)

# 这个路径按自己的实际情况
include_directories(/usr/local/Cellar/open-scene-graph/3.6.5_1/include)

find_package(OpenSceneGraph REQUIRED COMPONENTS osgDB osgGA osgUtil osgViewer)

add_executable(main main.cpp)

target_link_libraries(${PROJECT_NAME} ${OPENSCENEGRAPH_LIBRARIES})
```

#### 编译和运行

cmake编译运行
```shell
$ mkdir build
$ cd build
$ cmake ..
// main.cpp里加了GL_SILENCE_DEPRECATION定义, 所以make编译时不会有warning, 可以去掉那一行看看warning信息
$ make
$ ./main
```
就会出现:
<img src="/images/posts/cow.png">  
也可以用命令行编译运行:
```shell
$ g++ main.cpp -I /usr/local/include/ -o main -L /usr/local/lib/ -lOpenThreads -losgDB -losgText -losgUtil -losg -losgViewer -losgGA -losgManipulator -losgVolume -losgSim
$ ./main
```

我看很多文章里都是OSG+QT的GUI环境配置, 我对QT不熟, 对GUI操作也不太感冒, 之后可能换到Windows环境下再试试.