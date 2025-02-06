#!/bin/bash

# Exit on any error
set -e

# Check if input directory is provided
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <input_directory> [output_directory]"
    echo "Example: $0 /path/to/videos /path/to/output"
    exit 1
fi

# Directory containing .mov files to process
TARGET_DIR="$1"

# Output directory (optional)
OUTPUT_DIR="${2:-transcripts}"

# Path to virtual environment
VENV_PATH="$(dirname "$0")/venv"

# Check if directories exist
if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Input directory '$TARGET_DIR' does not exist"
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Activate virtual environment
source "$VENV_PATH/bin/activate"

echo "🎬 Processing .mov files in $TARGET_DIR..."
echo "📝 Saving transcripts to $OUTPUT_DIR..."

# Run MediaMind batch processing
python -m mediamind batch "$TARGET_DIR" --output-dir "$OUTPUT_DIR"

echo "✨ Processing complete!"

