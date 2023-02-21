---
layout: post
title: "React common skills"
date: 2023-02-16
categories: Frontend
tags:
  - React
---

- [组件加载后就跳转 \& useEffect 里 async function](#组件加载后就跳转--useeffect-里-async-function)
- [React Router](#react-router)
  - [如何获取 url request args](#如何获取-url-request-args)
- [drag and drop](#drag-and-drop)
- [resize](#resize)
- [useEffect](#useeffect)
  - [提示: React Hook useEffect has a missing dependency: 'xxx'. Either include it or remove the dependency array react-hooks/exhaustive-deps](#提示-react-hook-useeffect-has-a-missing-dependency-xxx-either-include-it-or-remove-the-dependency-array-react-hooksexhaustive-deps)
- [split panel](#split-panel)

### 组件加载后就跳转 & useEffect 里 async function

```js
import { useNavigate } from "react-router-dom";

function SSO() {
  const navigate = useNavigate();
  const { user, setUser } = useState();

  useEffect(() => {
    async function fetchData() {
      const response = await fetchAuthInfo(token);
      setUser(response.user);
      navigate(reponse.next_url);
    }
    fetchData();
  });
}
```

### React Router

#### 如何获取 url request args

```js
import { useSearchParams } from "react-router-dom";

const [searchParams] = useSearchParams();
const [carId] = useState(searchParams.get("car_id"));
```

### drag and drop

<https://docs.dndkit.com/>

this package is also cool: <https://github.com/react-grid-layout/react-draggable#draggable>

### resize

<https://github.com/bokuweb/re-resizable>

### useEffect

#### 提示: React Hook useEffect has a missing dependency: 'xxx'. Either include it or remove the dependency array react-hooks/exhaustive-deps

<https://stackoverflow.com/questions/55840294/how-to-fix-missing-dependency-warning-when-using-useeffect-react-hook>
在函数里加上:

```js
// eslint-disable-next-line react-hooks/exhaustive-deps
```

### split panel

<https://github.com/johnwalley/allotment>
