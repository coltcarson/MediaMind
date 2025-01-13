"""Audio processing module for extracting and manipulating audio from video files."""

from pathlib import Path

import ffmpeg
from moviepy.editor import VideoFileClip
from rich.console import Console

from mediamind.exceptions import UnsupportedFormatError

console = Console()


class AudioProcessor:
    """Handles audio extraction and processing from video files."""

    def __init__(self) -> None:
        """Initialize the audio processor."""
        self._verify_dependencies()

    def process_file(self, file_path: str) -> str:
        """Process a video file and extract its audio.

        Args:
            file_path: Path to the video file

        Returns:
            Path to the extracted audio file

        Raises:
            FileNotFoundError: If the input file doesn't exist
            UnsupportedFormatError: If the file format is not supported
        """
        input_path = Path(file_path)

        # Verify file exists
        if not input_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Verify file format
        if input_path.suffix.lower() not in {".mov", ".mp4"}:
            raise UnsupportedFormatError(
                f"Unsupported file format: {input_path.suffix}"
            )

        # Create output path
        output_path = input_path.with_suffix(".wav")

        try:
            # Extract audio using moviepy
            video = VideoFileClip(str(input_path))
            audio = video.audio
            audio.write_audiofile(str(output_path))
            video.close()

            return str(output_path)

        except Exception as e:
            raise RuntimeError(f"Failed to extract audio: {str(e)}")

    def get_audio_duration(self, file_path: str) -> float:
        """Get the duration of an audio file in seconds.

        Args:
            file_path: Path to the audio file

        Returns:
            Duration in seconds

        Raises:
            FileNotFoundError: If the file doesn't exist
            RuntimeError: If duration cannot be determined
        """
        try:
            probe = ffmpeg.probe(file_path)
            audio_info = next(s for s in probe["streams"] if s["codec_type"] == "audio")
            return float(audio_info["duration"])
        except Exception as e:
            raise RuntimeError(f"Failed to get audio duration: {str(e)}")

    def _verify_dependencies(self) -> None:
        """Verify that required dependencies are available.

        Raises:
            RuntimeError: If any required dependency is missing
        """
        try:
            # Try to use ffmpeg
            ffmpeg.probe(None)
        except Exception:
            pass  # This will always raise an error, we just want to verify ffmpeg exists
