#!/usr/bin/env python3
"""
Personal Growth Devotional Script Generator for Puritan Gold.

Generates ~2100-word (~15-minute) personal growth scripts in one of three
rotating types:
    - "reading"     : Guided Puritan text walkthrough
    - "pastoral"    : Direct pastoral encouragement / challenge
    - "theological" : Doctrine deep-dive

Script structure:
    1. Opening / Invocation           (~150 words)
    2. Scripture reading              (~200 words)
    3. Main content                   (~1500 words) -- varies by type
    4. Reflection questions           (~150 words)
    5. Prayer / closing               (~100 words)

Public API:
    generate_personal_script(ep) -> str
"""

# ---------------------------------------------------------------------------
# Rotation pools -- shared across types
# ---------------------------------------------------------------------------

_OPENINGS_READING = [
    (
        "Welcome, friend. Tonight we take up a spiritual discipline that "
        "was at the very heart of the Puritan life: the slow, careful, "
        "prayerful reading of a great Christian text. We are not skimming. "
        "We are not rushing. We are walking through these pages the way "
        "the Puritans did, with a Bible in one hand and a prayer in our "
        "hearts."
    ),
    (
        "Good evening. One of the great losses of the modern church is "
        "the loss of slow reading. The Puritans read deeply, digesting "
        "every paragraph, pausing to pray, pausing to think. Tonight, "
        "we recover that practice as we walk through a treasured text "
        "together."
    ),
    (
        "Welcome to our guided reading. The book before us tonight has "
        "nourished Christians for centuries. We approach it not as critics "
        "but as students, not as experts but as hungry learners. Let us "
        "read together, slowly and prayerfully."
    ),
    (
        "Good evening. There is a reason the Puritans read so many books "
        "alongside their Bibles. They knew that God raises up teachers in "
        "every generation to illuminate His Word. Tonight we sit with one "
        "of those teachers and listen carefully."
    ),
    (
        "Welcome, dear listener. The practice of reading great Christian "
        "literature is a form of spiritual formation. It shapes how we "
        "think, how we pray, and how we see God. Tonight, let us be "
        "formed by what we read."
    ),
    (
        "Good evening. We are continuing our journey through one of the "
        "treasures of the Puritan library. These are not dusty old words. "
        "They are living truths that have the power to transform your "
        "walk with God."
    ),
    (
        "Welcome. Tonight we read together. Not quickly, not casually, "
        "but with the kind of attentive, worshipful reading that the "
        "Puritans practiced every day. Open your heart as we open this "
        "text."
    ),
]

_OPENINGS_PASTORAL = [
    (
        "Good evening, dear brother or sister. Tonight I speak to you "
        "not as a lecturer but as a pastor, as a fellow traveler on the "
        "road of faith. Wherever you are tonight, whatever burden you "
        "carry, you are not alone. God is near, and He has a word for "
        "you."
    ),
    (
        "Welcome, friend. There are nights when what we need most is not "
        "more information but more encouragement. Tonight is one of those "
        "nights. Let the Lord speak directly to your heart."
    ),
    (
        "Good evening. If you are weary tonight, you are in good company. "
        "The saints of old knew weariness well. And yet they also knew "
        "the God who gives strength to the faint. Let us draw near to "
        "Him together."
    ),
    (
        "Welcome. Tonight's devotional is personal. It is a word spoken "
        "from heart to heart, from one sinner saved by grace to another. "
        "Let us lay aside pretense and come before God as we truly are."
    ),
    (
        "Good evening. The Christian life is a marathon, not a sprint. "
        "And every marathon runner needs a voice along the way saying: "
        "keep going, you are not alone, the finish line is real. That "
        "is tonight's word for you."
    ),
    (
        "Welcome, dear listener. The Puritans were master pastors. They "
        "knew how to comfort the afflicted and afflict the comfortable. "
        "Tonight, in that tradition, we bring a word of pastoral "
        "encouragement and challenge."
    ),
    (
        "Good evening. Before we begin, take a deep breath. Release the "
        "tension of the day. You are in a safe place, a place where "
        "truth is spoken in love and where the gospel meets you exactly "
        "where you are."
    ),
]

_OPENINGS_THEOLOGICAL = [
    (
        "Good evening, student of the faith. Tonight we engage in one of "
        "the noblest pursuits of the Christian life: the study of "
        "doctrine. The Puritans did not shy away from deep theology. "
        "They embraced it, because they knew that right thinking about "
        "God leads to right living before God."
    ),
    (
        "Welcome. Doctrine is not a dry, academic exercise. It is the "
        "scaffolding on which the entire Christian life is built. Tonight "
        "we examine a foundational truth that, rightly understood, will "
        "transform the way you worship, pray, and live."
    ),
    (
        "Good evening. The Puritans were theologians of the highest "
        "order, but they were also the most practical of people. They "
        "knew that theology untethered from life is useless, and that "
        "life untethered from theology is dangerous. Tonight, we hold "
        "the two together."
    ),
    (
        "Welcome to our doctrine study. What we believe about God "
        "matters. It matters infinitely. Tonight we go deep into a "
        "truth that has anchored the church through centuries of "
        "storm and struggle."
    ),
    (
        "Good evening. A.W. Tozer said that what comes into our minds "
        "when we think about God is the most important thing about us. "
        "Tonight we think carefully, biblically, and reverently about "
        "a great doctrine of the faith."
    ),
    (
        "Welcome, friend. The Puritans called doctrine the bones of "
        "the body of divinity. Without strong bones, the body collapses. "
        "Tonight we strengthen those bones as we study a vital truth "
        "together."
    ),
    (
        "Good evening. There is a reason the church has always valued "
        "catechesis, the systematic teaching of Christian truth. Without "
        "it, faith becomes shallow and vulnerable. Tonight we go deeper."
    ),
]

_REFLECTION_INTROS = [
    "Let us pause and reflect. Consider these questions in the quiet of your heart.",
    "Before we close, take a few moments with these reflection questions.",
    "Here are some questions to carry with you into the coming days.",
    "The Puritans kept spiritual journals. Consider writing your answers to these questions.",
    "Let these questions search your heart. Answer honestly before God.",
    "Reflection is where truth becomes personal. Consider these questions carefully.",
    "Now let us turn the lens inward. What is God saying to you through tonight's study?",
]

_CLOSING_PRAYERS_READING = [
    (
        "Lord, thank You for the gift of this text and the truths it "
        "contains. Help me to absorb what I have read, not just with "
        "my mind but with my whole being. May these words bear fruit "
        "in my life. In Jesus' name. Amen."
    ),
    (
        "Father, I thank You for the teachers You have raised up "
        "throughout history. Thank You for preserving their words for "
        "my benefit. Help me to read more deeply, to think more "
        "carefully, and to live more faithfully. Amen."
    ),
]

_CLOSING_PRAYERS_PASTORAL = [
    (
        "Lord, You know the state of my heart tonight. You know my "
        "struggles, my fears, and my hopes. I bring them all to You. "
        "Strengthen me. Encourage me. Remind me that You are near and "
        "that You are good. In Christ's name. Amen."
    ),
    (
        "Father, thank You for meeting me here tonight. Thank You that "
        "You are a God who draws near to the weary and the broken. "
        "Renew my strength. Restore my joy. Help me to press on. "
        "In Jesus' name. Amen."
    ),
]

_CLOSING_PRAYERS_THEOLOGICAL = [
    (
        "Lord God, You are great beyond our comprehension, and yet You "
        "invite us to know You. Thank You for the truths we have studied "
        "tonight. Deepen my understanding and let sound doctrine produce "
        "a life of holiness and love. In Christ. Amen."
    ),
    (
        "Father, I thank You that You have revealed Yourself in Your "
        "Word. Help me to hold fast to the truth, to defend it with "
        "humility, and to live it with integrity. May my theology always "
        "lead me to worship. Amen."
    ),
]

_CLOSINGS = [
    "Goodnight, friend. Walk with God tomorrow.",
    "Until next time. May the Lord deepen your faith with every passing day.",
    "Rest in His grace tonight. Tomorrow is a new day of growth.",
    "Go in peace. The God who began a good work in you will bring it to completion.",
    "Goodnight. Remember: the same God who spoke to the Puritans speaks to you.",
    "May the Lord guard your mind and your heart tonight. Until we meet again.",
    "Press on, dear saint. The race is worth running, and the prize is Christ Himself.",
]


# ---------------------------------------------------------------------------
# Public generator function
# ---------------------------------------------------------------------------

def generate_personal_script(ep):
    """
    Generate a ~2100-word personal growth devotional script.

    Parameters
    ----------
    ep : dict
        Episode data with keys:
            day, title, subtitle, personal_type ("reading"|"pastoral"|"theological"),
            scripture_ref, scripture_text, puritan_author, puritan_work,
            main_content, reflection_questions (list of 3), prayer

    Returns
    -------
    str
        Complete personal growth script text ready for TTS.
    """
    day = ep["day"]
    idx = (day - 1) % 7
    ptype = ep.get("personal_type", "reading")

    lines = []

    # --- Header ---
    type_labels = {
        "reading": "Guided Puritan Reading",
        "pastoral": "Pastoral Encouragement",
        "theological": "Doctrine Deep-Dive",
    }
    type_label = type_labels.get(ptype, "Personal Growth")

    lines.append(f"PURITAN GOLD -- Personal Growth: {type_label}, Day {day}")
    lines.append(f'"{ep["title"]}"')
    lines.append(ep["subtitle"])
    lines.append("")
    lines.append("---")
    lines.append("")

    # --- 1. Opening / Invocation (~150 words) ---
    if ptype == "reading":
        lines.append(_OPENINGS_READING[idx])
    elif ptype == "pastoral":
        lines.append(_OPENINGS_PASTORAL[idx])
    else:
        lines.append(_OPENINGS_THEOLOGICAL[idx])
    lines.append("")

    # Author intro for reading/theological types
    if ptype in ("reading", "theological"):
        lines.append(
            f"Tonight we draw from the work of {ep['puritan_author']}, "
            f'specifically from "{ep["puritan_work"]}." This text has been '
            f"a source of spiritual nourishment for Christians across the "
            f"centuries, and it remains profoundly relevant today."
        )
        lines.append("")

    # --- 2. Scripture reading (~200 words) ---
    lines.append("--- Scripture ---")
    lines.append("")
    lines.append(
        f"Let us ground ourselves in God's Word before we go further. "
        f"Our passage tonight is {ep['scripture_ref']}:"
    )
    lines.append("")
    lines.append(f'"{ep["scripture_text"]}"')
    lines.append("")
    lines.append(
        f"Hold these words in your heart as we continue. They are the "
        f"foundation upon which everything else tonight is built."
    )
    lines.append("")

    # --- 3. Main content (~1500 words) ---
    if ptype == "reading":
        lines.append("--- Guided Reading ---")
    elif ptype == "pastoral":
        lines.append("--- Pastoral Word ---")
    else:
        lines.append("--- Doctrine Study ---")
    lines.append("")

    main_content = ep.get("main_content", "").strip()
    if main_content:
        lines.append(main_content)
    else:
        # Fallback content by type
        if ptype == "reading":
            lines.append(
                f"{ep['puritan_author']} writes with a depth and clarity "
                f"that is rare. As we walk through this passage together, "
                f"notice how every point is rooted in Scripture, how every "
                f"argument is shaped by a reverence for God's Word."
            )
        elif ptype == "pastoral":
            lines.append(
                f"The Christian life is not easy. It was never meant to "
                f"be. But it was always meant to be sustained by grace. "
                f"Tonight, let the grace of God wash over you afresh."
            )
        else:
            lines.append(
                f"The doctrine we study tonight is not peripheral. It is "
                f"central to the Christian faith. Without it, our "
                f"understanding of God and of salvation is incomplete."
            )
    lines.append("")

    # --- 4. Reflection questions (~150 words) ---
    lines.append("--- Reflection ---")
    lines.append("")
    lines.append(_REFLECTION_INTROS[idx])
    lines.append("")

    questions = ep.get("reflection_questions", [])
    for i, q in enumerate(questions, 1):
        lines.append(f"Question {i}: {q}")
        lines.append("")

    if questions:
        lines.append(
            "Do not rush past these questions. Sit with them. Journal "
            "about them if you can. The Puritans believed that truth "
            "must be digested, not merely tasted."
        )
        lines.append("")

    # --- 5. Prayer / closing (~100 words) ---
    lines.append("--- Closing Prayer ---")
    lines.append("")

    custom_prayer = ep.get("prayer", "").strip()
    if custom_prayer:
        lines.append(custom_prayer)
    else:
        # Type-specific default prayer
        if ptype == "reading":
            lines.append(_CLOSING_PRAYERS_READING[idx % 2])
        elif ptype == "pastoral":
            lines.append(_CLOSING_PRAYERS_PASTORAL[idx % 2])
        else:
            lines.append(_CLOSING_PRAYERS_THEOLOGICAL[idx % 2])
    lines.append("")

    lines.append(_CLOSINGS[idx])
    lines.append("")
    lines.append(f"[END OF PERSONAL GROWTH DEVOTIONAL, DAY {day}]")

    return "\n".join(lines)
