from .AsyncSingletonMeta import DataStore

class Text(DataStore):
    
    def get_text(self, key):
        
        data = self.get_data(key)
        
        return data 

    async def set_text(self, key, value):
        if self.get_text(key) is None:
            await self.set_data(key, [value])
        else:
            data = self.get_data(key)
            data.append(value)

    def clear_text(self, key):
        self.clear_data(key)