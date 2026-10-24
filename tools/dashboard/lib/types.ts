export type JobStatus = 'CHUA_LAM' | 'DANG_LAM' | 'DA_LAM_VIDEO' | 'DA_DANG';

export type FilterType =
  | 'ALL'
  | JobStatus
  | 'HAS_VIDEO'
  | 'HAS_SHOP'
  | 'VIRAL'
  | 'TOP_LIKES';

export type CardViewMode = 'grid' | 'compact';

export interface JobStats {
  plays: number;
  likes: number;
  comments: number;
  shares: number;
  engagement_rate?: string;
}

export interface JobPrompts {
  google_flow_prompt: string;
  voiceover_script: string;
  tiktok_caption: string;
  hyperframes_spec: string;
}

export interface JobItem {
  id: string;
  product_id: string;
  title: string;
  keyword: string;
  pdp_url: string;
  affiliate_pdp_url: string;
  cover_url: string;
  price: number;
  categories: string[];
  author: {
    unique_id: string;
    nickname: string;
    avatar?: string;
  };
  source_video: {
    video_id: string;
    url: string;
    desc: string;
    duration?: number;
  };
  stats: JobStats;
  assets: {
    video_url?: string;
    cover_url?: string;
    has_video: boolean;
    has_cover: boolean;
    folder: string;
  };
  status: JobStatus;
  generated_video_path?: string;
  video_type?: 'talking_head' | 'product_only';
  ingested_at: string;
  prompts: JobPrompts;
}

export interface JobFilterState {
  status: FilterType;
  searchQuery: string;
  sortBy: 'ingested_at' | 'plays' | 'likes';
}
