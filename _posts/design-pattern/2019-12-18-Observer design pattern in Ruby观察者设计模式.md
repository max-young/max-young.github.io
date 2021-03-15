---
layout:     post
title:      "Observer design pattern in Ruby观察者设计模式"
subtitle:   ""
date:       2019-12-18
categories: Program
tags:
    - Design Pattern
---

假设有这样的情景, 职员的薪资变化了, 需要通知到薪资部门, 我们可以这么实现:

```ruby
class Employee
 attr_reader :name
 attr_accessor  :title, :salary
 def initialize( name, title, salary, payroll )
   @name = name
   @title = title
   @salary = salary
   @payroll = payroll
  end

  def salary=(new_salary)
    @salary = new_salary
    @payroll.update(self)
  end
end

class Payroll
  def update( changed_employee )
    puts("Cut a new check for #{changed_employee.name}!")
    puts("His salary is now #{changed_employee.salary}!")
  end
end

payroll = Payroll.new
fred = Employee.new('Fred', 'Crane Operator', 30000, payroll)
fred.salary = 35000
```

这样实现有两个问题:

1. Employee和Payroll两个类“缠绕”在一起了
2. 如果还需要通知到其他部门, 我们还需要修改Employee的代码, 比如增加initialize的参数, 修改salary=函数

为了解决这个问题, 我们可以这样做:

```ruby
class Employee
 attr_reader :name
 attr_accessor  :title, :salary
 def initialize( name, title, salary )
   @name = name
   @title = title
   @salary = salary
   @observers = []
  end

  def salary=(new_salary)
    @salary = new_salary
    @notify_observers
  end

  def notify_observers
    @observers.each do |observer|
      observer.update(self)
    end
  end

  def add_observer(observer)
    @observers << observer
  end

  def delete_observer(observer)
    @observers.delete(observer)
  end
end

class Payroll
  def update( changed_employee )
    puts("Cut a new check for #{changed_employee.name}!")
    puts("His salary is now #{changed_employee.salary}!")
  end
end

fred = Employee.new('Fred', 'Crane Operator', 30000.0)
payroll = Payroll.new
fred.add_observer( payroll )
fred.salary=35000.0

class TaxMan
  def update( changed_employee )
    puts("Send #{changed_employee.name} a new tax bill!")
  end
end

tax_man = TaxMan.new
fred.add_observer(tax_man)
fred.salary=90000.0
```

这样我们就解决了上面的两个问题, 还有没有优化空间呢?

对于Employee来说, 只需关注自身的逻辑即可, 通知Payroll这些observer的任务是附加的工作, 把notify_observer, add_obser, delete_observer放在类里面, 干扰了自身的逻辑, 切让代码看着很乱很庞大, 我们可以按照strategy设计模式一样, 把通知的任务独立出来

```ruby
module Subject
  def initialize
    @observers=[]
  end

  def add_observer(observer)
    @observers << observer
  end

  def delete_observer(observer)
    @observer.delete(observer)
  end

  def notify_observers
    @observers.each do |observer|
      observer.update(self)
    end
  end
end


class Employee
  include Subject

  attr_reader :name, :title
  attr_reader :salary

  def initialize(name, title, salary)
    super()
    @name = name
    @title = title
    @salary = salary
  end

  def salary=(new_salary)
    @salary = new_salary
    notify_observers
  end
end

class Payroll
  def update(changed_employee)
    puts("Cut a new check for #{changed_employee.name}!")
    puts("His salary is now #{changed_employee.salary}")
  end
end

fred = Employee.new("Fred Flintstone", "Crane Operator", 30000.0)
payroll = Payroll.new
fred.add_observer(payroll)

fred.salary = 35000.0

class TaxMan
  def update(changed_employee)
    puts("Send #{changed_employee.name} a new tax bill!")
  end
end

tax_man = TaxMan.new
fred.add_observer(tax_man)

fred.salary=90000.0
```

> 这里用到了Ruby的module, 因为Ruby只能继承一个父类, 如果把Subject写成一个类, Employee继承的话, 就不能继承其他父类了, 在Python里可以继承多个类, 就没有这个问题

这就是Observer观察者设计模式, 创建一个干净的接口, 将被观察者和观察者隔离开来, 实现生产和消费, 而不用将两者耦合在一起

The Observer pattern allows you to build components that know about the activities of other components without having to tightly couple everything together in an unmanageable mess of code-flavored spaghetti. By creating a clean interface between the source of the news (the observable object) and the consumer of that news (the observers), the Observer pattern moves the news without tangling things up.
