#!/usr/bin/env python3
"""
Generate Bible chapter audio using edge-tts (en-GB-RyanNeural).
Same deep male voice as the Puritan Gold podcast episodes.

Usage:
  python3 tools/gen_bible_audio.py genesis 1
  python3 tools/gen_bible_audio.py psalms 23
  python3 tools/gen_bible_audio.py --batch   # generates all key chapters
"""

import asyncio, sys, os, json, urllib.request

VOICE = "en-GB-RyanNeural"
RATE = "-8%"
PITCH = "-12Hz"
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "audio", "bible")

# Key chapters to pre-generate
KEY_CHAPTERS = [
    ("genesis", 1), ("genesis", 2), ("genesis", 3),
    ("psalms", 23), ("psalms", 1), ("psalms", 91), ("psalms", 119),
    ("proverbs", 1), ("proverbs", 2), ("proverbs", 3),
    ("isaiah", 53), ("isaiah", 40),
    ("matthew", 5), ("matthew", 6), ("matthew", 7),
    ("john", 1), ("john", 3), ("john", 14), ("john", 15),
    ("romans", 1), ("romans", 8), ("romans", 12),
    ("1 corinthians", 13),
    ("ephesians", 6),
    ("hebrews", 11),
    ("revelation", 21), ("revelation", 22),
]


def fetch_chapter_text(book, chapter):
    """Fetch KJV chapter text from bible-api.com"""
    url = f"https://bible-api.com/{urllib.parse.quote(book + ' ' + str(chapter))}?translation=kjv"
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read())
            if "verses" in data:
                lines = []
                for v in data["verses"]:
                    text = v["text"].replace("\n", " ").strip()
                    lines.append(text)
                return " ".join(lines)
            return data.get("text", "")
    except Exception as e:
        print(f"  ERROR fetching {book} {chapter}: {e}")
        return None


async def generate_audio(book, chapter):
    """Generate MP3 for a Bible chapter using edge-tts"""
    import edge_tts

    # Normalize book name for filename
    book_id = book.replace(" ", "").lower()
    out_file = os.path.join(OUTPUT_DIR, f"{book_id}_{chapter}.mp3")

    if os.path.exists(out_file):
        print(f"  SKIP {book} {chapter} — already exists")
        return out_file

    print(f"  Fetching text for {book} {chapter}...")
    text = fetch_chapter_text(book, chapter)
    if not text:
        print(f"  SKIP {book} {chapter} — no text")
        return None

    # Add a brief intro
    intro = f"{book.title()}, chapter {chapter}."
    full_text = f"{intro} {text}"

    print(f"  Generating audio ({len(full_text)} chars)...")
    communicate = edge_tts.Communicate(
        full_text,
        VOICE,
        rate=RATE,
        pitch=PITCH,
    )
    await communicate.save(out_file)
    size_mb = os.path.getsize(out_file) / (1024 * 1024)
    print(f"  DONE: {out_file} ({size_mb:.1f} MB)")
    return out_file


async def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if len(sys.argv) >= 3 and sys.argv[1] != "--batch":
        book = sys.argv[1]
        chapter = int(sys.argv[2])
        await generate_audio(book, chapter)
    elif "--batch" in sys.argv:
        print(f"Generating {len(KEY_CHAPTERS)} key chapters...")
        for book, chapter in KEY_CHAPTERS:
            await generate_audio(book, chapter)
        print("\nAll done!")
    else:
        print("Usage: python3 gen_bible_audio.py <book> <chapter>")
        print("       python3 gen_bible_audio.py --batch")


if __name__ == "__main__":
    import urllib.parse
    asyncio.run(main())
