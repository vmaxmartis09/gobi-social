'use client';

import React, { useEffect, useState } from 'react';
import Navbar from '../components/Navbar';
import StatsOverview from '../components/StatsOverview';
import JobFilterTabs from '../components/JobFilterTabs';
import JobList from '../components/JobList';
import JobDetailModal from '../components/JobDetailModal';
import CreateJobModal from '../components/CreateJobModal';
import { useJobStore } from '../store/useJobStore';
import { Sparkles, Terminal, Video, Plus, Link as LinkIcon, ArrowRight } from 'lucide-react';

export default function DashboardPage() {
  const { initRealtimeSync, createJob, isCreating } = useJobStore();
  const [quickUrl, setQuickUrl] = useState('');

  // Mount Realtime SSE Listener
  useEffect(() => {
    const cleanup = initRealtimeSync();
    return () => {
      cleanup();
    };
  }, [initRealtimeSync]);

  const handleQuickSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!quickUrl.trim() || isCreating) return;
    const url = quickUrl.trim();
    setQuickUrl('');
    await createJob(url);
  };

  return (
    <div className="min-h-screen bg-[#09090b] text-zinc-100 flex flex-col font-sans selection:bg-white selection:text-black">
      {/* Navbar with Realtime SSE Status */}
      <Navbar />

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 relative">
        {/* Subtle Ambient Radial Glow in Header */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[700px] h-[280px] bg-gradient-to-b from-white/[0.04] to-transparent rounded-full blur-3xl pointer-events-none -z-10" />

        {/* Hero Title & Fast Ingestion Strip */}
        <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-6 pb-6 border-b border-white/[0.08]">
          <div className="max-w-xl">
            <div className="flex items-center gap-2 mb-2">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              <span className="text-xs font-mono uppercase tracking-widest text-zinc-400">
                Gobi Social Autonomous Engine • Realtime Active
              </span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-white">
              Affiliate Video Job Pipeline
            </h1>
            <p className="text-xs sm:text-sm text-zinc-400 mt-1 font-mono leading-relaxed">
              Quản lý tiến độ sản xuất video KOC AI từ dữ liệu nạp sản phẩm, chỉ số tương tác, sinh prompt Google Flow & render HeyGen HyperFrames.
            </p>
          </div>

          {/* Quick Input Bar Directly in Hero (Kokonut UI Fast Ingest) */}
          <form
            onSubmit={handleQuickSubmit}
            className="w-full lg:max-w-md p-1.5 rounded-2xl bg-zinc-900/80 border border-zinc-700/70 backdrop-blur-xl flex items-center gap-2 shadow-lg"
          >
            <div className="pl-3 text-zinc-500">
              <LinkIcon className="w-4 h-4" />
            </div>
            <input
              type="url"
              placeholder="Dán link TikTok (vd: https://vt.tiktok.com/...)"
              value={quickUrl}
              onChange={(e) => setQuickUrl(e.target.value)}
              disabled={isCreating}
              className="flex-1 bg-transparent text-xs sm:text-sm text-zinc-100 placeholder:text-zinc-500 focus:outline-none font-mono py-1.5"
            />
            <button
              type="submit"
              disabled={!quickUrl.trim() || isCreating}
              className="px-4 py-2 rounded-xl bg-white hover:bg-zinc-200 text-black font-semibold text-xs font-mono flex items-center gap-1.5 transition active:scale-95 disabled:opacity-40 shadow-sm flex-shrink-0"
            >
              <span>{isCreating ? 'Đang Nạp...' : 'Xử Lý Job'}</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </form>
        </div>

        {/* 4 Stats Cards */}
        <StatsOverview />

        {/* Status Filter Tabs */}
        <JobFilterTabs />

        {/* Grid of Job Cards */}
        <JobList />
      </main>

      {/* Modals */}
      <CreateJobModal />
      <JobDetailModal />

      {/* Footer */}
      <footer className="border-t border-white/[0.06] py-6 text-center text-xs text-zinc-600 font-mono">
        Gobi Social © 2026 • Black & White Minimalist Suite • Realtime Event-Driven Architecture
      </footer>
    </div>
  );
}
