# Gobi Social - Claude Code & Agent Directives

## Project Overview
Gobi Social is an autonomous AI KOC & Social Media Video Production and Intelligence System for "Gô Bi (Gobi Thúi)". It automates end-to-end social commerce video creation:
1. Big Data fashion trends mining (`configs/koc_fashion_bigdata_analytics.json`)
2. Master Character DNA consistency via 36-angle matrix (`MASTER_GOBI_OFFICIAL.jpg`, `GOBI_36_PANELS_OFFICIAL.jpg`)
3. Neural Vietnamese voiceover synthesis (`core/generate_gobi_voice.py`, `tools/voice/koc_voice_cloner.py`)
4. 9:16 Video rendering with Ken Burns motion & TikTok Safe Zone (`core/video_engine.py`, `core/render_gobi_boutique_v1.py`)
5. Policy compliance & AIGC safe-zone scanning (`tools/video/policy_compliance_checker.py`)
6. Continuous learning & dynamic prompt weight tuning (`core/continuous_learning_engine.py`)

## Core Rules for All Agents
1. **Relentless Execution:** Always adhere to `AGENTS.md`. Never give up on the first failure. Test at least 3-5 alternative strategies before asking user input.
2. **Strict Portability:** NEVER hardcode absolute paths (e.g. `C:\Users\...`). Always use `os.path.dirname(os.path.abspath(__file__))`, `os.path.expanduser("~")`, or relative paths.
3. **Character Consistency:** Preserve Gobi's character persona, face DNA, and 36-angle camera matrix.
4. **Session Documentation:** When completing a new milestone, document it in `conversation/sessions/` using `conversation/TEMPLATE_CONVERSATION_LOG.md` and add a new row to `conversation/SESSION_INDEX.md`.

## Key Commands
- Check policy compliance: `python tools/video/policy_compliance_checker.py --script "<text>"`
- Run continuous learning engine: `python core/continuous_learning_engine.py`
- Generate KOC prompts: `python core/koc_prompt_generator.py`
- Render Gobi video: `python core/render_gobi_boutique_v1.py`
- Run voice cloner: `python clone_voice_from_video.py --input <path> --name <voice_name>`
