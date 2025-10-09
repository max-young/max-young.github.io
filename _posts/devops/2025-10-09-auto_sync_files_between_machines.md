---
layout: post
title: "Auto sync files between machines"
date: 2025-10-09
categories: Linux
tags:
  - Ubuntu
---

auto detect new files in a directory, and sync to another machine.

1. create a script to sync files

  file path `/usr/local/bin/rsync_newfiles.sh`

  ```bash
  #!/usr/bin/env bash
  set -Eeuo pipefail

  SRC="/data4/products"
  DST="rino@114.111.24.169:/data4/products"
  LOG="/data1/logs/verman/rsync_newfiles.log"
  LOCKDIR="/var/lock/rsync_newfiles"
  mkdir -p "$LOCKDIR"

  RSYNC_OPTS=(
    -a
    --partial
    --temp-dir=.rsync-tmp
    --info=progress2
    --ignore-existing
    --chmod=F644,D755
    -e "ssh -o StrictHostKeyChecking=no"
  )

  # 发送钉钉告警
  dingtalk_warn() {
    local MESSAGE=$1
    local userId=$2
    local WEBHOOK_URL="https://oapi.dingtalk.com/robot/send?access_token=92db77e369e03ae2b73a0a10698db582147c87f4f2849e443f53fde265628165"
    # 简单转义换行和双引号，避免 JSON 崩
    MESSAGE=${MESSAGE//$'\n'/ }
    MESSAGE=${MESSAGE//\"/\\\"}
    local JSON_PAYLOAD
    JSON_PAYLOAD=$(cat <<EOF
  {"msgtype":"text","text":{"content":"$MESSAGE"},"at":{"atDingtalkIds":["$userId"]}}
  EOF
  )
    curl -sS -X POST "$WEBHOOK_URL" -H "Content-Type: application/json" -d "$JSON_PAYLOAD" >/dev/null || true
  }

  # 匹配需要同步的文件名（更严谨，避免跨目录）
  MATCH_RE='(^trtcache-[^/]*\.tar$|^video-[^/]*\.tar$|^map-[^/]*\.tar$)'

  # 同步一个文件，带重试与加锁
  sync_one() {
    local file="$1"           # 仅文件名（不含路径）
    local path="$SRC/$file"   # 源全路径
    local tries=0
    local rc=1

    # 针对单文件的排他锁，避免多个进程撞同一目标
    exec 9>"$LOCKDIR/${file}.lock"
    if ! flock -n 9; then
      echo "$(date '+%F %T') [SKIP] lock busy for $file" >>"$LOG"
      return 0
    fi

    while (( tries < 3 )); do
      tries=$((tries+1))
      echo "$(date '+%F %T') [INFO] rsync try#$tries $file" >>"$LOG"

      # 屏蔽 -e 导致的立即退出，用命令状态码判断
      if rsync "${RSYNC_OPTS[@]}" "$path" "$DST"; then
        echo "$(date '+%F %T') [OK] synced $file" >>"$LOG"
        rc=0
        break
      else
        rc=$?
        echo "$(date '+%F %T') [WARN] rsync failed rc=$rc on $file (try $tries)" >>"$LOG"
        # 退避：5s, 10s
        sleep $((tries*5))
      fi
    done

    if (( rc != 0 )); then
      local msg="rsync FAILED after $tries tries for $file (rc=$rc) at $(date '+%F %T')"
      echo "$(date '+%F %T') [FAIL] $msg" >>"$LOG"
      # 指定要@的人（DingTalk内部ID），不需要就留空字符串
      dingtalk_warn "$msg" "maxyangle"
    fi

    return "$rc"
  }

  # 监听新增与写完成事件（仅顶层目录；要递归可改为 -mr 并输出 %w%f）
  inotifywait -m -e close_write,moved_to --format '%f' "$SRC" | while read -r FILE; do
    [[ $FILE =~ $MATCH_RE ]] || continue
    echo "$(date '+%F %T') [INFO] new file: $FILE" >>"$LOG"
    sync_one "$FILE" || true
  done
   ```

2. make it executable

  ```bash
  chmod +x /usr/local/bin/rsync_newfiles.sh
  ```

3. create a systemd service
   
  file path `/etc/systemd/system/rsync_newfiles.service`

  ```ini
  [Unit]
  Description=Sync new tar files from /data4/products to remote
  After=network-online.target

  [Service]
  User=root
  ExecStart=/usr/local/bin/rsync_newfiles.sh
  Restart=always
  RestartSec=5

  [Install]
  WantedBy=multi-user.target
  ```

4. enable and start the service

  ```bash
  sudo systemctl daemon-reload
  sudo systemctl enable rsync_newfiles.service
  sudo systemctl start rsync_newfiles.service
  ```

5. check the service status

  ```bash
  sudo systemctl status rsync_newfiles.service
  ```