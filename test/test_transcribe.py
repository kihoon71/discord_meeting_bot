import pytest
import pytest_asyncio
import os
import sys
import io
import dotenv
from pydub import AudioSegment

sys.path.append(os.path.join(os.path.dirname(__file__), "../src/transcribe"))

from Util import load_audio_to_memory
from Transcribe import Transcribe
from Text import Text


@pytest.fixture(scope="module")
def api_key():
    env_path = dotenv.find_dotenv()
    dotenv.load_dotenv(env_path)
    api_key = os.getenv("OPENAI_API_KEY")
    assert api_key is not None
    return api_key 


def test_dotenv(api_key):
    assert api_key is not None

@pytest.fixture(scope="module")
def transcribe():
    assert Transcribe is not None
    transcribe = Transcribe(
        api_key=os.getenv("OPENAI_API_KEY")
    )

    return transcribe


@pytest.mark.asyncio
async def test_transcription(transcribe):
    audio = load_audio_to_memory('./files/test.wav')
    print(type(audio))
    
    result = await transcribe.transcribe(audio)
    assert result is not None
    print(result)
    assert isinstance(result, list)
    assert isinstance(result[0], str)


    
