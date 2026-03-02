from __future__ import annotations

import os
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

CLAUDE_MODEL = "claude-opus-4-6"
DEFAULT_WHISPER_MODEL = "medium"
TMP_DIR_NAME = ".vimeo_tmp"


@dataclass
class AppConfig:
    anthropic_api_key: str
    tmp_dir: Path
    output_path: Optional[Path]
    keep_tmp: bool
    keep_raw: bool
    vimeo_cookie_file: Optional[Path]
    verbose: bool
    whisper_model: str
    no_format: bool


def load_config(args) -> AppConfig:
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key and not args.no_format:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY environment variable is not set.\n"
            "Set it with: export ANTHROPIC_API_KEY=sk-ant-...\n"
            "Or skip formatting with: --no-format"
        )

    tmp_dir = Path.cwd() / TMP_DIR_NAME

    output_path: Optional[Path] = None
    if hasattr(args, "output") and args.output:
        output_path = Path(args.output).expanduser().resolve()

    cookie_file: Optional[Path] = None
    if hasattr(args, "cookies") and args.cookies:
        cookie_file = Path(args.cookies).expanduser().resolve()
        if not cookie_file.exists():
            raise FileNotFoundError(f"Cookie file not found: {cookie_file}")

    return AppConfig(
        anthropic_api_key=api_key,
        tmp_dir=tmp_dir,
        output_path=output_path,
        keep_tmp=args.keep_tmp,
        keep_raw=args.keep_raw,
        vimeo_cookie_file=cookie_file,
        verbose=args.verbose,
        whisper_model=args.whisper_model,
        no_format=args.no_format,
    )
