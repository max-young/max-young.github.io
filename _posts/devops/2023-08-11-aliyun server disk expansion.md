---
layout: post
title: "Aliyun server disk expansion"
date: 2023-08-11
categories: DevOps
tags:
  - ali
---

##### 背景

数据服务器的磁盘空间不足，如下所示：

```shell
[root@ksxing-db1 ~]# df -h
Filesystem      Size  Used Avail Use% Mounted on
/dev/vda1        20G  5.3G   14G  29% /
devtmpfs        7.8G     0  7.8G   0% /dev
tmpfs           7.8G     0  7.8G   0% /dev/shm
tmpfs           7.8G  8.3M  7.8G   1% /run
tmpfs           7.8G     0  7.8G   0% /sys/fs/cgroup
/dev/vdb1       246G  229G  5.3G  98% /data
```

挂载的`/data`数据盘使用率已达到 98%，很危险，于是我们需要对数据盘扩容，升级到 300G

##### 步骤

参考文档：[https://help.aliyun.com/document_detail/25452.html?spm=5176.doc35095.2.4.u8aior](https://help.aliyun.com/document_detail/25452.html?spm=5176.doc35095.2.4.u8aior)

文档大体没问题，下面结合实际详述一遍：

1. 在阿里云控制台扩容数据盘，此处不再赘述

2. 控制台重启服务器

3. 终端登录服务器

4. 卸载数据盘

   ```shell
   # umount后面加上数据盘的路径
   shell> umount /data
   ```

5. 重新分区

   查看现有分区，我们看到/dev/vdb 磁盘是 327.5，有一个/dev/vdb1 分区

   ```shell
   [root@ksxing-db1 ~]# fdisk -l

   Disk /dev/vda: 21.5 GB, 21474836480 bytes, 41943040 sectors
   Units = sectors of 1 * 512 = 512 bytes
   Sector size (logical/physical): 512 bytes / 512 bytes
   I/O size (minimum/optimal): 512 bytes / 512 bytes
   Disk label type: dos
   Disk identifier: 0x0009e68a

      Device Boot      Start         End      Blocks   Id  System
   /dev/vda1   *        2048    41943039    20970496   83  Linux

   Disk /dev/vdb: 327.5 GB, 327491256320 bytes, 639631360 sectors
   Units = sectors of 1 * 512 = 512 bytes
   Sector size (logical/physical): 512 bytes / 512 bytes
   I/O size (minimum/optimal): 512 bytes / 512 bytes
   Disk label type: dos
   Disk identifier: 0xf9d16acd

      Device Boot      Start         End      Blocks   Id  System
   /dev/vdb1            2048   639631359   319814656   83  Linux
   ```

   对磁盘/dev/vdb 重新分区，d 删除原有分区，依次输入 n，p，1 来新建分区。(npl 分别代表什么意思下面会有提示)，选择 sector 时，直接回车选择默认值即可

   ```shell
   [root@ksxing-db1 ~]# fdisk /dev/vdb

   Welcome to fdisk (util-linux 2.23.2).

   Changes will remain in memory only, until you decide to write them.

   Be careful before using the write command.

   Command (m for help): d

   Selected partition 1

   Partition 1 is deleted

   Command (m for help): n

   Partition type:

      p   primary (0 primary, 0 extended, 4 free)

      e   extended

   Select (default p): p

   Partition number (1-4, default 1): 1

   First sector (2048-639631359, default 2048):

   Using default value 2048

   Last sector, +sectors or +size{K,M,G} (2048-639631359, default 639631359):

   Using default value 639631359

   Partition 1 of type Linux and of size 305 GiB is set

   Command (m for help): wq

   The partition table has been altered!

   Calling ioctl() to re-read partition table.

   Syncing disks.
   ```

6. 重新卸载数据盘

   > 官方文档里没有这一步，但是实际操作中我们发现重新分区后，系统又自动挂载数据盘了

7. 检查文件系统，并变更文件系统大小。

   使用 e2fsck 的时候由于系统需要检查并订正文件系统元数据，所以速度较慢、耗时较长，请耐心等待。

   使用 e2fsck 和 resize2fs 指令，正确操作情况下，不会造成原有数据丢失的。

   > 分区命令`fdisk`是对磁盘`/dev/vdb`操作， 这里是对文件系统（就是分区`/dev/vdb1`）进行操作

   ```shell
   [root@ksxing-db1 ~]# e2fsck -f /dev/vdb1
   e2fsck 1.42.9 (28-Dec-2013)
   Pass 1: Checking inodes, blocks, and sizes
   Pass 2: Checking directory structure
   Pass 3: Checking directory connectivity
   Pass 4: Checking reference counts
   Pass 5: Checking group summary information
   /dev/vdb1: 72352/16384000 files (6.5% non-contiguous), 60867041/65535744 blocks
   [root@ksxing-db1 ~]# resize2fs /dev/vdb1
   resize2fs 1.42.9 (28-Dec-2013)
   Resizing the filesystem on /dev/vdb1 to 79953664 (4k) blocks.
   The filesystem on /dev/vdb1 is now 79953664 blocks long.
   ```

8. 重新挂载数据盘

   ```shell
   # 第一个参数是数据盘分区，第二个参数是路径名
   [root@ksxing-db1 ~]# mount /dev/vdb1 /data
   ```

9. 查看状态

   数据盘大小变成了 300G，升级成功

   ```shell
   [root@ksxing-db1 ~]# df -h
   Filesystem      Size  Used Avail Use% Mounted on
   /dev/vda1        20G  5.3G   14G  29% /
   devtmpfs        7.8G     0  7.8G   0% /dev
   tmpfs           7.8G     0  7.8G   0% /dev/shm
   tmpfs           7.8G  8.3M  7.8G   1% /run
   tmpfs           7.8G     0  7.8G   0% /sys/fs/cgroup
   /dev/vdb1       301G  229G   57G  81% /data
   ```

   ​
