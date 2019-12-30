---
layout:     post
title:      "Adapter design pattern in Ruby适配器设计模式"
subtitle:   ""
date:       2019-12-30
categories: Program
tags:
    - Design Pattern
---

假设我们有这样的一个加密代码:

```ruby
class Encrypter
  def initialize(key)
    @key = key
  end

  def encrypt(reader, writer)
    key_index = 0
    while not reader.eof?
      clear_char = reader.getc
      encrypted_char = (clear_char.ord ^ @key[key_index].ord).chr
      writer.putc(encrypted_char)
      key_index = (key_index + 1) % @key.size
    end
  end
end

reader = File.open('message.txt')
writer = File.open('message.encrypted', 'w')
encrypter = Encrypter.new('my secrect key')
encrypter.encrypt(reader, writer)
```

我们可以对文件进行加密, 并输出到另外一个文件.

加入我们需要对一个字符串进行加密呢? 可以看见, 并不支持

这个时候适配器设计模式就可以登场了.

在动态语言里, 有鸭子类型的概念, 就是说, 只要不同的对象有同样的方法, 那么我们就可以视之为相同的对象(可能表达不准确2333)

对于上面的例子来说, 只要对象有像文件一样的eof?和getc方法, 就可以适用于Encrypter, 好, 那么我们写一个适配器, 对字符串进行封装:

```ruby
class StringIOAdapter
  def initialize(string)
    @string = string
    @position = 0
  end

  def getc
    if @position >= @string.length
      raise EOFError
    end
    ch = @string[@position]
    @position += 1
    return ch
  end

  def eof?
    return @position >= @string.length
  end
end

encrypter = Encrypter.new('XYZZY')
reader = StringIOAdapter.new('We attack a dawn')
writer=File.open('out.txt', 'w')
encrypter.encrypt(reader, writer)
```

这个就是适配器设计模式:

There really is no magic to adapters: They exist to soak up the differences between the interfaces that we need and the objects that we have.

The Adapter pattern is the first member of a family of patterns we will encounter—a family of patterns in which one object stands in for another object. This family of object-oriented impostors also includes proxies and decorators. In each case, an object acts more or less as the front man for another object. As you will see in sub- sequent chapters, in each of these patterns the code will look vaguely familiar. At the risk of repeating myself, keep in mind that a pattern is not just about code: Intent is critical. An adapter is an adapter only if you are stuck with objects that have the wrong interface and you are trying to keep the pain of dealing with these ill-fitting interfaces from spreading throughout your system.
