#!/usr/bin/env python3
"""Generate a warm, realistic crackling fireplace ambient track.

Improved version: warmer base tone, more realistic crackle/pop patterns,
gentle low-frequency warmth, reduced harshness. Sounds like a real fireplace
rather than static noise.
"""

import struct
import wave
import random
import math
import os

SAMPLE_RATE = 44100
DURATION_SECONDS = 600  # 10 minutes (looped in the app)
OUTPUT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "ambient_crackling.wav")


def generate_warm_base(n_samples):
    """Generate warm brown noise base — filtered to remove harsh highs."""
    samples = []
    last = 0.0
    prev = 0.0
    for _ in range(n_samples):
        white = random.uniform(-1, 1)
        # Slower random walk = warmer/deeper sound
        last = (last + (0.012 * white)) / 1.012
        # Two-pole low-pass filter to remove harshness
        filtered = 0.7 * last + 0.3 * prev
        prev = filtered
        samples.append(filtered * 2.5)
    return samples


def add_gentle_warmth(samples):
    """Add very gentle low-frequency warmth — like the deep hum of a fire."""
    n = len(samples)
    for i in range(n):
        t = i / SAMPLE_RATE
        # Multiple slow sine waves for organic warmth
        warmth = (
            0.015 * math.sin(2 * math.pi * 12 * t + math.sin(2 * math.pi * 0.07 * t) * 4) +
            0.010 * math.sin(2 * math.pi * 8 * t + math.sin(2 * math.pi * 0.05 * t) * 3) +
            0.008 * math.sin(2 * math.pi * 25 * t + math.sin(2 * math.pi * 0.12 * t) * 2)
        )
        samples[i] += warmth
    return samples


def add_crackles(samples, rate=8):
    """Add realistic crackle/pop sounds with natural envelopes.

    Three types:
    - Tiny pops (fast, sharp, quiet)
    - Medium crackles (sizzle for 50-200ms)
    - Big pops (occasional loud snap with resonant decay)
    """
    n = len(samples)

    # Tiny pops — frequent, subtle
    for _ in range(int(DURATION_SECONDS * rate)):
        pos = random.randint(0, n - 1000)
        intensity = random.uniform(0.03, 0.12)
        pop_len = random.randint(50, 400)
        decay = 1.0
        for j in range(min(pop_len, n - pos)):
            decay *= random.uniform(0.92, 0.998)
            samples[pos + j] += intensity * decay * random.uniform(-1, 1)

    # Medium crackles — sizzle with slower decay
    for _ in range(int(DURATION_SECONDS * rate * 0.4)):
        pos = random.randint(0, n - SAMPLE_RATE // 5)
        intensity = random.uniform(0.06, 0.18)
        crackle_len = random.randint(2000, 8000)
        decay = 1.0
        freq = random.uniform(800, 3000)  # Higher freq = sizzle
        for j in range(min(crackle_len, n - pos)):
            decay *= random.uniform(0.9985, 0.9998)
            t = j / SAMPLE_RATE
            sizzle = math.sin(2 * math.pi * freq * t) * random.uniform(0.3, 1.0)
            samples[pos + j] += intensity * decay * sizzle * 0.3

    # Big pops — rare, satisfying snaps
    for _ in range(int(DURATION_SECONDS * 0.5)):
        pos = random.randint(0, n - SAMPLE_RATE)
        intensity = random.uniform(0.15, 0.35)
        # Sharp attack
        attack_len = random.randint(10, 50)
        for j in range(min(attack_len, n - pos)):
            samples[pos + j] += intensity * random.uniform(-1, 1) * (1 - j/attack_len)
        # Resonant decay
        decay_len = random.randint(1000, 5000)
        decay = 1.0
        for j in range(min(decay_len, n - pos - attack_len)):
            decay *= random.uniform(0.997, 0.9995)
            samples[pos + attack_len + j] += intensity * 0.3 * decay * random.uniform(-1, 1)

    return samples


def add_breathing(samples):
    """Add subtle volume 'breathing' — fire intensity slowly rises and falls."""
    n = len(samples)
    for i in range(n):
        t = i / SAMPLE_RATE
        # Slow breathing: volume gently cycles every 15-30 seconds
        breath = 1.0 + 0.12 * math.sin(2 * math.pi * 0.04 * t) + 0.08 * math.sin(2 * math.pi * 0.07 * t + 1.2)
        samples[i] *= breath
    return samples


def lowpass_filter(samples, cutoff_freq=2500):
    """Simple RC low-pass filter to remove harsh high frequencies."""
    rc = 1.0 / (2 * math.pi * cutoff_freq)
    dt = 1.0 / SAMPLE_RATE
    alpha = dt / (rc + dt)

    filtered = [samples[0]]
    for i in range(1, len(samples)):
        filtered.append(filtered[-1] + alpha * (samples[i] - filtered[-1]))
    return filtered


def normalize(samples, target_peak=0.6):
    """Normalize samples to target peak level."""
    peak = max(abs(s) for s in samples)
    if peak > 0:
        factor = target_peak / peak
        return [s * factor for s in samples]
    return samples


def main():
    print("Generating warm crackling fireplace ambient track...")
    n_samples = SAMPLE_RATE * DURATION_SECONDS

    print("  Creating warm brown noise base...")
    samples = generate_warm_base(n_samples)

    print("  Adding gentle low-frequency warmth...")
    samples = add_gentle_warmth(samples)

    print("  Adding crackle and pop effects...")
    samples = add_crackles(samples)

    print("  Adding fire breathing (volume modulation)...")
    samples = add_breathing(samples)

    print("  Applying low-pass filter (removing harshness)...")
    samples = lowpass_filter(samples, cutoff_freq=2200)

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
    print("  Warmer base, realistic crackles, gentle breathing, no harshness.")


if __name__ == "__main__":
    main()
