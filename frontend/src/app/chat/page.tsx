'use client';

import React, { useEffect } from 'react';
import ChatInput from '@/components/chat/ChatInput';
import ChatStream from '@/components/chat/ChatStream';

import { getDecryptedMessages } from '@/lib/encrypted-db-adapter';
import { addMessageToDB } from '@/lib/offline-db';

export default function ChatPage() {
  // Restore encrypted chats on mount
  useEffect(() => {
    (async () => {
      try {
        const msgs = await getDecryptedMessages();
        // Optionally hydrate UI store if you use Zustand/Redux.
        console.log("Decrypted offline messages:", msgs);
      } catch (err) {
        console.error("Failed loading encrypted messages", err);
      }
    })();
  }, []);

  // Optional: local AI fallback boot (WebGPU)
  useEffect(() => {
    async function loadLocalAI() {
      if (!navigator.onLine) {
        console.log("Offline → enable WebGPU fallback");
        try {
          const mod = await import('@/lib/local-ai/webgpu-engine');
          await mod.initLocalModel();
        } catch (err) {
          console.warn("Local WebGPU fallback unavailable:", err);
        }
      }
    }
    loadLocalAI();
  }, []);

  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-2xl font-semibold mb-4">Chat</h1>

      {/* STREAM UI */}
      <div className="border rounded p-4 mb-4 bg-ne-card">
        <ChatStream />
      </div>

      {/* INPUT UI */}
      <ChatInput />

      <div className="mt-4 text-xs text-muted-foreground">
        NeuroEdge can make mistakes — verify important info.
      </div>
    </div>
  );
}
