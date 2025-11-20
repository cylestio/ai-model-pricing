Claude: Please follow the following instructions and do them


# How to update pricing

This guide explains how to manually update the `latest.json` file with current AI model pricing.

## 📁 File Format

The `latest.json` file has the following structure:

```json
{
  "last_updated": "2025-11-20T00:00:00+00:00",
  "models": {
    "anthropic": {
      "model-api-id": {
        "description": "Human-readable model name",
        "input": 3.0,
        "output": 15.0
      }
    },
    "openai": {
      "model-name": {
        "description": "Human-readable model name",
        "input": 2.5,
        "output": 10.0
      }
    }
  },
  "sources": {
    "anthropic": "https://claude.com/pricing#api",
    "openai": "https://platform.openai.com/docs/pricing"
  }
}
```

### Field Descriptions

- **`last_updated`**: ISO 8601 timestamp (UTC) of when the data was last updated
- **`models`**: Object containing pricing by provider
- **`description`**: Human-readable model name for display
- **`input`**: Price per 1 million input tokens (USD)
- **`output`**: Price per 1 million output tokens (USD)
- **`sources`**: URLs to official pricing pages

## 🔵 Anthropic (Claude) Pricing

### Official Sources

#### 1. Latest Models & Pricing
**URL**: https://claude.com/pricing#api

This page shows:
- **Latest models** (Sonnet 4.5, Haiku 4.5, Opus 4.1)
- **Legacy models** (older versions still available)
- Pricing per million tokens (MTok)

#### 2. Model API Names
**URL**: https://platform.claude.com/docs/en/about-claude/models/overview

This page shows:
- **Claude API ID** (e.g., `claude-sonnet-4-5-20250929`)
- **Claude API alias** (e.g., `claude-sonnet-4-5`)
- Model features and specifications

#### 3. Deprecated Models
**URL**: https://platform.claude.com/docs/en/about-claude/model-deprecations

This page lists:
- Models that are deprecated but may still work
- Deprecation dates
- Recommended migration paths

### How to Update Claude Pricing

1. Go to https://claude.com/pricing#api
2. Scroll to the "Latest models" section
3. For each model, note:
   - Model name (for description)
   - Input price ($ / MTok)
   - Output price ($ / MTok)
4. Go to https://platform.claude.com/docs/en/about-claude/models/overview
5. Find the **Claude API ID** for each model (this is the key in JSON)
6. Also add the **Claude API alias** if listed
7. Update `latest.json` with both the dated version and alias

### Claude Pricing Example

From the pricing page, you see:
```
Sonnet 4.5
Input: $3 / MTok
Output: $15 / MTok
```

From the models page, the API ID is: `claude-sonnet-4-5-20250929`

Add to JSON:
```json
"claude-sonnet-4-5-20250929": {
  "description": "Claude Sonnet 4.5",
  "input": 3.0,
  "output": 15.0
},
"claude-sonnet-4-5": {
  "description": "Claude Sonnet 4.5 (latest)",
  "input": 3.0,
  "output": 15.0
}
```

### Current Claude Models (as of Nov 2025)

**Latest models:**
- Sonnet 4.5: `claude-sonnet-4-5-20250929` / `claude-sonnet-4-5`
- Haiku 4.5: `claude-haiku-4-5-20251001` / `claude-haiku-4-5`
- Opus 4.1: `claude-opus-4-1-20250805` / `claude-opus-4-1`

**Legacy models** (mark with "(legacy)" in description):
- Sonnet 4: `claude-sonnet-4-20250514` / `claude-sonnet-4-0`
- Sonnet 3.7: `claude-3-7-sonnet-20250219` / `claude-3-7-sonnet-latest`
- Opus 4: `claude-opus-4-20250514` / `claude-opus-4-0`
- Haiku 3.5: `claude-3-5-haiku-20241022` / `claude-3-5-haiku-latest`
- Haiku 3: `claude-3-haiku-20240307`

## 🟢 OpenAI Pricing

### Official Source

**URL**: https://platform.openai.com/docs/pricing?latest-pricing=standard

This page shows:
- All current models with pricing tiers (Batch, Flex, Standard, Priority)
- Pricing per 1M tokens
- Model capabilities

**Important**: We use the **Standard** pricing tier for all models in `latest.json`. This is the most common tier that most users will use.

### How to Update OpenAI Pricing

1. Go to https://platform.openai.com/docs/pricing?latest-pricing=standard
2. Scroll to the **"Text tokens"** section and select the **"Standard"** tab
3. For each model in the pricing table:
   - Note the model name (e.g., `gpt-5`, `gpt-4.1`, `gpt-4o`)
   - Note input price per 1M tokens (under "Input" column)
   - Note output price per 1M tokens (under "Output" column)
   - Ignore "Cached input" column (not tracked in our dataset)
4. Update `latest.json` with each model
5. **Skip**: Image tokens, Audio tokens, Video, Fine-tuning, and other non-text sections

### OpenAI Model Naming

OpenAI uses straightforward model names:
- **Base models**: `gpt-5`, `gpt-5.1`, `gpt-4.1`, `gpt-4o`
- **Dated versions**: `gpt-4o-2024-11-20`, `o1-mini-2024-09-12`
- **Size variants**: `gpt-5-mini`, `gpt-5-nano`, `gpt-4.1-mini`, `gpt-4o-mini`
- **Specialized**: `gpt-5-codex`, `gpt-5-pro`, `gpt-5-search-api`
- **o-series**: `o1`, `o1-pro`, `o3`, `o3-pro`, `o4-mini`
- **Preview/specialized**: `gpt-4o-audio-preview`, `gpt-realtime`, `computer-use-preview`

### Current OpenAI Models (verify on site)

**GPT-5 series (latest):**
- `gpt-5.1`, `gpt-5` - Main GPT-5 models
- `gpt-5-mini`, `gpt-5-nano` - Smaller variants
- `gpt-5.1-chat-latest`, `gpt-5-chat-latest` - Chat-optimized
- `gpt-5.1-codex`, `gpt-5-codex`, `gpt-5.1-codex-mini` - Code-optimized
- `gpt-5-pro` - Premium model
- `gpt-5-search-api` - Search-optimized

**GPT-4.1 series (latest):**
- `gpt-4.1` - Main model
- `gpt-4.1-mini`, `gpt-4.1-nano` - Smaller variants

**GPT-4o family:**
- `gpt-4o` - Main model
- `gpt-4o-mini` - Smaller variant
- `gpt-4o-2024-11-20`, `gpt-4o-2024-08-06`, `gpt-4o-2024-05-13` - Dated versions
- Preview models: `gpt-4o-audio-preview`, `gpt-4o-realtime-preview`, `gpt-4o-search-preview`
- Mini previews: `gpt-4o-mini-audio-preview`, `gpt-4o-mini-realtime-preview`, `gpt-4o-mini-search-preview`

**o-series (reasoning models):**
- `o1`, `o1-pro` - Latest o1 models
- `o1-preview`, `o1-mini` - Preview versions
- `o3`, `o3-pro`, `o3-mini` - o3 series
- `o3-deep-research` - Deep research variant
- `o4-mini`, `o4-mini-deep-research` - o4 series

**Specialized models:**
- `gpt-realtime`, `gpt-realtime-mini` - Realtime processing
- `gpt-audio`, `gpt-audio-mini` - Audio processing
- `gpt-image-1`, `gpt-image-1-mini` - Image understanding
- `codex-mini-latest` - Code generation
- `computer-use-preview` - Computer use

**Legacy models:**
- GPT-4 Turbo: `gpt-4-turbo`, `gpt-4-turbo-2024-04-09`, `chatgpt-4o-latest`
- GPT-4: `gpt-4`, `gpt-4-0613`, `gpt-4-32k`, etc.
- GPT-3.5: `gpt-3.5-turbo`, `gpt-3.5-turbo-0125`, `gpt-3.5-turbo-instruct`, etc.
- Base models: `davinci-002`, `babbage-002`

## 📝 Step-by-Step Update Process

### 1. Check Official Sources

- [ ] Visit https://claude.com/pricing#api
- [ ] Visit https://platform.claude.com/docs/en/about-claude/models/overview
- [ ] Visit https://platform.openai.com/docs/pricing?latest-pricing=standard

### 2. Update latest.json

1. Open `latest.json` in your editor
2. Update `last_updated` timestamp:
   ```json
   "last_updated": "2025-11-20T00:00:00+00:00"
   ```
   (Use current date/time in ISO 8601 format)

3. Update Claude models in `models.anthropic` section
4. Update OpenAI models in `models.openai` section
5. Verify JSON is valid (use `json.tool` or online validator)

### 3. Verify Changes

```bash
# Validate JSON syntax
python3 -m json.tool latest.json > /dev/null && echo "✓ Valid JSON"

# View current models
python3 -c "
import json
with open('latest.json') as f:
    data = json.load(f)
    print('Anthropic models:', len(data['models']['anthropic']))
    print('OpenAI models:', len(data['models']['openai']))
"
```

### 4. Commit and Push

```bash
git add latest.json
git commit -m "Update pricing - [date]"
git push
```

## ⚠️ Important Notes

### Pricing Format
- All prices are in **USD per 1 million tokens**
- Use decimal format (e.g., `3.0`, not `3`)
- Input and output prices are separate
- **Text tokens only** - we don't track image, audio, video, or fine-tuning pricing
- Use **Standard pricing tier** for OpenAI models (not Batch, Flex, or Priority)

### Model Naming
- Use the **exact API ID** from documentation
- For Claude: Use the full dated ID (e.g., `claude-sonnet-4-5-20250929`)
- Include aliases when available (e.g., `claude-sonnet-4-5`)
- For OpenAI: Use lowercase, exact as shown on pricing page

### Legacy Models
- Keep legacy models that are still accessible
- Mark them with "(legacy)" in the description
- Remove only when officially deprecated and non-functional

### Common Mistakes
- ❌ Using pricing per 1K tokens (should be per 1M)
- ❌ Missing decimal point (use `3.0`, not `3`)
- ❌ Wrong model IDs (copy exactly from docs)
- ❌ Forgetting to update timestamp
- ❌ Using Batch/Flex/Priority pricing instead of Standard
- ❌ Including image/audio/video model pricing (text tokens only)
- ❌ Copying "Cached input" prices (we don't track those)

## 🔍 Quick Reference

### Claude Model ID Format
```
claude-{family}-{version}-{date}
Examples:
  claude-sonnet-4-5-20250929
  claude-haiku-4-5-20251001
  claude-opus-4-1-20250805
```

### OpenAI Model ID Format
```
{model}-{variant}
{model}-{version}-{date}
Examples:
  gpt-5, gpt-5.1, gpt-5-mini, gpt-5-nano
  gpt-4.1, gpt-4.1-mini, gpt-4.1-nano
  gpt-4o, gpt-4o-mini
  gpt-4o-2024-11-20
  o1, o1-pro, o1-mini
  o3, o3-pro, o3-mini, o3-deep-research
  o4-mini, o4-mini-deep-research
  gpt-5-codex, gpt-5-search-api
  gpt-realtime, gpt-audio, gpt-image-1
```

## 📊 Pricing Comparison Table Template

| Model | Input ($/1M) | Output ($/1M) | Source |
|-------|-------------|--------------|---------|
| **Anthropic** | | | |
| Claude Sonnet 4.5 | $3 | $15 | claude.com/pricing |
| Claude Haiku 4.5 | $1 | $5 | claude.com/pricing |
| Claude Opus 4.1 | $15 | $75 | claude.com/pricing |
| **OpenAI** | | | |
| GPT-5 / GPT-5.1 | $1.25 | $10 | platform.openai.com |
| GPT-5 Mini | $0.25 | $2 | platform.openai.com |
| GPT-5 Pro | $15 | $120 | platform.openai.com |
| GPT-4.1 | $2 | $8 | platform.openai.com |
| GPT-4.1 Mini | $0.40 | $1.60 | platform.openai.com |
| GPT-4o | $2.50 | $10 | platform.openai.com |
| GPT-4o Mini | $0.15 | $0.60 | platform.openai.com |
| o1 | $15 | $60 | platform.openai.com |
| o1 Pro | $150 | $600 | platform.openai.com |
| o3 | $2 | $8 | platform.openai.com |
| o3 Pro | $20 | $80 | platform.openai.com |
| o4 Mini | $1.10 | $4.40 | platform.openai.com |

## 🤖 Asking AI to Update

When asking an AI assistant (like me!) to update the pricing:

**Good prompt:**
```
Please update latest.json with current pricing from:
- Claude: https://claude.com/pricing#api
- OpenAI: https://platform.openai.com/docs/pricing?latest-pricing=standard

For OpenAI, use the "Text tokens" section, "Standard" pricing tier only.
Ignore image, audio, video, and fine-tuning pricing.

Check the official model names at:
- https://platform.claude.com/docs/en/about-claude/models/overview

Include both latest and legacy models.
```

**What to verify:**
- Timestamp is current (ISO 8601 format)
- Model IDs match official documentation exactly
- Prices are per 1M tokens (not 1K)
- Using Standard pricing tier for OpenAI (not Batch/Flex/Priority)
- Text tokens only (no image/audio/video pricing)
- JSON is valid
- All current models are included
- Legacy models are marked with "(legacy)" in description

---

Last updated: November 20, 2025

