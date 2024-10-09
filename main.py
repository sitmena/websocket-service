from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException,Request

from pydantic import BaseModel
import os
JWT_TOKEN_KEY = os.getenv("JWT_KEY")
class Message(BaseModel):
    token: str
    message: str

app = FastAPI()
from fastapi import WebSocket
from typing import Dict


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: str):
        self.active_connections.pop(user_id, None)

    async def send_message(self, user_id: str, title: str, message: str):
        websocket = self.active_connections.get(user_id)
        if websocket:
            await websocket.send_json({"message": message, "title": title})

manager = ConnectionManager()

async def get_current_user_id(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization token")

    # Simulate token decoding. In a real scenario, decode the token here
    token = auth_header.split(" ")[1]
    from jwt import decode
    decoded = decode(token, JWT_TOKEN_KEY, algorithms=["HS256"])
    user_id = decoded.get('user_id')
    return user_id


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        user_id = await get_current_user_id(websocket)
        await manager.connect(websocket, user_id)
        try:
            while True:
                data = await websocket.receive_text()
                # Handle received data from WebSocket if needed
        except WebSocketDisconnect:
            manager.disconnect(user_id)
    except HTTPException:
        await websocket.close()


# REST API endpoint to send a message to a specific user
@app.post("/send-message/")
async def send_message(request: Request, user_id: str, title: str, message: str):
    """Send a push notification to a specific user using a RESTful API"""
    await manager.send_message(message, title, user_id)
    return {"status": "Message sent"}

# Dependency to extract user_id from an authorization token
