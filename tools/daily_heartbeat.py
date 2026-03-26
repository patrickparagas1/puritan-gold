#!/usr/bin/env python3
"""
Daily Heartbeat — generates one new episode per section each day.
Runs via GitHub Actions cron or manually.
"""

import json
import os
import sys
import random
import asyncio
import subprocess
from datetime import datetime, timezone, timedelta

# ── Config ──────────────────────────────────────────────────
SECTIONS = ["study", "family", "school", "together", "personal"]
EPISODES_JSON = "episodes.json"
SCRIPTS_DIR = "scripts"
AUDIO_DIR = "audio"
ASSETS_DIR = "assets"
AMBIENT_FILE = os.path.join(ASSETS_DIR, "ambient_crackling.wav")

VOICE = "en-GB-RyanNeural"
RATE = "-15%"
PITCH = "-12Hz"

EST = timezone(timedelta(hours=-5))
TODAY = datetime.now(EST).strftime("%Y-%m-%d")
TODAY_DISPLAY = datetime.now(EST).strftime("%B %d, %Y")

# ── Puritan source excerpts for prompts ─────────────────────
PURITAN_SOURCES = [
    ("John Owen", "The Mortification of Sin", "mortification"),
    ("Thomas Watson", "A Body of Divinity", "body-of-divinity"),
    ("Richard Baxter", "The Reformed Pastor", "reformed-pastor"),
    ("John Bunyan", "The Pilgrim's Progress", "pilgrims-progress"),
    ("Thomas Boston", "Human Nature in Its Fourfold State", "fourfold-state"),
    ("Jonathan Edwards", "Religious Affections", "religious-affections"),
    ("C.H. Spurgeon", "All of Grace", "all-of-grace"),
    ("John Calvin", "Institutes of the Christian Religion", "institutes-book-one"),
    ("Arthur Pink", "The Attributes of God", "attributes-of-god"),
    ("Arthur Pink", "The Sovereignty of God", "sovereignty-of-god"),
    ("John Owen", "The Glory of Christ", "glory-of-christ"),
    ("John Flavel", "The Mystery of Providence", "mystery-of-providence"),
    ("John Flavel", "Keeping the Heart", "keeping-the-heart"),
    ("Jeremiah Burroughs", "The Rare Jewel of Christian Contentment", "rare-jewel"),
    ("Richard Sibbes", "The Bruised Reed", "bruised-reed"),
    ("Thomas Brooks", "Precious Remedies Against Satan's Devices", "precious-remedies"),
    ("C.H. Spurgeon", "Lectures to My Students", "lectures-to-students"),
    ("Thomas Goodwin", "The Heart of Christ", "heart-of-christ"),
    ("Arthur Pink", "Exposition of 1 John", "exposition-1-john"),
    ("Arthur Pink", "Dispensationalism", "dispensationalism"),
]

# ── Section-specific prompts ────────────────────────────────
SECTION_PROMPTS = {
    "study": """You are a Reformed theologian creating a 10-minute daily study episode for "Puritan Gold."
Today's source: "{author}" — "{book}"
Here is an excerpt from the book:

{excerpt}

Write a deep theological study episode (about 1500 words) that:
- Opens with a relevant Scripture passage (KJV)
- Exposits the key doctrine from this excerpt
- Connects it to the broader Reformed tradition
- Applies it to the Christian life today
- Closes with a prayer

Title the episode with a compelling theological title. Format:
TITLE: [Your Title]
CONTENT:
[Your content]""",

    "family": """You are a wise Puritan pastor creating a 10-minute family devotional for "Puritan Gold."
Today's source: "{author}" — "{book}"
Here is an excerpt:

{excerpt}

Write a warm family devotional episode (about 1500 words) that:
- Opens with a Scripture passage (KJV)
- Explains the truth in a way parents and children can discuss together
- Includes 2-3 discussion questions for the family
- Provides a practical family application
- Closes with a family prayer

Title it warmly. Format:
TITLE: [Your Title]
CONTENT:
[Your content]""",

    "school": """You are a Puritan educator creating a 10-minute youth lesson for "Puritan Gold."
Today's source: "{author}" — "{book}"
Here is an excerpt:

{excerpt}

Write an engaging youth study episode (about 1500 words) that:
- Opens with a Scripture passage (KJV)
- Explains the doctrine in clear, accessible language for teens and young adults
- Uses vivid illustrations and examples
- Includes thought-provoking questions
- Applies the truth to challenges young people face today
- Closes with a prayer

Title it to grab a young person's attention. Format:
TITLE: [Your Title]
CONTENT:
[Your content]""",

    "together": """You are a Puritan minister creating a 10-minute group discussion episode for "Puritan Gold."
Today's source: "{author}" — "{book}"
Here is an excerpt:

{excerpt}

Write a group study episode (about 1500 words) that:
- Opens with a Scripture passage (KJV)
- Presents the key truth from this passage
- Includes 4-5 discussion questions for small groups
- Provides cross-references to related Scripture
- Suggests a group activity or prayer exercise
- Closes with a corporate prayer

Format:
TITLE: [Your Title]
CONTENT:
[Your content]""",

    "personal": """You are a Puritan devotional writer creating a 10-minute personal growth episode for "Puritan Gold."
Today's source: "{author}" — "{book}"
Here is an excerpt:

{excerpt}

Write a personal devotional episode (about 1500 words) that:
- Opens with a Scripture passage (KJV)
- Meditates deeply on the spiritual truth in this excerpt
- Provides searching self-examination questions
- Gives practical directions for spiritual growth
- Closes with a personal prayer of application

Title it for deep personal reflection. Format:
TITLE: [Your Title]
CONTENT:
[Your content]""",
}


def load_episodes():
    with open(EPISODES_JSON) as f:
        return json.load(f)


def save_episodes(episodes):
    with open(EPISODES_JSON, "w") as f:
        json.dump(episodes, f, indent=2)


def get_next_id(episodes):
    return max(e["id"] for e in episodes) + 1


def already_generated_today(episodes):
    """Check if today's episodes already exist."""
    for ep in episodes:
        if ep.get("date") == TODAY and ep.get("heartbeat"):
            return True
    return False


def pick_source_and_excerpt():
    """Pick a random Puritan source and extract an excerpt."""
    author, book, slug = random.choice(PURITAN_SOURCES)

    # Find script files for this topic
    script_files = []
    for fn in os.listdir(SCRIPTS_DIR):
        if fn.startswith("ep_") and fn.endswith(".txt"):
            path = os.path.join(SCRIPTS_DIR, fn)
            # Read first line to check if it's from this topic
            try:
                with open(path) as f:
                    first_line = f.readline()
                if slug.replace("-", " ") in first_line.lower() or book.lower() in first_line.lower():
                    script_files.append(path)
            except:
                pass

    if not script_files:
        # Fallback: use any random script
        all_scripts = [os.path.join(SCRIPTS_DIR, f) for f in os.listdir(SCRIPTS_DIR)
                       if f.startswith("ep_") and f.endswith(".txt")]
        if all_scripts:
            script_files = [random.choice(all_scripts)]

    if not script_files:
        return author, book, "The fear of the Lord is the beginning of wisdom."

    # Pick a random script and extract ~500 words from a random position
    chosen = random.choice(script_files)
    with open(chosen) as f:
        text = f.read()

    words = text.split()
    if len(words) > 600:
        start = random.randint(100, max(100, len(words) - 500))
        excerpt = " ".join(words[start:start + 500])
    else:
        excerpt = " ".join(words[:500])

    return author, book, excerpt


def generate_with_gemini(section, author, book, excerpt):
    """Call Gemini API to generate episode content."""
    try:
        import google.generativeai as genai
    except ImportError:
        print("google-generativeai not installed, using fallback content")
        return None, None

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY not set, using fallback content")
        return None, None

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")

    prompt = SECTION_PROMPTS[section].format(
        author=author, book=book, excerpt=excerpt
    )

    try:
        response = model.generate_content(prompt)
        text = response.text

        # Parse title and content
        title = None
        content = text
        if "TITLE:" in text:
            parts = text.split("CONTENT:", 1)
            title_part = parts[0].replace("TITLE:", "").strip()
            title = title_part.strip().strip('"').strip("'")
            if len(parts) > 1:
                content = parts[1].strip()

        return title, content
    except Exception as e:
        print(f"Gemini API error for {section}: {e}")
        return None, None


def get_script_path(section, episode_id):
    """Get script file path based on section."""
    if section == "study":
        return os.path.join(SCRIPTS_DIR, f"ep_{episode_id}.txt")
    elif section == "personal":
        return os.path.join(SCRIPTS_DIR, f"ep_{episode_id}.txt")
    else:
        return os.path.join(SCRIPTS_DIR, f"{section}_{episode_id}.txt")


def get_audio_path(section, episode_id):
    """Get audio file path."""
    if section in ("study", "personal"):
        return os.path.join(AUDIO_DIR, f"ep{episode_id}.mp3")
    else:
        return os.path.join(AUDIO_DIR, f"{section}_{episode_id}.mp3")


async def generate_tts(text, output_path):
    """Generate TTS audio using edge-tts."""
    import edge_tts

    speech_path = output_path.replace(".mp3", "_speech.mp3")

    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE,
        rate=RATE,
        pitch=PITCH,
        volume="+0%",
    )
    await communicate.save(speech_path)

    # Mix with ambient if available
    if os.path.exists(AMBIENT_FILE):
        try:
            subprocess.run([
                "ffmpeg", "-y",
                "-i", speech_path,
                "-i", AMBIENT_FILE,
                "-filter_complex",
                "[1:a]aloop=loop=-1:size=2e+09[bg];[bg]volume=0.02[bgq];[0:a][bgq]amix=inputs=2:duration=first:dropout_transition=3[out]",
                "-map", "[out]",
                "-codec:a", "libmp3lame", "-b:a", "64k",
                output_path
            ], check=True, capture_output=True, timeout=300)
            os.remove(speech_path)
        except Exception as e:
            print(f"FFmpeg mixing failed: {e}, using raw speech")
            os.rename(speech_path, output_path)
    else:
        os.rename(speech_path, output_path)


def get_mp3_duration(filepath):
    """Get duration of an MP3 file."""
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


def main():
    print(f"=== Daily Heartbeat: {TODAY_DISPLAY} ===")

    episodes = load_episodes()

    # Check idempotency
    if already_generated_today(episodes):
        print(f"Episodes already generated for {TODAY}, skipping.")
        return

    next_id = get_next_id(episodes)
    new_episodes = []

    for i, section in enumerate(SECTIONS):
        episode_id = next_id + i
        print(f"\n[{i+1}/5] Generating {section} episode (ID {episode_id})...")

        # Pick source material
        author, book, excerpt = pick_source_and_excerpt()
        print(f"  Source: {author} — {book}")

        # Generate content with Gemini
        title, content = generate_with_gemini(section, author, book, excerpt)

        if not title or not content:
            # Fallback: use the excerpt directly
            title = f"Daily Meditation from {author}"
            content = f"PURITAN GOLD -- Daily Heartbeat\n{TODAY_DISPLAY}\n\n---\n\n"
            content += f"From \"{book}\" by {author}:\n\n{excerpt}"

        # Write script
        script_path = get_script_path(section, episode_id)
        header = f"PURITAN GOLD -- Daily Heartbeat: {section.title()}\n"
        header += f"{title}\n{TODAY_DISPLAY}\n\n---\n\n"
        full_script = header + content

        with open(script_path, "w") as f:
            f.write(full_script)
        print(f"  Script: {script_path} ({len(content.split())} words)")

        # Generate TTS
        audio_path = get_audio_path(section, episode_id)
        try:
            asyncio.run(generate_tts(full_script, audio_path))
            duration_str, duration_secs = get_mp3_duration(audio_path)
            file_size = os.path.getsize(audio_path)
            print(f"  Audio: {audio_path} ({duration_str})")
        except Exception as e:
            print(f"  TTS failed: {e}")
            duration_str, duration_secs, file_size = "0:00", 0, 0
            audio_path = None

        # Build episode entry
        section_labels = {
            "study": "Study", "family": "Family",
            "school": "School", "together": "Together",
            "personal": "Growth"
        }

        ep = {
            "id": episode_id,
            "title": title,
            "section": section,
            "date": TODAY,
            "heartbeat": True,
            "file": f"audio/{os.path.basename(audio_path)}" if audio_path else None,
            "audio": f"audio/{os.path.basename(audio_path)}" if audio_path else None,
            "duration": duration_str,
            "durationSecs": round(duration_secs),
            "fileSize": file_size,
            "tags": [section_labels.get(section, section), "Daily", author],
        }

        if section == "personal":
            ep["topic"] = None  # standalone growth episode

        new_episodes.append(ep)

    # Add new episodes to the list
    episodes.extend(new_episodes)
    save_episodes(episodes)

    print(f"\n=== Done! Generated {len(new_episodes)} episodes for {TODAY} ===")
    for ep in new_episodes:
        print(f"  [{ep['section']:10s}] ID {ep['id']}: {ep['title'][:50]}")


if __name__ == "__main__":
    main()
