"""Module for generating summaries using OpenAI's GPT API."""

import os
from pathlib import Path
from typing import Dict, List, Optional, cast

import openai
import tiktoken
from dotenv import load_dotenv

from mediamind.exceptions import SummarizationError


class Summarizer:
    """Class for generating summaries using OpenAI's GPT API."""

    def __init__(self) -> None:
        """Initialize the Summarizer.

        Raises:
            ValueError: If OPENAI_API_KEY is not set
        """
        # Try to load environment variables from .env file
        try:
            base_path = Path(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            )
            env_path = base_path / ".env"
            if env_path.exists():
                load_dotenv(env_path)
        except Exception:
            pass  # Ignore .env loading errors

        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        openai.api_key = self.api_key
        self.encoding = tiktoken.encoding_for_model("gpt-4o")
        # Set chunk sizes with some buffer for prompt and completion
        self.max_chunk_tokens = 96000  # 75% of model's context length for input
        self.max_completion_tokens = 16000  # Maximum allowed completion tokens

    def _count_tokens(self, text: str) -> int:
        """Count the number of tokens in a text string.

        Args:
            text: The text to count tokens for

        Returns:
            Number of tokens
        """
        return len(self.encoding.encode(text))

    def _split_text(self, text: str) -> List[str]:
        """Split text into chunks that fit within token limits.

        Args:
            text: The text to split

        Returns:
            List of text chunks
        """
        paragraphs = text.split("\n\n")
        chunks = []
        current_chunk = []
        current_tokens = 0

        for paragraph in paragraphs:
            paragraph_tokens = self._count_tokens(paragraph)

            if current_tokens + paragraph_tokens > self.max_chunk_tokens:
                if current_chunk:  # Save current chunk if it exists
                    chunks.append("\n\n".join(current_chunk))
                current_chunk = [paragraph]
                current_tokens = paragraph_tokens
            else:
                current_chunk.append(paragraph)
                current_tokens += paragraph_tokens

        if current_chunk:  # Add the last chunk
            chunks.append("\n\n".join(current_chunk))

        return chunks

    def _combine_summaries(self, summaries: List[str]) -> str:
        """Combine multiple summaries into a single coherent summary.

        Args:
            summaries: List of summaries to combine

        Returns:
            Combined summary
        """
        if len(summaries) == 1:
            return summaries[0]

        combine_prompt = (
            "Below are multiple sections of meeting minutes from the same meeting. "
            "Please combine them into a single, coherent set of meeting minutes, "
            "removing any duplicates and maintaining the same format. "
            "Ensure all unique information is preserved.\n\n"
            "Sections to combine:\n\n" + "\n---\n".join(summaries)
        )

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at combining meeting minutes into a single coherent summary.",
                    },
                    {"role": "user", "content": combine_prompt},
                ],
                temperature=0.7,
                max_tokens=self.max_completion_tokens,
            )
            return cast(str, response.choices[0].message.content).strip()
        except Exception as e:
            raise SummarizationError(f"Failed to combine summaries: {str(e)}")

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
            ValueError: If input text is empty or max_length is invalid
            SummarizationError: If summarization fails
        """
        # Validate input
        if not text.strip():
            raise ValueError("Input text is empty")

        if max_length is not None and max_length <= 0:
            raise ValueError("Invalid max_length: must be positive")

        try:
            # Split text into chunks if necessary
            text_chunks = self._split_text(text)
            summaries = []

            # Process each chunk
            for chunk in text_chunks:
                # Create prompt
                prompts = self._create_prompt(chunk, max_length, style)

                # Call OpenAI API
                response = openai.ChatCompletion.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": prompts["system"]},
                        {"role": "user", "content": prompts["user"]},
                    ],
                    temperature=0.7,
                    max_tokens=self.max_completion_tokens,
                )

                # Extract summary
                message_content = cast(str, response.choices[0].message.content)
                summary = message_content.strip()
                if not summary:
                    raise SummarizationError("Generated summary is empty")
                summaries.append(summary)

            # Combine summaries if there are multiple chunks
            final_summary = self._combine_summaries(summaries)
            if not final_summary:
                raise SummarizationError("Generated summary is empty")

            return final_summary

        except ValueError as e:
            raise e
        except Exception as e:
            raise SummarizationError(f"Failed to generate summary: {str(e)}")
