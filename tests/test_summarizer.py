"""Tests for the summarizer module."""

import os
from unittest.mock import Mock, patch

import pytest
from openai.error import AuthenticationError

from mediamind.exceptions import SummarizationError
from mediamind.summarizer import Summarizer


@pytest.fixture
def mock_openai():
    """Mock OpenAI API."""
    with patch("openai.ChatCompletion") as mock_chat:
        mock_chat.create.return_value.choices = [
            Mock(message=Mock(content="Test summary"))
        ]
        yield mock_chat


@pytest.fixture
def summarizer():
    """Create a Summarizer instance with mocked API key."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        return Summarizer()


def test_create_prompt(summarizer: Summarizer) -> None:
    """Test prompt creation."""
    prompt = summarizer._create_prompt("Test text", 3)
    assert isinstance(prompt, dict)
    assert "system" in prompt
    assert "user" in prompt


def test_summarize_empty_text(summarizer: Summarizer) -> None:
    """Test summarizing empty text."""
    with pytest.raises(SummarizationError, match="Input text is empty"):
        summarizer.summarize("")


def test_summarize_invalid_sentences(summarizer: Summarizer) -> None:
    """Test summarizing with invalid sentence count."""
    with pytest.raises(SummarizationError, match="Invalid max_length"):
        summarizer.summarize("Test text", 0)


@patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
def test_summarize_success(mock_openai) -> None:
    """Test successful summarization."""
    summarizer = Summarizer()
    summary = summarizer.summarize("Test text")
    assert summary == "Test summary"
    mock_openai.create.assert_called_once()


@patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
def test_summarize_api_error(mock_openai) -> None:
    """Test handling of API errors."""
    mock_openai.create.side_effect = AuthenticationError("API Error")
    summarizer = Summarizer()
    with pytest.raises(SummarizationError, match="Failed to generate summary"):
        summarizer.summarize("Test text")


def test_summarizer_init_no_api_key() -> None:
    """Test that Summarizer raises error when no API key is provided."""
    with pytest.raises(ValueError):
        Summarizer()


def test_summarizer_init_with_api_key() -> None:
    """Test that Summarizer initializes correctly with API key."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        summarizer = Summarizer()
        assert summarizer.api_key == "test-key"


@patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
def test_summarize_empty_text(mock_openai_response: dict) -> None:
    """Test that summarize raises error with empty text."""
    summarizer = Summarizer()
    with pytest.raises(ValueError):
        summarizer.summarize("")


@patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
def test_summarize_success(mock_openai_response: dict) -> None:
    """Test successful summarization."""
    summarizer = Summarizer()
    summary = summarizer.summarize("Test text")
    assert summary == "Test summary"


@patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
def test_summarize_api_error(mock_openai_response: dict) -> None:
    """Test error handling during summarization."""
    summarizer = Summarizer()
    with pytest.raises(SummarizationError, match="Failed to generate summary"):
        summarizer.summarize("Test text")
