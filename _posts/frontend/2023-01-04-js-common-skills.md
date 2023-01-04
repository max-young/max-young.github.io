---
layout: post
title: "js common slills"
date: 2023-01-04
categories: Frontend
tags:
  - JavaScript
---

- [array](#array)
  - [array remove by value](#array-remove-by-value)
  - [insert value](#insert-value)
- [dict object loop](#dict-object-loop)
- [打开新标签页](#打开新标签页)
- [Input](#input)
  - [onfocus cursor end](#onfocus-cursor-end)
- [event](#event)
  - [阻止父事件的发生](#阻止父事件的发生)
- [double click event](#double-click-event)

#### array

array 文档: <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort>

##### array remove by value

```js
var index = array.indexOf(item);
if (index !== -1) {
  array.splice(index, 1);
}
```

##### insert value

```js
arry.splice(insertIndex, 0, value);
```

#### dict object loop

array 可以用 map, forEach, dict object 怎么办?

```js
var myObject = { a: 1, b: 2, c: 3 };

Object.keys(myObject).forEach(function (key, index) {
  myObject[key] *= 2;
});

console.log(myObject);
// => { 'a': 2, 'b': 4, 'c': 6 }
```

#### 打开新标签页

```js
window.open(url, "_blank").focus();
```

#### Input

##### onfocus cursor end

```js
onFocus={(e) => {
  const val = e.target.value;
  e.target.value = "";
  e.target.value = val;
}}
```

#### event

##### 阻止父事件的发生

```js
e.stopPropagation();
```

#### double click event

```js
onClick={(e) => {
  if (e.detail === 2) {
    // double click
  }
}}
```
