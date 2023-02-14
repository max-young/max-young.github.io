---
layout: post
title: "monitor network traffic"
date: 2023-02-14
categories: Web
tags:
  - network
---

- [calculate network speed](#calculate-network-speed)
- [newwork knowlesge](#newwork-knowlesge)

#### calculate network speed

<https://blog.csdn.net/ck784101777/article/details/103662962>
<https://www.cnblogs.com/taosiyu/p/11431758.html>

this script can calculute network speed use ifconfig:

```shell
#!/bin/bash

while true
do
    # replace wlp0s20f3 with your network interface
    # replace 7 and 5 with your output of ifconfig, this command get RX and TX bytes of ifconfig
    RX_pre=`ifconfig wlp0s20f3 | awk 'NR==7{print $5}'`
    TX_pre=`ifconfig wlp0s20f3 | awk 'NR==9{print $5}'`
    sleep 1
    RX_aft=`ifconfig wlp0s20f3 | awk 'NR==7{print $5}'`
    TX_aft=`ifconfig wlp0s20f3 | awk 'NR==9{print $5}'`

    clear
    echo -e "`date +%k:%M:%S` \t TX \t RX"

    RX=$((RX_aft-RX_pre))
    TX=$((TX_aft-TX_pre))

    echo -e "\t \t $TX \t $RX "

    if [ $RX -lt 1024 ];then
        echo "${RX}k/s"
        elif [ $RX -lt 1048576 ];then
        echo "$((RX/1024))kb/s"
    else
        echo "$((RX/1048576))m/s"
    fi
    if [ $TX -lt 1024 ];then
        echo "${TX}k/S"
        elif [ $TX -lt 1048576 ];then
        echo "$((TX/1024))kb/s"
    else
        echo "$((TX/1048576))m/s"
    fi
done
```

#### newwork knowlesge

<http://nic.jljy.edu.cn/info/1022/1261.htm>

网络运营商提供的带宽单位是 bit, 我们一般说的网络速度是 byte, 1byte=8bit, 所以如果我们办的宽带是 100M, 那么实际的速度差不多是 10M/s.  
网络分为上行和下行, 家庭宽带一般是下行, 也就是我们从网络上浏览王爷, 下载数据的速度  
上行是指我们从本地上传数据到网络上, 比如上传, 或者自己的电脑当作服务器, 别人来访问, 这种情况比较少.  
所以家庭网络的带宽一般指的是下行带宽, 上行带宽很小, 一般是下行的 1/8  
公司的宽带可能上下行是一样的.
