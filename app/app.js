const App = {
  episodes: [],
  audio: new Audio(),
  currentEp: null,
  currentView: 'episodes',

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
      const dayLabel = this.getDayLabel(ep.id);

      html += `
        <div class="episode-card ${listened ? 'listened' : ''}" data-id="${ep.id}" onclick="App.playEpisode(${ep.id})">
          <div class="ep-number" id="ep-num-${ep.id}">${dayLabel}</div>
          <div class="ep-info">
            <div class="ep-title">${ep.title}</div>
            <div class="ep-subtitle">${ep.subtitle || ''}</div>
            <div class="ep-meta">
              <span class="ep-series-badge ${seriesClass}">${ep.series || 'General'}</span>
              ${ep.duration} min
            </div>
          </div>
        </div>`;
    });

    container.innerHTML = html;
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
      4: 'Living Wisely — Proverbs 13-16 & Practical Theology'
    };

    Object.keys(weeks).sort((a,b) => a-b).forEach(w => {
      const days = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
      html += `<div class="schedule-week">
        <div class="schedule-week-title">Week ${w}: ${weekThemes[w] || ''}</div>`;
      weeks[w].forEach((ep, i) => {
        const listened = this.isListened(ep.id);
        html += `<div class="schedule-day" onclick="App.playEpisode(${ep.id})" style="cursor:pointer;opacity:${listened ? 0.5 : 1}">
          <div class="schedule-day-label">${days[i] || ''}</div>
          <div class="schedule-day-title">${listened ? '✓ ' : ''}${ep.title}</div>
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
      // Save position every 5 seconds
      if (this.currentEp && Math.floor(this.audio.currentTime) % 5 === 0) {
        this.savePosition(this.currentEp.id, this.audio.currentTime);
      }
    });

    this.audio.addEventListener('ended', () => {
      this.markListened(this.currentEp.id);
      this.renderEpisodes();
      this.renderSchedule();
      // Auto-play next
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

    // Restore saved position
    const saved = this.getPosition(id);
    if (saved > 0) {
      this.audio.currentTime = saved;
    }

    this.audio.play();

    // Update UI
    document.querySelector('.player-bar').classList.add('visible');
    document.querySelector('.player-title').textContent = ep.title;
    document.querySelector('.player-time').textContent = '0:00 / ' + ep.duration;

    // Update play button
    this.updatePlayButton(true);

    // Highlight current card
    document.querySelectorAll('.episode-card').forEach(c => c.classList.remove('playing'));
    document.querySelectorAll('.ep-number').forEach(n => n.classList.remove('playing-indicator'));
    const card = document.querySelector(`.episode-card[data-id="${id}"]`);
    if (card) {
      card.classList.add('playing');
      card.querySelector('.ep-number').classList.add('playing-indicator');
    }

    // MediaSession API for lock screen controls
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

  skipBack() {
    this.audio.currentTime = Math.max(0, this.audio.currentTime - 15);
  },

  skipForward() {
    this.audio.currentTime = Math.min(this.audio.duration, this.audio.currentTime + 30);
  },

  // Helpers
  getWeekNumber(id) { return Math.ceil(id / 7); },

  getDayLabel(id) {
    const days = ['M','T','W','T','F','S','S'];
    return days[(id - 1) % 7] || id;
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
    if (this.currentEp) {
      localStorage.setItem('lastEp', this.currentEp.id.toString());
    }
  },

  restoreState() {
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
