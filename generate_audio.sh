#!/bin/bash

# Script to generate extended audio narrations for Palm Springs tour
# Splits long texts into sections, generates audio for each, then concatenates

NARRATIONS_DIR="narrations"
AUDIO_DIR="audio"
TEMP_DIR="/tmp/tts-narrations-$$"

mkdir -p "$TEMP_DIR"
mkdir -p "$AUDIO_DIR"

process_narration() {
    local HOME_ID=$1
    local INPUT_FILE="${NARRATIONS_DIR}/${HOME_ID}.txt"
    local OUTPUT_FILE="${AUDIO_DIR}/${HOME_ID}.mp3"
    local TEMP_LIST="${TEMP_DIR}/${HOME_ID}-files.txt"

    echo "Processing ${HOME_ID}..."

    if [ ! -f "$INPUT_FILE" ]; then
        echo "  ✗ Input file not found: $INPUT_FILE"
        return 1
    fi

    # Split into paragraphs (treating double newlines as paragraph breaks)
    # Generate audio for each paragraph
    rm -f "$TEMP_LIST"
    touch "$TEMP_LIST"

    local PARAGRAPH_NUM=0
    local CURRENT_PARA=""

    while IFS= read -r line || [ -n "$line" ]; do
        if [ -z "$line" ]; then
            # Empty line - end of paragraph
            if [ -n "$CURRENT_PARA" ]; then
                PARAGRAPH_NUM=$((PARAGRAPH_NUM + 1))
                echo "  Generating audio for paragraph $PARAGRAPH_NUM..."

                # Save paragraph to temp file
                PARA_FILE="${TEMP_DIR}/${HOME_ID}-para-${PARAGRAPH_NUM}.txt"
                echo "$CURRENT_PARA" > "$PARA_FILE"

                # Generate audio using OpenClaw TTS
                AUDIO_FILE="${TEMP_DIR}/${HOME_ID}-audio-${PARAGRAPH_NUM}.mp3"

                # Use the tts function directly - this requires the calling environment
                # to have access to the tts tool
                if command -v tts-cli &> /dev/null; then
                    tts-cli --text "$CURRENT_PARA" --output "$AUDIO_FILE"
                else
                    # Fallback - will need manual processing
                    echo "    ⚠️ Manual TTS needed for paragraph $PARAGRAPH_NUM"
                    echo "    Text length: $(echo "$CURRENT_PARA" | wc -w) words"
                fi

                if [ -f "$AUDIO_FILE" ]; then
                    echo "file '${AUDIO_FILE}'" >> "$TEMP_LIST"
                fi

                CURRENT_PARA=""
            fi
        else
            # Add line to current paragraph
            if [ -z "$CURRENT_PARA" ]; then
                CURRENT_PARA="$line"
            else
                CURRENT_PARA="$CURRENT_PARA $line"
            fi
        fi
    done < "$INPUT_FILE"

    # Handle last paragraph if file doesn't end with blank line
    if [ -n "$CURRENT_PARA" ]; then
        PARAGRAPH_NUM=$((PARAGRAPH_NUM + 1))
        echo "  Generating audio for final paragraph $PARAGRAPH_NUM..."
        PARA_FILE="${TEMP_DIR}/${HOME_ID}-para-${PARAGRAPH_NUM}.txt"
        echo "$CURRENT_PARA" > "$PARA_FILE"
    fi

    echo "  Generated $PARAGRAPH_NUM paragraphs"
    echo "  ✗ Automatic concatenation not available - see manual steps below"
    echo ""
}

# Main processing
echo "=== Palm Springs Audio Narration Generator ==="
echo ""
echo "This script helps generate extended audio narrations"
echo "Due to TTS limitations, manual processing may be required"
echo ""

for narration_file in narrations/*.txt; do
    if [ -f "$narration_file" ]; then
        HOME_ID=$(basename "$narration_file" .txt)
        process_narration "$HOME_ID"
    fi
done

echo "=== Manual Steps Required ==="
echo ""
echo "For each home, you'll need to:"
echo "1. Split the narration into sections (500-700 words each)"
echo "2. Generate audio for each section using the TTS tool"
echo "3. Concatenate the audio files using ffmpeg:"
echo "   ffmpeg -f concat -i files.txt -c copy output.mp3"
echo ""
echo "See generate_audio_sections.sh for automated approach"
