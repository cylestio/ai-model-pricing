# Setup Guide

This guide will help you set up the AI Model Pricing repository on GitHub.

## Quick Setup

### 1. Create GitHub Repository

1. Go to GitHub and create a new repository:
   - Name: `ai-model-pricing`
   - Description: "Always up-to-date pricing data for AI models from OpenAI and Anthropic"
   - Public repository (recommended for easy access)
   - Don't initialize with README (we already have one)

2. Copy this folder's contents to your new repo:
   ```bash
   cd ai-model-pricing
   git init
   git add .
   git commit -m "Initial commit: AI Model Pricing v1.0.0"
   git branch -M main
   git remote add origin git@github.com:YOUR_USERNAME/ai-model-pricing.git
   git push -u origin main
   ```

### 2. Update README

Replace `YOUR_USERNAME` with your GitHub username in:
- `README.md` (3 instances)
- Badge URLs
- Direct URLs to JSON file

### 3. Enable GitHub Actions

The repository includes a GitHub Action (`.github/workflows/update-pricing.yml`) that:
- Runs automatically every Monday at 2 AM UTC
- Can be triggered manually from the Actions tab
- Commits pricing updates automatically

**Enable it:**
1. Go to your repository on GitHub
2. Click "Actions" tab
3. Click "I understand my workflows, go ahead and enable them"

### 4. Test the Workflow

**Manual test:**
1. Go to Actions tab
2. Select "Update AI Model Pricing"
3. Click "Run workflow"
4. Watch it run (should complete in ~30 seconds)

### 5. Configure Permissions (if needed)

If the workflow fails to push commits:

1. Go to repository Settings
2. Click "Actions" → "General"
3. Scroll to "Workflow permissions"
4. Select "Read and write permissions"
5. Check "Allow GitHub Actions to create and approve pull requests"
6. Click "Save"

## Integration with Your Application

### Python Example

Create a helper module in your app:

```python
# pricing_client.py
import requests
from typing import Dict, Optional

class PricingClient:
    """Client for fetching AI model pricing."""
    
    def __init__(self, cache_ttl: int = 3600):
        self.url = "https://raw.githubusercontent.com/YOUR_USERNAME/ai-model-pricing/main/pricing/latest.json"
        self._cache = None
        self._cache_time = 0
        self._cache_ttl = cache_ttl
    
    def get_pricing(self, force_refresh: bool = False) -> Dict:
        """Get pricing data, using cache if available."""
        import time
        
        current_time = time.time()
        
        if not force_refresh and self._cache and (current_time - self._cache_time) < self._cache_ttl:
            return self._cache
        
        response = requests.get(self.url, timeout=10)
        response.raise_for_status()
        
        self._cache = response.json()
        self._cache_time = current_time
        
        return self._cache
    
    def get_model_price(self, model_name: str) -> Optional[Dict]:
        """Get price for a specific model."""
        pricing = self.get_pricing()
        
        for provider in pricing['models'].values():
            if model_name in provider:
                return provider[model_name]
        
        return None
    
    def calculate_cost(self, model_name: str, input_tokens: int, output_tokens: int) -> Optional[float]:
        """Calculate cost for an API call."""
        price = self.get_model_price(model_name)
        
        if not price:
            return None
        
        input_cost = (input_tokens / 1_000_000) * price['input']
        output_cost = (output_tokens / 1_000_000) * price['output']
        
        return input_cost + output_cost


# Usage in your app
client = PricingClient()

# Get pricing
price = client.get_model_price("gpt-4o")
print(f"GPT-4o: ${price['input']}/1M input, ${price['output']}/1M output")

# Calculate cost
cost = client.calculate_cost("gpt-4o", 1500, 500)
print(f"Cost: ${cost:.6f}")
```

### JavaScript/Node.js Example

```javascript
// pricing-client.js
const fetch = require('node-fetch');

class PricingClient {
  constructor(cacheTTL = 3600000) { // 1 hour in ms
    this.url = 'https://raw.githubusercontent.com/YOUR_USERNAME/ai-model-pricing/main/pricing/latest.json';
    this.cache = null;
    this.cacheTime = 0;
    this.cacheTTL = cacheTTL;
  }

  async getPricing(forceRefresh = false) {
    const currentTime = Date.now();
    
    if (!forceRefresh && this.cache && (currentTime - this.cacheTime) < this.cacheTTL) {
      return this.cache;
    }

    const response = await fetch(this.url);
    if (!response.ok) {
      throw new Error(`Failed to fetch pricing: ${response.statusText}`);
    }

    this.cache = await response.json();
    this.cacheTime = currentTime;

    return this.cache;
  }

  async getModelPrice(modelName) {
    const pricing = await this.getPricing();

    for (const provider of Object.values(pricing.models)) {
      if (modelName in provider) {
        return provider[modelName];
      }
    }

    return null;
  }

  async calculateCost(modelName, inputTokens, outputTokens) {
    const price = await this.getModelPrice(modelName);

    if (!price) return null;

    const inputCost = (inputTokens / 1_000_000) * price.input;
    const outputCost = (outputTokens / 1_000_000) * price.output;

    return inputCost + outputCost;
  }
}

// Usage
const client = new PricingClient();

(async () => {
  const price = await client.getModelPrice('gpt-4o');
  console.log(`GPT-4o: $${price.input}/1M input, $${price.output}/1M output`);

  const cost = await client.calculateCost('gpt-4o', 1500, 500);
  console.log(`Cost: $${cost.toFixed(6)}`);
})();
```

## Monitoring

### Check Action Runs

1. Go to Actions tab
2. View run history
3. Check for failures
4. Review pricing changes in commits

### Set Up Notifications

**Get notified of pricing changes:**

1. Watch the repository (top right)
2. Go to Settings → Notifications
3. Choose notification preferences

**Or use GitHub's RSS feed:**
```
https://github.com/YOUR_USERNAME/ai-model-pricing/commits/main.atom
```

## Maintenance

### When Scraping Breaks

If the GitHub Action fails to fetch pricing:

1. Check the Action logs for errors
2. Visit official pricing pages to see if structure changed
3. Update `scripts/fetch_pricing.py` scraping logic
4. Test locally: `python scripts/fetch_pricing.py --verbose`
5. Commit and push fixes

### Manually Update Pricing

If scraping is broken and you need to update prices:

1. Edit `pricing/latest.json` directly
2. Update the `last_updated` timestamp
3. Commit and push:
   ```bash
   git add pricing/latest.json
   git commit -m "Manual pricing update - [reason]"
   git push
   ```

### Add New Models

When new models are released:

1. Edit `pricing/latest.json`
2. Add model under appropriate provider
3. Use consistent format:
   ```json
   "model-name": {
     "description": "Model Name",
     "input": X.XX,
     "output": X.XX
   }
   ```
4. Commit and push

## Advanced Configuration

### Change Update Frequency

Edit `.github/workflows/update-pricing.yml`:

```yaml
schedule:
  # Daily at 2 AM UTC
  - cron: '0 2 * * *'
  
  # Or twice weekly (Monday and Thursday at 2 AM UTC)
  - cron: '0 2 * * 1,4'
```

### Disable Automatic Releases

Remove or comment out the "Create release" step in the workflow.

### Add Slack Notifications

Add this step to the workflow:

```yaml
- name: Notify Slack
  if: steps.fetch.outputs.has_changes == 'true'
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK }}
    payload: |
      {
        "text": "AI model pricing has been updated!"
      }
```

## Troubleshooting

### Action fails with permission error

**Solution:** Enable write permissions in Settings → Actions → Workflow permissions

### Pricing data looks wrong

**Solution:** Check official sources and update manually if needed

### Script times out

**Solution:** Increase timeout in `scripts/fetch_pricing.py` or `update-pricing.yml`

### No updates for weeks

**Solution:** Check Action is enabled and cron schedule is correct

## Getting Help

- Open an issue in your repository
- Check the main documentation in README.md
- Review existing issues and commits

## Next Steps

1. Star the repository ⭐
2. Share with others who might find it useful
3. Consider contributing improvements
4. Integrate into your applications

Enjoy always having up-to-date AI pricing data! 🎉

