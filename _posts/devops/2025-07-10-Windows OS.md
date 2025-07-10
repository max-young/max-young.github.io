---
layout: post
title: "Windows OS"
date: 2025-07-10
categories: Windows
tags:
  - Windows
---

- [use Udisk to install Windows OS](#use-udisk-to-install-windows-os)
  - [download windows ISO](#download-windows-iso)
  - [make bootable Udisk on Ubuntu](#make-bootable-udisk-on-ubuntu)
  - [install windows from udisk](#install-windows-from-udisk)
- [issues](#issues)
  - [无法在驱动器0分区上安装windows](#无法在驱动器0分区上安装windows)


### use Udisk to install Windows OS

#### download windows ISO

download windows iso on windows official website

#### make bootable Udisk on Ubuntu

1. plug in the udisk
2. check the disk mount path  
`lsblk`
3. umount the udisk  
`umount /dev/sdX`
4. download ventoy from [ventoy.net](https://www.ventoy.net/en/index.html)
5. unzip the ventoy package
6. cd to the ventoy directory
7. install ventoy to udisk  
`sudo ./Ventoy2Disk.sh -i /dev/sdX`
8. copy windows iso to udisk root path

#### install windows from udisk

### issues

#### 无法在驱动器0分区上安装windows
1. shift + F10
2. diskpart
3. list disk
4. select disk 0
5. clean
6. convert gpt | convert mbr
   - 如果是 UEFI 模式, 则使用 `convert gpt`
   - 如果是 Legacy 模式, 则使用 `convert mbr`
7. exit
