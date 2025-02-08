---
layout:     post
title:      "Github Pages"
subtitle:   ""
date:       2025-02-08
categories: Tools
tags:
    - Tools
---

#### github page with vite

1. create a vite project

2. create a repository on github

3. add remote repository

4. install gh-pages

   ```sh
   npm install gh-pages --save-dev
   ```

5. add deploy script in package.json

   ```json
   "scripts": {
     "deploy": "gh-pages -d dist"
   }
   ```

6. edit vite.config.js

   ```js
   export default defineConfig({
     base: '/repository-name/',
   })
   ```

7. config github page

   set branch to `gh-pages`

8. deploy

   ```sh
   npm run build
   npm run deploy
   ```

9. visit `https://username.github.io/repository-name/`

10. custom domain

   if you want to use custom domain like readom.maxyoun.fun,  
   you need to set custom domain in github page setting.  
   and the base of vite.config.js should be `/`

### github page with jekyll

1. github创建仓库

   参照https://pages.github.com/

2. jekyll

   https://jekyllrb.com/docs/

   需要注意的是, 在已有仓库里初始化jekyll, cd到仓库路径下, 运行

   ```sh
   $ jekyll new . --force
   ```

   在本地运行`bundle exec jekyll server`

   在浏览器访问`localhost:4000`就可以看到效果了

3. jekyll theme

   上一步看到的是默认模板, 可以采用网上的模板来美化我们的博客

   我采用的是https://github.com/willard-yuan/willard-yuan.github.io

   按照步骤做就可以了

### Docsify部署markdown文档

[Docsify](https://docsify.js.org/#/)部署markdown文档

#### 优化

1. C++ code color  
   在index.html里引用js:
   ```html
   <script src="//cdn.jsdelivr.net/npm/prismjs@1/components/prism-c.js"></script>
   <script src="//cdn.jsdelivr.net/npm/prismjs@1/components/prism-cpp.js"></script>
   ```
   markdown文件里写C++代码时加上cpp标签

<a id="markdown-material-for-mkdocs部署markdown文档" name="material-for-mkdocs部署markdown文档"></a>
### Material for MkDocs部署markdown文档

[Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)部署markdown文档