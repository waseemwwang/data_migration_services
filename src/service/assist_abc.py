from abc import ABC, abstractmethod


class ServiceABC(ABC):

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    async def load_data(self):
        pass

    @abstractmethod
    async def process_data(self):
        pass

    @abstractmethod
    def process_data(self):
        pass

    @abstractmethod
    async def update_data(self):
        pass

    def as_result(self):
        pass

    async def run(self):
        await self.load_data()
        await self.process_data()
        await self.update_data()
        return self.as_result()
