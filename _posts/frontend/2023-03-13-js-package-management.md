---
layout: post
title: "js package management"
date: 2022-09-07
categories: Frontend
tags:
  - npm
  - pnpm
---

### npm

https://stackoverflow.com/questions/22891211/what-is-the-difference-between-save-and-save-dev

npm install --save 和 --save-dev 的区别

--save 安装的是运行需要的.  
--save-dev 安装的只是开发需要的

### pnpm

pnpm is a fast, disk space efficient package manager. can be used as a drop-in replacement for npm and yarn.

#### dlx

dlx can execute a package without installing it. It is similar to npx, but it uses the pnpm store to execute the package.

```bash
pnpm dlx create-umi@latest
```
