---
layout: post
title: "Linux disk"
date: 2025-09-17
categories: Linux
tags:
  - Ubuntu
---

- [查看路径挂载在哪个磁盘下](#查看路径挂载在哪个磁盘下)
- [check disk info](#check-disk-info)
- [format disk to another file system](#format-disk-to-another-file-system)
- [format a new disk](#format-a-new-disk)
- [monitor disk](#monitor-disk)


### 查看路径挂载在哪个磁盘下
  ```shell
  # df -h再加上路径
  $ df -h /tmp
    Filesystem      Size  Used Avail Use% Mounted on
    /dev/sde2       439G   21G  395G   6% /
  ```

### check disk info
  
  ```shell
  $ lsblk -f
  NAME   FSTYPE LABEL UUID                                 MOUNTPOINT
  sda
    ├─sda1 vfat         12345678-1234-1234-1234-123456789012 /
  ```

### format disk to another file system

  for example, format from vfat to exfat(exfat is better for large files):

  1. install exfat-utils

     ```shell
     # ubuntu 18 or 20
     sudo apt install exfat-utils
     # ubuntu > 20
     sudo apt install exfatprogs
     ```
  2. unmount the disk

     ```shell
     sudo umount /dev/sda1
     ```
  3. format the disk
     ```shell
     sudo mkfs.ext4 -L rino /dev/sda1
     ```

### format a new disk

if a disk is new, and could only be seen by 'lsvlk', we need to create a partition and format it.

1. create a partition

    ```
    sudo parted /dev/sda
    ```

    then in the parted shell:

    ```
    mklabel gpt
    mkpart primary ext4 0% 100%
    quit
    ```

2. format the partition

    ```
    sudo mkfs.exfat /dev/sda1
    ```
    or

    ```
    sudo mkfs.ext4 /dev/sda1
    ```

    use `-L` to add a label

    ```
    sudo mkfs.ext4 -L rino /dev/sda1
    ```

### monitor disk

we can use `iostat` to monitor the disk usage

```bash
iostat -x 5
iostat -dx 1
iostat -dx /dev/sdd 1
```

and we can use `iotop` to monitor the disk usage by process

```bash
sudo iotop
```