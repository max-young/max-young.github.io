---
layout: post
title: "mqtt mosquitto"
date: 2023-05-11
categories: Linux
tags:
  - mqtt
---

- [broker](#broker)
- [client](#client)
  - [shell cli](#shell-cli)
  - [client tools](#client-tools)
  - [python](#python)
  - [js](#js)
  - [node.js](#nodejs)
- [references](#references)

mqtt is a lightweight messaging protocol for small sensors and mobile devices, optimized for high-latency or unreliable networks.
it is widely used in the field of IoT(Internet of things 物联网).

mqtt is a protocal, it has many implementations, such as mosquitto, emqtt, etc.  
mosquitto is a open source mqtt broker, it is written in C, and it is very small, it is easy to install and use.

it has broker and client. client can pub/sub message to broker.

let's see how to install and use it.

### broker

we can use docker to implent broker, it is very easy.

1. create directory and config file in the home directory
   the file tree is like this:
   ```text
   ├── mosquitto-mqtt
        ├── config
        │   └── mosquitto.conf
        ├── data
        └── log
   ```
   `mosquitto.conf` is the config file, it is like this:
   ```text
   pid_file  /mosquitto/data/mosquitto.pid
   persistence true
   persistence_location /mosquitto/data/
   log_dest file /mosquitto/log/mosquitto.log
   log_type error
   log_type notice
   log_type information
   log_type debug
   log_type websockets
   connection_messages true
   log_dest topic
   log_dest stdout
   allow_anonymous true
   listener 1883
   ```
2. docker run

   ```bash
   docker run -it --rm --name surge-mqtt -p 1883:1883  -v ~/mosquitto-mqtt:/mosquitto  eclipse-mosquitto
   ```

### client

#### shell cli

<https://hivemq.github.io/mqtt-cli/>

```shell
# test
mqtt test -h 192.168.199.102 -p 8808
# sub
mqtt sub -h 192.168.199.102 -p 8808 -t test
# pub
mqtt pub -h 192.168.199.102 -p 8808 -t test -m test
```

#### client tools

[mqttx](https://mqttx.app/) is a elegent mqtt client.  
 you can use web or install in your computer.

#### python

install paho-mqtt client:

```shell
pip install paho-mqtt
```

we can pub and sub message to the above broker.
this is pub code:

```python
# python 3.6

import random
import time

from paho.mqtt import client as mqtt_client


broker = 'localhost'
port = 1883
topic = "test"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'emqx'
password = 'public'

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def publish(client):
    msg_count = 0
    while True:
        time.sleep(1)
        msg = f"messages: {msg_count}"
        result = client.publish(topic, msg)
        # result: [0, 1]
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message to topic {topic}")
        msg_count += 1


def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    run()
```

sub code:

```python
# python3.6

import random

from paho.mqtt import client as mqtt_client


# broker = 'broker.emqx.io'
broker = 'localhost'
port = 1883
topic = "test"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'emqx'
password = 'public'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
```

run these two file, we can see the effect.

#### js

<https://github.com/mqttjs/MQTT.js>

react code:

```js
import React, { useEffect, useState } from "react";
import { Map as AMap, Polyline } from "react-amap";
import * as mqtt from "mqtt/dist/mqtt";

const Map: React.FC = () => {
  const [path, setPath] = useState(Array(50).fill(true).map(randomPath));

  const [connectStatus, setConnectStatus] = useState("Connecting");
  const [client, setClient] = useState(
  mqtt.connect("mqtt://192.168.199.102:8808", {
    protocol: "ws",
    keepalive: 20,
    clientId: "mqttjs\_" + Math.random().toString(16).substr(2, 8),
    })
  );

  useEffect(() => {
    if (client) {
      console.log(client);
      client.on("connect", () => {
        setConnectStatus("Connected");
        console.log("connected");
      });
      client.on("error", (err) => {
        console.error("Connection error: ", err);
        client.end();
      });
      client.on("reconnect", () => {
        setConnectStatus("Reconnecting");
      });
      client.on("message", (topic, message) => {
        const payload = { topic, message: message.toString() };
        setPayload(payload);
      });
    }
  }, [client]);

  ...
}
```

maybe you will get an error: websocket connection failed  
you should add `protocol websockets` to the mqtt broker config and restart.

#### node.js

create a file `mqtt.js`:

```javascript
const mqtt = require("mqtt");
const client = mqtt.connect("mqtt://localhost:1883");

const EdgeServerMountpointStateTopic =
  "/surge/edge_server_monitor/disk/mountpoint_state_report";
const EdgeServerHotPlugEventTopic =
  "/surge/edge_server_monitor/disk/hot_plug_event_report";

client.on("connect", function () {
  client.subscribe(EdgeServerMountpointStateTopic, function (err) {
    if (err) {
      console.log("监控边缘服务器数据盘状态MQTT订阅失败");
    }
  });
  client.subscribe(EdgeServerHotPlugEventTopic, function (err) {
    if (err) {
      console.log("监控车辆数据盘是否插盘MQTT订阅失败");
    }
  });
});

client.on("message", function (topic, message) {
  // client.end();
  let data;
  switch (topic) {
    // 边缘服务器盘是否在线
    case EdgeServerMountpointStateTopic:
      try {
        data = JSON.parse(message.toString());
      } catch (e) {
        console.log(
          "监控边缘服务器数据盘状态MQTT消息解析失败: " + message.toString()
        );
        return;
      }
      break;
    // 车辆数据盘是否插入边缘服务器
    case EdgeServerHotPlugEventTopic:
      try {
        data = JSON.parse(message.toString());
      } catch (e) {
        console.log(
          "监控车辆数据盘是否插盘MQTT消息解析失败: " + message.toString()
        );
        return;
      }
      break;
    default:
      console.log("default");
      break;
  }
});
```

install mqtt.js:

```shell
npm install mqtt --save
```

use node.js to run:

```node
node mqtt.js
```

### references

<https://www.emqx.com/en/blog/how-to-use-mqtt-in-python>
<http://www.steves-internet-guide.com/running-the-mosquitto-mqtt-broker-in-docker-beginners-guide/>
