---
layout:     post
title:      "supervisor"
date:       2023-06-10
categories: Devops
tags:
    - Deploy
---

- [install](#install)
- [run supervisord](#run-supervisord)
- [run supervisorctl](#run-supervisorctl)
- [其他问题](#其他问题)


http://supervisord.org/

#### install

在Python项目里可以pip安装  

#### run supervisord

可以指定配置文件来启动:
`supervisord -c ./supervisord.conf`

配置模板文件可以用`echo_supervisord_conf > supervisord.conf`来生成, 然后修改

配置文件里可以配置program和group
```conf
[program:surge-backend]
command=gunicorn main:app              ; the program (relative uses PATH, can take args)
autostart=true                ; start at supervisord start (default: true)
autorestart=true        ; when to restart if exited after running (def: unexpected)
stdout_logfile=/tmp/surge/logs/supervisor.out.log        ; stdout log path, NONE for none; default AUTO
stderr_logfile=/tmp/surge/logs/supervisor.err.log        ; stderr log path, NONE for none; default AUTO

[program:websocket]
command=python websocket_server.py              ; the program (relative uses PATH, can take args)
autostart=true                ; start at supervisord start (default: true)
autorestart=true        ; when to restart if exited after running (def: unexpected)
stopasgroup=true             ; send stop signal to the UNIX process group (default false)
killasgroup=true             ; SIGKILL the UNIX process group (def false)
stdout_logfile=/tmp/surge/logs/websocket.out.log        ; stdout log path, NONE for none; default AUTO
stderr_logfile=/tmp/surge/logs/websocket.err.log        ; stderr log path, NONE for none; default AUTO

[group:surge]
programs=surge-backend,websocket  ; each refers to 'x' in [program:x] definitions
```

#### run supervisorctl

配置好之后就可以用supervisorctl来管理
```bash
supervisorctl start surge:websocket
supervisorctl stop surge:websocket
supervisorctl start surge:*
supervisorctl restart surge:*
supervisorctl stop surge:*
```

#### 其他问题

如果一台服务器上要启动多个supervisord, 那么各个supervisord的配置文件需要配置不一样的file和pidfile.
