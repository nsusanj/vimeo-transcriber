# vimeo-transcriber

Download a Vimeo video, transcribe the audio with [Whisper](https://github.com/openai/whisper), and format the transcript into clean prose with Claude.

## Requirements

- Python >= 3.11
- [ffmpeg](https://ffmpeg.org/) (`brew install ffmpeg`)
- An [Anthropic API key](https://console.anthropic.com/)

## Install

```bash
uv venv
source .venv/bin/activate
uv pip install -e .
```

## Usage

```bash
export ANTHROPIC_API_KEY=sk-ant-...

vimeo-transcriber <vimeo-url>
```

The formatted transcript is written to `<video-title>.txt` in the current directory.

### Options

| Flag | Description |
|------|-------------|
| `-o FILE` | Output file path (default: `<video-title>.txt`) |
| `--cookies FILE` | Netscape-format cookie file for private Vimeo videos |
| `--whisper-model MODEL` | Whisper model size: `tiny`, `base`, `small`, `medium` (default), `large` |
| `--keep-tmp` | Keep the temporary working directory after completion |
| `--keep-raw` | Save the raw Whisper transcript alongside the formatted output |
| `--no-format` | Skip Claude formatting and output the raw Whisper transcript |
| `-v, --verbose` | Enable verbose/debug logging |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | Required unless `--no-format` is used |
