---
layout:     post
title:      "Singleton design pattern单例设计模式"
subtitle:   ""
date:       2020-01-02
categories: Program
tags:
    - Design Pattern
---

The motivation behind the Singleton pattern is very simple: There are some things that are unique. Programs frequently have a single configuration file. It is not unusual for a program to let you know how it is doing via a single log file. GUI applications frequently have a one main window, and they typically take input from exactly one keyboard. Many applications need to talk to exactly one database. If you only ever have one instance of a class and a lot of code that needs access to that instance, it seems silly to pass the object from one method to another. In this kind of situation, the GoF suggest that you build a singleton—a class that can have only one instance and that provides global access to that one instance.

我们可以在class层面实现单例模式, 也是GOF推荐的模式, 也可以用全局变量来实现, 但是在唯一性方面是欠缺的.
