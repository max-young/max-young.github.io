---
layout: post
title: "js common skills"
date: 2023-12-12
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
- [about CSS](#about-css)
- [change url without reload](#change-url-without-reload)
- [display html string](#display-html-string)
- [wait multi fetch finish then do something](#wait-multi-fetch-finish-then-do-something)

### array

array 文档: <https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/sort>

#### array remove by value

```js
var index = array.indexOf(item);
if (index !== -1) {
  array.splice(index, 1);
}
```

#### insert value

```js
arry.splice(insertIndex, 0, value);
```

### dict object loop

array 可以用 map, forEach, dict object 怎么办?

```js
var myObject = { a: 1, b: 2, c: 3 };

Object.keys(myObject).forEach(function (key, index) {
  myObject[key] *= 2;
});

console.log(myObject);
// => { 'a': 2, 'b': 4, 'c': 6 }
```

### 打开新标签页

```js
window.open(url, "_blank").focus();
```

### Input

#### onfocus cursor end

```js
onFocus={(e) => {
  const val = e.target.value;
  e.target.value = "";
  e.target.value = val;
}}
```

### event

#### 阻止父事件的发生

```js
e.stopPropagation();
```

### double click event

```js
onClick={(e) => {
  if (e.detail === 2) {
    // double click
  }
}}
```

### about CSS

- get window size

  ```js
  window.innerWidth;
  window.innerHeight;
  ```

### change url without reload

```js
window.history.pushState({}, "", "/new-url");
```

### display html string

```js
<div dangerouslySetInnerHTML={{ __html: htmlString }} />
```

### wait multi fetch finish then do something

```js
export async function getAdminCaseStatistics(paramsString) {
  const response = await fetch(
    `${apiHost}/api/admin/cases/statistics?${paramsString}`,
    {
      method: "GET",
      headers: {
        Authorization: `${localStorage.getItem("token")}`,
      },
    }
  );
  if (response.status !== 200) {
    throw new Error(await response.text());
  }
  return response.json();
}

export async function getAdminTodoStatistics(paramsString) {
  const response = await fetch(
    `${apiHost}/api/admin/todos/statistics?${paramsString}`,
    {
      method: "GET",
      headers: {
        Authorization: `${localStorage.getItem("token")}`,
      },
    }
  );
  if (response.status !== 200) {
    throw new Error(await response.text());
  }
  return response.json();
}

Promise.all([
  getAdminCaseStatistics(queryArgs),
  getAdminTodoStatistics(queryArgs),
]).then(([caseStatistics, todoStatistics]) => {
  caseStatistics.forEach((element) => {
    if (userStatisticsMap.has(element.username)) {
      userStatisticsMap.get(element.username).caseCount = element.count;
    } else {
      userStatisticsMap.set(element.username, {
        username: element.username,
        firstName: element.first_name,
        caseCount: element.count,
        bugCount: 0,
      });
    }
  });
  todoStatistics.forEach((element) => {
    if (userStatisticsMap.has(element.username)) {
      userStatisticsMap.get(element.username).bugCount = element.count;
    } else {
      userStatisticsMap.set(element.username, {
        username: element.username,
        firstName: element.first_name,
        caseCount: 0,
        bugCount: element.count,
      });
    }
  });
  setStatistics(Array.from(userStatisticsMap.values()));
});
```js
