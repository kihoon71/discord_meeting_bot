import os
import io
import tempfile
from pydub import AudioSegment

def create_temp_file(audio_input):
    """
    Converts an audio file (path) or an AudioSegment object into a temporary WAV file.
    Returns the path to the temporary file.
    """
    if isinstance(audio_input, str):
        # If input is a file path, check extension and convert if necessary.
        if not audio_input.lower().endswith('.wav'):
            audio = AudioSegment.from_file(audio_input)
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
                audio.export(tmp.name, format="wav")
                return tmp.name
        else:
            # Already a WAV file
            return audio_input
    elif hasattr(audio_input, "export"):
        # Assume it's an AudioSegment or similar object
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            audio_input.export(tmp.name, format="wav")
            return tmp.name
        
    elif isinstance(audio_input, io.BytesIO):
        # Assume it's a BytesIO object
        audio = AudioSegment.from_file(audio_input)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            audio.export(tmp.name, format="wav")
            return tmp.name
    else:
        raise ValueError("Unsupported audio input type. Provide a file path or an AudioSegment object.")
    
def process_segments(segments):
    """
    연속해서 동일 화자의 세그먼트를 병합합니다.
    
    Args:
        segments (list of dict): 각 세그먼트는 {"start_sample": float, "end_sample": float, "label": str} 형식.
                                 반드시 start 기준으로 정렬되어 있어야 합니다.
    
    Returns:
        list of dict: 병합된 세그먼트 리스트.
    """
    if not segments:
        return []
    
    # 시작 시간이 오름차순으로 정렬되어 있지 않다면 정렬합니다.
    segments = sorted(segments, key=lambda s: s["start_sample"])
    
    merged = []
    current = segments[0].copy()
    
    for seg in segments[1:]:
        # 동일 화자인 경우, 연속 여부는 관계없이 (중간에 gap이 있어도) 병합합니다.
        if seg["label"] == current["label"]:
            # 현재 청크의 종료 시간을 업데이트
            current["end_sample"] = seg["end_sample"]
        else:
            # 화자가 바뀌면 현재 청크를 결과에 추가하고 새 청크 시작
            merged.append(current)
            current = seg.copy()
    merged.append(current)
    
    return merged

def load_audio_to_memory(file_path):
    """
    file_path: str, WAV 파일 경로 
    ---
    WAV 파일을 메모리에 로드하여 AudioSegment 객체로 반환
    
    """
    if isinstance(file_path, str):
        with open(file_path, "rb") as f:
            audio_data = io.BytesIO(f.read())  # 파일을 메모리에 올림
        return audio_data
    else:
        raise ValueError("Unsupported audio input type. Provide a file path.")

def split_audio_memory(audio, start_time, stop_time):
    """메모리에 올라간 오디오 데이터를 자르고 반환"""
    return audio[start_time:stop_time]  