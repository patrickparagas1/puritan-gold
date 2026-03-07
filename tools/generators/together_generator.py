#!/usr/bin/env python3
"""
Together (Couples) Devotional Script Generator for Puritan Gold.

Generates ~1400-word (~10-minute) couples devotional scripts with the
following structure:
    1. Opening for couples          (~100 words)
    2. Scripture reading            (~200 words)
    3. Puritan commentary           (~400 words)
    4. Marriage application         (~300 words)
    5. Reflection questions         (~150 words)
    6. Prayer focus                 (~150 words)
    7. Closing blessing             (~100 words)

Public API:
    generate_together_script(ep) -> str
"""

# ---------------------------------------------------------------------------
# Rotation pools
# ---------------------------------------------------------------------------

_OPENINGS = [
    (
        "Good evening, dear husband and wife. Welcome to tonight's "
        "couples devotional from Puritan Gold. Thank you for setting "
        "aside this time to draw near to God and to each other. The "
        "moments you invest in your marriage before the Lord are among "
        "the most important moments of your day."
    ),
    (
        "Hello, beloved couple. It is a beautiful thing when husband "
        "and wife sit down together in God's Word. The Puritans called "
        "marriage a little church within the church. Tonight, your "
        "little church is in session. Welcome."
    ),
    (
        "Welcome, dear ones. Marriage is a gift from God, and so is "
        "this time together in His presence. Whether this has been an "
        "easy day or a hard one, you are here, together, and that "
        "matters more than you know."
    ),
    (
        "Good evening. What a blessing it is to see a husband and wife "
        "seeking the Lord together. The Puritans believed that a "
        "praying couple is an unstoppable force for the kingdom of God. "
        "Let us pray together tonight."
    ),
    (
        "Hello and welcome to your couples devotional. Whether you are "
        "sitting side by side on the couch or listening together at the "
        "end of a long day, God is here with you both. He meets married "
        "couples in a special way when they turn their hearts to Him "
        "together."
    ),
    (
        "Good evening, dear couple. The Puritans believed that marriage "
        "was one of the greatest means of grace God provides. Tonight "
        "we enter into that grace together. Let us open our hearts and "
        "our ears to what the Lord has for us."
    ),
    (
        "Welcome, husband and wife. There is something powerful about "
        "two hearts turning toward God at the same time. When you both "
        "face the same direction, toward Christ, everything in your "
        "marriage finds its proper alignment. Let us do that now."
    ),
]

_SCRIPTURE_INTROS = [
    "Let us open God's Word together. Our passage tonight comes from {ref}:",
    "Tonight we turn to {ref}. Listen with your hearts, not just your ears:",
    "Our Scripture reading this evening is from {ref}. Let us receive it together:",
    "The Word of God has sustained marriages for thousands of years. Tonight it speaks to yours from {ref}:",
    "Let me read our passage for this evening. It comes from {ref}:",
    "As we settle in together, let us hear from {ref}:",
    "Every marriage needs a foundation that does not shift. Let us hear from that foundation now, from {ref}:",
]

_COMMENTARY_INTROS = [
    (
        "Now let us hear from {author}, one of the great Puritan voices "
        "on this subject. The Puritans wrote extensively about marriage "
        "because they saw it as one of God's most profound gifts."
    ),
    (
        "{author} had deep insight into the truths we have just read. "
        "The Puritans did not separate theology from daily life, and "
        "their reflections on marriage are remarkably practical."
    ),
    (
        "The Puritans understood marriage in a way that the modern world "
        "has largely forgotten. Let us hear from {author}, who wrote "
        "with great wisdom on this subject."
    ),
    (
        "Let us sit at the feet of a Puritan teacher. {author} reflected "
        "deeply on the truths of Scripture and how they apply to the "
        "covenant of marriage."
    ),
    (
        "{author} was a faithful pastor and theologian whose words still "
        "carry weight centuries later. Listen to what the Puritans had "
        "to say about the truths in tonight's passage."
    ),
    (
        "One of the gifts of the Christian tradition is that we do not "
        "study alone. We have the wisdom of the saints who came before "
        "us. Tonight we hear from {author}."
    ),
    (
        "The Puritans treasured marriage as a covenant made before God. "
        "{author} wrote beautifully about how Scripture speaks to the "
        "hearts of married couples."
    ),
]

_REFLECTION_INTROS = [
    (
        "Now let us pause for reflection. Here are some questions for "
        "you and your spouse to discuss together. Be honest. Be gentle. "
        "Listen more than you speak."
    ),
    (
        "It is time for reflection. Turn to each other and consider "
        "these questions together. There is no rush. Let the conversation "
        "go wherever the Spirit leads."
    ),
    (
        "The Puritans practiced what they called holy conference, "
        "speaking honestly about spiritual things with those they loved "
        "most. Do that now with these questions."
    ),
    (
        "Here are some questions to guide your conversation tonight. "
        "Take turns sharing, and give each other the gift of your "
        "full attention."
    ),
    (
        "Let us reflect together. These questions are designed to help "
        "you go deeper, both with God and with each other."
    ),
    (
        "Discussion time. Husband, listen to your wife. Wife, listen to "
        "your husband. Let this be a safe and sacred space."
    ),
    (
        "Now turn to each other. Here are tonight's reflection questions. "
        "Answer from the heart, not from the head."
    ),
]

_PRAYER_INTROS = [
    (
        "Let us move into a time of prayer together. If you are able, "
        "hold hands as you pray. There is something powerful about a "
        "husband and wife joining hands before the throne of grace."
    ),
    (
        "Now let us pray together. The Puritans said that a couple who "
        "prays together is bound by cords that cannot be broken. Let "
        "us strengthen those cords tonight."
    ),
    (
        "It is time to bring what we have heard and discussed before "
        "the Lord in prayer. Pray out loud if you can. Let your spouse "
        "hear your heart."
    ),
    (
        "Prayer is the heartbeat of a Christian marriage. Let us pray "
        "together now. You do not need eloquent words, just honest ones."
    ),
    (
        "As we near the end of tonight's devotional, let us bring our "
        "hearts before God in prayer. Pray for each other. Pray for "
        "your marriage. Pray for your home."
    ),
    (
        "Let us close our eyes and open our hearts to the Lord in "
        "prayer. Husband, pray for your wife. Wife, pray for your "
        "husband. There is no greater gift you can give each other."
    ),
    (
        "The Puritans ended every evening with prayer. Let us follow "
        "their example and bring our marriage before the Lord."
    ),
]

_BLESSINGS = [
    (
        "May the Lord bless your marriage and keep it strong. May He "
        "make His face to shine upon your home, and give you peace. "
        "Goodnight, dear couple. Walk together in His love."
    ),
    (
        "The grace of our Lord Jesus Christ, the love of God, and the "
        "fellowship of the Holy Spirit be with you both, tonight and "
        "always. Goodnight."
    ),
    (
        "May the God who brought you together continue to bind you "
        "together in love, in faith, and in purpose. Sleep well "
        "tonight. He watches over your marriage."
    ),
    (
        "May your love for each other grow deeper with every passing "
        "day, and may your love for God be the source and the strength "
        "of it all. Goodnight, dear ones."
    ),
    (
        "The Lord bless you and keep you. The Lord make His face shine "
        "upon you and be gracious to you. The Lord lift up His "
        "countenance upon you both, and give you peace. Amen."
    ),
    (
        "Go in peace, husband and wife. The God who ordained your "
        "marriage is faithful to sustain it. Trust Him. Love each "
        "other. And come back tomorrow for more. Goodnight."
    ),
    (
        "May the words you have heard tonight bear fruit in your "
        "marriage for years to come. The Lord be with you both. "
        "Until next time."
    ),
]


# ---------------------------------------------------------------------------
# Public generator function
# ---------------------------------------------------------------------------

def generate_together_script(ep):
    """
    Generate a ~1400-word couples devotional script.

    Parameters
    ----------
    ep : dict
        Episode data with keys:
            day, title, subtitle, scripture_ref, scripture_text,
            puritan_author, puritan_commentary, marriage_application,
            reflection_questions (list of 3), prayer_focus, blessing

    Returns
    -------
    str
        Complete couples devotional script text ready for TTS.
    """
    day = ep["day"]
    idx = (day - 1) % 7

    lines = []

    # --- Header ---
    lines.append(f"PURITAN GOLD -- Together: Couples Devotional, Day {day}")
    lines.append(f'"{ep["title"]}"')
    lines.append(ep["subtitle"])
    lines.append("")
    lines.append("---")
    lines.append("")

    # --- 1. Opening for couples (~100 words) ---
    lines.append(_OPENINGS[idx])
    lines.append("")

    # --- 2. Scripture reading (~200 words) ---
    intro = _SCRIPTURE_INTROS[idx].format(ref=ep["scripture_ref"])
    lines.append(intro)
    lines.append("")
    lines.append(f'"{ep["scripture_text"]}"')
    lines.append("")
    lines.append(
        f"That is {ep['scripture_ref']}. Take a breath. Let those words "
        f"settle between the two of you. God is speaking to your marriage "
        f"through this passage."
    )
    lines.append("")

    # --- 3. Puritan commentary (~400 words) ---
    lines.append("--- Puritan Commentary ---")
    lines.append("")
    commentary_intro = _COMMENTARY_INTROS[idx].format(
        author=ep["puritan_author"]
    )
    lines.append(commentary_intro)
    lines.append("")

    commentary = ep.get("puritan_commentary", "").strip()
    if commentary:
        lines.append(commentary)
    else:
        lines.append(
            f"{ep['puritan_author']} reminds us that the truths of "
            f"Scripture are meant to be lived out in the closest of "
            f"human relationships: marriage. What we have read tonight "
            f"is not merely academic. It speaks directly to the covenant "
            f"you have made with each other and with God."
        )
    lines.append("")

    # --- 4. Marriage application (~300 words) ---
    lines.append("--- Marriage Application ---")
    lines.append("")
    application = ep.get("marriage_application", "").strip()
    if application:
        lines.append(application)
    else:
        lines.append(
            f"Consider how the truths from {ep['scripture_ref']} apply "
            f"to your marriage right now, in this season. What is God "
            f"asking of you as a husband or wife? What change does He "
            f"want to make in your relationship?"
        )
    lines.append("")

    lines.append(
        "The Puritans understood that marriage is not a destination but "
        "a journey. Every day presents new opportunities to love, to "
        "serve, to forgive, and to grow together. The truths we have "
        "studied tonight are not just for tonight. They are for tomorrow "
        "morning when the alarm goes off, for the difficult conversation "
        "that has been waiting, for the quiet moments when only God sees "
        "how you treat each other."
    )
    lines.append("")

    # --- 5. Reflection questions (~150 words) ---
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
            "Take a few minutes with each question. Do not rush. The "
            "best conversations in marriage happen when both people feel "
            "truly heard."
        )
        lines.append("")

    # --- 6. Prayer focus (~150 words) ---
    lines.append("--- Prayer ---")
    lines.append("")
    lines.append(_PRAYER_INTROS[idx])
    lines.append("")

    prayer_focus = ep.get("prayer_focus", "").strip()
    if prayer_focus:
        lines.append(f"Tonight's prayer focus: {prayer_focus}")
    else:
        lines.append(
            "Pray for your marriage. Pray for unity, for patience, for "
            "deeper love. Pray that God would make your marriage a "
            "reflection of Christ's love for His church."
        )
    lines.append("")

    lines.append(
        "If one of you finds it difficult to pray out loud, that is "
        "perfectly fine. Simply holding hands in silence before the Lord "
        "is itself a powerful act of worship. Let the Spirit intercede "
        "where words fail."
    )
    lines.append("")

    # --- 7. Closing blessing (~100 words) ---
    lines.append("--- Blessing ---")
    lines.append("")
    blessing = ep.get("blessing", "").strip()
    if blessing:
        lines.append(blessing)
        lines.append("")

    lines.append(_BLESSINGS[idx])
    lines.append("")
    lines.append(f"[END OF COUPLES DEVOTIONAL, DAY {day}]")

    return "\n".join(lines)
