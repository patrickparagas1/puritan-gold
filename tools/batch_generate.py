#!/usr/bin/env python3
"""Batch generate TTS audio for all episodes that have scripts but no audio file.

Usage:
    python3 tools/batch_generate.py              # Generate all missing
    python3 tools/batch_generate.py --section family  # Only family section
    python3 tools/batch_generate.py --limit 10   # Only first 10
    python3 tools/batch_generate.py --ids 5001,5002,5003  # Specific IDs
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
    """Determine script file path for an episode."""
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


def get_mp3_duration(filepath):
    """Get duration of an MP3 file using ffprobe."""
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
             "-of", "csv=p=0", filepath],
            capture_output=True, text=True
        )
        seconds = float(result.stdout.strip())
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins}:{secs:02d}", seconds
    except Exception:
        return "0:00", 0


def generate_single(episode, episodes_list):
    """Generate audio for a single episode."""
    import edge_tts

    eid = episode['id']
    title = episode.get('title', f'Episode {eid}')
    script_path = get_script_path(episode)

    if not os.path.exists(script_path):
        print(f"  ⚠ No script for ID {eid}: {script_path}")
        return False

    audio_filename = f"ep{eid:03d}.mp3" if eid < 1000 else f"ep{eid}.mp3"
    final_path = os.path.join(AUDIO_DIR, audio_filename)

    # Skip if already exists
    if os.path.exists(final_path):
        print(f"  ✓ Already exists: {audio_filename}")
        return True

    with open(script_path, 'r') as f:
        script_text = f.read()

    # Step 1: TTS
    print(f"  [TTS] {title}...")
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        speech_path = tmp.name

    try:
        communicate = edge_tts.Communicate(
            text=script_text,
            voice="en-GB-RyanNeural",
            rate="-15%",
            pitch="-12Hz",
            volume="+0%"
        )
        asyncio.run(communicate.save(speech_path))
    except Exception as e:
        print(f"  ✗ TTS failed for {eid}: {e}")
        if os.path.exists(speech_path):
            os.unlink(speech_path)
        return False

    # Step 2: Mix with ambient
    if os.path.exists(AMBIENT_FILE):
        duration_str, duration_secs = get_mp3_duration(speech_path)
        result = subprocess.run([
            "ffmpeg", "-y",
            "-i", speech_path,
            "-stream_loop", "-1", "-i", AMBIENT_FILE,
            "-filter_complex",
            f"[1:a]atrim=0:{duration_secs},volume=0.02[amb];[0:a][amb]amix=inputs=2:duration=first:dropout_transition=3",
            "-codec:a", "libmp3lame", "-q:a", "4",
            final_path
        ], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"  ✗ FFmpeg failed for {eid}: {result.stderr[:200]}")
            os.unlink(speech_path)
            return False
    else:
        subprocess.run([
            "ffmpeg", "-y", "-i", speech_path,
            "-codec:a", "libmp3lame", "-q:a", "4",
            final_path
        ], capture_output=True)

    os.unlink(speech_path)

    # Step 3: Update episode in JSON
    duration_str, duration_secs = get_mp3_duration(final_path)
    file_size = os.path.getsize(final_path)

    episode['file'] = f"audio/{audio_filename}"
    episode['duration'] = duration_str
    episode['durationSecs'] = int(duration_secs)
    episode['fileSize'] = file_size

    print(f"  ✓ {audio_filename} ({duration_str}, {file_size / (1024*1024):.1f} MB)")
    return True


def main():
    parser = argparse.ArgumentParser(description="Batch generate TTS audio")
    parser.add_argument("--section", help="Only process this section")
    parser.add_argument("--limit", type=int, help="Max episodes to process")
    parser.add_argument("--ids", help="Comma-separated episode IDs")
    parser.add_argument("--dry-run", action="store_true", help="Just list what would be generated")
    args = parser.parse_args()

    os.makedirs(AUDIO_DIR, exist_ok=True)

    with open(EPISODES_FILE) as f:
        episodes = json.load(f)

    # Filter to episodes needing audio
    need_audio = [e for e in episodes if e.get('file') is None]

    if args.section:
        need_audio = [e for e in need_audio if e.get('section') == args.section]

    if args.ids:
        id_set = set(int(x) for x in args.ids.split(','))
        need_audio = [e for e in need_audio if e['id'] in id_set]

    if args.limit:
        need_audio = need_audio[:args.limit]

    print(f"Episodes to generate: {len(need_audio)}")

    if args.dry_run:
        for e in need_audio:
            script = get_script_path(e)
            exists = "✓" if os.path.exists(script) else "✗"
            print(f"  {exists} ID {e['id']:5d} [{e.get('section','?'):10s}] {e.get('title','')[:50]}")
        return

    start_time = time.time()
    success = 0
    failed = 0

    for i, ep in enumerate(need_audio, 1):
        print(f"\n[{i}/{len(need_audio)}] Episode {ep['id']}:")
        if generate_single(ep, episodes):
            success += 1
            # Save episodes.json after every episode (in case of crash)
            if success % 5 == 0:
                with open(EPISODES_FILE, 'w') as f:
                    json.dump(episodes, f, indent=2)
                print(f"  [Saved episodes.json — {success} done so far]")
        else:
            failed += 1

    # Final save
    with open(EPISODES_FILE, 'w') as f:
        json.dump(episodes, f, indent=2)

    elapsed = time.time() - start_time
    print(f"\n{'='*50}")
    print(f"Done! {success} generated, {failed} failed")
    print(f"Time: {elapsed/60:.1f} minutes")
    print(f"Episodes.json updated with audio paths + durations")


if __name__ == "__main__":
    main()
