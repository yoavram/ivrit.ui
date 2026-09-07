---
name: ivrit-ui
description: Transcribe Hebrew (or English) audio recordings — meetings, lab discussions, interviews — into text using ivrit.ai's Whisper models via faster-whisper, and optionally summarize the result. Use when asked to transcribe an audio file, especially a Hebrew-language recording, or to summarize a recorded meeting from audio.
---

# ivrit-ui: Hebrew Audio Transcription

This skill runs `transcribe.py`, a local CLI that transcribes audio files using
[`ivrit`](https://pypi.org/project/ivrit/) (faster-whisper under the hood, with
`ivrit-ai/whisper-large-v3-turbo-ct2` as the default model — tuned for Hebrew,
but works for English too).

## Setup (once per machine)

```bash
cd <path to this repo checkout>
pixi install --locked
```

## Running a transcription

```bash
pixi run python transcribe.py <audio_file>
```

Useful options:

- `--language he` — force Hebrew (recommended; auto-detect can be wrong on noisy audio)
- `--stream` — emit timestamped segments as they're produced, instead of one final blob
- `--device cpu|cuda|mps|auto` — inference device (Apple Silicon defaults to `cpu`, which is the fastest option there with CTranslate2)
- `--model <id>` — override the model (default: `ivrit-ai/whisper-large-v3-turbo-ct2`)
- `--engine` — transcription engine (default: `faster-whisper`)
- `--verbose` — verbose model/transcription output

Example:

```bash
pixi run python transcribe.py meeting.m4a --language he --stream
```

## Operational notes

1. Long recordings can run silently for many minutes, especially on CPU. Don't assume it's stuck.
2. If redirecting stdout to a file, setup/log lines are mixed in with the transcript — strip them before treating the file as a clean transcript.
3. Confirm completion via the `✓ Transcription complete!` marker (non-streaming mode) or the process exiting cleanly (streaming mode).
4. Expect ASR noise and occasional speaker confusion, especially with overlapping speech or technical jargon.

## Summarizing a transcribed meeting

When asked to summarize, not just transcribe:

1. Summarize recurring themes and decisions, not one-off ASR glitches or mistranscribed phrases.
2. Keep user-provided speaker roles/names explicit in the summary when the user supplies them (the transcript itself won't have speaker labels).
3. Default summary structure: decisions, options considered, open questions, next steps.
4. Preserve user-requested output filenames exactly, unless asked to rename.

## Privacy

Transcripts of real recordings often contain unpublished research, personal
conversation, or third parties who didn't consent to publication. Treat any
transcript output as sensitive by default:

1. Never commit a real transcript or audio file into this (public) repo — `.gitignore` already excludes `*.txt`, `*.mp3`, `*.wav`, `*.m4a`, `*.qta` for this reason. Don't override that for a specific file without asking.
2. Don't paste transcript content into a public artifact, issue, or any other shared/public destination without the user's explicit go-ahead.
