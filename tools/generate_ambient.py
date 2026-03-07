#!/usr/bin/env python3
"""Generate a synthetic crackling fire ambient track."""

import struct
import wave
import random
import math
import os

SAMPLE_RATE = 44100
DURATION_SECONDS = 600  # 10 minutes (will be looped by ffmpeg)
OUTPUT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "ambient_crackling.wav")


def generate_brown_noise(n_samples):
    """Generate brown noise samples."""
    samples = []
    last = 0.0
    for _ in range(n_samples):
        white = random.uniform(-1, 1)
        last = (last + (0.02 * white)) / 1.02
        samples.append(last * 3.0)
    return samples


def add_crackles(samples, rate=15):
    """Add random crackle/pop sounds."""
    n = len(samples)
    for _ in range(int(DURATION_SECONDS * rate)):
        pos = random.randint(0, n - SAMPLE_RATE // 10)
        intensity = random.uniform(0.05, 0.25)
        crackle_len = random.randint(100, 2000)
        decay = 1.0
        for j in range(min(crackle_len, n - pos)):
            decay *= random.uniform(0.9, 0.999)
            samples[pos + j] += intensity * decay * random.uniform(-1, 1)
    return samples


def add_low_rumble(samples):
    """Add very low frequency rumble like a fire."""
    n = len(samples)
    for i in range(n):
        t = i / SAMPLE_RATE
        rumble = 0.02 * math.sin(2 * math.pi * 20 * t + math.sin(2 * math.pi * 0.1 * t) * 5)
        samples[i] += rumble
    return samples


def normalize(samples, target_peak=0.7):
    """Normalize samples to target peak level."""
    peak = max(abs(s) for s in samples)
    if peak > 0:
        factor = target_peak / peak
        return [s * factor for s in samples]
    return samples


def main():
    print("Generating crackling fire ambient track...")
    n_samples = SAMPLE_RATE * DURATION_SECONDS

    print("  Creating brown noise base...")
    samples = generate_brown_noise(n_samples)

    print("  Adding low rumble...")
    samples = add_low_rumble(samples)

    print("  Adding crackle effects...")
    samples = add_crackles(samples)

    print("  Normalizing...")
    samples = normalize(samples, 0.5)

    print(f"  Writing to {OUTPUT_PATH}...")
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    with wave.open(OUTPUT_PATH, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        for s in samples:
            s = max(-1.0, min(1.0, s))
            wf.writeframes(struct.pack('<h', int(s * 32767)))

    file_size = os.path.getsize(OUTPUT_PATH) / (1024 * 1024)
    print(f"  Done! {file_size:.1f} MB, {DURATION_SECONDS // 60} minutes")


if __name__ == "__main__":
    main()
