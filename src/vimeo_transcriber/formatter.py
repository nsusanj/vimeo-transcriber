from __future__ import annotations

import logging

import anthropic

from .config import CLAUDE_MODEL

log = logging.getLogger(__name__)

SYSTEM_PROMPT = """\
You are a professional editor specializing in video transcripts. \
Your task is to take a raw, unedited transcript and format it into clean, readable prose.

Guidelines:
- Add proper punctuation and capitalization
- Break the text into logical paragraphs
- Remove filler words and false starts (um, uh, you know, like, etc.)
- Fix run-on sentences for readability
- Preserve the speaker's voice, tone, and message exactly
- Do NOT add, remove, or alter the speaker's ideas or content
- Do NOT add any commentary, summaries, headers, or introductions
- Output only the formatted transcript text, nothing else
"""


class FormattingError(RuntimeError):
    pass


def format_transcript(raw_text: str, api_key: str) -> str:
    """Format a raw Whisper transcript into clean prose using Claude.

    Args:
        raw_text: Raw transcript string from Whisper.
        api_key: Anthropic API key.

    Returns:
        Formatted transcript as a string.
    """
    client = anthropic.Anthropic(api_key=api_key)

    log.info("Formatting transcript with Claude (%s)...", CLAUDE_MODEL)

    chunks: list[str] = []
    try:
        with client.messages.stream(
            model=CLAUDE_MODEL,
            max_tokens=8192,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": f"Please format the following video transcript:\n\n{raw_text}",
                }
            ],
        ) as stream:
            for text_chunk in stream.text_stream:
                chunks.append(text_chunk)
                if log.isEnabledFor(logging.DEBUG):
                    print(text_chunk, end="", flush=True)

    except anthropic.APIError as e:
        raise FormattingError(f"Claude API error: {e}") from e

    if log.isEnabledFor(logging.DEBUG):
        print()  # newline after streaming output

    formatted = "".join(chunks)
    log.info("Formatting complete. Characters: %d", len(formatted))
    return formatted
