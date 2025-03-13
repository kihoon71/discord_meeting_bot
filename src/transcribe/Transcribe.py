import os
import io
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../UTIL"))
from Text import Text

from openai import OpenAI
from pydub import AudioSegment
from Util import load_audio_to_memory, split_audio_memory, create_temp_file
from Diarizer import SpeakerDiarizer
from pprint import pprint
import json

class Transcribe:
    def __init__(self, api_key, channel_id):
        '''
        api_key : str, whisper API key
        audio_data : bytes or path like object, audio data to transcribe
        '''
        self.diarizer = SpeakerDiarizer(embed_model='xvec', cluster_method='sc')
        self.whisper = OpenAI(api_key=api_key)
        self.channel_id = channel_id

    async def transcribe(self, audio, num_speakers=2):
        segments = self.diarizer.diarize_(audio, num_speakers)
        audio_sample = AudioSegment.from_file(audio, format="wav")
        
        # Text 클래스의 인스턴스 생성
        text_instance = Text()
        for segment in segments:
            audio_segment = split_audio_memory(audio_sample, segment['start'], segment['end'])
            
            temp_file_for_whisper = io.BytesIO() # to send a file to the whisper API
            audio_segment.export(temp_file_for_whisper, format="wav")
            temp_file_for_whisper.seek(0)

            transcript = self.whisper.audio.transcriptions.create(
                # file=temp_file_for_whisper,
                file=("audio.wav", temp_file_for_whisper),
                model="whisper-1"
                )
            string_format = f"{segment['start']} - {segment['end']} - Speaker {segment['label']} - {transcript.text}"
            await text_instance.set_text(self.channel_id, string_format)

        sorted_text = sorted(text_instance.get_text(self.channel_id), key=lambda x: float(x.split('-')[0]))

        print(sorted_text)
        
        return sorted_text
    
    def clean_up(self):
        Text().clear_text()
