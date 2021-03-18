---
layout:     post
title:      "Builder design pattern in Ruby建造者设计模式"
subtitle:   ""
date:       2020-01-06
categories: Program
tags:
    - Design Pattern
---

假设我们要组装一台电脑, 我们可以这样写:

```ruby
class Computer
  attr_accessor :display
  attr_accessor :motherboard
  attr_reader :drives

  def initialize(display=:crt, motherboard=Motherboard.new, drives=[])
    @motherboard = motherboard
    @drives = drives
    @display = display
  end
end

class CPU
  # Common CPU stuff...
end

class BasicCPU < CPU
  # Lots of not very fast CPU-related stuff...
end

class TurboCPU < CPU
  # Lots of very fast CPU stuff...
end

class Motherboard
  attr_accessor :cpu
  attr_accessor :memory_size

  def initialize(cpu=BasicCPU.new, memory_size=1000)
    @cpu = cpu
    @memory_size = memory_size
  end
end

class Drive
  attr_reader :type # either :hard_disk, :cd or :dvd
  attr_reader :size # in MB
  attr_reader :writable # true if this drive is writable

  def initialize(type, size, writable)
    @type = type
    @size = size
    @writable = writable
  end
end

# Build a fast computer with lots of memory...

motherboard = Motherboard.new(TurboCPU.new, 4000)

# ... and a hard drive, a CD writer, and a DVD

drives = []
drives << Drive.new(:hard_drive, 200000, true)
drives << Drive.new(:cd, 760, true)
drives << Drive.new(:dvd, 4700, false)

computer = Computer.new(:lcd, motherboard, drives)
```

我们创建了很多复杂的类来表示电脑组件, 然后用一连串的操作来组装电脑, 我们可以把这一连串的组装整合在一起:

```ruby
class ComputerBuilder
  attr_reader :computer

  def initialize
    @computer = Computer.new
  end

  def turbo(has_turbo_cpu=true)
    @computer.motherboard.cpu = TurboCPU.new
  end

  def display=(display)
    @computer.display=displau
  end

  def memory_size=(size_in_mb)
    @computer.motherboard.memory_size = size_in_mb
  end

  def add_cd(writer=false)
    @computer.drives << Drive.new(:cd, 760, writer)
  end

  def add_dvd(writer=false)
    @computer.drives << Drive.new(:dvd, 4000, writer)
  end

  def add_hard_disk(size_in_mb)
    @computer.drives << Drive.new(:hard_disk, size_in_mb, true)
  end
end

builder = ComputerBuilder.new
builder.turbo
builder.add_cd(true)
builder.add_dvd
builder.add_hard_disk(100000)
computer = Builder.computer
```

这样的构建避免了选择正确的class的问题, 我们只需关注如何配置. 而且还能保证构建出完美的对象, 比如我们在builder里增加检查, 没有CPU则报错.

如果创建对象很简单, 配置很少, 我们就不要滥用构建设计模式了.只有在构建很复杂的情况下, 才应考虑这个设计模式.
