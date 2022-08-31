---
layout:     post
title:      "websocket"
date:       2022-08-31
categories: Python
tags:
    - Python
---

- [server](#server)
- [python client](#python-client)
- [js client](#js-client)

##### server

```python
#!/usr/bin/env python

import asyncio
import json
import secrets

import websockets

from config import WEBSOCKET_PORT

JOIN = {}


async def error(websocket, message):
    """
    Send an error message.
    """
    event = {
        "type": "error",
        "message": message,
    }
    await websocket.send(json.dumps(event))


async def start(websocket):
    key = secrets.token_urlsafe(12)
    JOIN[key] = websocket
    try:
        event = {
            "type": "init",
            "key": key,
        }
        await websocket.send(json.dumps(event))
        async for message in websocket:
            print(message)
    finally:
        del JOIN[key]


async def progress(websocket, event):
    try:
        key = event.pop("key")
        client_websocket = JOIN[key]
    except KeyError:
        await error(websocket, "cilent not found.")
        return
    await client_websocket.send(json.dumps(event))


async def echo(websocket):
    async for message in websocket:
        event = json.loads(message)
        event_type = event["type"]
        if event_type == "client":
            await start(websocket)
        else:
            await progress(websocket, event)


async def main():
    async with websockets.serve(echo, "0.0.0.0", WEBSOCKET_PORT):
        await asyncio.Future()  # run forever


asyncio.run(main())
```
```bash
python server.py
```

##### python client

```python
#!/usr/bin/env python

import json

import websockets

from config import WEBSOCKET_PORT


async def send_progress(event: dict):
    async with websockets.connect(
            "ws://localhost:{}".format(WEBSOCKET_PORT)) as websocket:
        await websocket.send(json.dumps(event))
```
```python
import asyncio
from websocket_client import send_progress
asyncio.run(send_progress({"type": "rate", "key": progress_token, "message": line}))
```

##### js client

```javascript
const websocket = new WebSocket("ws://" + window.location.hostname + ":{{websocket_port}}/");
websocket.addEventListener("open", () => {
  let event = { type: "client" };
  websocket.send(JSON.stringify(event));
});
websocket.addEventListener("message", ({ data }) => {
  const event = JSON.parse(data);
  console.log(event);
  switch (event.type) {
    case "init":
      let token = event.key;
      window.progressToken = token;
      switch (window.fileType) {
        case "simple":
          if ($("#carID").val() && $("#caseTime").val() && $("#beforeSeconds").val() && $("#afterSeconds").val()) {
            $("#play").click();
          }
          break;
        case "complete":
          if ($("#carIDCompleteFile").val() && $("#caseTimeCompleteFile").val()) {
            $("#playCompleteFile").click();
          }
          break;
      }
      break
    case "progress":
      $('#message').append("<span>" + event.message + '<span></br>');
      current_type = "progress";
      break;
    case "rate":
      if (current_type == "rate") {
        $("#message span").last().text(event.message);
      } else {
        $('#message').append("<span>" + event.message + '</span></br>');
        current_type = "rate";
      }
      break;
    case "play":
      $("#download-input").val("rsync -avPz dat102:" + event.data_path + " .");
      let playUrl = window.location.protocol + "//" + window.location.hostname + ":" + event.message;
      let iframe = '<iframe id="dv-play" class="w-100 h-100" src="' + playUrl + '"></iframe>'
      $("#screen").html(iframe);
      break;
    case "control":
      let shellUrl = window.location.protocol + "//" + window.location.hostname + ":" + event.message;
      $("#shell").attr("src", shellUrl);
      $("#shell").focus();
      break;
    default:
      throw new Error(`Unsupported event type: ${event.type}.`);
  }
});
``` 