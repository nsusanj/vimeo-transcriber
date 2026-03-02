from __future__ import annotations

import argparse
import logging
import sys

from .config import DEFAULT_WHISPER_MODEL, load_config
from .pipeline import run
from .utils import setup_logging

WHISPER_MODEL_CHOICES = ["tiny", "base", "small", "medium", "large"]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="vimeo-transcriber",
        description="Download a Vimeo video, transcribe it with Whisper, and format the transcript with Claude.",
    )
    parser.add_argument("url", help="Vimeo video URL")
    parser.add_argument(
        "-o", "--output",
        metavar="FILE",
        help="Output file path (default: <video-title>.txt in current directory)",
    )
    parser.add_argument(
        "--cookies",
        metavar="FILE",
        help="Netscape-format cookie file for private Vimeo videos",
    )
    parser.add_argument(
        "--whisper-model",
        metavar="MODEL",
        choices=WHISPER_MODEL_CHOICES,
        default=DEFAULT_WHISPER_MODEL,
        help=f"Whisper model size (default: {DEFAULT_WHISPER_MODEL}; choices: {', '.join(WHISPER_MODEL_CHOICES)})",
    )
    parser.add_argument(
        "--keep-tmp",
        action="store_true",
        help="Keep the temporary directory after completion",
    )
    parser.add_argument(
        "--keep-raw",
        action="store_true",
        help="Save the raw Whisper transcript alongside the formatted output",
    )
    parser.add_argument(
        "--no-format",
        action="store_true",
        help="Skip Claude formatting and output the raw Whisper transcript",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose/debug logging",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    setup_logging(args.verbose)
    log = logging.getLogger(__name__)

    try:
        cfg = load_config(args)
    except (EnvironmentError, FileNotFoundError) as e:
        log.error(str(e))
        sys.exit(1)

    try:
        run(args.url, cfg)
    except KeyboardInterrupt:
        log.info("Interrupted by user.")
        sys.exit(130)
    except Exception as e:
        log.error("Fatal error: %s", e)
        if args.verbose:
            raise
        sys.exit(1)


if __name__ == "__main__":
    main()
