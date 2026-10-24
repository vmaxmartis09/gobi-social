import fs from 'fs';
import path from 'path';
import { JobItem, JobStatus } from './types';

const PROJECT_ROOT = '/Volumes/Data/gobi-social';
const PRODUCTS_DIR = path.join(PROJECT_ROOT, 'data/products');

export function generatePromptsForProduct(title: string, author: string, stats: any) {
  const shortTitle = title.length > 50 ? title.substring(0, 50) + '...' : title;

  const flowPrompt = `Gobi, nữ KOC thời trang Việt Nam 22 tuổi, gương mặt thanh tú, da trắng sứ mịn màng, tóc đen tuyền suôn mượt buông xõa vai. Mặc ${shortTitle}, mỉm cười rạng rỡ với camera, nhẹ nhàng sải bước catwalk tự tin, tay chạm nhẹ khoe form dáng và chất liệu vải cao cấp. Ánh sáng studio lookbook Quiet Luxury ấm áp, góc máy chân dung 50mm xóa phông mượt mà, chuyển động tự nhiên 24fps, khung hình dọc 9:16 chuẩn TikTok.`;

  const voiceScript = `Mấy bà ơi, set này tui săn được từ kênh @${author} đang viral rần rần nè! Điểm 10 cho chất vải siêu mềm mịn, co giãn êm ái mà mặc lên tôn dáng dã man. Giá hạt dẻ bất ngờ luôn, tui để link chuẩn chính hãng ở giỏ hàng góc trái bên dưới rồi nhé, tranh thủ chốt kẻo hết size!`;

  const tiktokCaption = `Áo/set đồ xinh đỉnh chóp mấy bà ơi ✨ Form tôn dáng, chất vải sờ mê liền! Mua ngay tại giỏ hàng góc trái nha 👇 #thoitrangnu #reviewthoitrang #gobi #koc #tiktokshopvn #outfitlookbook #affiliate`;

  const hyperframesSpec = `<!-- HyperFrames Composition 9:16 (1080x1920) -->
<hf-composition width="1080" height="1920" fps="30">
  <div class="clip top-badge" data-track="2" style="top:220px;">${shortTitle}</div>
  <video class="clip main-footage" src="video_clean.mp4" data-track="1" />
  <div class="clip subtitle-pill" data-track="3" style="top:1380px;">[Kinetic Karaoke Subtitles]</div>
  <audio class="clip voice" src="voiceover_lyly.mp3" data-track="4" volume="1.0" />
  <audio class="clip bgm" src="bgm.mp3" data-track="5" volume="0.16" />
</hf-composition>`;

  return {
    google_flow_prompt: flowPrompt,
    voiceover_script: voiceScript,
    tiktok_caption: tiktokCaption,
    hyperframes_spec: hyperframesSpec,
  };
}

export function getAllJobs(): JobItem[] {
  const jobs: JobItem[] = [];

  if (!fs.existsSync(PRODUCTS_DIR)) {
    return [];
  }

  const entries = fs.readdirSync(PRODUCTS_DIR, { withFileTypes: true });

  for (const entry of entries) {
    if (!entry.isDirectory()) continue;
    const folderPath = path.join(PRODUCTS_DIR, entry.name);
    const productJsonPath = path.join(folderPath, 'product.json');
    const videoCleanJsonPath = path.join(folderPath, 'video_clean.json');
    const videoMp4Path = path.join(folderPath, 'video_clean.mp4');
    const coverJpgPath = path.join(folderPath, 'cover.jpg');
    const generatedVideoPath = path.join(folderPath, 'generated_video.mp4');

    let prodData: any = {};
    let videoData: any = {};

    if (fs.existsSync(productJsonPath)) {
      try {
        prodData = JSON.parse(fs.readFileSync(productJsonPath, 'utf-8'));
      } catch (e) {}
    }

    if (fs.existsSync(videoCleanJsonPath)) {
      try {
        videoData = JSON.parse(fs.readFileSync(videoCleanJsonPath, 'utf-8'));
      } catch (e) {}
    }

    const productId = prodData.product_id || entry.name.split('_')[0] || `PROD-${Date.now()}`;
    const title = prodData.title || videoData.title || entry.name;
    const authorUnique = prodData.source_video?.author || videoData.author?.unique_id || 'creator';
    const authorNick = prodData.source_video?.nickname || videoData.author?.nickname || authorUnique;
    const plays = videoData.stats?.plays || 0;
    const likes = videoData.stats?.likes || 0;
    const comments = videoData.stats?.comments || 0;
    const shares = videoData.stats?.shares || 0;

    const hasVideo = fs.existsSync(videoMp4Path);
    const hasCover = fs.existsSync(coverJpgPath);
    const hasGeneratedVideo = fs.existsSync(generatedVideoPath);

    const status: JobStatus = prodData.status || (hasGeneratedVideo ? 'DA_LAM_VIDEO' : 'CHUA_LAM');
    const prompts = generatePromptsForProduct(title, authorUnique, { plays, likes });

    const job: JobItem = {
      id: `JOB-${productId}`,
      product_id: productId,
      title: title,
      keyword: prodData.keyword || 'Sản phẩm hot',
      pdp_url: prodData.pdp_url || '',
      affiliate_pdp_url: prodData.affiliate_pdp_url || prodData.pdp_url || '',
      cover_url: `/api/media/${entry.name}/cover.jpg`,
      price: prodData.price || 0,
      categories: prodData.categories || ['Thời trang nữ'],
      author: {
        unique_id: authorUnique,
        nickname: authorNick,
        avatar: videoData.author?.avatar || '',
      },
      source_video: {
        video_id: prodData.source_video?.video_id || videoData.id || '',
        url: prodData.source_video?.video_url || videoData.original_url || '',
        desc: prodData.source_video?.desc || videoData.title || '',
        duration: videoData.duration || 60,
      },
      stats: {
        plays,
        likes,
        comments,
        shares,
        engagement_rate: plays > 0 ? (((likes + comments + shares) / plays) * 100).toFixed(2) + '%' : '0%',
      },
      assets: {
        video_url: hasVideo ? `/api/media/${entry.name}/video_clean.mp4` : undefined,
        cover_url: hasCover ? `/api/media/${entry.name}/cover.jpg` : undefined,
        has_video: hasVideo,
        has_cover: hasCover,
        folder: entry.name,
      },
      status: status,
      generated_video_path: hasGeneratedVideo ? `/api/media/${entry.name}/generated_video.mp4` : undefined,
      video_type: prodData.video_type || undefined,
      ingested_at: prodData.ingested_at || new Date().toISOString(),
      prompts: prompts,
    };

    jobs.push(job);
  }

  jobs.sort((a, b) => new Date(b.ingested_at).getTime() - new Date(a.ingested_at).getTime());
  return jobs;
}
