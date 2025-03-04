from simple_diarizer.diarizer import Diarizer
from pydub import AudioSegment
import soundfile as sf
import numpy as np
import os
from Util import create_temp_file, process_segments

class SpeakerDiarizer:
    def __init__(self, embed_model='xvec', cluster_method='sc'):
        ''' parameters
        embed_model : str, ['xvec','ecapa'] supported
        cluster_method : str, ['sc','ahc'] supported

        '''
        assert embed_model in ['xvec', 'ecapa'], "embed_model should be 'xvec' or 'ecapa'"
        assert cluster_method in ['sc', 'ahc'], "cluster_method should be 'sc' or 'ahc'"

        self.diarizer = Diarizer(embed_model=embed_model, cluster_method=cluster_method)

    def diarize_(self, audio_input, num_speakers):

        temp_file = create_temp_file(audio_input)

        segments = self.diarizer.diarize(temp_file, num_speakers)

        proecessed_segments = process_segments(segments)
        
        return proecessed_segments