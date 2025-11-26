'use client';

import React, { useEffect, useRef, useState } from 'react';
import { db } from '@/lib/offline-db';
import { getStreamURL } from '@/services/backendSelector';

export default function ChatStream() {
  const [messages, setMessages] = useState<string[]>([]);
  const evtRef = useRef<EventSource | null>(null);

  useEffect(() => {
    let mounted = true;

    // 1. Load OFFLINE cached conversations (Dexie)
    (async () => {
      try {
        const cached = await db.messages.toArray();
        if (cached && cached.length && mounted) {
          setMessages(cached.map((m) => m.text));
        }
      } catch (e) {
        console.warn("Dexie load error", e);
      }
    })();

    // 2. Start the streaming connection
    async function start() {
      const url = await getStreamURL();
      if (!url) {
        console.error("No backend URL: backendSelector returned null");
        return;
      }

      const es = new EventSource(url);
      evtRef.current = es;

      es.onmessage = async (ev) => {
        if (!mounted) return;

        let token = ev.data;

        // Support JSON { token: "hi", done: false }
        try {
          const parsed = JSON.parse(ev.data);
          if (parsed?.token) token = parsed.token;
        } catch {
          /* plain text token */
        }

        setMessages((prev) => {
          if (prev.length === 0) {
            const next = [token];
            // save offline
            db.messages.add({ text: token });
            return next;
          }

          const last = prev[prev.length - 1];
          const updated = [...prev.slice(0, -1), last + token];

          // update offline db
          db.messages.clear().then(() => {
            updated.forEach((msg) => db.messages.add({ text: msg }));
          });

          return updated;
        });
      };

      es.onerror = (err) => {
        console.error("SSE error", err);
        es.close();
      };
    }

    start();

    // cleanup on unmount
    return () => {
      mounted = false;
      if (evtRef.current) evtRef.current.close();
    };
  }, []);

  return (
    <div className="p-3">
      <div className="space-y-3">
        {messages.map((m, i) => (
          <div
            key={i}
            className="p-3 bg-white dark:bg-neutral-800 border dark:border-neutral-700 rounded shadow-sm"
            data-testid="assistant-message-stream"
          >
            {m}
          </div>
        ))}
      </div>
    </div>
  );
          }
