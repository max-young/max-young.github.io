---
layout: post
title: "Linux disk"
date: 2025-09-10
categories: Linux
tags:
  - Ubuntu
---


if a disk is new, and could only be seen by 'lsvlk', we need to create a partition and format it.

1. create a partition

```
sudo parted /dev/sda
```

then in the parted shell:

```
mklabel gpt
mkpart primary exfat 0% 100%
quit
```

2. format the partition

```
sudo mkfs.exfat /dev/sda1
```
