# AI Model Pricing

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Up-to-date pricing data for AI models from OpenAI and Anthropic.**

Simple JSON file with pricing for 50+ AI models, updated regularly via automated scraping.

## 🚀 Quick Start

```python
import requests

PRICING_URL = "https://raw.githubusercontent.com/cylestio/ai-model-pricing/main/latest.json"

pricing = requests.get(PRICING_URL).json()

# Get price for a model
gpt4o = pricing['models']['openai']['gpt-4o']
print(f"GPT-4o: ${gpt4o['input']}/1M input, ${gpt4o['output']}/1M output")

# Calculate cost
def calculate_cost(model_name, input_tokens, output_tokens):
    for provider in pricing['models'].values():
        if model_name in provider:
            model = provider[model_name]
            return (input_tokens / 1_000_000) * model['input'] + \
                   (output_tokens / 1_000_000) * model['output']
    return None

cost = calculate_cost("gpt-4o", 1500, 500)
print(f"Cost: ${cost:.6f}")
```

## 📦 Direct Access

**Raw JSON URL:**
```
https://raw.githubusercontent.com/cylestio/ai-model-pricing/main/latest.json
```

**CDN (faster, with caching):**
```
https://cdn.jsdelivr.net/gh/cylestio/ai-model-pricing@main/latest.json
```

## 📊 Available Models

- **OpenAI**: GPT-4o, GPT-4 Turbo, GPT-3.5, o1 series (40+ variants)
- **Anthropic**: Claude Sonnet 4, Claude Opus 4, Claude Haiku 3.5 (10+ variants)
- All prices in **USD per 1 million tokens**

## 📁 Data Format

```json
{
  "last_updated": "2025-11-19T00:00:00+00:00",
  "models": {
    "openai": {
      "gpt-4o": {
        "input": 2.50,
        "output": 10.00,
        "description": "GPT-4o"
      }
    },
    "anthropic": {
      "claude-sonnet-4-20250514": {
        "input": 3.00,
        "output": 15.00,
        "description": "Claude Sonnet 4"
      }
    }
  },
  "sources": {
    "openai": "https://platform.openai.com/docs/pricing",
    "anthropic": "https://docs.anthropic.com/en/docs/about-claude/models"
  }
}
```

## 🛠️ Run Locally

```bash
# Install dependencies
pip install -r script/requirements.txt

# Optional: For OpenAI Cloudflare bypass
pip install cloudscraper

# Fetch latest pricing
python3 script/fetch_pricing.py
```

## 📝 How It Works

1. Script scrapes pricing from official OpenAI and Anthropic pages
2. Validates and compares with existing data
3. Updates `latest.json` if changes detected
4. Falls back to existing data if scraping fails

**Note**: OpenAI blocks automated requests (Cloudflare). Use `cloudscraper` or run manually.

## 🤝 Contributing

Found incorrect pricing? Open an issue or submit a PR updating `latest.json`.

## ⚠️ Disclaimer

Unofficial project. Data scraped from public sources and provided as-is. No warranty. Always verify with official sources.

## 📜 License

MIT License - See [LICENSE](LICENSE)

---

**Data Sources**: [OpenAI Pricing](https://platform.openai.com/docs/pricing) • [Anthropic Models](https://docs.anthropic.com/en/docs/about-claude/models)
