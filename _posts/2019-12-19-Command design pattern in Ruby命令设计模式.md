---
layout:     post
title:      "Command design pattern in Ruby命令设计模式"
subtitle:   ""
date:       2019-12-19
categories: Program
tags:
    - Design Pattern
---

我们还是说具体的场景, 在GUI里面的一个按钮, 不同的场景下需要点击按钮执行不同的操作, 熟悉的场景, 我们可以想到模板设计模式, 然后用策略设计模式进行优化:

```ruby
class SlickButton
  attr_accessor :command
  def initialize(command)
    @command = command
  end
  #
  # Lots of button drawing and management
  # code omitted...
  #
  def on_button_push
    @command.execute if @command
  end
end

class SaveCommand
  def execute
    #
    # Save the current document...
    #
  end
end

save_button = SlickButton.new( SaveCommand.new )
```

命令设计模式当然并不单单只是如此

假设我们要执行的操作比较复杂呢, 创建一个文件, 复制, 然后删除原文件, 我们应该怎样实现这个command呢

```ruby
class Command
  attr_reader :description

  def initialize(description)
    @description = description
  end

  def
    execute
  end
end

class CreateFile < Command
  def initialize(path, contents)
    super("Create file: #{path}")
    @path = path
    @contents = contents
  end

  def execute
    f = File.open(@path, "w")
    f.write(@contents)
    f.close
  end
end

class DeleteFile < Command
  def initialize(path)
    super("Delete file: #{path}")
    @path = path
  end

  def execute
    File.delete(@path)
  end
end

class CopyFile < Command
  def initialize(source, target)
    super("Copy file: #{source} to #{target}")
    @source = source
    @target = target
  end

  def execute
    FileUtils.copy(@source, @target)
  end
end

class CompositeCommand < Command
  def initialize
    @commands = []
  end

  def add_command(cmd)
    @commands << cmd
  end

  def execute
    @commands.each {|cmd| cmd.execute}
  end

  def description
    description = ''
    @commands.each {|cmd| description += cmd.description + "\n"}
    description
  end
end

cmds = CompositeCommand.new
cmds.add_command(CreateFile.new('file1.txt', "hello world\n"))
cmds.add_command(CopyFile.new('file1.txt', 'file2.txt'))
cmds.add_command(DeleteFile.new('file1.txt'))
```

这里又有一点像观察者模式. 所以命令设计模式其实是各种设计模式的组合变化. 但是各个设计模式有不同的应用场景.

但是这三个操作是有联系的, 针对的是相关的文件.  文件又是可以配置的. 可以灵活配置和组合. 所以在一些复杂的事务里面可以用到命令模式
