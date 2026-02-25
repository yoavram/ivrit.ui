# Repository Guidelines

## Project Structure & Module Organization
This repository is intentionally minimal:
1. `transcribe.py`: main CLI entry point for audio transcription with `ivrit`.
2. `pixi.toml`: workspace metadata and dependency declarations.
3. `pixi.lock`: locked, reproducible dependency resolution (treat as generated but committed).
4. `.pixi/`: local environment cache (ignored except `.pixi/config.toml`).

If you add features, keep modules small and place new Python files at repo root or under a new `ivrit_ui/` package directory. Put tests in `tests/`.

## Build, Test, and Development Commands
Use Pixi for all environment management:
1. `pixi install --locked`: install exactly what `pixi.lock` defines; fail if manifest and lock drift.
2. `pixi shell --locked`: open an activated dev shell with locked dependencies.
3. `pixi run python transcribe.py <audio_file>`: run the CLI (example: `pixi run python transcribe.py sample.mp3 --language he --stream`).
4. `pixi run python transcribe.py --help`: inspect available CLI options.

## Coding Style & Naming Conventions
1. Python style: PEP 8, 4-space indentation, UTF-8 source.
2. Naming: `snake_case` for functions/variables, `UPPER_SNAKE_CASE` for constants.
3. Keep CLI option names explicit (for example, `--language`, `--device`), and prefer clear error messages via `click.echo(..., err=True)`.
4. Keep imports grouped: standard library, third-party, local.

## Testing Guidelines
There is currently no test suite in this repository. For new logic:
1. Add `pytest` tests under `tests/` with names like `test_<feature>.py`.
2. Cover argument parsing, device selection behavior, and failure paths.
3. Run tests with `pixi run pytest` once `pytest` is added to dependencies.

## Commit & Pull Request Guidelines
This repo currently has no commit history, so follow this baseline:
1. Commit format: imperative, present tense (example: `Add stream output for segment timestamps`).
2. Keep commits scoped to one logical change.
3. PRs should include: purpose, behavior changes, test notes, and CLI examples for user-facing changes.
4. Link related issues and include terminal output snippets when debugging behavior changes.

## Transcribe + Summarize Pipeline Notes
1. Run transcription from repo root with `pixi run python transcribe.py <audio_file>`.
2. On Apple Silicon, default device behavior is CPU; long files can run silently for many minutes.
3. If redirecting stdout to a file, logs and transcript are mixed. Strip setup/teardown lines before summarizing.
4. Confirm completion using both file size and terminal marker (`✓ Transcription complete!`).
5. Expect ASR noise and occasional speaker confusion; summarize recurring themes, not one-off phrases.
6. Keep user-provided speaker roles explicit in the summary when available.
7. Preserve user-requested output filenames exactly unless asked to rename.
8. For meeting summaries, default to: decisions, options, open questions, and next steps.
