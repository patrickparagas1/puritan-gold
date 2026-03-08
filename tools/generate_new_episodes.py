#!/usr/bin/env python3
"""Generate all new episode JSON entries for Study Topics + May/June daily sections."""
import json
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ─── Helper to generate dates ───
def may_dates(count=31):
    """Generate May 2026 dates (1-31)"""
    return [f"2026-05-{d:02d}" for d in range(1, count+1)]

def june_dates(count=30):
    """Generate June 2026 dates (1-30)"""
    return [f"2026-06-{d:02d}" for d in range(1, count+1)]

def weekday_dates_may():
    """Mon-Fri only in May 2026. May 1=Friday"""
    from datetime import date, timedelta
    dates = []
    d = date(2026, 5, 1)
    end = date(2026, 5, 31)
    while d <= end:
        if d.weekday() < 5:  # Mon=0 ... Fri=4
            dates.append(d.strftime('%Y-%m-%d'))
        d += timedelta(days=1)
    return dates[:20]

def weekday_dates_june():
    """Mon-Fri only in June 2026. June 1=Monday"""
    from datetime import date, timedelta
    dates = []
    d = date(2026, 6, 1)
    end = date(2026, 6, 30)
    while d <= end:
        if d.weekday() < 5:
            dates.append(d.strftime('%Y-%m-%d'))
        d += timedelta(days=1)
    return dates[:20]

# ═══════════════════════════════════════
# STUDY TOPICS (not date-based)
# ═══════════════════════════════════════

sirach_eps = [
    {"id":1001,"title":"The Wisdom of Ben Sira","subtitle":"Sirach Introduction — Who Was Ben Sira?","description":"Meet Jesus Ben Sira and discover why the early church treasured this wisdom book."},
    {"id":1002,"title":"The Crown of Wisdom","subtitle":"Sirach 1-2 — The Fear of the Lord","description":"All wisdom begins with the fear of God — Sirach's opening hymn."},
    {"id":1003,"title":"Honor Your Father and Mother","subtitle":"Sirach 3 — Duties to Parents","description":"Sirach expands the fifth commandment with searching counsel on filial piety."},
    {"id":1004,"title":"Humility and Patience","subtitle":"Sirach 4-5 — Walking Humbly Before God","description":"The blessings of humility and the dangers of pride and presumption."},
    {"id":1005,"title":"The Test of True Friendship","subtitle":"Sirach 6 — Faithful Friends","description":"How to recognize, test, and cherish true friendship."},
    {"id":1006,"title":"Wisdom and Self-Control","subtitle":"Sirach 18-19 — Mastering Tongue and Desire","description":"The wise man governs his speech and appetites with divine discipline."},
    {"id":1007,"title":"The Table and Hospitality","subtitle":"Sirach 31-32 — Moderation and Generosity","description":"Biblical wisdom on feasting, hosting, and the virtue of temperance."},
    {"id":1008,"title":"Prayer and True Worship","subtitle":"Sirach 34-35 — Approaching God","description":"What God requires in worship — sincerity, justice, and a contrite heart."},
    {"id":1009,"title":"The Praise of the Fathers","subtitle":"Sirach 44-50 — Heroes of Faith","description":"Ben Sira's majestic roll call from Enoch to Simon the High Priest."},
    {"id":1010,"title":"Sirach's Final Prayer","subtitle":"Sirach 51 — Thanksgiving and Wisdom's Hymn","description":"Ben Sira's personal prayer of gratitude and his invitation to seek wisdom."},
]
for i, ep in enumerate(sirach_eps):
    ep.update({"file":None,"duration":"15:00","durationSecs":900,"fileSize":0,"date":"2026-03-01",
               "series":"Sirach","section":"study","topic":"sirach","topicOrder":i+1,"topicTotal":10,
               "tags":["sirach","wisdom","apocrypha"]})

female_piety_eps = [
    {"id":1011,"title":"Introduction to Female Piety","subtitle":"John Angell James — His Life and Vision","description":"Meet John Angell James and his passionate vision for godly womanhood."},
    {"id":1012,"title":"The Importance of Female Piety","subtitle":"Female Piety — Why It Matters","description":"Why women's spiritual life matters to all of society."},
    {"id":1013,"title":"The Character of the Pious Woman","subtitle":"Female Piety — Virtue and Grace","description":"Humility, devotion, prayer, gentleness, and inner beauty."},
    {"id":1014,"title":"Woman in the Home","subtitle":"Female Piety — The Domestic Calling","description":"The home as a sacred realm of divine calling."},
    {"id":1015,"title":"The Christian Mother","subtitle":"Female Piety — Raising Children","description":"Training children in the nurture and admonition of the Lord."},
    {"id":1016,"title":"The Christian Wife","subtitle":"Female Piety — Love and Partnership","description":"Submission, sacrificial love, and gospel partnership in marriage."},
    {"id":1017,"title":"Female Influence on Society","subtitle":"Female Piety — Shaping Culture","description":"How godly women shape community and culture through quiet influence."},
    {"id":1018,"title":"Trials and Suffering","subtitle":"Female Piety — Grace in Affliction","description":"Finding strength in suffering with Puritan resilience."},
    {"id":1019,"title":"The Devotional Life","subtitle":"Female Piety — Prayer and Meditation","description":"Building a rich inner life through prayer, Scripture, and holy meditation."},
    {"id":1020,"title":"The Legacy of Female Piety","subtitle":"Female Piety — Generational Impact","description":"What godly women leave behind for generations to come."},
]
for i, ep in enumerate(female_piety_eps):
    ep.update({"file":None,"duration":"15:00","durationSecs":900,"fileSize":0,"date":"2026-03-01",
               "series":"Female Piety","section":"study","topic":"female-piety","topicOrder":i+1,"topicTotal":10,
               "tags":["female-piety","john-angell-james","godly-womanhood"]})

enoch_eps = [
    {"id":1021,"title":"Introduction to the Book of Enoch","subtitle":"1 Enoch — History and Significance","description":"What is the Book of Enoch, its history, and its relationship to Scripture."},
    {"id":1022,"title":"The Watchers","subtitle":"1 Enoch 1-5 — Angels Who Left Their Domain","description":"The angelic beings who descended and their cosmic rebellion."},
    {"id":1023,"title":"The Fall of the Watchers","subtitle":"1 Enoch 6-16 — Sons of God and Daughters of Men","description":"The expansion of Genesis 6 — the Watchers' corruption of humanity."},
    {"id":1024,"title":"Enoch's Cosmic Journeys","subtitle":"1 Enoch 17-36 — Visions of Heaven and Earth","description":"Enoch's guided tours of the cosmos, sheol, and paradise."},
    {"id":1025,"title":"The Parables of Enoch","subtitle":"1 Enoch 37-44 — Messianic Prophecy","description":"The Son of Man figure and messianic expectations in Jewish apocalyptic."},
    {"id":1026,"title":"The Son of Man","subtitle":"1 Enoch 45-57 — The Elect One","description":"The Christ-like figure who judges the nations and vindicates the righteous."},
    {"id":1027,"title":"The Book of Luminaries","subtitle":"1 Enoch 72-82 — Cosmic Order and Design","description":"The astronomical sections revealing God's ordered creation."},
    {"id":1028,"title":"The Dream Visions","subtitle":"1 Enoch 83-90 — The Animal Apocalypse","description":"Israel's history told through symbolic animal imagery."},
    {"id":1029,"title":"The Epistle of Enoch","subtitle":"1 Enoch 91-105 — Woes and Blessings","description":"Prophetic warnings and promises for the last generation."},
    {"id":1030,"title":"Jude and Enoch","subtitle":"Jude 14-15 — The New Testament Connection","description":"How the apostle Jude quotes Enoch and what it means for Scripture."},
]
for i, ep in enumerate(enoch_eps):
    ep.update({"file":None,"duration":"15:00","durationSecs":900,"fileSize":0,"date":"2026-03-01",
               "series":"Enoch","section":"study","topic":"enoch","topicOrder":i+1,"topicTotal":10,
               "tags":["enoch","pseudepigrapha","apocalyptic"]})

melchizedek_eps = [
    {"id":1031,"title":"The Mysterious King of Salem","subtitle":"Genesis 14:17-20 — Melchizedek Appears","description":"The first appearance of the priest-king who blessed Abraham."},
    {"id":1032,"title":"A Priest Forever","subtitle":"Psalm 110:4 — David's Prophetic Declaration","description":"David's messianic psalm declaring an eternal priesthood."},
    {"id":1033,"title":"Without Father, Without Mother","subtitle":"Hebrews 7:1-3 — The Eternal Priesthood","description":"The author of Hebrews reveals Melchizedek as a type of Christ."},
    {"id":1034,"title":"Greater Than Abraham","subtitle":"Hebrews 7:4-10 — The Superiority of Melchizedek","description":"How Melchizedek's priesthood surpasses the Levitical order."},
    {"id":1035,"title":"A Better Covenant","subtitle":"Hebrews 7:11-22 — The Need for a New Priesthood","description":"Why the Levitical priesthood had to give way to something greater."},
    {"id":1036,"title":"The Unchangeable Priesthood","subtitle":"Hebrews 7:23-28 — Christ's Eternal Intercession","description":"Jesus lives forever to make intercession for His people."},
    {"id":1037,"title":"Melchizedek in Puritan Theology","subtitle":"Owen, Goodwin, and the Type","description":"How the great Puritan theologians interpreted the Melchizedek type."},
    {"id":1038,"title":"King of Righteousness, King of Peace","subtitle":"The Full Typology Fulfilled in Christ","description":"The complete fulfillment of Melchizedek's type in the Lord Jesus Christ."},
]
for i, ep in enumerate(melchizedek_eps):
    ep.update({"file":None,"duration":"15:00","durationSecs":900,"fileSize":0,"date":"2026-03-01",
               "series":"Melchizedek","section":"study","topic":"melchizedek","topicOrder":i+1,"topicTotal":8,
               "tags":["melchizedek","typology","hebrews"]})

# ═══════════════════════════════════════
# MAY FAMILY (162-192) — "Puritan Household Masters"
# ═══════════════════════════════════════

may_d = may_dates(31)
family_may_titles = [
    # Week 1: William Gouge — Domestical Duties (May 1-7)
    ("The Puritan Household Vision","William Gouge — Domestical Duties","Gouge's vision of the Christian home as a little commonwealth."),
    ("Mutual Duties of Husband and Wife","William Gouge — Domestical Duties","What husbands and wives owe one another in the fear of God."),
    ("The Husband as Provider and Protector","William Gouge — Domestical Duties","A husband's duty to provide for and protect his family."),
    ("The Wife's Domestic Governance","William Gouge — Domestical Duties","The wife's role in managing the household with wisdom."),
    ("Training Children in the Way","William Gouge — Domestical Duties","Gouge on the parent's duty to educate and discipline children."),
    ("Servants and Masters in the Home","William Gouge — Domestical Duties","How every member of the household serves God in their station."),
    ("Family Worship as Daily Practice","William Gouge — Domestical Duties","Establishing daily worship in the home."),
    # Week 2: John Angell James — Female Piety (May 8-14)
    ("The Godly Mother's Influence","John Angell James — Female Piety","How a mother's piety shapes the next generation."),
    ("Teaching Children to Pray","John Angell James — Female Piety","Training children in the practice of prayer from infancy."),
    ("The Mother's Example","John Angell James — Female Piety","Children learn more from what they see than what they hear."),
    ("Nurturing Young Faith","John Angell James — Female Piety","Cultivating genuine faith in children's hearts."),
    ("The Proverbs 31 Woman Today","John Angell James — Female Piety","Applying the virtuous woman passage to modern family life."),
    ("A Mother's Prayers","John Angell James — Female Piety","The power of a praying mother in the life of her children."),
    ("Raising Daughters in Piety","John Angell James — Female Piety","Preparing daughters for godly womanhood."),
    # Week 3: Matthew Henry — Family Worship (May 15-21)
    ("A Church in the House","Matthew Henry — Family Worship","Henry's classic case for family devotions."),
    ("Reading Scripture Together","Matthew Henry — Family Worship","How to read the Bible as a family with profit."),
    ("Singing Psalms at Home","Matthew Henry — Family Worship","The Puritan practice of family psalm-singing."),
    ("Catechizing Your Children","Matthew Henry — Family Worship","Teaching doctrine through questions and answers."),
    ("The Lord's Day in the Home","Matthew Henry — Family Worship","Making the Sabbath a delight for the whole family."),
    ("Mealtime Devotions","Matthew Henry — Family Worship","Giving thanks and speaking of God at the table."),
    ("Evening Family Prayers","Matthew Henry — Family Worship","Ending each day with worship, confession, and thanksgiving."),
    # Week 4: Richard Baxter — Christian Directory (May 22-28)
    ("Parenting with Patience","Richard Baxter — The Christian Directory","Baxter's counsel on patient, persistent parenting."),
    ("Correcting Children in Love","Richard Baxter — The Christian Directory","The Puritan approach to discipline — firm but tender."),
    ("Teaching Children About Death and Eternity","Richard Baxter — The Christian Directory","Preparing children to think about the life to come."),
    ("The Dangers of Worldly Education","Richard Baxter — The Christian Directory","Guarding children from harmful influences."),
    ("Building Family Unity","Richard Baxter — The Christian Directory","How families grow strong through shared worship and purpose."),
    ("The Father's Spiritual Leadership","Richard Baxter — The Christian Directory","Why the father must lead family devotions."),
    ("Baxter's Family Rules","Richard Baxter — The Christian Directory","Practical rules for a well-ordered Christian home."),
    # Days 29-31: Synthesis
    ("Building a Puritan Home Today","Synthesis — Household Masters","Applying Puritan household wisdom to modern family life."),
    ("The Family as God's Workshop","Synthesis — Household Masters","How God uses the family to sanctify every member."),
    ("A Family Covenant","Synthesis — Household Masters","Making a family covenant of faith and faithfulness."),
]

family_may_eps = []
for i, (title, subtitle, desc) in enumerate(family_may_titles):
    family_may_eps.append({
        "id": 162 + i, "title": title, "subtitle": subtitle, "description": desc,
        "file": None, "duration": "10:00", "durationSecs": 600, "fileSize": 0,
        "date": may_d[i], "series": "Family Devotional", "section": "family",
        "tags": ["family", "puritan-household"],
        "memoryVerse": "", "discussionQuestions": [], "day": i + 1
    })

# ═══════════════════════════════════════
# MAY SCHOOL (241-260) — Reformation + Ethics
# ═══════════════════════════════════════

school_may_dates = weekday_dates_may()
school_may_titles = [
    # Unit 1: Reformation & Church History (1-10)
    ("The Dawn of the Reformation","The Reformation — Lesson 1","The state of the church before Luther and the need for reform."),
    ("Martin Luther and the 95 Theses","The Reformation — Lesson 2","Luther's bold stand against indulgences in 1517."),
    ("Sola Scriptura: Scripture Alone","The Reformation — Lesson 3","The Reformation principle that Scripture is the final authority."),
    ("John Calvin and Geneva","The Reformation — Lesson 4","Calvin's theology and the city that became a model of Reformed faith."),
    ("The English Reformation","The Reformation — Lesson 5","How the Reformation came to England under Henry VIII and beyond."),
    ("John Knox and Scotland","The Reformation — Lesson 6","The fiery preacher who brought Reformed faith to Scotland."),
    ("William Tyndale and the English Bible","The Reformation — Lesson 7","Tyndale's martyrdom to give the Bible in English."),
    ("The Puritans: Reforming the Reformation","The Reformation — Lesson 8","How the Puritans sought to complete what the Reformation started."),
    ("The Great Ejection of 1662","The Reformation — Lesson 9","2,000 ministers expelled from the Church of England."),
    ("The Legacy of the Reformation","The Reformation — Lesson 10","How the Reformation shapes the church today."),
    # Unit 2: Christian Ethics (11-20)
    ("The Foundation of Christian Ethics","Christian Ethics — Lesson 11","God's moral law as the basis for all ethics."),
    ("No Other Gods: The First Commandment","Christian Ethics — Lesson 12","What it means to worship God alone in the modern world."),
    ("No Graven Images: Worship in Spirit","Christian Ethics — Lesson 13","The second commandment and pure worship."),
    ("Hallowing God's Name","Christian Ethics — Lesson 14","Using God's name with reverence in thought and speech."),
    ("Remember the Sabbath","Christian Ethics — Lesson 15","The Lord's Day as a gift and a duty."),
    ("Honor Your Father and Mother","Christian Ethics — Lesson 16","Submission to authority as a moral foundation."),
    ("You Shall Not Kill","Christian Ethics — Lesson 17","The sanctity of life and the ethics of anger."),
    ("Purity of Heart and Body","Christian Ethics — Lesson 18","The seventh commandment and sexual ethics."),
    ("Honest Living","Christian Ethics — Lesson 19","The eighth commandment and integrity in all dealings."),
    ("Truth-Telling and Contentment","Christian Ethics — Lesson 20","The ninth and tenth commandments — truth and satisfaction in God."),
]

school_may_eps = []
for i, (title, subtitle, desc) in enumerate(school_may_titles):
    school_may_eps.append({
        "id": 241 + i, "title": title, "subtitle": subtitle, "description": desc,
        "file": None, "duration": "30:00", "durationSecs": 1800, "fileSize": 0,
        "date": school_may_dates[i] if i < len(school_may_dates) else f"2026-05-{(i+1):02d}",
        "series": "Homeschool", "section": "school",
        "tags": ["school", "reformation" if i < 10 else "ethics"],
        "reviewQuestions": [], "activity": "", "lessonNumber": i + 1, "day": i + 1
    })

# ═══════════════════════════════════════
# MAY TOGETHER (362-392) — Song of Solomon
# ═══════════════════════════════════════

together_may_titles = [
    # Week 1: Song of Solomon 1-2
    ("The Song of Songs","Song of Solomon 1:1-4","The greatest song — an invitation to marital love."),
    ("I Am Dark but Lovely","Song of Solomon 1:5-8","The bride's honest self-assessment and the beloved's acceptance."),
    ("My Beloved Is Mine","Song of Solomon 1:9-17","The language of mutual admiration between husband and wife."),
    ("The Rose of Sharon","Song of Solomon 2:1-7","The beauty of the beloved and the charge not to stir love prematurely."),
    ("The Voice of My Beloved","Song of Solomon 2:8-13","Spring arrives — the beloved comes leaping over mountains."),
    ("The Little Foxes","Song of Solomon 2:14-17","Catching the small things that destroy the vineyard of love."),
    ("Until the Day Breaks","Song of Solomon 2:16-17","Belonging to one another until morning comes."),
    # Week 2: Song of Solomon 3-4
    ("Seeking Him by Night","Song of Solomon 3:1-5","The bride seeks her beloved through the city."),
    ("The Wedding Procession","Song of Solomon 3:6-11","Solomon's glorious wedding day."),
    ("You Are Altogether Beautiful","Song of Solomon 4:1-7","The bridegroom praises every part of his bride."),
    ("Come Away from Lebanon","Song of Solomon 4:8-11","An invitation to leave the old life and enter marital bliss."),
    ("A Garden Enclosed","Song of Solomon 4:12-16","The bride as a locked garden — purity and exclusivity in love."),
    ("Let My Garden Breathe","Song of Solomon 4:16-5:1","The bride opens her garden — the consummation of love."),
    ("Eat, O Friends, and Drink","Song of Solomon 5:1","God's blessing on marital intimacy."),
    # Week 3: Song of Solomon 5-6
    ("I Sleep, But My Heart Wakes","Song of Solomon 5:2-8","The painful moment of rejection and regret in marriage."),
    ("My Beloved Is Radiant","Song of Solomon 5:9-16","The bride describes her husband's beauty."),
    ("Where Has Your Beloved Gone?","Song of Solomon 6:1-3","Seeking and finding one another again."),
    ("Beautiful as Tirzah","Song of Solomon 6:4-10","The bridegroom's renewed praise after reconciliation."),
    ("Return, Return, O Shulamite","Song of Solomon 6:11-13","The invitation to come back and be seen."),
    ("The Dance of Mahanaim","Song of Solomon 6:13","Two camps rejoicing — the joy of reunion."),
    ("How Beautiful Are Your Feet","Song of Solomon 7:1-5","The bridegroom delights in his wife's beauty."),
    # Week 4: Song of Solomon 7-8
    ("I Am My Beloved's","Song of Solomon 7:6-13","The fullness of mutual desire and delight."),
    ("Under the Apple Tree","Song of Solomon 8:1-4","Longing for deeper intimacy and public affection."),
    ("Love Is Strong as Death","Song of Solomon 8:5-7","The seal of love — jealousy as fierce as the grave."),
    ("Many Waters Cannot Quench Love","Song of Solomon 8:7","Love that endures every flood and fire."),
    ("Our Little Sister","Song of Solomon 8:8-10","Protecting younger generations in matters of love."),
    ("Solomon's Vineyard","Song of Solomon 8:11-12","Stewarding the vineyard of your marriage."),
    ("Make Haste, My Beloved","Song of Solomon 8:13-14","The final invitation — keep your love alive."),
    # Days 29-31: Puritan Marriage
    ("Marriage as Mutual Society","Richard Baxter — The Christian Directory","Baxter on the primary purpose of marriage."),
    ("Domestical Duties for Couples","William Gouge — Domestical Duties","Gouge's practical counsel for husbands and wives."),
    ("A Good Wife, God's Gift","Thomas Gataker — A Good Wife","The Puritan view of marriage as God's richest earthly blessing."),
]

together_may_eps = []
for i, (title, subtitle, desc) in enumerate(together_may_titles):
    together_may_eps.append({
        "id": 362 + i, "title": title, "subtitle": subtitle, "description": desc,
        "file": None, "duration": "8:00", "durationSecs": 480, "fileSize": 0,
        "date": may_d[i], "series": "Together", "section": "together",
        "tags": ["together", "song-of-solomon", "marriage"],
        "memoryVerse": "", "reflectionPrompt": "", "prayerFocus": "", "day": i + 1
    })

# ═══════════════════════════════════════
# MAY GROWTH (462-492) — Rotating Reading/Pastoral/Theological
# ═══════════════════════════════════════

growth_may_titles = [
    ("Pilgrim's Progress: The Wicket Gate","Reading — John Bunyan","Bunyan's pilgrim enters through the narrow gate."),
    ("The Art of Divine Contentment","Reading — Thomas Watson","Watson on finding satisfaction in God alone."),
    ("Walking Humbly with God","Pastoral — Practical Holiness","Daily habits of humility and dependence on God."),
    ("The Doctrine of Justification","Theological — Sola Fide","Declared righteous by faith alone in Christ alone."),
    ("The Mortification of Sin","Reading — John Owen","Owen's classic on putting sin to death."),
    ("Morning and Evening Prayer","Pastoral — Prayer Life","Establishing a rhythm of daily prayer."),
    ("The Sovereignty of God","Theological — Divine Providence","God's absolute control over all things for His glory."),
    ("The Bruised Reed","Reading — Richard Sibbes","Christ's tender mercy toward weak and struggling believers."),
    ("Fighting Spiritual Laziness","Pastoral — Spiritual Disciplines","Overcoming sloth in the Christian life."),
    ("The Person and Work of Christ","Theological — Christology","Who Jesus is and what He accomplished."),
    ("Grace Abounding to the Chief of Sinners","Reading — John Bunyan","Bunyan's spiritual autobiography and God's relentless grace."),
    ("Dealing with Doubt","Pastoral — Assurance of Faith","How to find certainty when faith feels fragile."),
    ("The Covenant of Grace","Theological — Covenant Theology","God's unbreakable promise from Genesis to Revelation."),
    ("All Things for Good","Reading — Thomas Watson","How God works even trials for the believer's benefit."),
    ("Loving Your Neighbor Practically","Pastoral — Christian Love","Concrete ways to love those God places in your life."),
    ("The Holy Spirit's Work","Theological — Pneumatology","The Spirit who regenerates, sanctifies, and empowers."),
    ("Precious Remedies Against Satan's Devices","Reading — Thomas Brooks","Brooks's strategies for resisting the devil's temptations."),
    ("Guarding Your Heart","Pastoral — Keeping the Heart","Flavel's counsel on the most important work in the Christian life."),
    ("Predestination and Free Will","Theological — Election","Understanding God's sovereign election with humility and trust."),
    ("The Saints' Everlasting Rest","Reading — Richard Baxter","Baxter on the heavenly rest that awaits the faithful."),
    ("Forgiving Others","Pastoral — Forgiveness","The duty and freedom of extending grace to those who wrong us."),
    ("The Atonement of Christ","Theological — Substitutionary Sacrifice","How Christ's death satisfied divine justice and saved sinners."),
    ("The Mystery of Providence","Reading — John Flavel","Flavel on tracing God's hand through the events of life."),
    ("Bearing Trials with Patience","Pastoral — Suffering Well","The Puritan approach to enduring hardship with grace."),
    ("The Church: God's New Community","Theological — Ecclesiology","The nature, purpose, and marks of the true church."),
    ("Holiness: Its Nature and Necessity","Reading — J.C. Ryle","Ryle's clarion call to pursue practical holiness."),
    ("Confessing Sin Honestly","Pastoral — Repentance","The practice of honest, specific confession before God."),
    ("Eschatology: The Last Things","Theological — Christ's Return","What the Bible teaches about death, judgment, and eternal life."),
    ("The Rare Jewel of Christian Contentment","Reading — Jeremiah Burroughs","Burroughs on the mystery of being content in all circumstances."),
    ("Stewarding Your Time","Pastoral — Redeeming the Time","Using your days wisely for God's glory."),
    ("The Glory of God in All Things","Theological — Doxology","Everything exists for the praise of His glorious grace."),
]

growth_may_eps = []
for i, (title, subtitle, desc) in enumerate(growth_may_titles):
    ptype = "reading" if "Reading" in subtitle else ("pastoral" if "Pastoral" in subtitle else "theological")
    growth_may_eps.append({
        "id": 462 + i, "title": title, "subtitle": subtitle, "description": desc,
        "file": None, "duration": "12:00", "durationSecs": 720, "fileSize": 0,
        "date": may_d[i], "series": "Personal Growth", "section": "personal",
        "tags": ["growth", "puritan", ptype], "personalType": ptype, "day": i + 1
    })

# ═══════════════════════════════════════
# JUNE FAMILY (193-222) — "Family Virtues"
# ═══════════════════════════════════════

june_d = june_dates(30)
family_june_titles = [
    # Week 1: Thomas Watson — The Ten Commandments
    ("The First Commandment at Home","Thomas Watson — The Ten Commandments","Having no other gods before the Lord in family life."),
    ("Worshipping God in Spirit","Thomas Watson — The Ten Commandments","Keeping worship pure in the home — no idols."),
    ("Hallowing God's Name Together","Thomas Watson — The Ten Commandments","Teaching children to reverence God's name."),
    ("Keeping the Lord's Day as a Family","Thomas Watson — The Ten Commandments","Making the Sabbath a family treasure."),
    ("Honoring Parents: A Two-Way Street","Thomas Watson — The Ten Commandments","Children's duty and parents' responsibility."),
    ("Anger and Forgiveness at Home","Thomas Watson — The Ten Commandments","Applying 'thou shalt not kill' to family anger."),
    ("Purity in Marriage and Home","Thomas Watson — The Ten Commandments","The seventh commandment applied to family life."),
    # Week 2: John Flavel — Providence
    ("God's Providence Over Your Family","John Flavel — The Mystery of Providence","Every circumstance in your family is God's doing."),
    ("Trusting God in Family Trials","John Flavel — The Mystery of Providence","When hard things come to your family."),
    ("When Children Wander","John Flavel — The Mystery of Providence","Trusting God when a child strays from the faith."),
    ("Financial Pressures and Faith","John Flavel — The Mystery of Providence","Trusting God as provider for the family."),
    ("Family Moves and Transitions","John Flavel — The Mystery of Providence","God's hand in the big changes of life."),
    ("Sickness in the Family","John Flavel — The Mystery of Providence","Finding God's purposes in family illness."),
    ("Remembering God's Faithfulness","John Flavel — The Mystery of Providence","Building family altars of remembrance."),
    # Week 3: Jonathan Edwards — Religious Affections
    ("True Religion in the Home","Jonathan Edwards — Religious Affections","What genuine faith looks like in daily family life."),
    ("Holy Love Between Family Members","Jonathan Edwards — Religious Affections","Affection for God producing affection for one another."),
    ("Joy in Family Worship","Jonathan Edwards — Religious Affections","Cultivating real joy in family devotions."),
    ("Humility Among Family","Jonathan Edwards — Religious Affections","The marks of genuine humility in family interactions."),
    ("Persevering Faith at Home","Jonathan Edwards — Religious Affections","A faith that endures through family seasons."),
    ("Changed Lives, Changed Homes","Jonathan Edwards — Religious Affections","How genuine conversion transforms family dynamics."),
    ("Testing Our Family's Faith","Jonathan Edwards — Religious Affections","Are our family devotions real or merely routine?"),
    # Week 4: Jeremiah Burroughs — Contentment
    ("Contentment in Your Family Situation","Jeremiah Burroughs — Rare Jewel","The mystery of being content with your family."),
    ("Contentment in Small Things","Jeremiah Burroughs — Rare Jewel","Finding joy in the simple daily rhythms."),
    ("When Families Compare","Jeremiah Burroughs — Rare Jewel","Resisting the trap of comparing families."),
    ("Contentment in Limited Resources","Jeremiah Burroughs — Rare Jewel","Thriving when money is tight."),
    ("Contentment with Your Children","Jeremiah Burroughs — Rare Jewel","Loving the children God actually gave you."),
    ("Contentment in Marriage","Jeremiah Burroughs — Rare Jewel","Finding sufficiency in Christ for marital satisfaction."),
    ("The Secret of Gospel Contentment","Jeremiah Burroughs — Rare Jewel","How the gospel produces genuine family peace."),
    # Days 29-30: Summer Synthesis
    ("Summer Rhythms of Faith","Synthesis — Family Virtues","Carrying Puritan wisdom into summer family life."),
    ("A Family Benediction","Synthesis — Family Virtues","Blessing your family as you enter a new season."),
]

family_june_eps = []
for i, (title, subtitle, desc) in enumerate(family_june_titles):
    family_june_eps.append({
        "id": 5001 + i, "title": title, "subtitle": subtitle, "description": desc,
        "file": None, "duration": "10:00", "durationSecs": 600, "fileSize": 0,
        "date": june_d[i], "series": "Family Devotional", "section": "family",
        "tags": ["family", "family-virtues"],
        "memoryVerse": "", "discussionQuestions": [], "day": i + 1
    })

# ═══════════════════════════════════════
# JUNE SCHOOL (261-280) — Westminster + Apologetics
# ═══════════════════════════════════════

school_june_dates = weekday_dates_june()
school_june_titles = [
    # Unit 1: Westminster Standards (1-10)
    ("What Is the Westminster Confession?","Westminster Standards — Lesson 1","The history and significance of the Westminster Assembly."),
    ("Of Holy Scripture","Westminster Standards — Lesson 2","Chapter 1: The Bible as God's infallible Word."),
    ("Of God and the Holy Trinity","Westminster Standards — Lesson 3","Chapter 2: One God in three persons."),
    ("Of God's Eternal Decree","Westminster Standards — Lesson 4","Chapter 3: Predestination and God's sovereign plan."),
    ("Of Creation and Providence","Westminster Standards — Lesson 5","Chapters 4-5: God's creation and sustaining of all things."),
    ("Of the Fall and Sin","Westminster Standards — Lesson 6","Chapter 6: How sin entered the world."),
    ("Of God's Covenant with Man","Westminster Standards — Lesson 7","Chapter 7: The covenants of works and grace."),
    ("Of Christ the Mediator","Westminster Standards — Lesson 8","Chapter 8: Jesus as prophet, priest, and king."),
    ("Of Justification and Adoption","Westminster Standards — Lesson 9","Chapters 11-12: Declared righteous and made sons."),
    ("Of Sanctification and Good Works","Westminster Standards — Lesson 10","Chapters 13-16: Growing in holiness by God's grace."),
    # Unit 2: Apologetics (11-20)
    ("What Is Apologetics?","Apologetics — Lesson 11","Defending the faith — 1 Peter 3:15."),
    ("Does God Exist?","Apologetics — Lesson 12","Arguments for God's existence from nature and reason."),
    ("Can We Trust the Bible?","Apologetics — Lesson 13","Evidence for the reliability of Scripture."),
    ("The Problem of Evil","Apologetics — Lesson 14","How a good God can allow suffering."),
    ("Science and Faith","Apologetics — Lesson 15","Are science and Christianity really in conflict?"),
    ("The Resurrection of Jesus","Apologetics — Lesson 16","Historical evidence for the resurrection."),
    ("Other Religions and Christianity","Apologetics — Lesson 17","What makes Christianity unique among world religions?"),
    ("Common Objections to Christianity","Apologetics — Lesson 18","Answering the most common challenges."),
    ("Sharing Your Faith","Apologetics — Lesson 19","How to explain the gospel clearly and lovingly."),
    ("Living as a Young Apologist","Apologetics — Lesson 20","Being ready to give an answer with gentleness and respect."),
]

school_june_eps = []
for i, (title, subtitle, desc) in enumerate(school_june_titles):
    school_june_eps.append({
        "id": 5101 + i, "title": title, "subtitle": subtitle, "description": desc,
        "file": None, "duration": "30:00", "durationSecs": 1800, "fileSize": 0,
        "date": school_june_dates[i] if i < len(school_june_dates) else f"2026-06-{(i+1):02d}",
        "series": "Homeschool", "section": "school",
        "tags": ["school", "westminster" if i < 10 else "apologetics"],
        "reviewQuestions": [], "activity": "", "lessonNumber": i + 1, "day": i + 1
    })

# ═══════════════════════════════════════
# JUNE TOGETHER (393-422) — Ephesians 5 + Puritan Household
# ═══════════════════════════════════════

together_june_titles = [
    # Week 1: Ephesians 5:22-33
    ("Submit One to Another","Ephesians 5:21","Mutual submission in the fear of Christ."),
    ("Wives, Submit to Your Husbands","Ephesians 5:22-24","What biblical submission means — and what it doesn't."),
    ("Husbands, Love Your Wives","Ephesians 5:25-27","Sacrificial love modeled after Christ and the church."),
    ("Nourish and Cherish","Ephesians 5:28-30","Caring for your spouse as you care for your own body."),
    ("The Great Mystery","Ephesians 5:31-33","Marriage as a picture of Christ and the church."),
    ("Leaving and Cleaving","Genesis 2:24 + Ephesians 5","The priority of the marriage bond over all others."),
    ("Reverence and Love","Ephesians 5:33","The summary: wives reverence, husbands love."),
    # Week 2: Daily Applications
    ("Speaking the Truth in Love","Ephesians 4:15","Honest communication between husband and wife."),
    ("Be Angry and Sin Not","Ephesians 4:26-27","Handling conflict without letting the sun go down on wrath."),
    ("Building Each Other Up","Ephesians 4:29","Using words that edify your spouse."),
    ("Forgiving as Christ Forgave","Ephesians 4:32","The daily practice of marital forgiveness."),
    ("Walking in Love Daily","Ephesians 5:1-2","Imitating Christ's love in the small moments."),
    ("Redeeming the Time Together","Ephesians 5:15-16","Using your years of marriage wisely."),
    ("Being Filled with the Spirit Together","Ephesians 5:18-20","Spirit-filled marriage — singing, thanking, submitting."),
    # Week 3: William Gouge — Domestical Duties
    ("Gouge on Mutual Love","William Gouge — Domestical Duties","What Gouge taught about marital affection."),
    ("The Husband's Authority and Gentleness","William Gouge — Domestical Duties","Authority exercised with Christ-like meekness."),
    ("The Wife's Wisdom and Strength","William Gouge — Domestical Duties","The Puritan wife as a capable, godly partner."),
    ("Financial Stewardship Together","William Gouge — Domestical Duties","Managing money as one flesh."),
    ("Hospitality as a Couple","William Gouge — Domestical Duties","Opening your home to others."),
    ("Praying Together Daily","William Gouge — Domestical Duties","The Puritan practice of couples' prayer."),
    ("Resolving Disagreements","William Gouge — Domestical Duties","Gouge's counsel on marital conflict resolution."),
    # Week 4: Thomas Gataker — A Good Wife
    ("A Good Wife, God's Gift","Thomas Gataker — A Good Wife","Marriage as God's richest earthly blessing."),
    ("The Prudent Wife","Proverbs 19:14","Prudence, wisdom, and discernment in a wife."),
    ("A Wife of Noble Character","Proverbs 31:10-12","Her husband trusts in her completely."),
    ("She Opens Her Mouth with Wisdom","Proverbs 31:26-27","The wife who speaks wisdom and watches over her household."),
    ("Her Children Rise and Call Her Blessed","Proverbs 31:28-29","The fruit of a godly wife and mother."),
    ("Charm Is Deceitful, Beauty Is Vain","Proverbs 31:30-31","A woman who fears the Lord — she shall be praised."),
    ("The Crown of Her Husband","Proverbs 12:4","Being a crown rather than rottenness to your spouse."),
    # Days 29-30: Summer Marriage
    ("Summer Love: Keeping Romance Alive","Puritan Marriage Wisdom","Practical ways to nurture romance in summer rhythms."),
    ("Renewing Your Marriage Covenant","Puritan Marriage Wisdom","Recommitting your marriage to the Lord."),
]

together_june_eps = []
for i, (title, subtitle, desc) in enumerate(together_june_titles):
    together_june_eps.append({
        "id": 5201 + i, "title": title, "subtitle": subtitle, "description": desc,
        "file": None, "duration": "8:00", "durationSecs": 480, "fileSize": 0,
        "date": june_d[i], "series": "Together", "section": "together",
        "tags": ["together", "ephesians", "marriage"],
        "memoryVerse": "", "reflectionPrompt": "", "prayerFocus": "", "day": i + 1
    })

# ═══════════════════════════════════════
# JUNE GROWTH (493-522) — Rotating
# ═══════════════════════════════════════

growth_june_titles = [
    ("The Mortification of Sin, Part 1","Reading — John Owen","Owen on the nature and necessity of killing sin."),
    ("The Mortification of Sin, Part 2","Reading — John Owen","Owen's practical directions for mortifying sin."),
    ("Cultivating a Prayer Life","Pastoral — Deeper Prayer","Moving beyond rote prayer to communion with God."),
    ("The Doctrine of the Trinity","Theological — One God, Three Persons","The foundational Christian doctrine of the triune God."),
    ("Grace Abounding: Bunyan's Conversion","Reading — John Bunyan","Bunyan's dramatic conversion and wrestling with assurance."),
    ("Spiritual Warfare","Pastoral — Fighting the Good Fight","The believer's armor and daily battle against sin."),
    ("The Doctrine of Predestination","Theological — God's Sovereign Choice","Understanding election with humility and awe."),
    ("All Things for Good: Affliction","Reading — Thomas Watson","Watson on how God uses suffering for our benefit."),
    ("Dealing with Discouragement","Pastoral — Spiritual Depression","Puritan remedies for the downcast soul."),
    ("The Atonement: Penal Substitution","Theological — Christ Died for Us","How Christ's death satisfied God's justice."),
    ("Precious Remedies, Part 1","Reading — Thomas Brooks","Brooks on Satan's devices and how to resist them."),
    ("Precious Remedies, Part 2","Reading — Thomas Brooks","More of Brooks's practical strategies against temptation."),
    ("The Discipline of Bible Reading","Pastoral — Scripture Intake","Establishing a pattern of serious, profitable Bible reading."),
    ("The Perseverance of the Saints","Theological — Eternal Security","Can a true believer fall away? The Puritan answer."),
    ("Keeping the Heart","Reading — John Flavel","Flavel's masterwork on guarding the inner life."),
    ("Fasting and Self-Denial","Pastoral — Spiritual Disciplines","The forgotten discipline of fasting for spiritual power."),
    ("The Doctrine of Sanctification","Theological — Growing in Holiness","The progressive work of the Spirit in making us holy."),
    ("The Pilgrim's Progress: Vanity Fair","Reading — John Bunyan","Christian and Faithful face the world's temptations."),
    ("Serving in the Local Church","Pastoral — Using Your Gifts","Finding your place in the body of Christ."),
    ("The Doctrine of the Church","Theological — Ecclesiology","What makes a true church — Word, sacraments, discipline."),
    ("The Valley of Vision","Reading — Puritan Prayers","The rich devotional prayers of the Puritans."),
    ("Evangelism and Personal Witness","Pastoral — Sharing the Gospel","How to speak of Christ naturally and boldly."),
    ("The Last Judgment","Theological — The Final Reckoning","What Scripture teaches about the day of judgment."),
    ("The Saints' Everlasting Rest","Reading — Richard Baxter","Baxter on meditating upon the heavenly glory."),
    ("Generosity and Stewardship","Pastoral — Faithful Living","Using time, talent, and treasure for God's kingdom."),
    ("The New Heavens and New Earth","Theological — Eternal Glory","The final destiny of the redeemed — all things made new."),
    ("A Lifting Up for the Downcast","Reading — William Bridge","Bridge's counsel for discouraged believers."),
    ("Walking in Integrity","Pastoral — Honest Living","Living with transparency and moral courage."),
    ("The Whole Counsel of God","Theological — Systematic Summary","Bringing together the great doctrines of the faith."),
    ("Doxology: To God Be the Glory","Theological — Final Worship","All theology leads to worship — a closing benediction."),
]

growth_june_eps = []
for i, (title, subtitle, desc) in enumerate(growth_june_titles):
    ptype = "reading" if "Reading" in subtitle else ("pastoral" if "Pastoral" in subtitle else "theological")
    growth_june_eps.append({
        "id": 5301 + i, "title": title, "subtitle": subtitle, "description": desc,
        "file": None, "duration": "12:00", "durationSecs": 720, "fileSize": 0,
        "date": june_d[i], "series": "Personal Growth", "section": "personal",
        "tags": ["growth", "puritan", ptype], "personalType": ptype, "day": i + 1
    })

# ═══════════════════════════════════════
# MERGE INTO episodes.json
# ═══════════════════════════════════════

with open(os.path.join(BASE, 'episodes.json'), 'r') as f:
    existing = json.load(f)

new_eps = (
    sirach_eps + female_piety_eps + enoch_eps + melchizedek_eps +
    family_may_eps + school_may_eps + together_may_eps + growth_may_eps +
    family_june_eps + school_june_eps + together_june_eps + growth_june_eps
)

# Check for ID collisions
existing_ids = {e['id'] for e in existing}
for ep in new_eps:
    if ep['id'] in existing_ids:
        print(f"WARNING: ID collision: {ep['id']} — {ep['title']}")

all_eps = existing + new_eps
all_eps.sort(key=lambda e: e['id'])

with open(os.path.join(BASE, 'episodes.json'), 'w') as f:
    json.dump(all_eps, f, indent=2, ensure_ascii=False)

print(f"Done! Total episodes: {len(all_eps)} (was {len(existing)}, added {len(new_eps)})")
print(f"  Study topics: {len(sirach_eps + female_piety_eps + enoch_eps + melchizedek_eps)}")
print(f"  May daily: {len(family_may_eps + school_may_eps + together_may_eps + growth_may_eps)}")
print(f"  June daily: {len(family_june_eps + school_june_eps + together_june_eps + growth_june_eps)}")
