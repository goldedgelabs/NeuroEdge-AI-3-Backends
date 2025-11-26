// src/lib/encrypted-db-adapter.ts
import { db } from '@/lib/offline-db';
import { encryptJSON, decryptJSON } from '@/lib/secure-storage';

export async function addEncryptedMessage(msg: any) {
  const cipher = await encryptJSON(msg);
  return db.table('messages').add({ cipher, createdAt: Date.now() });
}

export async function getDecryptedMessages() {
  const rows = await db.table('messages').toArray();
  const out = [];
  for (const r of rows) {
    try {
      const obj = await decryptJSON(r.cipher);
      out.push({ ...obj, _id: r.id });
    } catch (e) {
      // fallback: if decryption fails, skip or return raw
      out.push({ _raw: r });
    }
  }
  return out;
}
