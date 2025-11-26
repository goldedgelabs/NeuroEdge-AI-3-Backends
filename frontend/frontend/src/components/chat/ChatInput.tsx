'use client';
import React, { useState } from 'react';
import { sendChatMessage } from '@/services/http';
export default function ChatInput(){
  const [text, setText] = useState('');
  const [sending, setSending] = useState(false);
  async function send(){
    if(!text) return;
    setSending(true);
    try{
      await sendChatMessage(text);
      setText('');
    }catch(e){
      console.error(e);
    }finally{
      setSending(false);
    }
  }
  return (
    <div className="flex items-center gap-2">
      <input value={text} onChange={e=>setText(e.target.value)} className="flex-1 border rounded px-3 py-2" placeholder="Type a message..." data-testid="chat-input"/>
      <button onClick={send} className="px-4 py-2 bg-ne-primary text-white rounded" data-testid="send-btn">
        {sending ? 'Sending...' : 'Send'}
      </button>
    </div>
  )
}
