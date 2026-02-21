# Questionable AI (qAI) — Roadmap

## Problem Statement

AI models have different training data, architectures, and reasoning biases. Relying on a single model means inheriting its blind spots. Power users already work around this by manually querying multiple models, comparing responses, and cross-pollinating insights between conversations. This works but is slow and tedious.

Every existing multi-model tool either operates within a single vendor's ecosystem (Grok 4.20's 4-agent system, Anthropic's agent teams) or does cross-vendor comparison without a reflection loop (LLM Council, PolyCouncil). Nobody builds the full cycle: fan-out → reflection → refinement → synthesis across different vendors.

Questionable AI (qAI) automates the workflow that power users already do manually — and logs the full debate as structured data for analysis.

---

## Phased Delivery

### Phase 1: Foundation

**Goal:** Working CLI that executes the core debate loop — fan-out, reflection, synthesis — and saves transcripts.

**Deliverables:**
- OpenRouter integration with async parallel model calls
- Core debate orchestrator: initial round → reflection round → synthesis
- Model alias system (claude, gpt, gemini, grok → OpenRouter model IDs)
- CLI with `ask` command and core flags (--panel, --synthesizer, --rounds)
- JSON transcript logging to `~/.questionable-ai/transcripts/`
- Terminal output formatting (show debate progression live)
- Configurable reflection and synthesis prompt templates
- Config file for API key and default settings

**Done when:** `questionable-ai ask "test query"` fans out to 4 models, runs a reflection round, synthesizes, prints result, and saves a transcript.

### Phase 2: Expansion

**Goal:** Replay capability, additional output formats, file input, and ground truth scoring.

**Deliverables:**
- `replay` command — re-run synthesis or add rounds to existing transcripts
- `list` and `show` commands for transcript management
- Markdown output format
- `--file` flag for text extraction and context injection
- `--ground-truth` flag with post-debate scoring
- Cost tracking per debate (token counts, estimated cost)
- `config` command for managing defaults

**Done when:** Can replay past debates with different synthesizers, attach files to queries, and score debates against known answers.

### Phase 3: Maturity

**Goal:** Research tooling, alternative topologies, and polish for potential public release.

**Deliverables:**
- Transcript analysis tooling (convergence metrics, disagreement patterns, influence scoring)
- Alternative debate topologies (ring, star, adversarial)
- Local model support via Ollama (hybrid panel: cloud + local)
- README, documentation, and examples suitable for public consumption
- Batch mode for running the same query across multiple configurations

**Done when:** Tool is useful as both a personal productivity tool and a research platform for multi-model behavior analysis. Ready for public repo if desired.

---

## What Success Looks Like

- A tool I actually use when the answer matters — replacing my manual cross-conversation workflow
- Structured dataset of multi-model debate transcripts for behavior analysis
- At least one publishable finding from consensus poisoning or convergence pattern research
- If public: a tool other AI power users adopt because nothing else does cross-vendor reflection

---

## Out of Scope (for now)

- Web frontend — CLI-first, web later only if demand justifies it
- Real-time streaming of individual model responses during debate (nice-to-have, not MVP)
- Integration with AnythingLLM, LibreChat, or other frontends
- Autonomous continuous debate (human initiates, human decides when to stop)
- Fine-tuning or training based on debate outcomes
