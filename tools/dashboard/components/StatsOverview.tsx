'use client';

import React from 'react';
import { useJobStore } from '../store/useJobStore';
import { Video, Eye, CheckCircle2, Clock, Flame } from 'lucide-react';

export default function StatsOverview() {
  const { jobs } = useJobStore();

  const totalJobs = jobs.length;
  const doneCount = jobs.filter((j) => j.status === 'DA_LAM_VIDEO' || j.status === 'DA_DANG').length;
  const pendingCount = jobs.filter((j) => j.status === 'CHUA_LAM').length;

  const totalPlays = jobs.reduce((acc, j) => acc + (j.stats.plays || 0), 0);
  const totalLikes = jobs.reduce((acc, j) => acc + (j.stats.likes || 0), 0);

  const formatNumber = (num: number) => {
    if (num >= 1_000_000) return (num / 1_000_000).toFixed(1) + 'M';
    if (num >= 1_000) return (num / 1_000).toFixed(1) + 'K';
    return num.toLocaleString();
  };

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-2.5 sm:gap-3 my-5">
      {/* Stat 1: Total Jobs */}
      <div className="kokonut-card p-3 rounded-xl relative overflow-hidden group transition hover:border-zinc-700">
        <div className="flex items-center justify-between mb-1.5">
          <span className="text-[10px] font-mono tracking-wider text-zinc-500 uppercase">Tổng Jobs</span>
          <div className="w-5 h-5 rounded-md bg-zinc-800/80 flex items-center justify-center text-zinc-300">
            <Clock className="w-3 h-3" />
          </div>
        </div>
        <div className="text-xl sm:text-2xl font-bold text-white tracking-tight">{totalJobs}</div>
        <div className="text-[10px] text-zinc-500 mt-0.5 flex items-center gap-1 font-mono">
          <span>{pendingCount} chưa làm video</span>
        </div>
      </div>

      {/* Stat 2: Video Done Rate */}
      <div className="kokonut-card p-3 rounded-xl relative overflow-hidden group transition hover:border-zinc-700">
        <div className="flex items-center justify-between mb-1.5">
          <span className="text-[10px] font-mono tracking-wider text-zinc-500 uppercase">Tiến Độ Video</span>
          <div className="w-5 h-5 rounded-md bg-white text-black flex items-center justify-center font-bold text-xs">
            <CheckCircle2 className="w-3 h-3" />
          </div>
        </div>
        <div className="text-xl sm:text-2xl font-bold text-white tracking-tight">
          {doneCount} <span className="text-xs font-normal text-zinc-500">/ {totalJobs}</span>
        </div>
        <div className="text-[10px] text-zinc-400 mt-0.5 font-mono">
          {totalJobs > 0 ? Math.round((doneCount / totalJobs) * 100) : 0}% hoàn thành
        </div>
      </div>

      {/* Stat 3: Total Captured Views */}
      <div className="kokonut-card p-3 rounded-xl relative overflow-hidden group transition hover:border-zinc-700">
        <div className="flex items-center justify-between mb-1.5">
          <span className="text-[10px] font-mono tracking-wider text-zinc-500 uppercase">Reach Cào Về</span>
          <div className="w-5 h-5 rounded-md bg-zinc-800/80 flex items-center justify-center text-zinc-300">
            <Eye className="w-3 h-3" />
          </div>
        </div>
        <div className="text-xl sm:text-2xl font-bold text-white tracking-tight">{formatNumber(totalPlays)}</div>
        <div className="text-[10px] text-zinc-500 mt-0.5 font-mono">
          {formatNumber(totalLikes)} lượt thích
        </div>
      </div>

      {/* Stat 4: Automation Engine */}
      <div className="kokonut-card p-3 rounded-xl relative overflow-hidden group transition hover:border-zinc-700">
        <div className="flex items-center justify-between mb-1.5">
          <span className="text-[10px] font-mono tracking-wider text-zinc-500 uppercase">Render Engine</span>
          <div className="w-5 h-5 rounded-md bg-zinc-800/80 flex items-center justify-center text-zinc-300">
            <Flame className="w-3 h-3" />
          </div>
        </div>
        <div className="text-sm font-semibold text-white tracking-tight flex items-center gap-1.5 mt-0.5">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
          <span>Flow + HyperFrames</span>
        </div>
        <div className="text-[10px] text-zinc-500 mt-0.5 font-mono">Chuẩn Safe Zone 9:16</div>
      </div>
    </div>
  );
}
