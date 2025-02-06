"""MediaMind CLI for processing video files."""

import datetime
import os
from typing import List, Optional

import click
from rich.console import Console

from mediamind.audio_processor import AudioProcessor
from mediamind.summarizer import Summarizer
from mediamind.transcriber import Transcriber

console = Console()


def process_file(
    file_path: str, summarize: bool = False, output_dir: str = "transcripts"
) -> None:
    """Process a single video file.

    Args:
        file_path: Path to the video file
        summarize: Whether to generate a summary
        output_dir: Directory to save output files
    """
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)

        # Initialize components
        processor = AudioProcessor()
        transcriber = Transcriber()
        summarizer_instance: Optional[Summarizer] = Summarizer() if summarize else None

        # Process video file
        console.print(f"Processing {file_path}...")
        audio_path = processor.process_file(file_path)

        try:
            # Transcribe audio
            console.print("Transcribing audio...")
            transcript = transcriber.transcribe(audio_path)

            # Format and save transcript
            current_time = datetime.datetime.now()
            file_timestamp = current_time.strftime("%Y-%m-%d %H-%M-%S")
            timestamp = current_time.strftime("%Y%m%d_%H%M%S")

            if summarize and summarizer_instance is not None:
                # Generate and save summary with transcript
                console.print("Generating summary...")
                summary = summarizer_instance.summarize(transcript)
                formatted_content = (
                    f"{summary}\n\n## Original Transcript\n\n{transcript}"
                )
            else:
                # Save transcript only
                formatted_content = f"# Transcript\n\n{transcript}"

            output_path = os.path.join(output_dir, f"{file_timestamp}_{timestamp}.md")
            with open(output_path, "w") as f:
                f.write(formatted_content)

        finally:
            # Clean up the temporary wav file
            if os.path.exists(audio_path):
                try:
                    os.remove(audio_path)
                    console.print(f"Cleaned up temporary audio file: {audio_path}")
                except Exception as e:
                    console.print(
                        f"Warning: Could not remove temporary audio file {audio_path}: {e}",
                        style="yellow",
                    )

        console.print("Processing complete!")

    except Exception as e:
        console.print(f"Error: {str(e)}", style="red")
        raise click.Abort()


@click.group()
def cli() -> None:
    """Mediamind CLI for processing video files."""
    pass


@cli.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.option(
    "--output-dir",
    type=click.Path(),
    default="transcripts",
    help="Directory to save output files",
)
@click.option(
    "--no-summary",
    is_flag=True,
    help="Skip generating a summary of the transcript",
)
def process(
    input_path: str, output_dir: str = "transcripts", no_summary: bool = False
) -> None:
    """Process a single video file.

    Args:
        input_path: Path to the video file to process
        output_dir: Directory to save output files
        no_summary: Whether to skip generating a summary
    """
    process_file(input_path, not no_summary, output_dir)


@cli.command()
@click.argument(
    "directory", type=click.Path(exists=True, file_okay=False, dir_okay=True)
)
@click.option(
    "--output-dir",
    type=click.Path(),
    default="transcripts",
    help="Directory to save output files",
)
@click.option(
    "--no-summary",
    is_flag=True,
    help="Skip generating summaries for transcripts",
)
def batch(
    directory: str, output_dir: str = "transcripts", no_summary: bool = False
) -> None:
    """Process all video files in a directory."""
    video_files: List[str] = []
    for file in os.listdir(directory):
        if file.lower().endswith((".mov", ".mp4")):
            video_files.append(os.path.join(directory, file))

    if not video_files:
        console.print("No media files found in directory")
        return

    for video_file in video_files:
        process_file(video_file, not no_summary, output_dir)


if __name__ == "__main__":
    cli()
