from __future__ import annotations

import logging
from pathlib import Path

import whisper

log = logging.getLogger(__name__)


def transcribe(audio_path: Path, model_name: str) -> str:
    """Transcribe audio using a local Whisper model.

    Args:
        audio_path: Path to the audio file.
        model_name: Whisper model size (e.g. "medium").

    Returns:
        Raw transcript as a single string.
    """
    log.info("Loading Whisper model: %s", model_name)
    model = whisper.load_model(model_name)

    log.info("Transcribing audio (this may take a while)...")
    result = model.transcribe(str(audio_path))

    text: str = result["text"]
    log.info("Transcription complete. Characters: %d", len(text))
    return text
