---
layout:     post
title:      "Flask SocketIO"
date:       2022-07-26
categories: Python
tags:
    - Python
    - Flask
---

服务端
```Python
import time
from threading import Thread
from flask import Flask, render_template
from flask_socketio import SocketIO, emit


app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")
thread = None


def background_stuff():
    """ Let's do it a bit cleaner """
    count = 0
    while True:
        count += 1
        time.sleep(1)
        socketio.emit('message', {'data': 'This is data', 'time': count}, namespace='/test')


@app.route('/')
def index():
    global thread
    if thread is None:
        thread = Thread(target=background_stuff)
        thread.start()
    return render_template('client.html')

@socketio.on('my event', namespace='/test')
def my_event(msg):
    print(msg['data'])

@socketio.on('connect', namespace='/test')
def connect():
    emit('my response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')
	
	
if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", debug=True, port=5001)
```
客户端
```html
<!DOCTYPE HTML>
<html>
<head>
    <title>Flask-SocketIO Test</title>
    <script src="https://cdn.staticfile.org/jquery/1.10.2/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js" integrity="sha512-q/dWJ3kcmjBLU4Qc47E4A9kTB4m3wuTY7vkFJDTZKjTs8jhyGQnaUrxa0Ytd0ssMZhbNua9hE+E7Qv1j+DyZwA==" crossorigin="anonymous"></script>
    <script type="text/javascript" charset="utf-8">
            var socket = io.connect('http://localhost:5001/test');
            socket.on('connect', function(msg) {
                socket.emit('my event', {data: 'I\'m connected!'});
                // socket.emit({data: 'I\'m connected!'});
            });
            socket.on('message', function(msg){
                console.log(msg.time)
                $('#test').append($('<li>').text(msg.time));
            });
    </script>
</head>
<body>
    <h3>Demo-Flask-SocketIO</h3>
    <p id='test'></p>
</body>
</html>
```