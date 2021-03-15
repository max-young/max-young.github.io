---
layout:     post
title:      "Decorator design pattern装饰器设计模式"
subtitle:   ""
date:       2020-01-02
categories: Program
tags:
    - Design Pattern
---

 what if you simply need to vary the responsibilities of an object? What do you do when sometimes your object needs to do a little more, but sometimes a little less?

The Decorator pattern is the last of the “one object stands in for another” patterns that we will consider in this book. The first was the Adapter pattern; it hides the fact that some object has the wrong interface by wrapping it with an object that has the right interface. The second was the Proxy pattern. A proxy also wraps another object, but not with the intent of changing the interface. Instead, the proxy has the same interface as the object that it is wrapping. The proxy isn’t there to translate; it is there to control. Proxies are good for tasks such as enforcing security, hiding the fact that an object really lives across the network, and delaying the creation of the real object until the last possible moment. And then we have the subject of this chapter, the decorator, which enables you to layer features on to a basic object.
