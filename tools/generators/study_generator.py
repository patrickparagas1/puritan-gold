#!/usr/bin/env python3
"""
Study Devotional Script Generator for Puritan Gold.

Generates ~2100-word (~15-minute) study devotional scripts, designed for
verse-by-verse or passage-by-passage study series (e.g., April's Romans
series).

Script structure:
    1. Opening / Series context       (~150 words)
    2. Scripture reading              (~200 words)
    3. Key verse focus                (~150 words)
    4. Main exposition / teaching     (~1200 words)
    5. Application                    (~400 words)
    6. Closing prayer                 (~100 words)

Public API:
    generate_study_script(ep) -> str
"""

# ---------------------------------------------------------------------------
# Rotation pools
# ---------------------------------------------------------------------------

_OPENINGS = [
    (
        "Good evening, and welcome to our study devotional from Puritan "
        "Gold. We are continuing our journey through one of the most "
        "important books in all of Scripture. The Puritans treasured "
        "careful, verse-by-verse study, and tonight we follow in their "
        "footsteps."
    ),
    (
        "Welcome, friend. Tonight we open our Bibles again for another "
        "session of deep, prayerful study. The Puritans believed that "
        "the richest treasures of Scripture are found not on the surface "
        "but beneath it, by those willing to dig."
    ),
    (
        "Good evening. There is no shortcut to spiritual depth. It "
        "comes through sustained, careful engagement with God's Word. "
        "That is what we are doing together in this study series, and "
        "tonight we take the next step."
    ),
    (
        "Welcome to our study devotional. The Apostle Paul told Timothy "
        "to study to show himself approved unto God, a workman that "
        "needeth not to be ashamed. That is our aim tonight: to study "
        "with diligence and devotion."
    ),
    (
        "Good evening, student of the Word. Every time we open the "
        "Scriptures, we stand on holy ground. The God of the universe "
        "has spoken, and He invites us to listen, to understand, and "
        "to respond. Let us listen well tonight."
    ),
    (
        "Welcome. The practice of sustained Bible study is one of the "
        "greatest gifts a Christian can give themselves. Tonight we "
        "continue to build our understanding, one passage at a time, "
        "guided by the Holy Spirit and the wisdom of the Puritans."
    ),
    (
        "Good evening. Whether this is your first time joining our "
        "study series or you have been with us from the beginning, "
        "you are welcome. God's Word is inexhaustible, and there is "
        "always more to discover."
    ),
]

_KEY_VERSE_INTROS = [
    "Let us focus on one verse that captures the heart of tonight's passage.",
    "Within tonight's passage, one verse stands out as a key that unlocks the rest.",
    "The Puritans often identified a single verse as the hinge of a passage. Tonight, that verse is this:",
    "Let us zoom in on a verse that is central to everything we will study tonight.",
    "Here is the key verse for tonight's study. Let it anchor everything else we discuss.",
    "One verse in particular demands our attention tonight. Let us read it carefully.",
    "The Puritans called the key verse of a passage its 'doctrine text.' Tonight, ours is this:",
]

_EXPOSITION_TRANSITIONS = [
    "Now let us move into the exposition of this passage.",
    "With our key verse before us, let us examine the broader teaching.",
    "Let us unfold the meaning of this passage together.",
    "Now we turn to the substance of tonight's study.",
    "Having read the text, let us explore its meaning in depth.",
    "Let us now exposit this passage carefully, as the Puritans would have done.",
    "The text is before us. Let us dig into its riches.",
]

_APPLICATION_TRANSITIONS = [
    (
        "Now let us consider: how does this truth apply to our lives? "
        "The Puritans never separated doctrine from practice. Every "
        "truth they studied was immediately applied."
    ),
    (
        "Application is where truth meets life. Let us consider what "
        "this passage demands of us."
    ),
    (
        "Study without application is like a seed without soil. Let us "
        "now plant what we have learned in the ground of daily life."
    ),
    (
        "The Puritans asked three questions of every passage: What does "
        "it teach? What does it rebuke? What does it require? Let us "
        "ask those questions now."
    ),
    (
        "Knowledge puffs up, Paul warns, but love builds up. Let us "
        "ensure that what we have studied tonight leads not to pride "
        "but to faithful, loving obedience."
    ),
    (
        "What does this truth look like in the ordinary moments of "
        "your life? At work, at home, in your relationships? Let us "
        "make it concrete."
    ),
    (
        "The true test of understanding is application. If we have "
        "truly grasped tonight's passage, it will change the way we "
        "live tomorrow."
    ),
]

_CLOSING_PRAYERS = [
    (
        "Let us close in prayer. Lord God, thank You for the riches of "
        "Your Word. What we have studied tonight is more precious than "
        "gold. Help us to guard it, to meditate on it, and to live by "
        "it. Give us understanding that goes beyond the intellect and "
        "reaches the heart. In Jesus' name. Amen."
    ),
    (
        "Father, we have studied Your Word tonight, and we are grateful. "
        "We confess that we need Your Spirit to illumine what we have "
        "read. Seal these truths in our hearts. Let them shape our "
        "thinking, our praying, and our living. Through Christ our "
        "Lord. Amen."
    ),
    (
        "Lord, Your Word is a lamp to our feet and a light to our path. "
        "Thank You for lighting the way tonight. Help us to walk in "
        "the light we have received. May our study never be merely "
        "academic, but always personal and transformative. In Jesus' "
        "name. Amen."
    ),
    (
        "Almighty God, we have opened Your Word and found it to be "
        "living and active, sharper than any two-edged sword. Continue "
        "to cut away everything in us that does not reflect Christ. "
        "We submit to Your truth tonight. Amen."
    ),
    (
        "Heavenly Father, thank You for the privilege of studying Your "
        "Word. Thank You for the teachers of the past who have helped "
        "us understand it more deeply. Continue to grow us in knowledge "
        "and in grace. In the name of Christ. Amen."
    ),
    (
        "Lord, we close this study with hearts full of gratitude. You "
        "have spoken, and we have listened. Now help us to obey. Give "
        "us the courage and the strength to live out what we have "
        "learned. Through Jesus Christ. Amen."
    ),
    (
        "Father, as we close tonight's study, we acknowledge that "
        "apart from Your Spirit we cannot understand Your Word rightly. "
        "Thank You for opening our eyes tonight. Continue to teach us, "
        "day by day, passage by passage. In Christ. Amen."
    ),
]

_CLOSINGS = [
    "Until next time, keep studying. The Word of God will never run dry.",
    "Goodnight. May the truths you have studied tonight take deep root in your heart.",
    "Continue to meditate on tonight's passage. The more you return to it, the more it will reveal.",
    "Go in peace, student of the Word. God rewards those who diligently seek Him.",
    "Until our next study, walk in the truth you have received.",
    "Goodnight. Remember, the goal of study is not information but transformation.",
    "May the Lord bless your continued study of His Word. Until next time.",
]


# ---------------------------------------------------------------------------
# Public generator function
# ---------------------------------------------------------------------------

def generate_study_script(ep):
    """
    Generate a ~2100-word study devotional script.

    Parameters
    ----------
    ep : dict
        Episode data with keys:
            day, title, subtitle, series, scripture_ref, scripture_text,
            puritan_author, puritan_commentary, key_verse, key_verse_ref,
            teaching, application, prayer

    Returns
    -------
    str
        Complete study devotional script text ready for TTS.
    """
    day = ep["day"]
    idx = (day - 1) % 7
    series = ep.get("series", "")

    lines = []

    # --- Header ---
    lines.append(f"PURITAN GOLD -- Study Devotional, Day {day}")
    if series:
        lines.append(f"Series: {series}")
    lines.append(f'"{ep["title"]}"')
    lines.append(ep["subtitle"])
    lines.append("")
    lines.append("---")
    lines.append("")

    # --- 1. Opening / Series context (~150 words) ---
    lines.append(_OPENINGS[idx])
    lines.append("")

    if series:
        lines.append(
            f"We are studying the book of {series} together. Tonight's "
            f'lesson is titled "{ep["title"]}." Each session builds on '
            f"what came before, so if you have been following along, "
            f"you will see how tonight's passage connects to the larger "
            f"argument of the book."
        )
        lines.append("")

    # --- 2. Scripture reading (~200 words) ---
    lines.append("--- Scripture Reading ---")
    lines.append("")
    lines.append(
        f"Let us read our passage for tonight. It comes from "
        f"{ep['scripture_ref']}:"
    )
    lines.append("")
    lines.append(f'"{ep["scripture_text"]}"')
    lines.append("")
    lines.append(
        f"Read that passage again to yourself. Mark any words or phrases "
        f"that stand out. The Puritans read with a pen in hand, always "
        f"ready to note what God was showing them."
    )
    lines.append("")

    # --- 3. Key verse focus (~150 words) ---
    key_verse = ep.get("key_verse", "")
    key_verse_ref = ep.get("key_verse_ref", "")
    if key_verse:
        lines.append("--- Key Verse ---")
        lines.append("")
        lines.append(_KEY_VERSE_INTROS[idx])
        lines.append("")
        lines.append(f'"{key_verse}" -- {key_verse_ref}')
        lines.append("")
        lines.append(
            f"This verse is the lens through which we will examine the "
            f"rest of tonight's passage. Keep it in the front of your "
            f"mind as we proceed."
        )
        lines.append("")

    # --- 4. Main exposition / teaching (~1200 words) ---
    lines.append("--- Exposition ---")
    lines.append("")
    lines.append(_EXPOSITION_TRANSITIONS[idx])
    lines.append("")

    # Puritan commentary
    lines.append(
        f"{ep['puritan_author']} offers valuable commentary on this "
        f"passage. The Puritans were expositors of the highest order, "
        f"and their insights remain remarkably fresh."
    )
    lines.append("")

    puritan_commentary = ep.get("puritan_commentary", "").strip()
    if puritan_commentary:
        lines.append(puritan_commentary)
        lines.append("")

    teaching = ep.get("teaching", "").strip()
    if teaching:
        lines.append(teaching)
    else:
        lines.append(
            f"The passage before us in {ep['scripture_ref']} is rich with "
            f"meaning. Let us examine its key themes carefully."
        )
    lines.append("")

    # --- 5. Application (~400 words) ---
    lines.append("--- Application ---")
    lines.append("")
    lines.append(_APPLICATION_TRANSITIONS[idx])
    lines.append("")

    application = ep.get("application", "").strip()
    if application:
        lines.append(application)
    else:
        lines.append(
            f"Consider how the truths from {ep['scripture_ref']} apply "
            f"to your life right now. What is God calling you to believe "
            f"more deeply? What is He calling you to do differently?"
        )
    lines.append("")

    lines.append(
        "Write down one concrete action you will take this week in "
        "response to tonight's study. Do not let this truth remain "
        "theoretical. The Puritans measured the success of a sermon "
        "not by how much the hearer learned but by how much the "
        "hearer changed."
    )
    lines.append("")

    # --- 6. Closing prayer (~100 words) ---
    lines.append("--- Closing ---")
    lines.append("")

    custom_prayer = ep.get("prayer", "").strip()
    if custom_prayer:
        lines.append(custom_prayer)
    else:
        lines.append(_CLOSING_PRAYERS[idx])
    lines.append("")

    lines.append(_CLOSINGS[idx])
    lines.append("")
    lines.append(f"[END OF STUDY DEVOTIONAL, DAY {day}]")

    return "\n".join(lines)
