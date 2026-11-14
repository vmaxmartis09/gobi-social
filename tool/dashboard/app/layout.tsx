import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Gobi Social — Affiliate Video Job Matrix',
  description: 'Minimalist Monochrome Dashboard for KOC AI Video Automation & Ingested Jobs',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="vi" className="dark">
      <body className="bg-[#09090b] text-zinc-100 min-h-screen antialiased selection:bg-white selection:text-black">
        {children}
      </body>
    </html>
  );
}
