

from service.assist_abc import ServiceABC


class GetUsers(ServiceABC):
    
    def __init__(self, filter, page = int, page_size = int):
        self.data = None
        self.list = None
        self.total_page = None
        self.total_num = None
        self.current_page = page
        self.page_size = page_size
        self.filter = filter
    
    async def load_data(self):
        return await super().load_data()
    
    async def process_data(self):
        return super().process_data()
    
    async def update_data(self):
        return await super().update_data()
    
    def as_result(self):
        return {
            "list": self.list,
            "total_num": self.total_num,
            "total_page": self.total_page,
            "current_page": self.current_page,
            "page_size": self.page_size,
        }