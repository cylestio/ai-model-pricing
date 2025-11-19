# Changelog

All notable changes to AI Model Pricing will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Support for Google AI models
- Support for Cohere models
- Historical pricing data visualization
- API wrapper package for popular languages
- Pricing alerts via webhook

## [1.0.0] - 2025-11-19

### Added
- Initial release of AI Model Pricing
- Automated pricing fetching from OpenAI and Anthropic
- GitHub Action for weekly pricing updates
- Comprehensive pricing data for 90+ models:
  - OpenAI: GPT-3.5, GPT-4, GPT-4o, GPT-5, o1 series
  - Anthropic: Claude 2, Claude 3, Claude 3.5, Claude 4, Claude 4.5
- JSON data format for easy consumption
- Python script for manual pricing updates
- Documentation and usage examples
- MIT License

### Data Sources
- OpenAI pricing: https://openai.com/api/pricing/
- Anthropic models: https://docs.anthropic.com/en/docs/about-claude/models

### Known Limitations
- OpenAI pricing may fail to fetch due to anti-scraping (fallback available)
- Web scraping is fragile and may break with website updates
- Updates are weekly (not real-time)

---

## Version Numbering

- **Major version** (X.0.0): Breaking changes to JSON format
- **Minor version** (0.X.0): New features (new providers, fields)
- **Patch version** (0.0.X): Bug fixes, pricing updates

## Release Process

1. Pricing updates are automated via GitHub Actions
2. Manual updates can be triggered from Actions tab
3. Each update creates a git commit
4. Significant changes create a new release
5. This changelog is updated for notable changes

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to contribute.

## Questions?

Open an issue or check the [README](README.md) for more information.

