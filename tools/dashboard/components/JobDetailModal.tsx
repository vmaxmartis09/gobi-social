'use client';

import React, { useState } from 'react';
import { useJobStore } from '../store/useJobStore';
import { JobStatus } from '../lib/types';
import {
  X,
  Play,
  Copy,
  Check,
  ExternalLink,
  Eye,
  Heart,
  MessageCircle,
  Share2,
  Sparkles,
  FileText,
  Video,
  Layers,
  CheckCircle2,
  Clock,
  ArrowRight,
  Wand2,
  Loader2,
  AlertTriangle,
} from 'lucide-react';

export default function JobDetailModal() {
  const {
    selectedJob,
    setSelectedJob,
    updateJobStatus,
    renderJob,
    isRendering,
    renderingJobId,
    renderLogs,
    renderError,
    generateBrief,
    isGeneratingBrief,
    briefText,
    briefError,
  } = useJobStore();
  const [activeTab, setActiveTab] = useState<'flow' | 'voice' | 'caption' | 'spec'>('flow');
  const [copiedKey, setCopiedKey] = useState<string | null>(null);
  const [briefCopied, setBriefCopied] = useState(false);

  if (!selectedJob) return null;

  const copyToClipboard = (text: string, key: string) => {
    navigator.clipboard.writeText(text);
    setCopiedKey(key);
    setTimeout(() => setCopiedKey(null), 2000);
  };

  const formatNumber = (num: number) => {
    if (num >= 1_000_000) return (num / 1_000_000).toFixed(1) + 'M';
    if (num >= 1_000) return (num / 1_000).toFixed(1) + 'K';
    return num.toLocaleString();
  };

  const steps: { key: JobStatus; label: string; desc: string }[] = [
    { key: 'CHUA_LAM', label: '1. Nạp Job', desc: 'Đã tải MP4, MP3, link sản phẩm' },
    { key: 'DANG_LAM', label: '2. Đang Xử Lý', desc: 'Sinh prompt, render Flow' },
    { key: 'DA_LAM_VIDEO', label: '3. Đã Làm Video', desc: 'Video MP4 9:16 hoàn thiện' },
    { key: 'DA_DANG', label: '4. Đã Đăng TikTok', desc: 'Gắn giỏ hàng & cắn view' },
  ];

  const getStepIndex = (st: JobStatus) => {
    switch (st) {
      case 'CHUA_LAM': return 0;
      case 'DANG_LAM': return 1;
      case 'DA_LAM_VIDEO': return 2;
      case 'DA_DANG': return 3;
      default: return 0;
    }
  };

  const currentStepIdx = getStepIndex(selectedJob.status);

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-black/80 backdrop-blur-md animate-fade-in overflow-y-auto">
      <div className="bg-[#0e0e11] border border-white/10 rounded-2xl w-full max-w-5xl max-h-[92vh] flex flex-col shadow-2xl overflow-hidden my-auto">
        {/* Modal Header */}
        <div className="px-6 py-4 border-b border-white/[0.08] flex items-center justify-between gap-4 bg-zinc-950/60">
          <div className="flex items-center gap-3 min-w-0">
            <span className="px-2 py-0.5 rounded text-[10px] font-mono tracking-widest bg-zinc-800 text-zinc-300 border border-zinc-700">
              {selectedJob.id}
            </span>
            <h2 className="text-sm sm:text-base font-semibold text-white truncate max-w-xl">
              {selectedJob.title}
            </h2>
            {selectedJob.video_type && (
              <span
                title="Loại video đã tự động phát hiện"
                className="px-2 py-0.5 rounded-full text-[10px] font-mono bg-zinc-800 text-zinc-300 border border-zinc-700 flex items-center gap-1 flex-shrink-0"
              >
                <span>{selectedJob.video_type === 'talking_head' ? '🗣️' : '🛍️'}</span>
                <span>{selectedJob.video_type === 'talking_head' ? 'Nói trực diện' : 'Chỉ sản phẩm'}</span>
              </span>
            )}
          </div>

          <button
            onClick={() => setSelectedJob(null)}
            className="p-1.5 rounded-lg bg-zinc-900 hover:bg-zinc-800 text-zinc-400 hover:text-white transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Process Status Stepper Bar */}
        <div className="px-6 py-3.5 border-b border-white/[0.06] bg-black/40">
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
            {steps.map((step, idx) => {
              const isPast = idx < currentStepIdx;
              const isCurrent = idx === currentStepIdx;
              return (
                <button
                  key={step.key}
                  onClick={() => updateJobStatus(selectedJob.id, step.key)}
                  className={`p-2.5 rounded-xl border text-left transition-all ${
                    isCurrent
                      ? 'bg-white text-black border-white shadow-sm'
                      : isPast
                      ? 'bg-zinc-900/90 text-zinc-300 border-zinc-700'
                      : 'bg-zinc-950/40 text-zinc-500 border-zinc-850 hover:border-zinc-700'
                  }`}
                >
                  <div className="flex items-center justify-between text-[11px] font-mono font-medium">
                    <span>{step.label}</span>
                    {isPast && <CheckCircle2 className="w-3.5 h-3.5 text-zinc-400" />}
                    {isCurrent && <span className="w-2 h-2 rounded-full bg-black animate-pulse"></span>}
                  </div>
                  <div className={`text-[10px] truncate mt-0.5 ${isCurrent ? 'text-zinc-700' : 'text-zinc-500'}`}>
                    {step.desc}
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Modal Body: 2 Columns */}
        <div className="flex-1 overflow-y-auto p-6 grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Left Column: Media & Engagement (5 cols) */}
          <div className="lg:col-span-5 flex flex-col gap-4">
            {/* Video Player */}
            <div className="rounded-xl overflow-hidden bg-black border border-zinc-800 relative aspect-[9/16] max-h-[460px] mx-auto w-full flex items-center justify-center">
              {selectedJob.assets.video_url ? (
                <video
                  src={selectedJob.assets.video_url}
                  controls
                  playsInline
                  className="w-full h-full object-contain"
                />
              ) : selectedJob.assets.cover_url ? (
                <img
                  src={selectedJob.assets.cover_url}
                  alt={selectedJob.title}
                  className="w-full h-full object-cover"
                />
              ) : (
                <div className="text-zinc-600 flex flex-col items-center gap-2">
                  <Play className="w-8 h-8" />
                  <span className="text-xs font-mono">Chưa có preview video</span>
                </div>
              )}
            </div>

            {/* Engagement Metrics Box */}
            <div className="kokonut-card rounded-xl p-4">
              <span className="text-[11px] font-mono tracking-wider text-zinc-500 uppercase block mb-2">
                Chỉ Số Tương Tác Video Gốc
              </span>
              <div className="grid grid-cols-4 gap-2 text-center font-mono">
                <div className="p-2 rounded-lg bg-black/40 border border-white/[0.04]">
                  <div className="text-[10px] text-zinc-500 flex items-center justify-center gap-1">
                    <Eye className="w-3 h-3" /> Views
                  </div>
                  <div className="text-sm font-bold text-white mt-0.5">
                    {formatNumber(selectedJob.stats.plays)}
                  </div>
                </div>
                <div className="p-2 rounded-lg bg-black/40 border border-white/[0.04]">
                  <div className="text-[10px] text-zinc-500 flex items-center justify-center gap-1">
                    <Heart className="w-3 h-3" /> Likes
                  </div>
                  <div className="text-sm font-bold text-white mt-0.5">
                    {formatNumber(selectedJob.stats.likes)}
                  </div>
                </div>
                <div className="p-2 rounded-lg bg-black/40 border border-white/[0.04]">
                  <div className="text-[10px] text-zinc-500 flex items-center justify-center gap-1">
                    <MessageCircle className="w-3 h-3" /> Cmt
                  </div>
                  <div className="text-sm font-bold text-white mt-0.5">
                    {formatNumber(selectedJob.stats.comments)}
                  </div>
                </div>
                <div className="p-2 rounded-lg bg-black/40 border border-white/[0.04]">
                  <div className="text-[10px] text-zinc-500 flex items-center justify-center gap-1">
                    <Share2 className="w-3 h-3" /> Share
                  </div>
                  <div className="text-sm font-bold text-white mt-0.5">
                    {formatNumber(selectedJob.stats.shares)}
                  </div>
                </div>
              </div>

              {/* Product PDP Link */}
              <div className="mt-3 pt-3 border-t border-white/[0.06] flex items-center justify-between text-xs">
                <span className="text-zinc-400 font-mono">TikTok Shop PDP:</span>
                <a
                  href={selectedJob.affiliate_pdp_url || selectedJob.pdp_url}
                  target="_blank"
                  rel="noreferrer"
                  className="px-2.5 py-1 rounded bg-zinc-800 hover:bg-zinc-700 text-white font-mono flex items-center gap-1 transition"
                >
                  <span>Mở Giỏ Hàng</span>
                  <ExternalLink className="w-3 h-3" />
                </a>
              </div>
            </div>

            {/* Content Remix Render Box (gobi remix — không swap mặt) */}
            <div className="kokonut-card rounded-xl p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-[11px] font-mono tracking-wider text-zinc-500 uppercase">
                  Render Video Gô Bi (Content Remix)
                </span>
                <button
                  onClick={() => renderJob(selectedJob.id)}
                  disabled={isRendering || !selectedJob.assets.has_video}
                  title={!selectedJob.assets.has_video ? 'Job chưa có video nguồn (video_clean.mp4)' : undefined}
                  className="px-3 py-1.5 rounded-lg bg-white text-black text-xs font-mono font-semibold flex items-center gap-1.5 transition disabled:opacity-40 disabled:cursor-not-allowed hover:bg-zinc-200"
                >
                  {isRendering && renderingJobId === selectedJob.id ? (
                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                  ) : (
                    <Wand2 className="w-3.5 h-3.5" />
                  )}
                  <span>{isRendering && renderingJobId === selectedJob.id ? 'Đang render...' : 'Render với Gô Bi'}</span>
                </button>
              </div>

              {renderingJobId === selectedJob.id && (isRendering || renderLogs.length > 0) && (
                <div className="mt-2 bg-black rounded-lg border border-zinc-800 p-2.5 h-40 overflow-y-auto font-mono text-[11px] text-zinc-400 leading-relaxed">
                  {renderLogs.length === 0 && <span className="text-zinc-600">Đang khởi động quy trình...</span>}
                  {renderLogs.map((line, i) => (
                    <div key={i} className="whitespace-pre-wrap break-all">{line}</div>
                  ))}
                </div>
              )}

              {renderError && !isRendering && (
                <div className="mt-2 flex items-start gap-2 bg-red-950/40 border border-red-900/60 rounded-lg p-2.5 text-xs text-red-300">
                  <AlertTriangle className="w-3.5 h-3.5 mt-0.5 shrink-0" />
                  <span>{renderError}</span>
                </div>
              )}

              {selectedJob.generated_video_path && !isRendering && (
                <div className="mt-2">
                  <div className="text-[10px] text-zinc-500 font-mono mb-1.5">Video Gô Bi đã render:</div>
                  <video
                    src={selectedJob.generated_video_path}
                    controls
                    playsInline
                    className="w-full rounded-lg border border-zinc-800 aspect-[9/16] max-h-[380px] bg-black mx-auto"
                  />
                </div>
              )}
            </div>

            {/* Brief cho Claude tự vận hành EGO Lite/Google Flow (video AI thật, không phải Ken Burns) */}
            <div className="kokonut-card rounded-xl p-4">
              <div className="flex items-center justify-between mb-2">
                <span className="text-[11px] font-mono tracking-wider text-zinc-500 uppercase">
                  Brief cho Gô Bi (Google Flow)
                </span>
                <button
                  onClick={() => generateBrief(selectedJob.id)}
                  disabled={isGeneratingBrief || !selectedJob.assets.has_video}
                  title={!selectedJob.assets.has_video ? 'Job chưa có video nguồn (video_clean.mp4)' : 'Sinh Brief rồi copy dán vào chat với Claude'}
                  className="px-3 py-1.5 rounded-lg bg-white text-black text-xs font-mono font-semibold flex items-center gap-1.5 transition disabled:opacity-40 disabled:cursor-not-allowed hover:bg-zinc-200"
                >
                  {isGeneratingBrief ? (
                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                  ) : (
                    <Sparkles className="w-3.5 h-3.5" />
                  )}
                  <span>{isGeneratingBrief ? 'Đang phân tích...' : 'Tạo Brief cho Gô Bi'}</span>
                </button>
              </div>

              <p className="text-[10px] text-zinc-500 mb-2 leading-relaxed">
                Phân tích video + sản phẩm thật, viết kịch bản (Gemini) — copy Brief rồi dán vào chat với Claude để
                tạo video AI thật qua Google Flow + ráp HyperFrames (không chạy trong dashboard).
              </p>

              {briefError && !isGeneratingBrief && (
                <div className="flex items-start gap-2 bg-red-950/40 border border-red-900/60 rounded-lg p-2.5 text-xs text-red-300 mb-2">
                  <AlertTriangle className="w-3.5 h-3.5 mt-0.5 shrink-0" />
                  <span>{briefError}</span>
                </div>
              )}

              {briefText && !isGeneratingBrief && (
                <div>
                  <div className="bg-black rounded-lg border border-zinc-800 p-3 max-h-64 overflow-y-auto font-mono text-[11px] text-zinc-300 whitespace-pre-wrap leading-relaxed mb-2">
                    {briefText}
                  </div>
                  <button
                    onClick={() => {
                      navigator.clipboard.writeText(briefText);
                      setBriefCopied(true);
                      setTimeout(() => setBriefCopied(false), 2000);
                    }}
                    className={`px-3 py-1.5 rounded-lg text-xs font-mono flex items-center gap-1.5 transition-all w-full justify-center ${
                      briefCopied
                        ? 'bg-emerald-500 text-black font-bold'
                        : 'bg-zinc-800 hover:bg-zinc-700 text-white border border-zinc-700'
                    }`}
                  >
                    {briefCopied ? <Check className="w-3.5 h-3.5" /> : <Copy className="w-3.5 h-3.5" />}
                    <span>{briefCopied ? 'Đã copy!' : 'Copy Brief'}</span>
                  </button>
                </div>
              )}
            </div>
          </div>

          {/* Right Column: AI Prompt Suite (7 cols) */}
          <div className="lg:col-span-7 flex flex-col gap-4">
            {/* Prompt Tabs Header */}
            <div className="flex items-center gap-1.5 p-1 rounded-xl bg-zinc-950 border border-zinc-800 font-mono text-xs">
              <button
                onClick={() => setActiveTab('flow')}
                className={`flex-1 py-1.5 px-2 rounded-lg flex items-center justify-center gap-1.5 transition ${
                  activeTab === 'flow' ? 'bg-white text-black font-semibold' : 'text-zinc-400 hover:text-white'
                }`}
              >
                <Sparkles className="w-3.5 h-3.5" />
                <span>Google Flow / Veo</span>
              </button>

              <button
                onClick={() => setActiveTab('voice')}
                className={`flex-1 py-1.5 px-2 rounded-lg flex items-center justify-center gap-1.5 transition ${
                  activeTab === 'voice' ? 'bg-white text-black font-semibold' : 'text-zinc-400 hover:text-white'
                }`}
              >
                <FileText className="w-3.5 h-3.5" />
                <span>Kịch Bản LyLy</span>
              </button>

              <button
                onClick={() => setActiveTab('caption')}
                className={`flex-1 py-1.5 px-2 rounded-lg flex items-center justify-center gap-1.5 transition ${
                  activeTab === 'caption' ? 'bg-white text-black font-semibold' : 'text-zinc-400 hover:text-white'
                }`}
              >
                <Layers className="w-3.5 h-3.5" />
                <span>TikTok Caption</span>
              </button>

              <button
                onClick={() => setActiveTab('spec')}
                className={`flex-1 py-1.5 px-2 rounded-lg flex items-center justify-center gap-1.5 transition ${
                  activeTab === 'spec' ? 'bg-white text-black font-semibold' : 'text-zinc-400 hover:text-white'
                }`}
              >
                <Video className="w-3.5 h-3.5" />
                <span>HyperFrames Spec</span>
              </button>
            </div>

            {/* Prompt Content Card */}
            <div className="kokonut-card rounded-xl p-5 flex-1 flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-white"></span>
                    <span className="text-xs font-mono font-medium text-white uppercase tracking-wider">
                      {activeTab === 'flow' && 'Google Flow Camera & DNA Motion Prompt'}
                      {activeTab === 'voice' && 'Kịch Bản Review KOC Thuần Việt (OmniVoice)'}
                      {activeTab === 'caption' && 'TikTok Caption & Hashtags Triệu View'}
                      {activeTab === 'spec' && 'HyperFrames Deterministic Composition (HTML5)'}
                    </span>
                  </div>

                  {/* 1-Click Copy Button */}
                  <button
                    onClick={() => {
                      let textToCopy = '';
                      if (activeTab === 'flow') textToCopy = selectedJob.prompts.google_flow_prompt;
                      if (activeTab === 'voice') textToCopy = selectedJob.prompts.voiceover_script;
                      if (activeTab === 'caption') textToCopy = selectedJob.prompts.tiktok_caption;
                      if (activeTab === 'spec') textToCopy = selectedJob.prompts.hyperframes_spec;
                      copyToClipboard(textToCopy, activeTab);
                    }}
                    className={`px-3 py-1.5 rounded-lg text-xs font-mono flex items-center gap-1.5 transition-all ${
                      copiedKey === activeTab
                        ? 'bg-emerald-500 text-black font-bold'
                        : 'bg-white hover:bg-zinc-200 text-black font-semibold shadow-sm'
                    }`}
                  >
                    {copiedKey === activeTab ? (
                      <>
                        <Check className="w-3.5 h-3.5" />
                        <span>Đã copy!</span>
                      </>
                    ) : (
                      <>
                        <Copy className="w-3.5 h-3.5" />
                        <span>Copy Prompt</span>
                      </>
                    )}
                  </button>

                  {activeTab === 'flow' && (
                    <a
                      href="https://labs.google/flow"
                      target="_blank"
                      rel="noreferrer"
                      title="Copy prompt ở trên rồi dán tay vào Flow — không tự động hoá để tránh rủi ro tài khoản Google"
                      className="px-3 py-1.5 rounded-lg text-xs font-mono flex items-center gap-1.5 transition-all bg-zinc-800 hover:bg-zinc-700 text-white border border-zinc-700"
                    >
                      <ExternalLink className="w-3.5 h-3.5" />
                      <span>Mở Flow.google.com</span>
                    </a>
                  )}
                </div>

                {/* Prompt Text Display Box */}
                <div className="p-4 rounded-xl bg-black/60 border border-white/[0.06] font-mono text-xs text-zinc-300 leading-relaxed max-h-[300px] overflow-y-auto whitespace-pre-wrap select-all">
                  {activeTab === 'flow' && selectedJob.prompts.google_flow_prompt}
                  {activeTab === 'voice' && selectedJob.prompts.voiceover_script}
                  {activeTab === 'caption' && selectedJob.prompts.tiktok_caption}
                  {activeTab === 'spec' && selectedJob.prompts.hyperframes_spec}
                </div>
              </div>

              {/* Prompt Usage Guidance */}
              <div className="mt-4 pt-3 border-t border-white/[0.06] text-[11px] text-zinc-500 font-mono flex items-center justify-between">
                <span>
                  {activeTab === 'flow' && '💡 Dán vào ProseMirror trên Google Flow (Ego Lite) để sinh video 8s.'}
                  {activeTab === 'voice' && '💡 Nạp vào Gobi Voice Studio (scripts/voice/voice_studio.py) để sinh file voiceover.'}
                  {activeTab === 'caption' && '💡 Dán trực tiếp vào caption khi đăng video lên TikTok Shop.'}
                  {activeTab === 'spec' && '💡 Dựng video tất định chuẩn TikTok Safe Zone 9:16 bằng HyperFrames.'}
                </span>
              </div>
            </div>

            {/* Quick Status Setter Bar */}
            <div className="p-3.5 rounded-xl bg-zinc-950 border border-zinc-800 flex items-center justify-between gap-3">
              <span className="text-xs font-mono text-zinc-400">Trạng thái hiện tại:</span>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => updateJobStatus(selectedJob.id, 'CHUA_LAM')}
                  className={`px-2.5 py-1 rounded-md text-xs font-mono transition ${
                    selectedJob.status === 'CHUA_LAM'
                      ? 'bg-zinc-800 text-white font-medium border border-zinc-700'
                      : 'text-zinc-500 hover:text-zinc-300'
                  }`}
                >
                  Chưa làm
                </button>
                <button
                  onClick={() => updateJobStatus(selectedJob.id, 'DANG_LAM')}
                  className={`px-2.5 py-1 rounded-md text-xs font-mono transition ${
                    selectedJob.status === 'DANG_LAM'
                      ? 'bg-amber-400/20 text-amber-300 font-medium border border-amber-400/30'
                      : 'text-zinc-500 hover:text-zinc-300'
                  }`}
                >
                  Đang làm
                </button>
                <button
                  onClick={() => updateJobStatus(selectedJob.id, 'DA_LAM_VIDEO')}
                  className={`px-3 py-1 rounded-md text-xs font-mono transition ${
                    selectedJob.status === 'DA_LAM_VIDEO'
                      ? 'bg-white text-black font-semibold'
                      : 'text-zinc-400 hover:text-white bg-zinc-900 border border-zinc-800'
                  }`}
                >
                  Đã làm video ✅
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
