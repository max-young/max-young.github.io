---
layout: post
title: "Pandas common skills"
subtitle: ""
date: 2023-03-03
categories: Python
tags:
  - Python
  - Pandas
---

- [create](#create)
  - [根据已有 column 创建 column](#根据已有-column-创建-column)
- [delete](#delete)
  - [删除列](#删除列)
  - [remove row by condition](#remove-row-by-condition)
- [筛选](#筛选)
- [edit](#edit)
  - [map default value](#map-default-value)
- [nan](#nan)
  - [replace nan](#replace-nan)
  - [check if nan](#check-if-nan)

### create

#### 根据已有 column 创建 column

```python
dataframe["new_column"] = dataframe.apply(
    lambda row: row.exist_column * 2, axis=1)
```

### delete

#### 删除列

```python
df.drop('column_name', axis=1, inplace=True)
```

inplace 代表修改 df, 不用重新创建一个变量

删除多列

```python
df.drop(['column_nameA', 'column_nameB'], axis=1, inplace=True)
```

#### remove row by condition

```python
dataframe.drop(dataframe[dataframe.location_ts.isnull()].index, inplace=True)
```

### 筛选

```python
 df[df['A'].isin([3, 6])]
```

### edit

#### map default value

we can use map to update dataframe data by dict:

```python

df['A'] = df['A'].map({'a': 1, 'b': 2, 'c': 3})
```

if `A` column has value not in dict, it will be NaN, and it will raise error when serializing, so we need to give map a default value:

```python
df['A'] = df['A'].map(lambda x: {'a': 1, 'b': 2, 'c': 3}.get(x, 0))
```

### nan

#### replace nan

```python
all_df = all_df.fillna(0)
```

#### check if nan

```python
dataframe.column_filed.isnull()
```
