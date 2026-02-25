# ivrit-ui

A minimal command-line tool for transcribing audio files with [`ivrit`](https://pypi.org/project/ivrit/).
It supports English transcription, but is primarily aimed at Hebrew workflows, where [ivrit.ai](https://ivrit.ai) excels.

## Requirements

1. `pixi` (project environment manager)
2. macOS arm64 is the current pinned platform in `pixi.toml`

## Setup

Install the environment from lockfile:

```bash
pixi install --locked
```

Run commands in the Pixi environment:

```bash
pixi run python transcribe.py --help
```

## Usage

Basic transcription:

```bash
pixi run python transcribe.py audio.mp3
```

Stream segments with timestamps:

```bash
pixi run python transcribe.py audio.mp3 --stream
```

Set language explicitly (for example Hebrew):

```bash
pixi run python transcribe.py audio.mp3 --language he
```

Override device/model:

```bash
pixi run python transcribe.py audio.mp3 --device cpu --model ivrit-ai/whisper-large-v3-turbo-ct2
```

## CLI Options

- `--engine`: transcription engine (default: `faster-whisper`)
- `--model`: model identifier to load
- `--device`: inference device (`cpu`, `cuda`, `mps`, `auto`, etc.)
- `--language`: language code such as `he` or `en`
- `--stream`: emit timestamped segments
- `--verbose`: verbose model/transcription output

## Notes

1. On Apple Silicon, `transcribe.py` defaults to `cpu` when `--device` is omitted.
2. Errors are surfaced through CLI output and terminate with a non-zero exit.
