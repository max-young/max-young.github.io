---
layout: post
title: "Docker GUI"
date: 2025-07-10
categories: Docker
tags:
  - Docker
---

- [Ubuntu](#ubuntu)
- [Windows](#windows)

If there are GUI applications that you want to run in Docker, you can use the following methods to achieve it:

#### Ubuntu

```
docker run --name car_production_line -itd --restart=always --env="DISPLAY" --env="QT_X11_NO_MITSHM=1" --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" car_production_line
xhost +local:docker && docker exec -it car_production_line bash -c "command"
```

#### Windows

1. Install [VcXsrv](https://sourceforge.net/projects/vcxsrv/)
2. Run VcXsrv
3. install docker desktop
3. run docker in powershell
    ```
    docker run --name car_production_line -itd --restart=always -e DISPLAY=host.docker.internal:0 car_production_line
    ```
4. run GUI application in power shell
    ```
    docker exec -it car_production_line bash -c 'command'
    ```

we can create a desktop shortcut to run the GUI application directly:
1. set docker to start when Windows starts
2. create a .bat file with the following content:
    ```bat
    @echo off
    setlocal

    tasklist /FI "IMAGENAME eq vcxsrv.exe" | find /I "vcxsrv.exe" >nul
    if errorlevel 1 (
        echo Starting VcXsrv...
        start "" "C:\Program Files\VcXsrv\vcxsrv.exe" :0 -multiwindow -clipboard -wgl -ac
        timeout /t 3 >nul
    ) else (
        echo VcXsrv is already running.
    )

    docker ps --format "{{.Names}}" | findstr /i "car_production_line" >nul
    if errorlevel 1 (
        echo Starting Docker container...
        docker run --name car_production_line -itd --restart=always -e DISPLAY=host.docker.internal:0 car_production_line
    ) else (
        echo Docker container already running.
    )

    powershell -Command "docker exec -it car_production_line bash -c 'biaoding'"

    endlocal
    pause
    ```
3. create a desktop shortcut to the .bat file
4. double-click the shortcut to run the GUI application
