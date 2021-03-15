---
layout:     post
title:      " Factory design pattern in Ruby工厂设计模式"
subtitle:   ""
date:       2020-01-03
categories: Program
tags:
    - Design Pattern
---

假设我们有一个模拟鸭子的类:

```ruby
class Duck
  def initialize(name)
    @name = name
  end

  def eat
    puts("Duck #{@name} is eatings.")
  end

  def speak
    puts("Duck #{@name} says Quack!")
  end

  def sleep
    puts("Duck #{@name} sleeps quitely.")
  end
end
```

还有一个模拟鸭子在池塘里生活的类:

```ruby
class Pond
  def initialize(number_ducks)
    @ducks = []
    number_ducks.times do |i|
      duck = Duck.new("Duck#{i}")
      @ducks << duck
    end
  end

  def simulate_one_day
    @ducks.each {|duck| duck.speak}
    @ducks.each {|duck| duck.eat}
    @ducks.each {|duck| duck.sleep}
  end
end

pond = Pond.new(3)
pond.simulate_one_day
```

很完美, 知道有一天, 有新的需求, 我们还要模拟在池塘里生活的青蛙, 青蛙的类和鸭子类似:

```ruby
class Frog
  def initialize(name)
    @name = name
  end

  def eat
    puts("Frog #{@name} is eatings.")
  end

  def speak
    puts("Frog #{@name} says Crooooaaaak!")
  end

  def sleep
    puts("Frog #{@name} doesn't sleep; he crosks all night!")
  end
end
```

那么怎么模拟青蛙在池塘生活呢? 修改Pond类吗? Pond类要兼容两者, 我们可以用Template模板设计模式来做, Pond改成一个基类, 然后创建两个子类, 如下所示:

```ruby
class Pond
  def initialize(number_animals)
    @animals = []
    number_animals.times do |i|
      animal = new_animal("Animal#{i}")
      @animals << animal
    end
  end

  def simulate_one_day
    @animals.each {|animal| animal.speak}
    @animals.each {|animal| animal.eat}
    @animals.each {|animal| animal.sleep}
  end
end

class DuckPond < Pond
  def new_animal(name)
    Duck.new(name)
  end
end

class FrogPond < Pond
  def new_animal(name)
    Frog.new(name)
  end
end

pond = FrogPond.new(3)
pond.simulate_one_day
```

我们用这张图老说明工厂模式:

creator就是Pond class, DuckPond和FrogPond就是ConcreteCreator, Duck class和Frog Class就是products, 他们有一个基类(这里需要说明一下,  虽然两者没有显式的继承同一个基类, 但是两者都有同样的方法集, 可以视为同样的类)

看到这里, 我们有个疑问, 这和Template模板设计模式有什么区别呢? 工厂设计模式只是把创建实例作为独立出来的方法放在子类中了, 其他和模板设计模式一样. 没有这么简单.

假设又有其他需求, 池塘里面还有植物生长......

```ruby
class Algae
  def initialize(name)
    @name = name
  end

  def grow
    puts("The Algae #{@name} soaks up the sun and grows")
  end
end

def WaterLilly
  def initialize(name)
    @name = name
  end

  def grow
    puts("The water lily #{@name} floats, soaks up the sun, and grows")
  end
end
```

假设在池塘里又有植物又有动物, 那么我们按照上面的创建子类的方式来做:

```ruby
class Pond
  def initialize(number_animals, number_plants)
    @animals = []
    number_animals.times do |i|
      animal = new_animal("Animal#{i}")
      @animals << animal
    end

    @plants = []
    number_plants.times do |i|
      plant = new_plant("Plant#{i}")
      @plants << plant
    end
  end

  def simulate_one_day
    @plants.each {|plant| plant.grow}
    @animals.each {|animal| animal.speak}
    @animals.each {|animal| animal.eat}
    @animals.each {|animal| animal.sleep}
  end
end

class DuckWaterLilyPond < Pond
  def new_animal(name)
    Duck.new(name)
  end

  def new_plant(name)
    WaterLilly.new(name)
  end
end

class FrogAlgaePond < Pond
  def new_animal(name)
    Frog.new(name)
  end

  def new_plant(name)
    Algae.new(name)
  end
end

pond = DuckWaterLilyPond.new(3, 4)
pond.simulate_one_day
pond = FrogAlgaePond.new(3, 4)
pond.simulate_one_day
```

我们可以把创建实例的两个方法用参数化的方式统一成一个方法, 就变成:

```ruby
class Pond
  def initialize(number_animals, number_plants)
    @animals = []
    number_animals.times do |i|
      animal = new_organism(:animal, "Animal#{i}")
      @animals << animal
    end

    @plants = []
    number_plants.times do |i|
      plant = new_organism(:plant, "Plant#{i}")
      @plants << plant
    end
  end

  def simulate_one_day
    @plants.each {|plant| plant.grow}
    @animals.each {|animal| animal.speak}
    @animals.each {|animal| animal.eat}
    @animals.each {|animal| animal.sleep}
  end
end

class DuckWaterLilyPond < Pond
  def new_organism(type, name)
    if type == :animal
      Duck.new(name)
    elsif type == :plant
      WaterLilly.new(name)
    else
      raise "Unknown organism type: #{type}"
    end
  end
end

class FrogAlgaePond < Pond
  def new_organism(type, name)
    if type == :animal
      Frog.new(name)
    elsif type == :plant
      Algae.new(name)
    else
      raise "Unknown organism type: #{type}"
    end
  end
end

pond = DuckWaterLilyPond.new(3, 4)
pond.simulate_one_day
pond = FrogAlgaePond.new(3, 4)
pond.simulate_one_day
```

在Ruby里class也是对象, 也可以作为参数, 那么我们可以把上面的代码简化为:

```ruby
class Pond
  def initialize(number_animals, animal_class,
                 number_plants, plant_class)
    @animal_class = animal_class
    @plant_class = plant_class

    @animals = []
    number_animals.times do |i|
      animal = new_organism(:animal, "Animal#{i}")
      @animals << animal
    end

    @plants = []
    number_plants.times do |i|
      plant = new_organism(:plant, "Plant#{i}")
      @plants << plant
    end
  end

  def simulate_one_day
    @plants.each {|plant| plant.grow}
    @animals.each {|animal| animal.speak}
    @animals.each {|animal| animal.eat}
    @animals.each {|animal| animal.sleep}
  end

  def new_organism(type, name)
    if type == :animal
      @animal_class.new(name)
    elsif type == :plant
      @plant_class.new(name)
    else
      raise "Unknown organism type: #{type}"
    end
  end
end

pond = Pond.new(3, Duck, 4, WaterLilly)
pond.simulate_one_day
pond = Pond.new(3, Frog, 4, Algae)
pond.simulate_one_day
```

我们能不能进一步简化, 将两个生物类统一在一起呢:

```ruby
class Pond
  def initialize(number_animals, number_plants, organism_factory)
    @organism_factory = organism_factory

    @animals = []
    number_animals.times do |i|
      animal = @organism_factory.new_animal("Animal#{i}")
      @animals << animal
    end

    @plants = []
    number_plants.times do |i|
      plant = @organism_factory.new_plant("Plant#{i}")
      @plants << plant
    end
  end

  def simulate_one_day
    @plants.each {|plant| plant.grow}
    @animals.each {|animal| animal.speak}
    @animals.each {|animal| animal.eat}
    @animals.each {|animal| animal.sleep}
  end

end

class OrganismFactory
  def initialize(plant_class, animal_class)
    @plant_class = plant_class
    @animal_class = animal_class
  end

  def new_animal(name)
    @animal_class.new(name)
  end

  def new_plant(name)
    @plant_class.new(name)
  end
end

waterlilly_duck_factory = OrganismFactory.new(WaterLilly, Duck)
pond = Pond.new(3, 4, waterlilly_duck_factory)
pond.simulate_one_day
```

好了, 我们已经说的够多了, 这就是工厂模式.

我们需要注意的是, 不要滥用, 如果只是很简单的需求, 很少的类, 那么后面的那些“优化”都是多余的.
