---
layout: post
title: "Pandas common skills"
subtitle: ""
date: 2023-01-04
categories: Python
tags:
  - Python
  - Pandas
---

- [根据已有 column 创建 column](#根据已有-column-创建-column)
- [删除列](#删除列)
- [筛选](#筛选)
- [map default value](#map-default-value)

#### 根据已有 column 创建 column

```python
dataframe["new_column"] = dataframe.apply(
    lambda row: row.exist_column * 2, axis=1)
```

#### 删除列

```python
df.drop('column_name', axis=1, inplace=True)
```

inplace 代表修改 df, 不用重新创建一个变量

删除多列

```python
df.drop(['column_nameA', 'column_nameB'], axis=1, inplace=True)
```

#### 筛选

```python
 df[df['A'].isin([3, 6])]
```

#### map default value

we can use map to update dataframe data by dict:

```python

df['A'] = df['A'].map({'a': 1, 'b': 2, 'c': 3})
```

if `A` column has value not in dict, it will be NaN, and it will raise error when serializing, so we need to give map a default value:

```python
df['A'] = df['A'].map(lambda x: {'a': 1, 'b': 2, 'c': 3}.get(x, 0))
```
