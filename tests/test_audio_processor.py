"""Tests for the audio processor module."""

from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from mediamind.audio_processor import AudioProcessor
from mediamind.exceptions import UnsupportedFormatError


@pytest.fixture
def audio_processor() -> AudioProcessor:
    """Create an AudioProcessor instance."""
    return AudioProcessor()


@pytest.fixture
def mock_video_file_clip() -> Mock:
    """Create a mock VideoFileClip."""
    mock = Mock()
    mock.audio = Mock()
    return mock


def test_init_verifies_dependencies(audio_processor: AudioProcessor) -> None:
    """Test that initialization verifies dependencies."""
    assert audio_processor is not None


def test_process_file_unsupported_format(
    audio_processor: AudioProcessor, tmp_path: Path
) -> None:
    """Test processing an unsupported file format."""
    # Create a test file
    test_file = tmp_path / "test.txt"
    test_file.touch()

    with pytest.raises(UnsupportedFormatError):
        audio_processor.process_file(str(test_file))


def test_process_file_not_found(audio_processor: AudioProcessor) -> None:
    """Test processing a non-existent file."""
    with pytest.raises(FileNotFoundError):
        audio_processor.process_file("nonexistent.mov")


@patch("mediamind.audio_processor.VideoFileClip")
def test_process_video_file(
    mock_video_file_clip: Mock, audio_processor: AudioProcessor, tmp_path: Path
) -> None:
    """Test processing a video file."""
    # Create test file
    test_file = tmp_path / "test.mov"
    test_file.touch()

    # Setup mock
    mock_video = Mock()
    mock_audio = Mock()
    mock_video.audio = mock_audio
    mock_video_file_clip.return_value = mock_video

    # Process file
    result = audio_processor.process_file(str(test_file))

    # Verify result
    assert result.endswith(".wav")
    mock_video_file_clip.assert_called_once()
    mock_audio.write_audiofile.assert_called_once()
    mock_video.close.assert_called_once()


@patch("mediamind.audio_processor.VideoFileClip")
def test_extract_audio_error(
    mock_video_file_clip: Mock, audio_processor: AudioProcessor, tmp_path: Path
) -> None:
    """Test error handling during audio extraction."""
    # Create test file
    test_file = tmp_path / "test.mov"
    test_file.touch()

    # Setup mock to raise an error
    mock_video_file_clip.side_effect = Exception("Mock error")

    # Attempt to process file
    with pytest.raises(RuntimeError):
        audio_processor.process_file(str(test_file))


@patch("mediamind.audio_processor.ffmpeg")
def test_get_audio_duration(mock_ffmpeg: Mock, audio_processor: AudioProcessor) -> None:
    """Test getting audio duration."""
    # Setup mock
    mock_ffmpeg.probe.return_value = {
        "streams": [{"codec_type": "audio", "duration": "10.5"}]
    }

    # Get duration
    duration = audio_processor.get_audio_duration("test.wav")

    # Verify result
    assert duration == 10.5
    mock_ffmpeg.probe.assert_called_once_with("test.wav")


@patch("mediamind.audio_processor.ffmpeg")
def test_get_audio_duration_error(
    mock_ffmpeg: Mock, audio_processor: AudioProcessor
) -> None:
    """Test error handling when getting audio duration."""
    # Setup mock to raise an error
    mock_ffmpeg.probe.side_effect = Exception("Mock error")

    # Attempt to get duration
    with pytest.raises(RuntimeError):
        audio_processor.get_audio_duration("test.wav")
