# AI Model Pricing

[![Update Pricing](https://github.com/YOUR_USERNAME/ai-model-pricing/actions/workflows/update-pricing.yml/badge.svg)](https://github.com/YOUR_USERNAME/ai-model-pricing/actions/workflows/update-pricing.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Always up-to-date pricing data for AI models from OpenAI and Anthropic.**

This repository automatically tracks and updates pricing for large language models (LLMs) from major providers. A GitHub Action runs weekly to fetch the latest pricing, and the data is available as a simple JSON file you can fetch directly from the repo.

## 🚀 Quick Start

### Use in Your Application

Fetch the latest pricing directly from GitHub:

```python
import requests

PRICING_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/ai-model-pricing/main/pricing/latest.json"

def get_pricing():
    response = requests.get(PRICING_URL)
    return response.json()

pricing_data = get_pricing()
print(f"Last updated: {pricing_data['last_updated']}")

# Get price for a specific model
gpt4o = pricing_data['models']['openai']['gpt-4o']
print(f"GPT-4o: ${gpt4o['input']}/1M input, ${gpt4o['output']}/1M output")
```

### Calculate API Costs

```python
def calculate_cost(model_name, input_tokens, output_tokens, pricing_data):
    """Calculate cost for an API call."""
    # Find model in pricing data
    for provider in pricing_data['models'].values():
        if model_name in provider:
            model = provider[model_name]
            input_cost = (input_tokens / 1_000_000) * model['input']
            output_cost = (output_tokens / 1_000_000) * model['output']
            return input_cost + output_cost
    return None

cost = calculate_cost("gpt-4o", 1500, 500, pricing_data)
print(f"Cost: ${cost:.6f}")
```

### Direct URL

Use this URL to fetch the latest pricing:
```
https://raw.githubusercontent.com/YOUR_USERNAME/ai-model-pricing/main/pricing/latest.json
```

## 📊 Available Data

The pricing data includes:

- **OpenAI Models**: GPT-4o, GPT-4, GPT-3.5, o1 series, and all variants
- **Anthropic Models**: Claude 3.5, Claude 3, and all variants
- **90+ model variants** tracked
- **Prices in USD per 1M tokens** (input and output)
- **Last updated timestamp**

## 🔄 How It Works

1. **Automated Updates**: GitHub Action runs every Monday at 2 AM UTC
2. **Price Fetching**: Script scrapes official pricing pages from OpenAI and Anthropic
3. **Change Detection**: Compares new prices with existing data
4. **Auto-Commit**: If changes detected, commits updated JSON to repository
5. **Notifications**: GitHub Action logs show what changed

## 📁 Data Format

```json
{
  "last_updated": "2025-11-19T00:00:00+00:00",
  "sources": {
    "openai": "https://openai.com/api/pricing/",
    "anthropic": "https://docs.anthropic.com/en/docs/about-claude/models"
  },
  "models": {
    "openai": {
      "gpt-4o": {
        "input": 2.50,
        "output": 10.00,
        "description": "GPT-4o"
      },
      "gpt-4o-mini": {
        "input": 0.15,
        "output": 0.60,
        "description": "GPT-4o Mini"
      }
    },
    "anthropic": {
      "claude-3-5-sonnet-20241022": {
        "input": 3.00,
        "output": 15.00,
        "description": "Claude 3.5 Sonnet"
      }
    }
  }
}
```

All prices are in **USD per 1 million tokens**.

## 🛠️ Local Usage

### Prerequisites

```bash
pip install -r requirements.txt
```

### Fetch Latest Pricing

```bash
python scripts/fetch_pricing.py
```

This will:
- Fetch pricing from OpenAI and Anthropic
- Compare with existing data
- Update `pricing/latest.json` if changes found
- Display summary of changes

### Options

```bash
# Force update even if no changes
python scripts/fetch_pricing.py --force

# Verbose output
python scripts/fetch_pricing.py --verbose
```

## 🤖 GitHub Action

The repository includes a GitHub Action (`.github/workflows/update-pricing.yml`) that:

- **Runs weekly**: Every Monday at 2 AM UTC
- **Manual trigger**: Can be triggered manually from Actions tab
- **Auto-commits**: Commits changes if pricing updates detected
- **Notifications**: Check the Actions tab for run history

### Manual Trigger

1. Go to the "Actions" tab
2. Select "Update AI Model Pricing"
3. Click "Run workflow"

## 📝 Data Sources

This repository fetches data from official sources:

- **OpenAI**: https://openai.com/api/pricing/
- **Anthropic**: https://docs.anthropic.com/en/docs/about-claude/models

### Limitations

- **Web scraping**: Data is scraped from public pages (no official API available)
- **Anti-bot measures**: Some providers may block automated requests
- **Fallback data**: If scraping fails, uses last known good data
- **Not real-time**: Updates weekly (sufficient for pricing which rarely changes)

### Reliability

✅ **OpenAI**: May be blocked (403), falls back to manual updates  
✅ **Anthropic**: Usually works, scraped from documentation  
✅ **Fallback**: Last known good pricing always available  

## 🤝 Contributing

### Report Incorrect Pricing

If you notice incorrect pricing:

1. Check the official source (links above)
2. Open an issue with details
3. Or submit a PR updating `pricing/latest.json`

### Improve Scraping

To improve the scraping logic:

1. Fork the repository
2. Update `scripts/fetch_pricing.py`
3. Test thoroughly
4. Submit a PR with description

### Add New Providers

Want to track more providers (Google, Cohere, etc.)?

1. Update `scripts/fetch_pricing.py` with new fetching logic
2. Update JSON schema in `pricing/latest.json`
3. Update this README
4. Submit a PR

## 📋 Use Cases

- **Cost Estimation**: Calculate estimated costs before making API calls
- **Budget Tracking**: Monitor spending across different models
- **Model Comparison**: Compare prices to choose cost-effective models
- **Alerting**: Monitor for price changes
- **Analytics**: Track pricing trends over time
- **Documentation**: Keep pricing documentation up-to-date

## 🔐 API Integration Examples

### Python

```python
import requests

class PricingClient:
    def __init__(self):
        self.url = "https://raw.githubusercontent.com/YOUR_USERNAME/ai-model-pricing/main/pricing/latest.json"
        self._cache = None
    
    def get_pricing(self, force_refresh=False):
        if not self._cache or force_refresh:
            response = requests.get(self.url)
            response.raise_for_status()
            self._cache = response.json()
        return self._cache
    
    def get_model_price(self, model_name):
        pricing = self.get_pricing()
        for provider in pricing['models'].values():
            if model_name in provider:
                return provider[model_name]
        return None

# Usage
client = PricingClient()
price = client.get_model_price("gpt-4o")
print(f"GPT-4o: ${price['input']}/1M input, ${price['output']}/1M output")
```

### JavaScript/TypeScript

```javascript
const PRICING_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/ai-model-pricing/main/pricing/latest.json";

async function getPricing() {
  const response = await fetch(PRICING_URL);
  return await response.json();
}

async function calculateCost(modelName, inputTokens, outputTokens) {
  const pricing = await getPricing();
  
  for (const provider of Object.values(pricing.models)) {
    if (modelName in provider) {
      const model = provider[modelName];
      const inputCost = (inputTokens / 1_000_000) * model.input;
      const outputCost = (outputTokens / 1_000_000) * model.output;
      return inputCost + outputCost;
    }
  }
  return null;
}

// Usage
const cost = await calculateCost("gpt-4o", 1500, 500);
console.log(`Cost: $${cost.toFixed(6)}`);
```

### Curl

```bash
# Fetch pricing
curl -s https://raw.githubusercontent.com/YOUR_USERNAME/ai-model-pricing/main/pricing/latest.json | jq '.models.openai."gpt-4o"'

# Output:
# {
#   "input": 2.50,
#   "output": 10.00,
#   "description": "GPT-4o"
# }
```

## 📈 Pricing History

Each commit to `pricing/latest.json` creates a historical record. To see pricing changes over time:

```bash
git log -p pricing/latest.json
```

## ⚠️ Disclaimer

This is an unofficial project and is not affiliated with OpenAI or Anthropic. Pricing data is scraped from public sources and provided as-is. Always verify pricing with official sources before making business decisions.

**No Warranty**: This data is provided without warranty. Scraping may fail, and data may be outdated. Use at your own risk.

## 📜 License

MIT License - See [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for their pricing transparency
- Anthropic for their clear documentation
- The open-source community

## 📧 Contact

For questions or issues, please open a GitHub issue.

---

**Star ⭐ this repo if you find it useful!**

Last updated: 2025-11-19

