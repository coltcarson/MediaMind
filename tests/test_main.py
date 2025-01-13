"""Tests for the main CLI module."""

from datetime import datetime
from pathlib import Path
from typing import Dict
from unittest.mock import Mock, patch

import pytest
from click.testing import CliRunner

from mediamind.__main__ import cli


@pytest.fixture
def cli_runner() -> CliRunner:
    """Create a CliRunner instance."""
    return CliRunner()


@pytest.fixture
def mock_components():
    """Mock the main components."""
    with patch("mediamind.__main__.AudioProcessor") as mock_processor, patch(
        "mediamind.__main__.Transcriber"
    ) as mock_transcriber, patch("mediamind.__main__.Summarizer") as mock_summarizer:
        # Setup mock instances
        processor_instance = Mock()
        transcriber_instance = Mock()
        summarizer_instance = Mock()

        # Configure return values
        processor_instance.process_file.return_value = "test.wav"
        transcriber_instance.transcribe.return_value = "Test transcript"
        summarizer_instance.summarize.return_value = "Test summary"

        # Configure the mocks to return our instances
        mock_processor.return_value = processor_instance
        mock_transcriber.return_value = transcriber_instance
        mock_summarizer.return_value = summarizer_instance

        yield {
            "processor": processor_instance,
            "transcriber": transcriber_instance,
            "summarizer": summarizer_instance,
        }


def test_cli_help(cli_runner: CliRunner) -> None:
    """Test the CLI help output."""
    result = cli_runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "MediaMind CLI" in result.output


@patch("mediamind.__main__.datetime")
def test_process_command_with_summary(
    mock_datetime: Mock,
    cli_runner: CliRunner,
    mock_components: Dict,
    tmp_path: Path,
) -> None:
    """Test processing a single file with summary."""
    # Create test file
    test_file = tmp_path / "test.mov"
    test_file.touch()

    # Mock datetime
    mock_datetime.now.return_value = datetime(2025, 1, 13, 11, 9, 3)

    result = cli_runner.invoke(cli, ["process", str(test_file), "--summarize"])

    assert result.exit_code == 0
    assert "Processing complete" in result.output


def test_process_command_no_summary(
    cli_runner: CliRunner, mock_components: Dict, tmp_path: Path
) -> None:
    """Test processing a single file without summary."""
    # Create test file
    test_file = tmp_path / "test.mov"
    test_file.touch()

    result = cli_runner.invoke(cli, ["process", str(test_file)])

    assert result.exit_code == 0
    assert "Processing complete" in result.output


def test_process_command_error(
    cli_runner: CliRunner, mock_components: Dict, tmp_path: Path
) -> None:
    """Test error handling in process command."""
    # Create test file
    test_file = tmp_path / "test.mov"
    test_file.touch()

    # Make processor raise an error
    mock_components["processor"].process_file.side_effect = Exception("Test error")

    result = cli_runner.invoke(cli, ["process", str(test_file)])

    assert "Error" in result.output
    assert result.exit_code == 1


def test_batch_command(
    cli_runner: CliRunner, mock_components: Dict, tmp_path: Path
) -> None:
    """Test batch processing directory."""
    # Create test files
    media_dir = tmp_path / "media"
    media_dir.mkdir()

    test_files = [
        media_dir / "test1.mov",
        media_dir / "test2.mp4",
    ]
    for file in test_files:
        file.touch()

    result = cli_runner.invoke(cli, ["batch", str(media_dir)])

    assert result.exit_code == 0
    assert "Processing complete" in result.output
    assert mock_components["processor"].process_file.call_count == len(test_files)


def test_batch_command_no_files(
    cli_runner: CliRunner, mock_components: Dict, tmp_path: Path
) -> None:
    """Test batch processing with no media files."""
    # Create empty directory
    media_dir = tmp_path / "media"
    media_dir.mkdir()

    result = cli_runner.invoke(cli, ["batch", str(media_dir)])

    assert result.exit_code == 0
    assert "No media files found" in result.output


def test_batch_command_error(
    cli_runner: CliRunner, mock_components: Dict, tmp_path: Path
) -> None:
    """Test error handling in batch command."""
    # Create test file
    media_dir = tmp_path / "media"
    media_dir.mkdir()
    test_file = media_dir / "test.mov"
    test_file.touch()

    # Make processor raise an error
    mock_components["processor"].process_file.side_effect = Exception("Test error")

    result = cli_runner.invoke(cli, ["batch", str(media_dir)])

    assert "Error" in result.output
    assert result.exit_code == 1
