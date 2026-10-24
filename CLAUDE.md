# Gobi Social - Claude Code & Agent Directives

## Project Overview
Gobi Social is an autonomous AI KOC & Social Media Video Production and Intelligence System for "Gô Bi (Gobi Thúi)". It automates end-to-end social commerce video creation:
1. Big Data fashion trends mining (`configs/koc_fashion_bigdata_analytics.json`)
2. Master Character DNA consistency via 36-angle matrix (`assets/koc_dna/MASTER_GOBI_OFFICIAL.jpg`, `assets/koc_dna/GOBI_36_PANELS_OFFICIAL.jpg`)
3. Neural Vietnamese voiceover synthesis (`src/gobi/services/voice/generate_gobi_voice.py`, `src/gobi/services/voice/koc_voice_cloner.py`)
4. 9:16 Video rendering with Ken Burns motion & TikTok Safe Zone (`src/gobi/services/media/video_engine.py`, `src/gobi/services/media/render_gobi_boutique_v1.py`)
5. Policy compliance & AIGC safe-zone scanning (`src/gobi/domain/policy_compliance_checker.py`)
6. Continuous learning & dynamic prompt weight tuning (`src/gobi/services/intelligence/continuous_learning_engine.py`)

## Core Rules for All Agents
1. **Relentless Execution:** Always adhere to `AGENTS.md`. Never give up on the first failure. Test at least 3-5 alternative strategies before asking user input.
2. **Strict Portability:** NEVER hardcode absolute paths (e.g. `C:\Users\...`). Always use `os.path.dirname(os.path.abspath(__file__))`, `os.path.expanduser("~")`, or relative paths.
3. **Character Consistency:** Preserve Gobi's character persona, face DNA, and 36-angle camera matrix.
4. **Session Documentation:** When completing a new milestone, document it in `conversation/sessions/` using `conversation/TEMPLATE_CONVERSATION_LOG.md` and add a new row to `conversation/SESSION_INDEX.md`.
5. **Architecture Governance & Zero-Root-Pollution:** Strictly follow [`ARCHITECTURE.md`](ARCHITECTURE.md). NEVER create loose scripts or dumps in the root directory. Place business logic in `src/gobi/`, temporary debug scripts in `scratch/`, external repos in `integrations/<repo_name>/`, and raw data in `data/raw/`.
6. **Mandatory Video Post-Production with HyperFrames:** Always automatically use **HeyGen HyperFrames** (`HyperFramesEngine`, `HyperFramesAdapter`, see [`docs/HYPERFRAMES_POST_PRODUCTION_STANDARD.md`](docs/HYPERFRAMES_POST_PRODUCTION_STANDARD.md)) for editing, captions, overlays, badges, audio ducking, and final 9:16 master renders.

## Key Commands
- Render video with HyperFrames: `python -m gobi video render --engine hyperframes`
- Preview video in HyperFrames Studio: `python -m gobi video preview` or `npx hyperframes preview`
- Download clean TikTok video (SnapTik): `python -m gobi snaptik <URL> -a -c`
- Check policy compliance: `python src/gobi/domain/policy_compliance_checker.py --script "<text>"`
- Run continuous learning engine: `python src/gobi/services/intelligence/continuous_learning_engine.py`
- Generate KOC prompts: `python src/gobi/services/prompt/koc_prompt_generator.py`
- Run voice cloner: `python scripts/voice/clone_voice_from_video.py --input <path> --name <voice_name>`

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

Rules:
- When graphify-out/graph.json exists, run `graphify query "<question>"` before your first grep, search or source-file read for a codebase question, and put this rule in every subagent prompt that explores code. Read raw files only for lines the graph or an earlier read already located. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
- A committed graphify-out/graph.json is rewritten whole on every build, so a large diff to it in a pull request is expected. Do not flag it as churn or suggest skipping the graph rebuild or its hooks.
