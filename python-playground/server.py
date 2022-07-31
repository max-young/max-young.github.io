#!/usr/bin/env python

import asyncio
import websockets
import json
import secrets


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
        client_websocket = JOIN[event["key"]]
    except KeyError:
        await error(websocket, "cilent not found.")
        return
    event = {
        "type": "progress",
        "message": event["message"],
    }
    await client_websocket.send(json.dumps(event))

async def echo(websocket):
    async for message in websocket: 
        event = json.loads(message)
        event_type = event["type"]
        if event_type == "client":
            await start(websocket)
        elif event_type == "progress":
            await progress(websocket, event)
        else:
            error(websocket, "unknown event type.")

async def main():
    async with websockets.serve(echo, "localhost", 8001):
        await asyncio.Future()  # run forever

asyncio.run(main())