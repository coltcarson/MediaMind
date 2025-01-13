"""Tests for the summarizer module."""

import os
from unittest.mock import Mock, patch

import pytest
from openai.error import AuthenticationError

from mediamind.summarizer import SummarizationError, Summarizer


def test_summarizer_init_no_api_key() -> None:
    """Test that Summarizer raises error when no API key is provided."""
    with patch("mediamind.summarizer.load_dotenv", return_value=None):
        with patch.dict(os.environ, {}, clear=True):  # Remove all env vars
            with pytest.raises(
                ValueError, match="OPENAI_API_KEY environment variable is not set"
            ):
                Summarizer()


def test_summarizer_init_with_api_key() -> None:
    """Test that Summarizer initializes correctly with API key."""
    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        summarizer = Summarizer()
        assert summarizer.api_key == "test-key"


@patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
def test_summarize_empty_text() -> None:
    """Test that summarize raises error with empty text."""
    summarizer = Summarizer()
    with pytest.raises(ValueError, match="Input text is empty"):
        summarizer.summarize("")


@patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"})
def test_summarize_invalid_sentences() -> None:
    """Test summarizing with invalid sentence count."""
    summarizer = Summarizer()
    with pytest.raises(ValueError, match="Invalid max_length: must be positive"):
        summarizer.summarize("Test text", max_length=0)


@patch("openai.ChatCompletion.create")
def test_summarize_success(mock_create: Mock) -> None:
    """Test successful summarization."""
    mock_create.return_value.choices = [Mock(message=Mock(content="Test summary"))]

    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        summarizer = Summarizer()
        summary = summarizer.summarize("Test text")
        assert summary == "Test summary"


@patch("openai.ChatCompletion.create")
def test_summarize_api_error(mock_create: Mock) -> None:
    """Test error handling during summarization."""
    mock_create.side_effect = AuthenticationError("Invalid API key")

    with patch.dict(os.environ, {"OPENAI_API_KEY": "test-key"}):
        summarizer = Summarizer()
        with pytest.raises(
            SummarizationError, match="Failed to generate summary: Invalid API key"
        ):
            summarizer.summarize("Test text")
