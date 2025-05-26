---
layout:     post
title:      "Go Module Management"
subtitle:   ""
date:       2025-05-26
categories: Backend
tags:
    - Go
---

- [参考资料](#参考资料)
- [使用方法](#使用方法)
- [原理](#原理)
- [Issues](#issues)
	- [Network](#network)

go的包管理有很多工具, 比如govendor等等, govendor在自己使用过程中有一些问题, 例如只能在$GOPATH下进行, 有时候找不到包
go module是go1.11版本退出的包管理工具, 有官方的加持, 我们来看看module使用情况怎么样

### 参考资料

<https://roberto.selbach.ca/intro-to-go-modules/>
<https://github.com/golang/go/wiki/Modules>

### 使用方法

go module不像govendor一样局限在$PATH下, 事实上在$GOPATH下执行`go mod init`会报错: `go: modules disabled inside GOPATH/src by GO111MODULE=auto; see 'go help modules'`

我是在$GOPATH下已有一个开发中的项目, 采用的是govendor管理, 我在$PATH之外的路径下clone这个项目, 在这个项目基础上使用go module

```shell
$ git clone git@gitlab.luojilab.com/rock/chaos
$ cd chaos
$ go mod init gitlab.luojilab.com/rock/chaos
go: creating new go.mod: module gitlab.luojilab.com/rock/chaos
go: copying requirements from vendor/vendor.json
```
执行上面的命令之后, 在仓库下多出来一个文件: `go.mod`, 内容如下:
```
module gitlab.luojilab.com/rock/chaos

go 1.12

require (
	github.com/DataDog/zstd v0.0.0-20160706220725-2bf71ec48360
    ...
)
```
我们把之前的vendor路径全部删除, 项目还能运行起来吗?
```shell
$ go run main.go
go: finding github.com/DataDog/zstd v0.0.0-20160706220725-2bf71ec48360
...
build command-line-arguments: cannot load github.com/ugorji/go/codec: ambiguous import: found github.com/ugorji/go/codec in multiple modules:
	github.com/ugorji/go v1.1.4 (/Users/yangle/go/pkg/mod/github.com/ugorji/go@v1.1.4/codec)
	github.com/ugorji/go/codec v0.0.0-20181204163529-d75b2dcb6bc8 (/Users/yangle/go/pkg/mod/github.com/ugorji/go/codec@v0.0.0-20181204163529-d75b2dcb6bc8)
```
运行报错, 我们在代码里面没看到这个包的引用, 采用go module的清理命令试试:
```shell
$ go mod tidy
```
依然还是这个错, google之, 是gin的版本问题: <https://github.com/gin-gonic/gin/issues/1673>
```shell
$ go get github.com/ugorji/go/codec@none
```
这样执行之后`go run main.go`就可以了

### 原理

// TODO

### Issues

#### Network

A proxy could be set to solve timeout issues in China:
```shell
go env -w GOPROXY=https://goproxy.cn,direct
```