---
layout:     post
title:      "用swagger给Go Web项目写API文档"
subtitle:   ""
date:       2019-06-17
categories: Backend
tags:
    - Go
---

[swagger](#swagger)  
[go-swagger安装](#go-swagger安装)  
[文档编写](#文档编写)  
[生成文档](#生成文档)  
[部署](#部署)  
[参考资料](#参考资料)  

### swagger

简而言之, swagger就是让你更好更方便的写API文档的框架, 支持多种语言

编写格式和含义, 可以参照这篇文章:

### go swagger安装

GITHUB地址: <https://github.com/go-swagger/go-swagger>

安装方法参照这里: <https://goswagger.io/install.html>

### 文档编写

以一个get返回list数据的接口做一个简单的示例:

- 在`main.go`里有一个`plutus-package`接口

  ```go
  r := gin.Default()
  authorized := r.Group("/api/", auth.SessionAuth())
  authorized.GET("/plutus-package/", orderpackage.PackageView)
  ```

  这里不需要写注释

- 这个接口对应的view函数是:

  ```go
  // PackageView is a view function return Package data                    1
  func PackageView(c *gin.Context) {
  	// swagger:route GET /plutus-package/ package package_list         2
  	//
  	// Package Model list 接口                                         3
  	// 当查询参数是package_id_list或者count和update_time一起查询时     4
  	// 直接返回数据数组, 不再返回count, next_url和previous_url         5
  	//
  	//     Schemes: http, https                                        6
  	//
  	//     Responses:                                                  7
  	//       200: package_list_response                                8
    ......
    response := PackageResponse{}
    c.JSON(http.StatusBadRequest, response)
  }
  ```

  **1**: 这行注释和swagger没关系, 是go文档规范要求向外暴露的函数需要写注释

  **2**: `swagger:route`固定格式, `GET是`请求方法, `/plutus-package/`是请求地址, `package`是tag, 最后展示的文档界面以tag分类, `package_list`代表这个view的标识, 在其他地方比如查询参数里会用到

  **3-5**: 是这个view的描述

  **6**: schema

  **7-8**: 返回数据格式, `package_list_response`是返回数据结构的标识, 之后会在response数据结构里用到

- 对应的查询参数是:

  ```go
  // package view query args                                 1
  // swagger:parameters package_list                         2
  type packageQuery struct {
  	Limit  uint `form:"limit"`
  	Offset uint `form:"offset"`
  	// 示例: [1, 2, 3]                                   3
  	PackageIDList string `form:"package_id_list"`
  	Count         uint   `form:"count"`
  	CompanyID     uint   `form:"company_id"`
  	// 示例: 2019-05-05 00:00:00                         4
  	Updated time.Time `form:"update_time" time_format:"2006-01-02 00:00:00" time_utc:"8"`
  }
  ```

  **1**: go语言注释, 与swagger无关

  **2**: `swagger:parameters`固定格式, `package_list`是view router注释里的标识, 上面已提到

  **3, 4**: 字段的description, 在文档页面会有显示

- 返回的数据格式是:

  ```go
  // PackagesResponse PackagesView response data struct             1
  type PackagesResponse struct {
  	Count    int               `json:"count"`
  	Next     string            `json:"next"`
  	Previous string            `json:"previous"`
  	Results  []EinsteinPackage `json:"results"`
  }
  ```

  **1**: go语言注释, 与swagger无关

  > 这里不写swagger注释, 生成的页面不对, 返回数据文档按下面的步骤写

- 返回数据文档

  我们可以在包里新建一个`doc.go`的文件, 在这个文件里写文档:

  ```go
  // Package orderpackage 包括package相关的接口                      1
  package orderpackage
  
  // package list response                                           2
  // swagger:response package_list_response                          3
  type packageResponseWrapper struct {                               
  	// in: body                                                  4
  	Body PackagesResponse
  }
  ```

  **1**: 这里可以写上整个包的注释, 与swagger无关

  **2**: go注释, 与swagger无关

  **3**: `swagger:response`固定格式, `package_list_response`是view router里定义的response的标识, 上文已提到

  **4**: `in: body`, response文档的参数

上面就是一个简单的接口文档示例, swagger文档还有很多别的参数和选项, 可以参照官方文档尝试去修改和添加

写了那么多, 怎么看写的对不对呢, 生成的文档界面是什么样的呢? 我们看下一节

### 生成文档

上一节我们只是参照go swagger的文档和格式写了一个接口的文档, 到底我们写的对不对呢? 我们用此命令生成一个json或者yaml文件:

```sh
$ swagger generate spec -o ./swagger.yml
```

这里我指定的是yaml文件(后缀可以使yam也可以是yaml), yaml文件和json文件格式不太一样, 看个人习惯, 生成之后, 我们可以在编辑器里看效果:

这个是在线的编辑器: <https://editor.swagger.io/>, 也可以本地启动编辑器, 参照文档, 不赘述

在编辑器里点击`file-->import file`, 在编辑器右侧即可看到效果:

<img src="/images/posts/2019/go-swagger.png">

### 部署

// TODO

### 参考资料

<https://juejin.im/post/5b05138cf265da0ba7701a37>
