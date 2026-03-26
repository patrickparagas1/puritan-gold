#!/bin/bash
# Reduce ambient crackling noise on all audio files
# Uses highpass filter + FFT denoising to clean up the ambient layer
set -e

AUDIO_DIR="$(cd "$(dirname "$0")/../audio" && pwd)"
TEMP_DIR="/tmp/noise_reduce_$$"
mkdir -p "$TEMP_DIR"

total=$(ls "$AUDIO_DIR"/*.mp3 2>/dev/null | wc -l | tr -d ' ')
count=0
failed=0

echo "Processing $total audio files..."

for f in "$AUDIO_DIR"/*.mp3; do
    count=$((count + 1))
    base=$(basename "$f")
    temp="$TEMP_DIR/$base"

    # Process with noise reduction
    if ffmpeg -y -i "$f" -af "highpass=f=80,afftdn=nf=-25" -codec:a libmp3lame -q:a 4 "$temp" 2>/dev/null; then
        mv "$temp" "$f"
        if [ $((count % 50)) -eq 0 ]; then
            echo "  [$count/$total] Done..."
        fi
    else
        failed=$((failed + 1))
        echo "  FAILED: $base"
        rm -f "$temp"
    fi
done

rm -rf "$TEMP_DIR"
echo "Complete! $count processed, $failed failed"
