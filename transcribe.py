#!/usr/bin/env python
"""
Simple CLI tool to transcribe audio files using ivrit.ai
"""
import platform
import click
import ivrit
import tqdm

@click.command()
@click.argument('audio_file', type=click.Path(exists=True))
@click.option(
    '--engine',
    default='faster-whisper',
    help='Transcription engine to use (default: faster-whisper)',
    show_default=True
)
@click.option(
    '--model',
    default='ivrit-ai/whisper-large-v3-turbo-ct2',
    help='Model to use for transcription',
    show_default=True
)
@click.option(
    '--device',
    default=None,
    help='Device to use for inference (auto, cpu, cuda, mps, etc.). If not specified, will use MPS on Apple Silicon if available, otherwise auto.',
    show_default=True
)
@click.option(
    '--language',
    default=None,
    help='Language code (e.g., he for Hebrew, en for English)'
)
@click.option(
    '--stream',
    is_flag=True,
    help='Stream results with timestamps'
)
@click.option(
    '--verbose',
    is_flag=True,
    help='Enable verbose output'
)
def transcribe(audio_file, engine, model, device, language, stream, verbose):
    """
    Transcribe an audio file using ivrit.ai
    
    Example:
        transcribe audio.mp3
        transcribe audio.mp3 --language he --stream
        transcribe audio.mp3 --model base --device cpu
    """
    try:
        # Auto-detect device if not specified
        # On Apple Silicon Macs, try MPS first
        if device is None:
            if platform.system() == 'Darwin' and platform.machine() == 'arm64':
                device = 'cpu'  # faster-whisper with CTranslate2 works best with CPU on Apple Silicon
                click.echo("✓ Apple Silicon detected - using CPU (optimized with CTranslate2)")
            else:
                device = 'auto'
        
        click.echo(f"Loading model: {model} on {device}...")
        
        # Load the model
        model_obj = ivrit.load_model(
            engine=engine,
            model=model,
            device=device
        )
        
        click.echo(f"Transcribing: {audio_file}")
        
        # Transcribe the audio
        kwargs = {}
        if language:
            kwargs['language'] = language
        if verbose:
            kwargs['verbose'] = verbose
        
        if stream:
            # Stream results with timestamps
            kwargs['stream'] = True
            for segment in model_obj.transcribe(path=audio_file, **kwargs):
                click.echo(f"[{segment.start:.2f}s - {segment.end:.2f}s]: {segment.text}")
        else:
            # Get full transcription
            result = model_obj.transcribe(path=audio_file, **kwargs)
            click.echo("\n--- Transcription ---")
            click.echo(result["text"])
        
        click.echo("\n✓ Transcription complete!")
        
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise click.Abort()


if __name__ == '__main__':
    transcribe()
