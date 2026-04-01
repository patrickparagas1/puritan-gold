const CACHE_NAME = 'puritan-gold-v27';
const SHELL_FILES = [
  'index.html',
  'style.css',
  'app.js',
  'manifest.json'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(SHELL_FILES))
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);

  // Don't cache audio files (too large), stream them directly
  if (url.pathname.endsWith('.mp3')) {
    return;
  }

  // Don't cache Firebase SDK / Auth / Firestore requests — let them pass through
  const host = url.hostname;
  if (host.includes('gstatic.com') || host.includes('firebaseapp.com') ||
      host.includes('googleapis.com') || host.includes('firestore.googleapis.com') ||
      host.includes('identitytoolkit.googleapis.com') || host.includes('securetoken.googleapis.com')) {
    return;
  }

  // For episodes.json, try network first (so new episodes appear)
  if (url.pathname.endsWith('episodes.json')) {
    event.respondWith(
      fetch(event.request)
        .then(response => {
          const clone = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
          return response;
        })
        .catch(() => caches.match(event.request))
    );
    return;
  }

  // Network-first for app shell files (so updates appear faster)
  event.respondWith(
    fetch(event.request)
      .then(response => {
        const clone = response.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        return response;
      })
      .catch(() => caches.match(event.request))
  );
});
