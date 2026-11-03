# AI CAPABILITIES — Skill, Rule, Workflow & CLI của Gobi Social

> **Auto-generated** bởi `python scripts/agent/build_capability_registry.py` — KHÔNG sửa tay. Máy đọc: [`.agents/registry.json`](../.agents/registry.json).

## Quy ước chung cho MỌI AI tool (Claude Code, Cursor, Gemini, Codex, Antigravity...)
- **Nguồn sự thật duy nhất:** thư mục [`.agents/`](../.agents). `.agent/` và `.claude/skills` là symlink trỏ về đây — thêm/sửa skill CHỈ ở `.agents/skills/<tên>/SKILL.md`, rồi chạy lại script này.
- **Cách dùng 1 skill:** mở `.agents/skills/<tên>/SKILL.md`, đọc đầy đủ rồi làm theo. Tool không có cơ chế skill native vẫn dùng được bằng cách đọc file đó trực tiếp.
- **Video:** bắt đầu từ skill `hyperframes` (entry point bắt buộc), sau đó skill con phù hợp.
- Luật dự án: [`AGENTS.md`](../AGENTS.md) · kiến trúc: [`ARCHITECTURE.md`](../ARCHITECTURE.md) · tiếp quản: [`CONTINUITY.md`](../CONTINUITY.md).

## 1. Skills (25)

| Skill | Mô tả | Ghi chú |
|---|---|---|
| [`embedded-captions`](../.agents/skills/embedded-captions/SKILL.md) | Add captions or subtitles to an existing single-subject talking-head video without editing the footage. Use for plain verbatim captions, cinematic captions embedded behind the subject, VFX captions, “炸/特效/酷炫字幕,” or a ... |  |
| [`faceless-explainer`](../.agents/skills/faceless-explainer/SKILL.md) | Turn arbitrary text — an article, notes, a topic, a brief — into a faceless explainer video: there is no site or footage to capture, so the visuals are invented per scene (typography, abstract graphics, diagrams, data... |  |
| [`figma`](../.agents/skills/figma/SKILL.md) | Import Figma content into a HyperFrames composition — rendered assets, brand tokens, components, storyboard sections → reconstructed motion (frames read as states, not slides) (REST/CLI), connector-assisted motion whe... |  |
| [`flow-auto-video`](../.agents/skills/flow-auto-video/SKILL.md) | Biến một ý tưởng kịch bản ngắn thành video hoàn chỉnh trên Google Flow: tự viết kịch bản phân cảnh, Character Bible nhất quán, sinh 3 lớp prompt (Character ref sheet, Storyboard frame, Video prompt có neo style), và t... | chỉ gọi thủ công |
| [`general-video`](../.agents/skills/general-video/SKILL.md) | Author or edit a custom HyperFrames composition when no specialized workflow fits, or when BRIEF.md sets flow: companion. Use for longer or multi-scene pieces, brand and sizzle reels, montages, static loops, static ti... |  |
| [`hyperframes`](../.agents/skills/hyperframes/SKILL.md) | Mandatory entry point: read this first for any request to make, create, edit, animate, or render a video, animation, or motion graphic, including a promo, explainer, captioned clip, title card, overlay, slideshow or i... |  |
| [`hyperframes-animation`](../.agents/skills/hyperframes-animation/SKILL.md) | All animation knowledge for HyperFrames — atomic motion rules, multi-phase scene blueprints, scene transitions, broader motion-design techniques, AND the seven runtime adapters (GSAP default, plus Lottie, Three.js, An... |  |
| [`hyperframes-audio`](../.agents/skills/hyperframes-audio/SKILL.md) | Use when audio already placed in a HyperFrames composition needs to be mixed: fade-in/fade-out, crossfade, track gain or volume, volume automation, ducking, a music bed that fights a voiceover (voiceover carve), effec... |  |
| [`hyperframes-cli`](../.agents/skills/hyperframes-cli/SKILL.md) | Use the HyperFrames CLI development loop: init, add, catalog, capture, lint, check, snapshot, compare, grade-compare, preview, play, present, beats, keyframes, single or batch render, publish, cloud, cloudrun, feedbac... |  |
| [`hyperframes-core`](../.agents/skills/hyperframes-core/SKILL.md) | The HyperFrames composition contract — build one renderable project. Use for composition structure, the `data-*` timing attributes, `class="clip"`, tracks, sub-compositions, variables, framework-owned media playback, ... |  |
| [`hyperframes-creative`](../.agents/skills/hyperframes-creative/SKILL.md) | Non-animation creative direction for HyperFrames videos. Use for design spec (frame.md / design.md) handling, palettes, typography, narration, beat planning, audio-reactive visuals, composition patterns, and brand / s... |  |
| [`hyperframes-keyframes`](../.agents/skills/hyperframes-keyframes/SKILL.md) | Use when a HyperFrames composition needs a punch-in, punch-out, zoom, reframe, Ken Burns treatment, camera move, visual match/whip handoff, or other seek-safe 2D/3D keyframes; also for GSAP, CSS keyframes, Anime.js, W... |  |
| [`hyperframes-registry`](../.agents/skills/hyperframes-registry/SKILL.md) | Search, install, and wire registry blocks and components into HyperFrames compositions. Use BEFORE hand-building any named visual — whenever a brief, a user, or a storyboard names a look, effect, treatment, or transit... |  |
| [`hyperframes-studio`](../.agents/skills/hyperframes-studio/SKILL.md) | Use when working with a person on a HyperFrames project in Studio: first, whether their message asks for a change at all (questions, loose ideas and "don't change anything" get an answer and a plan, not an edit); for ... |  |
| [`media-use`](../.agents/skills/media-use/SKILL.md) | Agent Media OS for a HyperFrames project. Resolve BGM, SFX, image, icon, brand logo, voice, color grade, or LUT into a frozen local file or paste-ready block + ledger record (one verb, `resolve`); generate via TTS / m... |  |
| [`motion-graphics`](../.agents/skills/motion-graphics/SKILL.md) | Use when creating a short, design-led motion graphic where motion is the message — kinetic typography, stat count-up, chart/data-viz hit, logo sting / brand lockup, lower-third / callout / social overlay, animated map... |  |
| [`motion-mimic`](../.agents/skills/motion-mimic/SKILL.md) | Quy trình độc lập cho phép AI KOC Gobi (LyLy, Neau) bắt chước 100% chuyển động, nhép môi, cử chỉ từ một video bất kỳ (TikTok/Reels/Video nạp vào) và dựng xuất bản video 9:16 qua HeyGen HyperFrames. |  |
| [`music-to-video`](../.agents/skills/music-to-video/SKILL.md) | Turn a music track (an audio file, a video to pull audio from, or a track generated from a mood brief) into a beat-synced video — lyric video, slideshow, or kinetic promo. The music drives all pacing; any user-supplie... |  |
| [`pr-to-video`](../.agents/skills/pr-to-video/SKILL.md) | Turn a GitHub pull request (a PR URL, owner/repo#N, or 'this PR' in a checked-out repo) into a code-change explainer video — changelog, feature reveal, fix, or refactor walkthrough built from the diff, commits, and fi... |  |
| [`product-launch-video`](../.agents/skills/product-launch-video/SKILL.md) | Turn a product or marketing URL, pasted script, or brief into a product launch / promo video — SaaS promos, feature reveals, product demos, app and company launches. Use when the user wants to market, launch, promote,... |  |
| [`remotion-to-hyperframes`](../.agents/skills/remotion-to-hyperframes/SKILL.md) | Port an existing Remotion (React) composition's source to HyperFrames HTML. Use ONLY on an explicit ask to port/convert/migrate/translate a Remotion source — one-way, Remotion-only. A passing Remotion mention, referen... |  |
| [`slideshow`](../.agents/skills/slideshow/SKILL.md) | Author a HyperFrames slideshow — a presentation, pitch deck, or interactive deck with discrete slides, fragment reveals, branching, hotspot navigation, and built-in presenter mode with speaker notes; also converts an ... |  |
| [`talking-head-recut`](../.agents/skills/talking-head-recut/SKILL.md) | Package an existing talking-head / interview / podcast video with timed, designed GRAPHIC OVERLAY cards — kinetic titles, lower-thirds, data callouts, quotes, side panels, picture-in-picture — synced to the transcript... |  |
| [`unlimited-email-routing`](../.agents/skills/unlimited-email-routing/SKILL.md) | Tự động tạo và quản lý không giới hạn địa chỉ email miễn phí (Catch-all Email Routing) qua Addy.io hoặc Cloudflare để nhận mã OTP xác thực đăng ký hàng loạt tài khoản mạng xã hội (TikTok, Facebook, Instagram, Google).... |  |
| [`vietnamese-voice-clone`](../.agents/skills/vietnamese-voice-clone/SKILL.md) | Nhân bản bất kỳ giọng nói nào từ Video hoặc MP3 sang Tiếng Việt thuần Việt chuẩn ngữ điệu bằng OmniVoice SOTA, và dùng các giọng đã lưu trong kho (Voice Vault) để đọc kịch bản, content, văn bản review KOC TikTok/Reels... |  |

## 2. Rules (4)

| Rule | Always-on | Tóm tắt |
|---|---|---|
| [`architecture-governance`](../.agents/rules/architecture-governance.md) |  | SENIOR BACKEND ARCHITECTURE & REPOSITORY GOVERNANCE STANDARDS |
| [`graphify`](../.agents/rules/graphify.md) | yes | Consult the graphify knowledge graph at graphify-out/ for codebase and architecture questions. |
| [`hyperframes-post-production`](../.agents/rules/hyperframes-post-production.md) |  | MANDATORY VIDEO POST-PRODUCTION DIRECTIVE: HEYGEN HYPERFRAMES |
| [`relentless-execution`](../.agents/rules/relentless-execution.md) | yes | Quy tắc bắt buộc MẶC ĐỊNH làm việc đến cùng, không bỏ cuộc, không cần gõ /goal |

## 3. Workflows (1)

| Workflow | Tóm tắt |
|---|---|
| [`graphify`](../.agents/workflows/graphify.md) | Turn any folder of files into a navigable knowledge graph |

## 4. Gobi CLI (13)

| Lệnh | Chức năng |
|---|---|
| `python -m gobi account` | Quản lý ma trận 12 tài khoản KOC 12 Chòm Sao |
| `python -m gobi brief` | Phân tích video tham khảo + sản phẩm, in ra JSON kịch bản (không render video) |
| `python -m gobi learn` | Chạy chu trình tự học và tối ưu trọng số prompt |
| `python -m gobi mimic` | Chạy quy trình AI KOC bắt chước một video nạp vào và dựng qua HyperFrames |
| `python -m gobi policy` | Quét vi phạm chính sách & Safe Zone TikTok Shop |
| `python -m gobi product` | Quản trị kho sản phẩm KOC AI & tiến độ video |
| `python -m gobi prompt` | Sinh prompt ma trận 36 góc quay camera |
| `python -m gobi remix` | Dựa vào nội dung 1 video tham khảo, viết kịch bản mới (Gemini) và dựng video Gô Bi review sản phẩm (không swap mặt) |
| `python -m gobi snaptik` | Tải source video TikTok không logo (SnapTik) vào project |
| `python -m gobi tiktok` | Công cụ TikTok (Lấy link sản phẩm TikTok Shop từ video) |
| `python -m gobi video` | Render video hoặc xem trước timeline tự động với HyperFrames |
| `python -m gobi voice` | Tổng hợp giọng nói KOC tiếng Việt chuẩn |
| `python -m gobi warehouse` | Quản trị kho sản phẩm KOC AI (Mã SP, Status, Assigned KOC) |

## 5. Agent runtime trong code
- `scripts/agent/run_agent.py` → `gobi.services.os_kernel.AgentOS` (Agent-Reach, browser-use, video/subtitle inspector).
- `integrations/agent_reach/`, `integrations/hyperframes/` (có `AGENTS.md` riêng), `integrations/OmniVoice/`, `integrations/Wav2Lip/`.
- Subagent: không có định nghĩa riêng trong repo; tool nào hỗ trợ subagent thì dùng built-in của tool đó và truyền kèm quy tắc `AGENTS.md`.
