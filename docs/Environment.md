# Environment Variables

Mutual Dissent reads API keys from environment variables. Environment
variables override values in `~/.mutual-dissent/config.toml`.

## Supported Variables

| Variable | Provider | Required | Example |
|----------|----------|----------|---------|
| `OPENROUTER_API_KEY` | OpenRouter (universal fallback) | Yes* | `sk-or-v1-...` |
| `ANTHROPIC_API_KEY` | Anthropic (direct routing) | No | `sk-ant-...` |
| `OPENAI_API_KEY` | OpenAI (direct routing) | No | `sk-...` |
| `GOOGLE_API_KEY` | Google (direct routing) | No | `AI...` |
| `XAI_API_KEY` | xAI (direct routing) | No | `xai-...` |
| `GROQ_API_KEY` | Groq (direct routing) | No | `gsk_...` |

*At least one provider key is required. OpenRouter is the universal
fallback — if you only configure one key, use this one.

## Resolution Order

For each provider, Mutual Dissent resolves the API key in this order:

1. **Environment variable** (highest priority)
2. **`config.toml`** (`[providers]` section)
3. **Not configured** (requests to this provider will fail)

Environment variables **override** config file values — they do not merge.
If `OPENROUTER_API_KEY` is set in the environment, it replaces any
`openrouter_api_key` in `config.toml`.

## Setting Environment Variables

### PowerShell (current session)

```powershell
$env:OPENROUTER_API_KEY = "sk-or-v1-your-key-here"
```

### PowerShell (persistent — user profile)

Add to `$PROFILE`:

```powershell
$env:OPENROUTER_API_KEY = "sk-or-v1-your-key-here"
```

### Bash / Zsh (current session)

```bash
export OPENROUTER_API_KEY="sk-or-v1-your-key-here"
```

### Bash / Zsh (persistent)

Add to `~/.bashrc` or `~/.zshrc`:

```bash
export OPENROUTER_API_KEY="sk-or-v1-your-key-here"
```

### .env file

Mutual Dissent does not read `.env` files directly. Use a tool like
[direnv](https://direnv.net/) or load the file manually:

```bash
source .env
```

## Checking Configuration

Use `dissent config show` to verify which keys are configured and
their source (env var vs config file). API keys are always masked
in the output.

```
dissent config show
```

## Provider Status

| Provider | Status | Notes |
|----------|--------|-------|
| OpenRouter | Active | Routes to all models via unified API |
| Anthropic | Active | Direct Claude API calls (lower latency) |
| OpenAI | Planned | Direct routing not yet implemented |
| Google | Planned | Direct routing not yet implemented |
| xAI | Planned | Direct routing not yet implemented |
| Groq | Planned | Direct routing not yet implemented |
