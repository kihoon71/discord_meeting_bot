import sys
import pytest
import os
import json
import tempfile
import io

from pydub import AudioSegment

sys.path.append(os.path.join(os.path.dirname(__file__), "../src/transcribe"))

from Util import create_temp_file, process_segments, load_audio_to_memory, split_audio_memory


@pytest.fixture(scope="module")
def sample_audio():
    """Generates a short audio segment for testing (1 second of silence)."""
    return AudioSegment.silent(duration=1000)  # 1 second of silence

@pytest.fixture(scope="module")
def sample_with_open_method():
    """Generates a short audio segment for testing (1 second of silence)."""
    with open('./files/test.wav', 'rb') as f:
        return f.read()

def test_create_temp_file_from_wav():
    # Create a temporary WAV file using AudioSegment.silent
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        silent_audio = AudioSegment.silent(duration=1000)  # 1 second of silence
        silent_audio.export(tmp.name, format="wav")
        tmp_path = tmp.name
    try:
        # For a WAV file input, the function should return the same file path.
        result = create_temp_file(tmp_path)
        assert result == tmp_path
    finally:
        os.remove(tmp_path)

def test_create_temp_file_from_non_wav(tmp_path_factory):
    # Create a temporary non-WAV file, e.g. an MP3 file.
    tmp_dir = tmp_path_factory.mktemp("data")
    mp3_path = os.path.join(tmp_dir, "test.mp3")
    silent_audio = AudioSegment.silent(duration=1000)
    silent_audio.export(mp3_path, format="mp3")
    
    result = create_temp_file(mp3_path)
    # The returned file should be different (a temporary WAV file) and exist.
    assert result != mp3_path
    assert result.endswith(".wav")
    assert os.path.exists(result)
    os.remove(result)

def test_create_temp_file_from_AudioSegment():
    # Pass an AudioSegment object directly.
    silent_audio = AudioSegment.silent(duration=1000)
    result = create_temp_file(silent_audio)
    assert result.endswith(".wav")
    assert os.path.exists(result)
    os.remove(result)

def test_create_temp_file_invalid_input():
    # An unsupported input type should raise a ValueError.
    with pytest.raises(ValueError):
        create_temp_file(12345)


def test_process_segments_merging():
    # Test that the postprocess_segments function sorts segments by start time.
    # 
    segments = [
    {"start_sample": 0.0, "end_sample": 14.2, "label": "speaker_SPEAKER_01", "start": 0.0, "end": 14.2},
    {"start_sample": 14.9, "end_sample": 56.1, "label": "speaker_SPEAKER_01", "start": 14.9, "end": 56.1},
    {"start_sample": 56.5, "end_sample": 68.5, "label": "speaker_SPEAKER_01", "start": 56.5, "end": 68.5},
    {"start_sample": 68.6, "end_sample": 70.6, "label": "speaker_SPEAKER_01", "start": 68.6, "end": 70.6},
    {"start_sample": 70.7, "end_sample": 92.0, "label": "speaker_SPEAKER_01", "start": 70.7, "end": 92.0},
    {"start_sample": 92.0, "end_sample": 99.6, "label": "speaker_SPEAKER_00", "start": 92.0, "end": 99.6},
    {"start_sample": 99.9, "end_sample": 119.1, "label": "speaker_SPEAKER_00", "start": 99.9, "end": 119.1},
    {"start_sample": 119.3, "end_sample": 119.9, "label": "speaker_SPEAKER_01", "start": 119.3, "end": 119.9},
    {"start_sample": 119.9, "end_sample": 120.0, "label": "speaker_SPEAKER_00", "start": 119.9, "end": 120.0}
    ]
    
    expected_results = [
    {"start_sample": 0.0, "end_sample": 92.0, "label": "speaker_SPEAKER_01", "start": 0.0, "end": 92.0},
    {"start_sample": 92.0, "end_sample": 119.1, "label": "speaker_SPEAKER_00", "start": 92.0, "end": 119.1},
    {"start_sample": 119.3, "end_sample": 119.9, "label": "speaker_SPEAKER_01", "start": 119.3, "end": 119.9},
    {"start_sample": 119.9, "end_sample": 120.0, "label": "speaker_SPEAKER_00", "start": 119.9, "end": 120.0}
    ]


    merged_segments = process_segments(segments)

    assert len(merged_segments) == len(expected_results), "Segment count mismatch."

    for i, seg in enumerate(merged_segments):
        assert seg['start_sample'] == expected_results[i]["start_sample"], f"Start time mismatch at index {i}: expected {expected_results[i]['start_sample']}, got {seg['start_sample']}"
        assert seg["end_sample"] == expected_results[i]["end_sample"], f"Stop time mismatch at index {i}: expected {expected_results[i]['end_sample']}, got {seg['end_sample']}"
        
    # ensure the end time is correct

def test_process_segments_with_label_overlap():
    segments = [
    {"start_sample": 0.0, "end_sample": 10.0, "label": "A", "start": 0.0, "end": 10.0},
    {"start_sample": 5.0, "end_sample": 15.0, "label": "B", "start": 5.0, "end": 15.0},  # Overlaps with "A"
    {"start_sample": 15.0, "end_sample": 20.0, "label": "A", "start": 15.0, "end": 20.0},
    {"start_sample": 18.0, "end_sample": 25.0, "label": "B", "start": 18.0, "end": 25.0},  # Overlaps with "A"
    {"start_sample": 26.0, "end_sample": 30.0, "label": "A", "start": 26.0, "end": 30.0},
    {"start_sample": 28.0, "end_sample": 35.0, "label": "B", "start": 28.0, "end": 35.0}   # Overlaps with "A"
    ]

    expected_results = [
        {"start_sample": 0.0, "end_sample": 10.0, "label": "A", "start": 0.0, "end": 10.0},  # "A" remains separate
        {"start_sample": 5.0, "end_sample": 15.0, "label": "B", "start": 5.0, "end": 15.0},  # "B" remains separate
        {"start_sample": 15.0, "end_sample": 20.0, "label": "A", "start": 15.0, "end": 20.0}, # "A" remains separate
        {"start_sample": 18.0, "end_sample": 25.0, "label": "B", "start": 18.0, "end": 25.0}, # "B" remains separate
        {"start_sample": 26.0, "end_sample": 30.0, "label": "A", "start": 26.0, "end": 30.0}, # "A" remains separate
        {"start_sample": 28.0, "end_sample": 35.0, "label": "B", "start": 28.0, "end": 35.0}  # "B" remains separate
    ]

    merged_segments = process_segments(segments)

    assert len(merged_segments) == len(expected_results), f"Segment count mismatch: expected {len(expected_results)}, got {len(merged_segments)}"

    for i, seg in enumerate(merged_segments):
        assert seg["start_sample"] == expected_results[i]["start_sample"], f"start time mismatch at index {i}: expected {expected_results[i]['start_sample']}, got {seg['start_sample']}"
        assert seg["end_sample"] == expected_results[i]["end_sample"], f"Stop time mismatch at index {i}: expected {expected_results[i]['end_sample']}, got {seg['end_sample']}"
        assert seg["label"] == expected_results[i]["label"], f"label mismatch at index {i}: expected {expected_results[i]['label']}, got {seg['label']}"


def test_process_segments_empty():
    # Ensure an empty list returns an empty list.
    segments = []
    processed = process_segments(segments)
    assert processed == []

def test_load_audio_to_memory(tmp_path, sample_audio):
    """Tests if load_audio_to_memory correctly loads an audio file into memory."""
    wav_path = tmp_path / "test.wav"
    sample_audio.export(wav_path, format="wav")

    loaded_audio = load_audio_to_memory(str(wav_path))

    compare_data = AudioSegment.from_file(loaded_audio)

    assert isinstance(loaded_audio, io.BytesIO), "Loaded audio should be an AudioSegment object" 
    assert compare_data == sample_audio, "Loaded audio data should match the original audio data"


def test_split_audio_memory():
    """Tests if split_audio_memory correctly extracts a segment from audio."""
    sample_audio = AudioSegment.from_file('./files/test.wav', format="wav")
    split_audio = split_audio_memory(sample_audio, 1984544 , 3125616)  

    assert isinstance(split_audio, AudioSegment), "Split audio should be an AudioSegment object"
    assert abs(len(split_audio) / 1000 - 23.773) < 0.001  # allowing tiny floating-point discrepancies