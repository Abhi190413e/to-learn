const CACHE_NAME = 'new-educate-v1';
const ASSETS_TO_CACHE = [
  '/',
  '/static/css/styles.css',
  '/static/js/script.js',
  '/static/manifest.json',
  '/assets/logo.png',
  '/assets/students_hero.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        return cache.addAll(ASSETS_TO_CACHE);
      })
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        return response || fetch(event.request);
      })
  );
});
