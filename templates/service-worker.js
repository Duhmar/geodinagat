// templates/service-worker.js
const CACHE_NAME = 'geodinagat-v1';
const ASSETS_TO_CACHE = [
    '/', // Caches the home page
    '/offline/', // Optional: A fallback page
    'https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
    'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css',
    'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'
];

// 1. Install Event: Download and save the assets
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => {
                console.log('Opened cache');
                return cache.addAll(ASSETS_TO_CACHE);
            })
    );
});

// 2. Fetch Event: Intercept network requests
self.addEventListener('fetch', event => {
    event.respondWith(
        // Try the network first
        fetch(event.request).catch(() => {
            // If network fails (offline), load from cache!
            return caches.match(event.request);
        })
    );
});