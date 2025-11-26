'use client';

import React, { useEffect } from 'react';
import { registerServiceWorker } from '@/pwa/register-sw';
import '@/styles/globals.css';
import FloatingChat from '@/components/chat-floating/FloatingChat';
import { ReactNode } from 'react';

export const metadata = {
  title: 'NeuroEdge',
  description: 'NeuroEdge frontend',
};

export default function RootLayout({ children }: { children: ReactNode }) {
  useEffect(() => {
    registerServiceWorker();
  }, []);

  return (
    <html lang="en">
      <head />
      <body className="app-shell min-h-screen">
        {children}

        {/* Floating Chat UI */}
        <FloatingChat />
      </body>
    </html>
  );
}
