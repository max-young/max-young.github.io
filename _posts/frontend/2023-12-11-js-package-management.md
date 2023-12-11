---
layout: post
title: "js package management"
date: 2023-12-11
categories: Frontend
tags:
  - npm
  - pnpm
---

- [npm](#npm)
  - [speed up npm install](#speed-up-npm-install)
- [pnpm](#pnpm)
  - [dlx](#dlx)

### npm

https://stackoverflow.com/questions/22891211/what-is-the-difference-between-save-and-save-dev

npm install --save 和 --save-dev 的区别

--save 安装的是运行需要的.  
--save-dev 安装的只是开发需要的

after installing node.js, npm is automatically installed. node.js can be installed by nvm.

The installation of NVM can refer to [the official documentation](https://github.com/nvm-sh/nvm#installing-and-updating).  
according to the official documentation, the first step is download install script using curl or wget command.  
You may encounter this error:

```text
fatal: unable to access 'https://github.com/nvm-sh/nvm.git/': Failed to connect to github.com port 443: Connection timed out
Failed to clone nvm repo. Please report this!
```

the solution is below:

```bash
apt-get install gnutls-bin
git config --global http.sslVerify false
git config --global http.postBuffer 1048576000
```

#### speed up npm install

- 修改成淘宝镜像源

```shell
npm config set registry https://registry.npmmirror.com
# 验证,如果返回https://registry.npmmirror.com，说明镜像配置成功。
npm config get registry
```

- 通过使用淘宝定制的cnpm安装
```shell
# 安装cnpm
npm install -g cnpm --registry=https://registry.npmmirror.com
# 使用cnpm
cnpm install xxx
```

### pnpm

pnpm is a fast, disk space efficient package manager. can be used as a drop-in replacement for npm and yarn.

#### dlx

dlx can execute a package without installing it. It is similar to npx, but it uses the pnpm store to execute the package.

```bash
pnpm dlx create-umi@latest
```
