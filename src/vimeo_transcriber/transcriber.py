from __future__ import annotations

import logging
from pathlib import Path

import mlx_whisper

from .config import WHISPER_MODEL_REPOS

log = logging.getLogger(__name__)


def transcribe(audio_path: Path, model_name: str) -> str:
    """Transcribe audio using mlx-whisper (Apple Silicon optimized).

    Args:
        audio_path: Path to the audio file.
        model_name: Whisper model size (e.g. "medium").

    Returns:
        Raw transcript as a single string.
    """
    repo = WHISPER_MODEL_REPOS[model_name]
    log.info("Transcribing with mlx-whisper model: %s", repo)
    result = mlx_whisper.transcribe(str(audio_path), path_or_hf_repo=repo)
    text: str = result["text"]
    log.info("Transcription complete. Characters: %d", len(text))
    return text
