---
layout:     post
title:      "Flask-socketio笔记"
date:       2017-03-25 11:29:00
categories: Python
tags:
    - Python
    - Flask
---

##### 背景

实现celery任务完成之后，实时消息提醒    
##### 步骤    
1. 参考文档   
   [flask-socketio文档](https://flask-socketio.readthedocs.io/en/latest/)     
   [Flask, Flask-SocketIO, Celery, and Redis - Background task processing](https://celeodor.com/flask-flask-socketio-celery-and-redis-background-task-processing/)

2. 服务端代码

   ```python
   from flask_socketio import SocketIO, emit
   import eventlet
   """
   因为celery任务要执行socketio，不在一个服务里，所以需要设置eventlet，
   创建socketio里也要设置message_queue，
   设置的值与celery－redis的broker-url一样
   """
   eventlet.monkey_patch() 
   async_mode = 'eventlet'
   thread = None

   socketio = SocketIO(app, async_mode=async_mode, message_queue='redis://10.174.93.111:6379/2')

   ＃ 10秒钟运行一次
   def background_thread():
       """Example of how to send server generated events to clients."""
       while True:
           socketio.sleep(10)
           socketio.emit('my_response', {'data': 'Server generated event'}, namespace='/test')

   # 客户端可emit到此地址，然后服务端再emit到客户端
   @socketio.on('my_event', namespace='/test')
   def test_message(message):
       emit('my_response',
            {'data': message['data']})

   @socketio.on('my_ping', namespace='/test')
   def ping_pong():
       emit('my_pong')

   # 一旦服务链接，则向客户端emit数据
   @socketio.on('connect', namespace='/test')
   def test_connect():
       global thread
       if thread is None:
           thread = socketio.start_background_task(target=background_thread)
       emit('my_response', {'data': 'Server generated event'})

   # 运行socketio服务
   if __name__ == "__main__":
       socketio.run(app, host="0.0.0.0", port=19996)
   ```


3. celery socketio代码

   ```python
   from celery import Celery
   from flask_socketio import SocketIO, emit

   from config import CELERY_BROKER_URL, CELERY_RESULT_BACKEN

   ksxing_celery = Celery("ksxing", broker=CELERY_BROKER_URL,
                          backend=CELERY_RESULT_BACKEND)
                          
   # message_queue的设置与服务端一样
   socketio_celery = SocketIO(message_queue='redis://10.174.93.111:6379/2')

   @ksxing_celery.task
   def export_all_results():
       print "task complete"
       socketio_celery.emit('my_response', {'data': 'task complete'}, namespace='/test')
   ```


4. 客户端代码

   ```html
   <div id="log"></div>
   <script>
   var socket = io.connect('http://yangle.kaoshixing.com/test');
   //socket连上之后，往服务端my_eventemit数据
   socket.on('connect', function() {
   	socket.emit('my_event', {data: 'I\'m connected!'});
   });
   //服务端和celery任务往my_response发送数据，此函数往id为log的div添加html代码
   socket.on('my_response', function(msg) {
   	$('#log').append('<br>' + $('<div/>').text('Received: ' + msg.data).html());
   });
   </script>
   ```