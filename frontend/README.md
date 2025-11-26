# NeuroEdge Frontend
Prepared frontend bundle. Run `npm ci` and `npm run build` in the frontend directory.
NeuroEdge - Offline & Secure features

This document shows the new offline & secure features added:

- iOS standalone meta & CSS safe-area handling (`src/app/head.tsx`, `src/styles/globals.css`)
- Service worker with background sync & periodic sync (`public/sw.js`)
- Service worker registration & periodic sync client (`src/pwa/register-sw.ts`)
- Periodic flush fallback (`src/pwa/periodic-flush.ts`)
- Local WebGPU offline fallback generator (`src/lib/local-ai/webgpu.ts`)
- Encrypted local storage wrapper (`src/lib/secure-storage.ts`)
- Dexie encryption adapter example (`src/lib/encrypted-db-adapter.ts`)

Testing:
- With Chrome, install PWA and test offline behaviours:
  - Open DevTools → Application → Service Workers
  - Turn offline mode on, submit chat messages (they should be queued)
  - Turn online; background sync should flush queued items
- For iOS, Safari PWA support is limited: add to Home Screen and open the installed app to test safe-area CSS.

Security notes:
- If you want encryption protected by a passphrase, call `initMasterKey(passphrase)` on login or from Settings. If no passphrase given, the key is generated and persisted in IndexedDB (convenience; less secure than passphrase-protection).
