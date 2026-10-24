import { create } from 'zustand';
import { JobItem, JobStatus, FilterType, CardViewMode } from '../lib/types';

export interface IngestProgress {
  step: number;
  totalSteps: number;
  stageName: string;
  detail: string;
}

interface JobStore {
  jobs: JobItem[];
  selectedJob: JobItem | null;
  activeFilter: FilterType;
  cardViewMode: CardViewMode;
  searchQuery: string;
  isLoading: boolean;
  copiedKey: string | null;

  // Realtime state
  isRealtimeConnected: boolean;
  lastSyncTime: string | null;

  // Ingestion creation state
  isCreating: boolean;
  createProgress: IngestProgress | null;
  createError: string | null;
  isCreateModalOpen: boolean;

  // Render (Content Remix) state
  isRendering: boolean;
  renderingJobId: string | null;
  renderLogs: string[];
  renderError: string | null;

  // HyperFrames Studio live preview state (xem trực tiếp quá trình dựng/edit trong dashboard)
  hyperframesProjectId: string | null;
  hyperframesStudioUrl: string | null;
  isPreviewLoading: boolean;

  // Brief cho Claude tự vận hành EGO Lite/Flow (dashboard chỉ phân tích + sinh brief, không tự render)
  isGeneratingBrief: boolean;
  briefText: string | null;
  briefError: string | null;

  setJobs: (jobs: JobItem[]) => void;
  setSelectedJob: (job: JobItem | null) => void;
  setActiveFilter: (filter: FilterType) => void;
  setCardViewMode: (mode: CardViewMode) => void;
  setSearchQuery: (query: string) => void;
  setCopiedKey: (key: string | null) => void;
  setIsCreateModalOpen: (open: boolean) => void;
  updateJobStatus: (id: string, status: JobStatus) => Promise<void>;
  fetchJobs: (selectNewestId?: string) => Promise<void>;
  createJob: (url: string) => Promise<{ success: boolean; error?: string }>;
  renderJob: (id: string) => Promise<{ success: boolean; error?: string }>;
  generateBrief: (id: string) => Promise<{ success: boolean; brief?: string; error?: string }>;
  stopHyperframesPreview: () => void;
  initRealtimeSync: () => () => void;
}

export const useJobStore = create<JobStore>((set, get) => ({
  jobs: [],
  selectedJob: null,
  activeFilter: 'ALL',
  cardViewMode: 'grid',
  searchQuery: '',
  isLoading: false,
  copiedKey: null,

  isRealtimeConnected: false,
  lastSyncTime: null,

  isCreating: false,
  createProgress: null,
  createError: null,
  isCreateModalOpen: false,

  isRendering: false,
  renderingJobId: null,
  renderLogs: [],
  renderError: null,

  hyperframesProjectId: null,
  hyperframesStudioUrl: null,
  isPreviewLoading: false,

  isGeneratingBrief: false,
  briefText: null,
  briefError: null,

  setJobs: (jobs) => set({ jobs }),
  setSelectedJob: (job) => {
    if (job === null) {
      get().stopHyperframesPreview();
      set({ selectedJob: null });
      return;
    }
    set({ selectedJob: job });
  },
  setActiveFilter: (activeFilter) => set({ activeFilter }),
  setCardViewMode: (cardViewMode) => set({ cardViewMode }),
  setSearchQuery: (searchQuery) => set({ searchQuery }),
  setCopiedKey: (copiedKey) => set({ copiedKey }),
  setIsCreateModalOpen: (isCreateModalOpen) => set({ isCreateModalOpen }),

  updateJobStatus: async (id: string, status: JobStatus) => {
    const prevJobs = get().jobs;
    const updated = prevJobs.map((j) => (j.id === id ? { ...j, status } : j));
    const currentSelected = get().selectedJob;
    const updatedSelected = currentSelected && currentSelected.id === id ? { ...currentSelected, status } : currentSelected;

    set({ jobs: updated, selectedJob: updatedSelected });

    try {
      await fetch('/api/jobs/status', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id, status }),
      });
    } catch (err) {
      console.error('Failed to persist status update:', err);
    }
  },

  fetchJobs: async (selectNewestId?: string) => {
    try {
      const res = await fetch('/api/jobs');
      const data = await res.json();
      if (data && data.jobs) {
        set({ jobs: data.jobs, lastSyncTime: new Date().toLocaleTimeString('vi-VN') });
        if (selectNewestId) {
          const match = data.jobs.find((j: JobItem) => j.id === selectNewestId || j.product_id === selectNewestId);
          if (match) set({ selectedJob: match });
        }
      }
    } catch (err) {
      console.error('Error fetching jobs:', err);
    }
  },

  createJob: async (url: string) => {
    set({ isCreating: true, createError: null });

    const simulateSteps = [
      { step: 1, totalSteps: 4, stageName: 'Phân tích URL TikTok', detail: 'Đang kiểm tra liên kết video và cấu trúc giỏ hàng...' },
      { step: 2, totalSteps: 4, stageName: 'Tải Video Không Logo', detail: 'Đang nạp video HD sạch watermark qua SnapTik & tách audio...' },
      { step: 3, totalSteps: 4, stageName: 'Trích xuất TikTok Shop PDP', detail: 'Chuẩn hóa danh mục, giá bán và link affiliate an toàn...' },
      { step: 4, totalSteps: 4, stageName: 'Khởi tạo AI Prompts Suite', detail: 'Ghép Master DNA Gô Bi và hoàn thiện hồ sơ Job...' },
    ];

    let currentStep = 0;
    set({ createProgress: simulateSteps[0] });

    const timer = setInterval(() => {
      currentStep++;
      if (currentStep < simulateSteps.length) {
        set({ createProgress: simulateSteps[currentStep] });
      }
    }, 2800);

    try {
      const res = await fetch('/api/jobs/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url }),
      });

      clearInterval(timer);
      const data = await res.json();

      if (!res.ok || !data.success) {
        const errorMsg = data.error || 'Nạp Job thất bại. Vui lòng kiểm tra lại URL.';
        set({ isCreating: false, createError: errorMsg, createProgress: null });
        return { success: false, error: errorMsg };
      }

      set({
        isCreating: false,
        createProgress: null,
        isCreateModalOpen: false,
      });

      const newPid = data.product?.product_id;
      await get().fetchJobs(newPid ? `JOB-${newPid}` : undefined);

      return { success: true };
    } catch (err: any) {
      clearInterval(timer);
      const errorMsg = err.message || 'Lỗi kết nối khi nạp Job';
      set({ isCreating: false, createError: errorMsg, createProgress: null });
      return { success: false, error: errorMsg };
    }
  },

  renderJob: async (id: string) => {
    // Dừng preview Studio của lần render trước (nếu còn) trước khi bắt đầu job mới.
    get().stopHyperframesPreview();

    set({
      isRendering: true,
      renderingJobId: id,
      renderLogs: [],
      renderError: null,
      hyperframesProjectId: null,
      hyperframesStudioUrl: null,
      isPreviewLoading: false,
    });

    let previewPollTimer: ReturnType<typeof setInterval> | null = null;
    let detectedProjectId: string | null = null;

    // Log đầu tiên của ContentRemixWorkflow luôn có dạng
    // "🎬 BẮT ĐẦU GOBI CONTENT REMIX WORKFLOW [remix_<ts>_<hash>]" — đó cũng chính là tên
    // thư mục project dưới output/hyperframes_projects/. Bắt được job_id này là có thể mở
    // Studio preview ngay khi composition (index.html) được ghi ra, trong lúc render vẫn chạy.
    const detectAndPollPreview = (line: string) => {
      if (detectedProjectId) return;
      const match = line.match(/\[(remix_\d+_[a-f0-9]+)\]/);
      if (!match) return;

      detectedProjectId = match[1];
      set({ hyperframesProjectId: detectedProjectId, isPreviewLoading: true });

      const poll = async () => {
        try {
          const res = await fetch('/api/jobs/preview', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ projectId: detectedProjectId }),
          });
          const data = await res.json();
          if (data.ready && data.studioUrl) {
            set({ hyperframesStudioUrl: data.studioUrl, isPreviewLoading: false });
            if (previewPollTimer) {
              clearInterval(previewPollTimer);
              previewPollTimer = null;
            }
          }
        } catch {
          // Bỏ qua, thử lại ở lần poll kế tiếp.
        }
      };

      poll();
      previewPollTimer = setInterval(poll, 1500);
    };

    try {
      const res = await fetch('/api/jobs/render', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id }),
      });

      if (!res.ok || !res.body) {
        const data = await res.json().catch(() => ({}));
        const errorMsg = data.error || `Render thất bại (HTTP ${res.status})`;
        set({ isRendering: false, renderingJobId: null, renderError: errorMsg });
        return { success: false, error: errorMsg };
      }

      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';
      let finalSuccess = false;
      let finalError: string | undefined;

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });

        const events = buffer.split('\n\n');
        buffer = events.pop() || '';

        for (const evt of events) {
          const line = evt.replace(/^data:\s*/, '').trim();
          if (!line) continue;
          try {
            const parsed = JSON.parse(line);
            if (parsed.type === 'LOG') {
              set((state) => ({ renderLogs: [...state.renderLogs, parsed.line] }));
              detectAndPollPreview(parsed.line);
            } else if (parsed.type === 'DONE') {
              finalSuccess = !!parsed.success;
              if (!finalSuccess) finalError = `Tiến trình kết thúc với lỗi (exit code ${parsed.exitCode})`;
            }
          } catch {
            // dòng không phải JSON hợp lệ, bỏ qua
          }
        }
      }

      if (previewPollTimer) {
        clearInterval(previewPollTimer);
        previewPollTimer = null;
      }

      set({ isRendering: false, renderingJobId: null, renderError: finalError || null });

      if (finalSuccess) {
        await get().fetchJobs(id);
      }

      return { success: finalSuccess, error: finalError };
    } catch (err: any) {
      if (previewPollTimer) clearInterval(previewPollTimer);
      const errorMsg = err.message || 'Lỗi kết nối khi render video';
      set({ isRendering: false, renderingJobId: null, renderError: errorMsg });
      return { success: false, error: errorMsg };
    }
  },

  generateBrief: async (id: string) => {
    set({ isGeneratingBrief: true, briefText: null, briefError: null });
    try {
      const res = await fetch('/api/jobs/brief', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id }),
      });
      const data = await res.json().catch(() => ({}));

      if (!res.ok || !data.success) {
        const errorMsg = data.error || `Tạo Brief thất bại (HTTP ${res.status})`;
        set({ isGeneratingBrief: false, briefError: errorMsg });
        return { success: false, error: errorMsg };
      }

      set({ isGeneratingBrief: false, briefText: data.brief });
      return { success: true, brief: data.brief };
    } catch (err: any) {
      const errorMsg = err.message || 'Lỗi kết nối khi tạo Brief';
      set({ isGeneratingBrief: false, briefError: errorMsg });
      return { success: false, error: errorMsg };
    }
  },

  stopHyperframesPreview: () => {
    const projectId = get().hyperframesProjectId;
    set({ hyperframesProjectId: null, hyperframesStudioUrl: null, isPreviewLoading: false });
    if (projectId) {
      fetch(`/api/jobs/preview?projectId=${encodeURIComponent(projectId)}`, { method: 'DELETE' }).catch(() => {});
    }
  },

  initRealtimeSync: () => {
    let eventSource: EventSource | null = null;
    let fallbackInterval: NodeJS.Timeout | null = null;

    const setupSSE = () => {
      try {
        eventSource = new EventSource('/api/jobs/stream');

        eventSource.onopen = () => {
          set({ isRealtimeConnected: true });
        };

        eventSource.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            if (data.jobs && Array.isArray(data.jobs)) {
              const currentSelected = get().selectedJob;
              let newSelected = currentSelected;

              if (currentSelected) {
                const refreshed = data.jobs.find((j: JobItem) => j.id === currentSelected.id);
                if (refreshed) newSelected = refreshed;
              }

              set({
                jobs: data.jobs,
                selectedJob: newSelected,
                isRealtimeConnected: true,
                lastSyncTime: new Date().toLocaleTimeString('vi-VN'),
              });
            }
          } catch (e) {
            console.error('[Realtime SSE] Parse error:', e);
          }
        };

        eventSource.onerror = () => {
          set({ isRealtimeConnected: false });
          if (eventSource) {
            eventSource.close();
            eventSource = null;
          }
          // Retry SSE after 5 seconds
          setTimeout(setupSSE, 5000);
        };
      } catch (err) {
        console.warn('[Realtime SSE] Not supported or failed:', err);
        set({ isRealtimeConnected: false });
      }
    };

    setupSSE();

    // Secondary safety: fallback poll every 8 seconds if disconnected
    fallbackInterval = setInterval(() => {
      if (!get().isRealtimeConnected) {
        get().fetchJobs();
      }
    }, 8000);

    // Return cleanup unsubscribe function
    return () => {
      if (eventSource) eventSource.close();
      if (fallbackInterval) clearInterval(fallbackInterval);
      set({ isRealtimeConnected: false });
    };
  },
}));
