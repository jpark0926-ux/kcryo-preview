# Model Switching Guide for OpenClaw

## Current Setup
- **Provider:** Anthropic (API Key)
- **Current Model:** `anthropic/claude-sonnet-4-5` (Claude Sonnet 4.5)
- **Auth:** `ANTHROPIC_API_KEY` environment variable

## Available Anthropic Models

| Model ID | Alias | Use Case | Speed | Cost |
|----------|-------|----------|-------|------|
| `anthropic/claude-sonnet-4-5` | Sonnet | Balanced, fast, efficient | ⚡⚡⚡ | 💰 |
| `anthropic/claude-opus-4` | Opus | Deep research, max quality | ⚡ | 💰💰💰 |
| `anthropic/claude-sonnet-3-5` | Sonnet 3.5 | Cheaper, older | ⚡⚡⚡ | 💰 (cheaper) |

## How to Configure Multiple Models

### Option 1: Models Allowlist with Aliases (Recommended)

Add this to your `~/.openclaw/openclaw.json`:

```json5
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-sonnet-4-5",
        "fallbacks": [
          "anthropic/claude-opus-4",
          "anthropic/claude-sonnet-3-5"
        ]
      },
      "models": {
        "anthropic/claude-sonnet-4-5": { "alias": "sonnet" },
        "anthropic/claude-opus-4": { "alias": "opus" },
        "anthropic/claude-sonnet-3-5": { "alias": "sonnet3" }
      }
    }
  }
}
```

**Benefits:**
- Easy switching with `/model opus` or `/model sonnet`
- Automatic fallback if primary model fails
- Allowlist prevents accidentally using expensive models

### Option 2: CLI Commands

Use OpenClaw CLI to manage models:

```bash
# Set primary model
openclaw models set anthropic/claude-opus-4

# Add aliases
openclaw models aliases add opus anthropic/claude-opus-4
openclaw models aliases add sonnet anthropic/claude-sonnet-4-5

# Configure fallbacks
openclaw models fallbacks add anthropic/claude-opus-4
openclaw models fallbacks add anthropic/claude-sonnet-3-5

# View current status
openclaw models status
```

## Switching Models in Chat

### Method 1: Slash Command
```
/model                    # Show available models
/model list              # Same as above
/model opus              # Switch to Opus (using alias)
/model anthropic/claude-opus-4   # Switch using full ID
/model status            # Check current model
```

### Method 2: Natural Language (via Wayne Manor)
Just tell me:
- "Switch to Opus" or "Use Opus mode"
- "Back to Sonnet" or "Default model"
- "Deep research mode" (I'll switch to Opus automatically)

I'll use `session_status` tool to change the model for the current session.

## Adding Other Providers (Future)

### OpenAI GPT Models
```json5
{
  "agents": {
    "defaults": {
      "models": {
        "openai/gpt-4o": { "alias": "gpt4" },
        "openai/o1": { "alias": "o1" }
      }
    }
  },
  "env": {
    "OPENAI_API_KEY": "sk-..."
  }
}
```

### OpenRouter (Multi-Provider)
```json5
{
  "agents": {
    "defaults": {
      "models": {
        "openrouter/anthropic/claude-opus-4": { "alias": "opus-router" }
      }
    }
  },
  "env": {
    "OPENROUTER_API_KEY": "sk-or-..."
  }
}
```

## Automatic Model Selection (Smart Switching)

You can configure Wayne Manor to automatically switch models based on task type:

### Trigger Keywords
- **Deep research, 심층 분석, 자세히** → Switch to Opus
- **Quick, 빨리, 간단히** → Switch to Sonnet
- **Reasoning, 추론** → Switch to o1 (if configured)

### Implementation Options

**Option A: I handle it in conversation**
- You say "deep research on [topic]"
- I recognize the keyword and switch to Opus
- I perform the task
- I switch back to default

**Option B: Sub-agent spawn**
```
sessions_spawn with agentId + model override
→ Isolated session with Opus
→ Results delivered back
→ Main session stays on Sonnet
```

## Cost Considerations

| Model | Input (per 1M tokens) | Output (per 1M tokens) |
|-------|----------------------|------------------------|
| Sonnet 4.5 | $3 | $15 |
| Opus 4 | $15 | $75 |
| Sonnet 3.5 | $3 | $15 |

**Rule of thumb:** Use Sonnet for 90% of tasks, Opus for 10% where quality matters most.

## Next Steps

1. **Apply config**: Update `openclaw.json` with model allowlist + aliases
2. **Test switching**: Try `/model list` and `/model opus` in chat
3. **Set up triggers**: Decide which keywords should auto-switch models
4. **Monitor costs**: Use `session_status` to track model usage

---

**Created:** 2026-02-12  
**For:** Chris (@Chrisjpark)  
**By:** Wayne Manor 🦇
