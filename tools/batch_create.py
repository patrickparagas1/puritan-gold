#!/usr/bin/env python3
"""Batch create all podcast episodes from scripts directory."""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.expanduser("~/Library/Python/3.9/lib/python/site-packages"))

from create_episode import create_episode

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "scripts")
EPISODES_FILE = os.path.join(PROJECT_ROOT, "episodes.json")

# Episode metadata for all 28 episodes (4 weeks)
EPISODES = [
    # Week 1: Wisdom Begins — Proverbs 1-4 & Spurgeon
    {"num": 1, "title": "The Beginning of Wisdom", "subtitle": "Proverbs 1 — The Fear of the Lord", "series": "Proverbs", "tags": ["proverbs", "wisdom", "fear-of-god"]},
    {"num": 2, "title": "The Minister's Self-Watch", "subtitle": "From Spurgeon's Lectures to My Students", "series": "Spurgeon", "tags": ["spurgeon", "ministry", "self-examination"]},
    {"num": 3, "title": "The Treasure of Wisdom", "subtitle": "Proverbs 2 — Seeking Like Silver", "series": "Proverbs", "tags": ["proverbs", "wisdom", "scripture-study"]},
    {"num": 4, "title": "The Soul Winner's Prayer Life", "subtitle": "From Spurgeon's The Soul Winner", "series": "Spurgeon", "tags": ["spurgeon", "prayer", "evangelism"]},
    {"num": 5, "title": "Trust in the Lord", "subtitle": "Proverbs 3 — Lean Not on Your Own Understanding", "series": "Proverbs", "tags": ["proverbs", "trust", "guidance"]},
    {"num": 6, "title": "Guard Your Heart", "subtitle": "Proverbs 4 — Above All Else", "series": "Proverbs", "tags": ["proverbs", "heart", "practical"]},
    {"num": 7, "title": "The Puritan Practice of Daily Prayer", "subtitle": "A Devotional on the Discipline of Prayer", "series": "Devotional", "tags": ["prayer", "puritans", "devotional"]},

    # Week 2: Walking in Righteousness — Proverbs 5-8 & A.W. Pink
    {"num": 8, "title": "Flee from Temptation", "subtitle": "Proverbs 5 — Guarding Against Sin's Lure", "series": "Proverbs", "tags": ["proverbs", "temptation", "purity"]},
    {"num": 9, "title": "The Sovereignty of God", "subtitle": "From A.W. Pink's The Attributes of God", "series": "A.W. Pink", "tags": ["pink", "sovereignty", "doctrine"]},
    {"num": 10, "title": "Warnings Against Folly", "subtitle": "Proverbs 6 — The Sluggard and the Ant", "series": "Proverbs", "tags": ["proverbs", "folly", "diligence"]},
    {"num": 11, "title": "The Holiness of God", "subtitle": "From A.W. Pink's The Attributes of God", "series": "A.W. Pink", "tags": ["pink", "holiness", "doctrine"]},
    {"num": 12, "title": "The Danger of Sin's Allure", "subtitle": "Proverbs 7 — The Seduction of Folly", "series": "Proverbs", "tags": ["proverbs", "sin", "warning"]},
    {"num": 13, "title": "Wisdom's Call", "subtitle": "Proverbs 8 — Wisdom in Creation", "series": "Proverbs", "tags": ["proverbs", "wisdom", "creation"]},
    {"num": 14, "title": "Scripture Meditation: The Lost Discipline", "subtitle": "A Devotional on Prayerful Reading", "series": "Devotional", "tags": ["meditation", "scripture", "devotional"]},

    # Week 3: The Fear of the Lord — Proverbs 9-12 & Puritan Doctrine
    {"num": 15, "title": "The Fear of the Lord is the Beginning of Wisdom", "subtitle": "Proverbs 9 — Two Feasts, Two Ways", "series": "Proverbs", "tags": ["proverbs", "fear-of-god", "wisdom"]},
    {"num": 16, "title": "The Mortification of Sin", "subtitle": "From John Owen", "series": "Puritan Doctrine", "tags": ["owen", "sin", "sanctification"]},
    {"num": 17, "title": "The Righteous and the Wicked", "subtitle": "Proverbs 10 — Contrasts in Character", "series": "Proverbs", "tags": ["proverbs", "righteousness", "character"]},
    {"num": 18, "title": "The Art of Divine Contentment", "subtitle": "From Thomas Watson", "series": "Puritan Doctrine", "tags": ["watson", "contentment", "grace"]},
    {"num": 19, "title": "Integrity and Uprightness", "subtitle": "Proverbs 11 — The Value of Righteousness", "series": "Proverbs", "tags": ["proverbs", "integrity", "uprightness"]},
    {"num": 20, "title": "The Way of the Righteous", "subtitle": "Proverbs 12 — Character in Daily Life", "series": "Proverbs", "tags": ["proverbs", "righteousness", "daily-life"]},
    {"num": 21, "title": "Walking with God: The Puritan Daily Life", "subtitle": "A Devotional on Structuring Your Day", "series": "Devotional", "tags": ["puritans", "daily-life", "devotional"]},

    # Week 4: Living Wisely — Proverbs 13-16 & Practical Theology
    {"num": 22, "title": "The Fruit of Righteousness", "subtitle": "Proverbs 13 — Walking with the Wise", "series": "Proverbs", "tags": ["proverbs", "righteousness", "wisdom"]},
    {"num": 23, "title": "Spurgeon on the Sovereignty of Grace", "subtitle": "The Doctrines of Grace in Spurgeon's Preaching", "series": "Spurgeon", "tags": ["spurgeon", "grace", "election"]},
    {"num": 24, "title": "Wisdom Builds Her House", "subtitle": "Proverbs 14 — The Way That Seems Right", "series": "Proverbs", "tags": ["proverbs", "wisdom", "discernment"]},
    {"num": 25, "title": "The Doctrine of Election", "subtitle": "From A.W. Pink's Studies in the Scriptures", "series": "A.W. Pink", "tags": ["pink", "election", "doctrine"]},
    {"num": 26, "title": "A Gentle Answer Turns Away Wrath", "subtitle": "Proverbs 15 — The Power of the Tongue", "series": "Proverbs", "tags": ["proverbs", "speech", "relationships"]},
    {"num": 27, "title": "The Lord Directs Our Steps", "subtitle": "Proverbs 16 — Surrendering Our Plans", "series": "Proverbs", "tags": ["proverbs", "sovereignty", "trust"]},
    {"num": 28, "title": "Justification by Faith Alone", "subtitle": "The Doctrine That Changes Everything", "series": "Devotional", "tags": ["justification", "faith", "doctrine"]},
]


def main():
    # Check which scripts exist
    available = []
    missing = []
    for ep in EPISODES:
        script_path = os.path.join(SCRIPTS_DIR, f"ep{ep['num']:03d}.txt")
        if os.path.exists(script_path):
            available.append((ep, script_path))
        else:
            missing.append(ep['num'])

    if missing:
        print(f"Warning: Missing scripts for episodes: {missing}")

    print(f"Found {len(available)} scripts to process.\n")

    for i, (ep, script_path) in enumerate(available):
        print(f"\n{'='*60}")
        print(f"Episode {ep['num']}/{len(EPISODES)}: {ep['title']}")
        print(f"{'='*60}")

        audio_path = os.path.join(PROJECT_ROOT, "audio", f"ep{ep['num']:03d}.mp3")
        if os.path.exists(audio_path):
            print(f"  Skipping (already exists)")
            continue

        try:
            create_episode(
                script_path=script_path,
                title=ep['title'],
                subtitle=ep.get('subtitle', ''),
                description=ep.get('subtitle', ep['title']),
                series=ep.get('series', ''),
                tags=ep.get('tags', []),
                episode_num=ep['num']
            )
        except Exception as e:
            print(f"  ERROR: {e}")
            continue

    print(f"\n{'='*60}")
    print("Batch creation complete!")
    print(f"{'='*60}")

    # Show summary
    if os.path.exists(EPISODES_FILE):
        with open(EPISODES_FILE, 'r') as f:
            episodes = json.load(f)
        print(f"\nTotal episodes in feed: {len(episodes)}")
        total_duration = sum(e.get('durationSecs', 0) for e in episodes)
        print(f"Total duration: {total_duration // 3600}h {(total_duration % 3600) // 60}m")


if __name__ == "__main__":
    main()
