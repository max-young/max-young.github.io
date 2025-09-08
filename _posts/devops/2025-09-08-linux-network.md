---
layout: post
title: "Linux Network"
date: 2025-09-08
categories: Linux
tags:
  - Ubuntu
---

if there are several network in a linux server, we can use the command `ip addr` to check the network interfaces.

and we can set visiting an ip via a specific network.

for example, I installed a external 5G device on a linux server, so there are two networks, I want to set visiting an IP via this 5G device.

1. check the network interfaces

    ```bash
    ip addr
    ```

2. check the routing table

    ```bash
    ip route
    ```

3. add a routing rule(temperary, will be lost after reboot)

    ```bash
    ip route add <destination_ip> via <gateway_ip> dev <network_interface>
    ```
    for example:

    ```bash
    sudo ip route add 14.103.28.216 via 192.168.66.1 dev eno2
    ```

4. add a routing rule(persistent, will not be lost after reboot)

    ```
    vim /etc/netplan/01-netcfg.yaml
    ```
    the content is like:
    ```
    network:
      version: 2
      ethernets:
        eno2:
          addresses: [192.168.66.88/24]
          gateway4: 192.168.66.1
          routes:
            - to: 14.103.28.216/32
              via: 192.168.66.1
    ```
    then apply the netplan

    ```bash
    sudo netplan apply
    ```