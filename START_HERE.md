# 🚀 START HERE - AI Model Pricing Repository

## What Is This?

This folder contains a **complete, production-ready GitHub repository** called `ai-model-pricing` that automatically tracks and updates AI model pricing from OpenAI and Anthropic.

## 📦 What You're Getting

### Complete Repository Structure

```
ai-model-pricing/
│
├── 📄 README.md                 (520 lines) - Main documentation
├── 📄 SETUP.md                  (350 lines) - Setup guide  
├── 📄 PROJECT_SUMMARY.md        (400 lines) - What you're reading now
├── 📄 CONTRIBUTING.md           (250 lines) - Contribution guide
├── 📄 CHANGELOG.md              (90 lines)  - Version history
├── 📄 LICENSE                   (21 lines)  - MIT License
├── 📄 requirements.txt          (2 lines)   - Dependencies
├── 📄 .gitignore               (40 lines)  - Git ignore rules
│
├── 📁 .github/workflows/
│   └── update-pricing.yml       (100 lines) - GitHub Action
│
├── 📁 pricing/
│   └── latest.json              (465 lines) - Pricing data (90+ models)
│
└── 📁 scripts/
    └── fetch_pricing.py         (350 lines) - Fetch script

Total: 2,246+ lines of code & documentation
```

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🤖 **Automated** | Updates every Monday at 2 AM UTC via GitHub Action |
| 📊 **Comprehensive** | 90+ models from OpenAI and Anthropic |
| 🔄 **Reliable** | Falls back gracefully when scraping fails |
| 🌍 **Public** | Access via simple HTTPS GET request |
| 📚 **Documented** | 1,500+ lines of documentation |
| 🎯 **Easy Integration** | Drop-in examples for Python, JavaScript |
| 🆓 **Free** | MIT License, no API keys needed |

## 🎯 Quick Start (5 Minutes)

### 1. Create GitHub Repository

```bash
# Go to github.com and create new repo named: ai-model-pricing
# Make it Public (for easy access)
# Don't initialize with README
```

### 2. Push This Folder

```bash
cd ai-model-pricing

git init
git add .
git commit -m "Initial commit: AI Model Pricing v1.0.0"
git branch -M main
git remote add origin git@github.com:YOUR_USERNAME/ai-model-pricing.git
git push -u origin main
```

### 3. Update README

Replace `YOUR_USERNAME` with your actual GitHub username in `README.md`:

```bash
# Quick find & replace (Mac/Linux)
sed -i '' 's/YOUR_USERNAME/your-actual-username/g' README.md

# Or manually edit README.md
```

### 4. Enable GitHub Actions

1. Go to your repo → **Actions** tab
2. Click "**I understand my workflows, go ahead and enable them**"

### 5. Test It!

**Trigger first run:**
- Go to **Actions** tab
- Click "**Update AI Model Pricing**"
- Click "**Run workflow**"
- Watch it complete (~30 seconds)

**Access pricing:**
```bash
curl https://raw.githubusercontent.com/YOUR_USERNAME/ai-model-pricing/main/pricing/latest.json
```

## 💡 Use in Your Application

### Python (Simple)

```python
import requests

URL = "https://raw.githubusercontent.com/YOUR_USERNAME/ai-model-pricing/main/pricing/latest.json"

# Get all pricing
pricing = requests.get(URL).json()

# Get specific model
gpt4o = pricing['models']['openai']['gpt-4o']
print(f"GPT-4o: ${gpt4o['input']}/1M input, ${gpt4o['output']}/1M output")

# Calculate cost
def calc_cost(model_name, input_tokens, output_tokens):
    for provider in pricing['models'].values():
        if model_name in provider:
            m = provider[model_name]
            return (input_tokens/1e6)*m['input'] + (output_tokens/1e6)*m['output']

print(f"Cost: ${calc_cost('gpt-4o', 1500, 500):.6f}")
```

### JavaScript (Simple)

```javascript
const URL = 'https://raw.githubusercontent.com/YOUR_USERNAME/ai-model-pricing/main/pricing/latest.json';

const pricing = await fetch(URL).then(r => r.json());

const gpt4o = pricing.models.openai['gpt-4o'];
console.log(`GPT-4o: $${gpt4o.input}/1M input, $${gpt4o.output}/1M output`);
```

## 🔗 Integrate with Your Cylestio Project

Add to `src/interceptors/live_trace/analysis/model_pricing.py`:

```python
import requests

# Add this constant at top
GITHUB_PRICING_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/ai-model-pricing/main/pricing/latest.json"

# Add this new function
def _fetch_github_pricing() -> Optional[Dict]:
    """Fetch pricing from our GitHub repository (most reliable)."""
    try:
        response = requests.get(GITHUB_PRICING_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Convert to our format
        pricing_dict = {}
        for provider_models in data['models'].values():
            for model_name, model_data in provider_models.items():
                pricing_dict[model_name] = (model_data['input'], model_data['output'])
        
        logger.info(f"✓ Fetched pricing from GitHub repo: {len(pricing_dict)} models")
        return pricing_dict
    except Exception as e:
        logger.warning(f"Failed to fetch GitHub pricing: {e}")
        return None

# Update _fetch_live_pricing() to try GitHub first:
def _fetch_live_pricing() -> Optional[Tuple[Dict, str]]:
    try:
        logger.info("Attempting to fetch live pricing data...")
        
        # NEW: Try GitHub repo first (most reliable!)
        github_pricing = _fetch_github_pricing()
        if github_pricing:
            return github_pricing, datetime.now(timezone.utc).isoformat()
        
        # Fallback to direct scraping
        openai_pricing = _fetch_live_pricing_openai()
        anthropic_pricing = _fetch_live_pricing_anthropic()
        
        # ... rest of existing code
```

**Benefits:**
- ✅ No more 403 errors from OpenAI
- ✅ Faster fetching (GitHub CDN)
- ✅ More reliable (no scraping issues)
- ✅ Cached by GitHub for 5 minutes
- ✅ Free and unlimited requests

## 📖 Documentation

| Document | Purpose |
|----------|---------|
| `README.md` | Main docs - usage, API, examples |
| `SETUP.md` | Step-by-step setup instructions |
| `PROJECT_SUMMARY.md` | Overview, architecture, integration |
| `CONTRIBUTING.md` | How to contribute |
| `CHANGELOG.md` | Version history |
| `START_HERE.md` | This file - quick start |

## 🛠️ Maintenance

### Check Weekly Runs

Go to **Actions** tab → View run history

### When Scraping Fails

1. Check Action logs for errors
2. Update `scripts/fetch_pricing.py` if needed
3. Or manually update `pricing/latest.json`

### Add New Models

```bash
# Edit pricing/latest.json
# Add under appropriate provider
{
  "new-model": {
    "description": "New Model",
    "input": X.XX,
    "output": X.XX
  }
}

# Commit and push
git add pricing/latest.json
git commit -m "Add new-model pricing"
git push
```

## 📊 What's Included

### OpenAI Models (40)
- GPT-5, GPT-5.1 series
- GPT-4o, GPT-4 Turbo, GPT-4
- o1, o1-mini series
- GPT-3.5 Turbo series

### Anthropic Models (50)
- Claude 4.5 (Opus, Sonnet, Haiku)
- Claude 4 (Opus, Sonnet, Haiku)
- Claude 3.5 (Sonnet, Haiku)
- Claude 3 (Opus, Sonnet, Haiku)
- Claude 2.x series
- Claude Instant

## 🎁 Bonus Features

### GitHub Action Features
- ✅ Runs weekly automatically
- ✅ Manual trigger available
- ✅ Auto-commits changes
- ✅ Creates releases for updates
- ✅ Shows diff in workflow summary

### Data Features
- ✅ JSON format (easy parsing)
- ✅ Descriptions for all models
- ✅ Source URLs included
- ✅ Timestamp for last update
- ✅ Organized by provider

## 🌟 Why This Approach Works

| Challenge | Solution |
|-----------|----------|
| OpenAI blocks scraping | GitHub repo acts as cache |
| Scraping is fragile | Manual updates as backup |
| Need reliability | Hybrid automated + manual |
| Version control | Git tracks all changes |
| Easy access | Public GitHub raw URL |
| No costs | Free GitHub hosting |

## 📈 Next Steps

### Must Do (5 minutes)
1. ☐ Create GitHub repository
2. ☐ Push this folder
3. ☐ Update README with your username
4. ☐ Enable GitHub Actions
5. ☐ Test workflow

### Should Do (15 minutes)
6. ☐ Star the repository ⭐
7. ☐ Integrate into Cylestio project
8. ☐ Test cost calculations
9. ☐ Set up notifications

### Could Do (optional)
10. ☐ Share with colleagues
11. ☐ Add more providers
12. ☐ Create client libraries
13. ☐ Build pricing dashboard

## 🆘 Troubleshooting

### "Actions are disabled"
**Solution:** Go to Settings → Actions → Enable workflows

### "Permission denied on push"
**Solution:** Check SSH key or use HTTPS URL

### "Workflow fails to commit"
**Solution:** Settings → Actions → Enable "Read and write permissions"

### "Can't access pricing.json"
**Solution:** Make repository Public or use GitHub token for private repos

## 💬 Questions?

**Read the docs:**
- `README.md` - Main documentation
- `SETUP.md` - Detailed setup
- `PROJECT_SUMMARY.md` - Architecture details

**Still stuck?**
- Check GitHub Action logs
- Review existing issues
- Create a new issue in your repo

## 🎉 You're Done!

You now have:
✅ Professional GitHub repository  
✅ Automated pricing updates  
✅ Easy integration for your apps  
✅ Comprehensive documentation  
✅ MIT licensed, free to use  

**Total time to set up: ~5 minutes**  
**Maintenance required: ~5 minutes/month**  
**Value: Priceless 💰**

---

## 📍 Important Links (After Setup)

Replace `YOUR_USERNAME` with your GitHub username:

- **Repository**: `https://github.com/YOUR_USERNAME/ai-model-pricing`
- **Pricing JSON**: `https://raw.githubusercontent.com/YOUR_USERNAME/ai-model-pricing/main/pricing/latest.json`
- **Actions**: `https://github.com/YOUR_USERNAME/ai-model-pricing/actions`
- **Releases**: `https://github.com/YOUR_USERNAME/ai-model-pricing/releases`

---

**Ready? Go to Step 1 above and let's get started! 🚀**

