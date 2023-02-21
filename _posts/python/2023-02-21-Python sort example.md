---
layout: post
title: "Python sort example"
subtitle: ""
date: 2023-02-21
categories: Python
tags:
  - Python
---

sort with compare function in python.

```python
from functools import cmp_to_key

def label_cmp_function(label1, label2):
    """collection case label cmp function for sort

    Args:
        label1: label path list of dict, [{"description": "", "id": 33, "name": "123"}]
        label2: label path list of dict,
            [{ "description": "", "id": 40, "name": "default" }, { "description": "", "id": 31, "name": "感知" }]
    Returns:
        1 or -1
    """
    index = -1
    while index * -1 <= len(label1) and index * -1 <= len(label2):
        if label1[index]["name"] == label2[index]["name"]:
            index -= 1
        else:
            return -1 if label1[index]["name"] < label2[index]["name"] else 1
    return -1 if len(label1) < len(label2) else 1

result = sorted(label_list, key=cmp_to_key(label_cmp_function))
```
