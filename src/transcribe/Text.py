# singleton class for text
import asyncio

class Text:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Text, cls).__new__(cls)
            cls._instance.text = []
        return cls._instance
    
    async def set_text(self, text: str):
        await asyncio.sleep(0)
        self.text.append(text)
    
    def get_text(self):
        return self.text
    
    def clear_text(self):
        self.text.clear()

