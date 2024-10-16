# import enum
# import os
# import pika
# import json
# import time
# import logging
# import threading
# import uuid
# import aio_pika
#
#
# QUEUE_NAME = "websocket_notifications"
# CONSUME_QUEUE_NAME = "websocket_notifications_consumer"
# RABBITMQ_SERVICE = os.getenv('RABBITMQ_URL', "rabbitmq")
# RABBITMQ_PORT = os.getenv('RABBITMQ_PORT', 5672)
#
# logger = logging.getLogger(__name__)
# class RabbitMqActions(enum.Enum):
#     CONNECT = "connect"
#     DISCONNECT = "disconnect"
#     SEND_MESSAGE = "send_message"
#
#
# username = 'user'  # Replace with your RabbitMQ username
# password = 'pass'  # Replace with your RabbitMQ password
#
# credentials = pika.PlainCredentials(username, password)
# RABBITMQ_URL = "amqp://user:pass@rabbitmq/"
#
#
#
# class PikaClient:
#
#     def __init__(self, process_callable):
#         self.publish_queue_name = QUEUE_NAME
#         self.connection = pika.BlockingConnection(
#             pika.ConnectionParameters(host=RABBITMQ_SERVICE, credentials=credentials)
#         )
#         self.channel = self.connection.channel()
#         self.publish_queue = self.channel.queue_declare(queue=self.publish_queue_name)
#         self.callback_queue = self.publish_queue.method.queue
#         self.response = None
#         self.process_callable = process_callable
#         logger.info('Pika connection initialized')
#
#     async def consume(self, loop):
#         """Setup message listener with the current running loop"""
#         connection = await aio_pika.connect_robust(host=RABBITMQ_SERVICE,
#                                           port=RABBITMQ_PORT,
#                                           loop=loop)
#         channel = await connection.channel()
#         queue = await channel.declare_queue(CONSUME_QUEUE_NAME)
#         await queue.consume(self.process_incoming_message, no_ack=False)
#         logger.info('Established pika async listener')
#         return connection
#
#     async def process_incoming_message(self, message):
#         """Processing incoming message from RabbitMQ"""
#         message.ack()
#         body = message.body
#         logger.info('Received message')
#         if body:
#             self.process_callable(json.loads(body))
#
#     def send_message(self, message: dict):
#         """Method to publish message to RabbitMQ"""
#         self.channel.basic_publish(
#             exchange='',
#             routing_key=self.publish_queue_name,
#             properties=pika.BasicProperties(
#                 reply_to=self.callback_queue,
#                 correlation_id=str(uuid.uuid4())
#             ),
#             body=json.dumps(message)
#         )
#
#
# class RabbitMqService:
#     channel = None
#     # channel_lock = threading.Lock()
#
#     @classmethod
#     def c_conn(cls):
#         parameters = pika.URLParameters('amqp://user:pass@rabbitmq:5672')
#         connection = pika.BlockingConnection(parameters)
#         return connection
#
#     @classmethod
#     def get_channel(cls):
#         # with cls.channel_lock:
#         return cls.c_conn().channel()
#
#     @classmethod
#     def callback(cls, channel, method, properties, body):
#         from main import manager
#
#         try:
#             message = json.loads(body.decode("utf-8"))
#
#             if message["action"] == RabbitMqActions.CONNECT.value:
#                 user_id = message["user_id"]
#                 logger.info(f"\nUser connected: {user_id}")
#
#             elif message["action"] == RabbitMqActions.DISCONNECT.value:
#                 user_id = message["user_id"]
#                 logger.info(f"\nUser disconnected: {user_id}")
#
#             elif message["action"] == RabbitMqActions.SEND_MESSAGE.value:
#                 logger.info(f"\n callback: {message}\n")
#
#                 user_id = message["user_id"]
#                 title = message["title"]
#                 msg = message["message"]
#
#                 manager.send_message(user_id, title, msg)
#         except Exception as exc:
#             logger.exception(f"callback | {exc}")
#
#     @classmethod
#     def publish_to_rabbitmq(cls, message):
#         try:
#             logger.info(f"\n before publish_to_rabbitmq\n")
#
#             channel = cls.get_channel()
#             channel.queue_declare(queue=QUEUE_NAME, durable=True)
#             channel.basic_publish(
#                 exchange="",
#                 routing_key=QUEUE_NAME,
#                 body=json.dumps(message)
#             )
#             logger.info(f"\n after publish_to_rabbitmq: {message}\n")
#         except Exception as exc:
#             logger.exception(f"publish_to_rabbitmq | {exc}")
#
#     @classmethod
#     def start_consumer(cls):
#
#         try:
#             connection = cls.c_conn()
#             channel = connection.channel()
#             logger.info(f"\n\nstart_consumer | Connected to RabbitMQ... conn: {connection}\n\n")
#
#             channel.queue_declare(queue=QUEUE_NAME, durable=True)
#             channel.basic_qos(prefetch_count=1)
#             channel.basic_consume(
#                 queue=QUEUE_NAME,
#                 auto_ack=False,
#                 on_message_callback=cls.callback
#             )
#             channel.start_consuming()
#         except Exception as exc:
#             logger.exception(f"start_consumer | {exc}")
#
#
