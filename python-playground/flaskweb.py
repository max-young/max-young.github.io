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
    asyncio.run(hello("开始传送脚本......", token))
    print("11111")
    asyncio.run(hello("开始传送脚本......1111", token))
    print("22222")
    time.sleep(2)
    asyncio.run(hello("开始传送脚本......2222", token))
    

async def hello(message, token):
    async with websockets.connect("ws://localhost:8001") as websocket:
        await websocket.send(json.dumps({"type": "progress", "key": token, "message": message}))

if __name__ == "__main__":
    app.run()
    