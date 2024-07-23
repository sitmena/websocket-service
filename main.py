from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from .managers import ConnectionManager
from .dependencies import get_current_user
from .models import Message

app = FastAPI()

manager = ConnectionManager()


@app.websocket("/ws/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str):
    try:
        user_id = await get_current_user(token)
        await manager.connect(websocket, user_id)
        try:
            while True:
                data = await websocket.receive_text()
                # Handle received data from WebSocket if needed
        except WebSocketDisconnect:
            manager.disconnect(user_id)
    except HTTPException:
        await websocket.close()


@app.post("/send-message")
async def send_message_to_ws(data: Message):
    user_id = await get_current_user(data.token)
    await manager.send_message(user_id, data.message)
    return {"status": "message sent"}
