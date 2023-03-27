---
layout: post
title: "typescript"
date: 2023-03-20
categories: Frontend
tags:
  - typescript
---

- [forever run .ts file](#forever-run-ts-file)
- [omit check type](#omit-check-type)

<https://react-typescript-cheatsheet.netlify.app/docs/basic/getting-started/concurrent>

<https://www.typescriptlang.org/docs/handbook/react.html>

### forever run .ts file

```bash
# first use
npm install -g ts-node
# then use
forever start -v -c ts-node app.ts
```

### omit check type

我在.ts 文件里引用包时, 例如: `import Board from "react-trello";`, 会被提示`Could not find a declaration file for module 'react-trello'. '/Users/xxx/xxx/node_modules/react-trello/dist/index.js' implicitly has an 'any' type.`, 一般的解决办法是`npm i --save @types/react-trello`, 但是有的包会提示无法安装.  
解决方法可参照: <https://pjausovec.medium.com/how-to-fix-error-ts7016-could-not-find-a-declaration-file-for-module-xyz-has-an-any-type-ecab588800a8>  
我为了避免这种恼人的问题, 会选择第二个方案, 在 tsconfig.json 里的 compilerOptions 里加入`"noImplicitAny": false`
