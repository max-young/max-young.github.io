---
layout:     post
title:      "React Native"
date:       2024-12-23
tags:  
  - mobile
---

https://docs.expo.dev/


### Normal simple project

```shell
# create project
mkdir rrrrrandomly
cd rrrrrandomly
npx create-expo-app@latest .
# start develop, then use expo go app to scan the QR code
npx expo start
# remove the boilerplate(app directory) to app-example and create an empty app directory
npm run reset-project
```

https://docs.expo.dev/tutorial/introduction/

### Use third party libraries

If your project use some third-party libraries like "Realm", you need a development environment, you can't use Expo Go app to scan the QR code to run the app. Following the structure:
https://docs.expo.dev/get-started/set-up-your-environment/?mode=development-build&buildEnv=local

I use macbook and an android phone, works fine.  
android phone and macbook should be in the same network.

1. connect android phone with USB line, you will see your device use this command: `adb devices`
2. run the app: `npx expo run:android`
3. then press `a` to run the app on the android device.
  avoid using vpn on your phone, it may cause some problems.