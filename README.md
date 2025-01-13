# 🎥 MediaMind

MediaMind is an AI-powered tool that transcribes and summarizes .mov video files using OpenAI's Whisper model for transcription and GPT-4o for summarization.

## ✨ Features

- 🎬 Specialized .mov video file processing
- 🔊 Audio extraction from video files
- 🎯 Transcription using OpenAI's Whisper
- 🤖 Intelligent summarization using GPT-4o
- 📝 Markdown output for transcriptions and summaries
- 💻 Command-line interface for batch processing
- 📊 Progress tracking for long-running tasks
- 🔒 Secure API key handling

## 🚀 Installation

1. 📥 Clone the repository:
   ```bash
   git clone https://github.com/yourusername/mediamind.git
   cd mediamind
   ```

2. 🐍 Set up Python virtual environment (requires Python 3.11):
   ```bash
   # Create virtual environment
   python3.11 -m venv venv

   # Activate virtual environment (macOS/Linux)
   source venv/bin/activate

   # Activate virtual environment (Windows)
   .\venv\Scripts\activate
   ```

3. 🎵 Install FFmpeg (required for media processing):
   ```bash
   # macOS (using Homebrew)
   brew install ffmpeg

   # Ubuntu/Debian
   sudo apt-get install ffmpeg

   # Windows (using Chocolatey)
   choco install ffmpeg
   ```

4. 📦 Install the package and dependencies:
   ```bash
   # Install in development mode
   pip install -e .

   # Install dependencies
   pip install -r requirements.txt

   # Optional: Install development dependencies
   pip install -r requirements-dev.txt
   ```

## ⚙️ Configuration

1. 📄 Copy `.env.example` to `.env`
   ```bash
   cp .env.example .env
   ```

2. 🔑 Add your OpenAI API key to `.env`:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```

## 📚 Usage

Make sure your virtual environment is activated:
```bash
source venv/bin/activate  # macOS/Linux
.\venv\Scripts\activate   # Windows
```

### Process a single .mov file:
```bash
python -m mediamind process "path/to/your/video.mov"
```

### Batch process multiple .mov files in a directory:
```bash
python -m mediamind batch "path/to/directory"
```

### Generate summary from an existing transcript:
```bash
python -m mediamind summarize "path/to/transcript.md"
```

### Output
Transcripts and summaries are saved in the `transcripts` directory with timestamps:
```
transcripts/
├── video_20250112_103121.md
└── video_summary_20250112_103121.md
```

## 🏗️ Project Structure

```
mediamind/
├── src/mediamind/         # Source code
│   ├── __init__.py       # Package initialization
│   ├── __main__.py       # CLI entry point
│   ├── audio_processor.py # Audio processing module
│   ├── summarizer.py     # Text summarization module
│   └── transcriber.py    # Audio transcription module
├── tests/                # Test files
│   ├── conftest.py      # Shared test fixtures
│   ├── test_audio_processor.py
│   ├── test_summarizer.py
│   └── test_transcriber.py
├── .env.example         # Example environment variables
├── .pre-commit-config.yaml
├── LICENSE
├── README.md
├── requirements.txt     # Production dependencies
└── requirements-dev.txt # Development dependencies
```

## 📝 Example Outputs

### 📜 Transcription Output
```markdown
# Video: interview.mov
## Timestamp: 00:00:00 - 00:00:30
Speaker 1: Welcome to our tech talk. Today we're discussing AI and its impact...

## Timestamp: 00:00:30 - 00:01:00
Speaker 2: Thank you for having me. I believe AI will revolutionize...
```

### 📋 Summary Output
```markdown
# Summary: interview.mov

## Key Points
- Discussion focused on AI's impact on technology
- Speakers explored future applications
- Highlighted ethical considerations

## Main Topics
1. Current state of AI technology
2. Future developments
3. Ethical implications

## Action Items
- Research specific use cases
- Follow up on regulatory frameworks
- Schedule follow-up discussion
```

## 🔧 API Documentation

### 🎵 AudioProcessor
```python
def process_file(file_path: str) -> str:
    """Process audio/video file and extract audio.

    Args:
        file_path: Path to the input media file

    Returns:
        Path to the extracted audio file

    Raises:
        UnsupportedFormatError: If file format is not supported
        FileNotFoundError: If input file doesn't exist
    """
```

### 🎤 Transcriber
```python
def transcribe(audio_path: str) -> str:
    """Transcribe audio file using OpenAI Whisper.

    Args:
        audio_path: Path to the audio file

    Returns:
        Markdown formatted transcription
    """
```

### 📝 Summarizer
```python
def summarize(transcript: str) -> str:
    """Generate summary from transcript using GPT-4o.

    Args:
        transcript: Markdown formatted transcript

    Returns:
        Markdown formatted summary
    """
```

## ⚠️ Error Handling

The application handles the following errors:
- `UnsupportedFormatError`: Raised when input file format is not supported
- `FileNotFoundError`: Raised when input file doesn't exist
- `APIError`: Raised when there are issues with OpenAI API calls
- `TranscriptionError`: Raised when transcription fails
- `SummarizationError`: Raised when summary generation fails

## 👩‍💻 Development

1. 📦 Set up the development environment:
   ```bash
   # Install all dependencies and set up pre-commit hooks
   make install
   ```

2. 🧪 Run tests:
   ```bash
   # Run all tests with coverage report
   make test
   ```

3. 🔍 Run linting and type checking:
   ```bash
   # Run all pre-commit hooks
   make lint
   ```

4. 🧹 Clean up generated files:
   ```bash
   make clean
   ```

5. 📝 Update dependencies:
   ```bash
   # Update requirements.txt and requirements-dev.txt
   make update-deps
   ```

## 🤝 Contributing

Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 🔄 Continuous Integration

We use GitHub Actions for continuous integration. Every pull request will automatically:
- Run all tests
- Check code formatting (black)
- Run linting (flake8)
- Check import sorting (isort)
- Perform type checking (mypy)
- Generate test coverage report

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for the Whisper and GPT-4o models
- FFmpeg for media processing capabilities
- All our contributors and users
