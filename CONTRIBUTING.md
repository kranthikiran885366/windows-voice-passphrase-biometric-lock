# Contributing to Sivaji Security System

We welcome contributions! This project is open-source and community-driven.

## Development Setup

\`\`\`bash
git clone https://github.com/YOUR_REPO/sivaji-security-system
cd sivaji-security-system
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install -r dev-requirements.txt  # Testing, linting
\`\`\`

## Making Changes

1. **Create a branch**: `git checkout -b feature/your-feature`
2. **Make changes**: Follow the coding style below
3. **Test**: `pytest tests/`
4. **Commit**: `git commit -m "Feature: description"`
5. **Push**: `git push origin feature/your-feature`
6. **PR**: Open pull request on GitHub

## Coding Style

- **Python**: PEP 8 (use `black` formatter)
- **Naming**: snake_case for functions/variables, CamelCase for classes
- **Docstrings**: Google-style docstrings
- **Type hints**: Use type hints for all functions

## Areas for Contribution

- **Voice Processing**: Improve MFCC extraction, liveness detection
- **Model Architecture**: Experiment with different CNN+LSTM designs
- **UI/UX**: Enhance PyQt5 interface, add new themes
- **Testing**: Write more comprehensive tests
- **Documentation**: Improve docs, add tutorials
- **Translations**: Translate UI to other languages
- **Windows Integration**: Develop credential provider DLL
- **Linux Support**: Port to Linux with PAM integration

## Reporting Issues

1. Check existing issues first
2. Include: Python version, OS, error message, steps to reproduce
3. Provide minimal reproducible example

## Code Review

All PRs require:
- ✅ Passes tests
- ✅ Code style check
- ✅ Documentation updated
- ✅ At least 1 approval

## License

All contributions are under MIT License.

Thanks for contributing! 🎤
