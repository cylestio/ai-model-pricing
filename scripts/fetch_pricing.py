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


# File paths
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
PRICING_FILE = REPO_ROOT / "pricing" / "latest.json"


def fetch_openai_pricing() -> Optional[Dict]:
    """
    Fetch OpenAI pricing from their pricing page.
    
    Note: OpenAI often blocks automated scraping with 403 errors.
    This is expected and the script will fall back gracefully.
    """
    try:
        print("Fetching OpenAI pricing...")
        
        url = "https://openai.com/api/pricing/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
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
                                pricing_dict[model_name] = {
                                    "input": prices[0],
                                    "output": prices[1],
                                    "description": model_name.upper()
                                }
                    except Exception:
                        continue
        
        if pricing_dict:
            print(f"✓ OpenAI: Found {len(pricing_dict)} models")
            return pricing_dict
        else:
            print("⚠ OpenAI: No pricing data found")
            return None
            
    except requests.RequestException as e:
        print(f"⚠ OpenAI: Failed to fetch ({e})")
        return None
    except Exception as e:
        print(f"⚠ OpenAI: Error parsing ({e})")
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
        
        # Try to find tables with pricing
        tables = soup.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            if not rows:
                continue
                
            header_row = rows[0]
            headers = [h.get_text(strip=True).lower() for h in header_row.find_all(['th', 'td'])]
            
            # Find column indices
            model_col = next((i for i, h in enumerate(headers) if 'model' in h or 'name' in h), 0)
            input_col = next((i for i, h in enumerate(headers) if 'input' in h), None)
            output_col = next((i for i, h in enumerate(headers) if 'output' in h), None)
            
            for row in rows[1:]:
                cells = row.find_all(['td', 'th'])
                if len(cells) > model_col:
                    try:
                        model_text = cells[model_col].get_text(strip=True).lower()
                        
                        if 'claude' in model_text:
                            # Normalize model name
                            model_name = re.sub(r'\s+', '-', model_text)
                            
                            # Extract prices
                            input_price = None
                            output_price = None
                            
                            if input_col and input_col < len(cells):
                                input_text = cells[input_col].get_text(strip=True)
                                input_match = re.search(r'\$?([\d.]+)', input_text)
                                if input_match and input_match.group(1) != '.':
                                    input_price = float(input_match.group(1))
                            
                            if output_col and output_col < len(cells):
                                output_text = cells[output_col].get_text(strip=True)
                                output_match = re.search(r'\$?([\d.]+)', output_text)
                                if output_match and output_match.group(1) != '.':
                                    output_price = float(output_match.group(1))
                            
                            # Fallback: try to extract from any cell
                            if input_price is None or output_price is None:
                                prices = []
                                for cell in cells:
                                    price_match = re.search(r'\$?([\d.]+)', cell.get_text(strip=True))
                                    if price_match and price_match.group(1) != '.':
                                        try:
                                            price = float(price_match.group(1))
                                            if 0 < price < 1000:
                                                prices.append(price)
                                        except ValueError:
                                            pass
                                
                                if len(prices) >= 2:
                                    input_price = prices[0]
                                    output_price = prices[1]
                            
                            if input_price and output_price:
                                # Create nice description
                                description = model_text.replace('-', ' ').title()
                                pricing_dict[model_name] = {
                                    "input": input_price,
                                    "output": output_price,
                                    "description": description
                                }
                    
                    except Exception:
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
            "openai": "https://openai.com/api/pricing/",
            "anthropic": "https://docs.anthropic.com/en/docs/about-claude/models"
        },
        "models": {}
    }
    
    # Merge fetched data with existing data as fallback
    if openai_pricing:
        new_pricing["models"]["openai"] = openai_pricing
    elif existing_pricing and "openai" in existing_pricing.get("models", {}):
        print("Using existing OpenAI pricing (fetch failed)")
        new_pricing["models"]["openai"] = existing_pricing["models"]["openai"]
    
    if anthropic_pricing:
        new_pricing["models"]["anthropic"] = anthropic_pricing
    elif existing_pricing and "anthropic" in existing_pricing.get("models", {}):
        print("Using existing Anthropic pricing (fetch failed)")
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
        
        if args.force or input("Save updated pricing? (y/N): ").strip().lower() == 'y' or True:  # Auto-yes for CI
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

