# Contributing to AI Model Pricing

Thank you for your interest in contributing to AI Model Pricing! This document provides guidelines for contributing to the project.

## Ways to Contribute

### 1. Report Incorrect Pricing

If you notice pricing that doesn't match official sources:

1. Check the official pricing pages:
   - [OpenAI Pricing](https://openai.com/api/pricing/)
   - [Anthropic Models](https://docs.anthropic.com/en/docs/about-claude/models)

2. Open an issue with:
   - Model name
   - Current price in repo
   - Correct price from official source
   - Link to official source
   - Screenshot if helpful

### 2. Improve Scraping Logic

The scraping logic in `scripts/fetch_pricing.py` may break when providers update their websites. To improve it:

1. Fork the repository
2. Update the scraping logic
3. Test thoroughly:
   ```bash
   python scripts/fetch_pricing.py --verbose
   ```
4. Document what you changed and why
5. Submit a pull request

### 3. Add New Providers

Want to track models from Google AI, Cohere, or other providers?

1. Update `scripts/fetch_pricing.py`:
   - Add `fetch_PROVIDER_pricing()` function
   - Follow existing patterns
   - Include error handling

2. Update `pricing/latest.json`:
   - Add provider section
   - Use consistent format

3. Update `README.md`:
   - Add provider to "Available Data" section
   - Update usage examples

4. Test and submit PR

### 4. Documentation Improvements

Found a typo? Have a better usage example? Want to add more documentation?

- Submit a PR with your improvements
- All documentation contributions are welcome

## Pull Request Process

1. **Fork** the repository

2. **Create a branch** for your feature:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**:
   - Follow existing code style
   - Add comments for complex logic
   - Test your changes

4. **Test locally**:
   ```bash
   # Test the pricing script
   python scripts/fetch_pricing.py --verbose
   
   # Verify JSON is valid
   python -m json.tool pricing/latest.json > /dev/null
   ```

5. **Commit with clear messages**:
   ```bash
   git commit -m "Add support for Google AI models"
   ```

6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Create a Pull Request**:
   - Describe what you changed and why
   - Reference any related issues
   - Include test results

## Code Style

### Python

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions
- Include type hints where helpful

Example:
```python
def fetch_provider_pricing() -> Optional[Dict]:
    """
    Fetch pricing from Provider.
    
    Returns:
        Dictionary of model pricing or None if failed
    """
    try:
        # Your code here
        return pricing_dict
    except Exception as e:
        print(f"⚠ Provider: Failed to fetch ({e})")
        return None
```

### JSON

- Use 2-space indentation
- Sort keys alphabetically
- Include descriptions for all models
- Prices as floats (not strings)

Example:
```json
{
  "model-name": {
    "description": "Model Name",
    "input": 2.50,
    "output": 10.00
  }
}
```

## Testing

### Manual Testing

```bash
# Run the script
python scripts/fetch_pricing.py --verbose

# Check for changes
git diff pricing/latest.json

# Validate JSON
python -m json.tool pricing/latest.json > /dev/null && echo "Valid JSON"
```

### Integration Testing

Before submitting a PR, ensure:

- [ ] Script runs without errors
- [ ] JSON is valid
- [ ] Pricing data looks reasonable
- [ ] Changes are documented
- [ ] README updated if needed

## Reporting Issues

### Bug Reports

Include:
- What you were trying to do
- What happened
- What you expected to happen
- Error messages or logs
- Python version
- Operating system

### Feature Requests

Include:
- What feature you want
- Why it would be useful
- How you envision it working
- Any alternative solutions considered

## Questions?

- Open an issue with the `question` label
- Check existing issues first
- Be respectful and patient

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment.

### Our Standards

**Positive behavior:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community

**Unacceptable behavior:**
- Trolling, insulting/derogatory comments
- Public or private harassment
- Publishing others' private information
- Other conduct which could reasonably be considered inappropriate

### Enforcement

Instances of unacceptable behavior may be reported by opening an issue. All complaints will be reviewed and investigated.

## Recognition

Contributors will be recognized in:
- GitHub contributors list
- Release notes for significant contributions
- README acknowledgments for major features

Thank you for contributing! 🎉

