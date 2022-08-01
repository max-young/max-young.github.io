from flask import Flask, request
from flask_cors import CORS
import asyncio
import websockets
import json
import threading
import time


app = Flask(__name__)
CORS(app)

@app.route("/")
def hello_world():
    params = request.args
    token = params.get("token")
    thread = threading.Thread(target=start, args=(token,))
    thread.start()
    return "Hello, World!"

def start(token):
    global progress_token
    progress_token = token

    asyncio.run(hello("开始传送脚本......"))
    print("11111")
    asyncio.run(hello("开始传送脚本......1111"))
    print("22222")
    time.sleep(2)
    asyncio.run(hello("开始传送脚本......2222"))
    import subprocess
    with subprocess.Popen([ 'rsync', '-avz', '--progress', "/home/yangle/Downloads/docker-desktop-4.10.1-amd64.deb", "/home/yangle/Documents"],
                          stdout=subprocess.PIPE,
                          bufsize=1,
                          universal_newlines=True) as process:
        for line in process.stdout:
            line = line.rstrip()
            print(f"line = {line}")
            asyncio.run(hello(line))


async def hello(message):
    async with websockets.connect("ws://localhost:8001") as websocket:
        await websocket.send(json.dumps({"type": "progress", "key": progress_token, "message": message}))

if __name__ == "__main__":
    app.run()
    