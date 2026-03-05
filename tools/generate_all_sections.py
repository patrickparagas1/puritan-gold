#!/usr/bin/env python3
"""
Generate ALL content for Puritan Gold podcast app:
  - Family Devotional (IDs 101-131)
  - School / Puritan Academy (IDs 201-220)
  - Together / Couples (IDs 301-331)

Generates text scripts, audio via edge-tts + ffmpeg, and updates episodes.json.
Run: python3 tools/generate_all_sections.py
"""

import asyncio
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.expanduser("~/Library/Python/3.9/lib/python/site-packages"))

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(PROJECT_ROOT, "audio")
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "scripts")
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")
AMBIENT_FILE = os.path.join(ASSETS_DIR, "ambient_crackling.wav")
EPISODES_FILE = os.path.join(PROJECT_ROOT, "episodes.json")

# ---------------------------------------------------------------------------
# Audio pipeline helpers (mirrors create_episode.py)
# ---------------------------------------------------------------------------
from tts_engine import text_to_speech


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


def generate_audio(script_text, output_path):
    """Generate TTS audio, mix with ambient crackling, produce final MP3."""
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        speech_path = tmp.name

    try:
        text_to_speech(script_text, speech_path)

        if os.path.exists(AMBIENT_FILE):
            _, duration_secs = get_mp3_duration(speech_path)
            subprocess.run([
                "ffmpeg", "-y",
                "-i", speech_path,
                "-stream_loop", "-1", "-i", AMBIENT_FILE,
                "-filter_complex",
                f"[1:a]atrim=0:{duration_secs},volume=0.12[amb];"
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


# ---------------------------------------------------------------------------
# episodes.json helpers
# ---------------------------------------------------------------------------
def load_episodes():
    if os.path.exists(EPISODES_FILE):
        with open(EPISODES_FILE, 'r') as f:
            return json.load(f)
    return []


def save_episodes(episodes):
    episodes.sort(key=lambda e: e["id"])
    with open(EPISODES_FILE, 'w') as f:
        json.dump(episodes, f, indent=2)


# ===================================================================
# FAMILY DEVOTIONAL CONTENT  (IDs 101-131, Proverbs 1-31)
# ===================================================================
FAMILY_EPISODES = [
    # --- Day 1: Proverbs 1 ---
    {
        "day": 1, "id": 101,
        "title": "Wisdom for Our Family",
        "subtitle": "Proverbs 1 -- Family Devotional",
        "description": "A family devotional exploring what it means to fear the Lord together, based on Proverbs 1.",
        "memoryVerse": "The fear of the LORD is the beginning of knowledge: but fools despise wisdom and instruction. -- Proverbs 1:7",
        "discussionQuestions": [
            "What does it mean to 'fear' the Lord? Is it being scared, or something deeper?",
            "Why does Solomon say wisdom starts with respecting God?",
            "How can our family show reverence for God this week?"
        ],
    },
    # --- Day 2: Proverbs 2 ---
    {
        "day": 2, "id": 102,
        "title": "Seeking Treasure Together",
        "subtitle": "Proverbs 2 -- Family Devotional",
        "description": "Seeking God's wisdom like hidden treasure. When we search with all our hearts, we find something more valuable than gold.",
        "memoryVerse": "If thou seekest her as silver, and searchest for her as for hid treasures; Then shalt thou understand the fear of the LORD. -- Proverbs 2:4-5",
        "discussionQuestions": [
            "If you found a treasure map, how hard would you search for the treasure?",
            "How can we search for God's wisdom every day?",
            "What makes God's wisdom more valuable than gold or silver?"
        ],
    },
    # --- Day 3: Proverbs 3 ---
    {
        "day": 3, "id": 103,
        "title": "Trust in the Lord with All Your Heart",
        "subtitle": "Proverbs 3 -- Family Devotional",
        "description": "Learning to trust God with everything -- our worries, our plans, and our future as a family.",
        "memoryVerse": "Trust in the LORD with all thine heart; and lean not unto thine own understanding. In all thy ways acknowledge him, and he shall direct thy paths. -- Proverbs 3:5-6",
        "discussionQuestions": [
            "What does it mean to trust God with ALL your heart?",
            "Is there something our family can give to God in prayer right now?",
            "How does God direct our paths when we trust Him?"
        ],
    },
    # --- Day 4: Proverbs 4 ---
    {
        "day": 4, "id": 104,
        "title": "Guarding Our Hearts",
        "subtitle": "Proverbs 4 -- Family Devotional",
        "description": "Guarding what goes into our hearts and minds. What we watch, listen to, and think about shapes who we become.",
        "memoryVerse": "Keep thy heart with all diligence; for out of it are the issues of life. -- Proverbs 4:23",
        "discussionQuestions": [
            "What kinds of things go into our hearts through what we watch and listen to?",
            "Why does the Bible say our heart is so important?",
            "What is one thing we can change this week to better guard our hearts?"
        ],
    },
    # --- Day 5: Proverbs 5 ---
    {
        "day": 5, "id": 105,
        "title": "Walking the Right Path",
        "subtitle": "Proverbs 5 -- Family Devotional",
        "description": "Proverbs 5 teaches us to stay on the right path and avoid things that pull us away from God.",
        "memoryVerse": "Ponder the path of thy feet, and let all thy ways be established. -- Proverbs 4:26",
        "discussionQuestions": [
            "What does it mean to 'ponder the path of thy feet'?",
            "How can we help each other stay on the right path?",
            "What are some wrong paths that children and families need to watch for?"
        ],
    },
    # --- Day 6: Proverbs 6 ---
    {
        "day": 6, "id": 106,
        "title": "The Little Ant and the Big Lesson",
        "subtitle": "Proverbs 6 -- Family Devotional",
        "description": "The tiny ant teaches us a big lesson about hard work and planning ahead, from Proverbs 6.",
        "memoryVerse": "Go to the ant, thou sluggard; consider her ways, and be wise. -- Proverbs 6:6",
        "discussionQuestions": [
            "What can we learn from watching ants work together?",
            "Why does God want us to be diligent and not lazy?",
            "What chores or tasks can we do with a cheerful, hardworking attitude this week?"
        ],
    },
    # --- Day 7: Proverbs 7 ---
    {
        "day": 7, "id": 107,
        "title": "The Shield of Wisdom",
        "subtitle": "Proverbs 7 -- Family Devotional",
        "description": "Wisdom is like a shield that protects us from making foolish choices. Proverbs 7 teaches us to hold on to God's Word.",
        "memoryVerse": "Say unto wisdom, Thou art my sister; and call understanding thy kinswoman. -- Proverbs 7:4",
        "discussionQuestions": [
            "How is wisdom like a shield or a good friend?",
            "Why is it important to know God's Word before temptation comes?",
            "How can memorizing Scripture help protect our family?"
        ],
    },
    # --- Day 8: Proverbs 8 ---
    {
        "day": 8, "id": 108,
        "title": "Wisdom Was There at the Beginning",
        "subtitle": "Proverbs 8 -- Family Devotional",
        "description": "Proverbs 8 reveals that wisdom was with God when He created the world. God's wisdom is woven into everything He made.",
        "memoryVerse": "The LORD possessed me in the beginning of his way, before his works of old. -- Proverbs 8:22",
        "discussionQuestions": [
            "What does it mean that wisdom was with God when He made the world?",
            "Where can we see God's wisdom in creation around us?",
            "How does knowing God created everything help us trust Him more?"
        ],
    },
    # --- Day 9: Proverbs 9 ---
    {
        "day": 9, "id": 109,
        "title": "Two Invitations",
        "subtitle": "Proverbs 9 -- Family Devotional",
        "description": "Proverbs 9 shows two feasts -- Wisdom's feast and Folly's feast. Every day we choose which invitation to accept.",
        "memoryVerse": "The fear of the LORD is the beginning of wisdom: and the knowledge of the holy is understanding. -- Proverbs 9:10",
        "discussionQuestions": [
            "What is the difference between Wisdom's invitation and Folly's invitation?",
            "How do we choose the wise path every day?",
            "What does the 'knowledge of the holy' mean for our family?"
        ],
    },
    # --- Day 10: Proverbs 10 ---
    {
        "day": 10, "id": 110,
        "title": "Words That Build Up",
        "subtitle": "Proverbs 10 -- Family Devotional",
        "description": "Proverbs 10 teaches the power of our words -- to build up or tear down. A family that speaks kindly honors the Lord.",
        "memoryVerse": "The mouth of a righteous man is a well of life. -- Proverbs 10:11",
        "discussionQuestions": [
            "How can our words be like a 'well of life' for others?",
            "When have kind words made you feel better?",
            "What is one way we can use our words to encourage someone today?"
        ],
    },
    # --- Day 11: Proverbs 11 ---
    {
        "day": 11, "id": 111,
        "title": "Honesty and Kindness",
        "subtitle": "Proverbs 11 -- Family Devotional",
        "description": "Proverbs 11 teaches about the value of honesty and the blessing of generosity. A faithful family walks in integrity.",
        "memoryVerse": "A false balance is abomination to the LORD: but a just weight is his delight. -- Proverbs 11:1",
        "discussionQuestions": [
            "What does it mean to be honest in big and small things?",
            "Why does God care about fairness?",
            "How can our family practice generosity this week?"
        ],
    },
    # --- Day 12: Proverbs 12 ---
    {
        "day": 12, "id": 112,
        "title": "Loving Correction",
        "subtitle": "Proverbs 12 -- Family Devotional",
        "description": "Proverbs 12 teaches that wise children love correction because it helps them grow. Discipline is a sign of love.",
        "memoryVerse": "Whoso loveth instruction loveth knowledge: but he that hateth reproof is brutish. -- Proverbs 12:1",
        "discussionQuestions": [
            "Why is it hard to hear correction, even when it helps us?",
            "How is correction a sign that someone loves you?",
            "How can we receive correction with a grateful heart?"
        ],
    },
    # --- Day 13: Proverbs 13 ---
    {
        "day": 13, "id": 113,
        "title": "Walking with the Wise",
        "subtitle": "Proverbs 13 -- Family Devotional",
        "description": "Proverbs 13 teaches that the friends we choose shape who we become. Walking with wise people makes us wise.",
        "memoryVerse": "He that walketh with wise men shall be wise: but a companion of fools shall be destroyed. -- Proverbs 13:20",
        "discussionQuestions": [
            "Who are the wise people in your life?",
            "How do your friends influence who you are becoming?",
            "What makes someone a wise friend to walk with?"
        ],
    },
    # --- Day 14: Proverbs 14 ---
    {
        "day": 14, "id": 114,
        "title": "The Way That Seems Right",
        "subtitle": "Proverbs 14 -- Family Devotional",
        "description": "Proverbs 14 warns that some paths look good but lead to destruction. Only God's way is truly safe.",
        "memoryVerse": "There is a way which seemeth right unto a man, but the end thereof are the ways of death. -- Proverbs 14:12",
        "discussionQuestions": [
            "Why do some wrong choices look right at first?",
            "How can we check our decisions against God's Word?",
            "Can you think of a time the easy choice was not the right choice?"
        ],
    },
    # --- Day 15: Proverbs 15 ---
    {
        "day": 15, "id": 115,
        "title": "A Gentle Answer",
        "subtitle": "Proverbs 15 -- Family Devotional",
        "description": "Proverbs 15 teaches the power of a gentle answer to calm anger and bring peace to our home.",
        "memoryVerse": "A soft answer turneth away wrath: but grievous words stir up anger. -- Proverbs 15:1",
        "discussionQuestions": [
            "Why is it hard to give a gentle answer when we are upset?",
            "What happens when we respond with harsh words instead?",
            "How can our family practice gentle answers this week?"
        ],
    },
    # --- Day 16: Proverbs 16 ---
    {
        "day": 16, "id": 116,
        "title": "God Directs Our Steps",
        "subtitle": "Proverbs 16 -- Family Devotional",
        "description": "Proverbs 16 reminds us that we make plans, but the Lord directs our steps. We can trust His guidance.",
        "memoryVerse": "A man's heart deviseth his way: but the LORD directeth his steps. -- Proverbs 16:9",
        "discussionQuestions": [
            "What plans has our family made that God changed or directed?",
            "How does it feel to know God is guiding your steps?",
            "What can we pray about and surrender to God's direction today?"
        ],
    },
    # --- Day 17: Proverbs 17 ---
    {
        "day": 17, "id": 117,
        "title": "A Friend Who Loves at All Times",
        "subtitle": "Proverbs 17 -- Family Devotional",
        "description": "Proverbs 17 teaches about true friendship -- a friend who loves at all times and a brother born for adversity.",
        "memoryVerse": "A friend loveth at all times, and a brother is born for adversity. -- Proverbs 17:17",
        "discussionQuestions": [
            "What does it mean to love a friend at ALL times, even hard times?",
            "Who is a faithful friend in your life?",
            "How can we be a better friend to others this week?"
        ],
    },
    # --- Day 18: Proverbs 18 ---
    {
        "day": 18, "id": 118,
        "title": "Our Strong Tower",
        "subtitle": "Proverbs 18 -- Family Devotional",
        "description": "Proverbs 18 reveals that the name of the Lord is a strong tower. The righteous run into it and are safe.",
        "memoryVerse": "The name of the LORD is a strong tower: the righteous runneth into it, and is safe. -- Proverbs 18:10",
        "discussionQuestions": [
            "What does it mean that God's name is a strong tower?",
            "When you feel afraid, how can you 'run' to God?",
            "What are some names of God that remind us He is strong and safe?"
        ],
    },
    # --- Day 19: Proverbs 19 ---
    {
        "day": 19, "id": 119,
        "title": "Patience and Kindness",
        "subtitle": "Proverbs 19 -- Family Devotional",
        "description": "Proverbs 19 teaches about patience, kindness to the poor, and the wisdom of listening before speaking.",
        "memoryVerse": "The discretion of a man deferreth his anger; and it is his glory to pass over a transgression. -- Proverbs 19:11",
        "discussionQuestions": [
            "Why is it wise to be slow to get angry?",
            "How can we show kindness to someone who has less than we do?",
            "What does it mean to 'pass over a transgression' or forgive?"
        ],
    },
    # --- Day 20: Proverbs 20 ---
    {
        "day": 20, "id": 120,
        "title": "A Good Name",
        "subtitle": "Proverbs 20 -- Family Devotional",
        "description": "Proverbs 20 teaches about integrity, fairness, and the value of building a reputation that honors God.",
        "memoryVerse": "Even a child is known by his doings, whether his work be pure, and whether it be right. -- Proverbs 20:11",
        "discussionQuestions": [
            "What does it mean that even a child is known by what they do?",
            "What kind of reputation do you want to have?",
            "How can our family be known for honesty and kindness?"
        ],
    },
    # --- Day 21: Proverbs 21 ---
    {
        "day": 21, "id": 121,
        "title": "The Lord Weighs the Heart",
        "subtitle": "Proverbs 21 -- Family Devotional",
        "description": "Proverbs 21 reminds us that God sees our hearts, not just our outward actions. He values true obedience.",
        "memoryVerse": "Every way of a man is right in his own eyes: but the LORD pondereth the hearts. -- Proverbs 21:2",
        "discussionQuestions": [
            "What does it mean that God looks at our hearts?",
            "Can someone do the right thing for the wrong reason?",
            "How can we make sure our hearts are right before God?"
        ],
    },
    # --- Day 22: Proverbs 22 ---
    {
        "day": 22, "id": 122,
        "title": "Training Up a Child",
        "subtitle": "Proverbs 22 -- Family Devotional",
        "description": "Proverbs 22 contains the beloved promise about training up a child in the way they should go.",
        "memoryVerse": "Train up a child in the way he should go: and when he is old, he will not depart from it. -- Proverbs 22:6",
        "discussionQuestions": [
            "What does it mean to be trained in the way you should go?",
            "How are Mom and Dad training you to love God?",
            "What Bible truths do you want to remember when you grow up?"
        ],
    },
    # --- Day 23: Proverbs 23 ---
    {
        "day": 23, "id": 123,
        "title": "Giving God Your Heart",
        "subtitle": "Proverbs 23 -- Family Devotional",
        "description": "Proverbs 23 contains God's tender invitation: My son, give me thine heart. God wants our whole selves.",
        "memoryVerse": "My son, give me thine heart, and let thine eyes observe my ways. -- Proverbs 23:26",
        "discussionQuestions": [
            "What does it mean to give God your heart?",
            "Is there a part of your life you have not given to God yet?",
            "How can we give our hearts to God more fully as a family?"
        ],
    },
    # --- Day 24: Proverbs 24 ---
    {
        "day": 24, "id": 124,
        "title": "Getting Back Up Again",
        "subtitle": "Proverbs 24 -- Family Devotional",
        "description": "Proverbs 24 teaches that a righteous person may fall seven times but rises again. God gives us strength to persevere.",
        "memoryVerse": "For a just man falleth seven times, and riseth up again: but the wicked shall fall into mischief. -- Proverbs 24:16",
        "discussionQuestions": [
            "Why is it important to get back up when we fail or fall?",
            "How does God help us when we make mistakes?",
            "Can you think of a time you failed but tried again and it worked out?"
        ],
    },
    # --- Day 25: Proverbs 25 ---
    {
        "day": 25, "id": 125,
        "title": "Being Kind to Those Who Are Unkind",
        "subtitle": "Proverbs 25 -- Family Devotional",
        "description": "Proverbs 25 teaches us to respond to unkindness with kindness, heaping coals of fire through love.",
        "memoryVerse": "If thine enemy be hungry, give him bread to eat; and if he be thirsty, give him water to drink. -- Proverbs 25:21",
        "discussionQuestions": [
            "Why is it so hard to be kind to someone who is mean to us?",
            "How did Jesus show kindness to people who were unkind to Him?",
            "How can we show love to someone difficult this week?"
        ],
    },
    # --- Day 26: Proverbs 26 ---
    {
        "day": 26, "id": 126,
        "title": "The Wise and the Foolish",
        "subtitle": "Proverbs 26 -- Family Devotional",
        "description": "Proverbs 26 paints vivid pictures of the fool and the sluggard. Wisdom teaches us to avoid these pitfalls.",
        "memoryVerse": "Seest thou a man wise in his own conceit? there is more hope of a fool than of him. -- Proverbs 26:12",
        "discussionQuestions": [
            "What does it mean to be 'wise in your own eyes'?",
            "Why is pride more dangerous than foolishness?",
            "How can we stay humble and teachable as a family?"
        ],
    },
    # --- Day 27: Proverbs 27 ---
    {
        "day": 27, "id": 127,
        "title": "Iron Sharpens Iron",
        "subtitle": "Proverbs 27 -- Family Devotional",
        "description": "Proverbs 27 teaches that we grow sharper and stronger when we are close to people who help us grow.",
        "memoryVerse": "Iron sharpeneth iron; so a man sharpeneth the countenance of his friend. -- Proverbs 27:17",
        "discussionQuestions": [
            "How does a good friend help you become a better person?",
            "Who sharpens you like iron sharpens iron?",
            "How can our family sharpen each other spiritually?"
        ],
    },
    # --- Day 28: Proverbs 28 ---
    {
        "day": 28, "id": 128,
        "title": "Courage to Do Right",
        "subtitle": "Proverbs 28 -- Family Devotional",
        "description": "Proverbs 28 teaches that the righteous are bold as a lion. Trusting God gives us courage to stand for what is right.",
        "memoryVerse": "The wicked flee when no man pursueth: but the righteous are bold as a lion. -- Proverbs 28:1",
        "discussionQuestions": [
            "What does it mean to be 'bold as a lion'?",
            "When have you needed courage to do the right thing?",
            "How does trusting God make us braver?"
        ],
    },
    # --- Day 29: Proverbs 29 ---
    {
        "day": 29, "id": 129,
        "title": "Where There Is No Vision",
        "subtitle": "Proverbs 29 -- Family Devotional",
        "description": "Proverbs 29 teaches that without God's Word to guide us, people lose their way. His Word is our lamp.",
        "memoryVerse": "Where there is no vision, the people perish: but he that keepeth the law, happy is he. -- Proverbs 29:18",
        "discussionQuestions": [
            "What does 'vision' mean in this verse? (Hint: It means God's Word!)",
            "What happens to people who do not follow God's guidance?",
            "How can we keep God's Word as the guide for our family?"
        ],
    },
    # --- Day 30: Proverbs 30 ---
    {
        "day": 30, "id": 130,
        "title": "Every Word of God Is Pure",
        "subtitle": "Proverbs 30 -- Family Devotional",
        "description": "Proverbs 30 declares that every word of God is pure and trustworthy. We can rely on His promises completely.",
        "memoryVerse": "Every word of God is pure: he is a shield unto them that put their trust in him. -- Proverbs 30:5",
        "discussionQuestions": [
            "What does it mean that every word of God is pure?",
            "How is God like a shield for our family?",
            "What is your favorite promise from the Bible?"
        ],
    },
    # --- Day 31: Proverbs 31 ---
    {
        "day": 31, "id": 131,
        "title": "A Family That Fears the Lord",
        "subtitle": "Proverbs 31 -- Family Devotional",
        "description": "Proverbs 31 paints a picture of a family built on the fear of the Lord. A month of wisdom comes to a close with this beautiful portrait.",
        "memoryVerse": "Favour is deceitful, and beauty is vain: but a woman that feareth the LORD, she shall be praised. -- Proverbs 31:30",
        "discussionQuestions": [
            "What qualities does Proverbs 31 celebrate most?",
            "Why is fearing the Lord more important than outward beauty?",
            "What have you learned this month about wisdom and the fear of God?"
        ],
    },
]


# ===================================================================
# SCHOOL / PURITAN ACADEMY CONTENT  (IDs 201-220, 4 units x 5 lessons)
# ===================================================================
SCHOOL_EPISODES = [
    # ---- UNIT 1: The Fear of God (Lessons 1-5) ----
    {
        "lesson": 1, "id": 201,
        "title": "What Is the Fear of God?",
        "subtitle": "Unit 1, Lesson 1 -- Introduction to Reverential Awe",
        "description": "An introduction to the fear of God as reverential awe, based on Proverbs 1:7 with insights from Thomas Watson.",
        "unit": "Unit 1: The Fear of God",
        "reviewQuestions": [
            "What does Proverbs 1:7 say is the beginning of knowledge?",
            "What is the difference between being afraid of God and revering God?",
            "How did Thomas Watson describe the fear of God in his writings?",
            "Name three attributes of God that should fill us with awe."
        ],
        "activity": "Write a paragraph describing what the fear of God means in your own words. Then find three Scripture passages that speak about fearing the Lord and copy them into a journal.",
    },
    {
        "lesson": 2, "id": 202,
        "title": "The Puritans and the Fear of God",
        "subtitle": "Unit 1, Lesson 2 -- How the Puritans Lived in Holy Awe",
        "description": "How Puritan families like the Baxters and the Watsons ordered their entire lives around the fear of God.",
        "unit": "Unit 1: The Fear of God",
        "reviewQuestions": [
            "How did Puritan families practice the fear of God daily?",
            "What role did family worship play in the Puritan home?",
            "According to Richard Baxter, why was daily self-examination important?",
            "What can modern families learn from the Puritans about living in holy awe?"
        ],
        "activity": "Create a 'Puritan Daily Schedule' for your own family based on what you learned. Include morning devotions, Scripture reading, evening prayers, and self-examination.",
    },
    {
        "lesson": 3, "id": 203,
        "title": "Wisdom vs. Foolishness in Proverbs",
        "subtitle": "Unit 1, Lesson 3 -- The Two Paths",
        "description": "Proverbs presents two paths: wisdom and foolishness. Learn the contrast and why the fear of God makes the difference.",
        "unit": "Unit 1: The Fear of God",
        "reviewQuestions": [
            "What are the two paths described in Proverbs?",
            "Give three examples of wise choices and three examples of foolish choices from Proverbs.",
            "How does Proverbs 9:10 connect the fear of God to wisdom?",
            "Why does Solomon say fools despise wisdom and instruction?"
        ],
        "activity": "Draw a forked path. On one side, write characteristics and outcomes of wisdom from Proverbs 1-9. On the other side, write characteristics and outcomes of foolishness. Illustrate each path.",
    },
    {
        "lesson": 4, "id": 204,
        "title": "John Bunyan and the Pilgrim's Fear",
        "subtitle": "Unit 1, Lesson 4 -- Lessons from The Pilgrim's Progress",
        "description": "How John Bunyan portrayed the fear of God in The Pilgrim's Progress, and what his life teaches us about holy reverence.",
        "unit": "Unit 1: The Fear of God",
        "reviewQuestions": [
            "Who was John Bunyan and why was he put in prison?",
            "How does Christian's journey in The Pilgrim's Progress illustrate the fear of God?",
            "What temptations did Christian face, and how did the fear of God help him?",
            "What can we learn from Bunyan about courage and reverence?"
        ],
        "activity": "Read an excerpt from The Pilgrim's Progress describing Christian at the cross. Write a summary of the scene and explain how it shows the fear of God at work in Christian's heart.",
    },
    {
        "lesson": 5, "id": 205,
        "title": "The Westminster Catechism on the Fear of God",
        "subtitle": "Unit 1, Lesson 5 -- The Chief End of Man",
        "description": "The Westminster Shorter Catechism Q1: What is the chief end of man? To glorify God and enjoy Him forever. How this connects to holy fear.",
        "unit": "Unit 1: The Fear of God",
        "reviewQuestions": [
            "What is the chief end of man according to the Westminster Shorter Catechism?",
            "What does it mean to glorify God?",
            "How does enjoying God connect to fearing Him?",
            "Why did the Puritans consider the catechism so important for children?"
        ],
        "activity": "Memorize Westminster Shorter Catechism Q1 and its answer. Write a one-page essay explaining what it means to glorify God and enjoy Him forever in your daily life.",
    },
    # ---- UNIT 2: The Christian Character (Lessons 6-10) ----
    {
        "lesson": 6, "id": 206,
        "title": "The Heart of the Matter",
        "subtitle": "Unit 2, Lesson 6 -- Proverbs on the Inner Life",
        "description": "Proverbs 4:23 and the Puritan emphasis on the heart. Thomas Watson on guarding the inner life as the spring of all outward action.",
        "unit": "Unit 2: The Christian Character",
        "reviewQuestions": [
            "Why does Proverbs 4:23 say to guard the heart above all else?",
            "What did Thomas Watson teach about the connection between the heart and our actions?",
            "What are some ways we can examine and guard our hearts?",
            "How does the Holy Spirit help us in this work?"
        ],
        "activity": "Keep a heart journal for three days. Each evening, write down the thoughts, feelings, and desires that filled your heart that day. Pray over what you discover.",
    },
    {
        "lesson": 7, "id": 207,
        "title": "The Tongue and Its Power",
        "subtitle": "Unit 2, Lesson 7 -- What Proverbs Teaches About Speech",
        "description": "A survey of Proverbs on the power of the tongue, with Jeremiah Burroughs on speech as a reflection of character.",
        "unit": "Unit 2: The Christian Character",
        "reviewQuestions": [
            "List four proverbs about the power of the tongue.",
            "According to Jeremiah Burroughs, how does our speech reveal our character?",
            "What does Proverbs 15:1 teach about gentle words?",
            "How can we practically tame our tongues according to Scripture?"
        ],
        "activity": "For one full day, pay careful attention to everything you say. At the end of the day, write down instances where your words were helpful and instances where they were not. Pray for grace to speak wisely.",
    },
    {
        "lesson": 8, "id": 208,
        "title": "Diligence and the Sluggard",
        "subtitle": "Unit 2, Lesson 8 -- The Puritan Work Ethic",
        "description": "Proverbs on diligence and laziness, with Richard Baxter's teaching on redeeming the time and working heartily for the Lord.",
        "unit": "Unit 2: The Christian Character",
        "reviewQuestions": [
            "What does Proverbs 6:6-11 teach us through the example of the ant?",
            "How did Richard Baxter view the relationship between work and worship?",
            "What is the difference between godly diligence and worldly ambition?",
            "Why did the Puritans see laziness as a spiritual danger?"
        ],
        "activity": "Choose a task you have been avoiding. Complete it thoroughly and cheerfully as unto the Lord. Then write a reflection on how working diligently affected your attitude and spirit.",
    },
    {
        "lesson": 9, "id": 209,
        "title": "Humility and Pride",
        "subtitle": "Unit 2, Lesson 9 -- Proverbs and Jonathan Edwards on the Humble Heart",
        "description": "What Proverbs teaches about pride going before destruction, and Jonathan Edwards on true humility as the foundation of Christian virtue.",
        "unit": "Unit 2: The Christian Character",
        "reviewQuestions": [
            "What does Proverbs 16:18 warn about pride?",
            "How did Jonathan Edwards define true humility?",
            "Why is pride considered the root of all other sins by many Puritan writers?",
            "What are practical signs of humility in everyday life?"
        ],
        "activity": "Read Proverbs 16:18-19 and Philippians 2:3-8. Write a comparison showing how Christ is the ultimate example of humility. Include one way you can practice humility this week.",
    },
    {
        "lesson": 10, "id": 210,
        "title": "Integrity in All Things",
        "subtitle": "Unit 2, Lesson 10 -- Thomas Brooks on Walking Uprightly",
        "description": "Proverbs 11:3 on integrity guiding the upright. Thomas Brooks on the marks of true Christian integrity.",
        "unit": "Unit 2: The Christian Character",
        "reviewQuestions": [
            "What does Proverbs 11:3 say about the integrity of the upright?",
            "According to Thomas Brooks, what are the marks of a person of integrity?",
            "How did Brooks distinguish between outward morality and true heart-integrity?",
            "Why is integrity especially important when no one is watching?"
        ],
        "activity": "Write a personal integrity covenant listing five commitments you will make to live with honesty before God and others. Sign it and date it, and share it with a family member.",
    },
    # ---- UNIT 3: Walking in Wisdom (Lessons 11-15) ----
    {
        "lesson": 11, "id": 211,
        "title": "Wisdom in Friendships",
        "subtitle": "Unit 3, Lesson 11 -- Proverbs on Choosing Companions",
        "description": "Proverbs 13:20 and 27:17 on wise friendships. John Owen on the importance of godly fellowship for spiritual growth.",
        "unit": "Unit 3: Walking in Wisdom",
        "reviewQuestions": [
            "What does Proverbs 13:20 teach about the influence of friends?",
            "How does Proverbs 27:17 describe the effect of godly friendship?",
            "What did John Owen teach about the necessity of Christian fellowship?",
            "How can you evaluate whether a friendship is helping or hindering your walk with God?"
        ],
        "activity": "Make a list of your five closest friends or companions. For each one, write whether they generally encourage you toward wisdom or pull you toward folly. Pray about your friendships.",
    },
    {
        "lesson": 12, "id": 212,
        "title": "Wisdom in the Home",
        "subtitle": "Unit 3, Lesson 12 -- The Puritan Household",
        "description": "Proverbs 24:3-4 on building a house by wisdom. Richard Baxter's Christian Directory on ordering the household for God's glory.",
        "unit": "Unit 3: Walking in Wisdom",
        "reviewQuestions": [
            "What does Proverbs 24:3-4 say about building a house through wisdom?",
            "How did Richard Baxter instruct families in his Christian Directory?",
            "What were the key elements of a Puritan household?",
            "How can modern families apply Puritan principles to their home life?"
        ],
        "activity": "Interview your parents about how they try to run your household for God's glory. Write down their answers and suggest one new family practice you could start together.",
    },
    {
        "lesson": 13, "id": 213,
        "title": "Wisdom with Money",
        "subtitle": "Unit 3, Lesson 13 -- Proverbs on Wealth and Stewardship",
        "description": "What Proverbs teaches about money, generosity, and contentment. Thomas Watson on divine contentment as the antidote to greed.",
        "unit": "Unit 3: Walking in Wisdom",
        "reviewQuestions": [
            "What does Proverbs 11:24-25 teach about generosity?",
            "How did Thomas Watson describe the art of divine contentment?",
            "What warnings does Proverbs give about the love of money?",
            "How can we be content with what God has given us while still working diligently?"
        ],
        "activity": "Calculate how you could give a portion of your allowance or earnings to help someone in need. Plan a specific act of generosity and carry it out this week.",
    },
    {
        "lesson": 14, "id": 214,
        "title": "Wisdom Under Trials",
        "subtitle": "Unit 3, Lesson 14 -- Jeremiah Burroughs on the Rare Jewel",
        "description": "Proverbs 24:10 on strength in adversity. Jeremiah Burroughs and The Rare Jewel of Christian Contentment on finding peace in affliction.",
        "unit": "Unit 3: Walking in Wisdom",
        "reviewQuestions": [
            "What does Proverbs 24:10 say about trials revealing our strength?",
            "What was the 'rare jewel' that Jeremiah Burroughs wrote about?",
            "How did Burroughs define Christian contentment?",
            "What practical steps can we take to find peace during difficult times?"
        ],
        "activity": "Write about a trial you or your family has faced. How did God use it for good? Read Romans 8:28 and write a prayer of trust for your current challenges.",
    },
    {
        "lesson": 15, "id": 215,
        "title": "Wisdom and the Fear of the Lord Revisited",
        "subtitle": "Unit 3, Lesson 15 -- Unit Review and Deeper Study",
        "description": "A deeper look at the thread connecting the fear of God, wisdom, and daily living. Review of Units 1-3 with Jonathan Edwards on religious affections.",
        "unit": "Unit 3: Walking in Wisdom",
        "reviewQuestions": [
            "How does the fear of God connect to every area of wisdom we have studied?",
            "What did Jonathan Edwards teach about religious affections and true piety?",
            "What is the difference between head knowledge and heart knowledge of God?",
            "Summarize the three most important lessons you have learned so far."
        ],
        "activity": "Write a one-page reflection on how your understanding of the fear of God has grown over these lessons. Include specific examples from Proverbs and the Puritan writers.",
    },
    # ---- UNIT 4: The Faithful Life (Lessons 16-20) ----
    {
        "lesson": 16, "id": 216,
        "title": "Mortifying Sin",
        "subtitle": "Unit 4, Lesson 16 -- John Owen on the Battle Against Sin",
        "description": "John Owen's classic teaching on the mortification of sin. Be killing sin, or sin will be killing you. The daily battle of the Christian life.",
        "unit": "Unit 4: The Faithful Life",
        "reviewQuestions": [
            "What did John Owen mean by 'mortification of sin'?",
            "Why did Owen say 'Be killing sin, or sin will be killing you'?",
            "What role does the Holy Spirit play in putting sin to death?",
            "How does Proverbs describe the danger of unchecked sin?"
        ],
        "activity": "Identify one habitual sin or bad habit you struggle with. Write out a plan to fight it using Scripture, prayer, and accountability. Share your plan with a parent or mentor.",
    },
    {
        "lesson": 17, "id": 217,
        "title": "The Discipline of Prayer",
        "subtitle": "Unit 4, Lesson 17 -- Richard Baxter and the Puritan Prayer Life",
        "description": "Richard Baxter's teaching on prayer from The Saints' Everlasting Rest. How the Puritans made prayer the foundation of faithful living.",
        "unit": "Unit 4: The Faithful Life",
        "reviewQuestions": [
            "How did Richard Baxter structure his prayer life?",
            "What did Baxter teach about heavenly meditation in The Saints' Everlasting Rest?",
            "Why is prayer essential for the faithful Christian life?",
            "What practical advice does Proverbs give about seeking God in prayer?"
        ],
        "activity": "Set aside 15 minutes for focused prayer using the ACTS model: Adoration, Confession, Thanksgiving, Supplication. Write down your prayers and any impressions God gives you.",
    },
    {
        "lesson": 18, "id": 218,
        "title": "Perseverance of the Saints",
        "subtitle": "Unit 4, Lesson 18 -- Thomas Brooks on Enduring to the End",
        "description": "Thomas Brooks on the perseverance of believers. Proverbs 24:16 on the righteous falling seven times but rising again.",
        "unit": "Unit 4: The Faithful Life",
        "reviewQuestions": [
            "What does Proverbs 24:16 promise about the righteous person?",
            "How did Thomas Brooks encourage believers who felt weak in their faith?",
            "What is the doctrine of the perseverance of the saints?",
            "How does knowing God will keep us give us strength to keep going?"
        ],
        "activity": "Research one Puritan or Reformer who persevered through great suffering for their faith (e.g., Bunyan, Baxter, Latimer). Write a short biography focusing on how they endured.",
    },
    {
        "lesson": 19, "id": 219,
        "title": "The Virtuous Life in Proverbs 31",
        "subtitle": "Unit 4, Lesson 19 -- A Portrait of Faithful Living",
        "description": "Proverbs 31 as a portrait of faithful living for all believers. The virtues of diligence, generosity, and the fear of the Lord.",
        "unit": "Unit 4: The Faithful Life",
        "reviewQuestions": [
            "What virtues does Proverbs 31 celebrate?",
            "Why does Proverbs 31:30 say the fear of the Lord matters more than outward appearance?",
            "How do the virtues in Proverbs 31 apply to everyone, not just women?",
            "What qualities from Proverbs 31 do you most want to develop?"
        ],
        "activity": "Choose three virtues from Proverbs 31 (e.g., diligence, generosity, strength). For each one, write a practical plan for how you will cultivate that virtue this month.",
    },
    {
        "lesson": 20, "id": 220,
        "title": "A Life Built on Wisdom",
        "subtitle": "Unit 4, Lesson 20 -- Final Review and Commissioning",
        "description": "A comprehensive review of all four units. The call to build a life on the foundation of godly wisdom, fear of the Lord, and faithful living.",
        "unit": "Unit 4: The Faithful Life",
        "reviewQuestions": [
            "Summarize what you have learned about the fear of God across all four units.",
            "Which Puritan author's teaching has meant the most to you, and why?",
            "How has your understanding of Proverbs changed through this course?",
            "What three commitments will you make going forward to live wisely?"
        ],
        "activity": "Write a 'Personal Wisdom Creed' -- a document summarizing the key truths you have learned and the commitments you are making. Read it aloud to your family as a declaration.",
    },
]


# ===================================================================
# TOGETHER / COUPLES CONTENT  (IDs 301-331, Proverbs 1-31)
# ===================================================================
TOGETHER_EPISODES = [
    {"day": 1, "id": 301, "title": "Beginning in Wisdom Together", "subtitle": "Day 1 -- Couples Devotional",
     "description": "As a couple, explore what it means to build your marriage on the foundation of reverential awe for God, from Proverbs 1.",
     "reflectionPrompt": "How can we fear the Lord more deeply as a couple? What would change if reverence for God shaped every decision we make together?",
     "prayerFocus": "Pray for wisdom in your marriage. Ask God to help you both grow in reverence and to make Him the center of your relationship."},
    {"day": 2, "id": 302, "title": "Seeking Wisdom Side by Side", "subtitle": "Day 2 -- Couples Devotional",
     "description": "Proverbs 2 invites us to seek wisdom like hidden treasure. As a couple, discover the joy of pursuing God's Word together.",
     "reflectionPrompt": "What does it look like to seek wisdom as a team? How can we prioritize studying God's Word together?",
     "prayerFocus": "Pray for unity in pursuing God. Ask Him to give you both a hunger for His Word and the discipline to seek Him together consistently."},
    {"day": 3, "id": 303, "title": "Trusting God with Our Marriage", "subtitle": "Day 3 -- Couples Devotional",
     "description": "Proverbs 3:5-6 calls us to trust in the Lord with all our hearts. As a couple, surrender your plans and worries to Him.",
     "reflectionPrompt": "Where do we need to trust God more in our marriage? Are there plans or worries we are holding onto instead of surrendering?",
     "prayerFocus": "Surrender your plans to God together. Pray over any areas of anxiety or uncertainty and commit them to the Lord."},
    {"day": 4, "id": 304, "title": "Guarding Each Other's Hearts", "subtitle": "Day 4 -- Couples Devotional",
     "description": "Proverbs 4:23 calls us to guard our hearts. In marriage, we help each other protect what enters our minds and spirits.",
     "reflectionPrompt": "How can we help each other guard our hearts? Are there influences we should remove or habits we should build?",
     "prayerFocus": "Pray for each other's hearts and minds. Ask God to help you be watchful guardians of each other's spiritual health."},
    {"day": 5, "id": 305, "title": "Staying on the Path Together", "subtitle": "Day 5 -- Couples Devotional",
     "description": "Proverbs 5 warns us to stay on the right path. As a couple, commit to walking faithfully together.",
     "reflectionPrompt": "What temptations or distractions pull us off the path God has for our marriage? How can we strengthen each other?",
     "prayerFocus": "Pray for faithfulness and purity in your marriage. Ask God to keep your feet on His path and your eyes on Him."},
    {"day": 6, "id": 306, "title": "Working Together with Diligence", "subtitle": "Day 6 -- Couples Devotional",
     "description": "Proverbs 6 teaches about diligence through the example of the ant. In marriage, we build a life together through faithful daily effort.",
     "reflectionPrompt": "Are we working together diligently to build our home and family? Where might laziness or neglect be creeping in?",
     "prayerFocus": "Pray for a diligent spirit in your home. Ask God to help you serve each other and your family with cheerful, consistent effort."},
    {"day": 7, "id": 307, "title": "Holding Fast to Wisdom", "subtitle": "Day 7 -- Couples Devotional",
     "description": "Proverbs 7 warns against the seductions of folly. As a couple, hold fast to wisdom and to each other.",
     "reflectionPrompt": "How can we protect our marriage from the subtle temptations of the world? What safeguards should we put in place?",
     "prayerFocus": "Pray for protection over your marriage. Ask God to surround you both with wisdom and to shield you from the enemy's schemes."},
    {"day": 8, "id": 308, "title": "Delighting in God's Creation Together", "subtitle": "Day 8 -- Couples Devotional",
     "description": "Proverbs 8 celebrates wisdom present at creation. As a couple, marvel at the beauty and order God has woven into the world.",
     "reflectionPrompt": "When was the last time you paused to appreciate God's creation together? How does wonder deepen your relationship?",
     "prayerFocus": "Thank God for the beauty of His creation. Pray that a shared sense of wonder would draw you closer to Him and to each other."},
    {"day": 9, "id": 309, "title": "Choosing Wisdom's Feast", "subtitle": "Day 9 -- Couples Devotional",
     "description": "Proverbs 9 presents two invitations: Wisdom's feast and Folly's feast. Every day as a couple, you choose which table to sit at.",
     "reflectionPrompt": "What choices are we making daily as a couple? Are we accepting Wisdom's invitation or drifting toward foolish patterns?",
     "prayerFocus": "Pray for discernment in your daily choices. Ask God to help you both recognize Wisdom's voice and choose her feast every day."},
    {"day": 10, "id": 310, "title": "Speaking Life to Each Other", "subtitle": "Day 10 -- Couples Devotional",
     "description": "Proverbs 10 teaches about the power of the tongue. In marriage, our words can be a wellspring of life or a source of pain.",
     "reflectionPrompt": "How are we speaking to each other? Are our words building up or tearing down? What words does your spouse most need to hear?",
     "prayerFocus": "Pray for grace in your speech. Ask God to make your words a well of life for your spouse, especially during stressful seasons."},
    {"day": 11, "id": 311, "title": "Walking in Integrity as One", "subtitle": "Day 11 -- Couples Devotional",
     "description": "Proverbs 11 celebrates integrity. A marriage built on honesty and transparency is a marriage built on solid ground.",
     "reflectionPrompt": "Is there anything we are hiding from each other, even small things? How can we build deeper honesty between us?",
     "prayerFocus": "Pray for integrity and transparency in your marriage. Ask God to remove anything hidden and build a foundation of total trust."},
    {"day": 12, "id": 312, "title": "Receiving Correction in Love", "subtitle": "Day 12 -- Couples Devotional",
     "description": "Proverbs 12 teaches that the wise love correction. In marriage, we grow when we can lovingly speak truth to each other.",
     "reflectionPrompt": "How do we handle correction from each other? Can we receive honest feedback with grace instead of defensiveness?",
     "prayerFocus": "Pray for teachable hearts. Ask God to help you both give and receive correction with gentleness and love, not pride."},
    {"day": 13, "id": 313, "title": "Choosing Wise Companions", "subtitle": "Day 13 -- Couples Devotional",
     "description": "Proverbs 13:20 teaches that we become like our companions. As a couple, pursue friendships that strengthen your marriage.",
     "reflectionPrompt": "Do the people we spend the most time with build up or weaken our marriage? Are there friendships we should cultivate or boundaries we should set?",
     "prayerFocus": "Pray for wise friends and mentors. Ask God to surround your marriage with couples who love Him and will encourage your faithfulness."},
    {"day": 14, "id": 314, "title": "The Way That Seems Right", "subtitle": "Day 14 -- Couples Devotional",
     "description": "Proverbs 14:12 warns about the way that seems right but leads to death. As a couple, test your decisions against God's Word.",
     "reflectionPrompt": "Have we made decisions recently that seemed right but were not tested against Scripture? How can we build a habit of seeking God's counsel first?",
     "prayerFocus": "Pray for spiritual discernment. Ask God to protect your marriage from choices that seem right but lead away from His will."},
    {"day": 15, "id": 315, "title": "The Gentle Answer", "subtitle": "Day 15 -- Couples Devotional",
     "description": "Proverbs 15:1 teaches the power of a soft answer. In marriage, a gentle response can turn away conflict and bring peace.",
     "reflectionPrompt": "When conflict arises, do we respond with gentle words or harsh ones? What would change if we committed to soft answers?",
     "prayerFocus": "Pray for gentle tongues. Ask God to help you respond to each other with patience and kindness, even in heated moments."},
    {"day": 16, "id": 316, "title": "Surrendering Our Plans", "subtitle": "Day 16 -- Couples Devotional",
     "description": "Proverbs 16:9 reminds us that we plan, but the Lord directs our steps. As a couple, hold your plans loosely and trust His leading.",
     "reflectionPrompt": "What plans are we holding too tightly? How can we surrender our timeline, our goals, and our future to God's direction?",
     "prayerFocus": "Lay your plans before the Lord. Pray for open hands and willing hearts to follow wherever He leads your marriage."},
    {"day": 17, "id": 317, "title": "A Friend Who Loves at All Times", "subtitle": "Day 17 -- Couples Devotional",
     "description": "Proverbs 17:17 describes a friend who loves at all times. Your spouse is meant to be that friend -- through every season.",
     "reflectionPrompt": "Am I being a faithful friend to my spouse in this season? What does loving at ALL times look like when life is hard?",
     "prayerFocus": "Pray for steadfast love. Ask God to help you both be faithful friends to each other through every season of life."},
    {"day": 18, "id": 318, "title": "Running to the Strong Tower", "subtitle": "Day 18 -- Couples Devotional",
     "description": "Proverbs 18:10 tells us the name of the Lord is a strong tower. As a couple, run to Him together when storms come.",
     "reflectionPrompt": "When trouble comes, do we run to God together or try to handle it alone? How can we make prayer our first response?",
     "prayerFocus": "Pray together over any current storms or challenges. Run to the Strong Tower together and find your safety in Him."},
    {"day": 19, "id": 319, "title": "Patience with One Another", "subtitle": "Day 19 -- Couples Devotional",
     "description": "Proverbs 19:11 teaches that patience and forgiveness are glorious. In marriage, patience is among the greatest gifts we give.",
     "reflectionPrompt": "Where do I need more patience with my spouse? Am I quick to forgive or do I hold onto offenses?",
     "prayerFocus": "Pray for patience and a forgiving spirit. Ask God to help you release offenses quickly and extend grace freely."},
    {"day": 20, "id": 320, "title": "Building a Good Name Together", "subtitle": "Day 20 -- Couples Devotional",
     "description": "Proverbs 20 teaches about integrity and reputation. As a couple, you are building a legacy -- a name that will outlast you.",
     "reflectionPrompt": "What kind of legacy are we building together? How do others see our marriage? Does it point them to Christ?",
     "prayerFocus": "Pray for a godly legacy. Ask God to help your marriage reflect His love and faithfulness to everyone who sees it."},
    {"day": 21, "id": 321, "title": "God Sees Our Hearts", "subtitle": "Day 21 -- Couples Devotional",
     "description": "Proverbs 21:2 reminds us that God weighs our hearts. As a couple, pursue purity of heart before Him.",
     "reflectionPrompt": "If God weighed our hearts today, what would He find? Are we serving each other with pure motives?",
     "prayerFocus": "Ask God to search your hearts as a couple. Pray for purity of motive, sincerity of love, and freedom from selfishness."},
    {"day": 22, "id": 322, "title": "Training Up Our Children", "subtitle": "Day 22 -- Couples Devotional",
     "description": "Proverbs 22:6 calls parents to train up children in the way they should go. As a couple, carry this sacred responsibility together.",
     "reflectionPrompt": "How are we doing at training our children in the Lord? Are we aligned in our approach to spiritual formation at home?",
     "prayerFocus": "Pray for wisdom in parenting. Ask God to help you train your children together with consistency, love, and faithfulness."},
    {"day": 23, "id": 323, "title": "Giving God Our Hearts", "subtitle": "Day 23 -- Couples Devotional",
     "description": "Proverbs 23:26 is God's invitation: Give me thine heart. As a couple, give your marriage wholly to Him.",
     "reflectionPrompt": "Have we truly given our marriage to God, or are we holding parts of it back? What would full surrender look like?",
     "prayerFocus": "Pray a prayer of full surrender. Give God your marriage, your finances, your parenting, your future -- everything."},
    {"day": 24, "id": 324, "title": "Rising Together After Failure", "subtitle": "Day 24 -- Couples Devotional",
     "description": "Proverbs 24:16 promises the righteous fall seven times but rise again. In marriage, we help each other get back up.",
     "reflectionPrompt": "How do we respond when one of us fails or falls? Do we condemn or do we help each other rise?",
     "prayerFocus": "Pray for a spirit of restoration. Ask God to help you always extend a hand to lift each other up, never a foot to push down."},
    {"day": 25, "id": 325, "title": "Overcoming Evil with Good", "subtitle": "Day 25 -- Couples Devotional",
     "description": "Proverbs 25:21-22 teaches us to respond to enemies with kindness. As a couple, choose love even when it is difficult.",
     "reflectionPrompt": "Is there someone who has hurt us or our family? How can we respond with kindness and forgiveness as a couple?",
     "prayerFocus": "Pray for those who have wronged you. Ask God for the grace to overcome evil with good, together as one."},
    {"day": 26, "id": 326, "title": "Humility in Marriage", "subtitle": "Day 26 -- Couples Devotional",
     "description": "Proverbs 26:12 warns about being wise in our own eyes. In marriage, humility is the soil in which love grows.",
     "reflectionPrompt": "Am I being humble in our marriage, or am I always sure I am right? How can we cultivate humility together?",
     "prayerFocus": "Pray for humility. Ask God to root out pride and self-righteousness, and to help you serve each other in lowliness of heart."},
    {"day": 27, "id": 327, "title": "Sharpening Each Other", "subtitle": "Day 27 -- Couples Devotional",
     "description": "Proverbs 27:17 tells us iron sharpens iron. Your spouse is God's gift to help you grow into who He created you to be.",
     "reflectionPrompt": "Are we sharpening each other spiritually? How can we challenge each other to grow without causing wounds?",
     "prayerFocus": "Pray for the grace to sharpen each other. Ask God to use your marriage as a refining tool for both of your characters."},
    {"day": 28, "id": 328, "title": "Boldness and Courage Together", "subtitle": "Day 28 -- Couples Devotional",
     "description": "Proverbs 28:1 says the righteous are bold as a lion. As a couple, draw courage from God to stand firm together.",
     "reflectionPrompt": "Where does our marriage need more boldness? Are there stands we need to take together for the sake of righteousness?",
     "prayerFocus": "Pray for holy courage. Ask God to make you bold as lions in standing for truth, righteousness, and the gospel."},
    {"day": 29, "id": 329, "title": "Holding to the Vision", "subtitle": "Day 29 -- Couples Devotional",
     "description": "Proverbs 29:18 warns that without vision, people perish. As a couple, keep God's Word as the vision for your marriage.",
     "reflectionPrompt": "Do we have a shared vision for our marriage rooted in God's Word? What is God calling us to build together?",
     "prayerFocus": "Pray for vision. Ask God to give you a clear picture of what He is calling your marriage to be and to do for His kingdom."},
    {"day": 30, "id": 330, "title": "Every Word of God Is Pure", "subtitle": "Day 30 -- Couples Devotional",
     "description": "Proverbs 30:5 declares every word of God is pure. As a couple, build your marriage on the bedrock of His trustworthy promises.",
     "reflectionPrompt": "Which promises of God are we standing on together? Are we building our marriage on His Word or on shifting sand?",
     "prayerFocus": "Thank God for His pure and trustworthy Word. Commit together to building your marriage on the promises of Scripture."},
    {"day": 31, "id": 331, "title": "A Marriage That Fears the Lord", "subtitle": "Day 31 -- Couples Devotional",
     "description": "Proverbs 31:30 says a woman who fears the Lord shall be praised. A marriage rooted in the fear of God will bear lasting fruit.",
     "reflectionPrompt": "As we close this month, what has God taught us about our marriage? How has the fear of the Lord shaped our love for each other?",
     "prayerFocus": "Pray a prayer of thanksgiving for your marriage. Commit to continuing to fear the Lord together and to building on the foundation of wisdom."},
]


# ===================================================================
# KEY SCRIPTURE PASSAGES FOR EACH PROVERBS CHAPTER (KJV)
# These are used across family + together generators
# ===================================================================
PROVERBS_KEY_VERSES = {
    1: ("Proverbs 1:7", "The fear of the LORD is the beginning of knowledge: but fools despise wisdom and instruction."),
    2: ("Proverbs 2:6", "For the LORD giveth wisdom: out of his mouth cometh knowledge and understanding."),
    3: ("Proverbs 3:5-6", "Trust in the LORD with all thine heart; and lean not unto thine own understanding. In all thy ways acknowledge him, and he shall direct thy paths."),
    4: ("Proverbs 4:23", "Keep thy heart with all diligence; for out of it are the issues of life."),
    5: ("Proverbs 5:21", "For the ways of man are before the eyes of the LORD, and he pondereth all his goings."),
    6: ("Proverbs 6:6-8", "Go to the ant, thou sluggard; consider her ways, and be wise: Which having no guide, overseer, or ruler, Provideth her meat in the summer, and gathereth her food in the harvest."),
    7: ("Proverbs 7:1-2", "My son, keep my words, and lay up my commandments with thee. Keep my commandments, and live; and my law as the apple of thine eye."),
    8: ("Proverbs 8:11", "For wisdom is better than rubies; and all the things that may be desired are not to be compared to it."),
    9: ("Proverbs 9:10", "The fear of the LORD is the beginning of wisdom: and the knowledge of the holy is understanding."),
    10: ("Proverbs 10:11", "The mouth of a righteous man is a well of life: but violence covereth the mouth of the wicked."),
    11: ("Proverbs 11:1-3", "A false balance is abomination to the LORD: but a just weight is his delight. When pride cometh, then cometh shame: but with the lowly is wisdom. The integrity of the upright shall guide them."),
    12: ("Proverbs 12:1", "Whoso loveth instruction loveth knowledge: but he that hateth reproof is brutish."),
    13: ("Proverbs 13:20", "He that walketh with wise men shall be wise: but a companion of fools shall be destroyed."),
    14: ("Proverbs 14:12", "There is a way which seemeth right unto a man, but the end thereof are the ways of death."),
    15: ("Proverbs 15:1", "A soft answer turneth away wrath: but grievous words stir up anger."),
    16: ("Proverbs 16:9", "A man's heart deviseth his way: but the LORD directeth his steps."),
    17: ("Proverbs 17:17", "A friend loveth at all times, and a brother is born for adversity."),
    18: ("Proverbs 18:10", "The name of the LORD is a strong tower: the righteous runneth into it, and is safe."),
    19: ("Proverbs 19:11", "The discretion of a man deferreth his anger; and it is his glory to pass over a transgression."),
    20: ("Proverbs 20:11", "Even a child is known by his doings, whether his work be pure, and whether it be right."),
    21: ("Proverbs 21:2", "Every way of a man is right in his own eyes: but the LORD pondereth the hearts."),
    22: ("Proverbs 22:6", "Train up a child in the way he should go: and when he is old, he will not depart from it."),
    23: ("Proverbs 23:26", "My son, give me thine heart, and let thine eyes observe my ways."),
    24: ("Proverbs 24:16", "For a just man falleth seven times, and riseth up again: but the wicked shall fall into mischief."),
    25: ("Proverbs 25:21", "If thine enemy be hungry, give him bread to eat; and if he be thirsty, give him water to drink."),
    26: ("Proverbs 26:12", "Seest thou a man wise in his own conceit? there is more hope of a fool than of him."),
    27: ("Proverbs 27:17", "Iron sharpeneth iron; so a man sharpeneth the countenance of his friend."),
    28: ("Proverbs 28:1", "The wicked flee when no man pursueth: but the righteous are bold as a lion."),
    29: ("Proverbs 29:18", "Where there is no vision, the people perish: but he that keepeth the law, happy is he."),
    30: ("Proverbs 30:5", "Every word of God is pure: he is a shield unto them that put their trust in him."),
    31: ("Proverbs 31:30", "Favour is deceitful, and beauty is vain: but a woman that feareth the LORD, she shall be praised."),
}

# Puritan author quotes / insights keyed by Proverbs chapter
PURITAN_INSIGHTS = {
    1: ("Thomas Watson", "Thomas Watson once wrote that the fear of God is the beginning of all wisdom, and the practice of wisdom is the beginning of all obedience. To fear God aright is to reverence His majesty, tremble at His power, and rest in His love."),
    2: ("John Owen", "John Owen reminds us that the searching out of wisdom is not merely an intellectual pursuit. It is a spiritual discipline, an act of love toward the God who has hidden treasures in His Word for those who earnestly seek Him."),
    3: ("Richard Baxter", "Richard Baxter, in his Christian Directory, counseled families to begin each day by surrendering their plans to God. He wrote that trust is not passive; it is the active leaning of the whole soul upon the promises of a faithful God."),
    4: ("Thomas Brooks", "Thomas Brooks, in Precious Remedies Against Satan's Devices, taught that guarding the heart is the Christian's first and most important battle. Satan's primary strategy is to enter through the heart, and so the heart must be garrisoned by grace."),
    5: ("John Owen", "John Owen, in The Mortification of Sin, warned that we must watch our paths with great diligence. Sin does not announce itself with a trumpet; it creeps in quietly, through small compromises and unguarded moments."),
    6: ("Richard Baxter", "Richard Baxter urged believers to be diligent stewards of their time. In his Saints' Everlasting Rest, he wrote that the diligent soul finds God in labor, in rest, and in every duty. The sluggard loses not only time but communion with God."),
    7: ("Thomas Watson", "Thomas Watson taught that the Word of God, hidden in the heart, is the believer's strongest shield against temptation. He that fills his mind with Scripture leaves no room for the enemy's suggestions."),
    8: ("Jonathan Edwards", "Jonathan Edwards marveled at the wisdom of God displayed in creation, seeing in every leaf and star the handiwork of infinite intelligence and boundless love. Wisdom is not abstract; it is woven into the very fabric of the world."),
    9: ("Thomas Watson", "Thomas Watson wrote that every day sets before us two feasts: the feast of Wisdom, which nourishes the soul unto eternal life, and the feast of Folly, which poisons the heart unto destruction. Choose wisely, for your very life depends upon it."),
    10: ("Jeremiah Burroughs", "Jeremiah Burroughs taught that the tongue is the most powerful instrument God has placed in human hands. A word fitly spoken can heal a broken heart, but a careless word can wound a soul for years."),
    11: ("Thomas Brooks", "Thomas Brooks urged believers to walk in integrity at all times, for God sees what man cannot. He wrote that the upright man has nothing to hide, for his conscience is clear before God and man."),
    12: ("John Owen", "John Owen reminded his listeners that correction from a loving hand is one of God's greatest mercies. He who refuses reproof has already begun the path toward spiritual ruin."),
    13: ("Richard Baxter", "Richard Baxter strongly counseled young people to choose their companions with great care. He wrote that the friends you walk with will shape the person you become, for the influence of daily fellowship is stronger than we know."),
    14: ("Jonathan Edwards", "Jonathan Edwards warned that the human heart is endlessly creative in justifying its own desires. The way that seems right often appeals to our pride, our comfort, or our fear. Only the light of Scripture can reveal the true path."),
    15: ("Jeremiah Burroughs", "Jeremiah Burroughs, in The Rare Jewel of Christian Contentment, observed that a gentle spirit is the fruit of a contented heart. He who is at peace with God can afford to be gentle with men."),
    16: ("Thomas Watson", "Thomas Watson counseled believers to hold their plans loosely, for God is the supreme director of all events. Our hearts devise, but His hand overrules all things for His glory and our good."),
    17: ("John Bunyan", "John Bunyan, who knew the depths of friendship through his years of imprisonment, wrote that a true friend is one who loves not only in the sunshine but in the storm. Such friendship is a portrait of Christ's love for His people."),
    18: ("Thomas Brooks", "Thomas Brooks wrote that the name of the Lord encompasses all His perfections, His power, His mercy, His faithfulness, His love. When the righteous run into this tower, they find not merely safety but rest for the soul."),
    19: ("Richard Baxter", "Richard Baxter taught that patience is not weakness but strength under control. He wrote that the man who governs his spirit is greater than he who conquers a city, for self-mastery is the fruit of the Holy Spirit at work."),
    20: ("Thomas Watson", "Thomas Watson reminded parents that children are known by their deeds from their earliest years. The habits formed in childhood become the character of the adult. Therefore, train them in righteousness from the very first."),
    21: ("Jonathan Edwards", "Jonathan Edwards taught that true religion is not about outward conformity but about the affections of the heart. God weighs not merely our actions but the motives and desires that drive them."),
    22: ("Richard Baxter", "Richard Baxter, in his Christian Directory, devoted many pages to the sacred duty of training children. He saw it as the most important work any parent could undertake, for the souls of children are entrusted to us by God Himself."),
    23: ("Thomas Brooks", "Thomas Brooks wrote that giving God your heart is not a single act but a daily surrender. Each morning, we must renew our commitment, offering Him not the leftovers of our affection but the first fruits."),
    24: ("John Bunyan", "John Bunyan himself was a living example of this proverb. Cast down many times by doubt, despair, and persecution, he rose again and again by the grace of God. His Pilgrim's Progress was written from the very dungeon where he fell and rose."),
    25: ("Jeremiah Burroughs", "Jeremiah Burroughs taught that responding to enemies with kindness is the most powerful testimony a Christian can give. It is not natural; it is supernatural. It is the love of Christ flowing through a surrendered heart."),
    26: ("Thomas Watson", "Thomas Watson warned that self-conceit is the most dangerous form of foolishness, for the man who thinks he knows everything is unteachable. Humility is the first step on the road to true wisdom."),
    27: ("John Owen", "John Owen valued the sharpening influence of Christian friendship above almost everything else in the spiritual life. He wrote that iron cannot sharpen itself; we need the faithful wounds of a friend to refine our character."),
    28: ("Thomas Brooks", "Thomas Brooks wrote that the boldness of the righteous comes not from self-confidence but from God-confidence. When you know that the Almighty stands with you, you can face any adversary without flinching."),
    29: ("Richard Baxter", "Richard Baxter lamented the spiritual blindness that comes when people cast off the authority of God's Word. Without the vision of Scripture, he wrote, men wander in darkness and perish for lack of direction."),
    30: ("Jonathan Edwards", "Jonathan Edwards treasured the purity and sufficiency of God's Word. He wrote that every promise in Scripture is backed by the full faithfulness and power of the Almighty. We can trust every word completely."),
    31: ("Thomas Watson", "Thomas Watson wrote beautifully about the fear of the Lord as the crowning virtue of a godly life. All outward graces fade, but the soul that fears the Lord possesses an imperishable beauty that grows brighter unto the perfect day."),
}

# ===================================================================
# Family devotional teaching paragraphs (unique per day/chapter)
# ===================================================================
FAMILY_TEACHINGS = {
    1: """Now, what does it mean to fear the Lord? It does not mean to be terrified of God, as though He were an angry giant looking to punish us. No, no. To fear the Lord means to stand in awe of Him, to reverence Him, to know deep in your heart that He is great and holy and wonderful. Think of it this way: imagine you were standing at the edge of a mighty waterfall, hearing the thunder of the water, feeling the mist on your face. You would not be afraid that the waterfall was angry at you. But you would feel small. You would feel amazed. That is something like what it means to fear the Lord.

And here is the beautiful part: this great and holy God is also our loving Father. He is not far away. He is right here, closer than your own breath, and He loves you more than you can imagine. The Puritans understood this. Thomas Watson, a Puritan pastor who lived hundreds of years ago, taught his people that the fear of God and the love of God go together like two wings on a bird. You cannot fly with only one.

So when we read our Bibles, when we pray together as a family, when we obey God even when it is hard, we are showing that we fear and love Him. And that, dear ones, is where all true wisdom begins. Not in being the smartest or the strongest, but in knowing that God is God, and we are His beloved children.""",

    2: """Solomon tells us in Proverbs chapter 2 to seek wisdom as if we were looking for hidden treasure. Now, if someone told you there was a chest of gold buried in your backyard, what would you do? Would you sit on the couch and say, maybe I will look for it tomorrow? No! You would grab a shovel and start digging right away! You would search until you found it.

That is how God wants us to search for His wisdom. Not casually, not halfway, but with our whole hearts. And here is the wonderful promise: when we seek Him, we find Him. God does not hide from those who truly look for Him. He rewards the diligent seeker.

John Owen, one of the greatest Puritan thinkers, wrote that searching the Scriptures is an act of love toward God. When you open your Bible and read it carefully, you are saying to God, I love You, and I want to know You better. What a beautiful thought! Reading the Bible is not a chore. It is a treasure hunt. And the treasure is knowing God Himself.

So tonight, or tomorrow morning, when we open God's Word together, let us do it with the excitement of treasure hunters. Because the riches we will find in Scripture are worth more than all the gold and silver in the world.""",

    3: """Trust in the Lord with all thine heart. Those words from Proverbs chapter 3 are some of the most beloved in all the Bible. But what does it really mean to trust God with ALL your heart?

Think about a time when you were learning to swim. At some point, you had to let go of the side of the pool and trust the water to hold you up. That was scary, was it not? But once you let go, you discovered that the water could hold you. That is what trusting God is like. It means letting go of our need to control everything and believing that God's hands are strong enough to hold us.

Richard Baxter, a Puritan pastor who helped many families grow in their faith, taught that trust is not something we do once. It is something we practice every single day. Every morning when we wake up, we have a choice: will I try to figure everything out on my own, or will I ask God to guide my steps? The second way is the way of wisdom.

And notice what God promises: He shall direct thy paths. He does not promise that the path will always be easy. But He promises that if we trust Him, He will lead us the right way. That is a promise our whole family can hold onto, no matter what we face.""",

    4: """Keep thy heart with all diligence, Solomon writes in Proverbs chapter 4. Your heart is like a garden. Whatever seeds you plant in it will grow. If you plant seeds of kindness, truth, and love for God, beautiful things will grow. But if you let weeds of anger, lies, or selfishness take root, they will choke out the good things.

That is why God tells us to guard our hearts. He knows that what goes into our hearts through our eyes and ears eventually comes out in our words and actions. The things we watch, the music we listen to, the conversations we have, the thoughts we think, they all plant seeds.

Thomas Brooks, a Puritan preacher who wrote a famous book about how to fight temptation, warned that the devil's favorite strategy is to sneak bad things into our hearts when we are not paying attention. He does not knock loudly on the front door. He slips in through a window we left open. That is why guarding our hearts is so important.

So how do we guard our hearts? By filling them with good things! When we read the Bible, sing hymns, pray, and speak kindly to one another, we are planting good seeds and locking the windows against the enemy. Let us be a family that guards our hearts together.""",

    5: """Proverbs chapter 5 has a message that is important for every age: be careful which path you walk on. In life, there are many roads we can take. Some look exciting and fun, but they lead to places we do not want to go. Other paths seem harder at first, but they lead to safety, joy, and peace.

John Owen, who wrote much about the Christian's daily battle against sin, taught that sin never announces itself honestly. It never says, Hello, I am here to ruin your life. Instead, it dresses up in attractive clothing and whispers, This will be fun. Come, try it just once. That is why we must learn to recognize the wrong path before we start walking down it.

How do we do that? By knowing God's Word so well that we can spot a lie when we hear one. The Bible is like a lamp for our feet, as the Psalmist wrote. It lights up the path so we can see where we are going. Without it, we stumble in the dark.

As a family, let us commit to walking the right path together. When one of us starts to stray, the others can gently say, Wait, come back this way. That is what a family that fears the Lord does. We watch out for each other.""",

    6: """Go to the ant, thou sluggard! What a funny verse that is. Imagine God telling us to go watch bugs! But there is deep wisdom here. The tiny ant works hard every single day. Nobody has to tell her to get up and get to work. She does not have a boss standing over her. She simply does what needs to be done, day after day, storing up food for the future.

God is telling us that we can learn something from this little creature. Hard work is not a punishment. It is a gift. When we work diligently, whether it is homework, chores, practicing an instrument, or helping a neighbor, we are honoring God with the strength and abilities He has given us.

Richard Baxter taught that the Puritans saw all honest work as worship. Whether you were a farmer, a baker, a student, or a mother caring for children, if you did your work heartily as unto the Lord, it was pleasing to God. There was no division between sacred work and ordinary work. All of it was sacred when done for God's glory.

So the next time you feel like putting off your chores or your homework, remember the little ant. She does not complain. She does not procrastinate. She just gets to work. And God calls that wise.""",

    7: """Proverbs chapter 7 is about keeping God's commandments close to us, like a treasured friend. Solomon says, Say unto wisdom, Thou art my sister; and call understanding thy kinswoman. What a beautiful picture. Wisdom should be as close to us as our own family.

Thomas Watson taught that hiding God's Word in our hearts is the single best defense against temptation. When we have memorized Scripture, we carry it with us everywhere we go. It is always there, ready to help us when we face a hard choice.

Think of it like a shield. A soldier would never go into battle without his shield. And God's Word is our shield. When a temptation comes, when a lie whispers in our ear, we can answer it with the truth of Scripture. That is exactly what Jesus did when He was tempted in the wilderness. He answered every temptation with the Word of God.

That is why we memorize our memory verses as a family. We are building our shields together. We are filling our hearts and minds with truth so that when the hard moments come, we are ready.""",

    8: """Proverbs chapter 8 takes us all the way back to the beginning of everything, to creation itself. Listen to what wisdom says: The LORD possessed me in the beginning of his way, before his works of old. Wisdom was there when God laid the foundations of the earth, when He set the stars in the sky, when He scooped out the oceans and piled up the mountains.

Jonathan Edwards, the great American preacher who lived in the 1700s, was filled with wonder at God's creation. He would walk through the woods and see the wisdom of God in every leaf, every spider's web, every ray of sunlight. He believed that creation was like a beautiful book written by God, and those who had eyes to see could read it everywhere.

What does this mean for us? It means that the same God who designed the galaxies and the snowflakes and the human eye, that same God is directing our lives. His wisdom is not small or limited. It is vast beyond our imagination. And this wise, powerful, infinite God invites us to know Him!

Next time you see a sunset, or hold a ladybug, or look up at the stars, remember: the God who made all of this is your Father, and He wants to share His wisdom with you.""",

    9: """In Proverbs chapter 9, Solomon paints a picture of two feasts. Wisdom has prepared a great banquet and calls out to everyone: Come, eat of my bread, and drink of the wine which I have mingled. Forsake the foolish, and live. But there is another feast too. Folly sits at her door and also calls out, inviting people to a meal that looks enticing but ends in darkness.

Every single day, we face this choice. Will we sit at Wisdom's table or at Folly's table? The things we choose to do, the words we speak, the attitudes we carry, they all show which feast we have chosen.

Thomas Watson wrote that the daily choices of a Christian are like small steps on a long journey. Each step seems small by itself, but over time, those steps take you either toward God or away from Him. That is why the small choices matter just as much as the big ones.

As a family, let us choose Wisdom's feast every day. Let us fill our home with the good bread of God's Word, the sweet wine of prayer and praise, and the nourishing food of love and encouragement.""",

    10: """The mouth of a righteous man is a well of life. What a beautiful picture from Proverbs chapter 10. Imagine a well of cool, clear water in the middle of a desert. People come to it and find refreshment, strength, and life. That is what our words can be.

But Solomon also warns that the wrong kinds of words bring destruction. Hurtful words, lies, gossip, and angry outbursts are like poison in the well. They make everything bitter.

Jeremiah Burroughs, a Puritan pastor known for his gentle spirit, taught that the tongue reveals what is truly in the heart. If our hearts are full of God's love, our words will bring life. If our hearts are full of anger or selfishness, our words will bring pain.

So here is a challenge for our family this week: let us pay close attention to the words we speak to each other. Before we say something, let us ask: Is this true? Is this kind? Is this necessary? If we can answer yes to all three, then our words will be like that well of life, refreshing everyone around us.""",

    11: """Proverbs chapter 11 begins with something that might seem unusual in a book of wisdom: a lesson about honest weights and measures. A false balance is abomination to the LORD: but a just weight is his delight. In the ancient marketplace, dishonest merchants would use rigged scales to cheat their customers. And God says, I hate that.

Why? Because God is a God of truth. He cannot lie, and He cannot stand lying. And this goes far beyond marketplace scales. It applies to everything. Are we honest in our words? Are we fair in how we treat others? Do we tell the truth even when it costs us something?

Thomas Brooks wrote that integrity means being the same person in private that you are in public. It means that if God pulled back the curtain and showed the whole world what you do when nobody is watching, you would not be ashamed.

And here is the beautiful thing: when we walk in honesty and integrity, we experience the delight of the Lord. He does not just tolerate honesty. He delights in it. Let us be a family that walks in truth, in big things and small.""",

    12: """Whoso loveth instruction loveth knowledge: but he that hateth reproof is brutish. Those are strong words from Proverbs chapter 12! But Solomon is making an important point: the wise person is the one who is willing to be corrected.

Nobody likes being told they are wrong. It stings. It makes us feel small. But the Puritans understood that correction is one of the greatest gifts God gives us. John Owen wrote that every reproof from a loving hand is a mercy from heaven. It is God using other people to help us see our blind spots and grow.

Think about it this way: if you had spinach stuck in your teeth, would you rather have a friend tell you, or would you rather walk around all day with no one saying anything? Of course you would want your friend to tell you! That is a small example, but it shows how correction, even when it is uncomfortable, is an act of love.

In our family, let us create a safe place where we can lovingly correct each other without anyone getting angry or defensive. That is a family that is growing in wisdom.""",

    13: """He that walketh with wise men shall be wise: but a companion of fools shall be destroyed. Proverbs chapter 13, verse 20, is one of the most practical verses in the whole Bible. Your friends shape who you become.

Richard Baxter wrote that the people you spend the most time with will have more influence on your character than almost anything else. If you walk with those who fear the Lord, you will grow in the fear of the Lord. But if you walk with those who mock God and ignore His ways, their attitudes will slowly rub off on you, even if you do not realize it.

This does not mean we should be unkind to people who do not know God. Not at all! But it does mean we should be intentional about who our closest friends and companions are. The people we trust, confide in, and spend the most time with should be people who love the Lord and encourage us to grow.

As a family, let us pray for wise friends. Let us ask God to bring people into our lives who will sharpen us and encourage our faith. And let us be that kind of friend to others too.""",

    14: """There is a way which seemeth right unto a man, but the end thereof are the ways of death. Proverbs 14, verse 12, is one of the most sobering verses in all of Scripture. Some paths look perfectly fine on the surface. They seem reasonable, safe, even wise. But they lead somewhere terrible.

Jonathan Edwards warned his listeners about the deceitfulness of the human heart. We are very good at convincing ourselves that what we want to do is the right thing to do. We can come up with reasons and excuses for almost anything. That is why we cannot trust our own feelings alone. We need a higher standard. We need God's Word.

How do we avoid the way that seems right but leads to destruction? By testing every decision, every plan, every desire against the truth of Scripture. Does this choice honor God? Does it line up with what the Bible teaches? Would I be comfortable making this choice in front of Jesus?

These are hard questions, but they are life-saving questions. Let us be a family that asks them honestly and follows God's way, even when it is not the popular way or the easy way.""",

    15: """A soft answer turneth away wrath: but grievous words stir up anger. Proverbs 15, verse 1. Oh, how much peace this one verse could bring into our homes if we truly lived it!

Think about the last time someone spoke harshly to you. What did it make you want to do? Probably speak harshly right back! That is the natural response. But God's way is different. God's way is the soft answer. The gentle reply. The patient word that refuses to pour gasoline on the fire.

Jeremiah Burroughs, who wrote about Christian contentment, observed that a gentle spirit flows from a heart that is at peace with God. When we are resting in God's love, we do not need to win every argument. We do not need to have the last word. We can afford to be gentle because our security is not in being right but in being God's.

This does not mean we never speak hard truths. Sometimes love requires honest words. But even hard truths can be spoken gently. Let us practice this in our home. The next time we feel anger rising, let us take a breath, pray a quick prayer, and choose the soft answer.""",

    16: """Proverbs 16, verse 9 says, A man's heart deviseth his way: but the LORD directeth his steps. We make plans. That is not wrong. God gave us minds to think and plan. But the beautiful truth of this proverb is that God is the one who actually directs where we end up.

Thomas Watson wrote that this should give us great comfort. We do not have to carry the burden of figuring out our entire future. We plan wisely, we work diligently, and then we trust God with the outcome. He sees the whole picture. We only see a small piece.

Have you ever planned a trip and then something unexpected happened that changed everything? Maybe you got lost and discovered a beautiful place you never would have seen otherwise. That is often how God works. He takes our plans and redirects them for something better than we could have imagined.

As a family, let us hold our plans loosely. Let us make them prayerfully and then trust that God's direction is always better than our own. He knows the way, even when we do not.""",

    17: """A friend loveth at all times, and a brother is born for adversity. Proverbs chapter 17 gives us one of the most beautiful descriptions of friendship in all of Scripture.

What does it mean to love at all times? It means loving when it is easy and when it is hard. It means showing up when your friend is happy and when your friend is hurting. It means being loyal even when it costs you something.

John Bunyan, who spent twelve years in prison for preaching the gospel, knew what it meant to have faithful friends. While he was locked away, some friends abandoned him, but others stayed true. They visited him, cared for his family, and encouraged him. Those were friends who loved at all times.

And here is the wonderful truth: Jesus is the ultimate Friend who loves at all times. He loves us when we succeed and when we fail. He loves us in our joy and in our sorrow. He is the Brother born for adversity, who walks beside us through every trial.

Let us be that kind of friend to others, and let us thank God for the truest Friend we will ever have.""",

    18: """The name of the LORD is a strong tower: the righteous runneth into it, and is safe. What a mighty picture Proverbs 18, verse 10, gives us!

Imagine a great stone tower in the middle of a battlefield. The enemy is coming. Arrows are flying. But you run to the tower, you get inside, and the thick walls protect you completely. You are safe. That is what the name of the Lord is for us.

Thomas Brooks wrote that the name of the Lord includes everything He is: His power, His love, His faithfulness, His mercy, His wisdom. When we run to God, we are running to all of that. We are placing ourselves under the protection of the mightiest being in all of existence.

And notice that the verse says the righteous runneth into it. This is not a casual stroll. It is a running. It is urgent. When fear comes, when trouble strikes, when the world feels overwhelming, we run to God. Not to our phones, not to our worries, not to our own strength. We run to the strong tower.

As a family, let us make God our first refuge. When something scary happens, let us pray first. When anxiety knocks on the door, let us run together to the strong tower of the Lord.""",

    19: """Proverbs 19, verse 11 says, The discretion of a man deferreth his anger; and it is his glory to pass over a transgression. In other words: it takes real strength to be patient, and it is actually glorious to forgive.

The world tells us that strong people fight back, that real strength means standing your ground and never letting anyone get away with anything. But God says the opposite. Real strength is being able to hold your anger, to wait, to think before you react, and then to forgive.

Richard Baxter wrote that patience is one of the most difficult virtues because it goes against our natural instincts. When someone wrongs us, everything inside us screams, Fight back! But the Holy Spirit whispers, Be still. Trust Me. Forgive.

Forgiving does not mean pretending nothing happened. It means choosing not to hold it against the person. It means letting go of the anger and trusting God to make all things right in His time.

As a family, let us practice patience and forgiveness. When someone in our family makes a mistake or hurts our feelings, let us be slow to anger and quick to forgive. That is the way of wisdom.""",

    20: """Even a child is known by his doings, whether his work be pure, and whether it be right. That is Proverbs 20, verse 11. Children, listen closely: God is saying that even you, right now, at your age, are building a reputation by the things you do.

What kind of person do you want to be known as? Kind? Honest? Hardworking? Faithful? The choices you make today, even the small ones, are writing your story. When you tell the truth even when it is hard, you are becoming an honest person. When you share with your sibling even when you would rather keep everything for yourself, you are becoming a generous person.

Thomas Watson told parents that the seeds planted in childhood bloom in adulthood. The habits you form now, the character you build now, will stay with you for the rest of your life. That is both a responsibility and an opportunity.

And the good news is that you do not have to do this in your own strength. God is with you. His Holy Spirit helps you make wise choices. And your family is here to support you and cheer you on. Let us build good reputations together, as a family that is known for doing what is pure and right.""",

    21: """Every way of a man is right in his own eyes: but the LORD pondereth the hearts. Proverbs 21, verse 2. Have you ever noticed how easy it is to think you are right? We can always find a reason for why we did what we did. But God sees deeper than our reasons. He sees our hearts.

Jonathan Edwards taught that the difference between true religion and false religion is what is happening on the inside. You can do all the right things on the outside, going to church, saying your prayers, being polite, but if your heart is full of pride or selfishness, God knows.

This is not meant to scare us. It is meant to free us. Because when we stop pretending and come to God honestly, saying, Lord, my heart is not right, please change it, He does. He is the great heart-changer. He can take a proud heart and make it humble. He can take a selfish heart and fill it with love.

Let us be a family that cares about the inside as much as the outside. Let us ask God every day to examine our hearts and make them clean.""",

    22: """Train up a child in the way he should go: and when he is old, he will not depart from it. Proverbs 22, verse 6 is one of the most famous verses about parenting in all the Bible. But it is not just for parents. It is for the whole family.

Richard Baxter devoted much of his ministry to helping families understand this sacred responsibility. He believed that the training of children was the most important work on earth, because the soul of a child is an eternal soul. What is learned in the home echoes into eternity.

Training does not just mean teaching facts. It means living the faith in front of your children. It means praying together, reading Scripture together, showing kindness, asking for forgiveness, worshipping God as a family. Children learn more from what they see than from what they are told.

And children, this verse has a promise in it for you too: when you are old, you will not depart from it. The things you are learning now, the verses you are memorizing, the prayers you are praying, they are being planted deep in your heart. And one day, when you are grown, they will bear beautiful fruit.""",

    23: """My son, give me thine heart, and let thine eyes observe my ways. Proverbs 23, verse 26. Of all the things God could ask for, He asks for the one thing that is most precious: your heart.

God does not just want our good behavior. He does not just want our church attendance. He does not just want us to follow rules. He wants our hearts. He wants our love, our affection, our devotion, our trust. He wants all of us.

Thomas Brooks wrote that giving God your heart is not a one-time event. It is a daily practice. Every morning we wake up and say, Lord, here is my heart again. Today, it is Yours. Direct it, fill it, use it for Your glory. And every evening, we examine whether we truly gave Him our hearts that day, or whether we kept parts of it for ourselves.

As a family, let us give God our hearts tonight. Not just the easy parts, not just the parts we are proud of, but all of it. The fears, the doubts, the struggles, everything. He can handle it all, and He will fill us with more joy and peace than we ever thought possible.""",

    24: """For a just man falleth seven times, and riseth up again. Proverbs 24, verse 16. What a comforting truth! The wise and righteous person is not someone who never falls. It is someone who gets back up.

John Bunyan understood this deeply. His life was marked by falls and failures, by doubts and dark seasons. But every time he fell, he got back up by the grace of God. His famous book, The Pilgrim's Progress, is really the story of a man who falls down again and again but keeps walking toward the Celestial City.

You will make mistakes. We all do. There will be days when you lose your temper, when you say something you regret, when you give in to a temptation. But the measure of your character is not whether you fall. It is whether you get back up.

And here is the best part: you do not have to get up alone. God is there to lift you. He forgives the penitent heart. He strengthens the weary. He picks up His children when they stumble. So if you have fallen today, do not stay down. Rise up. Ask for forgiveness. And keep walking with God.""",

    25: """If thine enemy be hungry, give him bread to eat; and if he be thirsty, give him water to drink. Proverbs 25, verse 21. This is one of the hardest commands in all of Scripture. Be kind to your enemies. Give good things to people who have been unkind to you.

Everything in us wants to fight back. When someone is mean to us, we want to be mean right back. But God's way is radically different. God's way is to overcome evil with good. And this is not just a nice idea. It is what Jesus actually did. While we were still sinners, still His enemies, Christ died for us. He gave us the greatest gift while we were at our worst.

Jeremiah Burroughs wrote that returning good for evil is the most powerful testimony a Christian can give. It is so unnatural, so surprising, that people cannot help but notice. And when they ask why you are being kind to someone who hurt you, you can point them to Jesus.

This is hard. Really hard. But with God's help, our family can learn to do it. Let us start small. Let us pray for someone who has been unkind to us. And let us ask God for the strength to return their unkindness with love.""",

    26: """Seest thou a man wise in his own conceit? there is more hope of a fool than of him. Proverbs 26, verse 12 has a startling message: the person who thinks they already know everything is in worse shape than a fool!

Why? Because the fool at least has the possibility of learning. But the person who is puffed up with pride, who thinks they are always right, who refuses to listen to anyone else, that person has closed the door to growth.

Thomas Watson warned that self-conceit is one of the most dangerous spiritual diseases. It blinds us to our faults, makes us deaf to good advice, and slowly hardens our hearts. The Puritans called it the root of all other sins, because a proud heart says, I know better than God.

Humility is the opposite. Humility says, I do not know everything. I need help. I need God. I need the counsel of wise people in my life. Humility keeps the door open for God to teach us, shape us, and grow us.

As a family, let us practice humility. Let us be quick to listen, willing to admit when we are wrong, and always ready to learn something new.""",

    27: """Iron sharpeneth iron; so a man sharpeneth the countenance of his friend. Proverbs 27, verse 17. This is one of the most practical and powerful proverbs about relationships.

When a blacksmith sharpens a piece of iron, he does not use a feather pillow. He uses another piece of iron. There is friction. There are sparks. It is not always comfortable. But the result is a sharp, useful tool.

John Owen believed that one of the greatest gifts God gives us is faithful friends who are not afraid to speak truth into our lives. Friends who will say, I love you, but I think you are headed in the wrong direction. Those kinds of friends are rare and precious.

In our family, we sharpen each other every day. When Mom or Dad corrects you, that is sharpening. When a sibling challenges you to be better, that is sharpening. When we study the Bible together and ask hard questions, that is sharpening.

It is not always comfortable. Sometimes it produces sparks. But the result is that we all become stronger, wiser, and more useful for God's kingdom. Let us thank God for the people who sharpen us, and let us be willing to sharpen others in love.""",

    28: """The righteous are bold as a lion. Proverbs 28, verse 1. What a thrilling picture! Not timid as a mouse, but bold as a lion.

Where does this boldness come from? Not from ourselves. Not from being big and strong and brave on our own. It comes from knowing that God is with us. When you know that the Creator of the universe is on your side, you can face anything.

Thomas Brooks wrote that godly boldness is not recklessness. It is not showing off or being foolish. It is the quiet, steady courage that comes from trusting God completely. It is Daniel in the lion's den. It is David facing Goliath. It is a child standing up for what is right even when everyone else is doing the wrong thing.

You will face moments in your life when it takes courage to follow God. Maybe you will be the only one in your class who stands for truth. Maybe you will have to say no when everyone else says yes. In those moments, remember: the righteous are bold as a lion. God is with you, and He will never leave you.

Let us be a bold family. Not loud or arrogant, but quietly, steadfastly courageous in doing what is right.""",

    29: """Where there is no vision, the people perish: but he that keepeth the law, happy is he. Proverbs 29, verse 18. The word vision here does not mean seeing into the future. It means the Word of God. Where there is no Word of God to guide people, they wander and perish.

Richard Baxter grieved over families that neglected the Scriptures. He saw the terrible results: children growing up without direction, husbands and wives losing their way, communities falling apart. Without God's Word as our guide, we are like ships without a compass, drifting wherever the wind blows.

But the opposite is also true: the family that keeps God's law, that reads and obeys His Word, that family is happy. Not because life is always easy, but because they know where they are going. They have direction. They have purpose. They have a vision that comes from the eternal God.

That is what we are doing right now, together, as a family. By reading these proverbs, by studying God's Word, by praying and discussing and memorizing Scripture, we are keeping the vision alive. And God promises that this will lead to happiness, the deep kind, the lasting kind.""",

    30: """Every word of God is pure: he is a shield unto them that put their trust in him. Proverbs 30, verse 5. Every word. Not some words. Not most words. Every single word that comes from God is pure, trustworthy, and true.

Jonathan Edwards once wrote that the promises of God are backed by His full power and faithfulness. When God says something, it is as certain as if it has already happened. He cannot lie. He cannot fail. His Word is more solid than the ground beneath your feet.

And He is a shield. A shield protects you from arrows, from swords, from danger. When you trust in God's Word, it surrounds you and protects you from the lies of the enemy, from the confusion of the world, from the doubts that try to creep into your mind.

As a family, we can trust every word of God. When the Bible says He loves us, He loves us. When it says He will never leave us, He will never leave us. When it says He works all things for good, He works all things for good. Let us stand on these promises together, holding up the shield of faith as one family.""",

    31: """We have come to the end of our month in Proverbs, and Proverbs chapter 31 is a beautiful place to finish. This chapter paints a picture of a virtuous life, a life marked by hard work, generosity, strength, and above all, the fear of the Lord.

Favour is deceitful, and beauty is vain: but a woman that feareth the LORD, she shall be praised. This verse tells us what truly matters. Not outward appearance. Not popularity. Not how many likes you get or how fashionable your clothes are. What matters most is fearing the Lord, reverencing Him, loving Him, obeying Him.

Thomas Watson wrote that the fear of God is like a golden thread that runs through the entire fabric of a godly life. Take it out, and everything unravels. Keep it in, and everything holds together beautifully.

As we close this month of family devotions, let us carry this truth with us: the fear of the LORD is the beginning and the end and the middle of wisdom. It is the foundation of a life that pleases God. And by His grace, we have been building on that foundation together, one day at a time.

Thank you for walking through Proverbs with your family. May the Lord bless you, keep you, and fill your home with His wisdom and His peace.""",
}


# ===================================================================
# SCRIPT GENERATORS
# ===================================================================

def generate_family_script(ep):
    """Generate a complete Family Devotional script (~700-1000 words)."""
    day = ep["day"]
    ref, verse = PROVERBS_KEY_VERSES[day]
    _, puritan_insight = PURITAN_INSIGHTS[day]
    teaching = FAMILY_TEACHINGS.get(day, "")
    mv = ep["memoryVerse"]
    questions = ep["discussionQuestions"]

    lines = []
    lines.append(f'PURITAN GOLD -- Family Devotional, Day {day}')
    lines.append(f'"{ep["title"]}"')
    lines.append(f'Proverbs {day} -- {ep["subtitle"]}')
    lines.append("")
    lines.append("---")
    lines.append("")

    # Opening greeting (varied)
    greetings = [
        "Good evening, dear family. Welcome to tonight's family devotional from Puritan Gold.",
        "Hello, dear ones. Gather round for our family devotional time.",
        "Welcome, family. It is so good to be together in God's Word tonight.",
        "Good evening, beloved family. Let us draw near to God together.",
        "Hello and welcome to our family devotional. Come, let us sit together and listen to what God has to say.",
    ]
    lines.append(greetings[(day - 1) % len(greetings)])
    lines.append("")

    # Scripture reading
    lines.append(f"Tonight we are in Proverbs chapter {day}. Let me read our key passage:")
    lines.append("")
    lines.append(f'"{verse}"')
    lines.append(f"That is {ref}.")
    lines.append("")

    # Teaching
    if teaching:
        lines.append(teaching.strip())
    lines.append("")

    # Memory verse callout
    lines.append(f"Now, here is our memory verse for today. Let us say it together:")
    lines.append("")
    lines.append(f'"{mv}"')
    lines.append("")
    lines.append("Try to say it from memory before we go to bed tonight. And tomorrow, see if you can remember it still!")
    lines.append("")

    # Discussion questions
    lines.append("Here are some questions for our family to discuss:")
    lines.append("")
    for i, q in enumerate(questions, 1):
        lines.append(f"Number {i}: {q}")
        lines.append("")

    # Closing prayer
    prayers = [
        f"Let us close in prayer. Heavenly Father, thank You for gathering our family together in Your Word tonight. Thank You for the wisdom of Proverbs chapter {day}. Help us to live out what we have learned. Guard our hearts, guide our steps, and fill our home with Your love and peace. We pray in the name of Jesus Christ. Amen.",
        f"Let us pray together. Lord God, we thank You for this time as a family. Thank You for speaking to us through Proverbs chapter {day}. Plant these truths deep in our hearts, especially in the hearts of our children. Help us to walk in wisdom tomorrow and every day. In Jesus' name, Amen.",
        f"Let us bow our heads and pray. Dear Father in heaven, what a privilege it is to gather as a family around Your Word. We have heard from Proverbs chapter {day} tonight, and we ask You to write these truths on our hearts. Bless our family, protect our home, and lead us in the path of righteousness for Your name's sake. In Christ we pray, Amen.",
    ]
    lines.append(prayers[(day - 1) % len(prayers)])
    lines.append("")

    # Closing
    closings = [
        "Goodnight, dear ones. Walk in wisdom tomorrow.",
        "Sleep well tonight, knowing that God watches over your family.",
        "Until tomorrow, family. May the Lord bless you and keep you.",
        "Rest well tonight. God is faithful, and His wisdom is sure.",
        "Goodnight. Remember your memory verse, and carry it with you tomorrow.",
    ]
    lines.append(closings[(day - 1) % len(closings)])
    lines.append("")
    lines.append(f"[END OF FAMILY DEVOTIONAL, DAY {day}]")

    return "\n".join(lines)


def generate_school_script(ep):
    """Generate a complete School / Puritan Academy script (~2000-2800 words)."""
    lesson = ep["lesson"]
    unit = ep["unit"]
    title = ep["title"]
    review_qs = ep["reviewQuestions"]
    activity = ep["activity"]

    # Pick relevant Proverbs chapters based on lesson
    if lesson <= 5:
        prov_chapters = [1, 2, 3, 4, 9]
    elif lesson <= 10:
        prov_chapters = [4, 10, 11, 12, 16]
    elif lesson <= 15:
        prov_chapters = [13, 14, 15, 22, 24]
    else:
        prov_chapters = [21, 24, 28, 29, 31]

    primary_ch = prov_chapters[min(lesson - 1, len(prov_chapters) - 1) % len(prov_chapters)]
    ref, verse = PROVERBS_KEY_VERSES[primary_ch]
    author, insight = PURITAN_INSIGHTS[primary_ch]

    lines = []
    lines.append(f'PURITAN GOLD -- Puritan Academy')
    lines.append(f'{unit}')
    lines.append(f'Lesson {lesson}: "{title}"')
    lines.append(f'{ep["subtitle"]}')
    lines.append("")
    lines.append("---")
    lines.append("")

    # Introduction
    lines.append(f"Welcome to the Puritan Academy, a place where we study God's Word deeply and learn from the great teachers of the Christian faith. Today we begin Lesson {lesson}, which is part of {unit}. Our lesson title is: {title}.")
    lines.append("")

    # Scripture passage
    lines.append(f"Let us begin by reading from God's Word. Our primary text today comes from {ref}:")
    lines.append("")
    lines.append(f'"{verse}"')
    lines.append("")

    # Generate detailed teaching content based on the lesson
    lines.append(_get_school_teaching(lesson, title, unit, ref, verse, author, insight))
    lines.append("")

    # Historical Puritan context
    lines.append("--- Historical Context ---")
    lines.append("")
    lines.append(_get_school_historical(lesson, author, insight))
    lines.append("")

    # Application
    lines.append("--- Application ---")
    lines.append("")
    lines.append(_get_school_application(lesson, title))
    lines.append("")

    # Review questions
    lines.append("--- Review Questions ---")
    lines.append("")
    lines.append("Now let us review what we have learned today. Consider these questions carefully:")
    lines.append("")
    for i, q in enumerate(review_qs, 1):
        lines.append(f"Question {i}: {q}")
        lines.append("")

    # Activity
    lines.append("--- Activity ---")
    lines.append("")
    lines.append(f"Here is your activity for this lesson: {activity}")
    lines.append("")

    # Closing
    lines.append(f"That concludes Lesson {lesson} of {unit}. Well done. Continue to meditate on what you have learned, and may the Lord deepen your understanding as you apply these truths to your life. We will continue in our next lesson. Until then, walk in wisdom and in the fear of the Lord.")
    lines.append("")
    lines.append(f"[END OF SCHOOL LESSON {lesson}]")

    return "\n".join(lines)


def generate_together_script(ep):
    """Generate a complete Together / Couples Devotional script (~700-1000 words)."""
    day = ep["day"]
    ref, verse = PROVERBS_KEY_VERSES[day]
    puritan_author, puritan_insight = PURITAN_INSIGHTS[day]
    reflection = ep["reflectionPrompt"]
    prayer_focus = ep["prayerFocus"]

    lines = []
    lines.append(f'PURITAN GOLD -- Together: Couples Devotional, Day {day}')
    lines.append(f'"{ep["title"]}"')
    lines.append(f'Proverbs {day} -- {ep["subtitle"]}')
    lines.append("")
    lines.append("---")
    lines.append("")

    # Opening greeting (varied for husband and wife)
    greetings = [
        "Good evening, dear husband and wife. Welcome to tonight's couples devotional from Puritan Gold. Thank you for setting aside this time to draw near to God and to each other.",
        "Hello, beloved couple. It is a beautiful thing when husband and wife sit down together in God's Word. Welcome to your couples devotional time.",
        "Welcome, dear ones. Marriage is a gift from God, and so is this time together in His presence. Let us open our hearts to what He has for us tonight.",
        "Good evening. What a blessing it is to see a husband and wife seeking the Lord together. That is exactly what this time is for. Let us begin.",
        "Hello and welcome to your couples devotional. Whether you are sitting side by side on the couch or listening together at the end of a long day, God is here with you both.",
        "Good evening, dear couple. The Puritans believed that marriage was one of the greatest means of grace God provides. Let us enter into that grace together tonight.",
        "Welcome, husband and wife. There is something powerful about two hearts turning toward God at the same time. Let us do that now, together.",
    ]
    lines.append(greetings[(day - 1) % len(greetings)])
    lines.append("")

    # Scripture reading
    lines.append(f"Tonight we turn to Proverbs chapter {day}. Let me read our key passage for this evening:")
    lines.append("")
    lines.append(f'"{verse}"')
    lines.append(f"That is {ref}.")
    lines.append("")

    # Teaching connecting to marriage/couples
    _together_teachings = {
        1: f"The fear of the Lord is the beginning of knowledge. And it is also the beginning of a strong marriage. When both husband and wife stand in awe of God, something beautiful happens. You begin to see your spouse not merely as a partner, but as a fellow image-bearer of the living God. Your marriage becomes more than a contract; it becomes a covenant under the watchful, loving eye of the Almighty.\n\n{puritan_author} reminds us: {puritan_insight}\n\nWhen we place the fear of God at the center of our marriage, everything else finds its proper order. Our disagreements become smaller, our love becomes deeper, and our purpose becomes clearer. We are not just building a household. We are building a little outpost of the kingdom of God.",
        2: f"Solomon invites us to seek wisdom like hidden treasure. And what greater treasure hunt is there than seeking God together as a couple? When husband and wife open the Scriptures side by side, when they pray together, when they discuss what God is teaching them, they are digging for treasure that will never rust or fade.\n\n{puritan_author} wrote: {puritan_insight}\n\nMany couples invest heavily in their careers, their home, their children's activities, and yet neglect the greatest investment of all: seeking God together. Tonight, you are doing something counter-cultural and deeply valuable. You are choosing to seek eternal treasure side by side.",
        3: f"Trust in the Lord with all thine heart. For a married couple, this is both a personal and a shared command. There are moments in every marriage when the path ahead is unclear, when finances are tight, when health is uncertain, when the children bring worry. In those moments, the temptation is to lean on our own understanding, to try to figure it all out ourselves.\n\n{puritan_author} counseled: {puritan_insight}\n\nBut God calls us to something better. He calls us to trust Him together. When a husband and wife join hands and say, Lord, we do not know the way, but we trust You, that is one of the most powerful prayers in the world.",
        4: f"Keep thy heart with all diligence. In marriage, this takes on a special meaning. You are not only guarding your own heart, you are helping to guard your spouse's heart as well. What enters your home, what you watch, what you discuss, what attitudes you tolerate, all of these shape the spiritual atmosphere of your marriage.\n\n{puritan_author} taught: {puritan_insight}\n\nAs a couple, you can create a home where hearts are protected and nurtured. You can be each other's watchman, gently pointing out when something harmful is creeping in, and encouraging one another toward what is pure, lovely, and true.",
        5: f"Proverbs chapter five speaks directly to the marriage covenant. It calls us to faithfulness, to cherish the spouse of our youth, and to guard ourselves against anything that would draw us away from the sacred bond God has given us.\n\n{puritan_author} warned: {puritan_insight}\n\nFaithfulness in marriage is not just the absence of betrayal. It is the active, daily choice to love, to honor, to protect, and to cherish. It is choosing your spouse again and again, in every season, through every difficulty. The Puritans understood that marriage is a daily discipline of love, and that the path of faithfulness is the path of greatest joy.",
        6: f"The ant works diligently without needing anyone to tell her what to do. In marriage, this principle is transformative. A strong marriage is built not in dramatic moments but in the faithful, daily work of two people who love each other enough to serve without being asked.\n\n{puritan_author} taught: {puritan_insight}\n\nWhen a husband serves his wife without waiting to be asked, when a wife encourages her husband without expecting anything in return, when both partners contribute to the household with cheerful diligence, the home becomes a place of warmth and strength. Small acts of service, done consistently, build an unshakable foundation.",
        7: f"Solomon urges us to keep God's commandments close, like the apple of our eye. For a married couple, this means making God's Word the standard by which you measure everything in your marriage.\n\n{puritan_author} taught: {puritan_insight}\n\nWhen couples saturate their minds with Scripture, they build a defense against the temptations and deceptions that threaten every marriage. The world offers many counterfeit versions of love, intimacy, and fulfillment. But God's Word reveals the real thing. Hold fast to it together.",
        8: f"Wisdom was present at creation, and wisdom is present in your marriage. The same God who set the stars in their courses and formed the mountains and the seas, He is the one who brought you together. Your marriage is not an accident. It is part of His grand design.\n\n{puritan_author} observed: {puritan_insight}\n\nWhen we see our marriage through the lens of God's creative wisdom, it changes everything. The daily routines, the challenges, the joys, all of it is part of a larger story that God is writing. Take time tonight to marvel at the wisdom of God displayed in your relationship.",
        9: f"Proverbs nine sets before us two invitations: Wisdom's feast and Folly's feast. Every day in your marriage, you choose which table to sit at. The conversations you have, the way you resolve conflict, the priorities you set, these all determine which feast you are attending.\n\n{puritan_author} wrote: {puritan_insight}\n\nChoose Wisdom's feast together. Fill your marriage with the nourishment of God's Word, with prayer, with honest conversation, and with the sweetness of mutual encouragement. The feast of Folly may look attractive for a moment, but its end is bitterness.",
        10: f"The mouth of a righteous man is a well of life. In no relationship is this more true than in marriage. The words you speak to your spouse have enormous power, power to heal or to wound, to build up or to tear down, to bring life or to bring death.\n\n{puritan_author} taught: {puritan_insight}\n\nTonight, consider the words you have spoken to each other recently. Have they been a well of life? Have you expressed gratitude, admiration, encouragement? Or have critical, careless words crept in? Let us commit to speaking life to one another, for words of love spoken in marriage echo for a lifetime.",
        11: f"Integrity guides the upright. In marriage, integrity means being fully honest with your spouse, no hidden resentments, no secret struggles, no masks. It means being the same person in private that you are in public.\n\n{puritan_author} wrote: {puritan_insight}\n\nA marriage built on transparency is a marriage built on solid rock. When trust is deep, intimacy flourishes. When honesty is the norm, there is no room for the enemy to sow seeds of suspicion or division. Let us build marriages of radical integrity.",
        12: f"Proverbs tells us that the wise person loves correction. In marriage, this is one of the most difficult and most important lessons. Can you hear a hard truth from your spouse without becoming defensive? Can you receive feedback as a gift rather than an attack?\n\n{puritan_author} reminded us: {puritan_insight}\n\nThe couples who grow the most are those who can speak honestly with each other and receive correction with grace. This requires deep trust and deep humility. But the fruit is a marriage that is constantly growing, constantly being refined by the loving truth of a faithful partner.",
        13: f"The friends you keep as a couple will shape the kind of marriage you build. Proverbs warns that a companion of fools shall be destroyed, but he who walks with the wise shall be wise. This applies powerfully to marriage.\n\n{puritan_author} counseled: {puritan_insight}\n\nSurround your marriage with couples who love the Lord. Seek out mentors, older and wiser couples who have walked the road before you. Avoid relationships that undermine your commitment or tempt you away from faithfulness. The community around your marriage matters more than you know.",
        14: f"There is a way which seemeth right unto a man, but the end thereof are the ways of death. In marriage, it is easy to follow the culture's path instead of God's path. The world has many ideas about relationships, roles, and love, but not all of them align with Scripture.\n\n{puritan_author} warned: {puritan_insight}\n\nAs a couple, commit to testing your decisions against God's Word, not against popular opinion, not against what feels right in the moment, but against the timeless truth of Scripture. When you do, you build a marriage that will stand when the storms come.",
        15: f"A soft answer turneth away wrath. If there is one proverb that could transform every marriage on earth, it might be this one. Conflict is inevitable in marriage. Two sinners living under the same roof will disagree. But how you handle that conflict makes all the difference.\n\n{puritan_author} observed: {puritan_insight}\n\nThe gentle answer is not weakness. It is extraordinary strength. It is the strength to hold your tongue when every instinct says to fight back. It is the courage to lower your voice when everything in you wants to raise it. When a husband and wife commit to the gentle answer, their home becomes a place of peace.",
        16: f"We make plans, but the Lord directs our steps. Every couple has dreams and goals: where to live, how many children to have, what kind of life to build. These are good things. But Proverbs reminds us that God's plans are higher than ours.\n\n{puritan_author} wrote: {puritan_insight}\n\nSome of the most beautiful chapters in a marriage are the ones you never planned. The unexpected move, the surprise pregnancy, the closed door that led to an open one. Hold your plans loosely and trust the sovereign hand of God to write a story better than you could have imagined.",
        17: f"A friend loveth at all times. Your spouse should be your dearest, most trusted friend. Not just your partner, not just your co-parent, but your friend. The one who knows you fully and loves you still.\n\n{puritan_author} wrote: {puritan_insight}\n\nFriendship in marriage must be cultivated. It requires time together, laughter, shared experiences, honest conversations, and the willingness to be vulnerable. Do not let the busyness of life steal the friendship from your marriage. Protect it. Nurture it. It is one of God's greatest gifts.",
        18: f"The name of the Lord is a strong tower. When storms hit your marriage, and they will, where do you run? Do you run to anger, to distraction, to blame? Or do you run together to the strong tower of the Lord?\n\n{puritan_author} wrote: {puritan_insight}\n\nThe couples who endure are the ones who pray together in crisis. Not perfectly, not with eloquent words, but honestly. Lord, we are scared. Lord, we do not know what to do. Lord, be our strong tower. That kind of prayer, spoken together, is stronger than any storm.",
        19: f"Patience and forgiveness, the two great currencies of a lasting marriage. Proverbs tells us that it is a man's glory to overlook an offense. In marriage, you will have many opportunities to practice this.\n\n{puritan_author} taught: {puritan_insight}\n\nForgiveness in marriage is not pretending nothing happened. It is choosing not to hold the offense as a weapon. It is releasing your spouse from the debt of their mistake. And patience is the daily grace that keeps small irritations from becoming large resentments. Practice both, and your marriage will flourish.",
        20: f"Even a child is known by his doings. As a couple, you are building a legacy, a reputation, a family name. Not in the worldly sense, but in the eternal sense. What kind of legacy will your marriage leave?\n\n{puritan_author} reminded us: {puritan_insight}\n\nYour children are watching. Your neighbors are watching. The world is watching. A marriage that reflects the love of Christ is one of the most powerful witnesses on earth. Live in such a way that your marriage points others to the gospel.",
        21: f"God ponders the hearts. He sees past our outward displays of affection to the true motives underneath. In marriage, it is possible to go through the motions, to say the right words and do the right things, while our hearts are far away.\n\n{puritan_author} taught: {puritan_insight}\n\nTonight, let God search your heart. Are you serving your spouse out of genuine love, or out of obligation? Are you present in your marriage, or just physically there? God wants not just your actions but your heart. Give it to Him afresh tonight, and ask Him to fill it with true love for your spouse.",
        22: f"Train up a child in the way he should go. This is a shared calling for husband and wife. The spiritual formation of your children is not the job of the church alone, nor of one parent alone. It is the sacred work of a mother and father walking together in the fear of the Lord.\n\n{puritan_author} wrote: {puritan_insight}\n\nAre you aligned in how you are raising your children spiritually? Do you pray together for your children? Do you model for them what a godly marriage looks like? The greatest gift you can give your children is not a perfect home, but a home where two imperfect people love God and love each other.",
        23: f"My son, give me thine heart. God asks for the deepest part of us. And in marriage, we are called to give our hearts not only to God but also to each other. Not partially, not conditionally, but fully.\n\n{puritan_author} wrote: {puritan_insight}\n\nFull surrender, to God and to your spouse, is the pathway to the deepest joy. It is terrifying and beautiful all at once. When you hold nothing back, when you are fully known and fully loved, that is when marriage becomes what God intended it to be.",
        24: f"A just man falleth seven times, and riseth up again. In marriage, you will both fall. You will fail each other. You will say the wrong thing, make the wrong choice, act selfishly. The question is not whether you will fall, but whether you will help each other get back up.\n\n{puritan_author} wrote: {puritan_insight}\n\nA marriage of grace is one where failure is not the end of the story. It is where repentance is met with forgiveness, where falling is met with a helping hand, and where rising together becomes the rhythm of your life.",
        25: f"If thine enemy be hungry, give him bread to eat. This teaching about overcoming evil with good applies within marriage too. There are moments when your spouse may feel like the enemy, when hurt and anger make love feel impossible. In those moments, choose kindness anyway.\n\n{puritan_author} taught: {puritan_insight}\n\nThe love that overcomes is not a feeling. It is a decision. It is choosing to serve when you would rather withdraw. It is choosing to speak kindly when you want to lash out. This is the supernatural love that only the Holy Spirit can produce in us.",
        26: f"Seest thou a man wise in his own conceit? There is more hope of a fool than of him. Pride is the great destroyer of marriages. The pride that says I am always right. The pride that refuses to apologize. The pride that keeps score.\n\n{puritan_author} warned: {puritan_insight}\n\nHumility is the soil in which marital love grows. When a husband humbles himself before his wife, when a wife humbles herself before her husband, when both humble themselves before God, there is no conflict that cannot be resolved, no wound that cannot be healed.",
        27: f"Iron sharpeneth iron. Your spouse is God's chosen instrument to sharpen your character, to refine you, to make you more like Christ. This process is not always comfortable. The grinding of iron against iron produces heat and sparks. But the result is a sharper, stronger edge.\n\n{puritan_author} valued this truth: {puritan_insight}\n\nDo not resent the sharpening. Welcome it. When your spouse challenges you, when the friction of close relationship reveals your rough edges, thank God. He is using your marriage to make you who He created you to be.",
        28: f"The righteous are bold as a lion. As a couple, there are times when you must stand together with courage, when the world pushes against your values, when it costs something to follow Christ, when you must make unpopular decisions for the sake of your family.\n\n{puritan_author} wrote: {puritan_insight}\n\nDraw your courage from God, not from yourselves. A couple who prays together, who stands on the Word of God together, who faces the world side by side in the strength of the Lord, that couple is bold as a lion.",
        29: f"Where there is no vision, the people perish. Does your marriage have a vision? Not just a plan for next year's vacation, but a God-given vision for what your marriage and family are meant to be and do for His kingdom?\n\n{puritan_author} wrote: {puritan_insight}\n\nTake time to dream together under the authority of God's Word. What is He calling your marriage to? What ministries, what service, what legacy? A marriage with a shared, God-given vision is a marriage with purpose and power.",
        30: f"Every word of God is pure. As a couple, you need a foundation that does not shift, a truth that does not change, a promise that does not fail. That foundation is the Word of God. Everything else, feelings, finances, health, circumstances, will shift. But His Word stands forever.\n\n{puritan_author} treasured this truth: {puritan_insight}\n\nBuild your marriage on the bedrock of Scripture. Read it together. Discuss it. Memorize it. Let it be the final authority in every disagreement, every decision, every dream. A marriage built on God's Word is a marriage that cannot be shaken.",
        31: f"Favour is deceitful, and beauty is vain: but a woman that feareth the Lord, she shall be praised. As we close this month of devotions together, let us reflect on what truly matters. The world chases after charm and beauty, but these things fade. What lasts is the fear of the Lord.\n\n{puritan_author} wrote beautifully: {puritan_insight}\n\nA marriage rooted in the fear of God is a marriage that will bear fruit in every season. The spring of young love, the summer of raising children, the autumn of the empty nest, the winter of old age, through it all, the fear of the Lord sustains, strengthens, and sweetens every chapter of your story together.",
    }

    teaching = _together_teachings.get(day, f"As we reflect on Proverbs chapter {day} tonight, let us consider how this ancient wisdom speaks into our marriage. {puritan_author} once wrote: {puritan_insight}\n\nGod's Word is living and active, and it has something to say to every couple in every season. Let us listen carefully and apply what we hear.")
    lines.append(teaching)
    lines.append("")

    # Reflection prompt
    lines.append("--- Reflection ---")
    lines.append("")
    lines.append(f"Here is a question for you and your spouse to discuss together:")
    lines.append("")
    lines.append(f"{reflection}")
    lines.append("")
    lines.append("Take a few minutes to share honestly with each other. Listen without interrupting. Let this be a safe place for both of you to speak from the heart.")
    lines.append("")

    # Prayer focus
    lines.append("--- Prayer ---")
    lines.append("")
    lines.append(f"{prayer_focus}")
    lines.append("")
    lines.append("If you are able, hold hands as you pray together. There is something powerful about a husband and wife joining hands before the throne of grace.")
    lines.append("")

    # Closing (varied)
    closings = [
        f"Goodnight, dear couple. May the wisdom of Proverbs chapter {day} take root in your marriage and bear lasting fruit.",
        f"Sleep well tonight, knowing that God is watching over your marriage with the same faithfulness He has shown to His people for generations.",
        f"Until tomorrow, dear ones. May the Lord who brought you together continue to bind your hearts in His love.",
        f"Rest well in the Lord tonight. He is faithful to your marriage, and His mercies are new every morning.",
        f"Goodnight. Carry the truth of Proverbs chapter {day} into tomorrow, and let it shape the way you love each other.",
        f"May the God of all grace strengthen your marriage tonight and in the days to come. Goodnight, dear husband and wife.",
        f"The Lord bless you and keep you both. May He make His face shine upon your marriage. Goodnight.",
    ]
    lines.append(closings[(day - 1) % len(closings)])
    lines.append("")
    lines.append(f"[END OF COUPLES DEVOTIONAL, DAY {day}]")

    return "\n".join(lines)


def _get_school_teaching(lesson, title, unit, ref, verse, author, insight):
    """Return detailed teaching content for each school lesson."""
    teachings = {
        1: f"""Let us explore this foundational truth: the fear of the Lord is the beginning of knowledge. This is not merely an introduction to the book of Proverbs. It is the thesis statement of the entire wisdom literature of Scripture. Everything Solomon writes, every proverb, every comparison, every warning, flows from this single, magnificent truth.

But what is the fear of God? The Hebrew word is yirah, and it carries a range of meaning that includes awe, reverence, wonder, and yes, a holy trembling before the Almighty. It is not the fear of a slave cowering before a tyrant. It is the fear of a creature who suddenly perceives the infinite greatness, holiness, and majesty of the Creator.

Consider the vision of Isaiah in chapter six of his prophecy. When Isaiah saw the Lord high and lifted up, with the seraphim crying Holy, holy, holy, his response was not calm admiration. It was Woe is me! for I am undone. That is the fear of the Lord. It is the response of a finite being confronted with the infinite.

And yet, this fear is not separate from love. The Puritans understood this profoundly. Thomas Watson wrote that the fear of God and the love of God are like two wings of a bird; take away either one and the bird cannot fly. The fear of God without love produces cold, legalistic obedience. The love of God without fear produces sentimental, shallow affection. But together, they produce the robust, deep, joyful reverence that is the foundation of all true wisdom.

This matters for every area of life. How we study, how we work, how we treat others, how we make decisions, all of it flows from our posture before God. If we truly fear Him, we will want to know His will. We will want to obey His Word. We will want to honor Him in everything. And that is precisely what the book of Proverbs unfolds for us across its thirty-one chapters.

Let us also consider what the fear of God is not. It is not superstition. It is not a vague sense of religious anxiety. It is not the belief that God is watching to catch us doing something wrong so He can punish us. The fear of God is the joyful, trembling awareness that we live every moment in the presence of a God who is utterly holy and utterly loving. It transforms everything.""",

        2: f"""The Puritans were not merely theologians who wrote books. They were families who lived out their faith in the daily rhythms of ordinary life. And the fear of God was not an abstract concept for them. It shaped every part of their household.

Consider the typical Puritan family in seventeenth-century England or New England. The day began before dawn with private devotions. Each family member was expected to spend time alone with God before the family gathered for corporate worship. The father, as the spiritual head of the household, would lead the family in Bible reading, prayer, and singing of psalms.

Richard Baxter, in his monumental work The Christian Directory, laid out detailed guidance for how families should order their lives. He wrote that the household is a little church, and the father is its pastor. He urged parents to catechize their children daily, to explain the Scriptures to them in language they could understand, and to pray with them and for them without ceasing.

But it was not only about formal religious exercises. The Puritans saw all of life as sacred. Mealtimes were occasions for thanksgiving and spiritual conversation. Work was done as unto the Lord. Even recreation was to be enjoyed in moderation as a gift from God. The entire structure of daily life was designed to cultivate an awareness of God's presence.

Thomas Watson wrote about the importance of self-examination, encouraging believers to review their hearts every evening before retiring to bed. He compared this to a merchant checking his accounts at the close of business. How did I spend the currency of this day? Did I invest it wisely for the kingdom, or did I squander it on vanity?

The children in Puritan homes were not mere spectators in this spiritual life. They were active participants. From a young age, they were taught to memorize Scripture, to answer the questions of the catechism, and to pray their own prayers. The Westminster Shorter Catechism, which we will study in a later lesson, was specifically designed for the instruction of children. The Puritans believed that the most important education a child could receive was not in reading, writing, or arithmetic, but in the knowledge of God.

This is a challenging model for modern families. We live in a world of constant distraction, where screens compete for our attention and schedules are packed beyond reason. But the Puritan example reminds us that the most important thing we can do for our families is to make God the center of our home. Not in a rigid, joyless way, but in a warm, consistent, daily way that weaves the fear of God into the fabric of everyday life.""",

        3: f"""The book of Proverbs is built upon a fundamental contrast: the way of wisdom and the way of foolishness. These are not merely two options among many. They are the only two paths. Every person, every day, is walking on one of these two roads.

In Proverbs chapters one through nine, Solomon personifies both Wisdom and Folly as women calling out to passersby. Wisdom calls from the heights, from the city gates, from the public square. She offers life, understanding, riches, and honor to those who will listen. Folly also calls, but her invitation leads to destruction.

Let us examine the characteristics of the wise person as described in Proverbs. The wise person fears the Lord, as we have already discussed. But the wise person also receives instruction gladly, controls the tongue, works diligently, practices honesty, chooses friends carefully, and plans for the future. Wisdom is not merely intellectual. It is profoundly practical. It shows up in how you speak to your parents, how you do your chores, how you treat your siblings, how you manage your time.

The fool, by contrast, despises instruction, speaks carelessly, is lazy, is dishonest, chooses companions unwisely, and lives only for the moment. Notice that the fool is not necessarily stupid in the worldly sense. Many fools are very clever. The defining mark of the fool in Proverbs is not low intelligence but a refusal to fear God and submit to His wisdom.

This is why Proverbs 9:10 is so foundational: The fear of the LORD is the beginning of wisdom. The difference between the wise path and the foolish path is not education, talent, or opportunity. It is the fear of God. Without it, even the most gifted person walks in folly. With it, even the simplest person walks in wisdom.

The practical implications for students are enormous. How you respond to correction tells you which path you are on. How you use your words tells you which path you are on. Whether you do your work faithfully or cut corners tells you which path you are on. Every choice is a step on one road or the other.

Let us be students who choose the way of wisdom, who welcome correction, who work with diligence, and who build our lives on the solid foundation of the fear of the Lord.""",

        4: f"""John Bunyan is one of the most remarkable figures in all of Christian history. Born in 1628 to a poor tinker's family in Bedford, England, Bunyan received little formal education. Yet he would go on to write one of the most widely read books in the English language: The Pilgrim's Progress.

Bunyan's early life was marked by spiritual turmoil. He was, by his own account, a profane young man who loved swearing and had little regard for God. But God was at work even in those dark years. Through the influence of his wife, through the reading of Christian books, and especially through the preaching of the gospel, Bunyan came under deep conviction of sin.

His conversion was not a sudden, easy thing. It was a long, agonizing struggle. In his autobiography, Grace Abounding to the Chief of Sinners, Bunyan describes years of doubt, fear, and spiritual warfare. He was haunted by the question: Had he committed the unpardonable sin? Was there any hope for a wretch like him?

But at last, the gospel broke through. Bunyan came to understand that salvation is by grace alone, through faith alone, in Christ alone. The fear of God that filled his heart was not the terror of a condemned sinner but the reverent awe of a forgiven one. He had tasted the bitterness of sin and the sweetness of grace, and from that point forward, his life was devoted to proclaiming the gospel.

In 1660, Bunyan was arrested for preaching without a license. He was told he could go free if he promised to stop preaching. He refused. And so he spent twelve years in Bedford jail. It was there, in that cold stone cell, that he wrote much of The Pilgrim's Progress.

The Pilgrim's Progress tells the story of a man named Christian who flees from the City of Destruction and journeys toward the Celestial City. Along the way, he faces every kind of trial: the Slough of Despond, Vanity Fair, Doubting Castle, the Valley of the Shadow of Death. At every stage, it is the fear of God that keeps him on the path.

When Christian reaches the cross and his burden of sin falls from his back, he weeps tears of joy and gratitude. This is the fear of God in its purest form: the overwhelming awareness that I, a sinner, have been forgiven by a holy God. That awareness produces not terror but love, not despair but hope, not paralysis but bold obedience.

What can we learn from Bunyan? First, that God can use anyone, regardless of background or education, for His great purposes. Second, that the fear of God is forged in the furnace of trial. Third, that faithful obedience to God sometimes comes at a great cost but is always worth it. And fourth, that the greatest works of Christian literature often come from the deepest places of suffering.""",

        5: f"""The Westminster Shorter Catechism was published in 1647 by the Westminster Assembly, a gathering of theologians and ministers convened by the English Parliament to reform the Church of England. The Shorter Catechism was designed specifically for the instruction of children and new believers, and it remains one of the greatest summaries of Christian doctrine ever written.

It begins with the most fundamental question any human being can ask: What is the chief end of man? And the answer: Man's chief end is to glorify God, and to enjoy Him forever.

Let us unpack this magnificent statement. First, notice that it tells us our purpose. Every human being was created for a reason. We are not accidents. We are not random collections of atoms. We are creatures made in the image of God, and we exist for His glory.

What does it mean to glorify God? It means to make God's greatness known. It means to live in such a way that the reality of who God is shines through everything we do. When we tell the truth, we glorify the God of truth. When we show mercy, we glorify the God of mercy. When we work diligently, we glorify the God who works all things according to His purpose. Glorifying God is not limited to church services or prayer times. It encompasses all of life.

And what does it mean to enjoy God forever? This is the part that surprises many people. God is not merely to be obeyed and feared. He is to be enjoyed! The Puritans were sometimes wrongly caricatured as joyless, dour people who hated pleasure. Nothing could be further from the truth. The Puritans understood that God Himself is the greatest pleasure in the universe. Jonathan Edwards wrote that God is the fountain of all good, the source of all true happiness, and that to enjoy God is the highest delight a human soul can experience.

How does this connect to the fear of God? Because true enjoyment of God flows from a right understanding of who He is. We enjoy God most deeply when we know how great, how holy, how powerful, how loving He truly is. And that knowledge produces the reverent awe we have been calling the fear of God.

The fear of God is not the opposite of enjoying God. It is the gateway to enjoying God. When we fear Him rightly, we see His beauty more clearly. We appreciate His grace more deeply. We delight in His presence more fully. The catechism's answer holds together what many wrongly separate: reverence and delight, awe and joy, trembling and dancing.

This is why the Puritans placed such emphasis on catechizing their children. They wanted every child to know from the earliest possible age why they existed and what they were made for. A child who knows that their chief end is to glorify God and enjoy Him forever has a compass for life that will guide them through every decision, every trial, and every joy.""",

        6: f"""Proverbs 4:23 commands us: Keep thy heart with all diligence; for out of it are the issues of life. The heart, in biblical language, is not merely the seat of emotions. It is the command center of the whole person. It encompasses the mind, the will, the affections, the desires, everything that makes you who you are on the inside.

This is why Solomon says to guard it with ALL diligence, not some diligence, not casual attention, but the highest possible vigilance. Because out of the heart flow the issues of life. Your words, your actions, your habits, your character, they all spring from what is happening in your heart.

Thomas Watson understood this profoundly. In his writings, Watson taught that the heart is like a spring that feeds a river. If the spring is pure, the river will be clean. If the spring is polluted, every stream that flows from it will be contaminated. That is why external reformation without internal transformation is useless. You can change your behavior for a time through willpower, but unless the heart is changed, the old patterns will return.

The Puritans emphasized what they called heart-work, the daily discipline of examining, cleansing, and directing the heart. This involved several practices. First, self-examination: regularly asking yourself, What is the true condition of my heart? Am I harboring any sin? Are my affections set on God or on the world? Second, confession: bringing what you discover honestly before God and asking for His forgiveness. Third, meditation on Scripture: filling the heart with God's truth so that it displaces the lies and temptations of the enemy. Fourth, prayer: asking the Holy Spirit to do the work that we cannot do ourselves, to change our hearts from the inside out.

Watson also warned about the deceptiveness of the heart. Quoting Jeremiah 17:9, The heart is deceitful above all things, and desperately wicked: who can know it? he argued that we are often the last people to see the true condition of our own hearts. We rationalize. We minimize. We excuse. That is why we need the mirror of God's Word and the honest counsel of Christian friends to help us see ourselves clearly.

For the student, this has immediate practical implications. What are you feeding your heart? What books, what media, what conversations, what thoughts are you allowing to take root? The seeds planted today will determine the harvest of tomorrow. Guard your heart with all diligence, and everything else in your life will be affected for good.""",

        7: f"""The book of Proverbs has more to say about the tongue than almost any other topic. Consider just a few examples: A soft answer turneth away wrath, but grievous words stir up anger (15:1). The tongue of the wise useth knowledge aright, but the mouth of fools poureth out foolishness (15:2). A wholesome tongue is a tree of life, but perverseness therein is a breach in the spirit (15:4). Death and life are in the power of the tongue, and they that love it shall eat the fruit thereof (18:21).

Death and life are in the power of the tongue. That is an astonishing statement. Your words have the power to give life, to encourage, to heal, to strengthen, to comfort, to teach. And your words also have the power to kill, to wound, to discourage, to tear down, to destroy. Every time you open your mouth, you are exercising that power.

Jeremiah Burroughs, in his writings on Christian speech, taught that the tongue is the instrument that most clearly reveals the condition of the heart. Out of the abundance of the heart, the mouth speaketh, as our Lord Jesus taught in Matthew 12:34. If the heart is full of love, the tongue will speak words of kindness. If the heart is full of bitterness, the tongue will speak words of poison.

The Puritans took this so seriously that they practiced what we might call tongue disciplines. They would set guardrails on their speech. Before speaking, they would ask: Is this true? Is this kind? Is this necessary? Is this edifying? If the answer to any of these was no, they would hold their tongue.

This is particularly important for young people, who are often under great social pressure to speak carelessly. Gossip, sarcasm, complaining, boasting, and crude joking are so common in our culture that they seem normal. But Proverbs calls them marks of foolishness. The wise person controls the tongue and uses it as an instrument of blessing.

James chapter 3 compares the tongue to the rudder of a ship. A small rudder turns a great vessel. So it is with the tongue. A few words can change the course of a relationship, a family, a community. Let us learn to steer wisely.""",

        8: f"""The Puritans had a profound theology of work. They did not divide life into sacred and secular categories. For them, all honest labor done unto the Lord was sacred. The farmer in the field, the mother in the kitchen, the merchant in the marketplace, the student at the desk, all were serving God through their vocations.

Proverbs chapter 6 gives us the vivid image of the ant: Go to the ant, thou sluggard; consider her ways, and be wise: Which having no guide, overseer, or ruler, Provideth her meat in the summer, and gathereth her food in the harvest. The ant works without supervision, without compulsion, without complaint. She works because it is her nature to work, and because the future depends on today's labor.

Richard Baxter, in his Christian Directory, devoted extensive attention to the topic of diligence and vocation. He taught that every lawful calling is a calling from God, and that to be lazy in your calling is to sin against God. He wrote that the diligent Christian redeems the time, recognizing that every hour is a gift from God and an opportunity for service.

But Baxter was careful to distinguish between godly diligence and worldly ambition. Worldly ambition is driven by pride, greed, and the desire to be admired. Godly diligence is driven by gratitude, love for God, and the desire to be faithful stewards of the gifts and time God has entrusted to us. The motive makes all the difference.

Proverbs also warns severely about laziness. The sluggard's field is overgrown with thorns (24:30-34). The sluggard puts his hand in the dish but is too lazy to bring it to his mouth again (26:15). These vivid, almost humorous images are meant to shock us into self-examination. Am I being diligent in my studies, my work, my responsibilities? Or am I making excuses?

For the student, this means approaching your schoolwork as a spiritual discipline. When you study diligently, you are training yourself in the virtue of faithfulness. When you complete your assignments thoroughly, you are honoring God with the mind He gave you. When you push through difficulty instead of quitting, you are building the character that will serve you for the rest of your life.

The Puritan work ethic was not about earning God's favor. It was about expressing gratitude for God's grace. We work hard not to be saved, but because we are saved. And that makes all the difference.""",

        9: f"""Pride goeth before destruction, and an haughty spirit before a fall. Proverbs 16:18 is one of the most well-known proverbs in all of Scripture, and for good reason. Pride is the most destructive force in the human soul. It was pride that caused Lucifer to fall from heaven. It was pride that led Adam and Eve to eat the forbidden fruit. And it is pride that lies at the root of virtually every sin we commit.

Jonathan Edwards, in his treatise on religious affections, devoted considerable attention to the subject of humility. He argued that true humility is not merely thinking badly of yourself. It is thinking rightly of yourself in relation to God. The humble person does not deny their gifts or abilities. They simply recognize that everything they have comes from God and belongs to God.

Edwards identified several marks of true humility. The humble person is teachable, willing to receive correction and instruction. The humble person is grateful, recognizing that every good thing is an undeserved gift. The humble person is patient with others, because they know their own weaknesses. And the humble person is dependent on God, living each day in conscious reliance on divine grace.

The opposite of humility is what Proverbs calls being wise in your own eyes. This is the person who has stopped learning because they think they already know everything. It is the person who cannot receive correction because they think they are always right. It is the person who looks down on others because they think they are better.

Proverbs warns us repeatedly about this danger. The fear of the LORD is to hate evil: pride, and arrogancy, and the evil way, and the froward mouth, do I hate (8:13). Before destruction the heart of man is haughty, and before honour is humility (18:12). By humility and the fear of the LORD are riches, and honour, and life (22:4).

For the student, cultivating humility begins with a simple acknowledgment: I do not know everything. I need teachers. I need Scripture. I need the Holy Spirit. I need correction. That posture of openness is the soil in which wisdom grows. Without it, no amount of study will produce true knowledge.""",

        10: f"""Proverbs 11:3 tells us: The integrity of the upright shall guide them: but the perverseness of transgressors shall destroy them. Integrity is one of the most important qualities a person can possess, and the Puritans placed enormous emphasis on it.

Thomas Brooks, in his writings, described integrity as the quality of being whole, consistent, and undivided. The word integrity comes from the Latin integritas, meaning wholeness or completeness. A person of integrity is the same person in public and in private, in the light and in the dark, when being watched and when alone.

Brooks distinguished between outward morality and true integrity. Outward morality is doing the right thing because others are watching. True integrity is doing the right thing because God is watching and because your heart genuinely desires to honor Him. Many people appear moral on the surface but are hollow underneath. Integrity goes all the way through, like the letters in a stick of rock candy.

The Puritans tested their integrity through regular self-examination. They would ask themselves hard questions: Did I speak the truth today, even when it was inconvenient? Did I keep my promises? Did I do my work honestly? Did I treat others fairly? Was I the same person at home as I was in public?

This kind of rigorous honesty with oneself is uncomfortable. It requires facing our failures and weaknesses head-on. But it is absolutely essential for spiritual growth. Without integrity, our faith is merely a performance. With integrity, it is a life.

For the student, integrity shows up in many practical ways. Do you do your own work, or do you copy from others? Do you tell the truth to your parents, or do you shade the truth to avoid consequences? Do you keep your commitments, or do you back out when something more appealing comes along?

Brooks concluded his teaching on integrity with a beautiful image. He wrote that the person of integrity walks through life as a person walks through a garden at noon: fully visible, with nothing to hide, enjoying the warmth of the sun without any fear of exposure. That is the peace that comes from walking uprightly before God and man.""",

        11: f"""Proverbs 13:20 states a principle that is as powerful as it is simple: He that walketh with wise men shall be wise: but a companion of fools shall be destroyed. The people you walk with determine the person you become.

John Owen, the great Puritan theologian, wrote extensively about the importance of Christian fellowship. He taught that God designed the Christian life to be lived in community. We are not meant to walk alone. We need the encouragement, accountability, correction, and example of fellow believers to grow in our faith.

Owen pointed to several specific blessings of godly friendship. First, encouragement: a wise friend lifts you up when you are downcast and reminds you of God's promises when you forget them. Second, accountability: a wise friend asks the hard questions and holds you to your commitments. Third, correction: as Proverbs 27:6 says, Faithful are the wounds of a friend. A true friend loves you enough to tell you the truth, even when it hurts. Fourth, example: a wise friend models the kind of life you aspire to live.

But Owen also warned about the danger of ungodly companions. The influence of foolish friends is subtle and gradual. You do not suddenly become a different person because of your friends. Instead, their attitudes, habits, language, and values slowly seep into your own character, like water soaking into a sponge. Before you know it, you have adopted patterns of thinking and behaving that you never would have chosen on your own.

This is why Scripture is so emphatic about choosing companions wisely. Paul echoes this in 1 Corinthians 15:33: Be not deceived: evil communications corrupt good manners. And David declares in Psalm 1 that the blessed man does not walk in the counsel of the ungodly, nor stand in the way of sinners, nor sit in the seat of the scornful.

For the student, this is one of the most important lessons you will ever learn. Your friendships are not neutral. They are either helping you grow in wisdom or pulling you toward folly. Be intentional about who you spend your time with. Seek out companions who love the Lord, who are serious about their faith, and who will challenge you to become the person God is calling you to be.""",

        12: f"""Proverbs 24:3-4 says: Through wisdom is an house builded; and by understanding it is established: And by knowledge shall the chambers be filled with all precious and pleasant riches. The home is not merely a physical structure. It is a spiritual institution, and it requires wisdom to build it well.

Richard Baxter understood this deeply. His Christian Directory, published in 1673, contains one of the most comprehensive guides to Christian household management ever written. Baxter covered everything: the duties of husbands and wives, the training of children, the management of servants, the ordering of daily worship, the handling of finances, and the cultivation of hospitality.

For Baxter, the household was a little church. The father was its pastor, responsible for the spiritual welfare of every soul under his roof. He was to lead daily worship, catechize the children, discipline with firmness and love, and model godliness in every aspect of his life. The mother was the heart of the home, creating an atmosphere of warmth, order, and nurture.

Baxter insisted that family worship was non-negotiable. Every morning and every evening, the family was to gather for prayer, Scripture reading, and singing. He wrote that a household without family worship is like a body without a soul. It may have the outward form of a family, but it lacks the spiritual vitality that gives it true life.

The Puritan home was also a place of learning. Children were educated not only in reading and writing but in theology, history, and practical skills. Education was never separated from spiritual formation. Every lesson was an opportunity to see the wisdom and glory of God.

For modern families, the Puritan model offers both challenge and inspiration. We may not be able to replicate every aspect of their lifestyle. But we can embrace their core conviction: that the home is the most important institution on earth, and that building it with wisdom is the most significant work any family can undertake.""",

        13: f"""Proverbs contains extensive teaching about money, wealth, and stewardship. On one hand, it recognizes that diligent work often produces material prosperity: The hand of the diligent maketh rich (10:4). On the other hand, it warns severely about the dangers of loving money: He that trusteth in his riches shall fall (11:28). And it constantly points us toward generosity: There is that scattereth, and yet increaseth; and there is that withholdeth more than is meet, but it tendeth to poverty (11:24).

Thomas Watson addressed this tension beautifully in his treatise The Art of Divine Contentment. Watson taught that contentment is not a natural virtue. It is a supernatural grace that must be learned through the Holy Spirit. The contented soul is not the soul that has everything it wants. It is the soul that wants everything it has, because it recognizes that everything comes from the hand of a loving Father.

Watson identified several root causes of discontentment. The first is comparison: looking at what others have and feeling that we deserve the same or more. The second is ingratitude: failing to recognize and give thanks for what God has already given. The third is unbelief: doubting that God knows what is best for us and will provide what we truly need.

The antidote, Watson taught, is to fix our eyes on the riches we have in Christ. The believer who has been forgiven of sin, adopted into God's family, sealed with the Holy Spirit, and promised an eternal inheritance, that believer has more wealth than all the kings of the earth combined. When we truly grasp what we have in Christ, earthly possessions lose their power over us.

For the student, this means developing a healthy, biblical relationship with money from an early age. Learn to give generously. Learn to save wisely. Learn to be content with what God provides. And above all, learn to hold material things loosely, recognizing that they are temporary gifts from an eternal God.""",

        14: f"""Proverbs 24:10 says: If thou faint in the day of adversity, thy strength is small. Trials have a way of revealing what is truly inside us. When everything is going well, it is easy to appear strong and faithful. But when adversity strikes, the real condition of our character is exposed.

Jeremiah Burroughs understood this deeply. His book The Rare Jewel of Christian Contentment, published in 1648, is one of the most beloved Puritan works ever written. In it, Burroughs defines Christian contentment as that sweet, inward, quiet, gracious frame of spirit, which freely submits to and delights in God's wise and fatherly disposal in every condition.

Notice the richness of that definition. Contentment is sweet, not bitter. It is inward, not dependent on outward circumstances. It is quiet, not anxious or complaining. It is gracious, produced by the grace of God rather than human willpower. And it freely submits to God's disposal, recognizing that God is both wise and fatherly in everything He allows.

Burroughs taught that trials are God's classroom. They are not punishments but training exercises designed to strengthen our faith, deepen our dependence on God, and conform us more closely to the image of Christ. He compared the Christian under trial to a seaman: anyone can sail in calm waters, but it takes a skilled sailor to navigate a storm.

Burroughs also gave practical counsel for finding contentment in affliction. First, compare your afflictions to your sins. However great your suffering, it is less than you deserve. Second, compare your afflictions to your blessings. In every trial, God's mercies still far outweigh your troubles. Third, compare your afflictions to Christ's sufferings. Whatever you endure, Christ endured infinitely more for your sake. Fourth, look to the future. Present afflictions are light and momentary compared to the eternal weight of glory that awaits.

For the student, this lesson is about building spiritual resilience. You will face trials in your life, some small and some great. The question is not whether you will face adversity, but whether you will be ready for it. By cultivating the fear of God, filling your heart with Scripture, and learning from the example of saints like Burroughs, you can develop the kind of deep, unshakeable contentment that glorifies God in every circumstance.""",

        15: f"""As we reach the midpoint of our curriculum, let us step back and consider the golden thread that runs through everything we have studied so far: the fear of the Lord. In Unit 1, we established the fear of God as the foundation of all wisdom. In Unit 2, we examined how that fear shapes our character, our speech, our work, our humility, and our integrity. In Unit 3, we have explored how wisdom works itself out in friendships, home life, stewardship, and trials.

Now let us deepen our understanding with the help of Jonathan Edwards, perhaps the greatest theologian America has ever produced. Edwards's work A Treatise Concerning Religious Affections is a masterful exploration of what true piety looks like. Edwards was deeply concerned about the difference between genuine spiritual experience and counterfeit religion.

Edwards argued that true religion does not consist in mere head knowledge about God. Many people know facts about God without truly knowing God. True religion consists in the affections, that is, in the deep movements of the heart that are stirred by the beauty, holiness, and glory of God. These affections include love, joy, holy fear, gratitude, repentance, and desire for God.

But Edwards was also clear that not all religious affections are genuine. He gave twelve signs of truly gracious affections and twelve signs that were inconclusive. Among the true signs: genuine affections are rooted in the beauty of divine things themselves, not in self-interest. They produce a humble spirit. They are accompanied by a change in practice. And they bear lasting fruit.

This connects directly to our study of Proverbs. The fear of the Lord is not merely a concept to be understood but an affection to be experienced. It is the deep, heartfelt response of a soul that has truly perceived the greatness of God. And from that affection flows everything else: wisdom in speech, diligence in work, humility in spirit, integrity in character, and contentment in trial.

As you reflect on your journey through these lessons so far, ask yourself: Has my understanding of the fear of God moved from my head to my heart? Am I merely learning about wisdom, or am I being changed by it? These are the most important questions you can ask.""",

        16: f"""We turn now to one of the most important and sobering topics in the Christian life: the mortification of sin. The word mortification comes from the Latin mortificare, meaning to put to death. And that is precisely what John Owen, the great Puritan theologian, calls us to do with our sin.

Owen's classic work The Mortification of Sin was first published in 1656. Its central message can be summarized in one unforgettable sentence: Be killing sin, or sin will be killing you. There is no neutrality in this battle. Every day, you are either making progress against sin or sin is making progress against you.

Owen begins by establishing that mortification of sin is the duty of every believer, not just pastors or monks or spiritual elite. If ye through the Spirit do mortify the deeds of the body, ye shall live, Paul writes in Romans 8:13. This is addressed to all Christians. And notice that it is through the Spirit. We cannot mortify sin in our own strength. It is the work of the Holy Spirit in and through us.

Owen then lays out a detailed method for fighting sin. First, know your sin. Do not be vague about it. Identify the specific sins that trouble you most. What are your characteristic temptations? Where are you weakest? Second, feel the weight of sin. Do not treat it lightly. Consider what sin cost Christ. Consider what it does to your soul. Consider the grief it brings to the Holy Spirit. Third, strike at the root. Do not just deal with outward behaviors. Dig down to the underlying desires and idols that feed the sin. Fourth, fill the void. When you put a sin to death, you must fill that space with positive spiritual disciplines: prayer, Scripture meditation, worship, fellowship.

Owen also warned about several mistakes in the fight against sin. Some people try to mortify sin through willpower alone, gritting their teeth and trying harder. This always fails. Others try to deal with sin through distraction, simply avoiding the temptation without ever addressing the heart issue. This also fails. True mortification requires the power of the Holy Spirit working through the means of grace: Scripture, prayer, the sacraments, and the fellowship of believers.

Proverbs speaks to this topic throughout. The repeated warnings against sin, temptation, and folly are calls to vigilance. The wise person does not play with sin. They flee from it. They hate it. They put it to death. And they do so not in their own strength but in the strength of the Lord.""",

        17: f"""Richard Baxter's The Saints' Everlasting Rest is one of the masterworks of Puritan devotional literature. Written in 1650 while Baxter was gravely ill and believed he was dying, it is a sustained meditation on the glory of heaven and the practice of heavenly meditation as a means of grace.

Baxter's central argument is that Christians should spend a portion of every day meditating on the glory that awaits them. He called this the duty of heavenly meditation and believed it was one of the most neglected disciplines in the Christian life. We spend so much time thinking about earthly things, earthly problems, earthly pleasures, earthly worries, that we forget we are pilgrims headed for a destination of unimaginable beauty.

Baxter gave practical instructions for this discipline. He recommended setting aside half an hour each day for deliberate, structured meditation on heaven. He suggested choosing a quiet place, free from distraction. He counseled beginning with Scripture passages about heaven and glory, then allowing the mind and affections to dwell on the implications. What will it be like to see Christ face to face? What will it be like to be free from sin forever? What will it be like to worship God without distraction, without weariness, without end?

But Baxter was clear that meditation is not daydreaming. It requires effort. It requires concentration. And above all, it requires prayer. Meditation without prayer becomes mere fantasy. Prayer without meditation becomes empty words. But when the two are joined together, they create a powerful engine of spiritual transformation.

Baxter also connected this practice to the whole of the Christian life. The person who spends daily time contemplating the glory of heaven will naturally live differently on earth. Earthly temptations lose their power when your heart is set on heavenly treasure. Earthly trials become bearable when you remember they are light and momentary compared to the eternal weight of glory.

For the student, this lesson points to the vital importance of a consistent prayer life. Prayer is not optional. It is the lifeline that connects us to God. Without it, we drift. With it, we are anchored to the only foundation that will never move. Let us learn from Baxter to be people of prayer, people who lift our eyes above the daily grind and fix our gaze on the everlasting rest that awaits all who love the Lord.""",

        18: f"""The doctrine of perseverance, sometimes called the perseverance of the saints, teaches that those whom God has truly saved will be kept by His power and will persevere in faith to the end. This does not mean that Christians never stumble or struggle. It means that God will not allow His children to fall away permanently.

Proverbs 24:16 captures this beautifully: For a just man falleth seven times, and riseth up again: but the wicked shall fall into mischief. The righteous person falls. Let us not pretend otherwise. Christians sin. Christians fail. Christians go through seasons of doubt, darkness, and discouragement. But the righteous person rises again. And the power to rise comes not from within but from God.

Thomas Brooks addressed this doctrine with great pastoral tenderness. He knew that many believers were plagued by doubts about their salvation. Am I truly saved? What if I fall away? What if my faith is not real? Brooks answered these fears by pointing to the faithfulness of God. He wrote that our perseverance does not depend on the strength of our grip on God, but on the strength of God's grip on us.

Brooks pointed to numerous Scripture passages to support this doctrine. John 10:28-29: I give unto them eternal life; and they shall never perish, neither shall any man pluck them out of my hand. My Father, which gave them me, is greater than all; and no man is able to pluck them out of my Father's hand. Philippians 1:6: Being confident of this very thing, that he which hath begun a good work in you will perform it until the day of Jesus Christ.

But Brooks was also careful to warn against presumption. The doctrine of perseverance is not a license to sin carelessly. It is a comfort for the believer who is genuinely fighting the fight of faith and sometimes feels like they are losing. God's preservation does not mean we can coast. It means that when we fall, He picks us up. When we wander, He brings us back. When we are weak, He carries us.

For the student, this is a profoundly encouraging truth. Your relationship with God does not depend on your perfection. It depends on His faithfulness. You will fail. You will stumble. But if your faith is genuine, God will not let you go. He is the Good Shepherd who leaves the ninety-nine to find the one lost sheep. And He always finds it.""",

        19: f"""Proverbs chapter 31 is most famous for its description of the virtuous woman, but its lessons apply to all believers who desire to live faithfully. Let us examine the virtues celebrated in this remarkable passage.

Diligence: She seeketh wool, and flax, and worketh willingly with her hands (31:13). She riseth also while it is yet night, and giveth meat to her household (31:15). The Proverbs 31 person is not idle. They are active, productive, and purposeful in their use of time and talent.

Generosity: She stretcheth out her hand to the poor; yea, she reacheth forth her hands to the needy (31:20). Faithful living is never inward-looking only. It always reaches outward to those in need. The virtuous person is open-handed and compassionate.

Strength and dignity: Strength and honour are her clothing; and she shall rejoice in time to come (31:25). This is not physical strength but moral and spiritual strength, the inner fortitude that comes from trusting God. This person can laugh at the future because they know who holds the future.

Wisdom in speech: She openeth her mouth with wisdom; and in her tongue is the law of kindness (31:26). The tongue is governed by both wisdom and kindness, exactly the combination Proverbs has been urging throughout.

And then the climax: Favour is deceitful, and beauty is vain: but a woman that feareth the LORD, she shall be praised (31:30). After describing all these external virtues, Solomon takes us back to the foundation: the fear of the Lord. This is what gives all the other virtues their depth and authenticity. Without the fear of God, diligence becomes mere ambition. Generosity becomes mere show. Strength becomes mere self-reliance. But with the fear of God, every virtue is transformed into genuine godliness.

For the student, Proverbs 31 is not a checklist of impossible standards. It is a portrait of the kind of person that the fear of the Lord produces over a lifetime. You do not become this person overnight. You become this person by walking faithfully with God, one day at a time, one choice at a time, one act of obedience at a time.""",

        20: f"""We have arrived at the final lesson of the Puritan Academy, and it is time to look back over everything we have learned and to look forward to a life built on the foundation of wisdom.

In Unit 1, we established the foundation: the fear of the Lord. We learned that all wisdom begins with reverential awe before the holy, loving, almighty God. We explored how the Puritans lived this out in their daily lives. We studied the two paths of wisdom and foolishness. We met John Bunyan and traced his journey of faith. And we memorized the first question of the Westminster Shorter Catechism: the chief end of man is to glorify God and enjoy Him forever.

In Unit 2, we examined the Christian character. We learned about guarding the heart, the power of the tongue, the blessing of diligence, the necessity of humility, and the beauty of integrity. We heard from Thomas Watson, Jeremiah Burroughs, Richard Baxter, Jonathan Edwards, and Thomas Brooks, each of whom showed us what it looks like to cultivate godly character in the nitty-gritty of daily life.

In Unit 3, we explored walking in wisdom. We studied wise friendships, the ordering of the household, stewardship of money, endurance under trials, and the thread of the fear of God that runs through all of life. We learned from John Owen about the necessity of Christian fellowship, from Baxter about building a household for God's glory, from Watson about divine contentment, and from Burroughs about the rare jewel of contentment in affliction.

In Unit 4, we have addressed the faithful life: mortifying sin with John Owen, cultivating prayer with Richard Baxter, persevering by the grace of God with Thomas Brooks, living virtuously from Proverbs 31, and now drawing it all together.

The call of Proverbs, from beginning to end, is this: Fear God. Walk in wisdom. Live faithfully. These are not three separate things. They are one life, viewed from three angles. The person who fears God will naturally seek wisdom. The person who walks in wisdom will naturally live faithfully. And the person who lives faithfully will naturally deepen in the fear of God.

As you leave this course and step into the rest of your life, carry these truths with you. They are not merely academic lessons. They are a map for living. The Puritans called the Christian life a pilgrimage, a journey toward the Celestial City. And these truths, drawn from the ancient well of Proverbs and illuminated by the great teachers of the faith, are your provision for the journey.

Go forth in the fear of the Lord. Walk in the path of wisdom. Live faithfully for the glory of God. And may the Lord bless you and keep you, and make His face to shine upon you, now and forevermore."""
    }
    return teachings.get(lesson, f"Today we study {title}, continuing our exploration of {unit}. Let us consider the wisdom of Scripture and the insights of the Puritan fathers as we delve deeper into this rich topic.")


def _get_school_historical(lesson, author, insight):
    """Return historical Puritan context for each school lesson."""
    contexts = {
        1: f"The concept of the fear of God was central to Puritan theology. The Puritans who settled in both England and New England in the 1600s built their entire society around this principle. Their churches, their schools, their governments, and their homes were all structured to cultivate reverence for God. {insight}",
        2: f"The Puritan household was perhaps the most distinctive feature of Puritan culture. Unlike modern Western society, where religion is often confined to Sunday mornings, the Puritans made worship the organizing principle of daily life. {insight}",
        3: f"The Puritans were deeply influenced by the wisdom literature of the Old Testament. They saw Proverbs as a divinely inspired guide for practical living, and they preached and taught from it constantly. {insight}",
        4: f"John Bunyan lived from 1628 to 1688, during one of the most turbulent periods in English history. The English Civil War, the Commonwealth under Cromwell, and the Restoration of the monarchy all took place during his lifetime. {insight}",
        5: f"The Westminster Assembly met from 1643 to 1653 in Westminster Abbey, London. It consisted of 121 ministers, 30 laymen, and commissioners from Scotland. Their work produced the Westminster Confession of Faith, the Larger and Shorter Catechisms, and the Directory for Public Worship. {insight}",
        6: f"The Puritans used the term heart-work to describe the interior spiritual disciplines that they considered essential to genuine Christianity. This was not mere introspection; it was a disciplined practice of self-examination guided by Scripture. {insight}",
        7: f"The Puritans lived in a time before electronic communication, but they understood the power of speech just as well as we do today. Their sermons could last two hours or more, and they weighed every word carefully. {insight}",
        8: f"The Puritan work ethic has been widely studied by historians and sociologists. Max Weber famously argued that the Protestant work ethic was a key factor in the rise of modern capitalism. {insight}",
        9: f"Jonathan Edwards was born in 1703 in East Windsor, Connecticut. He entered Yale College at age thirteen and would go on to become the most brilliant theologian in American history. His sermon 'Sinners in the Hands of an Angry God' is the most famous sermon in American literature. {insight}",
        10: f"Thomas Brooks served as a chaplain in the English navy and later as a pastor in London. He lived through the Great Plague and the Great Fire of London. His most famous works include Precious Remedies Against Satan's Devices and The Unsearchable Riches of Christ. {insight}",
        11: f"John Owen served as chaplain to Oliver Cromwell and as Vice-Chancellor of Oxford University. He wrote over eighty works of theology and devotion. His depth of learning and his pastoral warmth make him one of the most beloved of all the Puritans. {insight}",
        12: f"Richard Baxter's Christian Directory is one of the longest works of practical theology ever written. Running to over a million words, it addresses virtually every aspect of the Christian life. Baxter himself served as the pastor of Kidderminster, where his ministry transformed the entire town. {insight}",
        13: f"Thomas Watson served as rector of St. Stephen Walbrook in London until he was ejected from his pulpit in 1662 by the Act of Uniformity, along with nearly two thousand other Puritan ministers. Despite this persecution, Watson continued to preach and write. {insight}",
        14: f"Jeremiah Burroughs was one of the most gentle and irenic of the Puritan ministers. His contemporaries called him a prince of peace. He died in 1646, just two years before his most famous book was published. {insight}",
        15: f"Jonathan Edwards led what became known as the Great Awakening in the 1730s and 1740s, a revival that swept through the American colonies and transformed the spiritual landscape of a nation. His careful theological analysis of revival remains influential to this day. {insight}",
        16: f"John Owen was perhaps the most formidable intellect among all the Puritans. He served under Cromwell, debated with kings, and wrote with a depth and precision that still challenges scholars today. Yet his writing on sin is deeply pastoral, born from his own experience of spiritual warfare. {insight}",
        17: f"Richard Baxter nearly died at the age of thirty-five. It was during this illness, when he believed death was imminent, that he began writing The Saints' Everlasting Rest. The book was written not as an academic exercise but as a personal preparation for eternity. {insight}",
        18: f"Thomas Brooks ministered through some of the most difficult years in English Puritan history. The Great Ejection of 1662, when two thousand ministers were removed from their pulpits, was a devastating blow to the Puritan movement. Brooks endured this persecution with remarkable grace and resilience. {insight}",
        19: f"Proverbs 31 has been the subject of intense study and debate throughout Christian history. The Puritans viewed it not as an impossible ideal but as an aspirational portrait of what the grace of God can produce in a human life. {insight}",
        20: f"The Puritan movement spanned roughly from the 1560s to the 1700s. During that time, it produced some of the greatest theologians, preachers, and writers in Christian history. Their legacy endures in the Reformed tradition, in the Baptist and Congregationalist churches, and in the broader evangelical movement. {insight}",
    }
    return contexts.get(lesson, insight)


def _get_school_application(lesson, title):
    """Return application content for each school lesson."""
    apps = {
        1: "Apply this today by pausing before your studies or any task and acknowledging God's greatness. Let the fear of the Lord shape how you approach every subject, every conversation, and every decision. True learning begins on your knees.",
        2: "Consider implementing one element of the Puritan household model in your own home this week. Perhaps begin with daily family worship, or start a habit of evening self-examination. Small changes, consistently practiced, transform households.",
        3: "For the rest of this week, keep a journal of your daily choices. At the end of each day, honestly assess: were my choices today on the path of wisdom or the path of foolishness? Bring your journal to God in prayer.",
        4: "Bunyan's example challenges us to be faithful even when it is costly. Is there an area in your life where following God might cost you something? A friendship, a habit, a comfort? Ask God for the courage to be faithful.",
        5: "Memorize the first question and answer of the Westminster Shorter Catechism. Then, throughout this week, test your decisions against this standard: does this choice help me glorify God and enjoy Him?",
        6: "This week, practice heart-examination. Each evening, spend five minutes asking God to search your heart. Write down what He reveals, confess what needs confessing, and thank Him for His cleansing grace.",
        7: "Set a challenge for yourself this week: before speaking, ask three questions. Is it true? Is it kind? Is it necessary? Keep track of how this practice changes your conversations.",
        8: "Choose one area of your life where you have been lazy or half-hearted. Commit to doing that task with full diligence for one week as unto the Lord. Notice how it affects your attitude and your sense of purpose.",
        9: "Identify one area where pride may be operating in your life. It might be academic pride, social pride, or spiritual pride. Confess it to God and ask for the grace of humility.",
        10: "Write down five commitments for living with greater integrity. Be specific. Post them where you will see them daily and review them each evening.",
        11: "Evaluate your closest friendships using the standard of Proverbs 13:20. Are they making you wiser or pulling you toward folly? Pray for wisdom about your friendships.",
        12: "Choose one practical way to strengthen the spiritual life of your household this week. It might be starting a family devotion, serving a family member, or initiating a meaningful conversation about faith.",
        13: "Practice contentment this week by writing a gratitude list each morning. List ten things God has given you. Then commit one act of generosity, giving something of value to someone in need.",
        14: "Recall a recent trial you have experienced. Write out how God sustained you through it and what you learned. Then read Jeremiah Burroughs' definition of contentment and ask God to develop it in you.",
        15: "Take time this week for extended personal reflection. Write a letter to yourself summarizing the three most important truths you have learned so far in this course and how they have begun to change you.",
        16: "Identify one specific sin you struggle with and develop a mortification plan based on John Owen's method: know it, feel its weight, strike at the root, fill the void with Scripture and prayer.",
        17: "Set aside fifteen minutes each day this week for focused prayer using the structure Richard Baxter recommends. Begin with Scripture, move into meditation, and conclude with earnest prayer.",
        18: "Read one chapter of The Pilgrim's Progress or another Puritan classic this week. Write a reflection on how the author's perseverance through trial inspires your own faith.",
        19: "Choose three virtues from Proverbs 31 and develop a practical plan for cultivating each one over the next month. Share your plan with someone who will hold you accountable.",
        20: "Write your Personal Wisdom Creed. Summarize the key truths from all four units, the commitments you are making, and the vision you have for your life going forward. Read it aloud as a declaration of faith.",
    }
    return apps.get(lesson, f"Take time this week to apply the lessons from {title} to your daily life. Write a reflection and discuss it with your family or study group.")


# ===================================================================
# MAIN -- Generate all scripts, audio, and update episodes.json
# ===================================================================
if __name__ == "__main__":
    os.makedirs(SCRIPTS_DIR, exist_ok=True)
    os.makedirs(AUDIO_DIR, exist_ok=True)

    episodes = load_episodes()
    episode_map = {e["id"]: e for e in episodes}

    # Define the work: (label, episode list, script generator, id_key for filenames)
    sections = [
        ("family",   FAMILY_EPISODES,   generate_family_script,   "day"),
        ("school",   SCHOOL_EPISODES,   generate_school_script,   "lesson"),
        ("together", TOGETHER_EPISODES, generate_together_script, "day"),
    ]

    total = len(FAMILY_EPISODES) + len(SCHOOL_EPISODES) + len(TOGETHER_EPISODES)
    print(f"=== Puritan Gold: Generating ALL content ===")
    print(f"  Family episodes:   {len(FAMILY_EPISODES)}  (IDs 101-131)")
    print(f"  School episodes:   {len(SCHOOL_EPISODES)}  (IDs 201-220)")
    print(f"  Together episodes: {len(TOGETHER_EPISODES)} (IDs 301-331)")
    print(f"  Total: {total} episodes")
    print(f"  Scripts dir: {SCRIPTS_DIR}")
    print(f"  Audio dir:   {AUDIO_DIR}")
    print()

    count = 0
    for label, ep_list, generator, id_key in sections:
        print(f"--- Generating {label.upper()} section ({len(ep_list)} episodes) ---")
        for ep in ep_list:
            ep_id = ep["id"]
            ep_num = ep[id_key]
            count += 1

            # Generate script text
            print(f"  [{count}/{total}] {label}_{ep_id} ('{ep['title']}') ... ", end="", flush=True)
            script_text = generator(ep)

            # Save script to file
            script_path = os.path.join(SCRIPTS_DIR, f"{label}_{ep_id}.txt")
            with open(script_path, "w") as f:
                f.write(script_text)
            print("script OK ... ", end="", flush=True)

            # Generate audio
            audio_filename = f"{label}_{ep_id}.mp3"
            audio_path = os.path.join(AUDIO_DIR, audio_filename)
            generate_audio(script_text, audio_path)
            print("audio OK ... ", end="", flush=True)

            # Get duration
            duration_str, duration_secs = get_mp3_duration(audio_path)
            print(f"duration {duration_str}")

            # Update or create episode entry in episodes.json
            if ep_id in episode_map:
                episode_map[ep_id]["file"] = f"audio/{audio_filename}"
                episode_map[ep_id]["duration"] = duration_str
            else:
                new_entry = {
                    "id": ep_id,
                    "title": ep["title"],
                    "subtitle": ep.get("subtitle", ""),
                    "description": ep.get("description", ""),
                    "file": f"audio/{audio_filename}",
                    "duration": duration_str,
                }
                # Copy section-specific fields
                if label == "family":
                    new_entry["section"] = "family"
                    new_entry["day"] = ep["day"]
                elif label == "school":
                    new_entry["section"] = "school"
                    new_entry["lesson"] = ep["lesson"]
                    new_entry["unit"] = ep.get("unit", "")
                elif label == "together":
                    new_entry["section"] = "together"
                    new_entry["day"] = ep["day"]
                episodes.append(new_entry)
                episode_map[ep_id] = new_entry

        print()

    # Save updated episodes.json
    # Rebuild list from map to include any new entries
    episodes = list(episode_map.values())
    save_episodes(episodes)
    print(f"=== Done! Generated {count} episodes. episodes.json updated. ===")
