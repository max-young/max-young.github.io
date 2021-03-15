---
layout:     post
title:      "Composite design pattern in Ruby组合设计模式"
subtitle:   ""
date:       2019-12-18
categories: Program
tags:
    - Design Pattern
---

### Composite design pattern in Ruby组合设计模式

我们在实际项目中经常会遇到层级树状结构的模型, 在实际生活中也经常遇到, 比如公司的部门层级等等, 我们在这里以做蛋糕举例, 我们需要了解到做蛋糕的步骤, 跟踪每一步的时间, 抽象成一张图比较一目了然:

![composite-design-pattern](/images/posts/2019/composite-design-pattern.png)

做蛋糕也可以抽象成层级结构, 那么我们按照组合设计模式应该怎么做呢:

1. First, you need a common interface or base class for all of your objects. The GoF call this base class or interface the **component**

   我们需要找到所有节点的共性, 来创建一个基类, 这个基类成为**component**元件, 在这里, 基类需要初始化做蛋糕各个分解任务的名称, 已经这个任务所需要的时间

   ```ruby
   class Task
     attr_reader :name

     def initialize(name)
       @name = name
     end

     def get_time_required
       0.0
     end
   end
   ```

2. Second, you need one or more **leaf** classes

   我们创建最底层的子节点的类, 继承基类

   ```ruby
   class AddDryIngredientsTask < Task
     def initialize
       super('Add dry ingredients')
     end

     def get_time_required
       1.0             # 1 minute to add flour and sugar
     end
   end

   class AddLiquidTask < Task
     def initialize
       super('Add liquid')
     end

     def get_time_required
       1.0
     end
   end

   class MixTask < Task
     def initialize
       super('Mix that batter up!')
     end

     def get_time_required
       3.0             # Mix for 3 minutes
     end
   end
   ```

3. Third, we need at least one higher-level class, which the GoF call the **composite** class

   创建高一级的类, 这个类跟最底层的类就不太一样了

   ```ruby
   class MakeBatterTask < Task
     def initialize
       super('Make batter')
       @sub_tasks = []
       add_sub_task( AddDryIngredientsTask.new )
       add_sub_task( AddLiquidsTask.new )
       add_sub_task( MixTask.new )
     end

     def add_sub_task(task)
       @sub_tasks << task
     end

     def remove_sub_task(task)
       @sub_tasks.delete(task)
     end

     def get_time_required
       time=0.0
       @sub_tasks.each {|task| time += task.get_time_required}
       time
     end
   end
   ```

   这里我们需要用到策略设计模式, 把添加删除子任务的功能独立出来, 优化如下:

   Because we will have a number of composite tasks in our baking example (pack- aging the cake as well as the master task of manufacturing the cake), it makes sense to factor out the details of managing the child tasks into another base class:

   ```ruby
   class CompositeTask < Task
     def initialize(name)
       super(name)
       @sub_tasks = []
     end

     def add_sub_task(task)
       @sub_tasks << task
     end

     def remove_sub_task(task)
       @sub_tasks.delete(task)
     end

     def get_time_required
       time=0.0
       @sub_tasks.each {|task| time += task.get_time_required}
       time
     end
   end
   ```

   Our MakeBatterTask then reduces to the following code:

   ```ruby
   class MakeBatterTask < CompositeTask
     def initialize
       super('Make batter')
       add_sub_task( AddDryIngredientsTask.new )
       add_sub_task( AddLiquidsTask.new )
       add_sub_task( MixTask.new )
     end
   end
   ```

   The key point to keep in mind about composite objects is that the tree may be arbitrarily deep.

   Any one of the subtasks of MakeCakeTask might be a composite.

组合设计模式在面对这种层级结构时是利器, 他主要的目的是让层级结构的所有节点都是一样的, 但是又能保证层级结构. 在现实世界中这种层级结构是如此普遍, 所以组合设计模式也很通用, 而且有的设计模式其实就是组合设计模式的变种.
