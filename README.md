# AI Model Pricing

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Curated pricing data for OpenAI and Anthropic AI models.**

Simple JSON file with verified pricing for 80+ models. Manually maintained from official sources.

## 🚀 Usage

```python
import requests

url = "https://raw.githubusercontent.com/cylestio/ai-model-pricing/main/latest.json"
pricing = requests.get(url).json()

# Get model price
model = pricing['models']['openai']['gpt-4o']
print(f"${model['input']}/1M input, ${model['output']}/1M output")

# Calculate cost
def calc_cost(model_name, input_tokens, output_tokens):
    for models in pricing['models'].values():
        if model_name in models:
            m = models[model_name]
            return (input_tokens/1_000_000)*m['input'] + (output_tokens/1_000_000)*m['output']

cost = calc_cost("gpt-4o", 1500, 500)
print(f"Cost: ${cost:.6f}")
```

## 📦 What's Included

**Anthropic (16 models)**
- Latest: Claude Sonnet 4.5, Haiku 4.5, Opus 4.1
- Legacy: Claude 4, 3.7, 3.5, 3

**OpenAI (66 models)**
- Latest: GPT-5 series, GPT-4.1, GPT-4o, o3/o4 series
- Legacy: GPT-4 Turbo, o1 series, GPT-3.5

All prices in **USD per 1M tokens**.

## 🔗 Access

**Direct JSON:**
```
https://raw.githubusercontent.com/cylestio/ai-model-pricing/main/latest.json
```

**CDN (faster):**
```
https://cdn.jsdelivr.net/gh/cylestio/ai-model-pricing@main/latest.json
```

## 📁 Format

```json
{
  "last_updated": "2025-11-20T00:00:00+00:00",
  "models": {
    "anthropic": {
      "claude-sonnet-4-5-20250929": {
        "input": 3.0,
        "output": 15.0,
        "description": "Claude Sonnet 4.5"
      }
    },
    "openai": {
      "gpt-4o": {
        "input": 2.5,
        "output": 10.0,
        "description": "GPT-4o"
      }
    }
  },
  "sources": {
    "anthropic": "https://claude.com/pricing#api",
    "openai": "https://platform.openai.com/docs/pricing"
  }
}
```

## 🤖 For AI Agents

See **[MANUAL_UPDATE_GUIDE.md](MANUAL_UPDATE_GUIDE.md)** for update instructions.

**Quick prompt:**
```
Update latest.json per MANUAL_UPDATE_GUIDE.md

Sources:
- Claude: https://claude.com/pricing#api
- OpenAI: https://platform.openai.com/docs/pricing
```

## 📝 Data Sources

- **Claude**: [Pricing](https://claude.com/pricing#api) • [Models](https://platform.claude.com/docs/en/about-claude/models/overview)
- **OpenAI**: [Pricing](https://platform.openai.com/docs/pricing)

## 📜 License

MIT License - See [LICENSE](LICENSE)

---

*Manually curated • No warranty • Verify with official sources*
