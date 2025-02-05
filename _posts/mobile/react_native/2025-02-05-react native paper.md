---
layout:     post
title:      "React Native Paper"
date:       2025-02-05
tags:  
  - mobile
---

This is a piece of React Native Paper code:
```js
<FAB.Group
  open={FABOpen}
  visible
  icon={"plus"}
  actions={[
    { icon: "plus", onPress: () => router.push("/book/create") },
    {
      icon: "plus",
      onPress: () => console.log("Pressed star"),
    },
  ]}
  onStateChange={onFABStateChange}
/>
```
We can use string "plus" to represent the icon. Why? and what string can we use? 

In React Native Paper, the icon prop in components like <FAB.Group> accepts a string that refers to an icon from the Material Community Icons library. This works because React Native Paper internally uses react-native-vector-icons/MaterialCommunityIcons to render icons.

What icon strings can I use?
You can use any icon name from the Material Community Icons library.

👉 Full list of available icons:
🔗 https://materialdesignicons.com/