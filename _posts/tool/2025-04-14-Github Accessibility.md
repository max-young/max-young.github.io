---
layout: post
title: Github Accessibility
date: 2025-04-14
categories: Tools
tags:
  - Github
---

you might encounter error when git clone and git push. The following are some solutions to fix it.

1. <https://stackoverflow.com/questions/15589682/how-to-fix-ssh-connect-to-host-github-com-port-22-connection-timed-out-for-g>

    add following to your ~/.ssh/config

    ```
    Host github.com
        Hostname ssh.github.com
        Port 443
    ```
  

2. check your proxy port in your network settings.
3. set git proxy:

    ```shell
    git config --global http.proxy http://127.0.0.1:<your proxy port>
    git config --global https.proxy https://127.0.0.1:<your proxy port>
    ```
  1. set host use SwitchHosts according to this:
if you can't access raw.githubusercontent.com, try this:
<https://github.com/521xueweihan/GitHub520>