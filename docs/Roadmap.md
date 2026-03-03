# Mutual Dissent — Roadmap

## Problem Statement

AI models have different training data, architectures, and reasoning biases. Relying on a single model means inheriting its blind spots. Power users already work around this by manually querying multiple models, comparing responses, and cross-pollinating insights between conversations. This works but is slow and tedious.

Every existing multi-model tool either operates within a single vendor's ecosystem (Grok 4.20's 4-agent system, Anthropic's agent teams) or does cross-vendor comparison without a reflection loop (LLM Council, PolyCouncil). Nobody builds the full cycle: fan-out → reflection → refinement → synthesis across different vendors.

Mutual Dissent automates the workflow that power users already do manually — and logs the full debate as structured data for analysis.

---

## Development History & Status

### Core Debate Loop ✅

Working CLI that executes the fan-out → reflection → synthesis loop and saves transcripts. OpenRouter integration with async parallel model calls, configurable reflection rounds, Rich terminal output, and JSON transcript logging to `~/.mutual-dissent/transcripts/`. Completed 2026-02-21 — first live 4-vendor debate: 41,476 tokens.

### Provider Abstraction ✅

Replaced the single-provider OpenRouter client with a provider abstraction layer supporting direct vendor API keys alongside OpenRouter. Config schema drives the router interface; schema upgrades shipped concurrently with provider work for richer transcripts from day one. See design decisions below. Completed as part of the CLI expansion work.

| Decision | Rationale |
|----------|-----------|
| `resolved_config` dict over `config_hash` | Hash of TOML sections is fragile (ordering, whitespace). Full dict is more bytes, zero ambiguity. |
| Dynamic pricing from OpenRouter API | Model prices change weekly. Hardcoded pricing = constant maintenance. |
| Config schema before router implementation | Config shape drives the router interface, not the other way around. |
| Schema upgrades concurrent with provider work | Avoids migration later. Richer schema from the first multi-provider transcript. |
| Topology/roles/RAG deferred | They're the research payload — deferred because plumbing isn't ready, not because they're optional. |

### CLI Research Tools ✅

Replay capability, markdown export, file input, ground-truth scoring, and cost tracking — the CLI became a complete research tool. Completed 2026-02-28 with 325+ tests.

### Web GUI ✅

NiceGUI-based web interface with two modes: a power-tool debate view for running debates with live streaming, and a research dashboard for analyzing transcripts with convergence charts, influence heatmaps, and cost tracking.

**Cross-tool integration scaffolding** was added as a prerequisite: per-panelist context injection, round-level event hooks, and experiment metadata schema. These establish interface contracts for the broader research platform (CounterSignal, CounterAgent). See `Lab/Cross-Tool Research Directions.md` for the full context.

### Documentation ✅

Mintlify docs site with AI assistant, MCP server integration, and LLM-optimized content at [docs.mutual-dissent.dev](https://docs.mutual-dissent.dev).

### Desktop App & Batch Mode — Planned

Tauri 2 desktop wrapper, transcript analysis tooling, alternative debate topologies (ring, star, adversarial), local model support via Ollama, batch mode, and public release polish.

---

## What Success Looks Like

- A tool I actually use when the answer matters — replacing my manual
  cross-conversation workflow
- Structured dataset of multi-model debate transcripts for behavior analysis
- At least one publishable finding from consensus poisoning or convergence
  pattern research
- If public: a tool other AI power users adopt because nothing else does
  cross-vendor reflection
- A research dashboard that makes transcript analysis visual and fast

---

## Out of Scope (for now)

- Integration with AnythingLLM, LibreChat, or other frontends
- Autonomous continuous debate (human initiates, human decides when to stop)
- Fine-tuning or training based on debate outcomes
- Mobile app (Tauri 2 supports it, but not a priority)
