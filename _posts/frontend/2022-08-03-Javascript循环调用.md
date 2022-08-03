---
layout:     post
title:      "Javascript循环调用"
date:       2022-07-29
categories: Frontend
tags:
    - Javascript
---

定义一个function, 隔两秒执行一次, 其实就是在function里等待两秒, 然后recursive执行function

```javascript
let searchParams = new URLSearchParams(window.location.search);
let carId = searchParams.get('car_id');
let beginTime = searchParams.get('begin_time');
let endTime = searchParams.get('end_time');
var socket = io.connect('http://{{host}}:{{port}}/dv_progress');
socket.on('message', function (msg) {
  $('#message').append(msg.msg + '<br>');
});
async function playDV() {
  let refresh = false;
  $.ajaxSetup({ async: false });
  $.post("/vehiclecase/play_dv_api",
    {
      car_id: carId,
      begin_time: beginTime,
      end_time: endTime
    }, function (data, status) {
      if (status == "success") {
        message = data.message;
        displayHtml = `<div class="text-left position-absolute text-light d-flex align-content-end flex-wrap">${message}</div>`;
        dataStatus = data.status;
        if (dataStatus == 0) {
          $('#message').empty();
          $("#dv-iframe").attr("src", message);
        } else if (dataStatus == 1) {
          refresh = true;
        } else if (dataStatus == 2) {
          $('#message').append(message + '<br>');
        } else if (data.status == 3) {
          alert(message);
        } else {
          alert("未知错误");
        }
      } else {
        alert(data);
      }
    }
  );
  if (refresh == true) {
    await new Promise(resolve => setTimeout(resolve, 2000));
    playDV();
  }
}
playDV();
```