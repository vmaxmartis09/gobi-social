'use client';

import React from 'react';
import { useJobStore } from '../store/useJobStore';
import { Search, RefreshCw, Plus, Radio, Wifi, WifiOff } from 'lucide-react';

export default function Navbar() {
  const {
    searchQuery,
    setSearchQuery,
    fetchJobs,
    isLoading,
    jobs,
    setIsCreateModalOpen,
    isRealtimeConnected,
    lastSyncTime,
  } = useJobStore();

  return (
    <header className="sticky top-0 z-30 w-full border-b border-white/[0.08] bg-[#09090b]/80 backdrop-blur-xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
        {/* Brand identity */}
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-white text-black flex items-center justify-center font-bold text-sm tracking-tighter shadow-sm">
            GB
          </div>
          <div className="flex flex-col">
            <div className="flex items-center gap-2">
              <span className="font-semibold text-sm tracking-wide text-white uppercase">Gobi Studio</span>
              <span className="px-1.5 py-0.5 rounded text-[10px] font-mono tracking-widest bg-zinc-800 text-zinc-400 border border-zinc-700/60">
                AFFILIATE JOBS
              </span>
            </div>
            <span className="text-[11px] text-zinc-500 font-mono">Google Flow & HyperFrames Suite</span>
          </div>
        </div>

        {/* Search Input */}
        <div className="flex-1 max-w-md relative hidden sm:block">
          <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-zinc-500" />
          <input
            type="text"
            placeholder="Tìm theo tên sản phẩm, tác giả (@creator), ID..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full bg-zinc-900/90 border border-zinc-800 text-zinc-200 text-xs rounded-full pl-9 pr-4 py-2 focus:outline-none focus:border-zinc-500 transition placeholder:text-zinc-600 font-mono"
          />
        </div>

        {/* Right Actions & Realtime Sync Indicator */}
        <div className="flex items-center gap-2.5">
          {/* Realtime Status Badge (Kokonut UI Live Pulse) */}
          <div
            title={
              isRealtimeConnected
                ? `Thời gian thực đang kết nối (SSE). Cập nhật gần nhất: ${lastSyncTime || 'vừa xong'}`
                : 'Đang kết nối lại thời gian thực...'
            }
            className={`hidden sm:flex items-center gap-1.5 px-3 py-1 rounded-full border text-[11px] font-mono tracking-wider transition-all ${
              isRealtimeConnected
                ? 'bg-emerald-950/30 border-emerald-500/30 text-emerald-300'
                : 'bg-zinc-900 border-zinc-800 text-zinc-500'
            }`}
          >
            <span className="relative flex h-2 w-2">
              {isRealtimeConnected && (
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              )}
              <span
                className={`relative inline-flex rounded-full h-2 w-2 ${
                  isRealtimeConnected ? 'bg-emerald-500' : 'bg-zinc-600'
                }`}
              ></span>
            </span>
            <span>{isRealtimeConnected ? 'REALTIME LIVE' : 'SYNCING...'}</span>
            {lastSyncTime && (
              <span className="text-[10px] text-emerald-400/60 hidden lg:inline border-l border-emerald-500/20 pl-1.5">
                {lastSyncTime}
              </span>
            )}
          </div>

          {/* Primary CTA: Nạp Job Mới */}
          <button
            onClick={() => setIsCreateModalOpen(true)}
            className="px-3.5 py-1.5 rounded-full bg-white hover:bg-zinc-200 text-black font-semibold text-xs font-mono flex items-center gap-1.5 shadow-sm transition active:scale-95"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>Nạp Job Mới</span>
          </button>

          {/* Total Jobs Pill */}
          <div className="hidden md:flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-zinc-900 border border-zinc-800 text-xs font-mono text-zinc-400">
            <span>{jobs.length} JOBS</span>
          </div>

          <button
            onClick={() => fetchJobs()}
            disabled={isLoading}
            className="p-2 rounded-full bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 text-zinc-300 hover:text-white transition disabled:opacity-50"
            title="Làm mới danh sách Jobs"
          >
            <RefreshCw className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
          </button>
        </div>
      </div>
    </header>
  );
}
