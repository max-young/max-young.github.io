---
layout:     post
title:      "Discrete Mathematics with Application"
subtitle:   ""
date:       2021-03-11 00:00:00
author:     "alvy"
header-img: "img/post-bg-database1.jpg"
header-mask: 0.3
catalog:    true
tags:
    - Math
    - Algorithm
---

## Discrete Mathematics with Application

![](https://img3.doubanio.com/view/subject/l/public/s11240220.jpg)

<!-- TOC -->

- [Discrete Mathematics with Application](#discrete-mathematics-with-application)
    - [Preface](#preface)
    - [Chapter1 Speaking Mathematically](#chapter1-speaking-mathematically)
        - [Variables](#variables)
        - [The Language of Sets](#the-language-of-sets)
        - [The language of Relations and Functions](#the-language-of-relations-and-functions)
    - [Chapter2 The logic of compound statements](#chapter2-the-logic-of-compound-statements)
        - [Logical Form and Logical Equivalence](#logical-form-and-logical-equivalence)
        - [Conditional Statements](#conditional-statements)
        - [Valid and Invalid Arguments](#valid-and-invalid-arguments)
        - [Application: Digital Logic Circuits](#application-digital-logic-circuits)
        - [Application: Number Systems and Circuits for Addition](#application-number-systems-and-circuits-for-addition)
    - [Chapter3 The Logic of Quantified Statements](#chapter3-the-logic-of-quantified-statements)
        - [Predicates and Quantified Statements I](#predicates-and-quantified-statements-i)
        - [Predicates and Quantified Statements II](#predicates-and-quantified-statements-ii)
        - [Statements with Multiple Quantifiers](#statements-with-multiple-quantifiers)
    - [Chapter4 ELEMENTARY NUMBER THEORY AND METHODS OF PROOF](#chapter4-elementary-number-theory-and-methods-of-proof)
        - [Direct Proof and Counterexample I: Introduction](#direct-proof-and-counterexample-i-introduction)
        - [Applications: Algorithms](#applications-algorithms)
    - [Chapter5 SEQUENCES, MATHMATICAL INDUCTION, AND RECURSION](#chapter5-sequences-mathmatical-induction-and-recursion)
        - [Sequences](#sequences)
        - [Application: Correctness of Algorithms](#application-correctness-of-algorithms)
        - [General Recursive Definitions and Structural Induction](#general-recursive-definitions-and-structural-induction)
    - [Chapter 6 SET THEORY](#chapter-6-set-theory)
        - [Set Theory: Definition and the Element Method of Proof](#set-theory-definition-and-the-element-method-of-proof)
        - [Boolean Algebras, Russell's Paradox, and the Halting Problem](#boolean-algebras-russells-paradox-and-the-halting-problem)
    - [Chapter 7 FUNCTIONS函数](#chapter-7-functions%E5%87%BD%E6%95%B0)
        - [Function Defined on General Sets](#function-defined-on-general-sets)
        - [Ont-to-One and Onto, Inverse Functions](#ont-to-one-and-onto-inverse-functions)
        - [Cardinality with Applications to Computability](#cardinality-with-applications-to-computability)
    - [Chapter 8 RELATIONS](#chapter-8-relations)
        - [Relation on Sets](#relation-on-sets)
        - [Reflexivity, Symmetry, and Transitivity自反性, 对称性, 传递性](#reflexivity-symmetry-and-transitivity%E8%87%AA%E5%8F%8D%E6%80%A7-%E5%AF%B9%E7%A7%B0%E6%80%A7-%E4%BC%A0%E9%80%92%E6%80%A7)
        - [Equivalence Relations](#equivalence-relations)
        - [Modular Arithmetic with Applications to Cryptopraphy模块化算法在密码学中的应用](#modular-arithmetic-with-applications-to-cryptopraphy%E6%A8%A1%E5%9D%97%E5%8C%96%E7%AE%97%E6%B3%95%E5%9C%A8%E5%AF%86%E7%A0%81%E5%AD%A6%E4%B8%AD%E7%9A%84%E5%BA%94%E7%94%A8)
        - [Partial Order Relations偏序关系](#partial-order-relations%E5%81%8F%E5%BA%8F%E5%85%B3%E7%B3%BB)
    - [Chapter 9 COUNTING AND PROBABILITY 计数和概率](#chapter-9-counting-and-probability-%E8%AE%A1%E6%95%B0%E5%92%8C%E6%A6%82%E7%8E%87)
        - [Introduction 介绍](#introduction-%E4%BB%8B%E7%BB%8D)
        - [Possibility Trees and the Multiplication Rule](#possibility-trees-and-the-multiplication-rule)
        - [Counting Elements of Disjoint Sets: The Addition Rule加法法则](#counting-elements-of-disjoint-sets-the-addition-rule%E5%8A%A0%E6%B3%95%E6%B3%95%E5%88%99)
        - [The Pigeonhole Principle鸽洞原理](#the-pigeonhole-principle%E9%B8%BD%E6%B4%9E%E5%8E%9F%E7%90%86)
    - [Chapter 10 GRAPHS AND TREES 图和树](#chapter-10-graphs-and-trees-%E5%9B%BE%E5%92%8C%E6%A0%91)
        - [Graphs: Definitions and Basic Properties 图](#graphs-definitions-and-basic-properties-%E5%9B%BE)
        - [Trails, Paths, and Circuits](#trails-paths-and-circuits)
        - [Trees 树](#trees-%E6%A0%91)
        - [Rooted Trees](#rooted-trees)
        - [Spanning Trees and Shortest Paths](#spanning-trees-and-shortest-paths)
    - [Chapter 11 ANALYSIS OF ALGORITHM EFFICIENCY](#chapter-11-analysis-of-algorithm-efficiency)
        - [Real-Valued Functions of a Real Variable and Their Graphs](#real-valued-functions-of-a-real-variable-and-their-graphs)
        - [$\mathcal{O}$-, $\Omega$-, and $\Theta$- Notations](#%5Cmathcalo--%5Comega--and-%5Ctheta--notations)
        - [Application: Analysis of Algorithm Efficiency](#application-analysis-of-algorithm-efficiency)
        - [Application: Alalysis of Algorithm Efficiency 2](#application-alalysis-of-algorithm-efficiency-2)
    - [Chapter 12: Regular Expressions and Finite-State Automata](#chapter-12-regular-expressions-and-finite-state-automata)

<!-- /TOC -->

### Preface

书的preface很重要啊, 之前找到这一本书[Discrete Mathematics: An Open Introduction](https://book.douban.com/subject/30421347/), 看到preface说适合准备去中学教书的学生, 不太适合准备去读研究生和从事计算机科学的人群, 于是找到了这本书.

从书的preface里能确定本书适合什么样的人群, 也能找到本书的大概内容和使用方法, 例如, 本书贴心的讲了哪些事核心章节, 哪些章节适合普通数学, 哪些章节适合计算科学, 根据不同的目的, 可以去选择重点去读, 本书是这样说的:

| Chapter | Core Sections      | Sections Containing Optional Mathematical Material | Sections Containing Optional Computer Science Applications |
| ------- | ------------------ | -------------------------------------------------- | ---------------------------------------------------------- |
| 1       | 1.1-1.2            |                                                    |                                                            |
| 2       | 2.1-2.3            | 2.5                                                | 2.4,2.5                                                    |
| 3       | 3.1-3.4            | 3.3                                                | 3.3                                                        |
| 4       | 4.1-4.4, 4.6       | 4.5,4.7                                            | 4.8                                                        |
| 5       | 5.1, 5.2, 5.6, 5.7 | 5.3,5.4,5.8                                        | 5.1,5.5,5.9                                                |
| 6       | 6.1                | 6.2-6.4                                            | 6.1,6.4                                                    |
| 7       | 7.1, 7.2           | 7.3,7.4                                            | 7.1,7.2,7.4                                                |
| 8       | 8.1-8.3            | 8.4,8.5                                            | 8.4,8.5                                                    |
| 9       | 9.1-9.4            | 9.5-9.9                                            | 9.3                                                        |
| 10      | 10.1, 10.5         | 10.2-10.4,10.6                                     | 10.1,10.2,10.5-10.7                                        |
| 11      | 11.1, 11.2         | 11.4                                               | 11.3,11.5                                                  |
| 12      | 12.1, 12.2         | 12.3                                               | 12.1-12.3                                                  |

对于程序员的我把重点放在第一列和第三列

### Chapter1 Speaking Mathematically

#### 1.1 Variables

**Variable变量**可以作为一个占位符, 在下面两种情况下用到:

1. 有想象有一个或多个值, 但是是未知的
2. 又一个集合里面的值满足某个特性, 但是你不想用集合里的某一个特定的值来表达

**Statement声明**

A **universal statement** asserts that a certain property is true for all elements in a set.

A **conditional statement** asserts that if one thing is true then some other thing alse has to be true.

Given a property that may or may not be true, an **existential statement** assert that there is at least one thing for which the property is true.

#### 1.2 The Language of Sets

The **axiom of extension** says that a set is completely determined by what its elements are—not the order in which they might be listed or the fact that some elements might be listed more than once.

集合set又里面的元素来定义, 与元素的顺序和元素出现的顺序无关.

set刻意由大括号$$\{...\}$$来表示. 有一些约定俗成的符号来表示特定的集合, 比如R表示所有real number, Z表示所有整数, Q表示所有有理数rational numbers.

如果我们用直线来表示R的话, 中间是0, 两边是正负real number, 这条直线是连续的continuous.

Z不是连续的, 因为各个整数之间是有距离的, 我们称之为discrete. Discrete Mathematics就是来源于continuous和discrete的数学对象的区别.

另外一种set的表示方法是**Set-Builder Notation**, $${x\in S|P(x)}$$, We may define a new set to be **the set of all elements** **x** **in** **S** **such that** **P(x)** **is true**. 

- Subsets

  $$A\subseteq B$$ Means that For all elements x, if $$x\in A$$ then $$x\in B$$

  $$A\nsubseteq B$$ means that there is at least one element x such that $$x\in A$$ and  $$x\notin B$$

- ordered pair

  $$(a, b)$$是ordered pair, 元素是有序的

   $$(a, b)=(c, d)$$ means that $$a = c$$ and $$b = d$$

- Cartesian product笛卡尔积

  set of all ordered pairs $$(a, b)$$, where a is in A and b is in B.

  $$A\times B = {(a, b)|a\in A\ and\ b\in B}$$

   有趣的一点是: $$R\times R$$表示笛卡尔平面( Cartesian plane)

#### 1.3 The language of Relations and Functions

- Relations

  Let *A* and *B* be sets. A **relation** **R** **from** **A** **to** **B** is a subset of *A* × *B*. Given an ordered pair (*x*, *y*) in *A*×*B*, **x** **is related to** **y** **by** **R**, written *x R y*, if, and only if, (*x*, *y*) is in *R*. The set *A* is called the domain of *R* and the set *B* is called its co-domain.

  $$(x, y)$$是A和B两个集合的笛卡尔积的元素, 且$$(x, y)$$满足定义的关系, 那么我们说$$x\ R\ \ y$$

​		举两个例子:

​		Let$$ A = \{1,2\}$$ and $$B = \{1,2,3\}$$ and define a relation *R* from *A* to *B* as follows: Given any $$(x,  y) \in A \times  B$$

​						$$(x, y) \in R\ means\ that\ \frac{x - y}{2}\ is\ an\ integer$$.

​        再举一个Circle Relation的例子, 我们可以用Relation表示一个圆, 很神奇

​		Define a relation C from R to R as follows: For any$$(x, y)\in R\times R$$,

​						$$(x, y)\in C\ means\ that\ x^2 + y^2 = 1$$

- Functions

  A **function** **F** **from a set** **A** **to a set** **B** is a relation with domain *A* and co-domain *B*

  that satisfies the following two properties:

  1. For every element *x* in *A*, there is an element *y* in *B* such that$$(x, y)\in F$$.
  2. For all elements x in A and y and z in B, if $$(x, y)\in  F$$ and $$(x, z)\in F$$, then  y = z.

  也就是说对于A中的所有元素, 都有B中的一个元素满足function.

### Chapter2 The logic of compound statements

#### 2.1 Logical Form and Logical Equivalence

在此书中用~代表not, $$\lor$$代表or, $$\land$$代表and

- De Morgan's Laws

  The negation if an and statement is logically equicalent to the or statement in which each component is negated.

  The negation of an or statement is logically equivalent to the and statement in which each component is negated.

  也就是说:

  $$\lnot (p\land q) \equiv \lnot p \lor \lnot q$$

  $$\lnot (p\lor q) \equiv \lnot p \land \lnot q$$

- Tautologies and Contradictions

  A tautology is a statement form that is always true regardless of the truth values of the individual statement substituted for its statement variables. A statement whose form is a tautology is a taotulogical statement.

  A contradiction is a statement form that is always false regardless of the truth values of the individual statement substituted for its statment variables. A statement whose form is a contradictions is a contradictory statement.

  例如: $$p \lor \lnot p$$ 就是一个tautology, $$p \land \lnot p$$就是一个contradiction

  if t is a tautology and c is a contradiction, show that $$p \and t \equiv p$$ and $$p \and c \equiv c$$.

#### 2.2 Conditional Statements

- Conditional

  if *p* and *q* are statement variables, the conditional of *q* by *p* is **"If *p* then *q* "** or "*p* implies *q*" and is denoted $$p\to q$$ . It is false when *p* is true and *q* is false; otherwise it is true. We call *p* the hypothesis(or antecedent) of the conditional and *q* the conclusion(or consequent).

  True Table for $$p\to q$$

  | *p*  | *q*  | $$p\to q$$ |
  | :--: | :--: | :--------: |
  |  T   |  T   |     T      |
  |  T   |  F   |     F      |
  |  F   |  T   |     T      |
  |  F   |  F   |     T      |

​		这样我们能得出: $$p\to q \equiv \lnot p \or q$$

​		通俗的翻译是:

​		有这样一句话: 假如你做了某事A, 会得到某样东西B.

​		这句话的含义是, 你做了A, 肯定得到B, 如果你不做, 可能得到B也可能得不到B, 所以上面表格的意思就清楚了

- biconditional

  Given statement variable *p* and *q*, the biconditional of *p* and *q* is **"*p* if, and only if, *q*"** and is denoted $$p\iff q$$. It is true if both *p* and *q* have the same truth values and is false if *p* and *q* have opposite truth values. The words if and only if are sometimes abbreviated iff.

  True Table for $$p\iff q$$

  | *p*  | *q*  | $$p\iff q$$ |
  | :--: | :--: | :---------: |
  |  T   |  T   |      T      |
  |  T   |  F   |      F      |
  |  F   |  T   |      F      |
  |  F   |  F   |      T      |

​		通俗的翻译是:

​		有这样一句话: 假如你做了某事A, 会得到某样东西B.如果你不做A, 就得不到B. 所以上面表格的意思就清楚了

- Necessary and SufficientCOnditions

  If *r* and *s* are statements:

  ​	*r* is a sufficient condition for *s* means "if *r* then *s*."

  ​	*r* is a necessary condition for *s* means "if not *r* then not *s*."

  ​    *r* is a necessary condition for *s* also means "if *s* then *r*."

  ​	r is a necessary and sufficient condition for s means "r if, and only if, s."

#### 2.3 Valid and Invalid Arguments

An augument is a sequence of statements, nad an argument form is a sequence of statement forms. All statements in an argument and all statement forms in an argument form, except for the final one , are called **premise**(or assumptions or hypotheses). The final statement or statement form is called the **conclusion**. The symbol$$\therefore$$ , which is read "therefore", is normally placed just before the conclusion.

To say the argument form is **valid** means that no matter what particular statements are substituted for the statement variables in it's premises, if the resulting premises are all true, then the conclusion is also true. To say that argument is valid means that it's form is valid.
$$
p\to q \lor \neg r\\
q\to p \lor r\\
\therefore p \to r
$$

- Modus Ponens and Modus Tollens

  An argument form consisting of two premises and a conclusion is called a **syllogism**. The first and second premises are called the major premise and minor premise, respectively.

  The most famous form of syllogism in logic is called modus ponies. It has following form:
  $$
  If\ p\ then\ q. \\
  p \\
  \therefore q
  $$
  the term modus ponens is Ladin meaning "method of affirming"(the conclusion is an affirmation)

  modus tollens has the following form:
  $$
  If\ p \ then \ q. \\
  \neg q \\
  \therefore \neg p
  $$
  Modus tollens is Latin meaning "method of denying"

- Fallacies

  For an argument to be valid, every argument of the same form whose premises are all true must have a true conclusion. It follows that for an argument to be invalid means that there is an argument of that form whosr premises are all true and whose conclusion is false.

- Contradictions and Valid Arguments

  Contradiction Rule:

  If you can show that supposition that statement *p* is false leads logically to a contradiction, then you can conclude that *p* is true.
  $$
  \neg p \to c \\
  \therefore p
  $$
  

#### 2.4 Application: Digital Logic Circuits

 这一章的内容主要讲与非门, 在《[编码](https://book.douban.com/subject/4822685/)》这本书里有度过, 就不详细去读啦, 

#### 2.5 Application: Number Systems and Circuits for Addition

这一章也在《[编码](https://book.douban.com/subject/4822685/)》里看过, 主要讲二进制

### Chapter3 The Logic of Quantified Statements

#### 3.1 Predicates and Quantified Statements I

In grammar, the word *predicate* refers to the part of a sentence that gives information about the subject. In the sentence “James is a student at Bedford College,” the word *James* is the subject and the phrase *is a student at Bedford College* is the predicate. The predicate is the part of the sentence from which the subject has been removed.

- The Universal Quantifier: $$\forall$$

  One sure way to change predicates into statements is to assign specific values to all their variables. For example, if *x* represents the number 35, the sentence “*x* is (evenly) divis- ible by 5” is a true statement since 35 = 5·7. Another way to obtain statements from predicates is to add **quantifiers.** Quantifiers are words that refer to quantities such as “some” or “all” and tell for how many elements a given predicate is true

  The symbol ∀ denotes “for all” and is called the **universal quantifier.** For example, another way to express the sentence “All human beings are mortal” is to write

  ∀ human beings *x* , *x* is mortal.

- **The Existential Quantifier:** $$\exists$$

  The symbol ∃ denotes “there exists” and is called the **existential quantifier.** For example,

  the sentence “There is a student in Math 140” can be written as
   ∃ a person *p* such that *p* is a student in Math 140,

  or, more formally,

  ∃*p* ∈ *P* such that *p* is a student in Math 140,

  where *P* is the set of all people.

#### 3.2 Predicates and Quantified Statements II

- Negations of Quantified Statements

  Consider the statement “All mathematicians wear glasses.” Many people would say that its negation is “No mathematicians wear glasses,” but if even one mathematician does not wear glasses, then the sweeping statement that *all* mathematicians wear glasses is false. So a correct negation is “There is at least one mathematician who does not wear glasses.”

  **The negation of a universal statement (“all are”) is logically equivalent to an existential statement (“some are not” or “there is at least one that is not”).**

  **The negation of an existential statement (“some are”) is logically equivalent to a universal statement (“none are” or “all are not”).**

- Negations of Universal Conditional Statements

  ∼(∀*x*, *P*(*x*) → *Q*(*x*)) ≡ ∃*x* such that ∼(*P*(*x*) → *Q*(*x*))

  ∼(*P*(*x*) → *Q*(*x*)) ≡ *P*(*x*) ∧ ∼*Q*(*x*)

  ∼(∀*x*, *P*(*x*) → *Q*(*x*)) ≡ ∃*x* such that (*P*(*x*)∧ ∼*Q*(*x*))

#### 3.3 Statements with Multiple Quantifiers

many important technical statements contain both ∃ and ∀, a convention has developed for interpreting them uniformly. When a statement contains more than one quantifier, we imagine the actions suggested by the quantifiers as being performed in the order in which the quantifiers occur. For instance, consider a statement of the form

∀*x* in set *D*, ∃*y* in set *E* such that *x* and *y* satisfy property *P*(*x*, *y*)

- Negations of Multiply-Quantified Statements

  You can use the same rules to negate multiply-quantified statements that you used to negate simpler quantified statements. Recall that

  ∼(∀*x* in *D*, *P*(*x*)) ≡ ∃*x* in *D* such that ∼*P*(*x*).

  and

  ∼(∃*x* in *D* such that *P*(*x*)) ≡ ∀*x* in *D*,∼*P*(*x*).

   We apply these laws to find

  ∼(∀*x* in *D*,∃*y* in *E* such that *P*(*x*, *y*))

   by moving in stages from left to right along the sentence.

  First version of negation:* ∃*x* in *D* such that ∼(∃*y* in *E* such that *P*(*x*, *y*)).

   *Final version of negation:* ∃*x* in *D* such that ∀*y* in *E*, ∼*P*(*x*, *y*).

  Similarly, to find

  ∼(∃*x* in *D* such that ∀*y* in *E*, *P*(*x*, *y*)),

  we have

  ∼(∃*x* in *D* such that ∀*y* in *E*, *P*(*x*, *y*)),

  *First version of negation:* ∀*x* in *D*, ∼(∀*y* in *E*, *P*(*x*, *y*)).

  *Final version of negation:* ∀*x* in *D*, ∃*y* in *E* such that ∼*P*(*x*, *y*).

### Chapter4 ELEMENTARY NUMBER THEORY AND METHODS OF PROOF

基础数学理论和证明方法, 序言相当棒, 数学和逻辑的魅力展露无遗

#### 4.1 Direct Proof and Counterexample I: Introduction

- **Definitions**

  我们知道偶数是能被2整除, 奇数不能被2整除. 这是我们被“教育”的概念, 我们再来看看能够展现数学和逻辑的魅力的定义:

  An integer *n* is **even** if, and only if, *n* equals twice some integer. An integer *n* is **odd**

  if, and only if, *n* equals twice some integer plus 1.

  Symbolically, if *n* is an integer, then
  $$
  n\ is\ even \iff \exists\ an\ integer\ k\ such\ that\ n=2k\\
  n\ is\ odd \iff\ an\ integer\ k\ such\ that\ n=2k+1
  $$
  
- Proving Existential Statements

  ∃*x* ∈ *D* such that *Q*(*x*)

  我们要证明上面的statement, 我们可以在D集合里面找到一个元素, 来满足合格条件, 这种证明方法叫**constructive proofs of existence**

  或者我们通过理论证明D集合里面没有元素满足要求, 这种证明方法叫 **nonconstructive proof of existence**

- **Disproving Universal Statements by Counterexample**

  To disprove a statement of the form “∀*x* ∈ *D*, if *P*(*x*) then *Q*(*x*),” find a value of *x* in *D* for which the hypothesis *P*(*x*) is true and the conclusion *Q*(*x*) is false. Such an *x* is called a **counterexample.**

#### 4.8 Applications: Algorithms

- Division Algorithm

  如果我们不用计算机内置的除法, 怎么实现除法的算法呢?

  $$a=d \times q + r$$

  这里q是商数quotient, r是余数remainder, 我们要实现求得q和r的算法.

  余数r应该满足$$0\leq r < d$$ , 我们可以用a减去d, 一直减, 一直到剩下的值小于d, 最后, 减的次数就是q, 剩余的值就是r

  ```
  伪代码:
  Input: a[a nonnegative number], d[a positive number]
  Algorithm Body:
  q = 0, r = a
  a一只减b, 一直到r<d
  while (r>=d)
      r = r - d 
      q = q + 1
  end while
  while运行结束之后, a = b*q + r
  Output: q, r
  ```

- The Euclidean Algorithm

  求两个证书的最大公约数greatest common divisor, 最大公约数的定义是

  Let *a* and *b* be integers that are not both zero. The **greatest common divisor** of *a*

  and *b*, denoted **gcd**(**a**, **b**), is that integer *d* with the following properties: 

  1. *d* is a common divisor of both *a* and *b*. In other words,

  *d*|*a* and *d*|*b*.

  2. For all integers *c*, if *c* is a common divisor of both *a* and *b*, then *c* is less than or

  equal to *d*. In other words,

  for all integers*c*,if *c*|*a* and *c*|*b*,then*c* ≤ *d*.

  有两个推论:

  1. If *r* is a positive integer, then gcd(*r*, 0) = *r* .

  2. If *a* and *b* are any integers not both zero, and if *q* and *r* are any integers such that *a* = *bq* + *r*, then

     gcd(a, b) = gcd(b, r)
     $$
     a = b\times q + r\\
     假设c是a和b的最大公约数, 那么a=c\times m, b=c\times n\\
     c\times m = c\times n \times q + r\\
     r = c\times m - c\times n \times q\\
     r = (m - n\times q)\times c\\
     这样c也是r的约数, c是a和b的最大公约数, c又是b和r的约数, 那么c小于等于b和r的最大公约数.也就是:\\
     gcd(a, b) <= gcd(b, r)\\
     下面我们再来证明b和r的最大公约数小于等于a和b的最大公约数\\
     假设c是b和r的最大公约数, 那么b=c\times m, c=c\times n\\
     a = c\times m \times q + c\times n\\
     a = (m\times q + n)\times c\\
     这样c也是a的余数, c是b和r的最大公约数, c又是a和b的约数, 那么c小于等于a和b的最大公约数.也就是:\\
     gcd(b, r) <= gcd(a, b)\\
     从而得到gcb(a, b)=gcb(b, r)
     $$

  上面的证明对求两个正整数的最大公约数有什么关系呢? 

  如果没有上面的证明, 我们大概想到的方法就是穷举Exhaustion, 从2一直循环到最小的那个数, 对于数量较小的两个数还可行, 如果数字足够大, 那将相当耗费资源.

  如果我们利用上面的证明, 就能大幅提高计算速度.

  ```
  伪代码
  Input: A, B[integers with A > B >= 0]
  Algorithm Body:
      a = A, b = B
      如果b != 0, 计算a mod b, 得到余数r, 替换a=b, b=r. 重复这个过程
    while(b != 0):
          r = a mod b
          a = b
          b = r
      end while
      gcd = a
  Output: gcd
  ```

### Chapter5 SEQUENCES, MATHMATICAL INDUCTION, AND RECURSION

#### 5.1 Sequences

- sequence

  sequence的定义有一些奇怪: A **sequence** is a function whose domain is either all the integers between two given integers or all the integers greater than or equal to a given integer.

- Summation Notation

  有这样的一个sequence, $$A_k = 2^k$$, 我们要求前六个term的求和:

  $$A_1 + A_2 + A_3 + A_4 + A_5 + A_6 = 2^1 + 2^2 + 2^3 + 2^4 + 2^5 + 2^6 = 126$$

  有没有更简单的表示呢?

  if m and n are integers and $$m\leq n$$, the symbol $$\sum\limits_{k=m}^{n} a_k$$, read the summation from k equals m to n of a-sub-k, is the sum of all the terms $$a_m, a_{m+1}, a_{m+2}, ..., a_n$$. we say that $$a_m + a_{m+1} + a_{m+2} + ... + a_n$$ is the expand form of the sum, and we write:

  $$\sum\limits_{k=m}^na_k = a_m + a_{m+1} + a+{m+2} + ... + a_n$$

  we call k the index of the summation, m the lower limit of the summation, and n the upper limit of the summation.

- Product Notaion

  if m and n are integers and $$m\leq n$$, the symbol $$\prod\limits_{k=m}^n a_k$$(注释: 此处latex limits不起作用), read the product from k equals m to n of a-sub-k, is the product if all terms $$a_m, a_{m+1, a_{m+2}, ... , a_n}$$, we write:

  $$\prod\limits_{k=m}^n a_k = a_m.a_{m+1}.a_{m+2}...a_n $$

- Properties of Summations and Products

  if $$a_m, a_{m+1}, a_{m+2}, ...$$ and $$b_m, b_{m+1}, b_{m+2}, ...$$ are sequemces of real numbers and c is any real number, then the following equations hold for any integer $$n\geq m$$:

  1. $$\sum\limits_{k=m}^n a_k + \sum\limits_{k=m}^n b^k = \sum\limits_{k=m}^n (a_k+b_k)$$
  2. $$c.\sum\limits_{k=m}^n a_k = \sum\limits_{k=m}^n c.a_k$$
  3. $$\left( \prod\limits_{k=m}^n a_k \right) .\left(\prod\limits_{k=m}^n b_k\right) = \prod\limits_{k=m}^n (a_k.b_k)$$

- Factorial and "n choose r" Notation

  for each positive integer n , the quantity a factorial denoted $$n!$$, is defined to be the product of all the integers fro 1 to n:

  $$n! = a.(n-1)...3.2.1$$

  Zero factorial, denoted 0!, is defined to be 1:

  $$0! = 1$$

  Let n and r be integers with $$0\leq r \leq n$$. the symbol

  $${n \choose r}$$

  is read "n choose r" and represents the number of subsets of size r that can be chosen from a set with n elements.

  fro all integers n and r with $$0\leq r \leq n$$

  $${n \choose r} = \frac{n!}{r!(n-r)!} $$

- Sequence in computer programming

  计算机里用到的最多的是一位数组one-dimensional array

- Application: Algorithm to Convert from Base 10 to Base 2 Using Repeated Division by 2
  $$
  38 = 19.2 + 0 \\
  19 = 9.2 + 1 \\
  9 = 4.2 + 1 \\
  4 = 2.2 + 0 \\
  2 = 1.2 + 0 \\
  1 = 0.2 + 1
  $$
  
  $$
  38 = 19·2+0 \\
  = (9·2+1)·2+0 \\
  = 9·2^2 +1·2+0 \\
  = (4·2+1)·2^2 +1·2+0 \\
  = 4·2^3 +1·2^2 +1·2+0 \\
  = (2·2+0)·2^3 +1·2^2 +1·2+0 \\
  = 2·2^4 +0·2^3 +1·2^2 +1·2+0 \\
  = (1·2+0)·2^4 +0·2^3 +1·2^2 +1·2+0 \\
  = 1·2^5 +0·2^4 +0·2^3 +1·2^2 +1·2+0.
  $$

​	

​	$$a_{10} = (r[k]r[k-1]...r[2]r[1])_2$$

```
Algorithm Decimal to Binary Conversion Using Repeated Division by 2
Input: n[a nonnegtive integer]
Algorithm Body:
	q = n, i = 0
  q一直除以2知道q变成0, 存储remainder余数到一个一维数组
  while(i = 0 or q != 0)
  	r[i] = q mod 2
  	q = q div 2
  	i = i + 1
  end while 
Ouptput: r[0], r[1], ..., r[i-1]
```

#### 5.5 Application: Correctness of Algorithms

In this section we given an overview of the general format of correctness proofs and the details of one crucial technique, the *loop invariant procedure*

- Assertions

  Often the predicate describing the initial state is called **pre-condition for the algorithm**, and the predicate describing the final state is called the **post-condition for the algorithm**

  Example:

  Algorithm to compute a product if nonnegtive integers

  *Pre-condition*: The input variables *m* and *n* are nonnegative integers

  *Post-condition*: The output variable *p* equals m.n

- Loop invariants

  非常严谨的证明loop的方法, 无法描述, 看书吧

#### 5.9 General Recursive Definitions and Structural Induction

- Recursively Defined Sets

  定义方法是:

  1. BASE: A statement that certain objects belong to the set
  2. RECURSION: A collection of rules indicating how to form new set objects from those already known to be the set
  3. RESTRICTION: A statement that no objects belong to the set other than those coming from 1 and 2

-  Proving Properties about Recursively Defined Sets

  structural induction可证明

- Recursive Functions

### Chapter 6 SET THEORY

#### 6.1 Set Theory: Definition and the Element Method of Proof

If S is a set and P(x) is a property that element of S may or may not satisfy, then a set A may be defined by writing:

$$A = \{ x \in S | P(x) \}$$

which is read "The set of all x in S such that P of x"

- Subsets

  $$A \subseteq B \iff \forall x,\ if\ x \in A\ then\ x \in B$$

  $$A \not\subseteq B \iff \exists x,\ x \in A\ and\ x \notin B $$
  $$
  \begin{align*}
  &A\ is\  proper\ subset\ of\ B \iff \\
  &(1) A \subseteq B, and\\
  &(2) there\ is\ at\ least\ one\ element\ in\ B\ that\ is\ not\ in\ A.
  \end{align*}
  $$
  
- Set Equality

  $$A = B \iff A \subseteq B\ and\ B \subseteq A$$

- Operations on Sets

  the set of real numbers would be called a **universal set** or a **universe of discourse**

  Let A and B be sbubsets of a universal set U.

  1. The **uninon** of A and B, denoted $$A \cup B $$, is the set of all elements that are in at least one of A or B.
  2. The **intersection** of A and B, denoted $$A \cap B$$, is the set of all elements that are common to both A and B.
  3. The **difference** of B minus A (or **relative complement** of A in B), denoted $$B - A$$, is the set of all elements that are in B and not A.
  4. The **complement** of A, denoted $$ A^{c}  $$ , is the set of all elements in U that are not in A.

  Symbolically:
  $$
  \begin{align*}
  A \cup B &= \{x \in U | x \in A \ or\ x \in B\} \\
  A \cap B &= \{x \in U | x \in A \ and\ x \in B\} \\
  B - A &= \{x \in U | x \in B \ and\ x \notin A \} \\
  A^{c} &= \{x \in U | x \notin A \}
  \end{align*}
  $$
  
- The empty Set

  We call it the **empty set** (or **null set**) and denote it by the symbol $$\emptyset$$ . Thus $$\{1, 3\} \cap \{2, 4\} = \emptyset$$ and $$\{x \in R | x^2 = -1\} = \emptyset$$

- Partition of Sets

  Two sets are called **disjoint** if, and only if, they have no elements in common. Symbolically: 
  $$
  A\ and\ B\ are\ disjoint \iff A \cap B = \emptyset
  $$
  
- Power Set

  Given a set A, the **power set** of A, denoted $$\mathcal{P}(A)$$, is the set of all sub sets of A
  $$
  \mathcal{P}(\{x, y\}) = \{\emptyset, \{x\}, \{y\}, \{x, y\}\}
  $$
  
- Cartesian Products

  笛卡尔积

  Given sets $$A_1, A_2, ..., A_n$$, the **Cartesian product** of $$A_1, A_2, ..., A_n$$ denoted $$A_1 \times A_2 \times ... \times A_n$$, is the set of all ordered n-tuples $$(a_1, a_2, ..., a_n)$$ where $$a_1 \in A_1, a_2 \in A_2, ..., a_n \in A_n$$. 

  Symbolically: 
  $$
  A_1 \times A_2 \times ... \times A_n = \{(a_1, a_2, ..., a_n | a_1 \in A_1, a_2 \in A_2, ..., a_n \in A_n \}
  $$
  
  
  In particular,
  $$
  A_1 \times A_2 = \{(a_1, a_2) | a_1 \in A_1\ and\ a_2 \in A_2\}
  $$
  is the Cartesian product if $$A_1$$ and $$A_2$$.

#### 6.4 Boolean Algebras, Russell's Paradox, and the Halting Problem

- Boolean Algebras

  不太能理解

- Russell's Paradox

  很有趣的一个Paradox:

  In a certain town there is a male barber who shaves all those men, and only those men, who do not shave themselves. *Question:* Does the barber shave himself?

- The Halting problem

  太抽象, 看不懂. 大概是说计算机算法不会得出halting或者永远循环的输出. 和上面的悖论相关.

### Chapter 7 FUNCTIONS函数

#### 7.1 Function Defined on General Sets

- 定义

   一个函数$$f$$表示一个集合$$X$$到集合$$Y$$的关系, 表示为: $$f:X \to Y$$ , 必须满足$$X$$中的每一个元素都与$$Y$$中的某一个元素有关系. 

- 函数相等

  如果两个函数$$F:X \to Y$$和$$G: X \to Y$$, 如果$$F = G$$, 则所有$$x \in X$$都满足$$F(x) = G(x)$$

- 布尔函数Boolean Function

  有意思, 但是不清楚可以用在什么地方

#### 7.2 Ont-to-One and Onto, Inverse Functions

- One-to-One Functions一对一函数

  $$F$$是一个表示集合$$X$$到集合$$Y$$的函数, 如果说$$F$$是一个Ont-to-One函数, 那么它必须满足条件:

  如果$$F(x_{1}) = F(x_{2})$$, 那么$$x_{1} = x_{2}$$

  或者说如果$$x_{1} \neq x_{2}$$, 那么$$F(x_{1}) \neq F(x_{2})$$

  用符号可以表示为:

  $$F: X \to Y\ is\ one-to-one\ \iff \forall x_{1}, x_{2} \in X, if\ F(x_{1}) = F(x_{2})\ then\ x_{1} = x_{2}$$

- Application: Hash Functions

- Onto Functions

  $$F$$是一个表示集合$$X$$到集合$$Y$$的函数, 如果说$$F$$是一个onto函数, 那么集合$$Y$$中的所有元素, 都能在$$X$$中找到一个元素$$x$$满足$$F(x) = y$$

  用符号可以表示为:

  $$F: X \to Y\ is\ onto \iff \forall y \in\ Y, \exists x\ in\ X\ such\ that\ F(x) = y$$ 

- Inverse Functions

  $$F(x) = y$$反过来怎么表示呢? $$F^{-1}(y) = x$$

#### 7.4 Cardinality with Applications to Computability

*cardinal number* 表示一个集合set的大小("This set has *eight* elements"), *ordinal number*表示集合的元素顺序("This is the *right* element in the row")

Let *A* and *B* be any sets. **A** **has the same cardinality as** **B** if, and only if, there is a one-to-one correspondence from *A* to *B*. In other words, *A* has the same cardinality as *B* if, and only if, there is a function *f* from *A* to *B* that is one-to-one and onto.

后面的内容很理论, 看不懂, 略过

### Chapter 8 RELATIONS

#### 8.1 Relation on Sets

最后讲数据库很形象

#### 8.2 Reflexivity, Symmetry, and Transitivity自反性, 对称性, 传递性

书中用了这样的一个Relation做例子:

$$A=\{2, 3, 4, 6, 7, 9\}$$, for all $$x, y \in A$$,

$$x\ R\ y \iff 3|(x-y)$$

备注: $$3|(x-y)$$表示$$x-y$$能被3整除

这里能根据Relation画出图来, 看书吧

我们定义出Relation的3种特性::

1. Reflexive: $$R$$ is reflexive if, and only if, for all $$x \in A, x\ R\ x$$
2. symmetric: $$R$$ is symmetric if, and only if, for all $$x, y \in A, if\ x\ R\ y\ then\ y\ R\ x$$
3. Transitive: $$R$$ is transitive if, and only if, for all $$x, y, z \in A, if\ x\ R\ y\ and\ y\ R\ z\ then\ x\ R\ z$$

#### 8.3 Equivalence Relations

Let *A* be a set and *R* a relation on *A*. *R* is an **equivalence relation** if, and only if, *R*

is reflexive, symmetric, and transitive.

#### 8.4 Modular Arithmetic with Applications to Cryptopraphy模块化算法在密码学中的应用

#### 8.5 Partial Order Relations偏序关系

### Chapter 9 COUNTING AND PROBABILITY 计数和概率

#### 9.1 Introduction 介绍

sanple space: 样本空间

A sample space is the set of all possible outcomes of a random process or experiment.
An event is a subset of a sample space.

Equally Likely Probability Formula: 均等概率公式

#### 9.2 Possibility Trees and the Multiplication Rule

用可能树和乘法规则是计算规律的好方法

#### 9.3 Counting Elements of Disjoint Sets: The Addition Rule加法法则

例如, 密码是26个字母的组合, 长度是1位到3位, 那么密码的可能是1位、2位、3位三种可能性之和

#### 9.4 The Pigeonhole Principle鸽洞原理

5只鸽子飞往4个洞, 那么至少有一个洞有2个或2个以上鸽子, 好像是显而易见的哈. 用术语表达就是:

Pigeonhole Principle:  A function from one finite set to a smaller finite set cannot be one-to-one: There must be a least two elements in the domain that have the same image in the co-domain.

### Chapter 10 GRAPHS AND TREES 图和树

#### 10.1 Graphs: Definitions and Basic Properties 图

A **graph** G consists of  two finite sets: a nonempty set V(G) of **vertices**(顶点) and a set E(G) of **edges**(边), where each edge is associated with a set consisting of either one or two vertices called it‘s **endpoints**. The correspondence from edges to endpoints is called the **edge-endpoint function**.

An edge with just one endpoint is called a **loop**, and two or more distinct edges with the same set of endpoints are said to be **parallel**. An edge is said to connect it‘s endpoints; two vertices that are connected by an edge are called **adjacent**; and a vertex that is an endpoint of a loop is said to be adjacent to itself. 

An edge is said to be **incident** on each of it's endpoints, and two edges incident on the same endpoint are called adjacent. A vertex on which no edges are incident is called **isolated**.

#### 10.2 Trails, Paths, and Circuits

案例和定义很有趣

G是一个Graph, v、w是两个顶点

从v到w:

如果没有重复的边, 则叫**trail**

没有重复的顶点, 则叫**path**

如果v和w是同一个点, 则叫**closed walk**

一个closed walk, 如果至少包括一条边, 且不重复, 则是**circuit**

一个circuit, 除了起点和终点重复, 没有其他的重复的顶点, 则称为**simple curcuit**

#### 10.5 Trees 树

树其实是一种特殊的图

A graph is said to be circuit-free if, and only if, it has no circuits. A graph is called a tree if, and only if, it is circuit-free and connected. A trivial tree is a graph that consists of a single vertex. A graph is called a forest if, and only if, it is circuit-free and not connected.

#### 10.6 Rooted Trees

#### 10.7 Spanning Trees and Shortest Paths

### Chapter 11 ANALYSIS OF ALGORITHM EFFICIENCY

#### 11.1 Real-Valued Functions of a Real Variable and Their Graphs

- 笛卡尔平面坐标系

Let $$f$$ be a real-valued function of a real variable. The graph of $$f$$ is the set of all points (x, y) in the Cartesian coordinate plane with the property that $$x$$ is in the domain of $$f$$ and $$y= f(x)$$.

- power functions幂函数

Let $$a$$ be any nonnegative real number. Define $$p_a$$, the power function with exponent a, as follows:
$$p_a(x) = x^a$$ for each nonnegative real number x.

- Increasing and Decreasing Functions

  $x_1 < x_2, f(x_1) < f(x_2)$ Then increasing function

  $x_1 < x_2, f(x_1) > f(x_2)$ Then descreasing function

#### 11.2 $\mathcal{O}$-, $\Omega$-, and $\Theta$- Notations

同一项工作用不同的算法需要的时间和空间是不一样的, 这三个符号就可以来表示这种差别

#### 11.3 Application: Analysis of Algorithm Efficiency 

- The Sequential Search Algorithm 顺序查找算法

  很简单, 从第一个元素开始一次查找

- The Insertion Sort Algorithm 插入排序算法

  将一组数字按升序排列, 最开始, 用第2个元素和第1个元素比较, 如果小于第1个元素, 则交换.

  基本的思想, 是依次将元素放到左边序列里的正确的位置.

- Time Efficiency of an Algorithm 算法的时间效率

  Roughly speaking, the analysis of an algorithm for time efficiency begins by try- ing to count the number of elementary operations that must be performed when the algorithm is executed with an input of size *n* (in the best case, worst case, or average case).

  粗略的说, 分析一个算法的时间效率, 我们可以对大小为n的输入的情况下, 必须执行的操作数来作为开始.

  我们以一个简单的例子来做说明:
  $$
  \begin{align*}
  &p:=0, x:=2 \\
  &for\ i:=2\ to\ n \\
  &\ \ \ \ p := (p+i).x \\
  &next\ i
  \end{align*}
  $$
  这里是一个循环, 每一个循环里面会做一次加法和一次乘法, 循环的次数是n-2+1, 所以执行的操作数是:
  
  $$2*(n-2+1)=2n-2$$
  
  $$2n-2$$可能大于n, 也可能小于n, 所以这个算法的效率可以表示为$$\Theta(n)$$
  
- **The Insertion Sort Algorithm插入算法详解**

  强烈建议看看此算法, 算法的原理是**挪动位置**

- 插入算法的最差效率

  那就是a[k]前面的数字都小于a[k], 那么

#### 11.5 Application: Alalysis of Algorithm Efficiency 2

divide and conquer分而治之

采用此策略, 我们可以得出binary search算法, 来和11.3的sequential search算法做比较

已经merge sort算法和11.3的insert sort算法做比较

看效率是否提高

- Binary Search

  看书中的定义, 很清晰, 注意算法定义了3个变量: index = 0, bot = 1, top = n

- Merge Sort

  不太直观, 有点烧脑. 看Python的写法吧.

### Chapter 12: Regular Expressions and Finite-State Automata

正则表达式、有限状态机......应用到的时候再看吧