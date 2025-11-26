// -------------------------------------------------------
// NeuroEdge Service Worker v1
// Offline Mode + Background Sync + Cache-First Strategy
// -------------------------------------------------------

const CACHE_NAME = "neuroedge-cache-v1";
const OFFLINE_URL = "/offline.html";

const ASSETS = [
  "/",
  "/index.html",
  "/offline.html",
  "/manifest.json",
  "/icons/icon-192.png",
  "/icons/icon-512.png",
  "/styles.css"
];

// -------------------------------------------------------
// Install → cache assets
// -------------------------------------------------------
self.addEventListener("install", (e) => {
  console.log("[SW] Install event");
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

// -------------------------------------------------------
// Activate → cleanup old cache
// -------------------------------------------------------
self.addEventListener("activate", (e) => {
  console.log("[SW] Activate event");
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) return caches.delete(key);
        })
      )
    )
  );
  self.clients.claim();
});

// -------------------------------------------------------
// Fetch → Offline-first strategy
// -------------------------------------------------------
self.addEventListener("fetch", (event) => {
  const req = event.request;

  // Only handle GET requests
  if (req.method !== "GET") return;

  event.respondWith(
    caches.match(req).then((cachedRes) => {
      const fetchPromise = fetch(req)
        .then((networkRes) => {
          // Cache new version
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(req, networkRes.clone());
          });
          return networkRes;
        })
        .catch(() => {
          // Offline fallback
          return cachedRes || caches.match(OFFLINE_URL);
        });

      return cachedRes || fetchPromise;
    })
  );
});

// -------------------------------------------------------
// Background Sync → send queued messages
// -------------------------------------------------------
self.addEventListener("sync", async (event) => {
  if (event.tag === "neuroedge-sync") {
    console.log("[SW] Background sync triggered");

    event.waitUntil(
      (async () => {
        try {
          const db = await openDB("neuroedge_db", 1);
          const queue = await db.getAll("queue");

          for (const item of queue) {
            try {
              await fetch("/api/send", {
                method: "POST",
                body: JSON.stringify(item.payload),
                headers: { "Content-Type": "application/json" },
              });

              await db.delete("queue", item.id);
            } catch (e) {
              console.error("Background sync failed", e);
              return;
            }
          }
        } catch (e) {
          console.error("Sync error", e);
        }
      })()
    );
  }
});
