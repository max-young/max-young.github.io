---
layout:     post
title:      "Proxy design pattern in Ruby代理设计模式"
subtitle:   ""
date:       2019-12-31
categories: Program
tags:
    - Design Pattern
---

Proxies are the con artists of the programming world: They pretend to be some other object when they are not, in fact, that object. Inside the proxy is hidden a reference to the other, real object—an object that the GoF referred to as the subject.

一个对象, 我们可以直接给用户, 但有时候也特殊需求, 比如给特定的用户不同的权限, 我们就可以用到代理设计模式, 伪装成同一个对象, 但是是虚假的, 但内核是指向真正的对象.

例如银行账号对象:

```ruby
class BankAccount
  attr_reader :balance

  def initialize(starting_balance=0)
    @balance = starting_balance
  end

  def deposit(amount)
    @balance += amount
  end

  def withdraw(amount)
    @balance -= amount
  end
end

account = BankAccount.new(100)
account.deposit(50)
account.withdraw(10)
```

假设我们对特定的用户检查权限, 我们可以写一个代理, 而不是修改原始的BankAccount

```ruby
require 'etc'

class AccountProtectionProxy
  def initialize(real_account, owner_name)
    @subject = real_account
    @owner_name = owner_name
  end

  def deposit(amount)
    check_access
    return @subject.depost(amount)
  end

  def withdraw(amount)
    check_access
    return @subject.withdraw(amount)
  end

  def balance
    check_access
    return @subject.balance
  end

  def check_access
    if Etc.getlogin != @owner_name
      raise "Illegal access: #{Etc.getlogin} cannot access account."
    end
  end
end
```
