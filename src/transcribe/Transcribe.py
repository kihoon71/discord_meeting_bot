from openai import OpenAI
import os
import io
from pydub import AudioSegment
from Util import load_audio_to_memory, split_audio_memory, create_temp_file
from Diarizer import SpeakerDiarizer
from Text import Text
from pprint import pprint
import json

class Transcribe:
    def __init__(self, api_key):
        '''
        api_key : str, whisper API key
        audio_data : bytes or path like object, audio data to transcribe
        '''
        self.diarizer = SpeakerDiarizer(embed_model='xvec', cluster_method='sc')
        self.whisper = OpenAI(api_key=api_key)

    async def transcribe(self, audio, num_speakers=2):
        segments = self.diarizer.diarize_(audio, num_speakers)
        audio_sample = AudioSegment.from_file(audio, format="wav")
        print(f'sample rate of the audio sample: {audio_sample.frame_rate}')
        print(f"Audio sample loaded : {len(audio_sample)} ms")
        
        # Text 클래스의 인스턴스 생성
        text_instance = Text()
        for segment in segments:
            audio_segment = split_audio_memory(audio_sample, segment['start'], segment['end'])
            segment_duration_ms = len(audio_segment)
            print(f"expected duration: {segment['end_sample'] - segment['start_sample']}ms")
            print(f"Segment duration: {segment_duration_ms}ms for Speaker {segment['label']}")
            
            temp_file_for_whisper = io.BytesIO()
            audio_segment.export(temp_file_for_whisper, format="wav")
            temp_file_for_whisper.seek(0)

            transcript = self.whisper.audio.transcriptions.create(
                # file=temp_file_for_whisper,
                file=("audio.wav", temp_file_for_whisper),
                model="whisper-1"
                )
            string_format = f"{segment['start']} - {segment['end']} - Speaker {segment['label']} - {transcript.text}"
            await text_instance.set_text(string_format)

        sorted_text = sorted(text_instance.get_text(), key=lambda x: float(x.split('-')[0]))

        print(sorted_text)
        
        return sorted_text
    
    def clean_up(self):
        Text().clear_text()
