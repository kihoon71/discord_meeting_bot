import asyncio

class AsyncSingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
        

# 기본 데이터 저장 클래스
class DataStore(metaclass=AsyncSingletonMeta):
    def __init__(self):
        self.data = {}
        self.lock = asyncio.Lock()

    async def set_data(self, key, value):
        async with self.lock:
            self.data[key] = value

    def get_data(self, key):
        return self.data.get(key)
        
    def clear_data(self, key):
        del self.data[key]