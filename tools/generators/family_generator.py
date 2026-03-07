#!/usr/bin/env python3
"""
Family Devotional Script Generator for Puritan Gold.

Generates ~1400-word (~10-minute) family devotional scripts with the following
structure:
    1. Welcome & opening prayer         (~100 words)
    2. Scripture reading                 (~150 words)
    3. Story / narrative teaching        (~400 words)
    4. Puritan wisdom spotlight          (~200 words)
    5. Family discussion questions       (3-4 questions)
    6. Memory verse + explanation        (~100 words)
    7. Activity suggestion               (~100 words)
    8. Closing prayer                    (~100 words)

Public API:
    generate_family_script(ep) -> str
"""

# ---------------------------------------------------------------------------
# Greeting / closing rotation pools
# ---------------------------------------------------------------------------

_GREETINGS = [
    (
        "Good evening, dear family. Welcome to tonight's family devotional "
        "from Puritan Gold. Thank you for gathering together around God's "
        "Word. Let us quiet our hearts and prepare to listen to what the "
        "Lord has for us."
    ),
    (
        "Hello, dear ones. How wonderful it is to sit together as a family "
        "and open the Scriptures. Welcome to Puritan Gold's family "
        "devotional. Let us begin with thankful hearts."
    ),
    (
        "Welcome, family. Whether you are gathered on the couch, around "
        "the dinner table, or riding in the car, God is here with you. "
        "Let us turn our attention to Him and see what treasure He has "
        "stored up for us tonight."
    ),
    (
        "Good evening, beloved family. The Puritans believed that the "
        "family altar was the most important altar in all the land. "
        "Tonight we gather at that altar together. Welcome to Puritan "
        "Gold."
    ),
    (
        "Hello and welcome to our family devotional. Come, young and old "
        "alike. God's Word has something for every member of this family "
        "tonight. Let us draw near to Him."
    ),
    (
        "Good evening, family. There is no place God loves to meet His "
        "people more than when families gather in His name. Welcome to "
        "Puritan Gold. Let us open our Bibles and our hearts."
    ),
    (
        "Welcome, dear family. Another day has passed, and God has been "
        "faithful through it all. Now let us close this day together by "
        "sitting at the feet of Jesus and hearing His Word."
    ),
]

_OPENING_PRAYERS = [
    (
        "Let us begin with prayer. Heavenly Father, we thank You for "
        "this family. We thank You for bringing us safely through another "
        "day. Now we ask that You would open our eyes to see wonderful "
        "things in Your Word. Speak to each heart gathered here, from "
        "the oldest to the youngest. In Jesus' name we pray. Amen."
    ),
    (
        "Let us pray together. Lord God, we come before You as a family, "
        "grateful for Your love and Your provision. We ask that You would "
        "quiet our minds and soften our hearts as we hear from You tonight. "
        "Help us to understand, to remember, and to obey what You teach us. "
        "In Christ's name, Amen."
    ),
    (
        "Let us bow our heads. Dear Father in heaven, what a privilege it "
        "is to gather as a family in Your presence. We need Your wisdom "
        "tonight. We need Your guidance. Open our ears to hear, our minds "
        "to understand, and our hearts to receive. We pray in the precious "
        "name of Jesus. Amen."
    ),
    (
        "Let us come before the Lord. Gracious God, thank You for the gift "
        "of family. Thank You that we can come to You together. We pray "
        "that You would teach us from Your Word this evening. Let every "
        "word sink deep into our hearts. We love You, Lord. In Jesus' "
        "name, Amen."
    ),
    (
        "Shall we pray? Our Father, we gather tonight hungry for Your "
        "truth. We know that man does not live by bread alone, but by "
        "every word that comes from Your mouth. Feed us now, Lord. Bless "
        "our family time together. In the name of Christ we pray. Amen."
    ),
    (
        "Let us begin in prayer. Lord Jesus, You said that where two or "
        "three are gathered in Your name, there You are in the midst of "
        "them. We claim that promise tonight as a family. Be here with us. "
        "Teach us. Shape us. We pray in Your holy name. Amen."
    ),
    (
        "Let us pray. Almighty God, You are the giver of every good gift, "
        "and one of the greatest gifts You have given us is this family. "
        "We dedicate this time to You. Help us to listen well and to grow "
        "in wisdom together. Through Jesus Christ our Lord. Amen."
    ),
]

_SCRIPTURE_INTROS = [
    "Tonight we open our Bibles to {ref}. Listen carefully as I read our passage:",
    "Our Scripture reading this evening comes from {ref}. Let us hear the Word of the Lord:",
    "Let us turn together to {ref}. Follow along in your Bible if you have one:",
    "The Word of God is a lamp to our feet and a light to our path. Tonight that light shines from {ref}:",
    "God has preserved His Word for thousands of years so that families like ours could hear it tonight. Let us read from {ref}:",
    "Every word of Scripture is breathed out by God. Tonight we receive His breath from {ref}:",
    "Our passage tonight is {ref}. Listen with expectant hearts:",
]

_PURITAN_TRANSITIONS = [
    "Now let us hear from one of the great Puritan teachers of the faith.",
    "The Puritans were men and women who treasured God's Word above all else. Let us hear from one of them now.",
    "For centuries, faithful Christians have reflected on passages like this one. Let us hear from a trusted voice of the past.",
    "The wisdom of the Puritans remains as fresh today as when it was first written. Listen to this insight.",
    "There is much we can learn from those who walked with God before us. Consider these words.",
    "One of the great blessings of the Christian tradition is that we stand on the shoulders of faithful saints who came before us.",
    "Let us sit at the feet of a Puritan teacher and learn something that will deepen our understanding.",
]

_DISCUSSION_INTROS = [
    "Now it is time for our family discussion. Here are some questions to talk about together. Take your time with each one.",
    "Let us pause and talk as a family. Here are tonight's discussion questions. Everyone gets a turn to share.",
    "Discussion time. These questions are for every member of the family, young and old alike.",
    "Here are some questions for us to think about and discuss together. There are no wrong answers here, just honest hearts.",
    "Family, let us talk about what we have learned. Consider these questions together.",
    "Now we get to the best part: talking about God's Word together as a family. Here are tonight's questions.",
    "Let us discuss what we have heard. Parents, encourage even the youngest to share what they are thinking.",
]

_ACTIVITY_INTROS = [
    "Here is a family activity you can do this week to help these truths take root:",
    "To make tonight's lesson come alive, try this activity together as a family:",
    "The Puritans believed that truth must be practiced, not just heard. Here is something you can do together:",
    "Here is a hands-on way to remember what we have learned tonight:",
    "Learning sticks better when we do something with it. Try this activity as a family:",
    "Here is a practical way to live out tonight's devotional:",
    "Before we close, here is a family challenge for the days ahead:",
]

_CLOSING_PRAYERS = [
    (
        "Let us close in prayer. Heavenly Father, thank You for gathering "
        "our family together in Your Word tonight. Thank You for the "
        "truth we have heard from {scripture_ref}. Help us to live out "
        "what we have learned. Guard our hearts, guide our steps, and "
        "fill our home with Your love and peace. We pray in the name of "
        "Jesus Christ. Amen."
    ),
    (
        "Let us pray together. Lord God, we thank You for this time as a "
        "family. Thank You for speaking to us through Your Word. Plant "
        "these truths deep in our hearts, especially in the hearts of "
        "our children. Help us to walk in wisdom tomorrow and every day. "
        "In Jesus' name, Amen."
    ),
    (
        "Let us bow our heads and pray. Dear Father in heaven, what a "
        "privilege it is to gather as a family around Your Word. We ask "
        "You to write these truths on our hearts. Bless our family, "
        "protect our home, and lead us in the path of righteousness for "
        "Your name's sake. In Christ we pray. Amen."
    ),
    (
        "Father, we have heard Your Word tonight, and we are grateful. "
        "We confess that we cannot live it out in our own strength. Fill "
        "us with Your Spirit. Give us wisdom for tomorrow, patience with "
        "one another, and a deep love for You. Keep our family close to "
        "You always. In Jesus' name. Amen."
    ),
    (
        "Lord, as we close tonight's devotional, we place our family in "
        "Your hands. Watch over us as we sleep. Guard our dreams. Prepare "
        "our hearts for tomorrow. May the truths from {scripture_ref} "
        "follow us into the new day. We love You, Lord. Amen."
    ),
    (
        "Gracious God, thank You for meeting with our family tonight. "
        "Your Word never returns void, and we trust that what we have "
        "heard will bear fruit in each of our lives. Strengthen our "
        "family bonds, deepen our faith, and make us a light in this "
        "world. Through Jesus Christ our Lord. Amen."
    ),
    (
        "Heavenly Father, we end where we began, in gratitude. Thank You "
        "for Your Word, for this family, and for the hope we have in "
        "Christ. May tonight's lesson from {scripture_ref} shape the way "
        "we live, the way we speak, and the way we love one another. "
        "Amen and amen."
    ),
]

_CLOSINGS = [
    "Goodnight, dear ones. Walk in wisdom tomorrow.",
    "Sleep well tonight, knowing that God watches over your family.",
    "Until tomorrow, family. May the Lord bless you and keep you.",
    "Rest well tonight. God is faithful, and His wisdom is sure.",
    "Goodnight. Remember your memory verse, and carry it with you tomorrow.",
    "May the peace of God guard your hearts and minds tonight. Goodnight, family.",
    "Until next time, dear family. The Lord goes before you. Walk with Him.",
]


# ---------------------------------------------------------------------------
# Public generator function
# ---------------------------------------------------------------------------

def generate_family_script(ep):
    """
    Generate a ~1400-word family devotional script.

    Parameters
    ----------
    ep : dict
        Episode data with keys:
            day, title, subtitle, scripture_ref, scripture_text,
            puritan_author, puritan_work, puritan_quote, teaching,
            memory_verse, memory_verse_ref, discussion_questions (list),
            activity, prayer_theme

    Returns
    -------
    str
        The complete devotional script text ready for TTS.
    """
    day = ep["day"]
    idx = (day - 1) % 7

    lines = []

    # --- Header ---
    lines.append(f"PURITAN GOLD -- Family Devotional, Day {day}")
    lines.append(f'"{ep["title"]}"')
    lines.append(ep["subtitle"])
    lines.append("")
    lines.append("---")
    lines.append("")

    # --- 1. Welcome & opening prayer (~100 words) ---
    lines.append(_GREETINGS[idx])
    lines.append("")
    lines.append(_OPENING_PRAYERS[idx])
    lines.append("")

    # --- 2. Scripture reading (~150 words) ---
    intro = _SCRIPTURE_INTROS[idx].format(ref=ep["scripture_ref"])
    lines.append(intro)
    lines.append("")
    lines.append(f'"{ep["scripture_text"]}"')
    lines.append("")
    lines.append(
        f"That is {ep['scripture_ref']}. Let those words settle in your "
        f"heart for a moment before we continue."
    )
    lines.append("")

    # --- 3. Story / narrative teaching (~400 words) ---
    lines.append("--- Teaching ---")
    lines.append("")
    teaching = ep.get("teaching", "").strip()
    if teaching:
        lines.append(teaching)
    else:
        lines.append(
            f"Tonight's passage speaks powerfully to our family. "
            f"Let us consider what God is saying to us through these words."
        )
    lines.append("")

    # --- 4. Puritan wisdom spotlight (~200 words) ---
    lines.append("--- Puritan Wisdom ---")
    lines.append("")
    lines.append(_PURITAN_TRANSITIONS[idx])
    lines.append("")
    lines.append(
        f'{ep["puritan_author"]}, in his work "{ep["puritan_work"]}," '
        f"wrote these words:"
    )
    lines.append("")
    lines.append(f'"{ep["puritan_quote"]}"')
    lines.append("")
    lines.append(
        f"What {ep['puritan_author']} is reminding us is that the truths "
        f"we have read tonight in {ep['scripture_ref']} are not new. They "
        f"have been treasured by faithful Christians for centuries. "
        f"And they are just as true and just as needed in our family today "
        f"as they were hundreds of years ago. Let us take these words to "
        f"heart and let them shape the way we live together as a family."
    )
    lines.append("")

    # --- 5. Family discussion (~150 words) ---
    lines.append("--- Family Discussion ---")
    lines.append("")
    lines.append(_DISCUSSION_INTROS[idx])
    lines.append("")
    questions = ep.get("discussion_questions", [])
    for i, q in enumerate(questions, 1):
        lines.append(f"Question {i}: {q}")
        lines.append("")
    if questions:
        lines.append(
            "Take a few minutes to talk about these questions together. "
            "Let everyone share, and listen to one another with patience "
            "and love."
        )
        lines.append("")

    # --- 6. Memory verse + explanation (~100 words) ---
    lines.append("--- Memory Verse ---")
    lines.append("")
    lines.append(
        f"Now, here is our memory verse for today. Let us say it together:"
    )
    lines.append("")
    lines.append(f'"{ep["memory_verse"]}" -- {ep["memory_verse_ref"]}')
    lines.append("")
    lines.append(
        "Try to say it out loud three times right now. Then, before bed "
        "tonight, see if you can say it from memory. Tomorrow morning, "
        "try again. The more we hide God's Word in our hearts, the more "
        "it will guide us when we need it most."
    )
    lines.append("")

    # --- 7. Activity suggestion (~100 words) ---
    lines.append("--- Family Activity ---")
    lines.append("")
    lines.append(_ACTIVITY_INTROS[idx])
    lines.append("")
    activity = ep.get("activity", "").strip()
    if activity:
        lines.append(activity)
    else:
        lines.append(
            "As a family, take turns sharing one thing you learned tonight "
            "and one way you want to live it out this week."
        )
    lines.append("")

    # --- 8. Closing prayer + sign-off (~100 words) ---
    lines.append("--- Closing ---")
    lines.append("")
    prayer = _CLOSING_PRAYERS[idx].format(scripture_ref=ep["scripture_ref"])
    lines.append(prayer)
    lines.append("")
    lines.append(_CLOSINGS[idx])
    lines.append("")
    lines.append(f"[END OF FAMILY DEVOTIONAL, DAY {day}]")

    return "\n".join(lines)
