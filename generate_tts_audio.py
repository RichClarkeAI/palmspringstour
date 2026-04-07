#!/usr/bin/env python3
"""
Generate extended audio narrations for Palm Springs Architecture Tour
Splits long texts into manageable chunks, generates audio, and concatenates
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def split_text_into_chunks(text, max_words=150):
    """Split text into chunks of approximately max_words"""
    paragraphs = text.strip().split('\n\n')
    chunks = []
    current_chunk = []
    current_word_count = 0

    for para in paragraphs:
        para_words = len(para.split())

        if current_word_count + para_words > max_words and current_chunk:
            # Save current chunk and start new one
            chunks.append(' '.join(current_chunk))
            current_chunk = [para]
            current_word_count = para_words
        else:
            current_chunk.append(para)
            current_word_count += para_words

    # Don't forget the last chunk
    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks

def generate_audio_with_openclaw_tts(text):
    """
    Generate audio using OpenClaw's TTS tool
    Returns path to generated audio file
    """
    # The TTS tool is available as a function call, not command line
    # We'll need to handle this differently
    pass

def concatenate_audio_files(audio_files, output_path):
    """Concatenate multiple audio files into one"""
    # Create file list for ffmpeg
    list_file = '/tmp/audio_list.txt'
    with open(list_file, 'w') as f:
        for audio_file in audio_files:
            f.write(f"file '{audio_file}'\n")

    # Use ffmpeg to concatenate
    cmd = [
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
        '-i', list_file, '-c', 'copy', output_path
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def main():
    narrations_dir = Path('narrations')
    audio_dir = Path('audio')

    print("=== Palm Springs Extended Audio Narration Generator ===\n")
    print("This script helps generate longer narrations (3-4 minutes)")
    print("by splitting text into chunks and concatenating audio.\n")

    # Process each narration
    for narration_file in sorted(narrations_dir.glob('*.txt')):
        # Skip partial files
        if '-part' in narration_file.name:
            continue

        home_id = narration_file.stem
        print(f"Processing {home_id}...")

        with open(narration_file, 'r') as f:
            text = f.read()

        chunks = split_text_into_chunks(text)
        print(f"  Split into {len(chunks)} chunks")

        for i, chunk in enumerate(chunks):
            word_count = len(chunk.split())
            print(f"  Chunk {i+1}: {word_count} words")

            # Save chunk for reference
            chunk_file = narrations_dir / f"{home_id}-chunk{i+1}.txt"
            with open(chunk_file, 'w') as f:
                f.write(chunk)

        print()

if __name__ == '__main__':
    main()
