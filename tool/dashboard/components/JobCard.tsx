'use client';

import React, { useState } from 'react';
import { JobItem, JobStatus } from '../lib/types';
import { useJobStore } from '../store/useJobStore';
import {
  Play,
  Check,
  ExternalLink,
  Eye,
  Heart,
  MessageCircle,
  Share2,
  ChevronRight,
  Sparkles,
  ShoppingBag,
} from 'lucide-react';

interface JobCardProps {
  job: JobItem;
}

export default function JobCard({ job }: JobCardProps) {
  const { setSelectedJob, updateJobStatus, copiedKey, setCopiedKey, cardViewMode } = useJobStore();

  const formatNumber = (num: number) => {
    if (!num) return '0';
    if (num >= 1_000_000) return (num / 1_000_000).toFixed(1) + 'M';
    if (num >= 1_000) return (num / 1_000).toFixed(1) + 'K';
    return num.toLocaleString();
  };

  const videoTypeBadge =
    job.video_type === 'talking_head'
      ? { icon: '🗣️', label: 'Nói trực diện' }
      : job.video_type === 'product_only'
      ? { icon: '🛍️', label: 'Chỉ sản phẩm' }
      : null;

  const statusConfig: Record<
    JobStatus,
    { label: string; bg: string; text: string; border: string; dot: string }
  > = {
    CHUA_LAM: {
      label: 'Chưa làm',
      bg: 'bg-zinc-900',
      text: 'text-zinc-400',
      border: 'border-zinc-800',
      dot: 'bg-zinc-600',
    },
    DANG_LAM: {
      label: 'Đang làm',
      bg: 'bg-zinc-900',
      text: 'text-white',
      border: 'border-amber-400/40',
      dot: 'bg-amber-400 animate-pulse',
    },
    DA_LAM_VIDEO: {
      label: 'Đã làm',
      bg: 'bg-white',
      text: 'text-black font-semibold',
      border: 'border-white',
      dot: 'bg-black',
    },
    DA_DANG: {
      label: 'Đã đăng',
      bg: 'bg-zinc-800',
      text: 'text-zinc-200',
      border: 'border-emerald-500/40',
      dot: 'bg-emerald-400',
    },
  };

  const currentStatus = statusConfig[job.status] || statusConfig.CHUA_LAM;

  const handleCopyPrompt = (e: React.MouseEvent) => {
    e.stopPropagation();
    navigator.clipboard.writeText(job.prompts.google_flow_prompt);
    setCopiedKey(job.id);
    setTimeout(() => {
      setCopiedKey(null);
    }, 2000);
  };

  const handleStatusCycle = (e: React.MouseEvent) => {
    e.stopPropagation();
    const cycleOrder: JobStatus[] = ['CHUA_LAM', 'DANG_LAM', 'DA_LAM_VIDEO', 'DA_DANG'];
    const nextIdx = (cycleOrder.indexOf(job.status) + 1) % cycleOrder.length;
    updateJobStatus(job.id, cycleOrder[nextIdx]);
  };

  const isCopied = copiedKey === job.id;

  // COMPACT LIST VIEW
  if (cardViewMode === 'compact') {
    return (
      <div
        onClick={() => setSelectedJob(job)}
        className="kokonut-card rounded-xl px-3 py-2.5 cursor-pointer flex items-center justify-between gap-3 group transition-all duration-200 hover:border-zinc-500/40 hover:bg-zinc-900/90"
      >
        {/* Left: Thumbnail & Main Info */}
        <div className="flex items-center gap-3 min-w-0 flex-1">
          {/* Micro thumbnail */}
          <div className="w-10 h-10 rounded-lg bg-zinc-900 border border-zinc-800 overflow-hidden relative flex-shrink-0">
            {job.assets.cover_url ? (
              <img
                src={job.assets.cover_url}
                alt={job.title}
                className="w-full h-full object-cover group-hover:scale-105 transition duration-200"
              />
            ) : (
              <div className="w-full h-full flex items-center justify-center text-zinc-700">
                <Play className="w-3 h-3" />
              </div>
            )}
            {job.assets.has_video && (
              <div className="absolute inset-0 bg-black/40 flex items-center justify-center opacity-60">
                <Play className="w-2.5 h-2.5 fill-white text-white ml-0.5" />
              </div>
            )}
          </div>

          {/* Title & Metadata */}
          <div className="min-w-0 flex-1">
            <div className="flex items-center gap-2">
              <span className="font-mono text-[10px] text-zinc-500">{job.id}</span>
              <span className="text-[10px] text-zinc-400 font-mono">@{job.author.unique_id}</span>
              {job.affiliate_pdp_url && (
                <span className="px-1 py-0.2 rounded bg-zinc-800 text-[9px] font-mono text-zinc-400 flex items-center gap-0.5">
                  <ShoppingBag className="w-2.5 h-2.5" /> Shop
                </span>
              )}
            </div>
            <h4 className="text-xs font-medium text-zinc-200 truncate group-hover:text-white transition">
              {job.title}
            </h4>
          </div>
        </div>

        {/* Center: Micro stats */}
        <div className="hidden sm:flex items-center gap-3 text-[11px] font-mono text-zinc-400 flex-shrink-0">
          <span className="flex items-center gap-1">
            <Eye className="w-3 h-3 text-zinc-500" /> {formatNumber(job.stats.plays)}
          </span>
          <span className="flex items-center gap-1">
            <Heart className="w-3 h-3 text-zinc-500" /> {formatNumber(job.stats.likes)}
          </span>
        </div>

        {/* Right: Status & Actions */}
        <div className="flex items-center gap-2 flex-shrink-0">
          {videoTypeBadge && (
            <span
              title="Loại video đã tự động phát hiện"
              className="px-2 py-0.5 rounded-full text-[10px] font-mono bg-zinc-900 text-zinc-400 border border-zinc-800 flex items-center gap-1"
            >
              <span>{videoTypeBadge.icon}</span>
              <span>{videoTypeBadge.label}</span>
            </span>
          )}
          <button
            onClick={handleStatusCycle}
            title="Bấm để đổi nhanh trạng thái"
            className={`px-2 py-0.5 rounded-full text-[10px] font-mono tracking-wider flex items-center gap-1.5 transition-all border ${currentStatus.bg} ${currentStatus.text} ${currentStatus.border}`}
          >
            <span className={`w-1.5 h-1.5 rounded-full ${currentStatus.dot}`}></span>
            <span>{currentStatus.label}</span>
          </button>

          <button
            onClick={handleCopyPrompt}
            title="Copy Prompt Flow"
            className={`p-1.5 rounded-lg text-xs font-mono transition-all ${
              isCopied
                ? 'bg-white text-black font-semibold'
                : 'bg-zinc-900 hover:bg-zinc-800 text-zinc-400 hover:text-white border border-zinc-800'
            }`}
          >
            {isCopied ? <Check className="w-3.5 h-3.5" /> : <Sparkles className="w-3.5 h-3.5" />}
          </button>

          <span className="p-1 text-zinc-500 group-hover:text-zinc-200 transition">
            <ChevronRight className="w-4 h-4" />
          </span>
        </div>
      </div>
    );
  }

  // REFINED COMPACT GRID CARD VIEW (Default)
  return (
    <div
      onClick={() => setSelectedJob(job)}
      className="kokonut-card rounded-xl p-3 cursor-pointer flex flex-col justify-between group relative overflow-hidden transition-all duration-200 hover:-translate-y-0.5 hover:border-zinc-500/40 hover:shadow-lg hover:shadow-black/50"
    >
      {/* Top Bar: ID & Quick Status Pill */}
      <div>
        <div className="flex items-center justify-between gap-1.5 mb-2">
          <span className="font-mono text-[10px] text-zinc-500 tracking-wider truncate max-w-[120px]">
            {job.id}
          </span>

          <div className="flex items-center gap-1 flex-shrink-0">
            {videoTypeBadge && (
              <span
                title="Loại video đã tự động phát hiện"
                className="px-1.5 py-0.5 rounded-full text-[9px] font-mono bg-zinc-900 text-zinc-400 border border-zinc-800"
              >
                {videoTypeBadge.icon}
              </span>
            )}
            <button
              onClick={handleStatusCycle}
              title="Bấm để đổi nhanh trạng thái"
              className={`px-2 py-0.5 rounded-full text-[9px] font-mono tracking-wider flex items-center gap-1 transition-all border flex-shrink-0 ${currentStatus.bg} ${currentStatus.text} ${currentStatus.border}`}
            >
              <span className={`w-1.5 h-1.5 rounded-full ${currentStatus.dot}`}></span>
              <span>{currentStatus.label}</span>
            </button>
          </div>
        </div>

        {/* Thumbnail Preview Banner */}
        <div className="w-full h-32 sm:h-36 rounded-lg bg-zinc-900 border border-zinc-800/80 overflow-hidden relative group-hover:border-zinc-700 transition">
          {job.assets.cover_url ? (
            <img
              src={job.assets.cover_url}
              alt={job.title}
              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
            />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-zinc-700">
              <Play className="w-6 h-6" />
            </div>
          )}

          {/* Subtle gradient overlay */}
          <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-black/20 pointer-events-none" />

          {/* Center Play Icon if Video Available */}
          {job.assets.has_video && (
            <div className="absolute inset-0 flex items-center justify-center opacity-70 group-hover:opacity-100 transition">
              <div className="w-8 h-8 rounded-full bg-white/90 text-black flex items-center justify-center shadow-lg transform group-hover:scale-110 transition">
                <Play className="w-3.5 h-3.5 fill-current ml-0.5" />
              </div>
            </div>
          )}

          {/* Bottom Left Tag on Thumbnail */}
          <div className="absolute bottom-1.5 left-1.5 flex items-center gap-1 z-10">
            <span className="px-1.5 py-0.5 rounded-md bg-black/75 backdrop-blur-md text-[9px] font-mono text-zinc-300 border border-white/10">
              {job.keyword}
            </span>
          </div>

          {/* Bottom Right Duration or Clean badge */}
          {job.assets.has_video && (
            <div className="absolute bottom-1.5 right-1.5 z-10">
              <span className="px-1.5 py-0.5 rounded-md bg-black/75 backdrop-blur-md text-[9px] font-mono text-emerald-400 border border-white/10 flex items-center gap-1">
                <span className="w-1 h-1 rounded-full bg-emerald-400"></span> MP4
              </span>
            </div>
          )}
        </div>

        {/* Product Title & Author */}
        <div className="mt-2.5">
          <h3 className="text-xs sm:text-[13px] font-medium text-zinc-200 line-clamp-2 leading-snug group-hover:text-white transition">
            {job.title}
          </h3>

          <div className="flex items-center justify-between gap-1 mt-1 text-[11px] font-mono text-zinc-400">
            <span className="text-zinc-500 truncate">@{job.author.unique_id}</span>
            {job.affiliate_pdp_url && (
              <span className="text-[10px] text-zinc-400 flex items-center gap-0.5 bg-zinc-900 px-1 py-0.2 rounded border border-zinc-800">
                <ShoppingBag className="w-2.5 h-2.5" /> Shop
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Engagement Micro-Strip */}
      <div className="pt-2 border-t border-white/[0.06] mt-2.5">
        <div className="flex items-center justify-between text-center font-mono py-1 px-2 rounded-lg bg-black/40 border border-white/[0.04] text-[10px] text-zinc-400">
          <div className="flex items-center gap-1" title="Lượt xem video">
            <Eye className="w-3 h-3 text-zinc-500" />
            <span className="font-semibold text-zinc-200">{formatNumber(job.stats.plays)}</span>
          </div>
          <div className="flex items-center gap-1" title="Lượt thích">
            <Heart className="w-3 h-3 text-zinc-500" />
            <span className="font-semibold text-zinc-200">{formatNumber(job.stats.likes)}</span>
          </div>
          <div className="flex items-center gap-1" title="Bình luận">
            <MessageCircle className="w-3 h-3 text-zinc-500" />
            <span className="font-semibold text-zinc-200">{formatNumber(job.stats.comments)}</span>
          </div>
          <div className="flex items-center gap-1" title="Chia sẻ">
            <Share2 className="w-3 h-3 text-zinc-500" />
            <span className="font-semibold text-zinc-200">{formatNumber(job.stats.shares)}</span>
          </div>
        </div>

        {/* Card Footer Quick Actions */}
        <div className="flex items-center justify-between gap-1.5 mt-2.5">
          <button
            onClick={handleCopyPrompt}
            className={`flex-1 py-1 px-2 rounded-lg text-[11px] font-mono flex items-center justify-center gap-1.5 transition-all ${
              isCopied
                ? 'bg-white text-black font-semibold shadow-sm'
                : 'bg-zinc-900/90 hover:bg-zinc-800 text-zinc-300 hover:text-white border border-zinc-800'
            }`}
          >
            {isCopied ? (
              <>
                <Check className="w-3 h-3" />
                <span>Đã chép!</span>
              </>
            ) : (
              <>
                <Sparkles className="w-3 h-3 text-zinc-400" />
                <span>Copy Flow</span>
              </>
            )}
          </button>

          <div className="flex items-center gap-1">
            {job.affiliate_pdp_url && (
              <a
                href={job.affiliate_pdp_url}
                target="_blank"
                rel="noreferrer"
                onClick={(e) => e.stopPropagation()}
                title="Mở TikTok Shop"
                className="p-1 rounded-lg bg-zinc-900 hover:bg-zinc-800 text-zinc-400 hover:text-white border border-zinc-800 transition"
              >
                <ExternalLink className="w-3 h-3" />
              </a>
            )}

            <span className="p-1 rounded-lg bg-zinc-900 group-hover:bg-white group-hover:text-black text-zinc-400 transition">
              <ChevronRight className="w-3 h-3" />
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
