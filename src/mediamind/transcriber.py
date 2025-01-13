"""Audio transcription module using OpenAI's Whisper model."""

from pathlib import Path
from typing import Optional

import whisper
from rich.console import Console

from mediamind.exceptions import TranscriptionError

console = Console()


class Transcriber:
    """Handles audio transcription using OpenAI's Whisper model."""

    def __init__(self, model_name: str = "base") -> None:
        """Initialize the transcriber.

        Args:
            model_name: Name of the Whisper model to use
        """
        try:
            self.model = whisper.load_model(model_name)
        except Exception as e:
            raise TranscriptionError(f"Failed to load Whisper model: {str(e)}")

    def transcribe(self, audio_path: str, language: Optional[str] = None) -> str:
        """Transcribe an audio file.

        Args:
            audio_path: Path to the audio file
            language: Optional language code (e.g., "en" for English)

        Returns:
            Transcribed text

        Raises:
            TranscriptionError: If transcription fails
            FileNotFoundError: If audio file not found
        """
        try:
            # Verify file exists
            if not Path(audio_path).exists():
                raise FileNotFoundError(f"Audio file not found: {audio_path}")

            # Transcribe audio
            result = self.model.transcribe(
                audio_path,
                language=language,
                fp16=False,
            )

            return self._format_transcript(result["text"])

        except Exception as e:
            if isinstance(e, FileNotFoundError):
                raise
            raise TranscriptionError(f"Transcription failed: {str(e)}")

    def _format_transcript(self, text: str) -> str:
        """Format the transcribed text.

        Args:
            text: Raw transcribed text

        Returns:
            Formatted transcript text
        """
        # Remove extra whitespace and normalize line endings
        text = " ".join(text.split())

        # Add markdown formatting
        return f"# Transcript\n\n{text}\n"
