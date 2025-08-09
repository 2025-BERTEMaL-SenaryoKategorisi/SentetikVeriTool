# Contributing to Turkish Telecom Synthetic Data Generator

Thank you for your interest in contributing to this project! This guide will help you get started.

## 🚀 Quick Start for Contributors

### 1. Fork and Clone

```bash
git clone https://github.com/yourusername/SentetikVeri.git
cd SentetikVeri
```

### 2. Set Up Environment

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your API keys
```

### 3. Test Your Setup

```bash
# Test text-only generation (fast)
python demos/text_only_demo.py

# Test audio generation (requires API keys)
python demos/enhanced_tts_demo.py
```

## 📋 Development Guidelines

### Code Style

- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and under 50 lines when possible

### Project Structure

```
SentetikVeri/
├── generators/          # Main generation scripts
├── demos/              # Demo and test scripts
├── config/             # Configuration files
├── docs/               # Documentation
├── tools/              # Utility scripts
└── data/               # Generated data (gitignored)
```

### Testing

- Test your changes with both generators
- Verify incremental ID system works correctly
- Check that generated data validates properly
- Test with different API configurations

## 🎯 Areas for Contribution

### High Priority

- **New TTS Providers**: Add support for additional TTS services
- **Voice Variety**: Expand Turkish voice options and characteristics
- **Scenario Expansion**: Add new telecom conversation scenarios
- **Performance Optimization**: Improve generation speed and efficiency

### Medium Priority

- **Data Quality**: Enhance validation and quality control
- **Documentation**: Improve guides and examples
- **Testing**: Add automated tests and CI/CD
- **Internationalization**: Support for other languages

### Low Priority

- **UI/UX**: Web interface for easier usage
- **Analytics**: Data generation statistics and insights
- **Export Formats**: Additional output formats beyond JSONL

## 🔧 Technical Contributions

### Adding New TTS Providers

1. Add provider configuration to `generators/main_generator.py`
2. Implement provider-specific audio generation method
3. Add fallback logic and error handling
4. Update documentation and examples

### Adding New Scenarios

1. Define scenario in `config/config.py` under `TELECOM_SCENARIOS`
2. Add conversation flow and intent progression
3. Include Turkish telecom terminology
4. Test with both generators

### Improving Voice Management

1. Extend `ENHANCED_VOICE_CONFIGS` with new voices
2. Ensure gender-appropriate voice matching
3. Test voice consistency across conversations
4. Update voice selection algorithms

## 📝 Submission Process

### Before Submitting

- [ ] Code follows project style guidelines
- [ ] All tests pass with your changes
- [ ] Documentation is updated if needed
- [ ] No sensitive data (API keys, credentials) in commits
- [ ] Generated data files are not included (check .gitignore)

### Pull Request Process

1. **Create Feature Branch**: `git checkout -b feature/your-feature-name`
2. **Make Changes**: Implement your feature or fix
3. **Test Thoroughly**: Verify everything works correctly
4. **Commit Changes**: Use clear, descriptive commit messages
5. **Push Branch**: `git push origin feature/your-feature-name`
6. **Create PR**: Submit pull request with detailed description

### PR Description Template

```markdown
## Description

Brief description of changes made.

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing

- [ ] Tested with text-only generator
- [ ] Tested with audio generator
- [ ] Verified incremental ID system
- [ ] Checked data validation

## Checklist

- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No sensitive data included
```

## 🐛 Bug Reports

### Before Reporting

- Check existing issues for duplicates
- Test with latest version
- Verify it's not a configuration issue

### Bug Report Template

```markdown
**Describe the Bug**
Clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:

1. Run command '...'
2. With configuration '...'
3. See error

**Expected Behavior**
What you expected to happen.

**Environment**

- OS: [e.g., macOS, Windows, Linux]
- Python version: [e.g., 3.9.0]
- Dependencies: [paste requirements.txt versions]

**Additional Context**
Any other context about the problem.
```

## 💡 Feature Requests

### Feature Request Template

```markdown
**Feature Description**
Clear description of the feature you'd like to see.

**Use Case**
Explain why this feature would be useful.

**Proposed Implementation**
If you have ideas on how to implement this.

**Additional Context**
Any other context or screenshots.
```

## 🏆 Recognition

Contributors will be recognized in:

- README.md contributors section
- Release notes for significant contributions
- Special thanks for major features or fixes

## 📞 Getting Help

- **Issues**: Create GitHub issue for bugs or questions
- **Discussions**: Use GitHub Discussions for general questions
- **Documentation**: Check docs/ folder for detailed guides

## 🎯 TEKNOFEST 2025 Context

This project is designed for the TEKNOFEST 2025 Turkish Natural Language Processing competition. Contributions should keep this context in mind:

- Focus on Turkish language and telecom domain
- Ensure TEKNOFEST competition format compliance
- Prioritize data quality and realism
- Consider computational efficiency for large-scale generation

Thank you for contributing to this project! 🚀
