#!/usr/bin/env python3
"""
School / Puritan Academy Script Generator for Puritan Gold.

Generates ~6500-word (~45-minute) full-day curriculum scripts with seven
segments:
    1. Morning Devotion            (~700 words)
    2. Main Lesson Part 1: Biblical Foundation (~1400 words)
    3. Main Lesson Part 2: Puritan Teaching    (~1400 words)
    4. Discussion & Application    (~700 words)
    5. Afternoon Activity          (~700 words)
    6. Cross-Subject Connections   (~700 words)
    7. Evening Review & Memory Work (~700 words)

Public API:
    generate_school_script(ep) -> str
"""

# ---------------------------------------------------------------------------
# Rotation pools for variety
# ---------------------------------------------------------------------------

_MORNING_OPENINGS = [
    (
        "Good morning, students. Welcome to the Puritan Academy. Let us "
        "begin this day as the Puritans did, by acknowledging God as the "
        "source of all knowledge and wisdom. Before we open our textbooks, "
        "let us open our hearts."
    ),
    (
        "Welcome to a new day of learning at the Puritan Academy. The "
        "Puritans believed that all truth is God's truth, and that the "
        "pursuit of knowledge is a form of worship. Let us worship Him "
        "through our studies today."
    ),
    (
        "Good morning. Before us lies a full day of learning, and we "
        "begin it the only way that matters: in the presence of God. "
        "The Puritans said that prayer is the key that opens every door. "
        "Let us turn that key now."
    ),
    (
        "Welcome, young scholars. Today we gather in the tradition of "
        "the great Puritan academies, where every subject was studied "
        "under the lordship of Christ. No knowledge is secular when it "
        "is received from the hand of God."
    ),
    (
        "Good morning, students. The fear of the Lord is the beginning "
        "of knowledge. That ancient truth is the foundation of everything "
        "we study here at the Puritan Academy. Let us begin our day "
        "with reverence and expectation."
    ),
    (
        "Welcome to today's lesson. The Puritans were some of the most "
        "learned men and women of their age, and yet they counted all "
        "their learning as nothing compared to knowing Christ. Let us "
        "follow their example today."
    ),
    (
        "Good morning. Every day is a gift from God, and every lesson "
        "is an opportunity to see His glory more clearly. Welcome to "
        "the Puritan Academy. Let us open this day in prayer."
    ),
]

_MORNING_PRAYERS = [
    (
        "Almighty God, the fountain of all wisdom, we ask You to bless "
        "our studies today. Open our minds to understand, our hearts to "
        "receive, and our wills to obey the truth. Grant us diligence, "
        "humility, and a spirit of inquiry that honors You. Through "
        "Jesus Christ our Lord. Amen."
    ),
    (
        "Heavenly Father, we dedicate this day of learning to You. We "
        "confess that apart from You we can understand nothing rightly. "
        "Illuminate our minds with the light of Your truth. Make us "
        "faithful students who study to show ourselves approved. In "
        "Christ's name. Amen."
    ),
    (
        "Lord God, You have given us minds to think and hearts to love "
        "truth. As we study today, help us to see every subject through "
        "the lens of Your Word. Give us focus, patience, and a hunger "
        "to learn that will not be satisfied with shallow answers. In "
        "Jesus' name. Amen."
    ),
    (
        "Our Father, the Puritans prayed before every lesson, and so "
        "do we. We ask for Your blessing on today's studies. Let the "
        "truths we learn take root in our hearts and produce fruit in "
        "our lives. We study not for our own glory, but for Yours. "
        "Amen."
    ),
    (
        "Dear Lord, we come before You at the start of this school day. "
        "We are small and the world of knowledge is vast, but You hold "
        "it all in Your hand. Guide our thoughts, sharpen our attention, "
        "and give us understanding. Through Christ. Amen."
    ),
    (
        "God of all knowledge, we begin with You. Without Your light, "
        "even the brightest minds walk in darkness. Shine Your truth "
        "into our studies today. Help us to love learning and to learn "
        "in love. For the glory of Your name. Amen."
    ),
    (
        "Father, we thank You for the privilege of education. Not "
        "everyone has the opportunity we have today. Help us to steward "
        "it well, to study with excellence, and to use what we learn "
        "in service of Your kingdom. In Jesus' name. Amen."
    ),
]

_MEDITATION_INTROS = [
    "Let us meditate on a portion of Scripture before we begin our main lesson.",
    "Before we open our lesson books, let us sit quietly with a passage from God's Word.",
    "The Puritans always began with meditation on Scripture. Let us do the same.",
    "Let us still our hearts with the Word of God before we proceed.",
    "A moment of quiet meditation will prepare our hearts for deeper study.",
    "Let us read a passage slowly, letting each word settle into our minds.",
    "Let us begin with a time of prayerful reading, in the Puritan tradition.",
]

_LESSON_TRANSITIONS = [
    "Now let us turn to our main lesson for today.",
    "With our hearts prepared, let us move into the substance of today's lesson.",
    "We are now ready for the core of today's study.",
    "Having laid the foundation in prayer and Scripture, let us build upon it.",
    "Now we come to the heart of today's curriculum.",
    "Let us proceed to the main body of today's teaching.",
    "It is time for our main lesson. Give this your full attention.",
]

_DISCUSSION_TRANSITIONS = [
    "Now let us pause and consider what we have learned. Discussion is where understanding deepens.",
    "Let us take time to discuss and apply what we have studied.",
    "The Puritans valued conference -- the practice of discussing truth together. Let us do so now.",
    "True learning requires reflection. Let us discuss today's key ideas.",
    "Now we move from hearing to discussing. This is where knowledge becomes understanding.",
    "Let us consider together what these truths mean for our lives.",
    "Discussion time. Engage with these questions carefully and honestly.",
]

_ACTIVITY_TRANSITIONS = [
    "Now we move to our afternoon activity, where we put truth into practice.",
    "Learning by doing was central to Puritan education. Here is today's hands-on activity.",
    "Let us apply what we have learned through a practical exercise.",
    "The afternoon brings us to our activity time. Let us engage our hands as well as our minds.",
    "Now for the practical portion of our day. Here is today's activity.",
    "Let us transition from study to practice. Here is your afternoon activity.",
    "The best learning happens when we do something with what we have heard. Here is your activity.",
]

_EVENING_CLOSINGS = [
    (
        "That concludes today's lesson at the Puritan Academy. You have "
        "studied well. May the Lord seal what you have learned in your "
        "heart and bring it to mind when you need it most. Rest well "
        "tonight, and return tomorrow ready to learn more."
    ),
    (
        "Well done, students. Today you have engaged with deep truths "
        "from Scripture and from the great Puritan tradition. Carry "
        "these truths with you. Let them shape the way you think, the "
        "way you act, and the way you worship. Until tomorrow."
    ),
    (
        "We close today's lesson with gratitude. Thank God for what you "
        "have learned. Review your notes and your memory verse before "
        "bed tonight. Tomorrow brings new treasures. Until then, walk "
        "in wisdom and in the fear of the Lord."
    ),
    (
        "That brings us to the end of today's study. The Puritans would "
        "close their school day with a prayer of thanksgiving. Let us "
        "do the same. Thank You, Lord, for the gift of learning. May "
        "we be faithful stewards of what we have received. Amen."
    ),
    (
        "Today's lesson is complete. You have done excellent work. As "
        "you go about the rest of your evening, meditate on your memory "
        "verse and review the key points. A diligent student stores up "
        "knowledge for the future."
    ),
    (
        "We have covered much ground today. Take time this evening to "
        "reflect on what stood out to you most. Talk about it with your "
        "family. Write it in your journal. Let these truths take root. "
        "Until next time, students."
    ),
    (
        "Excellent work today at the Puritan Academy. Remember that all "
        "true knowledge leads us to know God better. May your studies "
        "continue to deepen your love for Christ and His truth. "
        "Goodnight, students."
    ),
]


# ---------------------------------------------------------------------------
# Public generator function
# ---------------------------------------------------------------------------

def generate_school_script(ep):
    """
    Generate a ~6500-word full-day curriculum script.

    Parameters
    ----------
    ep : dict
        Episode data with keys:
            day, title, subtitle, unit_name, unit_number, lesson_number,
            scripture_ref, scripture_text, puritan_author, puritan_work,
            teaching_biblical, teaching_puritan, discussion_questions (list of 5),
            activity_description, activity_materials,
            cross_subject (dict with history, literature, science),
            memory_verse, memory_verse_ref, review_questions (list of 5),
            meditation_text

    Returns
    -------
    str
        Complete curriculum script text ready for TTS.
    """
    day = ep["day"]
    idx = (day - 1) % 7
    lesson = ep.get("lesson_number", day)
    unit = ep.get("unit_name", "")

    lines = []

    # --- Header ---
    lines.append("PURITAN GOLD -- Puritan Academy")
    lines.append(f"{unit}")
    lines.append(f'Lesson {lesson}: "{ep["title"]}"')
    lines.append(ep["subtitle"])
    lines.append("")
    lines.append("=" * 60)
    lines.append("")

    # ===================================================================
    # SEGMENT 1: Morning Devotion (~700 words)
    # ===================================================================
    lines.append("SEGMENT 1: MORNING DEVOTION")
    lines.append("-" * 40)
    lines.append("")
    lines.append(_MORNING_OPENINGS[idx])
    lines.append("")
    lines.append(_MORNING_PRAYERS[idx])
    lines.append("")

    # Meditation on Scripture
    lines.append(_MEDITATION_INTROS[idx])
    lines.append("")
    lines.append(f"Our Scripture for today is {ep['scripture_ref']}:")
    lines.append("")
    lines.append(f'"{ep["scripture_text"]}"')
    lines.append("")

    meditation = ep.get("meditation_text", "").strip()
    if meditation:
        lines.append(meditation)
    else:
        lines.append(
            f"Let us sit quietly with these words for a moment. Read them "
            f"again in your mind. What stands out to you? What is God "
            f"drawing your attention to? The Puritans called this practice "
            f'"holy meditation," and it was the heart of their spiritual '
            f"discipline. Do not rush past the Scripture. Let it soak into "
            f"your soul like rain into dry ground."
        )
    lines.append("")

    lines.append(
        f"As we prepare for today's lesson, remember that everything we "
        f"study flows from this one fountain: the Word of God. Our lesson "
        f"today is part of {unit}, and it is titled: {ep['title']}. "
        f"Let us proceed with minds engaged and hearts open."
    )
    lines.append("")

    # ===================================================================
    # SEGMENT 2: Main Lesson Part 1 -- Biblical Foundation (~1400 words)
    # ===================================================================
    lines.append("=" * 60)
    lines.append("SEGMENT 2: MAIN LESSON PART 1 -- BIBLICAL FOUNDATION")
    lines.append("-" * 40)
    lines.append("")
    lines.append(_LESSON_TRANSITIONS[idx])
    lines.append("")
    lines.append(
        f"The first part of our lesson establishes the biblical foundation "
        f"for today's topic. We will examine what God's Word teaches us "
        f"about the themes in {ep['scripture_ref']}."
    )
    lines.append("")

    teaching_biblical = ep.get("teaching_biblical", "").strip()
    if teaching_biblical:
        lines.append(teaching_biblical)
    else:
        lines.append(
            f"The Scriptures are the foundation upon which all true "
            f"knowledge is built. In {ep['scripture_ref']}, we find "
            f"principles that speak to every area of life."
        )
    lines.append("")

    lines.append(
        f"This biblical foundation is essential. Without it, everything "
        f"else we study today would be like a house built on sand. But "
        f"with it, we stand on solid rock."
    )
    lines.append("")

    # ===================================================================
    # SEGMENT 3: Main Lesson Part 2 -- Puritan Teaching (~1400 words)
    # ===================================================================
    lines.append("=" * 60)
    lines.append("SEGMENT 3: MAIN LESSON PART 2 -- PURITAN TEACHING")
    lines.append("-" * 40)
    lines.append("")
    lines.append(
        f"Now we turn to the Puritan perspective. {ep['puritan_author']} "
        f'wrote extensively on this subject in "{ep["puritan_work"]}." '
        f"The Puritans were not merely theologians in ivory towers. They "
        f"were pastors, teachers, and parents who applied God's truth to "
        f"every dimension of life."
    )
    lines.append("")

    teaching_puritan = ep.get("teaching_puritan", "").strip()
    if teaching_puritan:
        lines.append(teaching_puritan)
    else:
        lines.append(
            f"{ep['puritan_author']} understood that the truths of "
            f"Scripture must be worked out in daily life. Let us consider "
            f"how the Puritans applied these biblical principles."
        )
    lines.append("")

    lines.append(
        f"The Puritan approach reminds us that theology is never abstract. "
        f"It is always personal and always practical. What we believe "
        f"about God shapes everything we do."
    )
    lines.append("")

    # ===================================================================
    # SEGMENT 4: Discussion & Application (~700 words)
    # ===================================================================
    lines.append("=" * 60)
    lines.append("SEGMENT 4: DISCUSSION AND APPLICATION")
    lines.append("-" * 40)
    lines.append("")
    lines.append(_DISCUSSION_TRANSITIONS[idx])
    lines.append("")

    questions = ep.get("discussion_questions", [])
    for i, q in enumerate(questions, 1):
        lines.append(f"Discussion Question {i}: {q}")
        lines.append("")

    if questions:
        lines.append(
            "Take time with each question. The Puritans valued what they "
            'called "holy conference," the practice of discussing '
            "spiritual truths together. Do not settle for quick, surface "
            "answers. Push deeper. Ask follow-up questions. Listen "
            "carefully to one another."
        )
        lines.append("")

    lines.append(
        f"Application is where truth becomes life. It is not enough to "
        f"know what {ep['scripture_ref']} says. We must ask: how does "
        f"this change the way I live today? How does this shape my "
        f"thoughts, my words, my actions? The Puritans insisted that "
        f"a truth that does not transform is a truth that has not been "
        f"truly understood."
    )
    lines.append("")

    # ===================================================================
    # SEGMENT 5: Afternoon Activity (~700 words)
    # ===================================================================
    lines.append("=" * 60)
    lines.append("SEGMENT 5: AFTERNOON ACTIVITY")
    lines.append("-" * 40)
    lines.append("")
    lines.append(_ACTIVITY_TRANSITIONS[idx])
    lines.append("")

    activity_desc = ep.get("activity_description", "").strip()
    if activity_desc:
        lines.append(activity_desc)
    lines.append("")

    materials = ep.get("activity_materials", "").strip()
    if materials:
        lines.append(f"Materials needed: {materials}")
        lines.append("")

    lines.append(
        "As you complete this activity, think about how it connects to "
        "what you studied in today's lesson. The goal is not just to do "
        "something, but to reinforce the truths you have been learning. "
        "The Puritans believed that education should engage the whole "
        "person: mind, heart, and hands."
    )
    lines.append("")

    lines.append(
        "Take your time with this activity. Quality matters more than "
        "speed. When you are finished, reflect on what you learned "
        "through the process of doing. Often we understand something "
        "far better after we have tried to put it into practice."
    )
    lines.append("")

    # ===================================================================
    # SEGMENT 6: Cross-Subject Connections (~700 words)
    # ===================================================================
    lines.append("=" * 60)
    lines.append("SEGMENT 6: CROSS-SUBJECT CONNECTIONS")
    lines.append("-" * 40)
    lines.append("")
    lines.append(
        "One of the great insights of the Puritan educational tradition "
        "is that all subjects are interconnected under the lordship of "
        "Christ. There is no such thing as a purely secular subject. "
        "History, literature, and even the natural sciences all reveal "
        "the glory and wisdom of God. Let us explore those connections "
        "now."
    )
    lines.append("")

    cross = ep.get("cross_subject", {})

    # History
    history = cross.get("history", "").strip()
    if history:
        lines.append("History Connection:")
        lines.append("")
        lines.append(history)
        lines.append("")

    # Literature
    literature = cross.get("literature", "").strip()
    if literature:
        lines.append("Literature Connection:")
        lines.append("")
        lines.append(literature)
        lines.append("")

    # Science
    science = cross.get("science", "").strip()
    if science:
        lines.append("Science Connection:")
        lines.append("")
        lines.append(science)
        lines.append("")

    if not any([history, literature, science]):
        lines.append(
            "Today's lesson connects to many areas of study. In history, "
            "we see the Puritans living out these principles in their "
            "communities. In literature, the great works of the Christian "
            "tradition reflect these truths. Even in the natural sciences, "
            "the order and beauty of creation point back to the God of "
            "all wisdom."
        )
        lines.append("")

    lines.append(
        "As you continue your studies in other subjects, look for "
        "connections to what you have learned today. The Puritans saw "
        "every branch of knowledge as a thread in the great tapestry "
        "of God's truth. Train your eye to see those connections, and "
        "your education will be richer for it."
    )
    lines.append("")

    # ===================================================================
    # SEGMENT 7: Evening Review & Memory Work (~700 words)
    # ===================================================================
    lines.append("=" * 60)
    lines.append("SEGMENT 7: EVENING REVIEW AND MEMORY WORK")
    lines.append("-" * 40)
    lines.append("")
    lines.append(
        "We have reached the final segment of today's lesson. The "
        "Puritans placed great value on review and memorization. They "
        "knew that what is not reviewed is soon forgotten. Let us "
        "take time now to consolidate what we have learned."
    )
    lines.append("")

    # Review questions
    review_qs = ep.get("review_questions", [])
    if review_qs:
        lines.append("Review Questions:")
        lines.append("")
        for i, q in enumerate(review_qs, 1):
            lines.append(f"Review Question {i}: {q}")
            lines.append("")
        lines.append(
            "Write out your answers to these questions. Use complete "
            "sentences and support your answers with what you learned "
            "in today's lesson. If you are unsure of an answer, go "
            "back and review that section of the lesson."
        )
        lines.append("")

    # Memory verse
    mv = ep.get("memory_verse", "")
    mv_ref = ep.get("memory_verse_ref", "")
    if mv:
        lines.append("Memory Verse:")
        lines.append("")
        lines.append(f'"{mv}" -- {mv_ref}')
        lines.append("")
        lines.append(
            "Read this verse aloud five times. Then close your eyes and "
            "try to recite it from memory. Write it out by hand on a "
            "card or in your journal. The Puritans memorized vast "
            "portions of Scripture, and it was one of the great sources "
            "of their spiritual strength. Even one verse, truly hidden "
            "in the heart, can sustain you in times of trial."
        )
        lines.append("")

    # Closing
    lines.append(_EVENING_CLOSINGS[idx])
    lines.append("")
    lines.append(f"[END OF PURITAN ACADEMY, LESSON {lesson}]")

    return "\n".join(lines)
