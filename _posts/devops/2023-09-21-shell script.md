---
layout: post
title: "shell script"
date: 2023-09-21
categories: Linux
tags:
  - shell
---

- [常用命令](#常用命令)
  - [shift](#shift)
  - [local](#local)
  - [echo](#echo)
- [运算符](#运算符)
  - [关系运算符](#关系运算符)
  - [文件测试运算符](#文件测试运算符)
  - [字符串运算符](#字符串运算符)
- [语法](#语法)
  - [if else](#if-else)
  - [获取命令的输出](#获取命令的输出)
  - [定义 dict 然后 loop](#定义-dict-然后-loop)
- [variables](#variables)
  - [$BASH\_SOURCE](#bash_source)
  - [define variable from env and default value](#define-variable-from-env-and-default-value)
- [handle string](#handle-string)
- [remove suffix](#remove-suffix)

### 常用命令

#### shift

删除参数

一个`run.sh`脚本:

```bash
#!/bin/bash
while [ $# != 0 ];do
echo "第一个参数为：$1,参数个数为：$#"
shift
done
```

执行`run.sh a b c d e f`
结果是

```shell
第一个参数为：a,参数个数为：6
第一个参数为：b,参数个数为：5
第一个参数为：c,参数个数为：4
第一个参数为：d,参数个数为：3
第一个参数为：e,参数个数为：2
第一个参数为：f,参数个数为：1
```

从上可知`shift(shift 1)`命令每执行一次, 变量的个数`$#`减一(之前的`$1`变量被销毁, 之后的`$2`就变成了`$1`), 而变量值提前一位.

#### local

定义局部变量, 默认是 global 变量, 加上 local 就是局部变量, 可以在函数里定义 local

```bash
function main() {
  local a="hello world"
  echo $a
}

main     # 结果是hello world
echo $a  # 这里打印不出来, 如果去掉local就可以打印出来
```

#### echo

echo 除了打印, 还能代表返回值:

```bash
function main() {
  local a="hello world"
  echo $a
  return 0
}

b=$(main)
echo $b # 这里输出是hello world, 而不是0
```

### 运算符

#### 关系运算符

- -lt 是否小于

#### 文件测试运算符

- -f file 检测文件是否是普通文件(既不是目录，也不是设备文件), 如果是, 则返回 true.
  ```bash
  if [ -f $file ]
  then
   echo "文件为普通文件"
  else
   echo "文件为特殊文件"
  fi
  ```

#### 字符串运算符

- -z 检查字符串长度是否为 0, 为 0 则返回为 true

  ```bash
  if [ -z $a ]
  then
   echo "-z $a : 字符串长度为 0"
  else
   echo "-z $a : 字符串长度不为 0"
  fi
  ```

- -z 检查字符串长度是否不为 0, 不为 0 则返回为 true

### 语法

#### if else

```bash
if [ a == b ]; then
  echo "a == b"
fi
```

或者不要分号, 把`then`换行

```bash
if [ a == b ]
then
  echo "a == b"
fi
```

#### 获取命令的输出

```bash
out=$([command])
```

#### 定义 dict 然后 loop

```bash

declare -A maps=(
    ["Antingxinzhen"]="antingxinzhen_v1"
    ["Hefei"]="hefei_v1"
    ["Huanbaoyuan"]="huanbaoyuan_v13"
    ["Shenzhen"]="shenzhen_v1"
)
for map in "${!maps[@]}";
do
    grep "$map" $2
    if [ $? == 0 ]; then
        declare new_map_dir="${maps[$map]}"
        echo $new_map_dir
        echo $MAPDIR_NAME
        if [[ $new_map_dir != $MAPDIR_NAME ]]; then
            echo "map dir name is $MAPDIR_NAME, change it to $new_map_dir"
            /home/apollo/apollo/scripts/dv_run.sh stop $1
            sleep 5
            export MAPDIR_NAME=$new_map_dir
        fi
        break
    fi
done
echo $MAPDIR_NAME
```

### variables

#### $BASH_SOURCE

`$BASH_SOURCE` is bash file's directory:

```sh
cd `dirname ${BASH_SOURCE}` && pwd
```

this code can cd to bash file's directory and output directory path.

#### define variable from env and default value

we can define a variable from env, if env value is not exist, we can use default value.

```sh
my_var=${ENV_VALUE:-default_value}
```

if not ENV_VALUE, then my_var is default_value

if we want sign a value to ENV_VALUE, we can use:

```sh
: ${ENV_VALUE:=default_value}
```

colon is a command, it do nothing. if we not use colon punctuation, th command after it will error: command not found.


### handle string

### remove suffix

file name is "abc.txt", we want to remove ".txt", we can use:

```sh
file_name="abc.txt"
echo ${file_name%.txt}
```