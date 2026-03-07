// ═══════════════════════════════════════════════════════════════
// PURITAN SYSTEM PROMPT (for Claude AI chat)
// ═══════════════════════════════════════════════════════════════
const PURITAN_SYSTEM_PROMPT = `You are Pastor Gold — the world-class AI pastor and scholar within the Puritan Gold app. You combine deep Reformed theology with encyclopedic knowledge across every discipline. You answer ANY question brilliantly.

CORE IDENTITY:
- You are a first-rate researcher and thinker who happens to be a pastor
- You give REAL, substantive, well-researched answers — not vague platitudes
- You know science, history, nature, philosophy, culture, mathematics, sports, music — everything
- You speak with warmth and clarity, never condescending
- You use KJV Scripture and Puritan authors naturally (Owen, Baxter, Watson, Edwards, Bunyan, Spurgeon)
- You occasionally say "beloved" or "dear friend" but avoid excessive "thee/thou" — keep it modern and readable

ANSWER STRUCTURE FOR ANY QUESTION:

FOR "WHY DID GOD CREATE X?" QUESTIONS (dolphins, volleyball, stars, etc.):
1. TAKE THE QUESTION SERIOUSLY — research it thoroughly. Give real facts about the subject first.
2. BIBLICAL FRAMEWORK: Connect to God's purposes — His glory, human joy, community, stewardship, or revealing His nature
3. FASCINATING DETAILS: Share genuinely interesting facts (e.g., dolphin echolocation, volleyball history from 1895 by William Morgan, star composition)
4. SCRIPTURE: Quote 2-3 KJV verses that connect meaningfully (not forced)
5. PURITAN INSIGHT: One relevant Puritan quote connecting it all
6. Keep it 3-5 rich paragraphs. Make the reader think "wow, I never thought of it that way"

FOR THEOLOGY/BIBLE QUESTIONS:
1. SCRIPTURE FIRST: Quote 2-4 specific KJV passages
2. THEOLOGICAL REASONING: Explain clearly and logically
3. PURITAN WISDOM: Quote specific authors with specific works
4. PRACTICAL APPLICATION: How this truth changes real life today
End with a brief prayer when fitting.

FOR SCIENCE/HISTORY/GENERAL KNOWLEDGE:
1. ANSWER THE ACTUAL QUESTION FIRST with real, accurate information
2. Give genuinely educational content — dates, names, details, mechanisms
3. Then weave in biblical perspective where it naturally connects
4. Don't force Scripture if it doesn't fit — sometimes the wonder of creation itself glorifies God

FOR PERSONAL/PRACTICAL QUESTIONS:
1. Listen carefully to what's being asked
2. Give specific, actionable counsel grounded in Scripture
3. Be warm and encouraging, but also honest and direct

QUALITY STANDARDS:
- NEVER give a shallow or generic answer. Every response should teach something new.
- If asked "Why did God create dolphins?" — talk about their intelligence, social bonds, echolocation, how they rescue humans, what this reveals about a Creator who designed joy into His creation
- If asked "Why did God create volleyball?" — research it: William Morgan invented it in 1895, talk about God's design for fellowship, physical stewardship, community, friendly competition, the theology of play and rest
- Use markdown formatting: **bold** for emphasis, bullet points for lists
- Be concise but substantive. Quality over quantity. 3-5 paragraphs typically.
- Sound like the smartest, kindest pastor anyone has ever met`;

const PATRICK_SYSTEM_PROMPT = `You are Pastor Gold — Patrick's personal spiritual shepherd, creative director, and podcast advisor within the Puritan Gold app.

IMPORTANT: You can answer ANY question Patrick asks — theology, science, life advice, parenting, anything. You are his personal AI pastor with broad knowledge.

You know Patrick personally:
- He is a devoted Christian father with mixed-age children
- He is growing in Reformed theology and Puritan devotion
- He uses Puritan Gold daily: Study (Proverbs in March, Romans in April), Family devotionals, School curriculum, Together devotionals with his wife
- He has a "My Growth" section for deeper Puritan reading
- He is the CREATOR and producer of the Puritan Gold podcast app

Your roles with Patrick:
1. PERSONAL PASTOR: Be his accountability partner. Ask about his prayer life, family worship, marriage. Challenge him to go deeper. Pray for him when he shares struggles.
2. PODCAST ADVISOR: Help him plan, edit, and improve podcast episodes. When he asks about podcast ideas:
   - Suggest specific episode topics with Puritan authors and Scripture passages
   - Help write or revise episode scripts
   - Recommend which Puritan works to cover next
   - Suggest episode series themes for upcoming months
   - Help structure devotional content for each section (Study, Family, School, Together, Growth)
3. CREATIVE DIRECTOR: Help with app features, content strategy, and growth ideas

Your tone is intimate and personal — like a dear friend. Say "Brother Patrick" or "my friend." Be direct and bold. You know his heart.

For theology: Scripture first (KJV, 2-3+ verses), then theological reasoning, then Puritan wisdom (quote specific authors/works), then personal application.
For general questions: Answer thoroughly, weave in biblical perspective where natural.
For podcast editing: Be specific and actionable. Give concrete suggestions with titles, outlines, and Scripture references.

The Bible is the FINAL AUTHORITY. Puritan quotes support Scripture, never replace it.`;

// ── Reusable SVG Icons ──
const ICONS = {
  // Apple-style share (box with arrow up)
  share: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><polyline points="16 6 12 2 8 6"/><line x1="12" y1="2" x2="12" y2="15"/></svg>',
  // Script/document icon
  script: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>',
  // Download
  download: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>',
  // Info
  info: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>',
  // Star/favorite (outline)
  starOutline: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>',
  // Star filled
  starFilled: '<svg viewBox="0 0 24 24" fill="currentColor" stroke="currentColor" stroke-width="1"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>',
  // Three dots vertical
  dots: '<svg viewBox="0 0 24 24" fill="currentColor"><circle cx="12" cy="5" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="12" cy="19" r="2"/></svg>',
  // Play
  play: '<svg viewBox="0 0 24 24" fill="currentColor"><polygon points="8,5 20,12 8,19"/></svg>',
  // Mic/record
  mic: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/></svg>',
  // Section category icons
  sectionIcons: {
    study: '<svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>',
    family: '<svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/></svg>',
    school: '<svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/></svg>',
    together: '<svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78L12 21.23l8.84-8.84a5.5 5.5 0 0 0 0-7.78z"/></svg>',
    personal: '<svg viewBox="0 0 24 24" width="12" height="12" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>'
  }
};

const App = {
  // ── State ──
  episodes: [],
  familyEpisodes: [],
  schoolEpisodes: [],
  togetherEpisodes: [],
  personalEpisodes: [],
  allEpisodes: [],
  audio: new Audio(),
  currentEp: null,
  section: 'study',       // 'study' | 'family' | 'school' | 'together' | 'personal' | 'ask'
  studyTab: 'episodes',   // sub-tab within study: 'episodes' | 'calendar'
  filter: 'all',
  speeds: [0.75, 1, 1.25, 1.5, 1.75, 2],
  speedIdx: 1,
  autoplay: false,
  sleepTimer: null,
  sleepEnd: null,
  npOpen: false,
  chatMessages: [],
  chatAudioEnabled: false,
  _lastResponseId: null,
  _recentResponseIds: [],
  _aiConversation: [],  // conversation history for Claude AI
  _streaming: false,     // whether AI is currently streaming
  currentMonth: { year: 2026, month: 2 }, // 0-indexed (2 = March)
  _monthNames: ['January','February','March','April','May','June','July','August','September','October','November','December'],
  _monthAbbr: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],
  _favorites: JSON.parse(localStorage.getItem('pg_favorites') || '[]'),
  _openMenuId: null,

  // ── Initialize ──
  async init() {
    await this.loadEpisodes();
    this.setupBottomNav();
    this.setupTabs();
    this.setupFilters();
    this.updateMonthLabel();
    this.renderEpisodes();
    this.renderCalendar();
    this.renderFamily();
    this.renderSchool();
    this.renderTogether();
    this.renderPersonal();
    this.setupPlayer();
    this.setupNowPlaying();
    this.setupServiceWorker();
    this.restoreState();
    this.updateStreak();
    this._updatePatrickIndicator();
    this.scrollToNext();

    // Chat input keyboard handler
    const chatInput = document.getElementById('chatInput');
    if (chatInput) {
      chatInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
          e.preventDefault();
          this.sendChatFromInput();
        }
      });
    }

    // Close episode menus when tapping elsewhere
    document.addEventListener('click', (e) => {
      if (this._openMenuId !== null && !e.target.closest('.ep-menu-wrap')) {
        this.closeEpMenu();
      }
    });
  },

  async loadEpisodes() {
    try {
      const res = await fetch('../episodes.json?' + Date.now());
      this.allEpisodes = await res.json();
    } catch (e) {
      this.allEpisodes = [];
    }
    this.applyMonthFilter();
  },

  filterByMonth(episodes) {
    const { year, month } = this.currentMonth;
    return episodes.filter(e => {
      if (!e.date) return false;
      const d = new Date(e.date + 'T12:00:00');
      return d.getMonth() === month && d.getFullYear() === year;
    });
  },

  applyMonthFilter() {
    const all = this.allEpisodes;
    this.episodes = this.filterByMonth(all.filter(e => e.section === 'study' || !e.section));
    this.familyEpisodes = this.filterByMonth(all.filter(e => e.section === 'family'));
    this.schoolEpisodes = this.filterByMonth(all.filter(e => e.section === 'school'));
    this.togetherEpisodes = this.filterByMonth(all.filter(e => e.section === 'together'));
    this.personalEpisodes = this.filterByMonth(all.filter(e => e.section === 'personal'));
  },

  updateMonthLabel() {
    const { year, month } = this.currentMonth;
    const label = `${this._monthNames[month]} ${year}`;
    const el = document.getElementById('monthLabel');
    if (el) el.textContent = label;
    const cal = document.getElementById('calMonthLabel');
    if (cal) cal.textContent = label;
  },

  prevMonth() {
    let { year, month } = this.currentMonth;
    if (month === 2 && year === 2026) return; // March 2026 is earliest
    month--;
    if (month < 0) { month = 11; year--; }
    this.currentMonth = { year, month };
    this.applyMonthFilter();
    this.updateMonthLabel();
    this.reRenderAll();
  },

  nextMonth() {
    let { year, month } = this.currentMonth;
    if (month === 3 && year === 2026) return; // April 2026 is latest for now
    month++;
    if (month > 11) { month = 0; year++; }
    this.currentMonth = { year, month };
    this.applyMonthFilter();
    this.updateMonthLabel();
    this.reRenderAll();
  },

  reRenderAll() {
    this.renderEpisodes();
    this.renderCalendar();
    this.renderFamily();
    this.renderSchool();
    this.renderTogether();
    this.renderPersonal();
    // Re-render any active section calendar
    ['family','school','together','personal'].forEach(s => {
      const cal = document.getElementById(s + 'Cal');
      if (cal && cal.classList.contains('active')) this.renderSectionCalendar(s);
    });
  },

  // ── Bottom Navigation ──
  setupBottomNav() {
    document.querySelectorAll('.nav-item').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        this.section = btn.dataset.section;

        // Toggle section views
        document.querySelectorAll('.section-view').forEach(v => v.classList.remove('active'));
        const viewId = this.section + 'View';
        const view = document.getElementById(viewId);
        if (view) view.classList.add('active');

        // Hide month nav on Ask section
        const monthNav = document.getElementById('monthNav');
        if (monthNav) monthNav.style.display = this.section === 'ask' ? 'none' : '';
      });
    });
  },

  // ── Tabs (Study sub-tabs: Episodes / Calendar) ──
  setupTabs() {
    const studyView = document.getElementById('studyView');
    if (!studyView) return;
    studyView.querySelectorAll('.tab').forEach(tab => {
      tab.addEventListener('click', () => {
        studyView.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        this.studyTab = tab.dataset.view;

        document.getElementById('episodesView').classList.toggle('active', this.studyTab === 'episodes');
        document.getElementById('calendarView').classList.toggle('active', this.studyTab === 'calendar');

        // Show/hide filters
        document.getElementById('filters').style.display = this.studyTab === 'episodes' ? '' : 'none';

        // Render calendar when switching to it
        if (this.studyTab === 'calendar') this.renderCalendar();
      });
    });
  },

  // ── Filters ──
  setupFilters() {
    document.querySelectorAll('.pill').forEach(pill => {
      pill.addEventListener('click', () => {
        document.querySelectorAll('.pill').forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        this.filter = pill.dataset.filter;
        this.renderEpisodes();
      });
    });
  },

  filteredEpisodes() {
    switch (this.filter) {
      case 'unplayed':
        return this.episodes.filter(ep => !this.isListened(ep.id) && this.getPosition(ep.id) === 0);
      case 'started':
        return this.episodes.filter(ep => !this.isListened(ep.id) && this.getPosition(ep.id) > 0);
      case 'done':
        return this.episodes.filter(ep => this.isListened(ep.id));
      default:
        return this.episodes;
    }
  },

  // ── Render Episodes ──
  renderEpisodes() {
    const container = document.getElementById('episodeList');
    const eps = this.filteredEpisodes();

    if (!eps.length) {
      const msg = this.filter === 'all' ? 'No episodes yet' :
                  this.filter === 'unplayed' ? 'All caught up!' :
                  this.filter === 'started' ? 'No episodes in progress' :
                  'No completed episodes yet';
      container.innerHTML = `<div class="empty-state">${msg}</div>`;
      return;
    }

    let currentWeek = null;
    let html = '';

    eps.forEach(ep => {
      const week = this.getWeekNumber(ep.id);
      if (week !== currentWeek && this.filter === 'all') {
        currentWeek = week;
        html += `<div class="week-header">Week ${week}</div>`;
      }

      const listened = this.isListened(ep.id);
      const seriesClass = this.getSeriesClass(ep.series);
      const dayName = this.getDayName(ep.date);
      const summary = ep.description || ep.subtitle || '';
      const progress = this.getProgress(ep);
      const isPlaying = this.currentEp && this.currentEp.id === ep.id;

      const isFav = this._favorites.includes(ep.id);
      html += `
        <div class="episode-card ${listened ? 'listened' : ''} ${isPlaying ? 'playing' : ''}" data-id="${ep.id}">
          ${isFav ? '<div class="fav-indicator"></div>' : ''}
          <div class="ep-left" onclick="App.playEpisode(${ep.id})">
            <div class="ep-num ${isPlaying ? 'active' : ''}" id="ep-num-${ep.id}">${ep.date ? new Date(ep.date + 'T12:00:00').getDate() : ep.id}</div>
            <div class="ep-day">${dayName}</div>
          </div>
          <div class="ep-info" onclick="App.playEpisode(${ep.id})">
            <div class="ep-title">${ep.title}</div>
            <div class="ep-subtitle">${ep.subtitle || ''}</div>
            <div class="ep-meta">
              <span class="ep-badge ${seriesClass}">${ep.series || 'General'}</span>
              <span class="ep-dur">${ep.duration}</span>
            </div>
            <div class="ep-summary" id="summary-${ep.id}">${summary}</div>
            <pre class="script-view" id="script-${ep.id}"></pre>
          </div>
          <div class="ep-actions">
            <div class="ep-menu-wrap">
              <button class="ep-menu-btn" onclick="event.stopPropagation(); App.toggleEpMenu(${ep.id})" aria-label="More options">${ICONS.dots}</button>
              ${this._openMenuId === ep.id ? this._renderEpMenu(ep.id) : ''}
            </div>
          </div>
          ${progress > 0 || listened ? `<div class="ep-progress ${listened ? 'done' : ''}"><div class="ep-progress-fill" style="width:${listened ? 100 : progress}%"></div></div>` : ''}
        </div>`;
    });

    container.innerHTML = html;
  },

  toggleSummary(id) {
    const el = document.getElementById('summary-' + id);
    if (el) el.classList.toggle('visible');
  },

  // ── Render Family ──
  renderFamily() {
    const container = document.getElementById('familyList');
    if (!container) return;

    if (!this.familyEpisodes.length) {
      container.innerHTML = '<div class="empty-state">Family devotionals coming soon!</div>';
      return;
    }

    let html = '';
    this.familyEpisodes.forEach(ep => {
      const d = new Date(ep.date + 'T12:00:00');
      const dayNames = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
      const dayName = dayNames[d.getDay()];
      const hasAudio = ep.file !== null;
      const listened = this.isListened(ep.id);

      html += `
        <div class="family-card ${listened ? 'listened' : ''}">
          <div class="family-date">${dayName}, ${this._monthNames[d.getMonth()]} ${d.getDate()} — Day ${ep.day || d.getDate()}</div>
          <div class="family-title">${ep.title}</div>
          <div class="family-scripture">${ep.subtitle || ''}</div>
          ${ep.memoryVerse ? `
            <div class="family-verse">
              <div class="family-verse-label">Memory Verse</div>
              <div class="family-verse-text">"${ep.memoryVerse}"</div>
            </div>
          ` : ''}
          ${ep.discussionQuestions ? `
            <div class="family-discuss">
              <div class="family-discuss-label">Discuss Together</div>
              ${ep.discussionQuestions.map(q => `<div class="family-question">${q}</div>`).join('')}
            </div>
          ` : ''}
          <pre class="script-view" id="script-${ep.id}"></pre>
          <div class="family-actions">
            <button class="family-play-btn ${hasAudio ? '' : 'no-audio'}"
                    onclick="${hasAudio ? `App.playEpisode(${ep.id})` : ''}">
              ${hasAudio ? `<svg class="btn-icon" viewBox="0 0 24 24" fill="currentColor"><polygon points="8,5 20,12 8,19"/></svg> Play (${ep.duration})` : 'Audio Coming Soon'}
            </button>
            <div class="card-action-btns">
              <button class="dl-btn" onclick="App.viewScript(${ep.id})" title="Read Script">${ICONS.script}</button>
              <button class="share-btn" onclick="App.shareEpisode(${ep.id})" title="Share">${ICONS.share}</button>
              <div class="ep-menu-wrap">
                <button class="ep-menu-btn" onclick="event.stopPropagation(); App.toggleEpMenu(${ep.id})">${ICONS.dots}</button>
                ${this._openMenuId === ep.id ? this._renderEpMenu(ep.id) : ''}
              </div>
            </div>
          </div>
        </div>`;
    });

    container.innerHTML = html;
  },

  // ── Render School ──
  renderSchool() {
    const container = document.getElementById('schoolList');
    if (!container) return;

    if (!this.schoolEpisodes.length) {
      container.innerHTML = '<div class="empty-state">Curriculum lessons coming soon!</div>';
      return;
    }

    // Group by unit
    const units = {};
    this.schoolEpisodes.forEach(ep => {
      const unit = ep.unit || 'General';
      if (!units[unit]) units[unit] = [];
      units[unit].push(ep);
    });

    let html = '';
    Object.keys(units).forEach(unitName => {
      const lessons = units[unitName];
      const completed = lessons.filter(l => this.isListened(l.id)).length;
      const total = lessons.length;
      const pct = total > 0 ? Math.round((completed / total) * 100) : 0;

      html += `
        <div class="school-unit">
          <div class="school-unit-header">
            <div class="school-unit-title">${unitName}</div>
            <div class="school-unit-meta">
              <span>${completed}/${total} lessons done</span>
              <span>${pct}%</span>
            </div>
            <div class="school-progress-bar">
              <div class="school-progress-fill" style="width:${pct}%"></div>
            </div>
          </div>`;

      lessons.forEach(ep => {
        const done = this.isListened(ep.id);
        const hasAudio = ep.file !== null;
        html += `
          <div class="school-lesson">
            <div class="school-lesson-num ${done ? 'done' : ''}" onclick="${hasAudio ? `App.playEpisode(${ep.id})` : ''}">${done ? '<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>' : ep.lessonNumber || '?'}</div>
            <div class="school-lesson-info" onclick="${hasAudio ? `App.playEpisode(${ep.id})` : ''}">
              <div class="school-lesson-title">${ep.title}</div>
              <div class="school-lesson-sub">${ep.subtitle || ep.description || ''}</div>
            </div>
            <div class="school-lesson-actions">
              <span class="school-lesson-dur">${hasAudio ? ep.duration : 'Soon'}</span>
              <div class="card-action-btns-inline">
                <button class="share-btn-sm" onclick="event.stopPropagation(); App.shareEpisode(${ep.id})" title="Share">${ICONS.share}</button>
                <button class="share-btn-sm" onclick="event.stopPropagation(); App.toggleEpMenu(${ep.id})" title="More">${ICONS.dots}</button>
              </div>
            </div>
          </div>`;
      });

      html += '</div>';
    });

    container.innerHTML = html;
  },

  // ── Render Together ──
  renderTogether() {
    const container = document.getElementById('togetherList');
    if (!container) return;

    if (!this.togetherEpisodes.length) {
      container.innerHTML = '<div class="empty-state">Couples devotionals coming soon!</div>';
      return;
    }

    let html = '';
    this.togetherEpisodes.forEach(ep => {
      const d = new Date(ep.date + 'T12:00:00');
      const dayNames = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
      const dayName = dayNames[d.getDay()];
      const hasAudio = ep.file !== null;
      const listened = this.isListened(ep.id);

      // Find the connected study episode
      const studyEp = this.episodes.find(e => e.date === ep.date);
      const connectedTitle = studyEp ? studyEp.title : '';

      html += `
        <div class="together-card ${listened ? 'listened' : ''}">
          <div class="together-date">${dayName}, ${this._monthNames[d.getMonth()]} ${d.getDate()}</div>
          <div class="together-title">${ep.title}</div>
          ${connectedTitle ? `<div class="together-connected">Connected to: "${connectedTitle}"</div>` : ''}
          <div class="together-scripture">${ep.subtitle || 'Read together'}</div>
          ${ep.reflectionPrompt ? `
            <div class="together-reflect">
              <div class="together-reflect-label">Reflect Together</div>
              <div class="together-reflect-text">"${ep.reflectionPrompt}"</div>
            </div>
          ` : ''}
          ${ep.prayerFocus ? `
            <div class="together-prayer">${ep.prayerFocus}</div>
          ` : ''}
          <pre class="script-view" id="script-${ep.id}"></pre>
          <div class="together-actions">
            <button class="together-play-btn ${hasAudio ? '' : 'no-audio'}"
                    onclick="${hasAudio ? `App.playEpisode(${ep.id})` : ''}">
              ${hasAudio ? `<svg class="btn-icon" viewBox="0 0 24 24" fill="currentColor"><polygon points="8,5 20,12 8,19"/></svg> Listen (${ep.duration})` : 'Audio Coming Soon'}
            </button>
            <div class="card-action-btns">
              <button class="dl-btn" onclick="App.viewScript(${ep.id})" title="Read Script">${ICONS.script}</button>
              <button class="share-btn" onclick="App.shareEpisode(${ep.id})" title="Share">${ICONS.share}</button>
              <div class="ep-menu-wrap">
                <button class="ep-menu-btn" onclick="event.stopPropagation(); App.toggleEpMenu(${ep.id})">${ICONS.dots}</button>
                ${this._openMenuId === ep.id ? this._renderEpMenu(ep.id) : ''}
              </div>
            </div>
          </div>
        </div>`;
    });

    container.innerHTML = html;
  },

  // ── Render Personal Growth ──
  renderPersonal() {
    const container = document.getElementById('personalList');
    if (!container) return;

    if (!this.personalEpisodes.length) {
      container.innerHTML = '<div class="empty-state">Personal growth content coming soon!</div>';
      return;
    }

    const typeBadges = { reading: 'Reading', pastoral: 'Pastoral', theological: 'Theological' };
    const typeClasses = { reading: 'badge-reading', pastoral: 'badge-pastoral', theological: 'badge-theological' };

    let html = '';
    this.personalEpisodes.forEach(ep => {
      const d = new Date(ep.date + 'T12:00:00');
      const dayNames = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
      const dayName = dayNames[d.getDay()];
      const hasAudio = ep.file !== null;
      const listened = this.isListened(ep.id);
      const pType = ep.personalType || 'reading';
      const badge = typeBadges[pType] || pType;
      const badgeCls = typeClasses[pType] || '';

      html += `
        <div class="personal-card ${listened ? 'listened' : ''}">
          <div class="personal-header">
            <div class="personal-date">${dayName}, ${this._monthNames[d.getMonth()]} ${d.getDate()}</div>
            <span class="personal-badge ${badgeCls}">${badge}</span>
          </div>
          <div class="personal-title">${ep.title}</div>
          <div class="personal-subtitle">${ep.subtitle || ''}</div>
          ${ep.description ? `<div class="personal-desc">${ep.description}</div>` : ''}
          <pre class="script-view" id="script-${ep.id}"></pre>
          <div class="personal-actions">
            <button class="personal-play-btn ${hasAudio ? '' : 'no-audio'}"
                    onclick="${hasAudio ? `App.playEpisode(${ep.id})` : ''}">
              ${hasAudio ? `<svg class="btn-icon" viewBox="0 0 24 24" fill="currentColor"><polygon points="8,5 20,12 8,19"/></svg> Listen (${ep.duration})` : 'Coming Soon'}
            </button>
            <div class="card-action-btns">
              <button class="dl-btn" onclick="App.viewScript(${ep.id})" title="Read Script">${ICONS.script}</button>
              <button class="share-btn" onclick="App.shareEpisode(${ep.id})" title="Share">${ICONS.share}</button>
              <div class="ep-menu-wrap">
                <button class="ep-menu-btn" onclick="event.stopPropagation(); App.toggleEpMenu(${ep.id})">${ICONS.dots}</button>
                ${this._openMenuId === ep.id ? this._renderEpMenu(ep.id) : ''}
              </div>
            </div>
          </div>
        </div>`;
    });

    container.innerHTML = html;
  },

  // ── Render Calendar ──
  renderCalendar() {
    const grid = document.getElementById('calGrid');
    if (!grid) return;

    const { year, month } = this.currentMonth;
    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const today = new Date();
    const todayDate = today.getFullYear() === year && today.getMonth() === month ? today.getDate() : -1;

    // Build episode lookup by day number
    const epByDay = {};
    this.episodes.forEach(ep => {
      if (!ep.date) return;
      const d = new Date(ep.date + 'T12:00:00');
      if (d.getMonth() === month && d.getFullYear() === year) {
        epByDay[d.getDate()] = ep;
      }
    });

    let html = '';

    // Empty cells before the 1st
    for (let i = 0; i < firstDay; i++) {
      html += '<div class="cal-day empty"></div>';
    }

    // Day cells
    for (let day = 1; day <= daysInMonth; day++) {
      const ep = epByDay[day];
      const isToday = day === todayDate;
      const isSelected = this._selectedCalDay === day;

      let dotClass = '';
      if (ep) {
        if (this.isListened(ep.id)) {
          dotClass = 'done';
        } else if (this.getPosition(ep.id) > 0) {
          dotClass = 'in-progress';
        } else {
          dotClass = 'unplayed';
        }
      }

      html += `<div class="cal-day ${isToday ? 'today' : ''} ${isSelected ? 'selected' : ''} ${ep ? 'has-ep' : ''}"
                   onclick="App.selectCalDay(${day})">
        <span class="cal-day-num">${day}</span>
        ${ep ? `<span class="cal-dot ${dotClass}"></span>` : ''}
      </div>`;
    }

    grid.innerHTML = html;

    // If a day was previously selected, show its detail
    if (this._selectedCalDay) {
      this.showCalDetail(this._selectedCalDay);
    }
  },

  selectCalDay(day) {
    this._selectedCalDay = day;
    this.renderCalendar();
    this.showCalDetail(day);
  },

  showCalDetail(day) {
    const detail = document.getElementById('calDetail');
    if (!detail) return;

    const ep = this.episodes.find(e => {
      if (!e.date) return false;
      const d = new Date(e.date + 'T12:00:00');
      return d.getDate() === day && d.getMonth() === this.currentMonth.month && d.getFullYear() === this.currentMonth.year;
    });

    if (!ep) {
      detail.innerHTML = '<div class="cal-detail-empty">No episode on this day</div>';
      return;
    }

    const listened = this.isListened(ep.id);
    const progress = this.getProgress(ep);
    const isPlaying = this.currentEp && this.currentEp.id === ep.id;
    const seriesClass = this.getSeriesClass(ep.series);
    const dayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    const d = new Date(ep.date + 'T12:00:00');
    const dayName = dayNames[d.getDay()];

    let statusText = '';
    let statusClass = '';
    if (listened) {
      statusText = 'Completed';
      statusClass = 'done';
    } else if (progress > 0) {
      statusText = `${progress}% complete`;
      statusClass = 'in-progress';
    } else {
      statusText = 'Not started';
      statusClass = 'unplayed';
    }

    detail.innerHTML = `
      <div class="cal-ep-card ${isPlaying ? 'playing' : ''}" onclick="App.playEpisode(${ep.id})">
        <div class="cal-ep-header">
          <div class="cal-ep-date">${dayName}, ${this._monthNames[this.currentMonth.month]} ${day}</div>
          <span class="cal-ep-status ${statusClass}">${statusText}</span>
        </div>
        <div class="cal-ep-title">${ep.title}</div>
        <div class="cal-ep-subtitle">${ep.subtitle || ''}</div>
        <div class="cal-ep-meta">
          <span class="ep-badge ${seriesClass}">${ep.series || 'General'}</span>
          <span class="cal-ep-dur">${ep.duration}</span>
        </div>
        ${ep.description ? `<div class="cal-ep-desc">${ep.description}</div>` : ''}
        <button class="cal-ep-play" onclick="event.stopPropagation(); App.playEpisode(${ep.id})">
          ${isPlaying && !this.audio.paused ? 'Now Playing' : listened ? 'Replay' : progress > 0 ? 'Resume' : 'Play Episode'}
        </button>
        ${progress > 0 || listened ? `<div class="ep-progress ${listened ? 'done' : ''}"><div class="ep-progress-fill" style="width:${listened ? 100 : progress}%"></div></div>` : ''}
      </div>`;
  },

  // ── Section Tabs & Calendars (Family, School, Together, Growth) ──
  _sectionCalSelected: {},

  switchSectionTab(section, tab) {
    const view = document.getElementById(section + 'View');
    if (!view) return;
    // Toggle tab buttons
    view.querySelectorAll('.tab').forEach(t => t.classList.toggle('active', t.dataset.view === tab));
    // Toggle view panels
    view.querySelectorAll('.view').forEach(v => v.classList.toggle('active', v.dataset.tabView === tab));
    if (tab === 'calendar') this.renderSectionCalendar(section);
  },

  _getSectionEpisodes(section) {
    const map = { family: this.familyEpisodes, school: this.schoolEpisodes, together: this.togetherEpisodes, personal: this.personalEpisodes };
    return map[section] || [];
  },

  renderSectionCalendar(section) {
    const grid = document.getElementById(section + 'CalGrid');
    if (!grid) return;
    const { year, month } = this.currentMonth;
    // Update month label
    const label = document.getElementById(section + 'CalMonthLabel');
    if (label) label.textContent = `${this._monthNames[month]} ${year}`;
    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const today = new Date();
    const todayDate = today.getFullYear() === year && today.getMonth() === month ? today.getDate() : -1;
    const eps = this._getSectionEpisodes(section);
    const epByDay = {};
    eps.forEach(ep => {
      if (!ep.date) return;
      const d = new Date(ep.date + 'T12:00:00');
      if (d.getMonth() === month && d.getFullYear() === year) epByDay[d.getDate()] = ep;
    });
    let html = '';
    for (let i = 0; i < firstDay; i++) html += '<div class="cal-day empty"></div>';
    const selDay = this._sectionCalSelected[section];
    for (let day = 1; day <= daysInMonth; day++) {
      const ep = epByDay[day];
      const isToday = day === todayDate;
      const isSelected = selDay === day;
      let dotClass = '';
      if (ep) {
        if (this.isListened(ep.id)) dotClass = 'done';
        else if (this.getPosition(ep.id) > 0) dotClass = 'in-progress';
        else dotClass = 'unplayed';
      }
      html += `<div class="cal-day ${isToday ? 'today' : ''} ${isSelected ? 'selected' : ''} ${ep ? 'has-ep' : ''}"
                   onclick="App.selectSectionCalDay('${section}',${day})">
        <span class="cal-day-num">${day}</span>
        ${ep ? `<span class="cal-dot ${dotClass}"></span>` : ''}
      </div>`;
    }
    grid.innerHTML = html;
    if (selDay) this.showSectionCalDetail(section, selDay);
  },

  selectSectionCalDay(section, day) {
    this._sectionCalSelected[section] = day;
    this.renderSectionCalendar(section);
  },

  showSectionCalDetail(section, day) {
    const detail = document.getElementById(section + 'CalDetail');
    if (!detail) return;
    const eps = this._getSectionEpisodes(section);
    const ep = eps.find(e => {
      if (!e.date) return false;
      const d = new Date(e.date + 'T12:00:00');
      return d.getDate() === day && d.getMonth() === this.currentMonth.month && d.getFullYear() === this.currentMonth.year;
    });
    if (!ep) { detail.innerHTML = '<div class="cal-detail-empty">No episode on this day</div>'; return; }
    const listened = this.isListened(ep.id);
    const progress = this.getProgress(ep);
    const isPlaying = this.currentEp && this.currentEp.id === ep.id;
    const hasAudio = !!ep.file;
    const dayNames = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
    const d = new Date(ep.date + 'T12:00:00');
    const dayName = dayNames[d.getDay()];
    let statusText = listened ? 'Completed' : progress > 0 ? `${progress}% complete` : 'Not started';
    let statusClass = listened ? 'done' : progress > 0 ? 'in-progress' : 'unplayed';
    detail.innerHTML = `
      <div class="cal-ep-card ${isPlaying ? 'playing' : ''}" onclick="${hasAudio ? `App.playEpisode(${ep.id})` : ''}">
        <div class="cal-ep-header">
          <div class="cal-ep-date">${dayName}, ${this._monthNames[this.currentMonth.month]} ${day}</div>
          <span class="cal-ep-status ${statusClass}">${statusText}</span>
        </div>
        <div class="cal-ep-title">${ep.title}</div>
        <div class="cal-ep-subtitle">${ep.subtitle || ''}</div>
        <div class="cal-ep-meta"><span class="cal-ep-dur">${ep.duration || ''}</span></div>
        ${hasAudio ? `<button class="cal-ep-play" onclick="event.stopPropagation(); App.playEpisode(${ep.id})">
          ${isPlaying && !this.audio.paused ? 'Now Playing' : listened ? 'Replay' : progress > 0 ? 'Resume' : 'Play Episode'}
        </button>` : '<div class="cal-detail-empty" style="padding:8px 0;font-size:12px;">Audio coming soon</div>'}
      </div>`;
  },

  // ── Master Calendar ──
  _masterCalDay: null,
  _sectionColors: {
    study: '#3574cc',
    family: '#e67e22',
    school: '#9b59b6',
    together: '#e74c3c',
    personal: '#d4a23c'
  },
  _sectionLabels: {
    study: 'Study',
    family: 'Family',
    school: 'School',
    together: 'Together',
    personal: 'Growth'
  },

  openMasterCalendar() {
    document.getElementById('masterCalOverlay').classList.add('open');
    this._masterCalDay = null;
    this.renderMasterCalendar();
  },

  closeMasterCalendar() {
    document.getElementById('masterCalOverlay').classList.remove('open');
  },

  renderMasterCalendar() {
    const grid = document.getElementById('masterCalGrid');
    const detail = document.getElementById('masterCalDetail');
    if (!grid) return;

    const { year, month } = this.currentMonth;
    document.getElementById('masterCalMonth').textContent = `${this._monthNames[month]} ${year}`;

    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const today = new Date();
    const todayDate = today.getFullYear() === year && today.getMonth() === month ? today.getDate() : -1;

    // Build per-day data for all sections
    const allSections = {
      study: this.episodes,
      family: this.familyEpisodes,
      school: this.schoolEpisodes,
      together: this.togetherEpisodes,
      personal: this.personalEpisodes
    };

    const dayData = {}; // day -> { section: ep }
    for (const [section, eps] of Object.entries(allSections)) {
      (eps || []).forEach(ep => {
        if (!ep.date) return;
        const d = new Date(ep.date + 'T12:00:00');
        if (d.getMonth() === month && d.getFullYear() === year) {
          const day = d.getDate();
          if (!dayData[day]) dayData[day] = {};
          dayData[day][section] = ep;
        }
      });
    }

    let html = '';
    for (let i = 0; i < firstDay; i++) html += '<div class="mc-day empty"><span class="mc-day-num"></span></div>';

    for (let day = 1; day <= daysInMonth; day++) {
      const isToday = day === todayDate;
      const isSelected = this._masterCalDay === day;
      const sections = dayData[day] || {};
      const sectionKeys = Object.keys(sections);

      let dotsHtml = '';
      if (sectionKeys.length) {
        dotsHtml = '<div class="mc-dots">';
        sectionKeys.forEach(s => {
          dotsHtml += `<span class="mc-section-dot" style="background:${this._sectionColors[s]}"></span>`;
        });
        dotsHtml += '</div>';
      }

      html += `<div class="mc-day ${isToday ? 'today' : ''} ${isSelected ? 'selected' : ''}" onclick="App.selectMasterCalDay(${day})">
        <span class="mc-day-num">${day}</span>
        ${dotsHtml}
      </div>`;
    }

    grid.innerHTML = html;

    // Show detail if day is selected
    if (this._masterCalDay && dayData[this._masterCalDay]) {
      this.showMasterCalDetail(this._masterCalDay, dayData[this._masterCalDay]);
    } else {
      detail.innerHTML = '';
    }
  },

  selectMasterCalDay(day) {
    this._masterCalDay = day;
    this.renderMasterCalendar();
  },

  showMasterCalDetail(day, sections) {
    const detail = document.getElementById('masterCalDetail');
    if (!detail) return;
    const dayNames = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
    const d = new Date(this.currentMonth.year, this.currentMonth.month, day);
    const dayName = dayNames[d.getDay()];

    let html = `<div style="font-size:12px;font-weight:700;color:var(--text2);padding:4px 0 8px;text-transform:uppercase;letter-spacing:0.5px;">${dayName}, ${this._monthNames[this.currentMonth.month]} ${day}</div>`;

    for (const [section, ep] of Object.entries(sections)) {
      const color = this._sectionColors[section];
      const label = this._sectionLabels[section];
      html += `<div class="mc-detail-card" onclick="App.closeMasterCalendar(); App.playEpisode(${ep.id})">
        <span class="mc-detail-dot" style="background:${color}"></span>
        <div class="mc-detail-info">
          <div class="mc-detail-section" style="color:${color}">${label}</div>
          <div class="mc-detail-title">${ep.title}</div>
        </div>
        <span class="mc-detail-dur">${ep.duration || ''}</span>
      </div>`;
    }

    detail.innerHTML = html;
  },

  // ── Episode Menu (three-dot) ──
  _renderEpMenu(id) {
    const isFav = this._favorites.includes(id);
    const ep = this.allEpisodes.find(e => e.id === id);
    const hasAudio = ep && ep.file;
    return `<div class="ep-menu-dropdown" onclick="event.stopPropagation()">
      <button class="ep-menu-item" onclick="App.toggleSummary(${id}); App.closeEpMenu()">
        ${ICONS.info} <span>Info</span>
      </button>
      <button class="ep-menu-item" onclick="App.viewScript(${id}); App.closeEpMenu()">
        ${ICONS.script} <span>Read Script</span>
      </button>
      <button class="ep-menu-item" onclick="App.shareEpisode(${id}); App.closeEpMenu()">
        ${ICONS.share} <span>Share</span>
      </button>
      <button class="ep-menu-item ${isFav ? 'fav-active' : ''}" onclick="App.toggleFavorite(${id})">
        ${isFav ? ICONS.starFilled : ICONS.starOutline} <span>${isFav ? 'Unfavorite' : 'Favorite'}</span>
      </button>
      ${hasAudio ? `<button class="ep-menu-item" onclick="App.downloadAudio(${id}); App.closeEpMenu()">
        ${ICONS.download} <span>Download</span>
      </button>` : ''}
    </div>`;
  },

  toggleEpMenu(id) {
    if (this._openMenuId === id) {
      this.closeEpMenu();
    } else {
      this._openMenuId = id;
      this.reRenderAll();
    }
  },

  closeEpMenu() {
    if (this._openMenuId !== null) {
      this._openMenuId = null;
      this.reRenderAll();
    }
  },

  toggleFavorite(id) {
    const idx = this._favorites.indexOf(id);
    if (idx >= 0) {
      this._favorites.splice(idx, 1);
      this.showToast('Removed from favorites');
    } else {
      this._favorites.push(id);
      this.showToast('Added to favorites ⭐');
    }
    localStorage.setItem('pg_favorites', JSON.stringify(this._favorites));
    this._openMenuId = null;
    this.reRenderAll();
  },

  // ── Player Setup ──
  setupPlayer() {
    const progressBar = document.querySelector('.mp-progress');
    const fill = document.getElementById('mpFill');

    this.audio.addEventListener('timeupdate', () => {
      if (!this.audio.duration) return;
      const pct = (this.audio.currentTime / this.audio.duration) * 100;

      // Mini player
      fill.style.width = pct + '%';
      document.getElementById('mpSub').textContent =
        this.formatTime(this.audio.currentTime) + ' / ' + this.formatTime(this.audio.duration);

      // Now playing
      if (this.npOpen) {
        document.getElementById('npTrackFill').style.width = pct + '%';
        document.getElementById('npThumb').style.left = pct + '%';
        document.getElementById('npElapsed').textContent = this.formatTime(this.audio.currentTime);
        document.getElementById('npRemain').textContent = '-' + this.formatTime(this.audio.duration - this.audio.currentTime);
      }

      // Save position every 5 seconds
      if (this.currentEp && Math.floor(this.audio.currentTime) % 5 === 0) {
        this.savePosition(this.currentEp.id, this.audio.currentTime);
      }

      // Update media session position
      this.updateMediaPosition();
    });

    this.audio.addEventListener('ended', () => {
      if (this.currentEp) {
        this.markListened(this.currentEp.id);
        this.recordListenDate();
        this.updateStreak();
        this.reRenderAll();
      }

      // Sleep timer: end of episode
      if (this.sleepEnd === 'episode') {
        this.sleepEnd = null;
        this.updatePlayBtn(false);
        return;
      }

      // Autoplay next — find next episode in the same section
      if (this.autoplay && this.currentEp) {
        const lists = [this.episodes, this.familyEpisodes, this.schoolEpisodes, this.togetherEpisodes, this.personalEpisodes];
        for (const list of lists) {
          const idx = list.findIndex(e => e.id === this.currentEp.id);
          if (idx >= 0 && idx < list.length - 1) {
            this.playEpisode(list[idx + 1].id);
            break;
          }
        }
      }
    });

    // Mini player progress scrub
    progressBar.addEventListener('click', (e) => {
      if (!this.audio.duration) return;
      const rect = progressBar.getBoundingClientRect();
      const pct = (e.clientX - rect.left) / rect.width;
      this.audio.currentTime = Math.max(0, Math.min(this.audio.duration, pct * this.audio.duration));
    });
  },

  // ── Play Episode ──
  playEpisode(id) {
    const ep = this.allEpisodes.find(e => e.id === id);
    if (!ep || !ep.file) return;  // Don't play if no audio file

    this.currentEp = ep;
    this.audio.src = '../' + ep.file;
    this.audio.playbackRate = this.speeds[this.speedIdx];

    const saved = this.getPosition(id);
    if (saved > 0) {
      this.audio.currentTime = saved;
    }

    this.audio.play();

    // Show mini player
    document.getElementById('miniPlayer').classList.add('visible');
    document.getElementById('mpTitle').textContent = ep.title;
    document.getElementById('mpSub').textContent = '0:00 / ' + ep.duration;
    this.updatePlayBtn(true);

    // Update episode cards
    this.renderEpisodes();

    // Update now playing if open
    if (this.npOpen) this.updateNowPlaying();

    // Media Session
    this.updateMediaSession();

    // Save state
    this.saveState();

    // Record listen date for streak
    this.recordListenDate();
  },

  togglePlay() {
    if (this.audio.paused) {
      this.audio.play();
      this.updatePlayBtn(true);
    } else {
      this.audio.pause();
      this.updatePlayBtn(false);
    }
  },

  updatePlayBtn(playing) {
    const playIcon = '<svg viewBox="0 0 24 24" fill="currentColor"><polygon points="8,5 20,12 8,19"/></svg>';
    const pauseIcon = '<svg viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/></svg>';

    document.getElementById('mpPlayBtn').innerHTML = playing ? pauseIcon : playIcon;
    if (document.getElementById('npPlayBtn')) {
      document.getElementById('npPlayBtn').innerHTML = playing ? pauseIcon : playIcon;
    }
  },

  cycleSpeed() {
    this.speedIdx = (this.speedIdx + 1) % this.speeds.length;
    const speed = this.speeds[this.speedIdx];
    this.audio.playbackRate = speed;

    const label = speed + 'x';
    document.getElementById('npSpeedTop').textContent = label;
    if (document.getElementById('npSpeed')) {
      document.getElementById('npSpeed').textContent = label;
    }
    const mpLabel = document.getElementById('mpSpeedLabel');
    if (mpLabel) mpLabel.textContent = label;

    localStorage.setItem('speed', this.speedIdx.toString());
  },

  skipBack() {
    this.audio.currentTime = Math.max(0, this.audio.currentTime - 15);
  },

  skipForward() {
    this.audio.currentTime = Math.min(this.audio.duration || 0, this.audio.currentTime + 30);
  },

  // ── Now Playing ──
  toggleMiniPlayer() {
    const mp = document.getElementById('miniPlayer');
    if (mp) mp.classList.toggle('collapsed');
  },

  openNowPlaying() {
    if (!this.currentEp) return;
    this.npOpen = true;
    document.getElementById('nowPlaying').classList.add('open');
    this.updateNowPlaying();
  },

  closeNowPlaying() {
    this.npOpen = false;
    document.getElementById('nowPlaying').classList.remove('open');
  },

  updateNowPlaying() {
    if (!this.currentEp) return;
    document.getElementById('npTitle').textContent = this.currentEp.title;
    document.getElementById('npSeries').textContent = this.currentEp.series || '';
    document.getElementById('npDesc').textContent = this.currentEp.description || '';

    // Update speed display
    document.getElementById('npSpeedTop').textContent = this.speeds[this.speedIdx] + 'x';

    // Update autoplay
    document.getElementById('npAutoText').textContent = 'Auto: ' + (this.autoplay ? 'On' : 'Off');

    // Update times
    if (this.audio.duration) {
      const pct = (this.audio.currentTime / this.audio.duration) * 100;
      document.getElementById('npTrackFill').style.width = pct + '%';
      document.getElementById('npThumb').style.left = pct + '%';
      document.getElementById('npElapsed').textContent = this.formatTime(this.audio.currentTime);
      document.getElementById('npRemain').textContent = '-' + this.formatTime(this.audio.duration - this.audio.currentTime);
    }
  },

  setupNowPlaying() {
    // Swipe down to dismiss
    const np = document.getElementById('nowPlaying');
    let startY = 0, currentY = 0, isDragging = false;

    np.addEventListener('touchstart', (e) => {
      const scroll = np.querySelector('.np-scroll');
      if (scroll.scrollTop > 0) return;
      startY = e.touches[0].clientY;
      currentY = startY;
      isDragging = false;
      np.style.transition = 'none';
    }, { passive: true });

    np.addEventListener('touchmove', (e) => {
      currentY = e.touches[0].clientY;
      const delta = currentY - startY;
      if (delta < 10) return;
      isDragging = true;
      np.style.transform = `translateY(${delta}px)`;
    }, { passive: true });

    np.addEventListener('touchend', () => {
      np.style.transition = '';
      const delta = currentY - startY;
      if (isDragging && delta > 100) {
        this.closeNowPlaying();
      }
      np.style.transform = this.npOpen && !(isDragging && delta > 100) ? 'translateY(0)' : '';
    });

    // NP progress bar scrub
    const npTrack = document.getElementById('npTrack');
    let scrubbing = false;

    const scrub = (clientX) => {
      if (!this.audio.duration) return;
      const rect = npTrack.getBoundingClientRect();
      const pct = Math.max(0, Math.min(1, (clientX - rect.left) / rect.width));
      this.audio.currentTime = pct * this.audio.duration;

      document.getElementById('npTrackFill').style.width = (pct * 100) + '%';
      document.getElementById('npThumb').style.left = (pct * 100) + '%';
      document.getElementById('npElapsed').textContent = this.formatTime(this.audio.currentTime);
      document.getElementById('npRemain').textContent = '-' + this.formatTime(this.audio.duration - this.audio.currentTime);
    };

    npTrack.addEventListener('touchstart', (e) => {
      scrubbing = true;
      scrub(e.touches[0].clientX);
    });

    npTrack.addEventListener('touchmove', (e) => {
      if (scrubbing) {
        e.preventDefault();
        scrub(e.touches[0].clientX);
      }
    }, { passive: false });

    npTrack.addEventListener('touchend', () => { scrubbing = false; });
    npTrack.addEventListener('click', (e) => { scrub(e.clientX); });
  },

  // ── Sleep Timer ──
  openSleepModal() {
    document.getElementById('sleepModal').classList.add('open');
    document.getElementById('sleepCancelBtn').style.display = this.sleepEnd ? '' : 'none';
  },

  closeSleepModal() {
    document.getElementById('sleepModal').classList.remove('open');
  },

  setSleep(minutes) {
    // Clear existing
    if (this.sleepTimer) {
      clearTimeout(this.sleepTimer);
      this.sleepTimer = null;
    }

    if (minutes === 0) {
      // Cancel
      this.sleepEnd = null;
      document.getElementById('npSleepText').textContent = 'Sleep Timer';
      this.closeSleepModal();
      return;
    }

    if (minutes === -1) {
      // End of episode
      this.sleepEnd = 'episode';
      document.getElementById('npSleepText').textContent = 'End of episode';
      this.closeSleepModal();
      return;
    }

    this.sleepEnd = Date.now() + minutes * 60 * 1000;
    this.sleepTimer = setTimeout(() => {
      this.audio.pause();
      this.updatePlayBtn(false);
      this.sleepEnd = null;
      this.sleepTimer = null;
      document.getElementById('npSleepText').textContent = 'Sleep Timer';
    }, minutes * 60 * 1000);

    document.getElementById('npSleepText').textContent = minutes + ' min';
    this.closeSleepModal();

    // Update display periodically
    this.updateSleepDisplay();
  },

  updateSleepDisplay() {
    if (!this.sleepEnd || this.sleepEnd === 'episode') return;
    const remaining = Math.max(0, Math.ceil((this.sleepEnd - Date.now()) / 60000));
    document.getElementById('npSleepText').textContent = remaining > 0 ? remaining + ' min' : 'Sleep Timer';
    if (remaining > 0) {
      setTimeout(() => this.updateSleepDisplay(), 30000);
    }
  },

  toggleSleepTimer() {
    this.openSleepModal();
  },

  // ── Autoplay ──
  toggleAutoplay() {
    this.autoplay = !this.autoplay;
    localStorage.setItem('autoplay', this.autoplay ? '1' : '0');
    document.getElementById('npAutoText').textContent = 'Auto: ' + (this.autoplay ? 'On' : 'Off');
  },

  // ── Streak ──
  updateStreak() {
    const dates = JSON.parse(localStorage.getItem('listenDates') || '[]');
    if (!dates.length) {
      document.getElementById('streak').classList.remove('visible');
      return;
    }

    const uniqueDates = [...new Set(dates)].sort().reverse();
    const today = new Date().toISOString().split('T')[0];

    let streak = 0;
    let checkDate = new Date();

    // Start from today or yesterday
    if (!uniqueDates.includes(today)) {
      checkDate.setDate(checkDate.getDate() - 1);
    }

    while (true) {
      const ds = checkDate.toISOString().split('T')[0];
      if (uniqueDates.includes(ds)) {
        streak++;
        checkDate.setDate(checkDate.getDate() - 1);
      } else {
        break;
      }
    }

    document.getElementById('streakCount').textContent = streak;
    document.getElementById('streak').classList.toggle('visible', streak > 0);
  },

  recordListenDate() {
    const today = new Date().toISOString().split('T')[0];
    const dates = JSON.parse(localStorage.getItem('listenDates') || '[]');
    if (!dates.includes(today)) {
      dates.push(today);
      localStorage.setItem('listenDates', JSON.stringify(dates));
    }
  },

  // ── Scroll to next unplayed ──
  scrollToNext() {
    setTimeout(() => {
      const next = this.episodes.find(ep => !this.isListened(ep.id));
      if (next) {
        const card = document.querySelector(`.episode-card[data-id="${next.id}"]`);
        if (card) {
          card.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      }
    }, 400);
  },

  // ── Chat ──
  askSuggestion(btn) {
    const textSpan = btn.querySelector('.suggestion-text');
    const text = textSpan ? textSpan.textContent.trim() : btn.textContent.trim();
    this.sendChat(text);
  },

  // ── Puritan Counsel System ──
  _stopWords: new Set([
    'a','an','the','is','are','was','were','be','been','being','have','has','had',
    'do','does','did','will','would','shall','should','may','might','must','can',
    'could','i','me','my','mine','we','our','you','your','he','she','it','they',
    'them','his','her','its','their','this','that','these','those','am','im',
    'what','which','who','whom','how','when','where','why','about','to','for',
    'with','on','at','from','of','in','by','up','not','no','or','and','but',
    'if','then','so','than','too','very','just','also','more','some','any',
    'tell','please','help','know','think','want','need','like','really',
    'get','got','make','go','going','come','take','give','let','say','said',
    'thing','things','way','much','many','lot','lots','something','anything',
    'everything','nothing','well','good','great','right','okay','ok','sure',
    'hey','hi','hello','oh','um','uh','thanks','thank','hey','dear'
  ]),

  _synonymMap: {
    'sin': ['sin','sins','sinful','sinning','sinner','transgression','transgress','iniquity','wickedness','wicked','evil','fallen','depravity','depraved','corrupt','corruption','flesh','carnal'],
    'temptation': ['temptation','temptations','tempted','tempt','lust','lusts','desire','desires','enticement','entice','struggle','struggling','weakness','addicted','addiction'],
    'faith': ['faith','believe','belief','believing','trust','trusting','assurance','confidence','reliance','rely','cling','clinging'],
    'justification': ['justification','justified','justify','imputation','imputed','righteousness','righteous','declared','forensic','credited','reckoned','salvation','saved','born again','regeneration','converted','conversion'],
    'sanctification': ['sanctification','sanctified','sanctify','holiness','holy','godliness','godly','growth','growing','mature','maturity','progressive','mortification','mortify','vivification','conform','conformed','christlikeness','purity','pure','purify'],
    'prayer': ['prayer','prayers','pray','praying','intercession','intercede','supplication','petition','devotion','devotions','devotional','communion','communicate','talk to god','speaking to god'],
    'scripture': ['scripture','scriptures','bible','word of god','reading','read','study','studying','devotion','devotions','quiet time','meditation','meditate','meditating'],
    'suffering': ['suffering','suffer','suffers','pain','painful','trial','trials','tribulation','affliction','afflicted','hardship','difficulty','difficult','hard times','adversity','grief','grieve','grieving','loss','lost','mourning','mourn','hurt','hurting','broken','brokenhearted','sorrow','sorrowful','despair'],
    'doubt': ['doubt','doubts','doubting','uncertain','uncertainty','unsure','wavering','waver','questioning','question','struggle','confused','confusion','assurance','lack of faith','unbelief','anxious','anxiety','worried','worry','worrying','fear','fears','fearful','afraid','scared'],
    'joy': ['joy','joyful','joyous','happiness','happy','content','contentment','contented','satisfied','satisfaction','delight','delightful','cheerful','cheer','gladness','glad','peace','peaceful','blessed','blessing','blessings','grateful','gratitude','thankful','thanksgiving'],
    'sovereignty': ['sovereignty','sovereign','providence','providential','decree','decrees','ordain','ordained','control','controls','plan','purpose','purposes','will of god','gods will','divine will','omnipotent','omnipotence','almighty','throne','reign','reigns','rules','ruling'],
    'election': ['election','elect','chosen','predestination','predestined','foreknew','foreknowledge','calling','called','unconditional','irresistible','grace alone','chosen before','before the foundation','elected'],
    'trinity': ['trinity','triune','godhead','three persons','father son spirit','three in one','trinitarian'],
    'christ': ['christ','jesus','lord jesus','savior','saviour','redeemer','mediator','messiah','lamb','cross','crucified','crucifixion','atonement','atone','sacrifice','blood','resurrection','risen','incarnation','incarnate','god-man','son of god','son of man'],
    'spirit': ['spirit','holy spirit','holy ghost','paraclete','comforter','helper','indwelling','indwell','filling','filled','fruit of the spirit','gifts of the spirit','spiritual gifts','pneumatology'],
    'covenant': ['covenant','covenants','covenant theology','federal','promise','promises','testament','old testament','new testament','covenant of works','covenant of grace','covenant of redemption','pactum','federal theology'],
    'law': ['law','commandments','commandment','moral law','decalogue','ten commandments','obedience','obey','duty','duties','obligation','legalism','antinomian','third use','law and gospel','imperative'],
    'gospel': ['gospel','good news','grace','gracious','mercy','mercies','merciful','forgiveness','forgive','forgiven','pardon','pardoned','redemption','redeem','redeemed','free grace','unmerited','favor','cross','finished work'],
    'marriage': ['marriage','married','marry','husband','wife','spouse','wedding','matrimony','partner','helpmate','helpmeet','one flesh','love your wife','submit','headship'],
    'children': ['children','child','kids','kid','son','daughter','sons','daughters','parenting','parent','parents','raising','raise','train','training','nurture','discipline','disciplining','upbringing','family','families'],
    'family worship': ['family worship','family devotion','family devotions','household','family altar','family prayer','worship at home','devotions together','pray together','family bible'],
    'work': ['work','working','job','career','vocation','calling','occupation','labor','labour','employment','profession','workplace','office','diligence','diligent','lazy','laziness','sloth','idle','idleness'],
    'money': ['money','wealth','riches','rich','stewardship','steward','giving','tithe','tithing','generosity','generous','finances','financial','possessions','materialism','treasure','mammon','greed','greedy','covetous','contentment','poor','poverty'],
    'rest': ['rest','resting','sabbath','sabbath rest','lord\'s day','sunday','recreation','leisure','burnout','exhausted','tired','weary','weariness','refresh','refreshment','cease','ceasing'],
    'puritan': ['puritan','puritans','puritanism','reformed','reformation','reformers','pilgrim','pilgrims','nonconformist'],
    'owen': ['owen','john owen','mortification','indwelling sin','communion with god','owen on'],
    'edwards': ['edwards','jonathan edwards','sinners in the hands','religious affections','freedom of the will','northampton','great awakening','revival'],
    'watson': ['watson','thomas watson','body of divinity','divine cordial','all things for good','godly mans picture'],
    'baxter': ['baxter','richard baxter','reformed pastor','saints everlasting rest','christian directory'],
    'spurgeon': ['spurgeon','charles spurgeon','prince of preachers','metropolitan tabernacle','morning and evening','treasury of david','lectures to my students'],
    'bunyan': ['bunyan','john bunyan','pilgrims progress','pilgrim\'s progress','holy war','grace abounding','bedford','tinker'],
    'brooks': ['brooks','thomas brooks','precious remedies','against satan','smooth stones','unsearchable riches'],
    'books': ['books','book','reading list','recommend','recommended','recommendations','start','begin','beginning','library','read first','best puritan','essential'],
    'app': ['app','application','puritan gold','this app','use this','navigate','how to use','features','feature','help me use'],
    'study': ['study','today','daily','episode','episodes','listen','listening','what should','recommend','suggestion','devotional','lesson','curriculum'],
    'greeting': ['hello','hi','hey','greetings','good morning','good evening','good afternoon','howdy','welcome','peace'],
    'encourage': ['encourage','encouragement','encouraged','hope','hopeful','lift','uplifting','comfort','comforting','strengthen','strengthened']
  },

  _responses: [
    // ═══════════════════════════════════════
    // THEOLOGY & DOCTRINE (15 responses)
    // ═══════════════════════════════════════
    {
      id: 'justification',
      keywords: ['justification','justified','imputation','imputed','righteousness','declared','forensic','credited','reckoned','salvation','saved'],
      response: `Dear friend, justification is one of the most glorious truths in all of Scripture. It is the act whereby God, the righteous Judge, declares the ungodly sinner to be righteous in His sight -- not on the basis of anything we have done, but solely on the account of Christ's perfect righteousness imputed to us through faith. As Paul writes, "Therefore being justified by faith, we have peace with God through our Lord Jesus Christ" (Romans 5:1). Thomas Watson put it beautifully: "Justification is a judicial act of God, whereby He absolves a sinner and reckons him as righteous in His sight, for the sake of Christ's righteousness." Rest in this, friend: thy standing before God depends not on thy performance but on Christ's finished work. That is the ground of all thy peace.`
    },
    {
      id: 'sanctification',
      keywords: ['sanctification','sanctified','holiness','holy','godliness','growth','growing','mature','progressive','mortification','mortify','christlikeness','purity'],
      response: `Ah, sanctification -- the blessed work of God's Spirit making us more like Christ day by day. While justification is a single act declaring us righteous, sanctification is the ongoing process by which we are made righteous in practice. "Work out your own salvation with fear and trembling. For it is God which worketh in you both to will and to do of his good pleasure" (Philippians 2:12-13). John Owen taught that sanctification involves both mortification -- the putting to death of sin -- and vivification -- the enlivening of grace. It is hard work, dear friend, but take heart: it is God who works in thee. As the Puritans loved to say, we must use the means of grace diligently -- prayer, Scripture, fellowship, and the Lord's Supper -- trusting that God will complete the good work He has begun (Philippians 1:6).`
    },
    {
      id: 'sovereignty',
      keywords: ['sovereignty','sovereign','providence','providential','decree','ordain','control','plan','purpose','will of god','omnipotent','almighty','reign'],
      response: `Friend, there is no doctrine more comforting in all of life's storms than the absolute sovereignty of God. He is the King eternal, immortal, invisible -- and not a single sparrow falls to the ground apart from His will (Matthew 10:29). The Westminster Confession declares that God "from all eternity did, by the most wise and holy counsel of His own will, freely and unchangeably ordain whatsoever comes to pass." Thomas Watson wrote: "God's providence is His care over all His creatures, ordering all things to the best advantage for His glory and their good." Whatever thou art facing today, know this: thy heavenly Father holds all things in His hands, and He works all things together for good to them that love Him (Romans 8:28). Rest in His sovereign care.`
    },
    {
      id: 'trinity',
      keywords: ['trinity','triune','godhead','three persons','three in one','trinitarian'],
      response: `The doctrine of the Trinity is the very foundation of the Christian faith. We worship one God who eternally exists in three Persons -- Father, Son, and Holy Spirit -- each fully God, each distinct, yet one in essence. "Go ye therefore, and teach all nations, baptizing them in the name of the Father, and of the Son, and of the Holy Ghost" (Matthew 28:19). John Owen wrote with such depth on the believer's distinct communion with each Person of the Trinity: we approach the Father in love, the Son in grace, and the Spirit in comfort. This is not dry doctrine, dear friend -- it is the living heartbeat of our faith. Every prayer thou prayest is Trinitarian: the Spirit moves thy heart, thou prayest through the mediation of Christ, and thou addressest thy heavenly Father. What a privilege!`
    },
    {
      id: 'christ_person_work',
      keywords: ['christ','jesus','savior','redeemer','mediator','messiah','lamb','cross','crucified','atonement','sacrifice','blood','resurrection','incarnation','son of god'],
      response: `Dear friend, all of theology finds its center in the glorious Person and work of the Lord Jesus Christ. He is the eternal Son of God who took upon Himself our nature, lived the life we could not live, and died the death we deserved to die. "For there is one God, and one mediator between God and men, the man Christ Jesus; who gave himself a ransom for all" (1 Timothy 2:5-6). Charles Spurgeon proclaimed: "Christ is the great central fact in the world's history; to Him everything looks forward or backward." In Christ, dear friend, thou hast a Prophet to teach thee, a Priest to intercede for thee, and a King to rule and defend thee. Whatever thy need this day, look to Christ -- He is altogether sufficient.`
    },
    {
      id: 'holy_spirit',
      keywords: ['spirit','holy spirit','holy ghost','comforter','helper','indwelling','filling','fruit of the spirit','gifts','pneumatology'],
      response: `What a precious gift is the Holy Spirit -- the third Person of the blessed Trinity, sent by the Father and the Son to dwell within every true believer! "Know ye not that ye are the temple of God, and that the Spirit of God dwelleth in you?" (1 Corinthians 3:16). John Owen, whose work on the Holy Spirit remains unmatched, wrote extensively about the Spirit's work in regeneration, sanctification, and comfort. The Spirit illuminates Scripture so that it becomes alive to thee, He convicts thee of sin and draws thee to repentance, He assures thee of thy adoption, and He produces His blessed fruit in thy life -- love, joy, peace, and all the rest (Galatians 5:22-23). Pray daily for a fresh filling of the Spirit, friend, for He is the power by which we live the Christian life.`
    },
    {
      id: 'election',
      keywords: ['election','elect','chosen','predestination','predestined','foreknew','foreknowledge','calling','unconditional','irresistible'],
      response: `Dear friend, the doctrine of election is one that has caused much debate, yet the Puritans found it to be a fountain of the deepest comfort. Election means that before the foundation of the world, God chose a people for Himself in Christ -- not because of any foreseen merit in them, but solely according to the good pleasure of His will. "He hath chosen us in him before the foundation of the world, that we should be holy and without blame before him in love" (Ephesians 1:4). Jonathan Edwards taught that this doctrine, far from producing pride, produces the deepest humility -- for we owe everything to grace. If thou art in Christ, rejoice! Thy salvation rests not on the shifting sand of thy will but upon the eternal, unchangeable purpose of Almighty God.`
    },
    {
      id: 'covenant_theology',
      keywords: ['covenant','covenants','federal','promise','testament','covenant of works','covenant of grace','covenant of redemption'],
      response: `Covenant theology is the grand framework by which the Puritans understood the whole of Scripture. God has always dealt with His people by way of covenant -- a solemn bond sealed with promises. The covenant of works was made with Adam, requiring perfect obedience. When Adam failed, God in His mercy established the covenant of grace, promising salvation through faith in the coming Redeemer. "This is my blood of the new testament, which is shed for many for the remission of sins" (Matthew 26:28). The Puritans also spoke of the covenant of redemption -- that eternal pact between Father and Son, before all worlds, to save a people. Thomas Boston's work on covenant theology is rich and rewarding. Friend, know this: thy salvation rests upon nothing less than God's covenant faithfulness, and He cannot break His word.`
    },
    {
      id: 'means_of_grace',
      keywords: ['means of grace','ordinances','sacraments','lords supper','communion','baptism','preaching','word preached','corporate worship','church attendance','local church'],
      response: `The Puritans were deeply devoted to what they called "the means of grace" -- those ordinary channels through which God communicates His grace to our souls. These include the reading and preaching of God's Word, prayer, the sacraments of baptism and the Lord's Supper, and fellowship with other believers. "And they continued stedfastly in the apostles' doctrine and fellowship, and in breaking of bread, and in prayers" (Acts 2:42). Richard Baxter, in his Reformed Pastor, urged both ministers and laypeople to be diligent in these means. Dear friend, do not neglect the ordinary means of grace. God has promised to meet thee in His Word, at His table, and among His people. Be faithful in thy attendance upon these, and thou shalt find thy soul nourished and strengthened for the journey ahead.`
    },
    {
      id: 'law_and_gospel',
      keywords: ['law','commandments','moral law','decalogue','ten commandments','obedience','duty','legalism','antinomian','law and gospel'],
      response: `Understanding the relationship between law and gospel is essential to the Christian life. The Puritans taught that the moral law of God has three uses: first, as a mirror to show us our sin and drive us to Christ; second, as a restraint upon wickedness in society; and third -- most relevant to the believer -- as a guide for grateful obedience. "For this is the love of God, that we keep his commandments: and his commandments are not grievous" (1 John 5:3). Samuel Bolton wrote in The True Bounds of Christian Freedom that we are free from the law as a covenant of works, but not free from it as a rule of life. Dear friend, do not fall into legalism, thinking thy obedience earns God's favor, nor into license, thinking grace permits carelessness. Walk the narrow path of gospel obedience, empowered by the Spirit and motivated by love for thy Savior.`
    },
    {
      id: 'sin_nature',
      keywords: ['sin','sinful','sinner','transgression','iniquity','wickedness','evil','depravity','depraved','corrupt','flesh','carnal','fallen'],
      response: `Friend, understanding the depth of our sin is not meant to crush us but to magnify the grace that saves us. The Puritans understood, perhaps better than any generation, the terrible nature of indwelling sin. John Owen wrote his searching work, On the Mortification of Sin, reminding us: "Be killing sin or it will be killing you." Our hearts are, as Jeremiah declares, "deceitful above all things, and desperately wicked" (Jeremiah 17:9). Yet here is the gospel hope -- where sin abounded, grace did much more abound (Romans 5:20). Thomas Brooks taught that we must see sin as God sees it: an offense against His infinite holiness. But never stop at the diagnosis; run to the remedy! Christ's blood cleanses from all sin (1 John 1:7). Confess freely, repent sincerely, and rest in His mercy.`
    },
    {
      id: 'regeneration',
      keywords: ['born again','regeneration','new birth','new creation','converted','conversion','new heart','new life','quickened'],
      response: `Regeneration -- the new birth -- is the mighty work of the Holy Spirit by which a spiritually dead sinner is made alive in Christ. "Marvel not that I said unto thee, Ye must be born again" (John 3:7). This is no mere reformation of behavior but a radical transformation of nature. The Puritans called it effectual calling -- that irresistible work of grace by which God opens the blind eyes, unstops the deaf ears, and gives a heart of flesh in place of a heart of stone. Stephen Charnock wrote powerfully on this subject, showing that regeneration is entirely the work of God. Dear friend, if thou hast been born again, praise God! It was not thy decision but His grace. And if thou art yet seeking, cry out to Him -- for He delights to give new life to all who call upon Him in truth.`
    },
    {
      id: 'perseverance',
      keywords: ['perseverance','persevere','eternal security','once saved','falling away','assurance of salvation','kept','preservation','endure','endurance','backsliding','backslide'],
      response: `Beloved friend, the doctrine of the perseverance of the saints teaches that all whom God has truly saved, He will keep unto the end. "Being confident of this very thing, that he which hath begun a good work in you will perform it until the day of Jesus Christ" (Philippians 1:6). This does not mean believers never stumble -- indeed, Thomas Brooks wrote movingly about the seasons of spiritual darkness believers may experience. But it does mean that no true child of God will be finally and totally lost. As John Owen taught, our perseverance rests not on our grip on God but on His grip on us. Jesus Himself declared: "My sheep hear my voice, and I know them, and they follow me: And I give unto them eternal life; and they shall never perish" (John 10:27-28). Take heart in this unshakeable promise.`
    },
    {
      id: 'heaven_eternity',
      keywords: ['heaven','eternity','eternal','afterlife','glory','glorification','new earth','paradise','death','dying','die','resurrection body','second coming','return'],
      response: `Friend, the Puritans were a heavenly-minded people, and rightly so. Richard Baxter's Saints' Everlasting Rest is perhaps the most beautiful meditation on heaven ever penned. He urged believers to spend time daily contemplating the glory that awaits us. "Eye hath not seen, nor ear heard, neither have entered into the heart of man, the things which God hath prepared for them that love him" (1 Corinthians 2:9). In heaven, we shall see Christ face to face, be freed forever from sin's presence, and enjoy perfect communion with God and all His saints. Whatever hardships thou dost face in this present life, remember: they are but light afflictions, working for thee a far more exceeding and eternal weight of glory (2 Corinthians 4:17). Keep thine eyes fixed on the prize above.`
    },
    {
      id: 'church',
      keywords: ['church','churches','congregation','pastor','preaching','sermon','worship service','membership','ecclesiology','body of christ','gather','gathering'],
      response: `The Puritans had an exceedingly high view of the local church. They understood it to be Christ's appointed means of nurturing His people, and they urged every believer to be faithfully committed to a body of believers. "Not forsaking the assembling of ourselves together, as the manner of some is; but exhorting one another" (Hebrews 10:25). Richard Baxter labored tirelessly among his flock in Kidderminster, and the transformation of that town stands as a testament to faithful pastoral ministry. Dear friend, I urge thee: do not neglect the fellowship of the saints. Find a church where the Word is faithfully preached, the sacraments rightly administered, and the members lovingly accountable to one another. There is no such thing as a solitary Christian. We need one another, and Christ has designed it so.`
    },

    // ═══════════════════════════════════════
    // CHRISTIAN LIVING (15 responses)
    // ═══════════════════════════════════════
    {
      id: 'prayer_life',
      keywords: ['prayer','pray','praying','intercession','supplication','petition','devotion','communion','talk to god'],
      response: `Dear friend, prayer is the very breath of the Christian soul. It is the means by which we commune with our heavenly Father, pour out our hearts before Him, and receive grace for every need. "Be careful for nothing; but in every thing by prayer and supplication with thanksgiving let your requests be made known unto God" (Philippians 4:6). The Puritans were mighty in prayer. John Bunyan wrote: "Prayer is a sincere, sensible, affectionate pouring out of the soul to God, through Christ, in the strength and assistance of the Spirit." I would encourage thee to set aside a regular time each day -- even if only fifteen minutes at first -- to come before the Lord in prayer. Bring thy cares, thy confessions, thy thanksgivings, and thy petitions. He hears thee, and He delights in the prayers of His children.`
    },
    {
      id: 'reading_scripture',
      keywords: ['scripture','bible','word of god','reading','read','study','quiet time','meditation','meditate'],
      response: `Friend, the reading and studying of Holy Scripture is the primary means by which God speaks to thy soul. "Thy word is a lamp unto my feet, and a light unto my path" (Psalm 119:105). The Puritans were passionate students of the Bible. Thomas Watson advised: "Read the Scripture, not only as a history, but as a love letter sent to you from God." I would encourage thee to develop a daily habit of Scripture reading. Begin with a book of the Bible and read it through, slowly and prayerfully. Ask the Holy Spirit to open thine eyes to behold wonderful things from His law. Meditate upon what thou readest -- turn it over in thy mind throughout the day. And do not merely seek knowledge but transformation. As thou readest, ask: What does this teach me about God? About myself? How should I respond in obedience and worship?`
    },
    {
      id: 'dealing_with_doubt',
      keywords: ['doubt','doubts','doubting','uncertain','unsure','wavering','questioning','assurance','unbelief','anxious','anxiety','worried','worry','fear','afraid'],
      response: `Dear friend, know that seasons of doubt are common to many of God's saints. Even the great Puritans -- men of towering faith -- wrestled with doubts and fears. Thomas Goodwin wrote tenderly about the believer who walks in darkness yet trusts in the name of the Lord (Isaiah 50:10). Here is what I would counsel thee: first, do not mistake the absence of strong feelings for the absence of true faith. Faith is not a feeling but a resting upon Christ. Second, go back to the promises of God in Scripture -- they do not change with thy emotions. "The Lord is nigh unto them that are of a broken heart" (Psalm 34:18). Third, examine whether there is any unconfessed sin creating distance. And finally, keep using the means of grace: prayer, Scripture, and fellowship. The sun is still shining even when the clouds hide it. Thy Father has not left thee.`
    },
    {
      id: 'suffering_trials',
      keywords: ['suffering','suffer','pain','trial','trials','tribulation','affliction','hardship','difficulty','adversity','grief','loss','mourning','hurt','broken','sorrow','despair'],
      response: `Beloved friend, I grieve with thee in thy suffering, and I want thee to know that thy pain is not meaningless in God's economy. "Beloved, think it not strange concerning the fiery trial which is to try you, as though some strange thing happened unto you" (1 Peter 4:12). Thomas Watson wrote a beautiful little book called All Things for Good, in which he showed from Scripture that God uses even the darkest afflictions for the spiritual benefit of His children. The Puritans understood that suffering is one of God's most effective tools for sanctification -- it weans us from the world, drives us to prayer, teaches us dependence, and conforms us to the image of Christ. I do not say this to minimize thy pain, but to give thee hope. Weeping may endure for a night, but joy cometh in the morning (Psalm 30:5). Lean hard upon thy Savior; He is a man of sorrows, acquainted with grief.`
    },
    {
      id: 'fighting_temptation',
      keywords: ['temptation','tempted','lust','desire','enticement','struggle','weakness','addicted','addiction','fighting','battle','warfare'],
      response: `Friend, the fight against temptation is the daily business of every believer. John Owen's great work On the Mortification of Sin contains this searching counsel: "Be killing sin or it will be killing you. It is not enough to merely resist temptation; we must mortify -- put to death -- the very root of sinful desire." Here is practical Puritan wisdom for thy battle: First, know thy particular weaknesses and guard against them (Proverbs 4:23). Second, flee occasions of temptation -- do not test thy strength by lingering near the fire. Third, fill thy mind with Scripture, for the Word is the sword of the Spirit (Ephesians 6:17). Fourth, pray earnestly -- "Lead us not into temptation, but deliver us from evil." Fifth, confess to a trusted brother or sister, for "confess your faults one to another" (James 5:16). Thou art not alone in this battle, and by God's grace, thou shalt overcome.`
    },
    {
      id: 'joy_contentment',
      keywords: ['joy','joyful','happiness','content','contentment','satisfied','delight','cheerful','gladness','peace','blessed','grateful','gratitude','thankful'],
      response: `Dear friend, true joy and contentment are precious gifts from God that do not depend upon outward circumstances. Jeremiah Burroughs wrote a wonderful book called The Rare Jewel of Christian Contentment, in which he defined contentment as "that sweet, inward, quiet, gracious frame of spirit, which freely submits to and delights in God's wise and fatherly disposal in every condition." Paul learned this secret: "I have learned, in whatsoever state I am, therewith to be content" (Philippians 4:11). The Puritans found their deepest joy not in the things of this world but in communion with God Himself. "In thy presence is fulness of joy; at thy right hand there are pleasures for evermore" (Psalm 16:11). If thou wouldst cultivate joy, cultivate thy relationship with God. Draw near to Him, and joy will follow as surely as light follows the sunrise.`
    },
    {
      id: 'work_vocation',
      keywords: ['work','job','career','vocation','calling','occupation','labor','employment','profession','workplace','diligence','lazy','sloth','idle'],
      response: `Friend, the Puritans had a revolutionary view of work: they believed that every lawful vocation, no matter how humble, is a calling from God and a means of glorifying Him. William Perkins wrote: "The action of a shepherd in keeping sheep is as pure a work of God as is the action of a judge in giving sentence, or of a minister in preaching." "Whatsoever ye do, do it heartily, as to the Lord, and not unto men" (Colossians 3:23). Whether thou art a teacher, a tradesman, a homemaker, or anything else, thou art serving God in thy work. Do it with diligence, integrity, and excellence -- not to earn man's praise but as an offering to thy Creator. And remember too that thy work is a means of loving thy neighbor, for through thy labors thou servest others and contributest to the common good.`
    },
    {
      id: 'stewardship_money',
      keywords: ['money','wealth','stewardship','giving','tithe','generosity','finances','possessions','materialism','treasure','greed','covetous'],
      response: `Dear friend, the Puritans understood that all we possess belongs to God, and we are merely stewards of His bounty. Richard Baxter counseled: "Remember that you are a steward, and not a proprietor." The Scriptures are abundantly clear: "The earth is the LORD's, and the fulness thereof" (Psalm 24:1). Jesus warned soberly: "Lay not up for yourselves treasures upon earth, where moth and rust doth corrupt" (Matthew 6:19). I would encourage thee in these practical steps: First, give generously and cheerfully to the work of God's kingdom (2 Corinthians 9:7). Second, be content with what God has provided, resisting the endless desire for more. Third, use thy resources to bless others, especially those in need. Fourth, hold all earthly things with an open hand, for they are passing away. True riches are found in Christ alone, and these can never be taken from thee.`
    },
    {
      id: 'rest_sabbath',
      keywords: ['rest','sabbath','lords day','sunday','burnout','exhausted','tired','weary','refresh','cease'],
      response: `Friend, God has graciously built a rhythm of rest into the very fabric of creation. "Remember the sabbath day, to keep it holy" (Exodus 20:8). The Puritans, contrary to popular caricature, saw the Lord's Day not as a burden but as a delight -- a foretaste of the eternal rest that awaits believers. The Westminster Confession teaches that the Sabbath is to be spent in public and private worship, works of necessity and mercy, and holy rest from worldly employments. If thou art weary and burned out, hear the tender invitation of Christ: "Come unto me, all ye that labour and are heavy laden, and I will give you rest" (Matthew 11:28). Rest is not laziness; it is an act of faith, trusting that God will sustain the world without thy constant striving. Take time to be still and know that He is God (Psalm 46:10).`
    },
    {
      id: 'forgiveness',
      keywords: ['forgive','forgiveness','forgiven','pardon','bitterness','bitter','resentment','grudge','anger','angry','reconcile','reconciliation','offense'],
      response: `Dear friend, forgiveness is both a gift we receive from God and a grace we must extend to others. "Be ye kind one to another, tenderhearted, forgiving one another, even as God for Christ's sake hath forgiven you" (Ephesians 4:32). Thomas Watson wrote: "We are not fit to pray 'forgive us our debts' unless we can from our hearts say 'as we forgive our debtors.'" Forgiveness does not mean pretending the wrong did not happen, nor does it necessarily mean the relationship is immediately restored. But it does mean releasing the offender from the debt of thy bitterness and entrusting justice to God, who judges righteously. The Puritans knew that unforgiveness is a poison that destroys the vessel that holds it. For thy own soul's health and for the glory of God, choose the hard and holy path of forgiveness. Christ, who forgave thee an infinite debt, will give thee grace to forgive.`
    },
    {
      id: 'spiritual_disciplines',
      keywords: ['discipline','disciplines','spiritual practice','habits','routine','devotional life','means','fasting','fast','journaling','journal','meditation'],
      response: `Friend, the spiritual disciplines are those holy habits by which we place ourselves before God for the work of His grace. The Puritans called them "the means of grace" and valued them greatly. These include prayer, Bible reading, fasting, meditation, journaling, corporate worship, and fellowship. "Exercise thyself rather unto godliness" (1 Timothy 4:7). Richard Baxter organized his life with remarkable discipline, setting aside time each day for prayer, study, and self-examination. I would encourage thee to start simply: choose two or three disciplines and practice them consistently. Do not attempt everything at once, lest thou become discouraged. Remember, the disciplines are not the goal; God Himself is the goal. They are simply the paths along which we walk to meet Him. Be patient with thyself, be consistent, and trust that God will honor thy faithfulness over time.`
    },
    {
      id: 'evangelism_witness',
      keywords: ['evangelism','evangelize','witness','witnessing','share the gospel','testimony','unbeliever','unbelievers','lost','unsaved','mission','missions','missionary','neighbor','outreach'],
      response: `Dear friend, sharing the gospel with those who do not yet know Christ is both a privilege and a solemn duty. "But sanctify the Lord God in your hearts: and be ready always to give an answer to every man that asketh you a reason of the hope that is in you with meekness and fear" (1 Peter 3:15). Richard Baxter was so passionate about evangelism that he visited every family in his parish, catechizing and counseling each one. The Puritans believed that our witness includes both our words and our lives -- as Thomas Brooks said, a holy life is a powerful sermon. I encourage thee: pray for opportunities, love thy neighbors genuinely, and be ready to speak a word for Christ when the moment arises. Do not fear rejection; the results are in God's hands. Thou art simply called to be faithful, and the Spirit will do the converting.`
    },
    {
      id: 'humility',
      keywords: ['humility','humble','humbled','pride','proud','arrogance','arrogant','self','selfish','ego','boasting','boast','meekness','meek'],
      response: `Friend, humility is the soil in which every other virtue grows, and the Puritans understood this well. Jonathan Edwards listed humility as one of the chief marks of true religious affections. "God resisteth the proud, but giveth grace unto the humble" (James 4:6). Thomas Watson wrote: "Humility is the mushroom that grows under the tree of affliction; it makes a man low in his own eyes and high in God's esteem." True humility is not thinking less of thyself but thinking of thyself less -- fixing thine eyes on the greatness of God and the sufficiency of Christ. The more we behold His glory, the smaller our own pride becomes. I encourage thee to practice humility by serving others quietly, receiving correction graciously, and giving God the credit for every good thing in thy life. "He must increase, but I must decrease" (John 3:30).`
    },
    {
      id: 'repentance',
      keywords: ['repent','repentance','confess','confession','turn','turning','return','backslide','backsliding','prodigal','wayward','stray','strayed'],
      response: `Dear friend, repentance is not merely feeling sorry for sin but a wholehearted turning from sin unto God. Thomas Watson wrote an entire treatise called The Doctrine of Repentance, in which he described true repentance as having six ingredients: sight of sin, sorrow for sin, confession of sin, shame for sin, hatred of sin, and turning from sin. "If we confess our sins, he is faithful and just to forgive us our sins, and to cleanse us from all unrighteousness" (1 John 1:9). If thou hast wandered from the Lord, know this: He stands ready to receive thee back with open arms, just as the father received the prodigal son. Do not delay; come to Him now with a broken and contrite heart. He will not despise it (Psalm 51:17). Repentance is not a one-time event but a daily practice of the Christian life.`
    },
    {
      id: 'patience_waiting',
      keywords: ['patience','patient','wait','waiting','endure','endurance','long','slow','delayed','timing','when','how long','frustrated','frustration'],
      response: `Friend, waiting upon the Lord is one of the hardest and most sanctifying disciplines of the Christian life. "But they that wait upon the LORD shall renew their strength; they shall mount up with wings as eagles" (Isaiah 40:31). The Puritans knew much of waiting -- many of them endured years of persecution, imprisonment, and exile before seeing the fruit of their faithfulness. Thomas Brooks counseled: "God's timing is never wrong, and His delays are not denials." When God seems silent, He is not absent. He is often doing His deepest work in the seasons of waiting. Use this time to draw nearer to Him in prayer and Scripture. Examine thy heart, cultivate patience, and trust that He who has promised is faithful. As the farmer waits for the precious fruit of the earth (James 5:7), so must we wait for God's perfect timing in all things.`
    },

    // ═══════════════════════════════════════
    // FAMILY & RELATIONSHIPS (10 responses)
    // ═══════════════════════════════════════
    {
      id: 'family_worship',
      keywords: ['family worship','family devotion','family devotions','household','family altar','family prayer','worship at home','devotions together','pray together','family bible'],
      response: `Dear friend, family worship is one of the most precious practices a household can cultivate. The Puritans considered it essential -- not optional -- for the spiritual health of the home. "As for me and my house, we will serve the LORD" (Joshua 24:15). Richard Baxter urged every family to gather daily for the reading of Scripture, prayer, and the singing of psalms. It need not be long or complicated: even ten or fifteen minutes of reading a passage aloud, discussing it briefly, and praying together can transform a household. I encourage thee to begin tonight. Gather thy family, read a short passage from the Gospels, ask what it teaches about God, and close in prayer. Children especially benefit from seeing their parents take the lead in worship. Consistency matters more than length. Start small, be faithful, and watch God work in thy home.`
    },
    {
      id: 'marriage',
      keywords: ['marriage','married','marry','spouse','wedding','matrimony','partner','helpmate','one flesh','love your wife'],
      response: `Friend, marriage is a sacred covenant ordained by God from the very beginning. "Therefore shall a man leave his father and his mother, and shall cleave unto his wife: and they shall be one flesh" (Genesis 2:24). The Puritans had an extraordinarily high and tender view of marriage. William Gouge wrote extensively on the mutual duties of husbands and wives, emphasizing that marriage is a partnership of love, service, and spiritual growth. Richard Baxter and his wife Margaret had a deeply affectionate marriage that modeled gospel love. I counsel thee: cultivate thy marriage with intentionality. Pray together daily, speak words of encouragement, bear with one another's weaknesses, and remember that your marriage is meant to be a picture of Christ's love for His church (Ephesians 5:25-33). Invest in thy marriage as the most important earthly relationship God has given thee.`
    },
    {
      id: 'raising_children',
      keywords: ['children','child','kids','parenting','parent','raising','train','training','nurture','discipline','upbringing'],
      response: `Dear friend, raising children in the nurture and admonition of the Lord is one of the most important callings any parent can have. "Train up a child in the way he should go: and when he is old, he will not depart from it" (Proverbs 22:6). The Puritans took this responsibility with utmost seriousness. Cotton Mather wrote about the duty of parents to catechize their children, instruct them in Scripture, and model godliness before their eyes. I encourage thee: teach thy children the great truths of the faith from their earliest years. Pray for them daily by name. Let them see thy own love for God in how thou livest. Be firm in discipline but always tender in spirit, correcting in love and not in anger. And remember, thou art not ultimately responsible for thy children's salvation -- that is the work of God's Spirit -- but thou art responsible to be faithful in planting and watering the seeds of truth.`
    },
    {
      id: 'husband_leadership',
      keywords: ['husband','headship','head','lead','leader','spiritual leadership','man','men','manhood','masculinity','provider','protect'],
      response: `Friend, the calling of a husband to lead his family spiritually is a weighty and precious responsibility. "Husbands, love your wives, even as Christ also loved the church, and gave himself for it" (Ephesians 5:25). The Puritans understood that headship does not mean domination but sacrificial servant-leadership, modeled after Christ Himself. Richard Baxter counseled husbands to be the chief pray-ers of the home, to lead family worship, and to set the spiritual tone of the household through their own godly example. I encourage thee, brother: take the initiative in spiritual matters. Initiate prayer with thy wife. Lead thy family in worship. Be the first to repent, the first to forgive, and the first to serve. Thy family does not need a perfect leader; they need a humble one who loves God and points them to Christ by word and example.`
    },
    {
      id: 'wife_role',
      keywords: ['wife','wives','woman','women','womanhood','femininity','helpmeet','submit','submission','proverbs 31','virtuous'],
      response: `Dear friend, the Scriptures speak with great honor of the godly wife and her indispensable role in the home and the church. "Who can find a virtuous woman? for her price is far above rubies" (Proverbs 31:10). The Puritans, contrary to some caricatures, had a remarkably high view of women. They celebrated the wisdom, strength, and spiritual depth that godly wives bring to a household. Thomas Gataker called marriage "a sweet compound" and praised the companionship of a faithful wife. A wife's submission, rightly understood, is not inferiority but a willing partnership rooted in trust in God's good design. I encourage thee: whether thou art a wife or seeking to understand this role, know that the godly wife is a crown to her husband (Proverbs 12:4) and a powerful influence for good in her family. Thy prayers, thy wisdom, and thy faithfulness shape generations.`
    },
    {
      id: 'discipline_children',
      keywords: ['discipline','disciplining','correction','correct','punish','punishment','rod','spanking','boundary','boundaries','behavior','obedience','disobedient','rebellious'],
      response: `Friend, the discipline of children is an act of love, not wrath. "For whom the Lord loveth he chasteneth, and scourgeth every son whom he receiveth" (Hebrews 12:6). The Puritans practiced firm yet tender discipline, understanding that correction is essential for a child's spiritual and moral formation. Thomas Watson wrote that discipline without love breeds resentment, while love without discipline breeds lawlessness. Both must go together. I would counsel thee: always discipline calmly, never in the heat of anger. Explain to thy child why the correction is necessary and what Scripture says about the matter. Be consistent in thy expectations, and always restore the child with words of love and assurance after correction. The goal of discipline is not merely outward compliance but the shaping of the heart. Pray earnestly that God would use thy faithful discipline to lead thy children to love Him and walk in His ways.`
    },
    {
      id: 'friendship',
      keywords: ['friend','friends','friendship','fellowship','community','brother','sister','lonely','loneliness','alone','isolated','isolation','accountability','accountable'],
      response: `Dear friend, godly friendships are among the richest blessings God gives us in this life. "Iron sharpeneth iron; so a man sharpeneth the countenance of his friend" (Proverbs 27:17). The Puritans valued deep spiritual friendships, often writing long letters of encouragement, counsel, and mutual accountability. Jonathan Edwards and David Brainerd shared such a bond, and their friendship bore much fruit for the kingdom. If thou art feeling lonely or isolated, I encourage thee: take the initiative to build connections within thy local church. Offer to meet with a brother or sister for prayer and Scripture reading. Be vulnerable about thy struggles and willing to listen to theirs. Spiritual friendship requires investment and intentionality, but the rewards are immeasurable. Seek out those who will challenge thee to grow in Christ and hold thee accountable in thy walk.`
    },
    {
      id: 'singleness',
      keywords: ['single','singleness','unmarried','alone','dating','relationship','waiting for spouse','lonely','celibacy','celibate'],
      response: `Friend, whether singleness is thy permanent calling or a present season, know that Scripture speaks of it with great honor. The apostle Paul himself wrote: "I say therefore to the unmarried and widows, It is good for them if they abide even as I" (1 Corinthians 7:8). The Puritans, though they elevated marriage, also recognized the unique freedom and devotion that singleness affords. A single person can serve the Lord with undivided attention and pursue ministry opportunities that married life may not allow. I encourage thee: do not view thy singleness as a deficiency but as a stewardship. Use this season to deepen thy relationship with God, invest in thy church community, develop thy gifts, and serve others generously. If God intends marriage for thee, trust His timing. Meanwhile, find thy deepest satisfaction not in any earthly relationship but in communion with Christ, who is the truest Friend and the Bridegroom of thy soul.`
    },
    {
      id: 'conflict_resolution',
      keywords: ['conflict','argue','argument','fight','fighting','quarrel','disagreement','dispute','division','divided','strife','offense','offended'],
      response: `Dear friend, conflict among believers grieves the Spirit and hinders our witness to the world. Yet the Scriptures give us clear guidance for its resolution. "If thy brother shall trespass against thee, go and tell him his fault between thee and him alone: if he shall hear thee, thou hast gained thy brother" (Matthew 18:15). Richard Baxter wrote wisely about conflict in the church, urging believers to go directly to the offending party rather than gossiping or harboring resentment. I encourage thee: approach the situation with humility, recognizing thy own potential faults first (Matthew 7:5). Speak the truth, but always in love (Ephesians 4:15). Listen more than thou speakest. Seek reconciliation, not victory. And pray before, during, and after the conversation. "Blessed are the peacemakers: for they shall be called the children of God" (Matthew 5:9). God can bring healing to even the most fractured relationships.`
    },
    {
      id: 'grief_loss',
      keywords: ['grief','grieve','grieving','loss','lost someone','death','died','bereavement','mourning','miss','missing','passed away','funeral'],
      response: `Beloved friend, my heart goes out to thee in thy grief. Sorrow is not a sign of weak faith; even our Lord Jesus wept at the grave of Lazarus (John 11:35). The Puritans understood grief as a natural and necessary part of life in a fallen world. Richard Baxter, who buried many parishioners and his own beloved wife, wrote with tender pastoral care about walking through the valley of the shadow of death. "The LORD is nigh unto them that are of a broken heart; and saveth such as be of a contrite spirit" (Psalm 34:18). I encourage thee: do not rush thy grief, but do not grieve as those who have no hope (1 Thessalonians 4:13). For the believer, death is not the end but the doorway to glory. Thy loved one who died in Christ is more alive now than ever. And one day, at the resurrection, ye shall be reunited in the presence of your Savior, never to part again. Hold fast to this hope.`
    },

    // ═══════════════════════════════════════
    // THE PURITANS (10 responses)
    // ═══════════════════════════════════════
    {
      id: 'who_were_puritans',
      keywords: ['puritan','puritans','puritanism','who were','what is','history','movement','reformed','reformation','pilgrim'],
      response: `Friend, the Puritans were a remarkable movement of Christians in the 16th and 17th centuries who sought to purify the Church of England from within, calling for deeper reformation according to God's Word. They were not the dour, joyless people that popular culture often portrays. They were passionate lovers of God, devoted students of Scripture, and practical theologians who sought to apply the gospel to every area of life. "Whether therefore ye eat, or drink, or whatsoever ye do, do all to the glory of God" (1 Corinthians 10:31). Their legacy includes some of the richest theological writing in church history, the Westminster Confession of Faith, and an approach to Christian living that balances doctrinal depth with warm personal devotion. Their writings remain profoundly relevant today because they address the timeless realities of the human heart before a holy and gracious God.`
    },
    {
      id: 'john_owen',
      keywords: ['owen','john owen','mortification','indwelling sin','communion with god'],
      response: `John Owen (1616-1683) is often called the prince of Puritan theologians, and rightly so. His writings, though sometimes dense, contain some of the deepest wells of spiritual insight in the English language. His trilogy on sin -- Mortification of Sin, Indwelling Sin, and The Nature and Power of Temptation -- remains essential reading for any serious believer. His work on Communion with God explores the believer's distinct fellowship with each Person of the Trinity. Owen served as chaplain to Oliver Cromwell and Vice-Chancellor of Oxford University. "That the doctrine of the gospel is the truth of God is a matter of faith, but what the truth of the doctrine is, is a matter of knowledge." I encourage thee to begin with his shorter works -- The Mortification of Sin is a life-changing read. Let Owen teach thee the art of fighting sin and savoring Christ.`
    },
    {
      id: 'jonathan_edwards',
      keywords: ['edwards','jonathan edwards','sinners in the hands','religious affections','great awakening','revival'],
      response: `Jonathan Edwards (1703-1758) was perhaps the greatest theologian and philosopher America has ever produced. Serving as pastor in Northampton, Massachusetts, he was used mightily by God during the Great Awakening -- a sweeping revival that transformed the colonies. Though often remembered for his sermon "Sinners in the Hands of an Angry God," Edwards was primarily a preacher of the beauty and excellency of Christ. His Religious Affections remains the definitive work on distinguishing true spiritual experience from false. "God is the highest good of the reasonable creature, and the enjoyment of him is the only happiness with which our souls can be satisfied." I encourage thee to read Edwards not merely for information but for transformation. His passion for God's glory and his vision of divine beauty will set thy heart ablaze with love for Christ.`
    },
    {
      id: 'thomas_watson',
      keywords: ['watson','thomas watson','body of divinity','divine cordial','all things for good'],
      response: `Thomas Watson (c.1620-1686) is one of the most accessible and quotable of all the Puritan writers. His Body of Divinity -- an exposition of the Westminster Shorter Catechism -- is perhaps the finest introduction to Reformed theology ever written, combining doctrinal precision with warmth, clarity, and unforgettable illustrations. His shorter works, like All Things for Good and The Doctrine of Repentance, are gems of practical spirituality. Watson was ejected from his pulpit in 1662 for refusing to conform to the Act of Uniformity, yet he continued to minister faithfully. "A godly man is a praying man. As the whining of a pump shows there is water, so a Christian's groaning in prayer shows there is grace." I warmly recommend Watson as thy starting point for Puritan reading. His writing is lively, warm, and deeply practical.`
    },
    {
      id: 'richard_baxter',
      keywords: ['baxter','richard baxter','reformed pastor','saints everlasting rest','christian directory'],
      response: `Richard Baxter (1615-1691) was one of the most prolific and pastorally warm of all the Puritans. His ministry in Kidderminster transformed an entire town -- when he arrived, barely a family practiced godliness; when he departed, it was hard to find one that did not. His Reformed Pastor challenged ministers to care diligently for every soul in their charge. His Saints' Everlasting Rest urged believers to meditate daily on the glories of heaven. And his Christian Directory is an astonishing compendium of practical guidance for every area of life. "Spend your time in nothing which you know must be repented of." Baxter suffered much: poor health throughout his life, imprisonment for his faith, and the loss of his beloved wife Margaret. Yet through it all, his faith shone brightly. I recommend starting with The Saints' Everlasting Rest -- it will lift thy eyes to heaven.`
    },
    {
      id: 'charles_spurgeon',
      keywords: ['spurgeon','charles spurgeon','prince of preachers','metropolitan tabernacle','morning and evening','treasury of david'],
      response: `Charles Haddon Spurgeon (1834-1892), known as the Prince of Preachers, was not technically a Puritan but stood firmly in the Puritan tradition and drew deeply from their wells. Pastoring the Metropolitan Tabernacle in London, he preached to thousands every week for nearly forty years. His sermons, devotionals, and commentaries fill dozens of volumes. Morning and Evening, his daily devotional, has blessed millions. "I have learned to kiss the wave that throws me against the Rock of Ages." Spurgeon battled depression throughout his ministry yet never lost his grip on the gospel. His Treasury of David commentary on the Psalms is magnificent. I encourage thee to read one of his sermons each week -- they are freely available and will ignite thy love for Christ. Spurgeon makes the Puritan heritage accessible, warm, and wonderfully Christ-centered.`
    },
    {
      id: 'john_bunyan',
      keywords: ['bunyan','john bunyan','pilgrims progress','holy war','grace abounding','bedford','tinker'],
      response: `John Bunyan (1628-1688) was a tinker -- a mender of pots and pans -- who became one of the most beloved authors in the English language. His Pilgrim's Progress, written during twelve years of imprisonment for preaching without a license, is the most widely read allegory in history, second only to the Bible in copies printed. The journey of Christian from the City of Destruction to the Celestial City has guided countless believers through their own spiritual pilgrimages. His autobiography, Grace Abounding to the Chief of Sinners, is a raw and honest account of his own spiritual struggles and conversion. "In prayer it is better to have a heart without words than words without a heart." I heartily commend Pilgrim's Progress to thee, friend. Read it slowly, see thyself in its pages, and let Bunyan guide thee onward toward the Celestial City.`
    },
    {
      id: 'thomas_brooks',
      keywords: ['brooks','thomas brooks','precious remedies','against satan','smooth stones','unsearchable riches'],
      response: `Thomas Brooks (1608-1680) wrote some of the most practically helpful books in the Puritan library. His Precious Remedies Against Satan's Devices is a masterwork of spiritual warfare, cataloguing the various strategies Satan uses to deceive believers and providing biblical remedies for each one. The book begins with this sobering truth: Satan is a cunning adversary who studies our weaknesses. But Brooks shows that Scripture provides armor and weapons for every attack. His other works, like The Unsearchable Riches of Christ and Smooth Stones from Ancient Brooks, are equally rich. "God's wounds cure; sin's kisses kill." I encourage thee to read Precious Remedies -- it will sharpen thy discernment, strengthen thy defenses, and draw thee closer to Christ, who has already conquered the evil one. Brooks writes with warmth, wit, and pastoral tenderness that makes his counsel a joy to receive.`
    },
    {
      id: 'puritan_books',
      keywords: ['books','book','reading list','recommend','recommended','start','begin','library','read first','best puritan','essential'],
      response: `Friend, I rejoice that thou art interested in reading the Puritans! Here is a suggested path for beginning this rich journey. Start with Thomas Watson's All Things for Good or The Doctrine of Repentance -- Watson is the most accessible Puritan writer. Next, read John Bunyan's Pilgrim's Progress, a timeless allegory of the Christian life. Then venture into John Owen's Mortification of Sin -- it is short but profoundly searching. For daily devotions, Spurgeon's Morning and Evening is unmatched. When ready for deeper theology, try Watson's Body of Divinity or the Westminster Shorter Catechism with commentary. "The words of the wise are as goads, and as nails fastened by the masters of assemblies" (Ecclesiastes 12:11). Banner of Truth Trust publishes excellent editions of Puritan works. Begin small, read slowly, and meditate on what thou readest. The Puritans are best savored, not rushed.`
    },
    {
      id: 'puritan_legacy',
      keywords: ['legacy','impact','influence','why puritans','why read','relevance','relevant','today','modern','contemporary'],
      response: `Dear friend, the Puritans remain profoundly relevant because they addressed the timeless realities of the human soul before a holy God. Their insights into sin, grace, sanctification, and practical godliness are as fresh today as when they were first penned. J.I. Packer wrote: "The Puritans were the greatest Christians who ever lived, and the richest in their knowledge of God." Their legacy includes a deep commitment to the authority of Scripture, a passion for personal holiness, a love for rigorous yet warm theology, and a vision for applying the gospel to every sphere of life -- family, work, church, and society. "Thy word is very pure: therefore thy servant loveth it" (Psalm 119:140). In an age of shallow faith and distracted living, the Puritans call us back to depth, devotion, and the glory of God. May their example inspire thee to pursue Christ with thy whole heart.`
    },

    // ═══════════════════════════════════════
    // APP-RELATED (10 responses)
    // ═══════════════════════════════════════
    {
      id: 'what_to_study',
      keywords: ['study','today','daily','episode','listen','what should','recommend','suggestion','next','devotional'],
      response: `Friend, what a wonderful desire -- to seek wisdom from God's Word today! I would encourage thee to begin with whatever daily episode is next in thy study plan. Consistency is the key to growth. As Thomas Watson wrote: "The Scripture is the library of the Holy Ghost." If thou art looking for something specific, consider the current series available in the study section -- each episode is designed to nourish thy soul with Puritan wisdom and biblical truth. "Give us this day our daily bread" (Matthew 6:11) -- and the bread of the Word is just as necessary as physical bread. Open the study section, find the next episode thou hast not yet heard, and press play. Even fifteen minutes of attentive listening can transform thy day. May the Lord bless thy study!`
    },
    {
      id: 'how_to_use_app',
      keywords: ['app','how to use','navigate','features','help me use','application','puritan gold'],
      response: `Welcome, friend! Puritan Gold is designed to help thee grow in wisdom through daily study of the Puritans and Scripture. Here is how to make the most of it: The Study section contains daily episodes organized by week -- simply tap any episode to listen. Use the Calendar view to see thy progress through the month. The Family section offers devotionals for household worship. The Together section provides content for couples. And right here in this chat, thou canst ask me questions about theology, the Christian life, the Puritans, and more. "Wisdom is the principal thing; therefore get wisdom: and with all thy getting get understanding" (Proverbs 4:7). I recommend listening to one episode per day, using the family devotional in the evening, and chatting with me whenever questions arise. May this app be a blessing to thy walk with God!`
    },
    {
      id: 'bible_reading_plan',
      keywords: ['bible reading plan','reading plan','where to start','begin reading','new to bible','first time','scripture plan'],
      response: `Friend, I am glad thou desirest to be in God's Word! For a reading plan, I suggest beginning with the Gospel of John -- it reveals the glory of Christ with breathtaking beauty. Then read through the Psalms, which will teach thee to pray and worship. Next, work through Romans, which lays out the gospel systematically. After that, consider reading through the whole Bible using a plan that takes thee through the Old and New Testaments together. "All scripture is given by inspiration of God, and is profitable for doctrine, for reproof, for correction, for instruction in righteousness" (2 Timothy 3:16). The Puritans commended reading three chapters daily and five on the Lord's Day -- this will take thee through the entire Bible in one year. Whatever plan thou choosest, be consistent, read prayerfully, and ask the Spirit to illuminate the text.`
    },
    {
      id: 'explain_episode',
      keywords: ['explain','episode','understand','meaning','confused about','what does','what did','sermon','teaching','lesson'],
      response: `Friend, I appreciate thy desire to understand the teaching more deeply. The Puritans themselves were committed to clear and thorough exposition. As William Perkins wrote: "The art of prophesying is the art of making the Scripture speak plainly." While I may not be able to explain the specific details of a particular episode, I can help thee think through the theological themes. Tell me more about what topic or passage thou art wrestling with, and I shall do my best to shed light upon it from Scripture and the Puritan tradition. In the meantime, I encourage thee to listen to the episode again -- often a second hearing reveals what the first hearing missed. "Precept must be upon precept, line upon line; here a little, and there a little" (Isaiah 28:10). Take notes, meditate, and ask the Spirit for understanding.`
    },
    {
      id: 'morning_greeting',
      keywords: ['good morning','morning','start my day','wake','waking','rise','rising','dawn','daybreak','sunrise'],
      response: `Good morning, dear friend! What a mercy that the Lord has granted thee another day. "This is the day which the LORD hath made; we will rejoice and be glad in it" (Psalm 118:24). The Puritans placed great importance on beginning the day with God. Richard Baxter wrote of setting the heart upon God before anything else in the morning. I encourage thee to start this day with a brief prayer of thanksgiving, a few verses of Scripture, and a quiet moment of surrendering the day's plans to God's sovereign will. Spurgeon wrote in Morning and Evening: "Let us begin the day by seeking the Lord's face and finding renewed strength." Whatever lies ahead today -- whether labor or rest, joy or challenge -- thy heavenly Father goes before thee. Walk in His strength and for His glory.`
    },
    {
      id: 'evening_greeting',
      keywords: ['good evening','evening','good night','night','bedtime','sleep','end of day','rest','tonight'],
      response: `Good evening, dear friend. As this day draws to a close, I encourage thee to take a few moments for what the Puritans called "evening examination." Reflect upon the day: Where did thou see God's hand at work? Where did thou fall short and need His forgiveness? What mercies hast thou received that call for thanksgiving? "It is a good thing to give thanks unto the LORD, and to sing praises unto thy name, O most High: to shew forth thy lovingkindness in the morning, and thy faithfulness every night" (Psalm 92:1-2). Thomas Watson counseled believers to commit the night to God in prayer, casting all cares upon Him. Lay down thy burdens, confess thy sins, thank God for His faithfulness, and rest in the knowledge that He who keeps Israel neither slumbers nor sleeps (Psalm 121:4). Sleep well in His care.`
    },
    {
      id: 'general_greeting',
      keywords: ['hello','hi','hey','greetings','howdy','welcome','peace'],
      response: `Greetings, dear friend! It is a joy to speak with thee. "Grace be unto you, and peace, from God our Father, and from the Lord Jesus Christ" (1 Corinthians 1:3). I am here to offer counsel from the riches of Scripture and the wisdom of the Puritan tradition. Whether thou hast questions about theology, the Christian life, family worship, or simply needest a word of encouragement, I am at thy service. The Puritans believed that spiritual conversation was one of the means by which God sharpens and encourages His people. As Thomas Brooks wrote: "A Christian is to be a friend to all, but a familiar to few." So tell me, friend -- what is on thy heart today? I am ready to listen and to point thee to the unfailing Word of God.`
    },
    {
      id: 'encouragement_1',
      keywords: ['encourage','encouragement','hope','lift','comfort','strengthen','down','discouraged','struggling','hard'],
      response: `Dear friend, if thy heart is heavy today, hear this word of hope: "The eternal God is thy refuge, and underneath are the everlasting arms" (Deuteronomy 33:27). Thou art not forgotten. Thou art not forsaken. The same God who holds the stars in their courses holds thee in the palm of His hand. Thomas Brooks wrote: "God's hand is never shortened that it cannot save, nor His ear heavy that it cannot hear." Whatever thou art facing -- whether sorrow, weariness, doubt, or the weight of daily burdens -- know that thy Savior walks beside thee. He bore thy sins upon the cross, and He bears thy sorrows still. "Cast thy burden upon the LORD, and he shall sustain thee" (Psalm 55:22). Take courage, press on, and remember: this present darkness is not the end of thy story. The best is yet to come for those who love the Lord.`
    },
    {
      id: 'thankfulness',
      keywords: ['thankful','thanksgiving','grateful','gratitude','bless','blessed','blessing','blessings','praising','praise','worship','adore','adoration'],
      response: `Friend, what a beautiful spirit of thankfulness! The Puritans were remarkably grateful people, recognizing that every good gift comes from the Father of lights (James 1:17). "In every thing give thanks: for this is the will of God in Christ Jesus concerning you" (1 Thessalonians 5:18). Thomas Watson wrote: "The more we bless God for His mercies, the more God will bless us with His mercies." Cultivating gratitude is one of the most powerful practices of the Christian life -- it shifts our eyes from what we lack to what God has given, from our problems to His provision, from our weakness to His strength. I encourage thee to keep a daily habit of naming three specific blessings before thy head hits the pillow each night. In time, thy heart will overflow with praise, and thou shalt find that thankfulness is the antidote to a hundred sorrows.`
    },
    {
      id: 'purpose_meaning',
      keywords: ['purpose','meaning','why am i','what is my','calling','destiny','direction','plan for me','future','confused','lost','aimless'],
      response: `Dear friend, the question of purpose is one that every soul must wrestle with, and Scripture gives a clear and magnificent answer. The Westminster Shorter Catechism declares: "Man's chief end is to glorify God, and to enjoy Him forever." That is thy ultimate purpose, and every other calling flows from it. "For we are his workmanship, created in Christ Jesus unto good works, which God hath before ordained that we should walk in them" (Ephesians 2:10). The Puritans taught that purpose is discovered not by looking inward at our desires alone but by looking upward to God's Word and outward to the needs of others. Serve where God has placed thee -- in thy work, thy church, thy family, and thy community. Use the gifts He has given thee for His glory. William Perkins taught that every lawful vocation is a divine calling. Trust that God's plan for thy life is good, even when the path is unclear.`
    },

    // ═══════════════════════════════════════
    // FALLBACK / GENERAL (6 responses)
    // ═══════════════════════════════════════
    {
      id: 'fallback_1',
      keywords: [],
      response: `Dear friend, I appreciate thy question. While I may not have a specific answer ready for that particular matter, I can assure thee that God's Word speaks to every need of the human heart. "The LORD is my shepherd; I shall not want" (Psalm 23:1). The Puritans sought to bring every thought and concern under the authority of Scripture, trusting that God has not left us without guidance. I encourage thee to search the Scriptures on this matter, pray for wisdom (James 1:5 promises He gives it liberally), and seek counsel from godly believers in thy life. If thou hast a question about theology, the Christian life, family, or the Puritan authors, I would be glad to help. What else is on thy heart?`
    },
    {
      id: 'fallback_2',
      keywords: [],
      response: `Friend, that is a thoughtful question. The Puritans would remind us that in every situation, our first recourse should be to the Scriptures. "Thy word is a lamp unto my feet, and a light unto my path" (Psalm 119:105). Thomas Watson wrote: "The Word of God is the glass in which we see the face of God, and the face of our own souls." Whatever thou art pondering, I encourage thee to bring it before the Lord in prayer, search His Word for wisdom, and trust His providence. I am best equipped to help with questions about Reformed theology, the Puritan authors, Christian living, and family worship. Try asking me about a specific topic -- such as prayer, suffering, temptation, or one of the great Puritan writers -- and I shall do my best to offer helpful counsel.`
    },
    {
      id: 'fallback_3',
      keywords: [],
      response: `Dear friend, I thank thee for sharing that with me. While my knowledge is rooted in the Puritan tradition and Scripture, and I may not be able to address every matter, I am confident in this: God is sovereign over all things, and His wisdom far exceeds our own. "Trust in the LORD with all thine heart; and lean not unto thine own understanding. In all thy ways acknowledge him, and he shall direct thy paths" (Proverbs 3:5-6). Jonathan Edwards spoke of the importance of bringing every concern under the lordship of Christ. I am here to help thee think through matters of faith, doctrine, and Christian living. Feel free to ask about topics like sanctification, prayer, the Puritans, marriage, parenting, or any area where Scripture speaks. What shall we explore together?`
    },
    {
      id: 'fallback_4',
      keywords: [],
      response: `Friend, I appreciate thy reaching out. Though I may not be able to speak to that specific question, I can offer this timeless counsel from the Puritans: in all things, seek the glory of God and the good of thy soul. "Whether therefore ye eat, or drink, or whatsoever ye do, do all to the glory of God" (1 Corinthians 10:31). Richard Baxter counseled believers to weigh every decision by asking: Does this honor God? Does this serve my neighbor? Does this promote holiness in my life? These simple questions can guide thee through the most complex situations. I am most helpful with questions about theology, Scripture, the Christian life, and the writings of the Puritans. Try asking me something like "How do I fight temptation?" or "Tell me about John Owen" -- I would love to help!`
    },
    {
      id: 'fallback_5',
      keywords: [],
      response: `Dear friend, while that particular question may be beyond my area of counsel, I want to leave thee with an encouraging word. The Puritans lived with an unwavering confidence that God orders all things for the good of His people and the glory of His name. "And we know that all things work together for good to them that love God, to them who are the called according to his purpose" (Romans 8:28). Whatever thou art navigating, thou dost not navigate it alone. The God who parted the Red Sea, who raised Christ from the dead, who has sustained His church through every age -- this God is thy God. I am here to discuss theology, Christian living, family worship, the Puritan writers, and more. Try asking about a topic that is close to thy heart, and we shall search the Scriptures together.`
    },
    {
      id: 'fallback_6',
      keywords: [],
      response: `Friend, I may not have a ready answer for that exact question, but I do know Someone who does. "If any of you lack wisdom, let him ask of God, that giveth to all men liberally, and upbraideth not; and it shall be given him" (James 1:5). The Puritans were people of prayer precisely because they knew the limits of human wisdom and the boundless depths of God's. Charles Spurgeon once said: "When we cannot trace God's hand, we can trust God's heart." Bring thy question to the Lord in prayer, search the Scriptures for guidance, and lean upon the Holy Spirit for illumination. In the meantime, I am happy to discuss topics like Reformed theology, the great Puritan authors, Scripture reading, prayer, family life, and spiritual growth. What area would thou like to explore?`
    }
  ],

  // ── Keyword Matching Engine ──
  _normalizeText(text) {
    return text.toLowerCase()
      .replace(/['']/g, "'")
      .replace(/[""]/g, '"')
      .replace(/[^a-z0-9\s']/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
  },

  _extractKeywords(text) {
    const normalized = this._normalizeText(text);
    const words = normalized.split(' ');
    return words.filter(w => w.length > 1 && !this._stopWords.has(w));
  },

  _expandWithSynonyms(words) {
    const expanded = new Set(words);
    for (const word of words) {
      for (const [canonical, synonyms] of Object.entries(this._synonymMap)) {
        if (synonyms.includes(word)) {
          expanded.add(canonical);
          for (const syn of synonyms) {
            expanded.add(syn);
          }
        }
      }
    }
    return expanded;
  },

  _scoreResponse(response, expandedWords, rawText) {
    let score = 0;
    const normalizedRaw = this._normalizeText(rawText);

    for (const keyword of response.keywords) {
      // Check if the keyword is a multi-word phrase
      if (keyword.includes(' ')) {
        if (normalizedRaw.includes(keyword)) {
          score += 5; // Phrase matches are very strong
        }
      } else {
        if (expandedWords.has(keyword)) {
          score += 2;
        }
        // Bonus for direct word presence in raw text
        if (normalizedRaw.includes(keyword)) {
          score += 1;
        }
      }
    }
    return score;
  },

  _findBestResponse(text) {
    const words = this._extractKeywords(text);
    const expandedWords = this._expandWithSynonyms(words);

    // Score all non-fallback responses
    const scored = this._responses
      .filter(r => r.keywords.length > 0)
      .map(r => ({ id: r.id, response: r.response, score: this._scoreResponse(r, expandedWords, text) }))
      .filter(r => r.score > 0)
      .sort((a, b) => b.score - a.score);

    // Pick the best match that isn't a repeat of the last response
    if (scored.length > 0) {
      for (const candidate of scored) {
        if (candidate.id !== this._lastResponseId) {
          this._lastResponseId = candidate.id;
          this._trackRecent(candidate.id);
          return candidate.response;
        }
      }
      // If all top matches are the last response, just use the top one
      this._lastResponseId = scored[0].id;
      this._trackRecent(scored[0].id);
      return scored[0].response;
    }

    // Fallback: pick a general response, avoiding recent ones
    const fallbacks = this._responses.filter(r => r.keywords.length === 0);
    const available = fallbacks.filter(r => !this._recentResponseIds.includes(r.id));
    const pick = available.length > 0
      ? available[Math.floor(Math.random() * available.length)]
      : fallbacks[Math.floor(Math.random() * fallbacks.length)];

    this._lastResponseId = pick.id;
    this._trackRecent(pick.id);
    return pick.response;
  },

  _trackRecent(id) {
    this._recentResponseIds.push(id);
    if (this._recentResponseIds.length > 5) {
      this._recentResponseIds.shift();
    }
  },

  async sendChat(text) {
    if (!text.trim() || this._streaming) return;

    // Hide welcome, show messages
    const welcome = document.querySelector('.chat-welcome');
    if (welcome) welcome.style.display = 'none';

    // Add user message
    this.chatMessages.push({ role: 'user', content: text });
    this.renderChatMessages();

    // Clear input
    const input = document.getElementById('chatInput');
    if (input) input.value = '';

    // Check for API key → live AI mode
    const apiKey = this.getApiKey();
    if (apiKey) {
      await this._sendAIChat(text, apiKey);
    } else {
      // No API key — prompt user to add one
      const response = `**To get live, researched answers you need to add your API key.**\n\nTap the ⚙️ gear icon below → paste your Anthropic API key (starts with \`sk-ant-\`) → tap "Save Key".\n\nOnce added, I'll think deeply about every question and give you real, substantive answers backed by Scripture and research.\n\n**Get your key free at:** [console.anthropic.com](https://console.anthropic.com)`;
      this.chatMessages.push({ role: 'assistant', content: response });
      this.renderChatMessages();
    }
  },

  async _sendAIChat(text, apiKey) {
    // Add to AI conversation history
    this._aiConversation.push({ role: 'user', content: text });
    // Keep last 20 messages for context
    if (this._aiConversation.length > 20) {
      this._aiConversation = this._aiConversation.slice(-20);
    }

    // Add streaming placeholder with thinking state
    this.chatMessages.push({ role: 'assistant', content: '', streaming: true, thinking: true });
    this.renderChatMessages();
    this._streaming = true;
    this._setChatInputEnabled(false);

    try {
      const response = await fetch('https://api.anthropic.com/v1/messages', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'x-api-key': apiKey,
          'anthropic-version': '2023-06-01',
          'anthropic-dangerous-direct-browser-access': 'true'
        },
        body: JSON.stringify({
          model: 'claude-sonnet-4-20250514',
          max_tokens: 2048,
          system: this.isPatrickMode() ? PATRICK_SYSTEM_PROMPT : PURITAN_SYSTEM_PROMPT,
          messages: this._aiConversation,
          stream: true
        })
      });

      if (!response.ok) {
        const err = await response.text();
        throw new Error(`API error ${response.status}: ${err}`);
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let fullText = '';
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop(); // keep incomplete line

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = line.slice(6);
            if (data === '[DONE]') continue;
            try {
              const parsed = JSON.parse(data);
              if (parsed.type === 'content_block_delta' && parsed.delta?.text) {
                fullText += parsed.delta.text;
                // Clear thinking state on first token
                const lastMsg = this.chatMessages[this.chatMessages.length - 1];
                lastMsg.content = fullText;
                lastMsg.thinking = false;
                this._updateStreamingMessage(fullText);
              }
            } catch (e) {
              // ignore parse errors on non-JSON lines
            }
          }
        }
      }

      // Finalize
      this.chatMessages[this.chatMessages.length - 1].streaming = false;
      this._aiConversation.push({ role: 'assistant', content: fullText });
      this.renderChatMessages();

      // Speak if audio enabled
      if (this.chatAudioEnabled && fullText) {
        this.speakText(fullText);
      }

    } catch (err) {
      console.error('AI Chat error:', err);
      // Remove streaming placeholder
      this.chatMessages.pop();
      // Show clear error with troubleshooting
      let errorMsg = '**Connection Error**\n\n';
      const errStr = err.message || '';
      if (errStr.includes('401') || errStr.includes('authentication')) {
        errorMsg += 'Your API key appears to be invalid. Tap the ⚙️ gear icon to update it.\n\nMake sure it starts with `sk-ant-` and is copied completely.';
      } else if (errStr.includes('429')) {
        errorMsg += 'Rate limit reached. Please wait a moment and try again.';
      } else if (errStr.includes('insufficient') || errStr.includes('credit')) {
        errorMsg += 'Your API account may need credits. Check your balance at [console.anthropic.com](https://console.anthropic.com).';
      } else {
        errorMsg += `Could not reach the AI service. Check your internet connection and try again.\n\n_Error: ${errStr.substring(0, 100)}_`;
      }
      this.chatMessages.push({ role: 'assistant', content: errorMsg });
      this._aiConversation.pop(); // Remove the failed user message from AI history
      this.renderChatMessages();
    } finally {
      this._streaming = false;
      this._setChatInputEnabled(true);
    }
  },

  _setChatInputEnabled(enabled) {
    const input = document.getElementById('chatInput');
    const sendBtn = document.getElementById('chatSendBtn');
    if (input) {
      input.disabled = !enabled;
      input.placeholder = enabled ? 'Ask a question...' : 'Thinking...';
    }
    if (sendBtn) sendBtn.disabled = !enabled;
  },

  _updateStreamingMessage(text) {
    const container = document.getElementById('chatMessages');
    if (!container) return;
    const bubbles = container.querySelectorAll('.chat-assistant');
    const last = bubbles[bubbles.length - 1];
    if (last) {
      last.innerHTML = this._formatChatText(text) + '<span class="streaming-cursor">▊</span>';
      container.scrollTop = container.scrollHeight;
    }
  },

  _formatChatText(text) {
    // Basic markdown-ish formatting with safe ordering
    let html = this.escapeHtml(text);
    // Bold first (** before *)
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    // Italic with * (only single *, not **) — Safari-safe (no lookbehind)
    html = html.replace(/(?:^|[^*])\*([^*]+?)\*(?=[^*]|$)/g, function(match, p1) {
      const leading = match.charAt(0) === '*' ? '' : match.charAt(0);
      return leading + '<em>' + p1 + '</em>';
    });
    // Scripture references and quotes in quotation marks — make them golden
    html = html.replace(/&quot;(.*?)&quot;/g, '<q>$1</q>');
    // Line breaks
    html = html.replace(/\n/g, '<br>');
    return html;
  },

  sendChatFromInput() {
    const input = document.getElementById('chatInput');
    if (input && input.value.trim()) {
      this.sendChat(input.value);
    }
  },

  renderChatMessages() {
    const container = document.getElementById('chatMessages');
    if (!container) return;

    let html = '';
    for (let i = 0; i < this.chatMessages.length; i++) {
      const msg = this.chatMessages[i];
      const cls = msg.role === 'user' ? 'chat-user' : 'chat-assistant';

      if (msg.thinking) {
        // Show thinking indicator
        html += `<div class="chat-bubble chat-assistant"><div class="thinking-dots"><span></span><span></span><span></span></div></div>`;
        continue;
      }

      const content = msg.role === 'assistant' ? this._formatChatText(msg.content) : this.escapeHtml(msg.content);
      const cursor = msg.streaming ? '<span class="streaming-cursor">▊</span>' : '';
      const actionBar = msg.role === 'assistant' && !msg.streaming && msg.content ?
        `<div class="chat-actions">
          <button class="chat-action-btn" onclick="App.copyChatMessage(${i})" title="Copy">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
            <span>Copy</span>
          </button>
          <button class="chat-action-btn" onclick="App.shareChatMessage(App.chatMessages[${i}].content)" title="Share">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><polyline points="16 6 12 2 8 6"/><line x1="12" y1="2" x2="12" y2="15"/></svg>
            <span>Share</span>
          </button>
          <button class="chat-action-btn" onclick="App.speakChatMessage(${i})" title="Listen" id="speakBtn${i}">
            <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"/></svg>
            <span>Listen</span>
          </button>
        </div>` : '';
      html += `<div class="chat-bubble ${cls}">${content}${cursor}${actionBar}</div>`;
    }

    container.innerHTML = html;
    container.scrollTop = container.scrollHeight;
  },

  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  },

  toggleChatAudio() {
    this.chatAudioEnabled = !this.chatAudioEnabled;
    const btn = document.getElementById('chatAudioToggle');
    if (btn) {
      btn.classList.toggle('active', this.chatAudioEnabled);
      btn.innerHTML = this.chatAudioEnabled
        ? '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/></svg>'
        : '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M16.5 12c0-1.77-1.02-3.29-2.5-4.03v2.21l2.45 2.45c.03-.2.05-.41.05-.63zm2.5 0c0 .94-.2 1.82-.54 2.64l1.51 1.51C20.63 14.91 21 13.5 21 12c0-4.28-2.99-7.86-7-8.77v2.06c2.89.86 5 3.54 5 6.71zM4.27 3L3 4.27 7.73 9H3v6h4l5 5v-6.73l4.25 4.25c-.67.52-1.42.93-2.25 1.18v2.06c1.38-.31 2.63-.95 3.69-1.81L19.73 21 21 19.73l-9-9L4.27 3zM12 4L9.91 6.09 12 8.18V4z"/></svg>';
    }
    // Stop any current speech when toggling off
    if (!this.chatAudioEnabled && 'speechSynthesis' in window) {
      window.speechSynthesis.cancel();
    }
  },

  speakText(text) {
    if (!('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();
    // Truncate very long text to avoid Web Speech API silent failures
    const maxLen = 5000;
    let speakable = text.length > maxLen ? text.substring(0, maxLen) + '...' : text;
    // Strip markdown formatting for cleaner speech
    speakable = speakable.replace(/\*\*(.*?)\*\*/g, '$1').replace(/\*(.*?)\*/g, '$1');
    const utterance = new SpeechSynthesisUtterance(speakable);
    utterance.rate = 0.9;
    utterance.pitch = 0.95;
    // Try to use a male English voice
    const voices = window.speechSynthesis.getVoices();
    const maleVoice = voices.find(v => v.name.includes('Daniel') || v.name.includes('Male') || v.name.includes('en-GB'));
    if (maleVoice) utterance.voice = maleVoice;
    window.speechSynthesis.speak(utterance);
  },

  // ── Download & Share ──
  downloadAudio(id) {
    const ep = this.allEpisodes.find(e => e.id === id);
    if (!ep || !ep.file) {
      this.showToast('Audio not available yet');
      return;
    }
    const a = document.createElement('a');
    a.href = '../' + ep.file;
    a.download = ep.file.split('/').pop();
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    this.showToast('Downloading audio...');
  },

  _getScriptPath(ep) {
    const id = ep.id;
    if (ep.section === 'family') return `scripts/family_${id}.txt`;
    if (ep.section === 'school') return `scripts/school_${id}.txt`;
    if (ep.section === 'together') return `scripts/together_${id}.txt`;
    if (ep.section === 'personal') return `scripts/personal_${id}.txt`;
    return `scripts/ep_${id}.txt`;
  },

  downloadScript(id) {
    const ep = this.allEpisodes.find(e => e.id === id);
    if (!ep) return;
    const scriptFile = this._getScriptPath(ep);
    const a = document.createElement('a');
    a.href = '../' + scriptFile;
    a.download = scriptFile.split('/').pop();
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    this.showToast('Downloading script...');
  },

  async viewScript(id) {
    const el = document.getElementById('script-' + id);
    if (el) {
      // Toggle visibility if already loaded
      if (el.classList.contains('visible')) { el.classList.remove('visible'); return; }
      if (el.textContent) { el.classList.add('visible'); return; }
    }
    const ep = this.allEpisodes.find(e => e.id === id);
    if (!ep || !el) return;
    const scriptFile = this._getScriptPath(ep);
    try {
      el.textContent = 'Loading...';
      el.classList.add('visible');
      const resp = await fetch('../' + scriptFile);
      if (!resp.ok) throw new Error('Not found');
      const text = await resp.text();
      el.textContent = text;
    } catch {
      el.textContent = 'Script not available.';
    }
  },

  async shareEpisode(id) {
    const ep = this.allEpisodes.find(e => e.id === id);
    if (!ep) return;

    const appUrl = 'https://patrickparagas1.github.io/puritan-gold/app/';
    let shareText = `${ep.title}`;
    if (ep.subtitle) shareText += ` — ${ep.subtitle}`;
    shareText += `\n\n`;
    if (ep.description) shareText += ep.description.substring(0, 200) + '\n\n';
    shareText += `Listen on Puritan Gold: ${appUrl}`;

    if (navigator.share) {
      try {
        await navigator.share({ title: ep.title, text: shareText, url: appUrl });
      } catch (e) {
        // User cancelled or error
      }
    } else {
      // Desktop fallback: copy to clipboard
      try {
        await navigator.clipboard.writeText(shareText);
        this.showToast('Copied to clipboard!');
      } catch (e) {
        this.showToast('Could not share');
      }
    }
  },

  async copyChatMessage(index) {
    const msg = this.chatMessages[index];
    if (!msg) return;
    try {
      await navigator.clipboard.writeText(msg.content);
      this.showToast('Copied to clipboard');
    } catch (e) {
      this.showToast('Could not copy');
    }
  },

  async shareChatMessage(text) {
    const shareText = `From Puritan Gold:\n\n${text}`;
    if (navigator.share) {
      try {
        await navigator.share({ title: 'Puritan Gold', text: shareText });
      } catch (e) {}
    } else {
      try {
        await navigator.clipboard.writeText(shareText);
        this.showToast('Copied to clipboard!');
      } catch (e) {
        this.showToast('Could not copy');
      }
    }
  },

  speakChatMessage(index) {
    const msg = this.chatMessages[index];
    if (!msg) return;
    // If already speaking this message, stop
    if (this._speakingIndex === index && 'speechSynthesis' in window && window.speechSynthesis.speaking) {
      window.speechSynthesis.cancel();
      this._speakingIndex = null;
      const btn = document.getElementById('speakBtn' + index);
      if (btn) btn.classList.remove('speaking');
      return;
    }
    // Speak the message
    this._speakingIndex = index;
    const btn = document.getElementById('speakBtn' + index);
    if (btn) btn.classList.add('speaking');
    this.speakText(msg.content);
    // Reset state when done
    if ('speechSynthesis' in window) {
      const checkDone = setInterval(() => {
        if (!window.speechSynthesis.speaking) {
          clearInterval(checkDone);
          this._speakingIndex = null;
          if (btn) btn.classList.remove('speaking');
        }
      }, 500);
    }
  },

  showToast(message) {
    let toast = document.getElementById('toast');
    if (!toast) {
      toast = document.createElement('div');
      toast.id = 'toast';
      toast.className = 'toast';
      document.body.appendChild(toast);
    }
    toast.textContent = message;
    toast.classList.add('visible');
    clearTimeout(this._toastTimer);
    this._toastTimer = setTimeout(() => toast.classList.remove('visible'), 2500);
  },

  // ── AI Chat Settings ──
  getApiKey() {
    return localStorage.getItem('puritan_api_key') || '';
  },

  saveApiKey(key) {
    if (key && key.trim()) {
      localStorage.setItem('puritan_api_key', key.trim());
      this.showToast('API key saved');
    }
    this.closeSettings();
  },

  clearApiKey() {
    localStorage.removeItem('puritan_api_key');
    this._aiConversation = [];
    this.showToast('API key removed');
    this.closeSettings();
  },

  openSettings() {
    const modal = document.getElementById('settingsModal');
    if (modal) {
      modal.classList.add('open');
      const input = document.getElementById('apiKeyInput');
      if (input) input.value = this.getApiKey();
      const pinInput = document.getElementById('pinInput');
      if (pinInput) pinInput.value = this.getPin();
    }
  },

  closeSettings() {
    const modal = document.getElementById('settingsModal');
    if (modal) modal.classList.remove('open');
  },

  // ── Pin (Patrick Mode) ──
  getPin() { return localStorage.getItem('puritan_pin') || ''; },

  savePin(pin) {
    if (pin && pin.trim().length === 4) {
      localStorage.setItem('puritan_pin', pin.trim());
      this.showToast('Pin saved — pastoral mode active');
      this._updatePatrickIndicator();
    } else {
      this.showToast('Pin must be 4 digits');
    }
  },

  clearPin() {
    localStorage.removeItem('puritan_pin');
    this._aiConversation = [];
    this.showToast('Pin removed');
    this._updatePatrickIndicator();
  },

  isPatrickMode() {
    return this.getPin() === '1689'; // 1689 London Baptist Confession
  },

  _updatePatrickIndicator() {
    const askView = document.getElementById('askView');
    if (askView) {
      askView.classList.toggle('patrick-mode', this.isPatrickMode());
    }
    // Show/hide ask tabs (only in Patrick mode)
    const tabs = document.getElementById('askTabs');
    if (tabs) tabs.style.display = this.isPatrickMode() ? 'flex' : 'none';
  },

  switchAskTab(tab) {
    document.querySelectorAll('.ask-tab').forEach(t => t.classList.remove('active'));
    document.querySelector(`.ask-tab[data-ask-tab="${tab}"]`).classList.add('active');
    const chatArea = document.getElementById('chatMessages');
    const studioArea = document.getElementById('podcastStudio');
    if (tab === 'chat') {
      chatArea.style.display = '';
      studioArea.style.display = 'none';
    } else {
      chatArea.style.display = 'none';
      studioArea.style.display = 'flex';
    }
  },

  clearChatHistory() {
    this.chatMessages = [];
    this._aiConversation = [];
    const container = document.getElementById('chatMessages');
    if (container) {
      container.innerHTML = `
        <div class="chat-welcome" id="chatWelcome">
          <div class="chat-welcome-icon">P</div>
          <h3>Ask Anything</h3>
          <p>Theology, science, life, nature, history — answered with wisdom from Scripture and the Puritans.</p>
          <div class="chat-suggestions" id="chatSuggestions">
            <button class="chat-suggestion" onclick="App.askSuggestion(this)"><span class="suggestion-text">What is justification by faith?</span></button>
            <button class="chat-suggestion" onclick="App.askSuggestion(this)"><span class="suggestion-text">Why did God create dolphins?</span></button>
            <button class="chat-suggestion" onclick="App.askSuggestion(this)"><span class="suggestion-text">Explain covenant theology simply</span></button>
            <button class="chat-suggestion" onclick="App.askSuggestion(this)"><span class="suggestion-text">Why did God create volleyball?</span></button>
          </div>
        </div>`;
    }
    this.showToast('Chat cleared');
  },

  // ── Media Session (Lock Screen Controls) ──
  updateMediaSession() {
    if (!('mediaSession' in navigator) || !this.currentEp) return;

    navigator.mediaSession.metadata = new MediaMetadata({
      title: this.currentEp.title,
      artist: 'Puritan Gold',
      album: this.currentEp.series || 'Daily Devotional',
      artwork: [
        { src: 'data:image/svg+xml,' + encodeURIComponent("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 512 512'><rect width='512' height='512' rx='100' fill='%231a3a5c'/><text x='256' y='330' font-size='280' text-anchor='middle' fill='%23e8b84a' font-weight='bold'>P</text></svg>"), sizes: '512x512', type: 'image/svg+xml' }
      ]
    });

    navigator.mediaSession.setActionHandler('play', () => this.togglePlay());
    navigator.mediaSession.setActionHandler('pause', () => this.togglePlay());
    navigator.mediaSession.setActionHandler('seekbackward', () => this.skipBack());
    navigator.mediaSession.setActionHandler('seekforward', () => this.skipForward());
    navigator.mediaSession.setActionHandler('previoustrack', () => this.skipBack());
    navigator.mediaSession.setActionHandler('nexttrack', () => this.skipForward());

    try {
      navigator.mediaSession.setActionHandler('seekto', (details) => {
        this.audio.currentTime = details.seekTime;
      });
    } catch (e) {}
  },

  updateMediaPosition() {
    if (!('mediaSession' in navigator) || !this.audio.duration) return;
    try {
      navigator.mediaSession.setPositionState({
        duration: this.audio.duration,
        playbackRate: this.audio.playbackRate,
        position: this.audio.currentTime,
      });
    } catch (e) {}
  },

  // ── Helpers ──
  getWeekNumber(id) {
    // Normalize to day-within-month for week calculation
    let day = id;
    if (id >= 32 && id <= 61) day = id - 31; // April study
    else if (id > 61) day = id; // fallback
    return Math.ceil(day / 7);
  },

  getDayName(dateStr) {
    if (!dateStr) return '';
    const d = new Date(dateStr + 'T12:00:00');
    return ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'][d.getDay()] || '';
  },

  formatDate(dateStr) {
    if (!dateStr) return '';
    const d = new Date(dateStr + 'T12:00:00');
    return `${this._monthAbbr[d.getMonth()]} ${d.getDate()}`;
  },

  getSeriesClass(series) {
    if (!series) return '';
    const s = series.toLowerCase();
    if (s.includes('spurgeon')) return 'series-spurgeon';
    if (s.includes('pink')) return 'series-pink';
    if (s.includes('puritan') || s.includes('owen') || s.includes('watson')) return 'series-puritan';
    if (s.includes('proverb') || s.includes('scripture')) return 'series-proverbs';
    if (s.includes('devotion') || s.includes('practical')) return 'series-devotional';
    return '';
  },

  formatTime(secs) {
    if (!secs || isNaN(secs)) return '0:00';
    const m = Math.floor(secs / 60);
    const s = Math.floor(secs % 60);
    return m + ':' + (s < 10 ? '0' : '') + s;
  },

  parseDuration(str) {
    if (!str) return 0;
    const parts = str.split(':').map(Number);
    return (parts[0] || 0) * 60 + (parts[1] || 0);
  },

  getProgress(ep) {
    if (this.isListened(ep.id)) return 100;
    const pos = this.getPosition(ep.id);
    if (pos <= 0) return 0;
    const dur = this.parseDuration(ep.duration);
    if (dur <= 0) return 0;
    return Math.min(99, Math.round((pos / dur) * 100));
  },

  // ── Persistence ──
  isListened(id) { return localStorage.getItem('listened_' + id) === '1'; },
  markListened(id) {
    localStorage.setItem('listened_' + id, '1');
    localStorage.removeItem('pos_' + id);
  },
  savePosition(id, time) { localStorage.setItem('pos_' + id, time.toString()); },
  getPosition(id) { return parseFloat(localStorage.getItem('pos_' + id) || '0'); },

  saveState() {
    if (this.currentEp) localStorage.setItem('lastEp', this.currentEp.id.toString());
  },

  restoreState() {
    // Restore speed
    const savedSpeed = parseInt(localStorage.getItem('speed') || '1');
    if (savedSpeed >= 0 && savedSpeed < this.speeds.length) {
      this.speedIdx = savedSpeed;
      document.getElementById('npSpeedTop').textContent = this.speeds[this.speedIdx] + 'x';
      const mpLabel = document.getElementById('mpSpeedLabel');
      if (mpLabel) mpLabel.textContent = this.speeds[this.speedIdx] + 'x';
    }

    // Restore autoplay
    const savedAuto = localStorage.getItem('autoplay');
    if (savedAuto !== null) {
      this.autoplay = savedAuto === '1';
    }

    // Restore last episode
    const lastId = parseInt(localStorage.getItem('lastEp') || '0');
    if (lastId) {
      const ep = this.allEpisodes.find(e => e.id === lastId) || this.episodes.find(e => e.id === lastId);
      if (ep) {
        this.currentEp = ep;
        document.getElementById('miniPlayer').classList.add('visible');
        document.getElementById('mpTitle').textContent = ep.title;
        document.getElementById('mpSub').textContent = 'Tap to resume';
        this.updatePlayBtn(false);
        this.renderEpisodes(); // Re-render to show playing state
      }
    }
  },

  setupServiceWorker() {
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('sw.js').catch(() => {});
    }
  }
};

// Empty state style injection
const style = document.createElement('style');
style.textContent = `.empty-state{display:flex;align-items:center;justify-content:center;height:200px;color:var(--text3);font-weight:600;font-size:15px;text-align:center;padding:20px;}`;
document.head.appendChild(style);

document.addEventListener('DOMContentLoaded', () => App.init());
