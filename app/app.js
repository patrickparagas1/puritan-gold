const App = {
  episodes: [],
  audio: new Audio(),
  currentEp: null,
  currentView: 'episodes',
  speeds: [0.75, 1, 1.25, 1.5, 1.75, 2],
  speedIndex: 1,

  async init() {
    await this.loadEpisodes();
    this.renderTabs();
    this.renderEpisodes();
    this.renderSchedule();
    this.setupPlayer();
    this.setupServiceWorker();
    this.restoreState();
  },

  async loadEpisodes() {
    try {
      const res = await fetch('../episodes.json?' + Date.now());
      this.episodes = await res.json();
    } catch (e) {
      this.episodes = [];
    }
  },

  renderTabs() {
    document.querySelectorAll('.tab').forEach(tab => {
      tab.addEventListener('click', () => {
        document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        const view = tab.dataset.view;
        this.currentView = view;
        document.querySelector('.episode-list-view').classList.toggle('active', view === 'episodes');
        document.querySelector('.schedule-view').classList.toggle('active', view === 'schedule');
      });
    });
  },

  renderEpisodes() {
    const container = document.querySelector('.episode-list');
    if (!this.episodes.length) {
      container.innerHTML = '<div class="loading">No episodes yet</div>';
      return;
    }

    let currentWeek = null;
    let html = '';

    this.episodes.forEach(ep => {
      const week = this.getWeekNumber(ep.id);
      if (week !== currentWeek) {
        currentWeek = week;
        html += `<div class="week-header">Week ${week}</div>`;
      }

      const listened = this.isListened(ep.id);
      const seriesClass = this.getSeriesClass(ep.series);
      const dateStr = this.formatDate(ep.date);
      const dayName = this.getDayName(ep.date);
      const summary = ep.description || ep.subtitle || '';

      html += `
        <div class="episode-card ${listened ? 'listened' : ''}" data-id="${ep.id}">
          <div class="ep-left" onclick="App.playEpisode(${ep.id})">
            <div class="ep-number" id="ep-num-${ep.id}">${ep.id}</div>
            <div class="ep-date">${dayName}</div>
          </div>
          <div class="ep-info" onclick="App.playEpisode(${ep.id})">
            <div class="ep-title">${ep.title}</div>
            <div class="ep-subtitle">${ep.subtitle || ''}</div>
            <div class="ep-meta">
              <span class="ep-series-badge ${seriesClass}">${ep.series || 'General'}</span>
              <span class="ep-duration">${ep.duration}</span>
            </div>
            <div class="ep-summary" id="summary-${ep.id}">${summary}</div>
          </div>
          <div class="ep-actions">
            <button class="info-btn" onclick="event.stopPropagation(); App.toggleSummary(${ep.id})">i</button>
          </div>
        </div>`;
    });

    container.innerHTML = html;
  },

  toggleSummary(id) {
    const el = document.getElementById('summary-' + id);
    if (el) el.classList.toggle('visible');
  },

  renderSchedule() {
    const container = document.querySelector('.schedule-view');
    const weeks = {};

    this.episodes.forEach(ep => {
      const w = this.getWeekNumber(ep.id);
      if (!weeks[w]) weeks[w] = [];
      weeks[w].push(ep);
    });

    let html = '';
    const weekThemes = {
      1: 'Wisdom Begins — Proverbs 1-4 & Spurgeon',
      2: 'Walking in Righteousness — Proverbs 5-8 & A.W. Pink',
      3: 'The Fear of the Lord — Proverbs 9-12 & Puritan Doctrine',
      4: 'Living Wisely — Proverbs 13-16 & Practical Theology',
      5: 'Pressing On — Proverbs 17-18 & Review'
    };

    Object.keys(weeks).sort((a, b) => a - b).forEach(w => {
      html += `<div class="schedule-week">
        <div class="schedule-week-title">Week ${w}: ${weekThemes[w] || ''}</div>`;
      weeks[w].forEach(ep => {
        const listened = this.isListened(ep.id);
        const d = new Date(ep.date + 'T12:00:00');
        const dayNum = d.getDate();
        const dayName = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'][d.getDay()];

        html += `<div class="schedule-day ${listened ? 'listened' : ''}" onclick="App.playEpisode(${ep.id})">
          <div class="schedule-day-date">
            <div class="schedule-day-num">${dayNum}</div>
            <div class="schedule-day-name">${dayName}</div>
          </div>
          <div class="schedule-day-title">${listened ? '&#10003; ' : ''}${ep.title}</div>
          <div class="schedule-day-series">${ep.series || ''}</div>
        </div>`;
      });
      html += '</div>';
    });

    container.innerHTML = html;
  },

  setupPlayer() {
    const progressBar = document.querySelector('.player-progress-bar');
    const progressFill = document.querySelector('.player-progress-fill');

    this.audio.addEventListener('timeupdate', () => {
      if (!this.audio.duration) return;
      const pct = (this.audio.currentTime / this.audio.duration) * 100;
      progressFill.style.width = pct + '%';
      document.querySelector('.player-time').textContent =
        this.formatTime(this.audio.currentTime) + ' / ' + this.formatTime(this.audio.duration);
      if (this.currentEp && Math.floor(this.audio.currentTime) % 5 === 0) {
        this.savePosition(this.currentEp.id, this.audio.currentTime);
      }
    });

    this.audio.addEventListener('ended', () => {
      this.markListened(this.currentEp.id);
      this.renderEpisodes();
      this.renderSchedule();
      const nextId = this.currentEp.id + 1;
      const next = this.episodes.find(e => e.id === nextId);
      if (next) this.playEpisode(nextId);
    });

    progressBar.addEventListener('click', (e) => {
      if (!this.audio.duration) return;
      const rect = progressBar.getBoundingClientRect();
      const pct = (e.clientX - rect.left) / rect.width;
      this.audio.currentTime = pct * this.audio.duration;
    });
  },

  playEpisode(id) {
    const ep = this.episodes.find(e => e.id === id);
    if (!ep) return;

    this.currentEp = ep;
    this.audio.src = '../' + ep.file;
    this.audio.playbackRate = this.speeds[this.speedIndex];

    const saved = this.getPosition(id);
    if (saved > 0) this.audio.currentTime = saved;

    this.audio.play();

    document.querySelector('.player-bar').classList.add('visible');
    document.querySelector('.player-title').textContent = ep.title;
    document.querySelector('.player-time').textContent = '0:00 / ' + ep.duration;
    this.updatePlayButton(true);

    document.querySelectorAll('.episode-card').forEach(c => c.classList.remove('playing'));
    document.querySelectorAll('.ep-number').forEach(n => n.classList.remove('playing-indicator'));
    const card = document.querySelector(`.episode-card[data-id="${id}"]`);
    if (card) {
      card.classList.add('playing');
      card.querySelector('.ep-number').classList.add('playing-indicator');
    }

    if ('mediaSession' in navigator) {
      navigator.mediaSession.metadata = new MediaMetadata({
        title: ep.title,
        artist: 'Puritan Gold',
        album: ep.series || 'Daily Devotional'
      });
      navigator.mediaSession.setActionHandler('play', () => this.togglePlay());
      navigator.mediaSession.setActionHandler('pause', () => this.togglePlay());
      navigator.mediaSession.setActionHandler('previoustrack', () => this.skipBack());
      navigator.mediaSession.setActionHandler('nexttrack', () => this.skipForward());
    }

    this.saveState();
  },

  togglePlay() {
    if (this.audio.paused) {
      this.audio.play();
      this.updatePlayButton(true);
    } else {
      this.audio.pause();
      this.updatePlayButton(false);
    }
  },

  updatePlayButton(playing) {
    document.querySelector('.play-btn').innerHTML = playing
      ? '<svg class="icon" viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/></svg>'
      : '<svg class="icon" viewBox="0 0 24 24" fill="currentColor"><polygon points="6,4 20,12 6,20"/></svg>';
  },

  cycleSpeed() {
    this.speedIndex = (this.speedIndex + 1) % this.speeds.length;
    const speed = this.speeds[this.speedIndex];
    this.audio.playbackRate = speed;
    document.querySelector('.speed-btn').textContent = speed + 'x';
    localStorage.setItem('speed', this.speedIndex.toString());
  },

  skipBack() {
    this.audio.currentTime = Math.max(0, this.audio.currentTime - 15);
  },

  skipForward() {
    this.audio.currentTime = Math.min(this.audio.duration || 0, this.audio.currentTime + 30);
  },

  // Helpers
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
    const m = Math.floor(secs / 60);
    const s = Math.floor(secs % 60);
    return m + ':' + (s < 10 ? '0' : '') + s;
  },

  // Persistence
  isListened(id) { return localStorage.getItem('listened_' + id) === '1'; },
  markListened(id) { localStorage.setItem('listened_' + id, '1'); },
  savePosition(id, time) { localStorage.setItem('pos_' + id, time.toString()); },
  getPosition(id) { return parseFloat(localStorage.getItem('pos_' + id) || '0'); },

  saveState() {
    if (this.currentEp) localStorage.setItem('lastEp', this.currentEp.id.toString());
  },

  restoreState() {
    // Restore speed
    const savedSpeed = parseInt(localStorage.getItem('speed') || '1');
    if (savedSpeed >= 0 && savedSpeed < this.speeds.length) {
      this.speedIndex = savedSpeed;
      document.querySelector('.speed-btn').textContent = this.speeds[this.speedIndex] + 'x';
    }

    const lastId = parseInt(localStorage.getItem('lastEp') || '0');
    if (lastId) {
      const ep = this.episodes.find(e => e.id === lastId);
      if (ep) {
        this.currentEp = ep;
        document.querySelector('.player-bar').classList.add('visible');
        document.querySelector('.player-title').textContent = ep.title;
        document.querySelector('.player-time').textContent = 'Tap to resume';
        this.updatePlayButton(false);
      }
    }
  },

  setupServiceWorker() {
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('sw.js').catch(() => {});
    }
  }
};

document.addEventListener('DOMContentLoaded', () => App.init());
