#!/usr/bin/env python3
"""Generate TTS audio for a single episode using subprocess-based timeout.
Usage: python3 tools/gen_single.py <episode_id>
"""
import json, os, sys, subprocess, tempfile, time

sys.path.insert(0, os.path.expanduser("~/Library/Python/3.9/lib/python/site-packages"))

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(PROJECT_ROOT, "audio")
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "scripts")
AMBIENT_FILE = os.path.join(PROJECT_ROOT, "assets", "ambient_crackling.wav")
EPISODES_FILE = os.path.join(PROJECT_ROOT, "episodes.json")

def main():
    eid = int(sys.argv[1])

    with open(EPISODES_FILE) as f:
        episodes = json.load(f)

    ep = next((e for e in episodes if e['id'] == eid), None)
    if not ep:
        print(f"SKIP no episode {eid}")
        sys.exit(1)

    audio_filename = f"ep{eid:03d}.mp3" if eid < 1000 else f"ep{eid}.mp3"
    final_path = os.path.join(AUDIO_DIR, audio_filename)

    if os.path.exists(final_path) and os.path.getsize(final_path) > 10000:
        print(f"SKIP exists {audio_filename}")
        sys.exit(0)

    # Determine script path
    section = ep.get('section', '')
    if section == 'personal' and ep.get('topic'):
        script_path = os.path.join(SCRIPTS_DIR, f'ep_{eid}.txt')
    elif section == 'family':
        script_path = os.path.join(SCRIPTS_DIR, f'family_{eid}.txt')
    elif section == 'school':
        script_path = os.path.join(SCRIPTS_DIR, f'school_{eid}.txt')
    elif section == 'together':
        script_path = os.path.join(SCRIPTS_DIR, f'together_{eid}.txt')
    else:
        script_path = os.path.join(SCRIPTS_DIR, f'ep_{eid}.txt')

    if not os.path.exists(script_path):
        print(f"SKIP no script {script_path}")
        sys.exit(1)

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        speech_path = tmp.name

    # Use edge-tts CLI with subprocess timeout (600s = 10 min)
    try:
        result = subprocess.run([
            sys.executable, "-m", "edge_tts",
            "-v", "en-GB-RyanNeural",
            "--rate=-15%",
            "--pitch=-12Hz",
            "--volume=+0%",
            "-f", script_path,
            "--write-media", speech_path
        ], capture_output=True, text=True, timeout=1200)

        if result.returncode != 0:
            print(f"FAIL TTS error: {result.stderr[:200]}")
            os.unlink(speech_path) if os.path.exists(speech_path) else None
            sys.exit(1)
    except subprocess.TimeoutExpired:
        print(f"FAIL TTS timeout 1200s")
        os.unlink(speech_path) if os.path.exists(speech_path) else None
        sys.exit(1)

    if not os.path.exists(speech_path) or os.path.getsize(speech_path) < 1000:
        print(f"FAIL TTS output empty")
        sys.exit(1)

    # Mix with ambient
    if os.path.exists(AMBIENT_FILE):
        dur_result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", speech_path],
            capture_output=True, text=True
        )
        try:
            dur = float(dur_result.stdout.strip())
        except:
            dur = 300

        mix = subprocess.run([
            "ffmpeg", "-y",
            "-i", speech_path,
            "-stream_loop", "-1", "-i", AMBIENT_FILE,
            "-filter_complex",
            f"[1:a]atrim=0:{dur},volume=0.02[amb];[0:a][amb]amix=inputs=2:duration=first:dropout_transition=3",
            "-codec:a", "libmp3lame", "-q:a", "4",
            final_path
        ], capture_output=True, text=True, timeout=300)

        if mix.returncode != 0:
            print(f"FAIL ffmpeg: {mix.stderr[:200]}")
            os.unlink(speech_path)
            sys.exit(1)
    else:
        subprocess.run([
            "ffmpeg", "-y", "-i", speech_path,
            "-codec:a", "libmp3lame", "-q:a", "4", final_path
        ], capture_output=True, timeout=300)

    os.unlink(speech_path)
    size = os.path.getsize(final_path)
    print(f"OK {audio_filename} ({size / (1024*1024):.1f} MB)")

if __name__ == "__main__":
    main()
