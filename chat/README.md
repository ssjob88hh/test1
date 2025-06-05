# WebSocket Chat Room Example

This is a simple chat room server implemented with Python's `websockets` library.
It supports multiple rooms and private messages between users.

## Running the server

1. Install the required dependency:
   ```bash
   pip install websockets
   ```
2. Run the server:
   ```bash
   python3 server.py
   ```
3. Open `static/index.html` in your browser and connect using a username and room.

Multiple clients can connect to the same room or different rooms. Use the
"private to" field to send a private message to a specific user.
