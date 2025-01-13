"""Tests for the transcriber module."""

from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from mediamind.exceptions import TranscriptionError
from mediamind.transcriber import Transcriber


@pytest.fixture
def transcriber() -> Transcriber:
    """Create a Transcriber instance."""
    return Transcriber()


def test_init_loads_model() -> None:
    """Test that initialization loads the Whisper model."""
    with patch("whisper.load_model") as mock_load:
        transcriber = Transcriber()
        mock_load.assert_called_once_with("base")


def test_init_error() -> None:
    """Test error handling during initialization."""
    with patch("whisper.load_model", side_effect=Exception("Mock error")):
        with pytest.raises(TranscriptionError):
            Transcriber()


def test_transcribe_file_not_found(transcriber: Transcriber) -> None:
    """Test transcribing a non-existent file."""
    with pytest.raises(FileNotFoundError):
        transcriber.transcribe("nonexistent.wav")


@patch("whisper.load_model")
def test_transcribe_success(mock_load: Mock) -> None:
    """Test successful transcription."""
    # Setup mock model
    mock_model = Mock()
    mock_model.transcribe.return_value = {
        "text": "Test transcription",
        "language": "en",
    }
    mock_load.return_value = mock_model

    # Create test file
    test_file = "test.wav"
    Path(test_file).touch()

    # Transcribe
    transcriber = Transcriber()
    result = transcriber.transcribe(test_file)

    # Verify result
    assert "Test transcription" in result
    mock_model.transcribe.assert_called_once_with(test_file, language=None, fp16=False)

    # Cleanup
    Path(test_file).unlink()


@patch("whisper.load_model")
def test_transcribe_with_language(mock_load: Mock) -> None:
    """Test transcription with specified language."""
    # Setup mock model
    mock_model = Mock()
    mock_model.transcribe.return_value = {
        "text": "Test transcription",
        "language": "es",
    }
    mock_load.return_value = mock_model

    # Create test file
    test_file = "test.wav"
    Path(test_file).touch()

    # Transcribe
    transcriber = Transcriber()
    result = transcriber.transcribe(test_file, language="es")

    # Verify result
    assert "Test transcription" in result
    mock_model.transcribe.assert_called_once_with(test_file, language="es", fp16=False)

    # Cleanup
    Path(test_file).unlink()


@patch("whisper.load_model")
def test_transcribe_error(mock_load: Mock) -> None:
    """Test error handling during transcription."""
    # Setup mock model
    mock_model = Mock()
    mock_model.transcribe.side_effect = Exception("Mock error")
    mock_load.return_value = mock_model

    # Create test file
    test_file = "test.wav"
    Path(test_file).touch()

    # Attempt transcription
    transcriber = Transcriber()
    with pytest.raises(TranscriptionError):
        transcriber.transcribe(test_file)

    # Cleanup
    Path(test_file).unlink()
