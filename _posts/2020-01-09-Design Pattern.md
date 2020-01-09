---
layout:     post
title:      "Design Pattern"
subtitle:   "《Design Patterns in Ruby》读书笔记"
date:       2020-01-09
categories: Program
tags:
    - Design Pattern
---

![Design patterns in Ruby](https://img3.doubanio.com/view/subject/l/public/s4263121.jpg)
[Design patterns in Ruby](https://book.douban.com/subject/2365029/)

## PART I: Patterns and Ruby

### Chapter1: Building Better Programs with Patterns

#### Patterns for Patterns

关于设计模式的著名的一本书: Design Patterns: Elements of Reusable Object-Oriented Software

简称The Gang of Four, 因为作者是4个人, 在和他人沟通这本书的时候, 书名太长, 于是取了一个简称~

关于设计模式有4个要点:

1. Separate out the things that change from those that stay the same.
2. Program to an interface, not an implementation.
3. Prefer composition over inheritance.
4. Delegate, delegate, delegate.

##### Separate out the things that change from those that stay the same

将变化和不变的分离开

##### Program to an interface, not an implementation

开发接口, 而不是实现

示例: 交通工具行驶, 可以这样实现:

```ruby
# Deal with cars and planes
if is_car
  my_car = Car.new
  my_car.drive(200)
else
  my_plane = AirPlane.new
  my_plane.fly(200)
end
```

用接口的方式可以这样做:

```ruby
my_vehicle = get_vehicle
my_vehicle.travel(200)
```

##### Prefer composition over inheritance

继承是这样做的:

```ruby
class Vehicle
  # All sorts of vehicle-related code...
  def start_engine
    # Start the engine
  end
    def stop_engine
      # Stop the engine
  end
end

class Car < Vehicle
  def sunday_drive
    start_engine
    # Cruise out into the country and return
    stop_engine
  end
end
```

car继承了父类的start_engine, stop_engine, 这样做的话要求所有的交通工具都需要引擎, 如果是自行车呢, 那么我们就需要改造Vehicle了.

我们可以把engine独立出来, car还可以继承Vehicle, engine是可选的组件:

```ruby
class Engine
  # All sorts of engine-related code...
  def start
    # Start the engine
  end

  def stop
    # Stop the engine
  end
end

class Car
  def initialize
    @engine = Engine.new
  end

  def sunday_drive
    @engine.start
    # Cruise out into the country and return...
    @engine.stop
  end
end
```

##### Delegate, delegate, delegate

在继承的实现里, car继承了Vehicle的start_engine和stop_engine方法, 那用composition的方法实现之后, 怎么实现这两个方法呢, 我们可以在Car里对engine做Delegate

```ruby
class Car
  def initialize
    @engine = GasolineEngine.new
  end

  def start_engine
    @engine.start
  end

  def stop_engine
    @engine.stop
  end
end
```

#### You Ain’t Gonna Need It

**YAGNI**, 开发的首要目的是解决问题, 设计模式是你解决问题的工具, 不要为了设计模式而去强行运用设计模式.

过度的运用会导致程序变得复杂和难懂. Your code will work better only if it focuses on the job it needs to do right now.

##### Fourteen Out of Twenty-Three

23个设计模式中常用的14个

- Template Method
- Strategy
- Observer
- Composite
- Iterator
- Command
- Adapter
- Proxy
- Decorator
- Singleton
- Factory Method
- Abstract Factory
- Builder
- Interpreter

### Chapter 2: Getting Started with Ruby

如果你对其他编程语言很熟悉, 而且熟悉Python这样的动态语言的话, Ruby应该不会陌生. 这里就不再赘述了.

代码规范往往很重要, 这里说明一下:

Ruby的命名规则是小写字母或者单下划线开头, Ruby推荐用下划线的方式命名, 不推荐驼峰命名法. class name例外.

常量命名是首字母大写, 常量也可以重新赋值, Ruby不做限制, 在irb解释器里会做提示, 但是我们为什么要重新赋值呢?

## PART II Patterns in Ruby

### Chapter 3: Varying the Algorithm with the Template Method

the general idea of the Template Method pattern is to build an abstract base class with a skeletal method.

The Template Method pattern is simply a fancy way of saying that if you want to vary an algorithm, one way to do so is to code the invariant part in a base class and to encapsulate the variable parts in methods that are defined by a number of subclasses. The base class can simply leave the methods completely undefined—in that case, the subclasses must supply the methods. Alternatively, the base class can provide a default implementation for the methods that the subclasses can override if they want.

具体参照: <a href="/blog/Template-Method-in-Ruby模板方法.html">Template-Method-in-Ruby模板方法</a>

### Chapter 4: Replacing the Algorithm with the Strategy

The Strategy pattern is a delegation-based approach to solving the same problem as the Template Method pattern. Instead of teasing out the variable parts of your algo- rithm and pushing them down into subclasses, you simply implement each version of your algorithm as a separate object

具体参照: <a href="/blog/Strategy-in-Ruby策略设计模式.html">Strategy-in-Ruby策略设计模式</a>

### Chapter 5: Keeping Up with the Times with the Observer

The Observer pattern allows you to build components that know about the activities of other components without having to tightly couple everything together in an unmanageable mess of code-flavored spaghetti. By creating a clean interface between the source of the news (the observable object) and the consumer of that news (the observers), the Observer pattern moves the news without tangling things up.

具体参照: <a href="/blog/Observer-design-pattern-in-Ruby观察者设计模式.html">Observer-design-pattern-in-Ruby观察者设计模式</a>

### Chapter6: Assembling the Whole from the Parts with the Composite

组合设计模式在面对这种层级结构时是利器, 他主要的目的是让层级结构的所有节点都是一样的, 但是又能保证层级结构. 在现实世界中这种层级结构是如此普遍, 所以组合设计模式也很通用, 而且有的设计模式其实就是组合设计模式的变种.

具体参照: <a href="/blog/Composite-design-pattern-in-Ruby组合设计模式.html">Composite-design-pattern-in-Ruby组合设计模式</a>

### Chapter7: Reaching into a Collection with the Iterator

Provide a way to access the elements of an aggregate object sequentially without exposing its underlying representation

具体参照: <a href="/blog/Iterator-design-pattern-in-Ruby迭代器设计模式.html">Iterator-design-pattern-in-Ruby迭代器设计模式</a>

### Chapter8: Getting Things Done with Commands

具体参照: <a href="/blog/Command-design-pattern-in-Ruby命令设计模式.html">Command-design-pattern-in-Ruby命令设计模式</a>

### Chapter9: Filling in the Gaps with the Adapter

There really is no magic to adapters: They exist to soak up the differences between the interfaces that we need and the objects that we have

具体参照: <a href="/blog/Adapter-design-pattern-in-Ruby适配器设计模式.html">Adapter-design-pattern-in-Ruby适配器设计模式</a>

### Chapter10: Getting in Front of Your Object with a Proxy

具体参照: <a href="/blog/Proxy-design-pattern-in-Ruby代理设计模式.html">Proxy-design-pattern-in-Ruby代理设计模式</a>

### Chapter11: Improving Your Objects with a Decorator

 what if you simply need to vary the responsibilities of an object? What do you do when sometimes your object needs to do a little more, but sometimes a little less?

The Decorator pattern is the last of the “one object stands in for another” patterns that we will consider in this book. The first was the Adapter pattern; it hides the fact that some object has the wrong interface by wrapping it with an object that has the right interface. The second was the Proxy pattern. A proxy also wraps another object, but not with the intent of changing the interface. Instead, the proxy has the same interface as the object that it is wrapping. The proxy isn’t there to translate; it is there to control. Proxies are good for tasks such as enforcing security, hiding the fact that an object really lives across the network, and delaying the creation of the real object until the last possible moment. And then we have the subject of this chapter, the decorator, which enables you to layer features on to a basic object.

具体参照: <a href="/blog/Decorator-design-pattern装饰器设计模式.html">Decorator design pattern装饰器设计模式</a>

### Chapter12: Making Sure There Is Only One with the Singleton

The motivation behind the Singleton pattern is very simple: There are some things that are unique. Programs frequently have a single configuration file. It is not unusual for a program to let you know how it is doing via a single log file. GUI applications frequently have a one main window, and they typically take input from exactly one keyboard. Many applications need to talk to exactly one database. If you only ever have one instance of a class and a lot of code that needs access to that instance, it seems silly to pass the object from one method to another. In this kind of situation, the GoF suggest that you build a **singleton**—a class that can have only one instance and that provides global access to that one instance.

我们可以在class层面实现单例模式, 也是GOF推荐的模式, 也可以用全局变量来实现, 但是在唯一性方面是欠缺的.

具体参照: <a href="/blog/Singleton-design-pattern单例设计模式.html">Singleton design pattern单例设计模式</a>

### Chapter13: Picking the Right Class with a Factory

具体参照: <a href="/blog/Factory-design-pattern-in-Ruby工厂设计模式.html">Factory design pattern in Ruby工厂设计模式</a>

### Chapter14: Easier Object Construction with the Builder

具体参照: <a href="/blog/Builder-design-pattern-in-Ruby建造者设计模式.html">Builder design pattern in Ruby建造者设计模式</a>

### Chapter15: Assembling Your System with the Interpreter

具体参照: <a href="/blog/Interprete-pattern-in-Ruby解释器设计模式.html">Interprete pattern in Ruby解释器设计模式</a>
