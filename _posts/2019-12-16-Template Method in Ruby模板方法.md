---
layout:     post
title:      "Template Method in Ruby模板方法"
subtitle:   ""
date:       2019-12-16
categories: Program
tags:
    - Design Pattern
---

直接用代码来说明

假设我们有输出文本的需求, 基本的实现是这样的:

```ruby
class Report
  def initialize
    @title = 'Monthly Report'
    @text =  [ 'Things are going', 'really, really well.' ]
  end

  def output_report
    puts('<html>')
    puts('  <head>')
    puts("    <title>#{@title}</title>")
    puts('  </head>')
    puts('  <body>')
    @text.each do |line|
      puts("    <p>#{line}</p>" )
    end
    puts('  </body>')
    puts('</html>')
  end
end

report = Report.new
report.output_report
```

这是输出HTML格式的文本, 那加入又有输出plain text的需求呢, 我们修改一下:

```ruby
class Report
  def initialize
    @title = 'Monthly Report'
    @text =  ['Things are going', 'really, really well.']
  end

  def output_report(format)
    if format == :plain
      puts("*** #{@title} ***")
    elsif format == :html
      puts('<html>')
      puts('  <head>')
      puts("    <title>#{@title}</title>")
      puts('  </head>')
      puts('  <body>')
    else
      raise "Unknown format: #{format}"
    end
    @text.each do |line|
      if format == :plain
        puts(line)
      else
        puts("    <p>#{line}</p>" )
      end
    end
    if format == :html
      puts('  </body>')
      puts('</html>')
    end
  end
end
```

代码很复杂有没有? 如果再增加格式, 按照这样的方式写下去, 那代码就太糟糕了.

而且违背了设计模式的原则之一: Separate out the things that change from those that stay the same, 将不变的与可变的分开

那么我们分析一下什么是可变的, 什么是不变的.

不论是HTML格式还是plain text格式, 都需要输出几个固定的部分, 只是各个部分根据不同的格式输出内容不一样, 代码可以这样优化

```ruby
class Report
  def initialize
    @title = 'MonthlyReport'
    @text =  ['Things are going', 'really, really well.']
  end

  def output_report
    output_start
    output_title(@title)
    output_body_start
    for line in @text
      output_line(line)
    end
    output_body_end
    output_end
  end

  def output_start
    puts('<html>')
  end

  def output_title(title)
    puts('  <head>')
    puts("    <title>#{title}</title>")
    puts('  </head>')
  end

  def output_body_start
    puts('  <body>')
  end

  def output_line(line)
    puts("    <p>#{line}")
  end

  def output_body_end
    puts('  </body>')
  end

  def output_end
    puts('</html')
  end
end

class HTMLReport < Report
end

class PlainTextReport < Report
  def output_start
  end

  def output_title(title)
    puts("*** #{title} ***")
  end

  def output_body_start
  end

  def output_line(line)
    puts("#{line}")
  end

  def output_body_end
  end

  def output_end
  end
end

report = HTMLReport.new
report.output_report

report = PlainTextReport.new
report.output_report
```

我们在基类里定义了“不变”的骨架, 在子类了复写了“可变”的方法, 这样不论多少种格式, 骨架都可以不变, 只需增加子类, 复写方法就可以了.

The Template Method pattern is simply a fancy way of saying that if you want to vary an algorithm, one way to do so is to code the invariant part in a base class and to encapsulate the variable parts in methods that are defined by a number of subclasses. The base class can simply leave the methods completely undefined—in that case, the subclasses must supply the methods. Alternatively, the base class can provide a default implementation for the methods that the subclasses can override if they want.
