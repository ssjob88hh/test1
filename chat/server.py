import asyncio
import json
import websockets
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError

# Stores room name -> set of connected websockets
rooms = {}

# Stores websocket -> username
users = {}

async def register(ws, username, room):
    users[ws] = username
    if room not in rooms:
        rooms[room] = set()
    rooms[room].add(ws)
    await notify_room(room, f"{username} joined {room}")

async def unregister(ws):
    username = users.get(ws)
    if username is None:
        return
    for r, sockets in list(rooms.items()):
        if ws in sockets:
            sockets.remove(ws)
            await notify_room(r, f"{username} left {r}")
            if not sockets:
                rooms.pop(r)
    users.pop(ws, None)

async def notify_room(room, message):
    if room not in rooms:
        return
    for ws in rooms[room]:
        await ws.send(json.dumps({"type": "room_message", "room": room, "message": message}))

async def send_private(sender_ws, target, message):
    for ws, name in users.items():
        if name == target:
            await ws.send(json.dumps({"type": "private_message", "from": users[sender_ws], "message": message}))
            break

async def handler(ws):
    try:
        async for msg in ws:
            data = json.loads(msg)
            if data["action"] == "join":
                await register(ws, data["username"], data["room"])
            elif data["action"] == "message":
                await notify_room(data["room"], f"{users[ws]}: {data['message']}")
            elif data["action"] == "private":
                await send_private(ws, data["to"], data["message"])
    except (ConnectionClosedOK, ConnectionClosedError):
        pass
    finally:
        await unregister(ws)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("Chat server started on ws://0.0.0.0:8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
