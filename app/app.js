const App = {
  // ── State ──
  episodes: [],
  audio: new Audio(),
  currentEp: null,
  view: 'episodes',
  filter: 'all',
  speeds: [0.75, 1, 1.25, 1.5, 1.75, 2],
  speedIdx: 1,
  autoplay: true,
  sleepTimer: null,
  sleepEnd: null,
  npOpen: false,

  // ── Initialize ──
  async init() {
    await this.loadEpisodes();
    this.setupTabs();
    this.setupFilters();
    this.renderEpisodes();
    this.renderCalendar();
    this.setupPlayer();
    this.setupNowPlaying();
    this.setupServiceWorker();
    this.restoreState();
    this.updateStreak();
    this.scrollToNext();
  },

  async loadEpisodes() {
    try {
      const res = await fetch('../episodes.json?' + Date.now());
      this.episodes = await res.json();
    } catch (e) {
      this.episodes = [];
    }
  },

  // ── Tabs ──
  setupTabs() {
    document.querySelectorAll('.tab').forEach(tab => {
      tab.addEventListener('click', () => {
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        this.view = tab.dataset.view;

        document.getElementById('episodesView').classList.toggle('active', this.view === 'episodes');
        document.getElementById('calendarView').classList.toggle('active', this.view === 'calendar');

        // Show/hide filters
        document.getElementById('filters').style.display = this.view === 'episodes' ? '' : 'none';

        // Render calendar when switching to it
        if (this.view === 'calendar') this.renderCalendar();
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
                  this.filter === 'unplayed' ? 'All caught up! 🎉' :
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

      html += `
        <div class="episode-card ${listened ? 'listened' : ''} ${isPlaying ? 'playing' : ''}" data-id="${ep.id}">
          <div class="ep-left" onclick="App.playEpisode(${ep.id})">
            <div class="ep-num ${isPlaying ? 'active' : ''}" id="ep-num-${ep.id}">${ep.id}</div>
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
          </div>
          <div class="ep-actions">
            <button class="info-btn" onclick="event.stopPropagation(); App.toggleSummary(${ep.id})">i</button>
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

  // ── Render Calendar ──
  renderCalendar() {
    const grid = document.getElementById('calGrid');
    if (!grid) return;

    // March 2026: starts on Sunday (day 0), 31 days
    const year = 2026, month = 2; // JS months are 0-indexed
    const firstDay = new Date(year, month, 1).getDay(); // 0 = Sunday
    const daysInMonth = new Date(year, month + 1, 0).getDate(); // 31
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
      return d.getDate() === day && d.getMonth() === 2 && d.getFullYear() === 2026;
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
      statusText = '✓ Completed';
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
          <div class="cal-ep-date">${dayName}, March ${day}</div>
          <span class="cal-ep-status ${statusClass}">${statusText}</span>
        </div>
        <div class="cal-ep-title">${ep.title}</div>
        <div class="cal-ep-subtitle">${ep.subtitle || ''}</div>
        <div class="cal-ep-meta">
          <span class="ep-badge ${seriesClass}">${ep.series || 'General'}</span>
          <span class="cal-ep-dur">⏱ ${ep.duration}</span>
        </div>
        ${ep.description ? `<div class="cal-ep-desc">${ep.description}</div>` : ''}
        <button class="cal-ep-play" onclick="event.stopPropagation(); App.playEpisode(${ep.id})">
          ${isPlaying && !this.audio.paused ? '⏸ Now Playing' : listened ? '🔄 Replay' : progress > 0 ? '▶ Resume' : '▶ Play Episode'}
        </button>
        ${progress > 0 || listened ? `<div class="ep-progress ${listened ? 'done' : ''}"><div class="ep-progress-fill" style="width:${listened ? 100 : progress}%"></div></div>` : ''}
      </div>`;
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
        this.renderEpisodes();
        this.renderCalendar();
      }

      // Sleep timer: end of episode
      if (this.sleepEnd === 'episode') {
        this.sleepEnd = null;
        this.updatePlayBtn(false);
        return;
      }

      // Autoplay next
      if (this.autoplay && this.currentEp) {
        const nextId = this.currentEp.id + 1;
        const next = this.episodes.find(e => e.id === nextId);
        if (next) this.playEpisode(nextId);
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
    const ep = this.episodes.find(e => e.id === id);
    if (!ep) return;

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

    localStorage.setItem('speed', this.speedIdx.toString());
  },

  skipBack() {
    this.audio.currentTime = Math.max(0, this.audio.currentTime - 15);
  },

  skipForward() {
    this.audio.currentTime = Math.min(this.audio.duration || 0, this.audio.currentTime + 30);
  },

  // ── Now Playing ──
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
  getWeekNumber(id) { return Math.ceil(id / 7); },

  getDayName(dateStr) {
    if (!dateStr) return '';
    const d = new Date(dateStr + 'T12:00:00');
    return ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'][d.getDay()] || '';
  },

  formatDate(dateStr) {
    if (!dateStr) return '';
    const d = new Date(dateStr + 'T12:00:00');
    return `Mar ${d.getDate()}`;
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
    }

    // Restore autoplay
    const savedAuto = localStorage.getItem('autoplay');
    if (savedAuto !== null) {
      this.autoplay = savedAuto === '1';
    }

    // Restore last episode
    const lastId = parseInt(localStorage.getItem('lastEp') || '0');
    if (lastId) {
      const ep = this.episodes.find(e => e.id === lastId);
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
