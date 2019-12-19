---
layout:     post
title:      "Iterator design pattern in Ruby迭代器设计模式"
subtitle:   ""
date:       2019-12-19
categories: Program
tags:
    - Design Pattern
---

在GOF里是这么描述Iterator的:

> Provide a way to access the elements of an aggregate object sequentially without exposing its underlying representation

获取集合的元素, 而不用管这个元素内部的机制.

我们可以这么实现:

```Ruby
class ArrayIterator
  def initialize(array)
    @array = array
    @index = 0
  end

  def has_next?
    @index < @array.length
  end

  def item
    @array[@index]
  end

  def next_item
    value = @array[@index]
    @index += 1
    value
  end
end

array = ['red', 'green', 'blue']

i = ArrayIterator.new(array)
while i.has_next?
  puts("item: #{i.next_item}")
end

i = ArrayIterator.new('abc')
while i.has_next?
  puts("item: #{i.next_item}")
end
```

迭代器有什么用呢? 下面举个例子, 将两个已经排序的list合并成一个list, 也是排序好的

```ruby
def merged (array1, array2)
  result = []
  iterator1 = ArrayIterator.new(array1)
  iterator2 = ArrayIterator.new(array2)

  while (iterator1.has_next? && iterator2.has_next?)
    if (iterator1.item < iterator2.item)
      result << iterator1.next_item
    else
      result << iterator2.next_item
    end
  end

  while (iterator1.has_next?)
    result << iterator1.next_item
  end

  while (iterator2.has_next?)
    result << iterator2.next_item
  end

  result
end

puts(merged([1, 2, 3], [2, 4, 5]))
```
在Python里面用yield就可以实现迭代器
上面只是举了一个迭代器的简单例子, 实际上还有很多用处, 比如节约内存等
