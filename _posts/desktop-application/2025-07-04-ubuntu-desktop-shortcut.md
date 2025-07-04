---
layout: post
title: "Ubuntu desktop shortcut application"
date: 2025-07-04
categories: Linux
tags:
  - Ubuntu
---

if you want to create a desktop shortcut for an application or simplely a shell script, you can follow this:

1. crate a file with `.desktop` extension, for example `main.desktop`.
2. add the following content to the file:

    ```ini
    [Desktop Entry]
    Version=1.0
    Type=Application
    Name=白犀牛车辆标定
    Comment=This is a shortcut to calibration shell script
    Exec=gnome-terminal -- bash -c "bd; exec bash"
    Icon=/opt/rino-calibration/vehicle-inspection.png
    Terminal=true
    ```
3. save the file to `~/Desktop/` directory.
4. use this command to make the file executable:

    ```bash
    gio set ~/Desktop/main.desktop metadata::trusted true
    ``` 
5. set an icon
    move your icon image to the directory which set in the `Icon` field.
