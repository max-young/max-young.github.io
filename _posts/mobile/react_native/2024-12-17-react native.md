---
layout:     post
title:      "React Native"
date:       2024-12-17
tags:  
  - mobile
---

https://docs.expo.dev/


```shell
# create project
mkdir rrrrrandomly
cd rrrrrandomly
npx create-expo-app@latest .
# start development, then use the Expo Go app to scan the QR code
npx expo start
# move the boilerplate (app directory) to app-example and create an empty app directory
npm run reset-project
```

https://docs.expo.dev/tutorial/introduction/


### Realm

I can use Realm as a local database.  
After using Realm, I cannot use Expo Go because it does not include this package.  
So, I need to build a custom Expo Go.

```
// filepath: /home/apollo/max/Readom/android/gradle/wrapper/gradle-wrapper.properties
distributionUrl=https\://mirrors.cloud.tencent.com/gradle/gradle-8.9-all.zip
```

```
// android/build.gradle
repositories {
    google()
    mavenCentral()
    jcenter()  // Older repositories can help resolve some issues
}
```