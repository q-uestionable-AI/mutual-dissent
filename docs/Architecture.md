# Questionable AI (qAI) — Design

## Architecture

```
┌─────────────────────────────────────────────────┐
│                     CLI                          │
│  query, --panel, --synthesizer, --rounds, etc.   │
└──────────────────────┬──────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────┐
│                 Orchestrator                     │
│  Fan-out, round management, reflection injection │
└──────────────────────┬──────────────────────────┘
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
    ┌──────────┐ ┌──────────┐ ┌──────────┐
    │ Model A  │ │ Model B  │ │ Model C  │  ... up to 4
    │ (Claude) │ │  (GPT)   │ │ (Gemini) │
    └────┬─────┘ └────┬─────┘ └────┬─────┘
         │            │            │
         └────────────┼────────────┘
                      ▼
┌─────────────────────────────────────────────────┐
│              Reflection Router                   │
│  Injects other models' responses into next round │
└──────────────────────┬──────────────────────────┘
                       │
                       ▼  (repeat for N rounds)
                       │
┌─────────────────────────────────────────────────┐
│                 Synthesizer                      │
│  User-selected model gets all rounds + query     │
│  Produces final consolidated response            │
└──────────────────────┬──────────────────────────┘
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
   ┌────────────┐ ┌──────────┐ ┌──────────┐
   │  Terminal   │ │ JSON Log │ │ Markdown  │
   │  Output    │ │ (full)   │ │ (summary) │
   └────────────┘ └──────────┘ └──────────┘
```

### Component Descriptions

**CLI** — Entry point. Parses user query, panel selection, synthesizer choice, round count, and output options. Thin layer — delegates immediately to Orchestrator.

**Orchestrator** — Core engine. Manages the debate lifecycle: initial fan-out, round tracking, reflection injection, and synthesis invocation. Handles async parallel API calls.

**Model Adapters** — Thin wrappers around OpenRouter API calls. Each adapter knows its model ID and any model-specific prompt formatting. All adapters share the same interface — swap models without changing orchestration logic.

**Reflection Router** — Between rounds, constructs reflection prompts by injecting other models' responses. Each model sees the other panelists' output but not its own restated. Configurable reflection prompt template.

**Synthesizer** — Final step. The user-selected model receives the full debate context (query + all rounds) and produces a consolidated answer. Same adapter interface as panel models.

**Transcript Logger** — Writes full structured JSON for every debate. Also produces optional Markdown summary for quick review.

---

## Data Models

```python
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class ModelResponse:
    """Single response from one model in one round."""
    model_id: str           # OpenRouter model identifier
    model_name: str         # Human-readable name (e.g., "Claude", "GPT")
    round_number: int       # 0 = initial, 1+ = reflection rounds
    content: str            # Full response text
    timestamp: datetime     # When response was received
    token_count: int | None = None      # Tokens used (if available from API)
    latency_ms: int | None = None       # Response time in milliseconds


@dataclass
class DebateRound:
    """All responses from one round of the debate."""
    round_number: int
    responses: list[ModelResponse]
    round_type: str         # "initial" | "reflection" | "synthesis"


@dataclass
class DebateTranscript:
    """Complete record of a debate session."""
    transcript_id: str              # UUID
    query: str                      # Original user query
    panel: list[str]                # Model IDs that participated
    synthesizer_id: str             # Model ID selected for synthesis
    max_rounds: int                 # Configured reflection rounds
    rounds: list[DebateRound] = field(default_factory=list)
    synthesis: ModelResponse | None = None
    created_at: datetime = field(default_factory=datetime.now)
    metadata: dict = field(default_factory=dict)  # Version, config, etc.
```

---

## Schema

### Transcript JSON Format

```json
{
  "transcript_id": "uuid",
  "query": "user's original question",
  "panel": ["anthropic/claude-sonnet-4-5", "openai/gpt-4o", "google/gemini-2.5-pro", "x-ai/grok-4"],
  "synthesizer_id": "anthropic/claude-sonnet-4-5",
  "max_rounds": 1,
  "created_at": "2026-02-21T15:30:00Z",
  "rounds": [
    {
      "round_number": 0,
      "round_type": "initial",
      "responses": [
        {
          "model_id": "anthropic/claude-sonnet-4-5",
          "model_name": "Claude",
          "round_number": 0,
          "content": "...",
          "timestamp": "2026-02-21T15:30:01Z",
          "token_count": 450,
          "latency_ms": 2100
        }
      ]
    },
    {
      "round_number": 1,
      "round_type": "reflection",
      "responses": [...]
    }
  ],
  "synthesis": {
    "model_id": "anthropic/claude-sonnet-4-5",
    "model_name": "Claude",
    "round_number": -1,
    "content": "...",
    "timestamp": "2026-02-21T15:30:15Z",
    "token_count": 600,
    "latency_ms": 3200
  },
  "metadata": {
    "version": "0.1.0",
    "openrouter_api": true
  }
}
```

### Transcript Storage

```
~/.questionable-ai/
└── transcripts/
    └── 2026-02-21_uuid-short.json
```

---

## CLI Interface

```
questionable-ai
  ask         Submit a query to the panel for debate
  replay      Re-run synthesis on an existing transcript
  list        List saved transcripts
  show        Display a transcript
  config      Manage default settings
```

### ask

```
questionable-ai ask "What is the most effective approach to securing MCP servers?"
```

### Flags

| Flag | Type | Default | Description |
|------|------|---------|-------------|
| `--panel` | str (comma-sep) | `claude,gpt,gemini,grok` | Models to include on the panel |
| `--synthesizer` | str | `claude` | Model to perform final synthesis |
| `--rounds` | int | `1` | Number of reflection rounds (1-3) |
| `--output` | str | `terminal` | Output format: `terminal`, `json`, `markdown` |
| `--no-save` | flag | false | Don't save transcript to disk |
| `--verbose` | flag | false | Show individual model responses as they arrive |
| `--ground-truth` | str | None | Known correct answer for post-debate scoring |
| `--file` | path | None | File to include as context (text extracted, injected into prompt) |

### replay

```
questionable-ai replay <transcript-id> --synthesizer grok --rounds 1
```

Loads an existing transcript and re-runs with a different synthesizer or additional reflection rounds.

### Model Aliases

Short names map to OpenRouter model IDs in config:

| Alias | OpenRouter Model ID |
|-------|-------------------|
| `claude` | `anthropic/claude-sonnet-4.5` |
| `gpt` | `openai/gpt-5.2` |
| `gemini` | `google/gemini-2.5-pro` |
| `grok` | `x-ai/grok-4` |

Model IDs verified against OpenRouter offerings as of 2026-02-21.

---

## Prompt Templates

### Initial Round

```
You are participating in a multi-model panel discussion. Answer the following
query to the best of your ability.

Query: {query}
```

### Reflection Round

```
You previously answered a query as part of a multi-model panel. Here is your
original response, followed by how other models on the panel responded.

Your response:
{own_response}

Other panel members' responses:
{other_responses}

Reflect on the other responses. Where do you agree? Where do you disagree?
What did they identify that you missed? What did you get right that they missed?
Provide your refined answer.
```

### Synthesis Prompt

```
You are the designated synthesizer for a multi-model panel discussion. Below is
the full debate transcript including initial responses and reflection rounds.

Query: {query}

{formatted_transcript}

Synthesize the strongest elements from all panel members into a single,
well-reasoned response. Note where the panel reached consensus and where
significant disagreements remain.
```

---

## Extension Points

### Adding a New Model

1. Add alias and OpenRouter model ID to config mapping
2. No code changes required — the adapter is generic via OpenRouter

### Adding a New Debate Topology

Currently: full mesh (every model sees every other model's response). Future options:

- **Ring** — each model sees only the previous model's response
- **Star** — all responses route through synthesizer as coordinator
- **Adversarial** — explicitly assign "devil's advocate" role to one model

Add topology as a strategy class that implements the reflection routing interface.

### Adding a New Output Format

1. Create a formatter that takes a `DebateTranscript` and produces output
2. Register in CLI `--output` choices

### Adding Ground Truth Scoring

The `--ground-truth` flag enables post-debate analysis:
- Score each model's initial response against the known answer
- Score each model's reflection response — did reflection improve or degrade accuracy?
- Score the synthesis — is the final answer better than any individual?
- Output a scoring summary alongside the transcript

---

## Security Considerations

- **API key management** — OpenRouter API key stored in environment variable or `~/.questionable-ai/config.toml`, never in code or transcripts.
- **Transcript sanitization** — if transcripts are shared publicly, they may contain sensitive query content. No automatic sharing — user controls what leaves their machine.
- **Prompt injection via model responses** — a model's response in round 1 becomes part of another model's prompt in round 2. A malicious or manipulated response could attempt to influence other models through the reflection prompt. This is an inherent property of the architecture and a research area, not a bug to fix.
- **Cost control** — each debate is 4 + 4 + 1 = 9 API calls minimum. No runaway loops — rounds are hard-capped at 3.

---

## Documentation Standards

- Google-style docstrings (Args, Returns, Raises, Example)
- New modules get docstrings when created, not retrofitted
- Inline comments for non-obvious logic only
