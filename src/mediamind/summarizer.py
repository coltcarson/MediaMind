"""Module for generating summaries using OpenAI's GPT API."""

import os
from pathlib import Path
from typing import Dict, Optional

import openai
from dotenv import load_dotenv

from mediamind.exceptions import SummarizationError


class Summarizer:
    """Class for generating summaries using OpenAI's GPT API."""

    def __init__(self) -> None:
        """Initialize the summarizer with API configuration."""
        # Load environment variables from .env file
        env_path = Path(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        ).joinpath(".env")
        load_dotenv(env_path)

        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise SummarizationError(
                "OpenAI API key not found. Please set OPENAI_API_KEY "
                "in your .env file."
            )
        openai.api_key = self.api_key

    def _create_prompt(
        self, text: str, max_length: Optional[int] = None, style: Optional[str] = None
    ) -> Dict[str, str]:
        """Create the prompt for the GPT model.

        Args:
            text: The text to summarize
            max_length: Maximum length of the summary in sentences
            style: Style of summary to generate (concise, detailed, bullets)

        Returns:
            Dictionary containing system and user prompts
        """
        system_prompt = (
            "You are an expert at summarizing meeting transcripts into structured meeting minutes. "
            "Extract and organize key information including participants, discussion points, "
            "decisions, and action items. Format the output in a clear, professional markdown structure. "
            "Do not include any duplicate headers or sections."
        )

        user_prompt = (
            "Analyze the following meeting transcript and create detailed meeting minutes following this exact format:\n\n"
            "# Meeting Minutes (Generated: <current_timestamp>)\n\n"
            "**Meeting Overview:**\n"
            "- **Date:** <extract_date_or_write_not_specified>\n"
            "- **Main Topic:** <extract_main_topic>\n\n"
            "**Participants:**\n"
            "<list_of_participants_from_transcript>\n\n"
            "**Key Discussion Points:**\n"
            "<bullet_points_of_main_topics>\n\n"
            "**Important Decisions Made:**\n"
            "<bullet_points_of_decisions>\n\n"
            "**Action Items:**\n"
            "<list_using_format: [Owner] - Task description - [Due: Date]>\n\n"
            "**Follow-up Meetings or Deadlines:**\n"
            "<description_of_next_steps>\n\n"
            "Rules:\n"
            "1. Do not include any duplicate headers\n"
            "2. Use bullet points for lists\n"
            "3. For action items, use exactly this format: [Owner] - Task - [Due: Date]\n"
            "4. If a date or owner is not specified, write 'Not specified'\n"
            "5. Extract participant names carefully from the transcript\n"
            "6. Keep the exact section titles and formatting\n\n"
            f"Here's the transcript to analyze:\n\n{text}"
        )

        if max_length:
            user_prompt += (
                f"\n\nLimit the summary to approximately {max_length} key points."
            )
        if style:
            user_prompt += f"\n\nUse a {style} style."

        return {
            "system": system_prompt,
            "user": user_prompt,
        }

    def summarize(
        self, text: str, max_length: Optional[int] = None, style: Optional[str] = None
    ) -> str:
        """Generate a summary of the input text.

        Args:
            text: The text to summarize
            max_length: Maximum length of the summary in sentences
            style: Style of summary to generate (concise, detailed, bullets)

        Returns:
            Generated summary text

        Raises:
            SummarizationError: If summarization fails
        """
        try:
            # Validate input
            if not text.strip():
                raise SummarizationError("Input text is empty")

            if max_length is not None and max_length <= 0:
                raise SummarizationError("max_length must be positive")

            # Create prompt
            prompts = self._create_prompt(text, max_length, style)

            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": prompts["system"]},
                    {"role": "user", "content": prompts["user"]},
                ],
                temperature=0.7,
                max_tokens=1000,
            )

            # Extract and return the summary
            return str(response.choices[0].message.content)

        except Exception as e:
            raise SummarizationError(f"Failed to generate summary: {str(e)}")
