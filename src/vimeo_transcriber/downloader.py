from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

import yt_dlp

log = logging.getLogger(__name__)


class DownloadError(RuntimeError):
    pass


def download_audio(
    url: str,
    output_dir: Path,
    cookie_file: Optional[Path] = None,
) -> tuple[Path, str]:
    """Download audio from a Vimeo URL to output_dir in its native format (typically m4a for Vimeo).

    Returns:
        (audio_path, video_title)
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    ydl_opts: dict = {
        "format": "bestaudio/best",
        "outtmpl": str(output_dir / "audio.%(ext)s"),
        "quiet": not log.isEnabledFor(logging.DEBUG),
        "no_warnings": not log.isEnabledFor(logging.DEBUG),
    }

    if cookie_file:
        ydl_opts["cookiefile"] = str(cookie_file)

    log.info("Downloading audio from: %s", url)
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title: str = info.get("title", "video") if info else "video"
    except yt_dlp.utils.DownloadError as e:
        raise DownloadError(f"Failed to download audio: {e}") from e

    ext = info.get("ext", "m4a") if info else "m4a"
    audio_path = output_dir / f"audio.{ext}"

    if not audio_path.exists():
        raise DownloadError(f"Expected audio file not found at: {audio_path}")

    log.info("Audio downloaded: %s (title: %r)", audio_path, title)
    return audio_path, title
