---
layout: post
title: "Loop With SSH in Shell Script"
date: 2024-08-13
categories: Linux
tags:
  - shell
---

The code is:

```shell
collect_data() {
  echo $1
  echo $2
  ssh car91 "echo 1"
}

minor_lidars='[ { "label": "前 右", "location": "frontright", "type": "bp" }, { "label": "后 左", "location": "rearleft", "type": "bp" } ]'

while read -r lidar; do
  location=$(echo $lidar | jq -r '.location')
  type=$(echo $lidar | jq -r '.type')
  if [ "$type" == "bp" ]; then
    type="rslidar"
  fi
  collect_data $type $location
  echo "Finished collect_data for $location"
done < <(echo "$minor_lidars" | jq -c '.[]')
```

The expcted result is execute function collect_data twice, but it was only once.  
the reason is: The issue you're encountering is likely due to the `ssh` command consuming the standard input, which interferes with the `while read` loop.  
we must change the ssh command line to:
```shell
ssh car91 "echo 1" < /dev/null
```
