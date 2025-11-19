# AI Model Pricing - Project Summary

## 🎯 Project Name

**`ai-model-pricing`** - A GitHub repository for tracking AI model pricing from OpenAI and Anthropic.

## 📦 What's Included

This folder contains a complete, ready-to-publish GitHub repository with:

### Core Files

```
ai-model-pricing/
├── README.md                    # Main documentation (comprehensive)
├── LICENSE                      # MIT License
├── SETUP.md                     # Step-by-step setup guide
├── CONTRIBUTING.md              # Contribution guidelines
├── CHANGELOG.md                 # Version history
├── requirements.txt             # Python dependencies
├── .gitignore                   # Git ignore rules
│
├── .github/
│   └── workflows/
│       └── update-pricing.yml   # GitHub Action (weekly updates)
│
├── pricing/
│   └── latest.json              # Current pricing data (90+ models)
│
└── scripts/
    └── fetch_pricing.py         # Pricing fetch script
```

### Key Features

✅ **90+ AI Models Tracked**
   - OpenAI: GPT-3.5, GPT-4, GPT-4o, GPT-5, o1 series
   - Anthropic: Claude 2, 3, 3.5, 4, 4.5 (all variants)

✅ **Automated Updates**
   - GitHub Action runs every Monday at 2 AM UTC
   - Can be manually triggered anytime
   - Auto-commits pricing changes

✅ **Easy Integration**
   - Fetch JSON directly from GitHub raw URL
   - No API keys needed
   - Examples for Python, JavaScript, Curl

✅ **Professional Documentation**
   - Comprehensive README with examples
   - Setup guide
   - Contributing guidelines
   - Change log

## 🚀 How to Use

### Step 1: Create GitHub Repository

1. Go to GitHub.com
2. Click "New repository"
3. Name it: `ai-model-pricing`
4. Make it **Public** (for easy access)
5. **Don't** initialize with README
6. Click "Create repository"

### Step 2: Push This Folder

```bash
cd ai-model-pricing

# Initialize git
git init
git add .
git commit -m "Initial commit: AI Model Pricing v1.0.0"

# Connect to your GitHub repo (replace YOUR_USERNAME)
git branch -M main
git remote add origin git@github.com:YOUR_USERNAME/ai-model-pricing.git
git push -u origin main
```

### Step 3: Update URLs in README

Replace `YOUR_USERNAME` in `README.md` with your actual GitHub username:
- Line 3: Badge URL
- Line 21: Direct URL example
- Line 29: PRICING_URL constant
- Line 161: Direct URL
- Multiple places in usage examples

**Quick find & replace:**
```bash
# On Mac/Linux
sed -i '' 's/YOUR_USERNAME/your-actual-username/g' README.md

# Or manually edit README.md
```

### Step 4: Enable GitHub Actions

1. Go to your repository on GitHub
2. Click "Actions" tab
3. Click "I understand my workflows, go ahead and enable them"

### Step 5: Test It!

**Trigger first update:**
1. Go to Actions tab
2. Click "Update AI Model Pricing"
3. Click "Run workflow" → "Run workflow"
4. Watch it run (takes ~30 seconds)

**Access pricing data:**
```bash
curl https://raw.githubusercontent.com/YOUR_USERNAME/ai-model-pricing/main/pricing/latest.json
```

## 💡 Integration Examples

### In Your Python Application

```python
import requests

PRICING_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/ai-model-pricing/main/pricing/latest.json"

def get_pricing():
    return requests.get(PRICING_URL).json()

# Get pricing for a model
pricing = get_pricing()
gpt4o = pricing['models']['openai']['gpt-4o']
print(f"GPT-4o: ${gpt4o['input']}/1M input, ${gpt4o['output']}/1M output")

# Calculate cost
def calculate_cost(model_name, input_tokens, output_tokens):
    pricing = get_pricing()
    for provider in pricing['models'].values():
        if model_name in provider:
            model = provider[model_name]
            return (input_tokens/1_000_000)*model['input'] + (output_tokens/1_000_000)*model['output']

cost = calculate_cost("gpt-4o", 1500, 500)
print(f"Cost: ${cost:.6f}")
```

### Update Your Cylestio Perimeter Project

Edit `src/interceptors/live_trace/analysis/model_pricing.py`:

```python
# Add at top
import requests

REMOTE_PRICING_URL = "https://raw.githubusercontent.com/YOUR_USERNAME/ai-model-pricing/main/pricing/latest.json"

def _fetch_remote_pricing() -> Optional[Dict]:
    """Fetch pricing from GitHub repository."""
    try:
        response = requests.get(REMOTE_PRICING_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Convert to expected format
        pricing_dict = {}
        for provider_models in data['models'].values():
            for model_name, model_data in provider_models.items():
                pricing_dict[model_name] = (model_data['input'], model_data['output'])
        
        return pricing_dict
    except Exception as e:
        logger.warning(f"Failed to fetch remote pricing: {e}")
        return None

# Update _fetch_live_pricing() to try remote first
def _fetch_live_pricing() -> Optional[Tuple[Dict, str]]:
    """Attempt to fetch live pricing data from all sources."""
    try:
        logger.info("Attempting to fetch live pricing data...")
        
        # Try GitHub repo first (most reliable)
        remote_pricing = _fetch_remote_pricing()
        if remote_pricing:
            logger.info(f"✓ Fetched pricing from GitHub repo")
            return remote_pricing, datetime.now(timezone.utc).isoformat()
        
        # Fall back to scraping
        openai_pricing = _fetch_live_pricing_openai()
        anthropic_pricing = _fetch_live_pricing_anthropic()
        # ... rest of existing code
```

## 📊 Data Format

The `pricing/latest.json` file contains:

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
      }
    },
    "anthropic": {
      "claude-3-5-sonnet-20241022": {
        "input": 3.00,
        "output": 15.00,
        "description": "Claude 3.5 Sonnet (2024-10-22)"
      }
    }
  }
}
```

**All prices are in USD per 1 million tokens.**

## 🔄 How It Works

### Automated Workflow

```
Monday 2 AM UTC
    ↓
GitHub Action runs
    ↓
├─→ Fetch OpenAI pricing (may fail - 403 blocked)
├─→ Fetch Anthropic pricing (usually works)
    ↓
Compare with existing pricing
    ↓
    ├─ Changes found?
    │   ├─ Yes → Commit to repo
    │   │         Create release
    │   │         Update JSON
    │   └─ No  → No action
    ↓
Your app fetches from raw.githubusercontent.com
    ↓
Always up-to-date pricing!
```

### Fallback Strategy

1. **Primary**: GitHub Action weekly scraping
2. **Backup**: Manual updates when scraping fails
3. **Guarantee**: Comprehensive initial pricing (90+ models)

## 🛠️ Maintenance

### Weekly Check
- Go to Actions tab
- Review latest run
- Check if it succeeded

### When Scraping Breaks
1. Check Action logs
2. Update `scripts/fetch_pricing.py` if needed
3. Or manually update `pricing/latest.json`

### Adding New Models
```bash
# Edit pricing/latest.json
# Add new model entry
# Commit and push
git add pricing/latest.json
git commit -m "Add GPT-6 pricing"
git push
```

## ✨ Benefits

### For Your Application
✅ No scraping logic in your app  
✅ No risk of being blocked by providers  
✅ Simple HTTP GET request  
✅ Cached by GitHub CDN  
✅ Version controlled pricing history  

### For the Community
✅ Open source pricing data  
✅ Community can contribute updates  
✅ Transparent pricing changes  
✅ Reusable by other projects  

## 📈 Next Steps

### Immediate
- [ ] Create GitHub repository
- [ ] Push code
- [ ] Update README with your username
- [ ] Enable Actions
- [ ] Test workflow

### Soon
- [ ] Star the repository ⭐
- [ ] Update your Cylestio project to use it
- [ ] Share with colleagues
- [ ] Add more providers (Google AI, Cohere?)

### Optional
- [ ] Add Slack notifications
- [ ] Create pricing comparison tools
- [ ] Build historical pricing charts
- [ ] Package as npm/pip module

## 🔗 Useful Links

After creating your repository, these will work:

- **Repository**: `https://github.com/YOUR_USERNAME/ai-model-pricing`
- **Pricing Data**: `https://raw.githubusercontent.com/YOUR_USERNAME/ai-model-pricing/main/pricing/latest.json`
- **Actions**: `https://github.com/YOUR_USERNAME/ai-model-pricing/actions`
- **Releases**: `https://github.com/YOUR_USERNAME/ai-model-pricing/releases`

## 💬 Support

The repository includes:
- Comprehensive documentation
- Code comments
- Setup guide
- Contributing guidelines
- Issue templates (add via GitHub)

## 📜 License

MIT License - Free to use, modify, and distribute.

---

## Summary

You now have a **complete, professional GitHub repository** for AI model pricing that:

1. ✅ Automatically updates weekly
2. ✅ Can be manually triggered anytime
3. ✅ Provides easy JSON access
4. ✅ Falls back gracefully when scraping fails
5. ✅ Includes 90+ models out of the box
6. ✅ Is professionally documented
7. ✅ Can be integrated in minutes

**Next Step**: Follow the "How to Use" section above to publish it to GitHub!

Good luck! 🚀

