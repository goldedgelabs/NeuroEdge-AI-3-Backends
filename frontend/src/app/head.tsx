// src/app/head.tsx
export default function HeadMeta() {
  return (
    <>
      {/* Standard PWA */}
      <meta name="application-name" content="NeuroEdge" />
      <meta name="apple-mobile-web-app-capable" content="yes" />
      <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
      <meta name="apple-mobile-web-app-title" content="NeuroEdge" />
      <meta name="theme-color" content="#071022" />

      {/* iOS splash icons (replace with actual PNG files in public/icons/) */}
      <link rel="apple-touch-icon" href="/icons/icon-192.png" />
      <link rel="apple-touch-icon" sizes="180x180" href="/icons/icon-192.png" />
      {/* iOS splash screens: generate images for each device or use one large maskable icon */}
      <link rel="manifest" href="/manifest.json" />

      {/* viewport for standalone styling (safe-area insets) */}
      <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover" />

      {/* Prevent telephone detection on iOS messing with layout */}
      <meta name="format-detection" content="telephone=no" />
    </>
  );
}
