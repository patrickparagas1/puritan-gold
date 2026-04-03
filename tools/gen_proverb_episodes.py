#!/usr/bin/env python3
"""
Generate daily Proverb podcast episodes with audio.
Each day maps to a Proverbs chapter. Monthly themes rotate.
Short months: last day covers remaining chapters.
"""

import asyncio, os, json, sys, urllib.request, urllib.parse
from datetime import datetime, timedelta
import calendar

VOICE = "en-GB-RyanNeural"
RATE = "-5%"
PITCH = "-4Hz"
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
AUDIO_DIR = os.path.join(BASE_DIR, "audio")
EPISODES_FILE = os.path.join(BASE_DIR, "episodes.json")

THEMES = [
    {"name": "Wisdom & Knowledge", "desc": "The foundation of wisdom begins with knowing God"},
    {"name": "Family & Love", "desc": "Proverbs on relationships, marriage, and family bonds"},
    {"name": "Work & Diligence", "desc": "Wisdom for effort, perseverance, and stewardship"},
    {"name": "Speech & Words", "desc": "The power of the tongue and gentle answers"},
    {"name": "Justice & Righteousness", "desc": "Walking uprightly with moral courage"},
    {"name": "Humility & Fear of the Lord", "desc": "The beginning of wisdom and a humble heart"},
    {"name": "Wealth & Generosity", "desc": "Stewardship, contentment, and giving to others"},
    {"name": "Character & Integrity", "desc": "A life of honor, truth, and faithfulness"},
    {"name": "Discipline & Growth", "desc": "Correction, training, and spiritual maturity"},
    {"name": "Leadership & Counsel", "desc": "Wise leadership and seeking godly advice"},
    {"name": "Trust & Providence", "desc": "Trusting in the Lord and His sovereign care"},
    {"name": "Gratitude & Reflection", "desc": "Year-end review of wisdom gained"},
]


def fetch_chapter(chapter):
    url = f"https://bible-api.com/proverbs+{chapter}?translation=kjv"
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read())
            return " ".join(v["text"].replace("\n", " ").strip() for v in data.get("verses", []))
    except Exception as e:
        print(f"  ERROR fetching Proverbs {chapter}: {e}")
        return None


def build_script(chapters, theme):
    parts = [f"Puritan Gold — Daily Proverbs. This month's theme: {theme['name']}. {theme['desc']}."]
    for ch in chapters:
        text = fetch_chapter(ch)
        if text:
            if len(chapters) > 1:
                parts.append(f"Proverbs chapter {ch}.")
            else:
                parts.append(f"Proverbs, chapter {ch}.")
            parts.append(text)
    parts.append("May the wisdom of Proverbs guide your steps today. Puritan Gold.")
    return " ".join(parts)


async def generate_episode(ep_id, date_str, chapters, theme, month_year):
    import edge_tts

    audio_file = f"audio/proverb_{ep_id}.mp3"
    audio_path = os.path.join(BASE_DIR, audio_file)

    if os.path.exists(audio_path) and os.path.getsize(audio_path) > 1000:
        print(f"  SKIP ep {ep_id} — exists")
        # Still return episode data for JSON
        size = os.path.getsize(audio_path)
        # Estimate duration from file size (~16KB/sec for speech MP3)
        dur_secs = int(size / 16000)
        return {
            "id": ep_id,
            "title": f"Proverbs {', '.join(str(c) for c in chapters)}",
            "subtitle": theme["name"],
            "description": f"Daily Proverbs — {theme['desc']}. Chapters: {', '.join(str(c) for c in chapters)}.",
            "file": audio_file,
            "duration": f"{dur_secs // 60}:{dur_secs % 60:02d}",
            "durationSecs": dur_secs,
            "fileSize": size,
            "date": date_str,
            "series": "Daily Proverbs",
            "section": "proverb",
            "tags": ["proverbs", "daily", theme["name"].lower()],
        }

    script = build_script(chapters, theme)
    if not script or len(script) < 50:
        print(f"  SKIP ep {ep_id} — no text")
        return None

    print(f"  Generating ep {ep_id}: Proverbs {chapters} ({len(script)} chars)...")
    try:
        comm = edge_tts.Communicate(script, VOICE, rate=RATE, pitch=PITCH)
        await comm.save(audio_path)
        size = os.path.getsize(audio_path)
        dur_secs = int(size / 16000)
        print(f"  DONE: {audio_file} ({size/1024:.0f}KB)")

        return {
            "id": ep_id,
            "title": f"Proverbs {', '.join(str(c) for c in chapters)}",
            "subtitle": theme["name"],
            "description": f"Daily Proverbs — {theme['desc']}. Chapters: {', '.join(str(c) for c in chapters)}.",
            "file": audio_file,
            "duration": f"{dur_secs // 60}:{dur_secs % 60:02d}",
            "durationSecs": dur_secs,
            "fileSize": size,
            "date": date_str,
            "series": "Daily Proverbs",
            "section": "proverb",
            "tags": ["proverbs", "daily", theme["name"].lower()],
        }
    except Exception as e:
        print(f"  ERROR: {e}")
        return None


async def main():
    # Generate for specified months (default: April + May + June 2026)
    year = 2026
    months = [4, 5, 6]  # April, May, June
    if len(sys.argv) > 1:
        months = [int(m) for m in sys.argv[1].split(",")]

    # Load existing episodes
    with open(EPISODES_FILE) as f:
        episodes = json.loads(f.read())

    # Remove old proverb episodes for these months
    episodes = [e for e in episodes if e.get("section") != "proverb" or
                not any(e.get("date", "").startswith(f"{year}-{m:02d}") for m in months)]

    ep_id_base = 7001
    new_episodes = []

    for month in months:
        theme = THEMES[month - 1]  # 0-indexed
        days_in_month = calendar.monthrange(year, month)[1]
        month_name = calendar.month_name[month]

        print(f"\n=== {month_name} {year}: {theme['name']} ({days_in_month} days) ===")

        for day in range(1, days_in_month + 1):
            date_str = f"{year}-{month:02d}-{day:02d}"

            # Map day to chapter(s)
            if day == days_in_month and days_in_month < 31:
                chapters = list(range(day, 32))  # e.g., day 30 → [30, 31]
            else:
                chapters = [day]

            ep_id = ep_id_base + (month - 4) * 31 + (day - 1)
            ep = await generate_episode(ep_id, date_str, chapters, theme, f"{month_name} {year}")
            if ep:
                new_episodes.append(ep)

            await asyncio.sleep(0.2)

    # Add new episodes to list
    episodes.extend(new_episodes)

    # Sort by id
    episodes.sort(key=lambda e: e["id"])

    # Write back
    with open(EPISODES_FILE, "w") as f:
        json.dump(episodes, f, indent=2)

    print(f"\n=== Done! Added {len(new_episodes)} proverb episodes ===")


if __name__ == "__main__":
    asyncio.run(main())
