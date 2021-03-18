---
layout:     post
title:      "Interprete pattern in Ruby解释器设计模式"
subtitle:   ""
date:       2020-01-06
categories: Program
tags:
    - Design Pattern
---

在石器时代, 数据库的操作都是由数据库专家在做. 直到SQL语言的出现, 简单的语言就可以执行很多数据库操作. 还有web页面, 以前也是由专业工程师经过大量的工作来完成, 现在, 中学生都能通过HTML语言来渲染界面.

这些都归功于Interpreter. Interpreter pattern被忽略, 因为程序员可能很擅长web开发和数据库设计, 但是却很少擅长AST和parser. 接下里我们来解释AST和parser.

我们有一段搜索文件的代码, 有非常多丰富的功能, 我们可以搜索所有文件, 可以根据文件名, 是否可写, 文件大小来搜索, 也可以做or and 搜索.

```ruby
require 'find'

class Expression
  # Common expression code will go here soon...
end

class All < Expression
  def evaluate(dir)
    results = []
    Find.find(dir) do |p|
      next unless File.file?(p)
      results << p
    end
    results
  end
end

class FileName < Expression
  def initialize(pattern)
    @pattern = pattern
  end

  def evaluate(dir)
    results = []
    Find.find(dir) do |p|
      next unless File.file?(p)
      name = File.basename(p)
      results << p if File.fnmatch(@pattern, name)
    end
    results
  end
end

expr_all = All.new
files = expr_all.evaluate('.')
puts(files)

puts('-------------------------------------')

expr_txt = FileName.new('*.txt')
txts = expr_txt.evaluate('.')
puts(txts)

puts('-------------------------------------')

class Bigger < Expression
  def initialize(size)
    @size = size
  end

  def evaluate(dir)
    results = []
    Find.find(dir) do |p|
      next unless File.file?(p)
      results << p if(File.size(p) > @size)
    end
    results
  end
end

class Writable < Expression
  def evaluate(dir)
    results = []
    Find.find(dir) do |p|
      next unless File.file?(p)
      results << p if(File.writable?(p))
    end
    results
  end
end

class Not < Expression
  def initialize(expression)
    @expression = expression
  end

  def evaluate(dir)
    All.new.evaluate(dir) - @expression.evaluate(dir)
  end
end

expr_not_writable = Not.new(Writable.new)
readonly_files = expr_not_writable.evaluate('.')
puts(readonly_files)

puts('-------------------------------------')

small_expr = Not.new(Bigger.new(1024))
small_files = small_expr.evaluate('.')
puts(small_files)

puts('-------------------------------------')

not_txt_expr = Not.new(FileName.new('*.txt'))
not_txts = not_txt_expr.evaluate('.')
puts(not_txts)

puts('-------------------------------------')

class Or < Expression
  def initialize(expression1, expression2)
    @expression1 = expression1
    @expression2 = expression2
  end

  def evaluate(dir)
    result1 = @expression1.evaluate(dir)
    result2 = @expression2.evaluate(dir)
    (result1 + result2).sort.uniq
  end
end

big_or_txt_expr = Or.new(Bigger.new(1024), FileName.new('*.mp3'))
big_or_txts = big_or_txt_expr.evaluate('.')
puts(big_or_txts)

puts('-------------------------------------')

class And < Expression
  def initialize(expression1, expression2)
    @expression1 = expression1
    @expression2 = expression2
  end

  def evaluate(dir)
    result1 = @expression1.evaluate(dir)
    result2 = @expression2.evaluate(dir)
    (result1 & result2)
  end
end

complex_expression = And.new(
  And.new(Bigger.new(1024), FileName.new('*.txt')),
  Not.new(Writable.new))
complex_result = complex_expression.evaluate('.')
puts(complex_result)

puts('-------------------------------------')
```

但是这些操作对于“用户”来说太复杂了, 我们可不可以提供简单的语句给“用户”, 来执行这些复杂的操作.

那么我们首先要做的是: 抽象出AST(abstract syntax tree), 这里不详述了, 反正就是需要整理出一个抽象化的模型.

比如我们需要查找大小大于1024kb, 类型是.rb, 并且是可写的文件, 那么我们可以抽象成:

```
and (and(bigger 1024)(filename *.rb)) writable
```

那么我们需要把这个语句parser成能执行的代码, 这样我们就需要构建一个parser:

```ruby
class Parser
  def initialize(text)
    @tokens = text.scan(/\(|\)|[\w\.\*]+/)
  end

  def next_token
    @tokens.shift
  end

  def expression
    token = next_token
    if token == nil
      return nil
    elsif token == '('
      result = expression
      raise 'Expected )' unless next_token == ')'
      result
    elsif token == 'all'
      return All.new
    elsif token == 'writable'
      return Writable.new
    elsif token == 'bigger'
      return Bigger.new(next_token.to_i)
    elsif token == 'filename'
      return FileName.new(next_token)
    elsif token == 'not'
      return Not.new(expression)
    elsif token == 'and'
      return And.new(expression, expression)
    elsif token == 'or'
      return Or.new(expression, expression)
    else
      raise "Unexpected token: #{token}"
    end
  end
end

parser = Parser.new "and (and(bigger 1024)(filename *.rb)) writable"
ast = parser.expression
result = ast.evaluate('.')
puts(result)
```

这就是interpreter pattern.
