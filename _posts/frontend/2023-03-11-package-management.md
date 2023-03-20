---
layout:     post
title:      "frontend package management"
date:       2023-03-11
categories: Frontend
tags:
    - npm
    - pnpm
---

### npm

https://stackoverflow.com/questions/22891211/what-is-the-difference-between-save-and-save-dev

npm install --save 和 --save-dev的区别

--save安装的是运行需要的.  
--save-dev安装的只是开发需要的

### pnpm

pnpm is said to be a more efficient package management tool

#### install 

```bash
curl -fsSL https://get.pnpm.io/install.sh | sh -
# then source your .zshrc or .bashrc according to the output
pnpm -v
```

#### usage

- pnpm dlx  
  https://pnpm.io/cli/dlx  
  Fetches a package from the registry without installing it as a dependency, hotloads it, and runs whatever default command binary it exposes.


