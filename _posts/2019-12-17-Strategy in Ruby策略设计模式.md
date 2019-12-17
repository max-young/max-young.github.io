---
layout:     post
title:      "Strategy in Ruby策略设计模式"
subtitle:   ""
date:       2019-12-17
categories: Program
tags:
    - Design Pattern
---

在Termplate Method模板方法的设计模式里, 我们设计了一个父类, 然后根据不同的文件格式用不同的子类去实现, 这样的话, 有多少种文件格式就需要创建多少个子类. 这样有没有觉得很不灵活?

设计模式的其中一个原则是: Prefer composition over inheritance. 在交通工具的例子里, 我们把engine这个关键因素独立出来做成了一个组件, 这样这个组件可以灵活的配置, 然后交通工具也可以选择是否装配这个组件.

我们依照这个原则来把导出文本改造一下, 把核心算法独立出来

```ruby
class HTMLFormatter
  def output_report(context)
    puts('<html>')
    puts('  <head>')
    puts("    <title>#{context.title}</title>")
    puts('  </head>')
    puts('  <body>')
    context.text.each do |line|
      puts("    <p>#{line}</p>")
    end
    puts('  </body>')
    puts('</html>')
  end
end

class PlainTextFormatter
  def output_report(context)
    puts("***** #{context.title} *****")
    context.text.each do |line|
      puts(line)
    end
  end
end

class Report
  attr_reader :title, :text
  attr_accessor :formatter

  def initialize(formatter)
    @title = 'Monthly Report'
    @text = ['Things are going', 'really, really well.']
    @formatter = formatter
  end

  def output_report
    @formatter.output_report(self)
  end
end
```

这样, 我们就不需要用继承的方法创建多个子类了, 只需要一个Report类了, 在这个类里面, 我们重新定义了`output_report`函数, 这就是设计模式的另一个原则: Delegate, delegate, delegate

这里可能有一个疑问, 我们不是一样创建了多个类吗?  HTMLFormatter, PlainTextFormatter

是的, 但是在Ruby里, 我们可以用proc的方式去做, 这里不做表述.

在Python里, 我们也可以直接定义函数, 而不是定义类.

策略设计模式, 避免了继承创建多个子类, 把核心算法独立出来做成了一个可装配的组件, 如同交通工具一样, 可以装不同的引擎, 也可以不装配引擎

The Strategy pattern is a delegation-based approach to solving the same problem as the Template Method pattern. Instead of teasing out the variable parts of your algo- rithm and pushing them down into subclasses, you simply implement each version of your algorithm as a separate object
