from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK
from pydantic import BaseModel
import asyncio
import logging

from managers import manager, mq
from services import get_current_user_id

logger = logging.getLogger(__name__)

trigger = APIRouter(prefix="", tags=["trigger_in"])


class NotificationBody(BaseModel):
    body: dict
    user_id: int


State = []

@trigger.post("/send-message/", status_code=200)
async def registration(notification_body: NotificationBody):
    notification_body = notification_body.dict()
    print(f"\n\nnotification_body: {notification_body}\n\n")
    if manager.get_ws(notification_body["user_id"]):
        ws_alive = await manager.pong(manager.get_ws(notification_body["user_id"]))
        if ws_alive:
            print(f"\n\nnotification_body: {notification_body}\n\n")

            await manager.send_personal_message(notification_body)
        else:
            mq.publish_notification(notification_body)
    else:
        mq.publish_notification(notification_body)

    State.append(notification_body)

    # print(State)
    return {"message": "This has been published"}


@trigger.websocket("/ws/")
async def notification_socket(
    websocket: WebSocket
):
    user_id = await get_current_user_id(websocket.cookies.get("Authorization", ""))
    await manager.connect(websocket, user_id)

    try:
        if manager.get_ws(user_id):
            user_meesage = mq.get_user_messages(user_id)

            if user_meesage != None:
                for message in user_meesage:
                    if message != None:
                        message_status = await manager.personal_notification(message)
                        # delete the message from the queue if successfully sent via WebSocket
                        if message_status:
                            mq.channel.basic_ack(delivery_tag=message["delivery_tag"])

        hang = True
        while hang:
            try:
                await asyncio.sleep(1)
                await manager.ping(websocket)
            except asyncio.exceptions.CancelledError:
                break

    except (WebSocketDisconnect, ConnectionClosedError, ConnectionClosedOK):
        manager.disconnect(user_id)
