"""Shared pytest fixtures."""

from pathlib import Path
from unittest.mock import Mock

import pytest


@pytest.fixture
def sample_audio_file(tmp_path: Path) -> str:
    """Create a temporary WAV file for testing."""
    audio_file = tmp_path / "test.wav"
    audio_file.touch()
    return str(audio_file)


@pytest.fixture
def sample_video_file(tmp_path: Path) -> str:
    """Create a temporary MP4 file for testing."""
    video_file = tmp_path / "test.mp4"
    video_file.touch()
    return str(video_file)


@pytest.fixture
def mock_openai_response() -> dict:
    """Create a mock OpenAI API response."""
    return {
        "choices": [
            {"message": {"content": "Sample summary of the transcribed content."}}
        ]
    }


@pytest.fixture
def mock_progress() -> Mock:
    """Create a mock Progress instance."""
    progress = Mock()
    progress.add_task.return_value = 1
    return progress
