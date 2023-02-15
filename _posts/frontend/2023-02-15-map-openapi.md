---
layout: post
title: "map openapi"
date: 2023-02-15
categories: Frontend
tags:
  - JavaScript
---

I suggeste amap than baidu. it's more friendly. baidu require a long text to explain why use it, and id identify is complicated.

this is the homepage of amap: <https://lbs.amap.com/>

the document is writed by common js: <https://lbs.amap.com/api/javascript-api/summary/>

we can find react format on the internet: <https://elemefe.github.io/react-amap/>

this is sample code:

```js
import React, { useEffect, useState } from "react";
import { Map as AMap, Polyline } from "react-amap";

const randomPath = () => ({
  longitude: 60 + Math.random() * 50,
  latitude: 10 + Math.random() * 40,
});

const Map: React.FC = () => {
  const [path, setPath] = useState(Array(50).fill(true).map(randomPath));

  return (
    <AMap
      amapkey="32845rdsajf82374"
      version="1.4.15"
      plugins={["ToolBar"]}
      zoom={3}
    >
      <Polyline path={path} />
    </AMap>
  );
};

export default Map;
```
