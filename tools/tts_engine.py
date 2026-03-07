#!/usr/bin/env python3
"""Text-to-speech engine using edge-tts with a calm, soothing male voice."""

import asyncio
import sys
import os

sys.path.insert(0, os.path.expanduser("~/Library/Python/3.9/lib/python/site-packages"))
import edge_tts

VOICE = "en-GB-RyanNeural"
RATE = "-15%"
PITCH = "-12Hz"
VOLUME = "+0%"


async def generate_speech(text: str, output_path: str, voice: str = VOICE,
                          rate: str = RATE, pitch: str = PITCH):
    """Generate speech audio from text using edge-tts."""
    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate,
        pitch=pitch,
        volume=VOLUME
    )
    await communicate.save(output_path)


def text_to_speech(text: str, output_path: str, **kwargs):
    """Synchronous wrapper for generate_speech."""
    asyncio.run(generate_speech(text, output_path, **kwargs))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 tts_engine.py <input_text_file> <output_mp3>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    with open(input_file, 'r') as f:
        text = f.read()

    print(f"Generating speech from {input_file}...")
    text_to_speech(text, output_file)
    print(f"Saved to {output_file}")
