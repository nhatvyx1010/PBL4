# consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer

class YourConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # Xử lý dữ liệu nhận được từ client
        # Ví dụ, gửi dữ liệu từ server đến client
        await self.send(text_data)
