#!/usr/bin/env python3
"""Create a single podcast episode: script → TTS → mix with ambient → final MP3."""

import argparse
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime

sys.path.insert(0, os.path.expanduser("~/Library/Python/3.9/lib/python/site-packages"))

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(PROJECT_ROOT, "audio")
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")
AMBIENT_FILE = os.path.join(ASSETS_DIR, "ambient_crackling.wav")
EPISODES_FILE = os.path.join(PROJECT_ROOT, "episodes.json")


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


def create_episode(script_path, title, subtitle="", description="",
                   series="", tags=None, episode_num=None):
    """Create a complete podcast episode from a script file."""
    from tts_engine import text_to_speech

    os.makedirs(AUDIO_DIR, exist_ok=True)

    # Determine episode number
    if episode_num is None:
        existing = [f for f in os.listdir(AUDIO_DIR) if f.startswith("ep") and f.endswith(".mp3")]
        episode_num = len(existing) + 1

    episode_id = f"ep{episode_num:03d}"
    final_path = os.path.join(AUDIO_DIR, f"{episode_id}.mp3")

    # Read script
    with open(script_path, 'r') as f:
        script_text = f.read()

    print(f"[1/3] Generating speech for '{title}'...")
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        speech_path = tmp.name

    text_to_speech(script_text, speech_path)

    # Mix with ambient if available
    if os.path.exists(AMBIENT_FILE):
        print(f"[2/3] Mixing with ambient crackling...")
        # Get speech duration to loop ambient
        duration_str, duration_secs = get_mp3_duration(speech_path)

        # Use ffmpeg to mix speech with looped ambient at low volume
        subprocess.run([
            "ffmpeg", "-y",
            "-i", speech_path,
            "-stream_loop", "-1", "-i", AMBIENT_FILE,
            "-filter_complex",
            f"[1:a]atrim=0:{duration_secs},volume=0.06[amb];[0:a][amb]amix=inputs=2:duration=first:dropout_transition=3",
            "-codec:a", "libmp3lame", "-q:a", "4",
            final_path
        ], capture_output=True)
    else:
        print(f"[2/3] No ambient file found, using speech only...")
        subprocess.run([
            "ffmpeg", "-y", "-i", speech_path,
            "-codec:a", "libmp3lame", "-q:a", "4",
            final_path
        ], capture_output=True)

    # Clean up temp file
    os.unlink(speech_path)

    # Get final duration
    duration_str, duration_secs = get_mp3_duration(final_path)
    file_size = os.path.getsize(final_path)

    print(f"[3/3] Updating episode registry...")
    update_episodes_json(
        episode_num=episode_num,
        title=title,
        subtitle=subtitle,
        description=description or title,
        filename=f"audio/{episode_id}.mp3",
        duration=duration_str,
        duration_secs=duration_secs,
        file_size=file_size,
        series=series,
        tags=tags or []
    )

    print(f"Done! {final_path} ({duration_str}, {file_size / (1024*1024):.1f} MB)")
    return final_path


def update_episodes_json(episode_num, title, subtitle, description,
                         filename, duration, duration_secs, file_size,
                         series, tags):
    """Add or update an episode in episodes.json."""
    episodes = []
    if os.path.exists(EPISODES_FILE):
        with open(EPISODES_FILE, 'r') as f:
            episodes = json.load(f)

    # Remove existing entry with same episode_num
    episodes = [e for e in episodes if e.get("id") != episode_num]

    episodes.append({
        "id": episode_num,
        "title": title,
        "subtitle": subtitle,
        "description": description,
        "file": filename,
        "duration": duration,
        "durationSecs": int(duration_secs),
        "fileSize": file_size,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "series": series,
        "tags": tags
    })

    episodes.sort(key=lambda e: e["id"])

    with open(EPISODES_FILE, 'w') as f:
        json.dump(episodes, f, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a podcast episode")
    parser.add_argument("--script", required=True, help="Path to script text file")
    parser.add_argument("--title", required=True, help="Episode title")
    parser.add_argument("--subtitle", default="", help="Episode subtitle")
    parser.add_argument("--description", default="", help="Episode description")
    parser.add_argument("--series", default="", help="Series name")
    parser.add_argument("--tags", default="", help="Comma-separated tags")
    parser.add_argument("--num", type=int, default=None, help="Episode number")

    args = parser.parse_args()
    tags = [t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else []

    create_episode(
        script_path=args.script,
        title=args.title,
        subtitle=args.subtitle,
        description=args.description,
        series=args.series,
        tags=tags,
        episode_num=args.num
    )
