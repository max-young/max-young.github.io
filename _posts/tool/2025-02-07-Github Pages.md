---
layout:     post
title:      "Github Pages"
subtitle:   ""
date:       2025-02-07
categories: Tools
tags:
    - Tools
---

<!-- TOC -->

- [github page创建个人博客](#github-page创建个人博客)
- [Docsify部署markdown文档](#docsify部署markdown文档)
  - [优化](#优化)
- [Material for MkDocs部署markdown文档](#material-for-mkdocs部署markdown文档)

<!-- /TOC -->

<a id="markdown-github-page创建个人博客" name="github-page创建个人博客"></a>
### github page创建个人博客

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

<a id="markdown-docsify部署markdown文档" name="docsify部署markdown文档"></a>
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