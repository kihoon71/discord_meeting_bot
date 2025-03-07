# singleton class for text
import asyncio

class Text:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Text, cls).__new__(cls)
            cls._instance.text = {}
        return cls._instance
    
    async def set_text(self, _id,text: str):
        await asyncio.sleep(0)
        if _id in self.text:
            self.text[_id].append(text)
        else:
            self.text.update({_id : [text]})
    
    def get_text(self, _id):
        return self.text[_id]
    
    def clear_text(self, _id):
        self.text[_id].clear()
        del self.text[_id]

