#!/usr/bin/env python3
"""Parallel-safe batch TTS generator. Does NOT write episodes.json (avoids race conditions).
Generates audio files only. Run sync_audio.py after all batches complete.

Usage:
    python3 tools/batch_generate_safe.py --ids 1001,1002,1003
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
import asyncio
import time

sys.path.insert(0, os.path.expanduser("~/Library/Python/3.9/lib/python/site-packages"))

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(PROJECT_ROOT, "audio")
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "scripts")
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")
AMBIENT_FILE = os.path.join(ASSETS_DIR, "ambient_crackling.wav")
EPISODES_FILE = os.path.join(PROJECT_ROOT, "episodes.json")


def get_script_path(episode):
    eid = episode['id']
    section = episode.get('section', '')
    if section == 'study':
        return os.path.join(SCRIPTS_DIR, f'ep_{eid}.txt')
    elif section == 'family':
        return os.path.join(SCRIPTS_DIR, f'family_{eid}.txt')
    elif section == 'school':
        return os.path.join(SCRIPTS_DIR, f'school_{eid}.txt')
    elif section == 'together':
        return os.path.join(SCRIPTS_DIR, f'together_{eid}.txt')
    elif section == 'personal':
        if episode.get('topic'):
            return os.path.join(SCRIPTS_DIR, f'ep_{eid}.txt')
        else:
            return os.path.join(SCRIPTS_DIR, f'personal_{eid}.txt')
    return os.path.join(SCRIPTS_DIR, f'ep_{eid}.txt')


def generate_single(episode):
    import edge_tts
    eid = episode['id']
    title = episode.get('title', f'Episode {eid}')
    script_path = get_script_path(episode)

    if not os.path.exists(script_path):
        print(f"  SKIP No script for ID {eid}", flush=True)
        return False

    audio_filename = f"ep{eid:03d}.mp3" if eid < 1000 else f"ep{eid}.mp3"
    final_path = os.path.join(AUDIO_DIR, audio_filename)

    if os.path.exists(final_path) and os.path.getsize(final_path) > 10000:
        print(f"  SKIP Already exists: {audio_filename}", flush=True)
        return True

    with open(script_path, 'r') as f:
        script_text = f.read()

    if len(script_text.strip()) < 10:
        print(f"  SKIP Empty script for {eid}", flush=True)
        return False

    print(f"  [TTS] {title}...", flush=True)
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        speech_path = tmp.name

    max_retries = 3
    for attempt in range(max_retries):
        try:
            communicate = edge_tts.Communicate(
                text=script_text,
                voice="en-GB-RyanNeural",
                rate="-15%",
                pitch="-12Hz",
                volume="+0%"
            )
            # Use asyncio.wait_for with 600s timeout to prevent hangs
            async def tts_with_timeout():
                await asyncio.wait_for(communicate.save(speech_path), timeout=600)
            asyncio.run(tts_with_timeout())
            break  # Success
        except asyncio.TimeoutError:
            print(f"  RETRY TTS timeout for {eid} (attempt {attempt+1}/{max_retries})", flush=True)
            if os.path.exists(speech_path):
                os.unlink(speech_path)
            if attempt == max_retries - 1:
                return False
            time.sleep(5)
        except Exception as e:
            print(f"  RETRY TTS error for {eid}: {e} (attempt {attempt+1}/{max_retries})", flush=True)
            if os.path.exists(speech_path):
                os.unlink(speech_path)
            if attempt == max_retries - 1:
                return False
            time.sleep(5)

    # Mix with ambient
    if os.path.exists(AMBIENT_FILE):
        try:
            result = subprocess.run(
                ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
                 "-of", "csv=p=0", speech_path],
                capture_output=True, text=True
            )
            duration_secs = float(result.stdout.strip())
        except:
            duration_secs = 300

        result = subprocess.run([
            "ffmpeg", "-y",
            "-i", speech_path,
            "-stream_loop", "-1", "-i", AMBIENT_FILE,
            "-filter_complex",
            f"[1:a]atrim=0:{duration_secs},volume=0.06[amb];[0:a][amb]amix=inputs=2:duration=first:dropout_transition=3",
            "-codec:a", "libmp3lame", "-q:a", "4",
            final_path
        ], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  FAIL FFmpeg for {eid}: {result.stderr[:200]}", flush=True)
            os.unlink(speech_path)
            return False
    else:
        subprocess.run([
            "ffmpeg", "-y", "-i", speech_path,
            "-codec:a", "libmp3lame", "-q:a", "4",
            final_path
        ], capture_output=True)

    os.unlink(speech_path)
    size = os.path.getsize(final_path)
    print(f"  OK {audio_filename} ({size / (1024*1024):.1f} MB)", flush=True)
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ids", required=True, help="Comma-separated episode IDs")
    args = parser.parse_args()

    os.makedirs(AUDIO_DIR, exist_ok=True)
    id_set = set(int(x) for x in args.ids.split(',') if x.strip())

    with open(EPISODES_FILE) as f:
        episodes = json.load(f)

    targets = [e for e in episodes if e['id'] in id_set]
    print(f"Generating {len(targets)} episodes (NO episodes.json writes)", flush=True)

    start_time = time.time()
    success = 0
    failed = 0

    for i, ep in enumerate(targets, 1):
        print(f"\n[{i}/{len(targets)}] Episode {ep['id']}:", flush=True)
        if generate_single(ep):
            success += 1
        else:
            failed += 1

    elapsed = time.time() - start_time
    print(f"\nDone! {success} generated, {failed} failed, {elapsed/60:.1f} min", flush=True)


if __name__ == "__main__":
    main()
