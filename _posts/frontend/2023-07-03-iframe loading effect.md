---
layout: post
title: "iframe loading effect"
date: 2023-07-03
categories: Frontend
tags:
  - React
---

when iframe's src request is slow, iframe will show a blank page, which is not a good user experience. So we need to add a loading effect to the iframe.

```jsx
import { LoadingOutlined } from "@ant-design/icons";
import { useState } from "react";

const antIcon = <LoadingOutlined style={{ fontSize: 24 }} spin />;

const App = () => {
  const [shellLoading, setShellLoading] = useState(true);

  return (
    <div className="flex-1 flex flex-col justify-center">
      {shellLoading && <Spin size="large" indicator={antIcon} />}
      <iframe
        title="console"
        loading="lazy"
        src={consoleUrl}
        width="100%"
        height={`${shellLoading ? "0" : "100%"}`}
        frameBorder="0"
        onLoad={() => {
          setShellLoading(false);
        }}
      ></iframe>
    </div>
  );
};
```
