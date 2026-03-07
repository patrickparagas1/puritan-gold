#!/usr/bin/env python3
"""
Puritan Gold -- Monthly Content Generation Pipeline.

Main entry point for generating devotional scripts, TTS audio, and updating
the episode registry for any month and section.

Usage:
    python3 tools/generate_month.py --month march --section family
    python3 tools/generate_month.py --month april --section all
    python3 tools/generate_month.py --month all --section all
    python3 tools/generate_month.py --month march --section family --scripts-only
    python3 tools/generate_month.py --month march --section family --start-day 15

Sections:
    family    -- Family Devotional (IDs 101+)
    school    -- Puritan Academy / Homeschool (IDs 201+)
    together  -- Couples Devotional (IDs 301+)
    personal  -- Personal Growth (IDs 401+)
    study     -- Study Devotional (IDs 501+ for April onwards, 1-31 for March)
    all       -- All sections for the given month

Months:
    march, april, all
"""

import argparse
import importlib
import json
import os
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(TOOLS_DIR)

sys.path.insert(0, TOOLS_DIR)
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.expanduser("~/Library/Python/3.9/lib/python/site-packages"))

AUDIO_DIR = os.path.join(PROJECT_ROOT, "audio")
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "scripts")
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")
AMBIENT_FILE = os.path.join(ASSETS_DIR, "ambient_crackling.wav")
EPISODES_FILE = os.path.join(PROJECT_ROOT, "episodes.json")

# ---------------------------------------------------------------------------
# Section configuration
# ---------------------------------------------------------------------------
# Maps section name -> (content module path pattern, generator module, generator func,
#                        ID offset, file prefix, series name, section tag)

SECTION_CONFIG = {
    "family": {
        "content_module": "tools.content.{month}.family_{month}",
        "generator_module": "tools.generators.family_generator",
        "generator_func": "generate_family_script",
        "id_offset": 100,          # IDs are 101, 102, ...
        "file_prefix": "family",
        "series": "Family Devotional",
        "section_tag": "family",
    },
    "school": {
        "content_module": "tools.content.{month}.school_{month}",
        "generator_module": "tools.generators.school_generator",
        "generator_func": "generate_school_script",
        "id_offset": 200,          # IDs are 201, 202, ...
        "file_prefix": "school",
        "series": "Homeschool",
        "section_tag": "school",
    },
    "together": {
        "content_module": "tools.content.{month}.together_{month}",
        "generator_module": "tools.generators.together_generator",
        "generator_func": "generate_together_script",
        "id_offset": 300,          # IDs are 301, 302, ...
        "file_prefix": "together",
        "series": "Together",
        "section_tag": "together",
    },
    "personal": {
        "content_module": "tools.content.{month}.personal_{month}",
        "generator_module": "tools.generators.personal_generator",
        "generator_func": "generate_personal_script",
        "id_offset": 400,          # IDs are 401, 402, ...
        "file_prefix": "personal",
        "series": "Personal Growth",
        "section_tag": "personal",
    },
    "study": {
        "content_module": "tools.content.{month}.study_{month}",
        "generator_module": "tools.generators.study_generator",
        "generator_func": "generate_study_script",
        "id_offset": 0,            # March 1-31, April 32-61 (month offset adds 31)
        "file_prefix": "ep",       # matches existing ep001.mp3 convention
        "series": "Study",
        "section_tag": "study",
    },
}

ALL_SECTIONS = list(SECTION_CONFIG.keys())
ALL_MONTHS = ["march", "april"]


# ---------------------------------------------------------------------------
# Audio pipeline helpers (mirrors create_episode.py / generate_all_sections.py)
# ---------------------------------------------------------------------------

def get_mp3_duration(filepath):
    """Get duration of an MP3 file using ffprobe. Returns (str, float)."""
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
        return "0:00", 0.0


def generate_audio(script_text, output_path):
    """
    Generate TTS audio from script text, mix with ambient crackling,
    and produce the final MP3.

    Uses edge_tts with voice en-GB-RyanNeural, rate -15%, pitch -12Hz.
    Mixes ambient crackling at 18% volume via ffmpeg with warm EQ.
    """
    from tts_engine import text_to_speech

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        speech_path = tmp.name

    try:
        # Step 1: TTS
        text_to_speech(script_text, speech_path)

        # Step 2: Mix with ambient
        if os.path.exists(AMBIENT_FILE):
            _, duration_secs = get_mp3_duration(speech_path)
            subprocess.run([
                "ffmpeg", "-y",
                "-i", speech_path,
                "-stream_loop", "-1", "-i", AMBIENT_FILE,
                "-filter_complex",
                f"[1:a]atrim=0:{duration_secs},volume=0.08,"
                f"lowpass=f=800,highpass=f=60,"
                f"equalizer=f=300:width_type=o:width=1.5:g=3[amb];"
                f"[0:a][amb]amix=inputs=2:duration=first:dropout_transition=3",
                "-codec:a", "libmp3lame", "-q:a", "4",
                output_path
            ], capture_output=True)
        else:
            subprocess.run([
                "ffmpeg", "-y", "-i", speech_path,
                "-codec:a", "libmp3lame", "-q:a", "4",
                output_path
            ], capture_output=True)
    finally:
        if os.path.exists(speech_path):
            os.unlink(speech_path)


def generate_audio_worker(args):
    """
    Worker function for ProcessPoolExecutor.

    Parameters
    ----------
    args : tuple
        (script_text, output_path, episode_id, title)

    Returns
    -------
    dict
        Result with keys: id, title, audio_path, duration_str, duration_secs,
        file_size, success, error
    """
    script_text, output_path, episode_id, title = args
    try:
        generate_audio(script_text, output_path)
        duration_str, duration_secs = get_mp3_duration(output_path)
        file_size = os.path.getsize(output_path)
        return {
            "id": episode_id,
            "title": title,
            "audio_path": output_path,
            "duration_str": duration_str,
            "duration_secs": duration_secs,
            "file_size": file_size,
            "success": True,
            "error": None,
        }
    except Exception as e:
        return {
            "id": episode_id,
            "title": title,
            "audio_path": output_path,
            "duration_str": "0:00",
            "duration_secs": 0,
            "file_size": 0,
            "success": False,
            "error": str(e),
        }


# ---------------------------------------------------------------------------
# Episode registry helpers
# ---------------------------------------------------------------------------

def load_episodes():
    """Load existing episodes.json."""
    if os.path.exists(EPISODES_FILE):
        with open(EPISODES_FILE, "r") as f:
            return json.load(f)
    return []


def save_episodes(episodes):
    """Save episodes.json, sorted by ID."""
    episodes.sort(key=lambda e: e["id"])
    with open(EPISODES_FILE, "w") as f:
        json.dump(episodes, f, indent=2)


def upsert_episode(episodes, entry):
    """Insert or update an episode entry by ID."""
    episodes = [e for e in episodes if e.get("id") != entry["id"]]
    episodes.append(entry)
    return episodes


# ---------------------------------------------------------------------------
# Content loading
# ---------------------------------------------------------------------------

def load_content_data(month, section):
    """
    Dynamically import the content data module for a given month and section.

    Returns the EPISODES list from the module, or None if the module does
    not exist yet.
    """
    config = SECTION_CONFIG[section]
    module_path = config["content_module"].format(month=month)

    try:
        mod = importlib.import_module(module_path)
        # Try multiple conventions: EPISODES, SECTION_MONTH, etc.
        for attr_name in [
            "EPISODES",
            f"{section.upper()}_{month.upper()}",    # e.g. PERSONAL_MARCH
            f"{section.upper()}_{month.upper()}_EPISODES",
        ]:
            data = getattr(mod, attr_name, None)
            if data is not None:
                return data
        # Fallback: look for any list attribute
        for attr_name in dir(mod):
            val = getattr(mod, attr_name)
            if isinstance(val, list) and len(val) > 0 and isinstance(val[0], dict):
                return val
        return None
    except ModuleNotFoundError:
        return None
    except Exception as e:
        print(f"  ERROR loading {module_path}: {e}")
        return None


def load_generator(section):
    """
    Dynamically import the generator function for a section.

    Returns the callable generator function.
    """
    config = SECTION_CONFIG[section]
    mod = importlib.import_module(config["generator_module"])
    return getattr(mod, config["generator_func"])


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def process_section(month, section, scripts_only=False, start_day=1,
                    workers=4, skip_existing=True):
    """
    Process a single section for a given month.

    Steps:
        1. Load content data module
        2. Load generator function
        3. For each episode: generate script text, save to scripts/
        4. (Unless scripts_only) Generate audio using ProcessPoolExecutor
        5. Update episodes.json

    Parameters
    ----------
    month : str
        Month name (e.g., "march", "april").
    section : str
        Section name (e.g., "family", "school").
    scripts_only : bool
        If True, generate scripts but skip audio generation.
    start_day : int
        Start from this day number (for resuming interrupted runs).
    workers : int
        Number of parallel workers for audio generation.
    skip_existing : bool
        If True, skip episodes whose audio files already exist.
    """
    config = SECTION_CONFIG[section]
    print(f"\n{'=' * 60}")
    print(f"  {section.upper()} -- {month.upper()}")
    print(f"{'=' * 60}")

    # Load content data
    content = load_content_data(month, section)
    if content is None:
        print(f"  No content data found for {month}/{section}. Skipping.")
        print(f"  (Expected module: {config['content_module'].format(month=month)})")
        return

    # Load generator
    try:
        generator = load_generator(section)
    except Exception as e:
        print(f"  ERROR loading generator for {section}: {e}")
        return

    # Ensure directories exist
    os.makedirs(SCRIPTS_DIR, exist_ok=True)
    os.makedirs(AUDIO_DIR, exist_ok=True)

    # Compute month-based ID offset: April IDs continue after March
    # March episodes for each section:
    #   family: 31 (101-131), school: 20 (201-220), together: 31 (301-331),
    #   personal: 31 (401-431), study: 31 (1-31)
    MARCH_EPISODE_COUNTS = {
        "family": 31, "school": 20, "together": 31,
        "personal": 31, "study": 31,
    }
    month_id_offset = MARCH_EPISODE_COUNTS.get(section, 0) if month != "march" else 0
    base_id_offset = config["id_offset"] + month_id_offset

    # Filter by start_day
    episodes = [ep for ep in content if ep.get("day", 0) >= start_day]
    if not episodes:
        print(f"  No episodes to process (start_day={start_day}).")
        return

    print(f"  Found {len(episodes)} episodes to process.")
    print(f"  ID range: {base_id_offset + 1} - {base_id_offset + max(e['day'] for e in episodes)}")
    print()

    # Phase 1: Generate scripts
    audio_tasks = []
    for ep in episodes:
        day = ep["day"]
        ep_id = base_id_offset + day
        title = ep.get("title", f"Day {day}")
        prefix = config["file_prefix"]

        script_path = os.path.join(SCRIPTS_DIR, f"{prefix}_{ep_id}.txt")
        audio_path = os.path.join(AUDIO_DIR, f"{prefix}_{ep_id}.mp3")

        # Check if audio already exists
        if skip_existing and os.path.exists(audio_path) and not scripts_only:
            print(f"  [SKIP] Day {day}: {title} (audio exists)")
            continue

        # Generate script
        print(f"  [SCRIPT] Day {day}: {title}...", end=" ", flush=True)
        try:
            script_text = generator(ep)
            word_count = len(script_text.split())
            with open(script_path, "w") as f:
                f.write(script_text)
            print(f"({word_count} words, saved to {os.path.basename(script_path)})")
        except Exception as e:
            print(f"ERROR: {e}")
            continue

        if not scripts_only:
            audio_tasks.append((script_text, audio_path, ep_id, title))

    if scripts_only:
        print(f"\n  Scripts generated. Skipping audio (--scripts-only).")
        return

    if not audio_tasks:
        print(f"\n  No audio to generate (all episodes up to date).")
        return

    # Phase 2: Generate audio in parallel
    print(f"\n  Generating audio for {len(audio_tasks)} episodes "
          f"({workers} workers)...")
    print()

    results = []
    start_time = time.time()

    with ProcessPoolExecutor(max_workers=workers) as executor:
        future_map = {
            executor.submit(generate_audio_worker, task): task
            for task in audio_tasks
        }
        for future in as_completed(future_map):
            result = future.result()
            results.append(result)
            if result["success"]:
                size_mb = result["file_size"] / (1024 * 1024)
                print(
                    f"  [AUDIO] ID {result['id']}: {result['title']} "
                    f"-- {result['duration_str']} ({size_mb:.1f} MB)"
                )
            else:
                print(
                    f"  [ERROR] ID {result['id']}: {result['title']} "
                    f"-- {result['error']}"
                )

    elapsed = time.time() - start_time
    success_count = sum(1 for r in results if r["success"])
    print(f"\n  Audio generation complete: {success_count}/{len(results)} "
          f"succeeded in {elapsed:.0f}s")

    # Phase 3: Update episodes.json
    print(f"  Updating episodes.json...")
    all_episodes = load_episodes()

    for result in results:
        if not result["success"]:
            continue

        ep_id = result["id"]
        day = ep_id - base_id_offset
        ep_data = next((e for e in content if e.get("day") == day), {})
        prefix = config["file_prefix"]

        entry = {
            "id": ep_id,
            "title": result["title"],
            "subtitle": ep_data.get("subtitle", ""),
            "description": ep_data.get("description", result["title"]),
            "file": f"audio/{prefix}_{ep_id}.mp3",
            "duration": result["duration_str"],
            "durationSecs": int(result["duration_secs"]),
            "fileSize": result["file_size"],
            "date": ep_data.get("date", datetime.now().strftime("%Y-%m-%d")),
            "series": config["series"],
            "section": config["section_tag"],
            "tags": ep_data.get("tags", [section]),
        }

        # Include extra metadata based on section
        if section == "family":
            if "memory_verse" in ep_data and "memory_verse_ref" in ep_data:
                entry["memoryVerse"] = (
                    f"{ep_data['memory_verse']} -- "
                    f"{ep_data['memory_verse_ref']}"
                )
            if "discussion_questions" in ep_data:
                entry["discussionQuestions"] = ep_data["discussion_questions"]

        elif section == "school":
            if "unit_name" in ep_data:
                entry["unit"] = ep_data["unit_name"]
            if "lesson_number" in ep_data:
                entry["lessonNumber"] = ep_data["lesson_number"]
            if "review_questions" in ep_data:
                entry["reviewQuestions"] = ep_data["review_questions"]
            if "activity_description" in ep_data:
                entry["activity"] = ep_data["activity_description"]

        elif section == "together":
            if "reflection_questions" in ep_data:
                entry["reflectionPrompt"] = " | ".join(
                    ep_data["reflection_questions"]
                )
            if "prayer_focus" in ep_data:
                entry["prayerFocus"] = ep_data["prayer_focus"]

        elif section == "personal":
            if "personal_type" in ep_data:
                entry["personalType"] = ep_data["personal_type"]

        # Add day field for proper app rendering
        entry["day"] = day

        all_episodes = upsert_episode(all_episodes, entry)

    save_episodes(all_episodes)
    print(f"  Done. Total episodes in registry: {len(all_episodes)}")


def process_month(month, sections, scripts_only=False, start_day=1,
                  workers=4, skip_existing=True):
    """Process all requested sections for a given month."""
    print(f"\n{'#' * 60}")
    print(f"  PROCESSING: {month.upper()}")
    print(f"  Sections: {', '.join(sections)}")
    print(f"{'#' * 60}")

    for section in sections:
        process_section(
            month=month,
            section=section,
            scripts_only=scripts_only,
            start_day=start_day,
            workers=workers,
            skip_existing=skip_existing,
        )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Puritan Gold -- Monthly Content Generation Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 tools/generate_month.py --month march --section family
  python3 tools/generate_month.py --month april --section all
  python3 tools/generate_month.py --month all --section all
  python3 tools/generate_month.py --month march --section family --scripts-only
  python3 tools/generate_month.py --month march --section school --start-day 10
  python3 tools/generate_month.py --month march --section all --workers 2
        """
    )

    parser.add_argument(
        "--month", required=True,
        choices=ALL_MONTHS + ["all"],
        help="Month to generate content for (march, april, or all)"
    )
    parser.add_argument(
        "--section", required=True,
        choices=ALL_SECTIONS + ["all"],
        help="Section to generate (family, school, together, personal, study, or all)"
    )
    parser.add_argument(
        "--scripts-only", action="store_true",
        help="Generate script text files only, skip audio generation"
    )
    parser.add_argument(
        "--start-day", type=int, default=1,
        help="Start from this day number (default: 1)"
    )
    parser.add_argument(
        "--workers", type=int, default=4,
        help="Number of parallel workers for audio generation (default: 4)"
    )
    parser.add_argument(
        "--no-skip", action="store_true",
        help="Regenerate audio even if files already exist"
    )

    args = parser.parse_args()

    # Determine months and sections to process
    months = ALL_MONTHS if args.month == "all" else [args.month]
    sections = ALL_SECTIONS if args.section == "all" else [args.section]

    print("=" * 60)
    print("  PURITAN GOLD -- Content Generation Pipeline")
    print("=" * 60)
    print(f"  Months:        {', '.join(months)}")
    print(f"  Sections:      {', '.join(sections)}")
    print(f"  Scripts only:  {args.scripts_only}")
    print(f"  Start day:     {args.start_day}")
    print(f"  Workers:       {args.workers}")
    print(f"  Skip existing: {not args.no_skip}")
    print(f"  Project root:  {PROJECT_ROOT}")
    print("=" * 60)

    start_time = time.time()

    for month in months:
        process_month(
            month=month,
            sections=sections,
            scripts_only=args.scripts_only,
            start_day=args.start_day,
            workers=args.workers,
            skip_existing=not args.no_skip,
        )

    elapsed = time.time() - start_time
    print(f"\n{'=' * 60}")
    print(f"  PIPELINE COMPLETE in {elapsed:.0f}s")
    print(f"{'=' * 60}")

    # Summary
    if os.path.exists(EPISODES_FILE):
        with open(EPISODES_FILE, "r") as f:
            all_eps = json.load(f)
        total_duration = sum(e.get("durationSecs", 0) for e in all_eps)
        hours = total_duration // 3600
        minutes = (total_duration % 3600) // 60
        print(f"  Total episodes in registry: {len(all_eps)}")
        print(f"  Total duration: {hours}h {minutes}m")

        # Per-section breakdown
        section_counts = {}
        for e in all_eps:
            s = e.get("section", "unknown")
            section_counts[s] = section_counts.get(s, 0) + 1
        for s, c in sorted(section_counts.items()):
            print(f"    {s}: {c} episodes")

    print()


if __name__ == "__main__":
    main()
