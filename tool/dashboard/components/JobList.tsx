'use client';

import React from 'react';
import { useJobStore } from '../store/useJobStore';
import JobCard from './JobCard';
import { Layers } from 'lucide-react';

export default function JobList() {
  const { jobs, activeFilter, searchQuery, isLoading, cardViewMode } = useJobStore();

  const filteredJobs = jobs
    .filter((job) => {
      // Filter by active category/status
      if (activeFilter !== 'ALL') {
        if (activeFilter === 'HAS_VIDEO') {
          if (!job.assets?.has_video) return false;
        } else if (activeFilter === 'HAS_SHOP') {
          if (!job.affiliate_pdp_url) return false;
        } else if (activeFilter === 'VIRAL') {
          if ((job.stats?.plays || 0) < 100000) return false;
        } else if (activeFilter === 'TOP_LIKES') {
          if ((job.stats?.likes || 0) < 5000) return false;
        } else {
          // JobStatus
          if (job.status !== activeFilter) return false;
        }
      }

      // Filter by search query
      if (searchQuery.trim()) {
        const q = searchQuery.toLowerCase();
        const matchTitle = job.title?.toLowerCase().includes(q);
        const matchAuthor =
          job.author?.unique_id?.toLowerCase().includes(q) ||
          job.author?.nickname?.toLowerCase().includes(q);
        const matchId = job.id?.toLowerCase().includes(q);
        const matchKeyword = job.keyword?.toLowerCase().includes(q);
        return matchTitle || matchAuthor || matchId || matchKeyword;
      }

      return true;
    })
    .sort((a, b) => {
      if (activeFilter === 'TOP_LIKES') {
        return (b.stats?.likes || 0) - (a.stats?.likes || 0);
      }
      if (activeFilter === 'VIRAL') {
        return (b.stats?.plays || 0) - (a.stats?.plays || 0);
      }
      return 0;
    });

  if (isLoading) {
    return (
      <div className="py-20 text-center">
        <div className="w-8 h-8 rounded-full border-2 border-white/20 border-t-white animate-spin mx-auto mb-3"></div>
        <p className="text-xs font-mono text-zinc-500 uppercase tracking-widest">
          Đang nạp danh sách Jobs...
        </p>
      </div>
    );
  }

  if (filteredJobs.length === 0) {
    return (
      <div className="kokonut-card rounded-2xl py-14 px-6 text-center border-dashed my-4">
        <div className="w-10 h-10 rounded-full bg-zinc-900 border border-zinc-800 flex items-center justify-center text-zinc-600 mx-auto mb-3">
          <Layers className="w-5 h-5" />
        </div>
        <h3 className="text-sm font-semibold text-zinc-200">Không tìm thấy Job nào</h3>
        <p className="text-xs text-zinc-500 max-w-sm mx-auto mt-1 font-mono">
          {searchQuery
            ? `Không có kết quả khớp với "${searchQuery}". Thử từ khoá khác.`
            : `Chưa có Job nào khớp với bộ lọc "${activeFilter}". Thử chọn bộ lọc khác.`}
        </p>
      </div>
    );
  }

  // Render in Compact List view
  if (cardViewMode === 'compact') {
    return (
      <div className="flex flex-col gap-2 my-3">
        {filteredJobs.map((job) => (
          <JobCard key={job.id} job={job} />
        ))}
      </div>
    );
  }

  // Render in Refined Compact Grid view (3-4 columns)
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-3 xl:grid-cols-4 gap-3 sm:gap-3.5 my-3">
      {filteredJobs.map((job) => (
        <JobCard key={job.id} job={job} />
      ))}
    </div>
  );
}
