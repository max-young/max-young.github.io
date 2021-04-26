---
layout:     post
title:      "利用pandas对多个list转换dataframe并切片计算平均分"
subtitle:   ""
date:       2017-03-25 17:47:00
author:     "alvy"
header-img: "img/post-bg-zhenghunqishi.jpg"
header-mask: 0.3
catalog:    true
tags:
    - Python
    - Pandas
---

##### 需求

例如，两个list[1, 2, 3], [4, 5, 6]，我们要求得这两个list前两个元素的和的平均值（当然可自定义）

##### 实现

上代码：    

```python
all_score_list = [
  [1, 2, 3],
  [4, 5, 6]
]
import pandas as pd
# 转换成dataframe
scores_df = pd.DataFrame(all_score_lists)
# 纵轴切片取sub_dataframe
sub_scores_df = scores_df.ix[:, start:end]
# 横轴计算每行的和
sum_df = sub_scores_df.sum(axis=1)
# 纵轴计算平均分
mean_score = sum_df.mean()
```
