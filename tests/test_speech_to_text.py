import pytest
from app.api.endpoints.speech_to_text import SpeechToTextEndpoint

@pytest.fixture
def speech_to_text_endpoint():
    return SpeechToTextEndpoint()

def test_convert_speech_to_text(speech_to_text_endpoint):
    # Mock input for testing
    mock_audio_input = "path/to/mock/audio/file.wav"
    
    # Call the method to test
    result = speech_to_text_endpoint.convert_speech_to_text(mock_audio_input)
    
    # Assert the expected output
    assert isinstance(result, str)  # Ensure the result is a string
    assert result != ""  # Ensure the result is not empty

def test_convert_speech_to_text_invalid_input(speech_to_text_endpoint):
    # Test with invalid input
    invalid_audio_input = "invalid/path/to/audio/file.wav"
    
    with pytest.raises(FileNotFoundError):
        speech_to_text_endpoint.convert_speech_to_text(invalid_audio_input)