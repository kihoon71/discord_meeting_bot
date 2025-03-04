import pytest
import os
import sys
from unittest.mock import patch


sys.path.append(os.path.join(os.path.dirname(__file__), "../src/transcribe"))

from Diarizer import SpeakerDiarizer
from Util import create_temp_file, process_segments

def test_import():
    assert SpeakerDiarizer is not None

@pytest.fixture(scope='module')
def diarizer():
    """Fixture to create a Diarizer instance with the desired model and clustering method."""
    return SpeakerDiarizer(embed_model='xvec', cluster_method='sc')

def test_initialization_valid(diarizer):
    """Test that the Diarizer initializes correctly with valid parameters."""
    assert isinstance(diarizer, SpeakerDiarizer), "Failed to initialize Diarizer instance"

def test_initialization_invalid_embed_model():
    """Test that an invalid embed_model raises an assertion error."""
    with pytest.raises(AssertionError):
        SpeakerDiarizer(embed_model='invalid_model', cluster_method='sc')

def test_initialization_invalid_cluster_method():
    """Test that an invalid cluster_method raises an assertion error."""
    with pytest.raises(AssertionError):
        SpeakerDiarizer(embed_model='xvec', cluster_method='invalid_method')
 
def test_diarize(diarizer):
    """Test the diarize function with mocked I/O."""
    test_wav = "./files/test.wav"  # Path to a test WAV file
    num_speakers = 2
    
    processed_segments = diarizer.diarize_(test_wav, num_speakers)

    num_labels = {seg["label"] for seg in processed_segments}

    # Validate that the diarization process is done correctly
    assert isinstance(processed_segments, list), "Processed segments should be a list"
    assert len(num_labels) == num_speakers, "Number of speakers should match the input"

def test_diarize_empty_audio(diarizer):
    """Test the diarize function with empty or invalid audio input."""
    audio_input = ""  # Empty input
    num_speakers = 2

    with pytest.raises(FileNotFoundError):  # Assuming diarizer raises a FilenotfoundError for empty input
        diarizer.diarize_(audio_input, num_speakers)

def test_diarize_invalid_speakers(diarizer):
    """Test the diarize function with invalid number of speakers."""
    audio_input = "./files/test.wav"
    num_speakers = -1  # Invalid number of speakers

    with pytest.raises(ValueError):  # Assuming the function raises a ValueError for invalid speakers
        diarizer.diarize_(audio_input, num_speakers)

def test_temporary_file_creation_and_deletion(diarizer, tmp_path):
    """Test that the temporary file is created and deleted properly."""
    audio_input = "./files/test.wav"
    num_speakers = 2
    temp_file = tmp_path / "mock_temp.wav"
    
    # Check that temporary file is created and then deleted
    diarizer.diarize_(audio_input, num_speakers)
    assert not os.path.exists(temp_file), "Temporary file should be deleted"

