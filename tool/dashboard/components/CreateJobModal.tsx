'use client';

import React, { useState } from 'react';
import { useJobStore } from '../store/useJobStore';
import {
  X,
  Link as LinkIcon,
  Sparkles,
  ArrowRight,
  Clipboard,
  CheckCircle2,
  AlertCircle,
  Loader2,
  Video,
  Layers,
} from 'lucide-react';

export default function CreateJobModal() {
  const {
    isCreateModalOpen,
    setIsCreateModalOpen,
    createJob,
    isCreating,
    createProgress,
    createError,
  } = useJobStore();

  const [inputUrl, setInputUrl] = useState('');

  if (!isCreateModalOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputUrl.trim() || isCreating) return;
    await createJob(inputUrl.trim());
  };

  const handlePaste = async () => {
    try {
      const text = await navigator.clipboard.readText();
      if (text) setInputUrl(text.trim());
    } catch (err) {
      console.warn('Clipboard read failed:', err);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6 bg-black/85 backdrop-blur-md animate-fade-in">
      <div className="bg-[#0e0e12] border border-white/10 rounded-2xl w-full max-w-xl shadow-2xl overflow-hidden relative">
        {/* Subtle Ambient Radial Glow */}
        <div className="absolute -top-24 -left-24 w-60 h-60 bg-white/5 rounded-full blur-3xl pointer-events-none" />

        {/* Modal Header */}
        <div className="px-6 py-5 border-b border-white/[0.08] flex items-center justify-between bg-zinc-950/40">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-white text-black flex items-center justify-center font-bold shadow-md">
              <LinkIcon className="w-4 h-4" />
            </div>
            <div>
              <h2 className="text-sm font-semibold text-white tracking-wide uppercase font-mono">
                Nạp Job Video Mới
              </h2>
              <p className="text-xs text-zinc-400 font-mono mt-0.5">
                Tự động cào video sạch logo, MP3, sản phẩm & sinh Prompt
              </p>
            </div>
          </div>

          <button
            onClick={() => !isCreating && setIsCreateModalOpen(false)}
            disabled={isCreating}
            className="p-1.5 rounded-lg bg-zinc-900 hover:bg-zinc-800 text-zinc-400 hover:text-white transition disabled:opacity-40"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Content */}
        <div className="p-6">
          {!isCreating ? (
            <form onSubmit={handleSubmit} className="space-y-5">
              <div>
                <label className="block text-xs font-mono text-zinc-300 uppercase tracking-wider mb-2">
                  Link Video TikTok / TikTok Shop
                </label>
                <div className="relative flex items-center">
                  <div className="absolute left-3.5 text-zinc-500">
                    <Video className="w-4 h-4" />
                  </div>
                  <input
                    type="url"
                    placeholder="https://www.tiktok.com/@user/video/..."
                    value={inputUrl}
                    onChange={(e) => setInputUrl(e.target.value)}
                    required
                    className="w-full bg-zinc-900/90 border border-zinc-700/80 rounded-xl pl-10 pr-24 py-3 text-xs sm:text-sm text-zinc-100 placeholder:text-zinc-600 focus:outline-none focus:border-white transition font-mono"
                  />
                  <button
                    type="button"
                    onClick={handlePaste}
                    className="absolute right-2 px-2.5 py-1 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 hover:text-white text-xs font-mono flex items-center gap-1 transition"
                  >
                    <Clipboard className="w-3 h-3" />
                    <span>Dán</span>
                  </button>
                </div>
                <p className="text-[11px] text-zinc-500 mt-2 font-mono">
                  Hỗ trợ cả link video có giỏ hàng (Shop PDP) và video review thời trang thông thường.
                </p>
              </div>

              {/* Error Alert */}
              {createError && (
                <div className="p-3.5 rounded-xl bg-red-950/40 border border-red-500/30 text-red-300 text-xs font-mono flex items-start gap-2.5">
                  <AlertCircle className="w-4 h-4 flex-shrink-0 mt-0.5 text-red-400" />
                  <div className="leading-relaxed">{createError}</div>
                </div>
              )}

              {/* Action Buttons */}
              <div className="flex items-center justify-end gap-3 pt-3 border-t border-white/[0.06]">
                <button
                  type="button"
                  onClick={() => setIsCreateModalOpen(false)}
                  className="px-4 py-2 rounded-xl text-xs font-mono text-zinc-400 hover:text-white hover:bg-zinc-900 transition"
                >
                  Hủy
                </button>
                <button
                  type="submit"
                  disabled={!inputUrl.trim()}
                  className="px-5 py-2.5 rounded-xl bg-white hover:bg-zinc-200 text-black font-semibold text-xs font-mono flex items-center gap-2 shadow-sm transition disabled:opacity-50"
                >
                  <Sparkles className="w-3.5 h-3.5" />
                  <span>Bắt Đầu Xử Lý Job</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>
            </form>
          ) : (
            /* Live Process Stepper View */
            <div className="py-4 space-y-6">
              <div className="text-center">
                <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-white text-black mb-3 shadow-lg animate-pulse">
                  <Loader2 className="w-6 h-6 animate-spin" />
                </div>
                <h3 className="text-sm font-semibold text-white tracking-wide">
                  Đang Xử Lý & Chuẩn Hóa Job...
                </h3>
                <p className="text-xs text-zinc-400 font-mono mt-1">
                  Hệ thống đang trích xuất media và nạp vào thư mục dữ liệu
                </p>
              </div>

              {/* Progress Bar */}
              {createProgress && (
                <div className="space-y-3">
                  <div className="flex items-center justify-between text-xs font-mono">
                    <span className="text-white font-medium flex items-center gap-1.5">
                      <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
                      {createProgress.stageName}
                    </span>
                    <span className="text-zinc-500">
                      Bước {createProgress.step} / {createProgress.totalSteps}
                    </span>
                  </div>

                  <div className="w-full h-1.5 rounded-full bg-zinc-900 overflow-hidden border border-white/[0.04]">
                    <div
                      className="h-full bg-white transition-all duration-500 ease-out"
                      style={{
                        width: `${(createProgress.step / createProgress.totalSteps) * 100}%`,
                      }}
                    />
                  </div>

                  <p className="text-[11px] text-zinc-500 font-mono text-center">
                    {createProgress.detail}
                  </p>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
