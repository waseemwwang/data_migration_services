from typing import Dict
from service.assist_abc import ServiceABC


# 添加用户
class CreateChatbotUser(ServiceABC):

    def __init__(self, data: Dict = None):
        self.data = data
        self.info = None

    async def load_data(self):
        return await super().load_data()

    async def process_data(self):
        return super().process_data()

    async def update_data(self):
        return await super().update_data()

    def as_result(self):
        return self.info
