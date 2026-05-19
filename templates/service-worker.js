const CACHE_NAME = 'geodinagat-v2'; // Updated to v2 to force a refresh

// ONLY cache local URLs to prevent CORS crashes
const ASSETS_TO_CACHE = [
    '/',
    '/offline/',
    '/static/manifest.json'
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(cache => {
            return cache.addAll(ASSETS_TO_CACHE);
        })
    );
    self.skipWaiting(); // Forces the browser to activate this worker immediately
});

self.addEventListener('activate', event => {
    event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', event => {
    // If the user is trying to navigate to a new webpage (HTML)
    if (event.request.mode === 'navigate') {
        event.respondWith(
            fetch(event.request).catch(() => {
                // If the network fails (offline), show the offline.html page
                return caches.match('/offline/');
            })
        );
    } else {
        // For everything else, try the network first, then cache
        event.respondWith(
            fetch(event.request).catch(() => {
                return caches.match(event.request);
            })
        );
    }
});