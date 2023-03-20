---
layout: post
title: "React Development Environment Construction "
date: 2023-03-20
categories: Frontend
tags:
  - React
---

- [准备](#准备)
  - [node.js 版本](#nodejs版本)
  - [npm vs yarn 包管理](#npm-vs-yarn包管理)
  - [语法](#语法)
- [搭建环境](#搭建环境)
  - [开发](#开发)
    - [环境变量](#环境变量)
    - [React Router](#react-router)
    - [Code Split](#code-split)
  - [问题](#问题)

### 准备

#### node.js 版本

可以用[nvm](https://github.com/nvm-sh/nvm#system-version-of-node)管理, 和 pyenv 类似, 可安装多个 node.js 版本, 然后切换

例如系统已安装 node 14, 但是有的项目需要 node 10, 那么可以用 nvm 安装:

```bash
nvm install 10
```

然后我们可以用`npm ls`查看有哪些版本:

```bash
$ nvm ls
->     v10.24.1
         system
default -> 10 (-> v10.24.1)
iojs -> N/A (default)
unstable -> N/A (default)
node -> stable (-> v10.24.1) (default)
stable -> 10.24 (-> v10.24.1) (default)
lts/* -> lts/gallium (-> N/A)
lts/argon -> v4.9.1 (-> N/A)
lts/boron -> v6.17.1 (-> N/A)
lts/carbon -> v8.17.0 (-> N/A)
lts/dubnium -> v10.24.1
lts/erbium -> v12.22.12 (-> N/A)
lts/fermium -> v14.20.0 (-> N/A)
lts/gallium -> v16.17.0 (-> N/A)
```

可以看到有两个版本: 10.24.1 和 system, system 指的就是在系统安装的版本, 那么 system 的版本是多少呢?

```bash
$ nvm run system --version
Running node system (npm v6.14.12)
v14.16.1
```

如果要切换版本, 那么就用 use 命令:

```bash
$ nvm use system
Now using system version of node: v14.16.1 (npm v6.14.12)
$ node --versio
v14.16.1
```

如果要切回到 10 版本呢?

```bash
# 不用输入完整的10版本, 因为在ls里显示default -> 10 (-> v10.24.1)
$ nvm use 10
Now using node v10.24.1 (npm v6.14.12)
```

#### npm vs yarn 包管理

[npm 和 yarn 的区别，我们该如何选择？](https://zhuanlan.zhihu.com/p/27449990)

都是包管理工具, 一样的用法

> 在 npm5.0 之前，yarn 的优势特别明显。但是在 npm 之后，通过以上一系列对比，我们可以看到 npm5 在速度和使用上确实有了很大提升，值得尝试，不过还没有超过 yarn。

> 综上我个人的建议是如果你已经在个人项目上使用 yarn，并且没有遇到更多问题，目前完全可以继续使用。但如果有兼容 npm 的场景，或者身处在使用 npm，cnpm，tnpm 的团队，以及还没有切到 yarn 的项目，那现在就可以试一试 npm5 了。

#### 语法

<https://babeljs.io/docs/en/learn>  
<https://www.babeljs.cn/docs/learn>  
<https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array>

### 搭建环境

编辑器推荐 vscode

创建步骤参照: <https://create-react-app.bootcss.com/docs/getting-started>

```bash
npx create-react-app my-app
cd my-app
npm start
```

#### 开发

按照官方文档<https://zh-hans.reactjs.org/tutorial/tutorial.html>的示例项目过一遍就大概熟悉了 React

##### 环境变量

参照<https://create-react-app.bootcss.com/docs/adding-custom-environment-variables>  
在项目目录下创建`.env`, `.env.development`, `.env.production`等文件, 分别对应不同的环境, 具体参照文档.  
环境变量必须以`REACT_APP_`开头, 在代码里使用`process.env.REACT_APP_XXX`获取值.  
如果是 dict string, 那么可以用`JSON.parse`来转换为 dict.

##### React Router

<https://reactrouter.com/en/main/start/tutorial>

##### Code Split

这个非常重要, 不然会把所以代码打包在一个文件里, 然后文件巨大, 加载会很慢.  
参照: <https://create-react-app.bootcss.com/docs/code-splitting>  
<https://reactjs.org/docs/code-splitting.html>

#### 问题

- URIError: Failed to decode param '%PUBLIC_URL%/manifest.json'  
  执行 webpack 错误, 将`public/index.html`里的`<link rel="manifest" href="%PUBLIC_URL%/manifest.json" />改成`<link rel="manifest" href="manifest.json" />

- react router nested webpack error  
  无法访问, 后台显示: URIError: Failed to decode param '%PUBLIC_URL%/favicon.ico'等信息  
  <https://stackoverflow.com/questions/56573363/react-router-v4-nested-routes-not-work-with-webpack-dev-server>  
  在 index.html 里加上`<base href="/" />`
