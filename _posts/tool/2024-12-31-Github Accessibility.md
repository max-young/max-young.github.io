---
layout: post
title: Github Accessibility
date: 2024-12-31
categories: Tools
tags:
  - Github
---

you might encounter error when git clone and git push.  
1. check your proxy port in your network settings.
2. set git proxy:

    ```shell
    git config --global http.proxy http://127.0.0.1:<your proxy port>
    git config --global https.proxy https://127.0.0.1:<your proxy port>
    ```
  3. set host use SwitchHosts according to this:
if you can't access raw.githubusercontent.com, try this:
<https://github.com/521xueweihan/GitHub520>