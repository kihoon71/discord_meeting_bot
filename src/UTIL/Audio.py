from .AsyncSingletonMeta import DataStore
from pydub import AudioSegment
from io import BytesIO
import mimetypes

class Audio(DataStore):
    
    def get_audio(self, key):
        
        data = self.get_data(key)
        
        return data 
    
    # check if the file is a wav file
    # check if instance is AudioSegment or BytesIO
    # if not raise ValueError
    async def set_audio(self, key, value):
        if self.get_audio(key) is not None:
            raise ValueError('Key already exists.')
        
        assert self.check_format(value)
        
        await self.set_data(key, value)

    def clear_audio(self, key):
        self.clear_data(key)

    def check_format(self, value):
        # check if file is pathlike object
        if isinstance(value, str) and value.endswith('.wav'):
            return True
            
        # check if the file is a wav file and if the instance is AudioSegment 
        if isinstance(value, AudioSegment):
            # to check the format of the file is a wav file
            if  value.frame_rate in [8000, 16000, 44100, 48000] and value.sample_width in [1, 2, 4]:
                return True
            else:
                raise ValueError('Invalid file type. Only WAV files are allowed.')
        elif isinstance(value, BytesIO):
            value.seek(0)
            file_type = mimetypes.guess_type(value.name)[0]
            if file_type != 'audio/wav':
                raise ValueError('Invalid file type. Only WAV files are allowed.')
            return True
        else:
            raise ValueError('Unsupported audio input type. Provide an AudioSegment object or a BytesIO object.')
        