import pytest
from app.services.text_to_speech import TextToSpeechService

@pytest.fixture
def text_to_speech_service():
    return TextToSpeechService()

def test_convert_text_to_speech(text_to_speech_service):
    text = "Hello, this is a test."
    audio_output = text_to_speech_service.convert_text_to_speech(text)
    assert audio_output is not None
    assert isinstance(audio_output, bytes)  # Assuming the output is in bytes format

def test_convert_empty_text_to_speech(text_to_speech_service):
    text = ""
    audio_output = text_to_speech_service.convert_text_to_speech(text)
    assert audio_output is None  # Assuming the service returns None for empty input

def test_convert_text_to_speech_invalid_input(text_to_speech_service):
    text = 12345  # Invalid input type
    with pytest.raises(TypeError):
        text_to_speech_service.convert_text_to_speech(text)