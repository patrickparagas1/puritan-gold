#!/usr/bin/env python3
"""
Generate audio for ALL 1,189 Bible chapters using edge-tts (en-GB-RyanNeural).
Skips chapters that already have an MP3 file.
"""

import asyncio, os, json, urllib.request, urllib.parse, sys

VOICE = "en-GB-RyanNeural"
RATE = "-8%"
PITCH = "-12Hz"
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "audio", "bible")

# All 66 Protestant Bible books with chapter counts
# Book name must match bible-api.com format
BOOKS = [
    # OT
    ("genesis", 50), ("exodus", 40), ("leviticus", 27), ("numbers", 36), ("deuteronomy", 34),
    ("joshua", 24), ("judges", 21), ("ruth", 4),
    ("1 samuel", 31), ("2 samuel", 24), ("1 kings", 22), ("2 kings", 25),
    ("1 chronicles", 29), ("2 chronicles", 36), ("ezra", 10), ("nehemiah", 13), ("esther", 10),
    ("job", 42), ("psalms", 150), ("proverbs", 31), ("ecclesiastes", 12), ("song of solomon", 8),
    ("isaiah", 66), ("jeremiah", 52), ("lamentations", 5), ("ezekiel", 48), ("daniel", 12),
    ("hosea", 14), ("joel", 3), ("amos", 9), ("obadiah", 1), ("jonah", 4),
    ("micah", 7), ("nahum", 3), ("habakkuk", 3), ("zephaniah", 3), ("haggai", 2),
    ("zechariah", 14), ("malachi", 4),
    # NT
    ("matthew", 28), ("mark", 16), ("luke", 24), ("john", 21), ("acts", 28),
    ("romans", 16), ("1 corinthians", 16), ("2 corinthians", 13), ("galatians", 6),
    ("ephesians", 6), ("philippians", 4), ("colossians", 4),
    ("1 thessalonians", 5), ("2 thessalonians", 3), ("1 timothy", 6), ("2 timothy", 4),
    ("titus", 3), ("philemon", 1), ("hebrews", 13), ("james", 5),
    ("1 peter", 5), ("2 peter", 3), ("1 john", 5), ("2 john", 1), ("3 john", 1),
    ("jude", 1), ("revelation", 22),
]


def book_id(name):
    return name.replace(" ", "").lower()


def fetch_chapter_text(book, chapter):
    url = f"https://bible-api.com/{urllib.parse.quote(book + ' ' + str(chapter))}?translation=kjv"
    try:
        with urllib.request.urlopen(url, timeout=20) as resp:
            data = json.loads(resp.read())
            if "verses" in data:
                return " ".join(v["text"].replace("\n", " ").strip() for v in data["verses"])
            return data.get("text", "")
    except Exception as e:
        print(f"    FETCH ERROR {book} {chapter}: {e}")
        return None


async def generate_audio(book, chapter):
    import edge_tts

    bid = book_id(book)
    out_file = os.path.join(OUTPUT_DIR, f"{bid}_{chapter}.mp3")

    if os.path.exists(out_file) and os.path.getsize(out_file) > 1000:
        return "skip"

    text = fetch_chapter_text(book, chapter)
    if not text:
        return "no_text"

    intro = f"{book.title()}, chapter {chapter}."
    full_text = f"{intro} {text}"

    try:
        communicate = edge_tts.Communicate(full_text, VOICE, rate=RATE, pitch=PITCH)
        await communicate.save(out_file)
        size_kb = os.path.getsize(out_file) / 1024
        return f"ok ({size_kb:.0f}KB)"
    except Exception as e:
        print(f"    TTS ERROR {book} {chapter}: {e}")
        return "tts_error"


async def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Allow starting from a specific book
    start_book = sys.argv[1] if len(sys.argv) > 1 else None
    started = start_book is None

    total = sum(ch for _, ch in BOOKS)
    done = 0
    generated = 0
    skipped = 0
    errors = 0

    print(f"Generating audio for {total} chapters across {len(BOOKS)} books")
    print(f"Voice: {VOICE}, Rate: {RATE}, Pitch: {PITCH}")
    print(f"Output: {OUTPUT_DIR}")
    print("=" * 60)

    for book_name, chapters in BOOKS:
        if not started:
            if book_id(book_name) == book_id(start_book):
                started = True
            else:
                done += chapters
                continue

        print(f"\n[{book_name.title()}] ({chapters} chapters)")

        for ch in range(1, chapters + 1):
            done += 1
            pct = (done / total) * 100
            sys.stdout.write(f"  Ch {ch}/{chapters} ({pct:.1f}% overall) ... ")
            sys.stdout.flush()

            result = await generate_audio(book_name, ch)

            if result == "skip":
                skipped += 1
                print("SKIP (exists)")
            elif result.startswith("ok"):
                generated += 1
                print(f"DONE {result}")
            else:
                errors += 1
                print(f"FAIL ({result})")

            # Small delay to avoid rate limiting
            if result.startswith("ok"):
                await asyncio.sleep(0.3)

    print("\n" + "=" * 60)
    print(f"COMPLETE: {generated} generated, {skipped} skipped, {errors} errors")
    print(f"Total files: {len(os.listdir(OUTPUT_DIR))}")


if __name__ == "__main__":
    asyncio.run(main())
