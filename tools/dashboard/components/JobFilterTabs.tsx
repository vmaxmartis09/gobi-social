'use client';

import React, { useRef, useState, useEffect } from 'react';
import { useJobStore } from '../store/useJobStore';
import { FilterType } from '../lib/types';
import {
  Layers,
  Clock,
  Flame,
  Clapperboard,
  Share2,
  Film,
  ShoppingBag,
  TrendingUp,
  Heart,
  ChevronLeft,
  ChevronRight,
  LayoutGrid,
  List,
} from 'lucide-react';

export default function JobFilterTabs() {
  const { activeFilter, setActiveFilter, jobs, cardViewMode, setCardViewMode } = useJobStore();
  const scrollRef = useRef<HTMLDivElement>(null);
  const [canScrollLeft, setCanScrollLeft] = useState(false);
  const [canScrollRight, setCanScrollRight] = useState(false);

  // Check scroll position to toggle arrow buttons visual state
  const checkScroll = () => {
    if (!scrollRef.current) return;
    const { scrollLeft, scrollWidth, clientWidth } = scrollRef.current;
    setCanScrollLeft(scrollLeft > 4);
    setCanScrollRight(scrollLeft < scrollWidth - clientWidth - 4);
  };

  useEffect(() => {
    checkScroll();
    window.addEventListener('resize', checkScroll);
    return () => window.removeEventListener('resize', checkScroll);
  }, [jobs]);

  const scroll = (direction: 'left' | 'right') => {
    if (!scrollRef.current) return;
    const offset = direction === 'left' ? -220 : 220;
    scrollRef.current.scrollBy({ left: offset, behavior: 'smooth' });
    setTimeout(checkScroll, 300);
  };

  const getCount = (filter: FilterType) => {
    if (filter === 'ALL') return jobs.length;
    if (filter === 'HAS_VIDEO') return jobs.filter((j) => j.assets?.has_video).length;
    if (filter === 'HAS_SHOP') return jobs.filter((j) => Boolean(j.affiliate_pdp_url)).length;
    if (filter === 'VIRAL') return jobs.filter((j) => (j.stats?.plays || 0) >= 100000).length;
    if (filter === 'TOP_LIKES') return jobs.filter((j) => (j.stats?.likes || 0) >= 5000).length;
    return jobs.filter((j) => j.status === filter).length;
  };

  const filterTabs: { key: FilterType; label: string; icon: React.ReactNode; tooltip: string }[] = [
    {
      key: 'ALL',
      label: 'Tất cả',
      icon: <Layers className="w-3.5 h-3.5" />,
      tooltip: 'Tất cả Jobs',
    },
    {
      key: 'CHUA_LAM',
      label: 'Chưa làm',
      icon: <Clock className="w-3.5 h-3.5" />,
      tooltip: 'Chưa làm video',
    },
    {
      key: 'DANG_LAM',
      label: 'Đang làm',
      icon: <Flame className="w-3.5 h-3.5 text-amber-400" />,
      tooltip: 'Đang làm video',
    },
    {
      key: 'DA_LAM_VIDEO',
      label: 'Đã làm',
      icon: <Clapperboard className="w-3.5 h-3.5" />,
      tooltip: 'Đã hoàn thành video',
    },
    {
      key: 'DA_DANG',
      label: 'Đã đăng',
      icon: <Share2 className="w-3.5 h-3.5 text-emerald-400" />,
      tooltip: 'Đã đăng TikTok Shop',
    },
    {
      key: 'HAS_VIDEO',
      label: 'Có Video sạch',
      icon: <Film className="w-3.5 h-3.5" />,
      tooltip: 'Đã tải MP4 không logo',
    },
    {
      key: 'HAS_SHOP',
      label: 'TikTok Shop',
      icon: <ShoppingBag className="w-3.5 h-3.5" />,
      tooltip: 'Có link sản phẩm Affiliate',
    },
    {
      key: 'VIRAL',
      label: 'Viral >100K',
      icon: <TrendingUp className="w-3.5 h-3.5 text-rose-400" />,
      tooltip: 'Video gốc trên 100,000 views',
    },
    {
      key: 'TOP_LIKES',
      label: 'Nhiều Likes',
      icon: <Heart className="w-3.5 h-3.5 text-pink-400" />,
      tooltip: 'Nhiều lượt yêu thích',
    },
  ];

  return (
    <div className="flex items-center justify-between gap-2 mb-6">
      {/* Scrollable Filter Bar with Icon Pills */}
      <div className="flex-1 min-w-0 flex items-center gap-1.5 p-1 rounded-2xl bg-zinc-900/60 border border-white/[0.06] backdrop-blur-md relative">
        {/* Left Scroll Button */}
        <button
          onClick={() => scroll('left')}
          disabled={!canScrollLeft}
          title="Cuộn bộ lọc sang trái"
          className={`w-7 h-7 rounded-xl flex items-center justify-center transition flex-shrink-0 ${
            canScrollLeft
              ? 'bg-zinc-800 text-zinc-200 hover:bg-zinc-700 hover:text-white border border-zinc-700'
              : 'opacity-25 text-zinc-600 cursor-not-allowed'
          }`}
        >
          <ChevronLeft className="w-4 h-4" />
        </button>

        {/* Scroll Container */}
        <div
          ref={scrollRef}
          onScroll={checkScroll}
          className="flex-1 overflow-x-auto scrollbar-none flex items-center gap-1.5 scroll-smooth py-0.5 px-0.5"
        >
          {filterTabs.map((tab) => {
            const isActive = activeFilter === tab.key;
            const count = getCount(tab.key);

            return (
              <button
                key={tab.key}
                onClick={() => setActiveFilter(tab.key)}
                title={tab.tooltip}
                className={`px-3 py-1.5 rounded-xl text-xs font-mono tracking-tight transition-all flex items-center gap-2 whitespace-nowrap flex-shrink-0 group ${
                  isActive
                    ? 'bg-white text-black font-semibold shadow-sm'
                    : 'bg-zinc-900/90 text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800 border border-zinc-800/80'
                }`}
              >
                <span className={`transition-transform duration-200 ${isActive ? 'scale-110' : 'group-hover:scale-110'}`}>
                  {tab.icon}
                </span>
                <span>{tab.label}</span>
                <span
                  className={`text-[10px] px-1.5 py-0.2 rounded-full font-mono transition ${
                    isActive
                      ? 'bg-black/10 text-black font-bold'
                      : 'bg-zinc-800/90 text-zinc-400 group-hover:text-zinc-300'
                  }`}
                >
                  {count}
                </span>
              </button>
            );
          })}
        </div>

        {/* Right Scroll Button */}
        <button
          onClick={() => scroll('right')}
          disabled={!canScrollRight}
          title="Cuộn bộ lọc sang phải"
          className={`w-7 h-7 rounded-xl flex items-center justify-center transition flex-shrink-0 ${
            canScrollRight
              ? 'bg-zinc-800 text-zinc-200 hover:bg-zinc-700 hover:text-white border border-zinc-700'
              : 'opacity-25 text-zinc-600 cursor-not-allowed'
          }`}
        >
          <ChevronRight className="w-4 h-4" />
        </button>
      </div>

      {/* View Mode Switcher: Grid vs Compact List */}
      <div className="flex items-center gap-1 p-1 rounded-2xl bg-zinc-900/60 border border-white/[0.06] backdrop-blur-md flex-shrink-0">
        <button
          onClick={() => setCardViewMode('grid')}
          title="Chế độ Thẻ nhỏ tinh tế"
          className={`p-1.5 rounded-xl transition ${
            cardViewMode === 'grid'
              ? 'bg-white text-black font-semibold shadow-sm'
              : 'text-zinc-400 hover:text-white hover:bg-zinc-800/60'
          }`}
        >
          <LayoutGrid className="w-4 h-4" />
        </button>
        <button
          onClick={() => setCardViewMode('compact')}
          title="Chế độ Danh sách siêu gọn"
          className={`p-1.5 rounded-xl transition ${
            cardViewMode === 'compact'
              ? 'bg-white text-black font-semibold shadow-sm'
              : 'text-zinc-400 hover:text-white hover:bg-zinc-800/60'
          }`}
        >
          <List className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}
