"""Custom exceptions for the MediaMind package."""


class MediaMindError(Exception):
    """Base exception for all MediaMind errors."""

    pass


class TranscriptionError(MediaMindError):
    """Raised when audio transcription fails."""

    pass


class SummarizationError(MediaMindError):
    """Raised when text summarization fails."""

    pass


class UnsupportedFormatError(MediaMindError):
    """Raised when an unsupported file format is encountered."""

    pass
