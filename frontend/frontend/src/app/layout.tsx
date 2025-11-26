import './globals.css';
import { ReactNode } from 'react';
export const metadata = { title: 'NeuroEdge', description: 'NeuroEdge frontend' };
export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <div className="min-h-screen">
          {children}
        </div>
      </body>
    </html>
  );
}
