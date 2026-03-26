#!/usr/bin/env python3
"""Generate TTS audio by splitting long texts into chunks.
Prevents edge-tts from hanging on very long texts.
Usage: python3 tools/gen_chunked.py <episode_id>
"""
import json, os, sys, subprocess, tempfile, glob

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(PROJECT_ROOT, "audio")
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "scripts")
AMBIENT_FILE = os.path.join(PROJECT_ROOT, "assets", "ambient_crackling.wav")
EPISODES_FILE = os.path.join(PROJECT_ROOT, "episodes.json")

MAX_CHUNK_CHARS = 5000  # ~1000 words, ~1-2 min audio per chunk

def split_text(text, max_chars=MAX_CHUNK_CHARS):
    """Split text into chunks at paragraph boundaries."""
    paragraphs = text.split('\n\n')
    chunks = []
    current = ""
    for para in paragraphs:
        if len(current) + len(para) + 2 > max_chars and current:
            chunks.append(current.strip())
            current = para
        else:
            current = current + "\n\n" + para if current else para
    if current.strip():
        chunks.append(current.strip())
    return chunks

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
        print(f"SKIP no script")
        sys.exit(1)

    with open(script_path) as f:
        text = f.read()

    chunks = split_text(text)
    print(f"Split into {len(chunks)} chunks ({len(text)} chars total)", flush=True)

    chunk_files = []
    tmpdir = tempfile.mkdtemp()

    for i, chunk in enumerate(chunks):
        chunk_file = os.path.join(tmpdir, f"chunk_{i}.txt")
        chunk_mp3 = os.path.join(tmpdir, f"chunk_{i}.mp3")

        with open(chunk_file, 'w') as f:
            f.write(chunk)

        print(f"  Chunk {i+1}/{len(chunks)} ({len(chunk)} chars)...", flush=True)

        success = False
        for attempt in range(3):
            try:
                proc = subprocess.Popen(
                    [sys.executable, "-m", "edge_tts",
                     "-v", "en-GB-RyanNeural",
                     "--rate=-15%", "--pitch=-12Hz", "--volume=+0%",
                     "-f", chunk_file,
                     "--write-media", chunk_mp3],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    preexec_fn=os.setsid
                )
                try:
                    stdout, stderr = proc.communicate(timeout=180)
                except subprocess.TimeoutExpired:
                    import signal
                    os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                    proc.wait()
                    print(f"    Timeout attempt {attempt+1}", flush=True)
                    continue

                if proc.returncode == 0 and os.path.exists(chunk_mp3) and os.path.getsize(chunk_mp3) > 1000:
                    chunk_files.append(chunk_mp3)
                    success = True
                    break
                else:
                    print(f"    Retry {attempt+1}: {stderr.decode()[:100]}", flush=True)
            except Exception as e:
                print(f"    Error attempt {attempt+1}: {e}", flush=True)

        if not success:
            print(f"FAIL chunk {i+1} failed after 3 attempts")
            # Cleanup
            import shutil
            shutil.rmtree(tmpdir, ignore_errors=True)
            sys.exit(1)

    # Concatenate chunks
    if len(chunk_files) == 1:
        speech_path = chunk_files[0]
    else:
        concat_list = os.path.join(tmpdir, "concat.txt")
        with open(concat_list, 'w') as f:
            for cf in chunk_files:
                f.write(f"file '{cf}'\n")
        speech_path = os.path.join(tmpdir, "concat.mp3")
        result = subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", concat_list, "-c", "copy", speech_path
        ], capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            print(f"FAIL concat: {result.stderr[:200]}")
            import shutil
            shutil.rmtree(tmpdir, ignore_errors=True)
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
            "ffmpeg", "-y", "-i", speech_path,
            "-stream_loop", "-1", "-i", AMBIENT_FILE,
            "-filter_complex",
            f"[1:a]atrim=0:{dur},volume=0.02[amb];[0:a][amb]amix=inputs=2:duration=first:dropout_transition=3",
            "-codec:a", "libmp3lame", "-q:a", "4",
            final_path
        ], capture_output=True, text=True, timeout=300)

        if mix.returncode != 0:
            print(f"FAIL ffmpeg mix: {mix.stderr[:200]}")
            import shutil
            shutil.rmtree(tmpdir, ignore_errors=True)
            sys.exit(1)
    else:
        subprocess.run([
            "ffmpeg", "-y", "-i", speech_path,
            "-codec:a", "libmp3lame", "-q:a", "4", final_path
        ], capture_output=True, timeout=300)

    import shutil
    shutil.rmtree(tmpdir, ignore_errors=True)

    size = os.path.getsize(final_path)
    print(f"OK {audio_filename} ({size / (1024*1024):.1f} MB)")

if __name__ == "__main__":
    main()
