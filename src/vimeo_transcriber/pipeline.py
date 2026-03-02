from __future__ import annotations

import logging
import shutil
from pathlib import Path

from .config import AppConfig
from .downloader import download_audio
from .formatter import format_transcript
from .transcriber import transcribe
from .utils import slugify

log = logging.getLogger(__name__)


def run(url: str, cfg: AppConfig) -> None:
    """Orchestrate the full download → transcribe → format → save pipeline."""
    cfg.tmp_dir.mkdir(parents=True, exist_ok=True)

    try:
        # Step 1: Download audio
        audio_path, video_title = download_audio(
            url,
            output_dir=cfg.tmp_dir,
            cookie_file=cfg.vimeo_cookie_file,
        )

        # Step 2: Transcribe
        raw_text = transcribe(audio_path, model_name=cfg.whisper_model)

        # Step 3: Resolve output path now that we have the title
        if cfg.output_path:
            output_path = cfg.output_path
        else:
            slug = slugify(video_title)
            output_path = Path.cwd() / f"{slug}.txt"

        # Step 4: Optionally save raw transcript
        if cfg.keep_raw:
            raw_path = output_path.with_stem(output_path.stem + "_raw")
            raw_path.write_text(raw_text, encoding="utf-8")
            log.info("Raw transcript saved: %s", raw_path)

        # Step 5: Format or pass through
        if cfg.no_format:
            final_text = raw_text
            log.info("Skipping formatting (--no-format).")
        else:
            final_text = format_transcript(raw_text, api_key=cfg.anthropic_api_key)

        # Step 6: Write output
        output_path.write_text(final_text, encoding="utf-8")
        log.info("Output saved: %s", output_path)

    finally:
        if cfg.keep_tmp:
            log.info("Keeping temporary directory: %s", cfg.tmp_dir)
        else:
            if cfg.tmp_dir.exists():
                shutil.rmtree(cfg.tmp_dir)
                log.debug("Removed temporary directory: %s", cfg.tmp_dir)
