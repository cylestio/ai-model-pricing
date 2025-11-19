#!/usr/bin/env python3
"""
Fetch latest AI model pricing from OpenAI and Anthropic.

This script scrapes official pricing pages and updates the pricing/latest.json file.
It compares with existing data and only updates if changes are detected.
"""

import json
import re
import sys
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional, Tuple

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: Required packages not installed")
    print("Run: pip install requests beautifulsoup4")
    sys.exit(1)

# Try to import cloudscraper for bypassing Cloudflare
try:
    import cloudscraper
    HAS_CLOUDSCRAPER = True
except ImportError:
    HAS_CLOUDSCRAPER = False


# File paths
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
PRICING_FILE = REPO_ROOT / "latest.json"


def fetch_openai_pricing() -> Optional[Dict]:
    """
    Fetch OpenAI pricing from their pricing page.
    
    Note: OpenAI uses Cloudflare protection and often blocks automated scraping.
    When this happens, the script will gracefully fall back to existing data.
    """
    try:
        print("Fetching OpenAI pricing...")
        
        # Try the API docs pricing page
        url = "https://platform.openai.com/docs/pricing"
        
        # Try cloudscraper first if available (bypasses Cloudflare)
        if HAS_CLOUDSCRAPER:
            try:
                print("  Using cloudscraper to bypass Cloudflare...")
                scraper = cloudscraper.create_scraper(
                    browser={
                        'browser': 'chrome',
                        'platform': 'darwin',
                        'desktop': True
                    }
                )
                response = scraper.get(url, timeout=30)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    pricing_dict = _parse_openai_pricing(soup)
                    if pricing_dict:
                        return pricing_dict
                    else:
                        print("⚠ OpenAI: No pricing data found (page format may have changed)")
                        return None
                else:
                    print(f"⚠ OpenAI: cloudscraper returned status {response.status_code}")
            except Exception as e:
                print(f"⚠ OpenAI: cloudscraper failed ({e})")
        else:
            print("  ℹ cloudscraper not installed (pip install cloudscraper)")
        
        # Fall back to regular requests
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        
        response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        
        # Check for Cloudflare or other blocks
        if response.status_code == 403:
            print("⚠ OpenAI: Blocked by Cloudflare (403)")
            if not HAS_CLOUDSCRAPER:
                print("  💡 Try: pip install cloudscraper")
            return None
        
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        pricing_dict = _parse_openai_pricing(soup)
        
        if pricing_dict:
            return pricing_dict
        else:
            print("⚠ OpenAI: No pricing data found (page format may have changed)")
            return None
            
    except requests.RequestException as e:
        if '403' in str(e):
            print(f"⚠ OpenAI: Blocked by Cloudflare protection")
        else:
            print(f"⚠ OpenAI: Failed to fetch ({e})")
        return None
    except Exception as e:
        print(f"⚠ OpenAI: Error parsing ({e})")
        return None


def _parse_openai_pricing(soup: BeautifulSoup) -> Optional[Dict]:
    """Parse OpenAI pricing from BeautifulSoup object."""
    pricing_dict = {}
    
    # Try to extract from tables
    tables = soup.find_all('table')
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 3:
                try:
                    cell_texts = [cell.get_text(strip=True) for cell in cells]
                    
                    # Look for model names (gpt- or o1)
                    model_name = None
                    for text in cell_texts:
                        text_lower = text.lower()
                        if text_lower.startswith('gpt-') or text_lower.startswith('o1'):
                            model_name = text_lower
                            break
                    
                    if model_name:
                        # Extract prices
                        prices = []
                        for text in cell_texts:
                            price_match = re.search(r'\$?([\d.]+)', text)
                            if price_match:
                                try:
                                    price = float(price_match.group(1))
                                    if 0 < price < 1000:
                                        prices.append(price)
                                except ValueError:
                                    pass
                        
                        if len(prices) >= 2:
                            # Create a nice description
                            desc = model_name.upper()
                            pricing_dict[model_name] = {
                                "input": prices[0],
                                "output": prices[1],
                                "description": desc
                            }
                except Exception:
                    continue
    
    if pricing_dict:
        print(f"✓ OpenAI: Found {len(pricing_dict)} models")
        return pricing_dict
    
    return None


def fetch_anthropic_pricing() -> Optional[Dict]:
    """Fetch Anthropic pricing from their documentation."""
    try:
        print("Fetching Anthropic pricing...")
        
        url = "https://docs.anthropic.com/en/docs/about-claude/models"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        pricing_dict = {}
        
        # Find all tables - we want the second one which has the pricing
        tables = soup.find_all('table')
        if len(tables) < 2:
            print("⚠ Anthropic: Could not find pricing table")
            return None
        
        # Use the second table (index 1) which contains the pricing info
        pricing_table = tables[1]
        rows = pricing_table.find_all('tr')
        
        if len(rows) < 6:
            print("⚠ Anthropic: Pricing table format unexpected")
            return None
        
        # Row 0: Model names (Claude Sonnet 4, Claude Opus 4, etc.)
        # Row 1: Claude API IDs
        # Row 5: Pricing info
        header_cells = rows[0].find_all(['th', 'td'])
        api_id_cells = rows[1].find_all(['td', 'th'])
        pricing_cells = rows[5].find_all(['td', 'th'])
        
        # Skip the first column which is the row label
        for i in range(1, len(header_cells)):
            try:
                model_name = header_cells[i].get_text(strip=True)
                
                # Skip if no model name
                if not model_name or 'claude' not in model_name.lower():
                    continue
                
                # Get the API ID (the canonical model identifier)
                if i < len(api_id_cells):
                    api_id_text = api_id_cells[i].get_text(strip=True)
                    # Remove "Copied!" suffix if present
                    api_id = re.sub(r'Copied!$', '', api_id_text).strip()
                else:
                    api_id = None
                
                # Get pricing (format: "$3 / input MTok$15 / output MTok")
                if i < len(pricing_cells):
                    pricing_text = pricing_cells[i].get_text(strip=True)
                    
                    # Extract input and output prices
                    # Pattern: $X / input MTok$Y / output MTok
                    matches = re.findall(r'\$?([\d.]+)\s*/\s*(?:input|output)\s*MTok', pricing_text)
                    
                    if len(matches) >= 2:
                        input_price = float(matches[0])
                        output_price = float(matches[1])
                        
                        # Use the API ID as the key if available, otherwise use normalized model name
                        if api_id:
                            model_key = api_id
                        else:
                            model_key = model_name.lower().replace(' ', '-')
                        
                        # Create entry with both the API ID and a friendly name
                        pricing_dict[model_key] = {
                            "input": input_price,
                            "output": output_price,
                            "description": model_name
                        }
                        
                        # Also add common aliases
                        if api_id and '-20' in api_id:  # Dated version like claude-sonnet-4-20250514
                            # Add version without date (e.g., claude-sonnet-4)
                            base_name = re.sub(r'-\d{8}$', '', api_id)
                            if base_name != api_id:
                                pricing_dict[base_name] = {
                                    "input": input_price,
                                    "output": output_price,
                                    "description": f"{model_name} (latest)"
                                }
            
            except Exception as e:
                # Skip this column if there's an error
                continue
        
        if pricing_dict:
            print(f"✓ Anthropic: Found {len(pricing_dict)} models")
            return pricing_dict
        else:
            print("⚠ Anthropic: No pricing data found")
            return None
            
    except requests.RequestException as e:
        print(f"⚠ Anthropic: Failed to fetch ({e})")
        return None
    except Exception as e:
        print(f"⚠ Anthropic: Error parsing ({e})")
        return None


def load_existing_pricing() -> Optional[Dict]:
    """Load existing pricing from JSON file."""
    if PRICING_FILE.exists():
        try:
            with open(PRICING_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠ Warning: Failed to load existing pricing: {e}")
    return None


def validate_pricing_data(pricing_dict: Dict, provider: str, existing_count: int = 0) -> bool:
    """
    Validate that pricing data looks reasonable before accepting it.
    
    Args:
        pricing_dict: The pricing data to validate
        provider: Provider name (for logging)
        existing_count: Number of existing models (if any)
    
    Returns:
        True if data looks valid, False otherwise
    """
    if not pricing_dict or not isinstance(pricing_dict, dict):
        return False
    
    # Check minimum number of models (at least 3)
    if len(pricing_dict) < 3:
        print(f"⚠ {provider}: Too few models ({len(pricing_dict)}) - data may be corrupted")
        return False
    
    # Validate each model has required fields and reasonable values
    valid_models = 0
    for model_name, model_data in pricing_dict.items():
        if not isinstance(model_data, dict):
            continue
        
        input_price = model_data.get('input')
        output_price = model_data.get('output')
        
        # Check that prices exist and are reasonable
        if isinstance(input_price, (int, float)) and isinstance(output_price, (int, float)):
            if 0 < input_price < 1000 and 0 < output_price < 1000:
                valid_models += 1
    
    # At least 80% of models should have valid pricing
    if valid_models < len(pricing_dict) * 0.8:
        print(f"⚠ {provider}: Only {valid_models}/{len(pricing_dict)} models have valid pricing")
        return False
    
    # If all models look valid but count is lower than existing, warn but accept
    # (Provider may have deprecated old models)
    if existing_count > 0 and len(pricing_dict) < existing_count:
        print(f"ℹ {provider}: Found {len(pricing_dict)} models (down from {existing_count}) - provider may have deprecated old models")
    
    return True


def compare_pricing(old: Dict, new: Dict) -> Tuple[bool, list]:
    """
    Compare old and new pricing data.
    Returns (has_changes, list_of_changes)
    """
    changes = []
    
    if not old:
        return True, ["Initial pricing data created"]
    
    old_models = old.get('models', {})
    new_models = new.get('models', {})
    
    # Check for new providers
    for provider in new_models:
        if provider not in old_models:
            changes.append(f"New provider: {provider}")
    
    # Check for removed providers
    for provider in old_models:
        if provider not in new_models:
            changes.append(f"Removed provider: {provider}")
    
    # Check models within each provider
    for provider, models in new_models.items():
        if provider not in old_models:
            continue
            
        old_provider_models = old_models[provider]
        
        for model_name, model_data in models.items():
            if model_name not in old_provider_models:
                changes.append(f"New model: {provider}/{model_name}")
            else:
                old_model = old_provider_models[model_name]
                if old_model.get('input') != model_data.get('input'):
                    changes.append(
                        f"Price change: {provider}/{model_name} input "
                        f"${old_model.get('input')} → ${model_data.get('input')}"
                    )
                if old_model.get('output') != model_data.get('output'):
                    changes.append(
                        f"Price change: {provider}/{model_name} output "
                        f"${old_model.get('output')} → ${model_data.get('output')}"
                    )
        
        # Check for removed models
        for model_name in old_provider_models:
            if model_name not in models:
                changes.append(f"Removed model: {provider}/{model_name}")
    
    return len(changes) > 0, changes


def save_pricing(pricing_data: Dict) -> bool:
    """Save pricing data to JSON file."""
    try:
        PRICING_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(PRICING_FILE, 'w') as f:
            json.dump(pricing_data, f, indent=2, sort_keys=True)
        return True
    except Exception as e:
        print(f"✗ Error: Failed to save pricing: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Fetch AI model pricing')
    parser.add_argument('--force', action='store_true', 
                       help='Force update even if no changes detected')
    parser.add_argument('--verbose', action='store_true',
                       help='Verbose output')
    args = parser.parse_args()
    
    print("=" * 70)
    print("AI Model Pricing Fetcher")
    print("=" * 70)
    print()
    
    # Load existing pricing
    existing_pricing = load_existing_pricing()
    if existing_pricing:
        print(f"Loaded existing pricing (last updated: {existing_pricing.get('last_updated', 'unknown')})")
    else:
        print("No existing pricing found - will create new file")
    print()
    
    # Fetch new pricing
    openai_pricing = fetch_openai_pricing()
    anthropic_pricing = fetch_anthropic_pricing()
    
    print()
    
    # Validate fetched data before using it
    existing_models = existing_pricing.get("models", {}) if existing_pricing else {}
    
    # Validate OpenAI data
    if openai_pricing:
        existing_openai_count = len(existing_models.get("openai", {}))
        if not validate_pricing_data(openai_pricing, "OpenAI", existing_openai_count):
            print("⚠ OpenAI: Fetched data failed validation - will use existing data")
            openai_pricing = None
    
    # Validate Anthropic data
    if anthropic_pricing:
        existing_anthropic_count = len(existing_models.get("anthropic", {}))
        if not validate_pricing_data(anthropic_pricing, "Anthropic", existing_anthropic_count):
            print("⚠ Anthropic: Fetched data failed validation - will use existing data")
            anthropic_pricing = None
    
    # If both failed and we have existing data, keep it
    if not openai_pricing and not anthropic_pricing:
        print("✗ Failed to fetch any pricing data")
        if existing_pricing:
            print("✓ Keeping existing pricing data")
            return 0
        else:
            print("✗ No existing pricing data available")
            return 1
    
    # Build new pricing structure
    new_pricing = {
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "sources": {
            "openai": "https://platform.openai.com/docs/pricing",
            "anthropic": "https://docs.anthropic.com/en/docs/about-claude/models"
        },
        "models": {}
    }
    
    # Merge fetched data with existing data as fallback
    if openai_pricing:
        new_pricing["models"]["openai"] = openai_pricing
    elif existing_pricing and "openai" in existing_pricing.get("models", {}):
        print("Using existing OpenAI pricing (fetch failed or invalid)")
        new_pricing["models"]["openai"] = existing_pricing["models"]["openai"]
    
    if anthropic_pricing:
        new_pricing["models"]["anthropic"] = anthropic_pricing
    elif existing_pricing and "anthropic" in existing_pricing.get("models", {}):
        print("Using existing Anthropic pricing (fetch failed or invalid)")
        new_pricing["models"]["anthropic"] = existing_pricing["models"]["anthropic"]
    
    # Compare with existing
    has_changes, changes = compare_pricing(existing_pricing, new_pricing)
    
    print()
    print("=" * 70)
    if has_changes:
        print("Changes detected:")
        print("-" * 70)
        for change in changes:
            print(f"  • {change}")
        print()
        
        # Auto-save if forced, otherwise ask for confirmation
        should_save = args.force
        if not should_save:
            try:
                response = input("Save updated pricing? (y/N): ").strip().lower()
                should_save = response == 'y'
            except (EOFError, KeyboardInterrupt):
                # Non-interactive mode or user cancelled
                print("\nNo response - skipping save")
                should_save = False
        
        if should_save:
            if save_pricing(new_pricing):
                print("✓ Pricing updated successfully")
                
                # Output for GitHub Actions
                if len(changes) > 0:
                    print(f"\n::set-output name=changes::true")
                    print(f"::set-output name=change_count::{len(changes)}")
                
                return 0
            else:
                return 1
        else:
            print("✗ Update cancelled")
            return 0
    else:
        print("No changes detected - pricing is up to date")
        if args.force:
            print("Forcing update anyway...")
            if save_pricing(new_pricing):
                print("✓ Pricing updated")
                return 0
            else:
                return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

