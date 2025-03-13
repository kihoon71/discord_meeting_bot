import sys
import os
import pytest_asyncio
import pytest
from io import BytesIO
from pydub import AudioSegment

sys.path.append(os.path.join(os.path.dirname(__file__), "../src/UTIL"))

from Audio import Audio
from Text import Text

@pytest.fixture(scope='module')
def audio():
    return Audio()

@pytest.fixture(scope='module')
def wav_file():
    return AudioSegment.silent(duration=1000, frame_rate=44100)

# Test get_audio_none
def test_get_audio_none(audio):
    assert audio.get_audio('test') == None

# Test set_audio
@pytest.mark.asyncio
async def test_set_audio(audio, wav_file):
    await audio.set_audio('test1', wav_file)
    await audio.set_audio('test2', wav_file)
    await audio.set_audio('test3', wav_file)
    assert audio.get_audio('test1') == wav_file
    assert audio.get_audio('test2') == wav_file
    assert audio.get_audio('test3') == wav_file

@pytest.mark.asyncio
async def test_invalid_file_type(audio, wav_file):
    with pytest.raises(ValueError):
        await audio.set_audio('test', 'test')

#test with the on memory audio file
@pytest.mark.asyncio
async def test_invalid_file_extension(audio, wav_file):
    memory_wav_file = BytesIO()
    memory_wav_file.name = 'test.wav'
    wav_file.export(memory_wav_file, format='mp3')
    memory_wav_file.seek(0)

    await audio.set_audio('test-memory', wav_file)
    assert audio.get_audio('test-memory') == wav_file

def test_clear_audio(audio):
    audio.clear_audio('test1')
    audio.clear_audio('test2')
    audio.clear_audio('test3')
    assert 'test1' not in audio.data
    assert 'test2' not in audio.data
    assert 'test3' not in audio.data

def test_is_same_instance():
    audio_instance1 = Audio()
    audio_instance2 = Audio()
    assert audio_instance1 == audio_instance2
    assert audio_instance1 is audio_instance2
    assert id(audio_instance1) == id(audio_instance2)

def test_text_audio_is_different_instance():
    text_instance = Text()
    audio_instance = Audio()
    assert text_instance != audio_instance
    assert text_instance is not audio_instance
    assert id(text_instance) != id(audio_instance)
    

