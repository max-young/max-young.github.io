---
layout:     post
title:      "Visual Studio Code"
date:       2022-05-13
categories: Tools
tags:
    - VSCode
---

<!-- TOC -->

- [操作](#操作)
- [快捷键](#快捷键)
  - [代码相关](#代码相关)
  - [操作相关](#操作相关)
  - [Markdown](#markdown)
- [自定义配置](#自定义配置)
- [Extensions](#extensions)

<!-- /TOC -->

环境: macos

<a id="markdown-操作" name="操作"></a>
### 操作

- workspace  
    工作空间, 我们在做某一个项目的时候, 可能不止一个folder(或者说一个repo)  
    常规的做法是打开多个windows窗口, 在多个窗口之间切换, 这样很麻烦, 我们能不能把多个文件夹组织在一个窗口呢?  
    1. 先打开一个folder
    2. 然后File-Add Folder to Workspace打开另外一个folder  
    这样我们就把两个folder组织在一个workspace里了, 我们还可以保存此workspace, 下次就直接打开这个workspace即可, 不用重复上面的操作  
    同时, 我们可以对workspace进行配置, 而不用对每个folder(repo)进行配置

<a id="markdown-快捷键" name="快捷键"></a>
### 快捷键

**这个命令非常关键, 可以查到相关操作, 以及快捷键, 并自定义快捷键**  
显示我能操作的命令: `command + shift + p`  

<a id="markdown-代码相关" name="代码相关"></a>
#### 代码相关

- 编译  
`command + shift + b`

- git blame  
安装gitlens, 搜索blame, 设置快捷键, 比如我设置成`alt + b`, 这样光标所在行就会显示git commit信息

- 跳转到definition  
`g + d`或者`F12`

- 回退到之前的代码位置  
`cmd + o`或者`alt + -`

<a id="markdown-操作相关" name="操作相关"></a>
#### 操作相关

- Terminal切换  
    ctrl + ` 或者 command + j

- Terminal split panel switch  
  alt + command + ->/<-

- 搜索文件  
    command + p

- 当前路径下全局搜索  
即左侧放大镜 `command + shift + f`

- 工作区(编辑区)切换  
  第1个编辑文件 `command + 1`  
  第2个编辑文件 `command + 2`

- explorer folder and unfold  
`command + down`

- show and hide explorer  
其实是toggle side bar visibbility  
`command + b`

<a id="markdown-markdown" name="markdown"></a>
#### Markdown

- Preview  
  command + k, v

<a id="markdown-自定义配置" name="自定义配置"></a>
### 自定义配置

- 下边栏panel的最大化和还原快捷键设置  
  找到这个操作的英文名称: 鼠标放置在下边栏panel的最大化按钮上, 就会显示: Maximize Panel Size  
  Ctrl/Command + shift + p搜索这个操作的英文名称
  点击配置按钮, 在新开页面里即可自定义快捷键, 根据需要配置  
  其他快捷键的配置都是这个步骤

- 切换窗口快捷键 switch window shortcut  
  command + shift + p 搜索quick switch window  
  点击配置按钮, 在新开页面里即可自定义快捷键, 我配置的是alt + tab

- 不同文件类型的tab size设置  
  例如python的tab size是4, 我们在settings.json里加上:  
  ```json
  "[python]": {
    "editor.insertSpaces": true,
    "editor.tabSize": 4  
  }
  ```

- 代码提示  

  <img src="/images/posts/vscode_snippet.png" style="width:80%">
  红色框里的提示可能不显示, 是因为Snippets Prevent Quick Suggestions这个配置给勾上了, 去掉就可以了  
  之后可能还是不显示, 但是多出来一个大于号, 点击大于号就出来了, 之后也就自动出来了

<a id="markdown-extensions" name="extensions"></a>
### Extensions

- Copilot  
  markdown文件按Tab键接受代码提示时不管用, 应该是tab键和markwon的extension有冲突, 需要修改keybinding.json配置(按Ctrl + shift + p, 找到Preferences: Open Keyboard Shortcuts (JSON))  
  参照<https://github.com/microsoft/vscode/issues/131953#issuecomment-909900927>:
  ```json
  [
  {
    "key": "tab",
    "command": "markdown.extension.onTabKey",
    "when": "editorTextFocus && !inlineSuggestionVisible && !editorReadonly && !editorTabMovesFocus && !hasOtherSuggestions && !hasSnippetCompletions && !inSnippetMode && !suggestWidgetVisible && editorLangId == 'markdown'"
  },
  {
    "key": "tab",
    "command": "-markdown.extension.onTabKey",
    "when": "editorTextFocus && !editorReadonly && !editorTabMovesFocus && !hasOtherSuggestions && !hasSnippetCompletions && !inSnippetMode && !suggestWidgetVisible && editorLangId == 'markdown'"
  }
  ]
  ```

  ### problems

  #### ipch空间过大, 导致文件无法保存

  ipch文件夹存储c++ intellisense cache, 默认路径是Library/Caches/vscode-cpptools/ipch. 可以删除里面的所以内容, 不会有影响.  
  还可以设置一下大小避免此问题, 在settings.json里加上:  
  ```json
  "C_Cpp.intelliSenseCacheSize": <number>
  ```
  比如可以设置为1024  
  <https://code.visualstudio.com/docs/cpp/faq-cpp#_what-is-the-ipch-folder>
