# Contributing to Sivaji Security System

Thank you for your interest in contributing to the Sivaji Security System! This document provides guidelines for contributing to this production-grade AI voice biometric authentication system.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Security Considerations](#security-considerations)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Development Workflow](#development-workflow)
- [Testing](#testing)
- [Documentation](#documentation)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Windows 10/11 (for full Windows integration features)
- Microphone for voice authentication testing
- Git for version control
- Basic understanding of:
  - Machine Learning (TensorFlow/Keras)
  - Audio processing (librosa)
  - Cryptography concepts
  - PyQt5 for UI development

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/yourusername/sivaji-ai-security.git
   cd sivaji-ai-security
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/macOS
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup Development Environment**
   ```bash
   # Setup developer fail-safe (for testing)
   python main.py --mode setup-developer-secret
   
   # Run system tests
   python main.py --mode test
   ```

5. **Enroll Test Voice**
   ```bash
   python main.py --mode enroll --username test_user
   ```

## Contributing Guidelines

### What We're Looking For

**High Priority Contributions:**
- Security vulnerability fixes
- Performance optimizations
- Cross-platform compatibility improvements
- Additional biometric modalities (iris, face)
- Advanced liveness detection techniques
- Documentation improvements

**Medium Priority:**
- UI/UX enhancements
- Additional language support
- Cloud integration features
- Mobile app development
- Advanced threat detection

**Please Avoid:**
- Breaking changes without discussion
- Hardcoded credentials or secrets
- Bypassing security mechanisms
- Removing encryption or audit logging

### Contribution Types

1. **Bug Fixes**
   - Security vulnerabilities (report privately first)
   - Functional bugs
   - Performance issues
   - Compatibility problems

2. **Feature Enhancements**
   - New biometric modalities
   - Improved algorithms
   - Better user experience
   - Additional integrations

3. **Documentation**
   - Code documentation
   - User guides
   - API documentation
   - Security documentation

4. **Testing**
   - Unit tests
   - Integration tests
   - Security tests
   - Performance benchmarks

## Security Considerations

### Critical Security Rules

⚠️ **NEVER commit:**
- Real biometric data or voice samples
- Encryption keys or secrets
- Authentication credentials
- Personal information
- Production configuration files

⚠️ **ALWAYS:**
- Use placeholder/synthetic data for testing
- Encrypt sensitive test data
- Follow secure coding practices
- Report security issues privately
- Test security features thoroughly

### Responsible Disclosure

If you discover a security vulnerability:

1. **DO NOT** create a public GitHub issue
2. **Email** the maintainers privately at [security@project.com]
3. **Provide** detailed information about the vulnerability
4. **Allow** 90 days for responsible disclosure
5. **Coordinate** public disclosure timing

### Security Testing

When testing security features:
- Use synthetic/test data only
- Don't attempt to extract real biometric templates
- Test in isolated environments
- Document security test procedures
- Verify encryption and audit logging

## Pull Request Process

### Before Submitting

1. **Check existing issues** and PRs to avoid duplicates
2. **Create an issue** for discussion (for major changes)
3. **Follow coding standards** (see below)
4. **Add tests** for new functionality
5. **Update documentation** as needed
6. **Test thoroughly** including security aspects

### PR Requirements

✅ **Required:**
- Clear, descriptive title and description
- Reference to related issue(s)
- Tests for new functionality
- Documentation updates
- No breaking changes (without discussion)
- Security review for sensitive changes

✅ **Code Quality:**
- Follows PEP 8 style guidelines
- Includes type hints where appropriate
- Has comprehensive docstrings
- Handles errors gracefully
- Includes logging for debugging

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update
- [ ] Security fix

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Security tests pass
- [ ] Manual testing completed

## Security Impact
- [ ] No security impact
- [ ] Security review required
- [ ] Affects authentication/encryption
- [ ] Changes fail-safe mechanisms

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
```

## Issue Reporting

### Bug Reports

Use the bug report template:

```markdown
**Bug Description**
Clear description of the bug

**Steps to Reproduce**
1. Step 1
2. Step 2
3. Step 3

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g., Windows 11]
- Python Version: [e.g., 3.9.7]
- Dependencies: [relevant package versions]

**Security Impact**
- [ ] No security impact
- [ ] Potential security issue
- [ ] Critical security vulnerability

**Additional Context**
Any other relevant information
```

### Feature Requests

```markdown
**Feature Description**
Clear description of the proposed feature

**Use Case**
Why is this feature needed?

**Proposed Solution**
How should this be implemented?

**Security Considerations**
Any security implications?

**Alternatives Considered**
Other approaches considered
```

## Development Workflow

### Branch Naming

- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `security/description` - Security fixes
- `docs/description` - Documentation updates
- `test/description` - Testing improvements

### Commit Messages

Follow conventional commits:

```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Testing
- `security`: Security fixes

**Examples:**
```
feat(auth): add iris recognition support
fix(security): resolve encryption key vulnerability
docs(api): update authentication API documentation
security(failsafe): strengthen OTK generation
```

## Testing

### Test Categories

1. **Unit Tests**
   ```bash
   python -m pytest tests/unit/
   ```

2. **Integration Tests**
   ```bash
   python -m pytest tests/integration/
   ```

3. **Security Tests**
   ```bash
   python -m pytest tests/security/
   ```

4. **System Tests**
   ```bash
   python main.py --mode test
   ```

### Test Requirements

- **Coverage**: Aim for >80% code coverage
- **Security**: Test all security-critical paths
- **Edge Cases**: Test boundary conditions
- **Error Handling**: Test failure scenarios
- **Performance**: Include performance benchmarks

### Writing Tests

```python
import pytest
from unittest.mock import Mock, patch
from security.encryption import EncryptionManager

class TestEncryptionManager:
    def test_encrypt_decrypt_roundtrip(self):
        """Test encryption/decryption roundtrip"""
        manager = EncryptionManager()
        original_data = "test data"
        
        encrypted = manager.encrypt_data(original_data)
        decrypted = manager.decrypt_data(encrypted)
        
        assert decrypted == original_data
    
    def test_invalid_key_raises_error(self):
        """Test that invalid keys raise appropriate errors"""
        with pytest.raises(ValueError):
            manager = EncryptionManager()
            manager.decrypt_data(b"invalid_data")
```

## Documentation

### Documentation Standards

1. **Code Documentation**
   - Comprehensive docstrings for all public functions
   - Type hints for function parameters and returns
   - Inline comments for complex logic
   - Security considerations noted

2. **API Documentation**
   - Clear parameter descriptions
   - Return value specifications
   - Usage examples
   - Error conditions

3. **User Documentation**
   - Step-by-step guides
   - Configuration examples
   - Troubleshooting sections
   - Security best practices

### Documentation Format

```python
def verify_voice(self, audio_data: np.ndarray) -> Dict[str, Any]:
    """
    Verify voice authentication with liveness detection.
    
    This function performs multi-factor voice verification including
    liveness detection to prevent playback attacks.
    
    Args:
        audio_data: Raw audio samples as numpy array (16kHz, mono)
    
    Returns:
        Dictionary containing:
        - authenticated: bool - Whether authentication succeeded
        - confidence: float - Confidence score (0.0-1.0)
        - liveness_score: float - Liveness detection score (0.0-1.0)
        - details: dict - Additional verification details
    
    Raises:
        ValueError: If audio_data is invalid or too short
        SecurityError: If potential spoofing detected
    
    Security:
        - All biometric data is encrypted before storage
        - Liveness detection prevents playback attacks
        - Failed attempts are logged and rate-limited
    
    Example:
        >>> verifier = VerificationPipeline()
        >>> result = verifier.verify_voice(audio_samples)
        >>> if result['authenticated']:
        ...     print("Access granted")
    """
```

## Code Style Guidelines

### Python Style

- Follow PEP 8
- Use type hints
- Maximum line length: 88 characters
- Use meaningful variable names
- Prefer composition over inheritance

### Security Coding Standards

```python
# ✅ Good: Secure random generation
import secrets
otk = secrets.token_hex(32)

# ❌ Bad: Predictable random
import random
otk = random.randint(1000000, 9999999)

# ✅ Good: Constant-time comparison
import hmac
is_valid = hmac.compare_digest(provided_hash, stored_hash)

# ❌ Bad: Timing attack vulnerable
is_valid = provided_hash == stored_hash

# ✅ Good: Input validation
def process_audio(audio_data: np.ndarray) -> Dict:
    if not isinstance(audio_data, np.ndarray):
        raise ValueError("Audio data must be numpy array")
    if len(audio_data) < 8000:  # Minimum 0.5 seconds at 16kHz
        raise ValueError("Audio too short for processing")
```

### Error Handling

```python
# ✅ Good: Specific exception handling
try:
    result = process_biometric_data(data)
except BiometricProcessingError as e:
    logger.error(f"Biometric processing failed: {e}")
    return {"error": "Processing failed", "authenticated": False}
except Exception as e:
    logger.critical(f"Unexpected error: {e}")
    return {"error": "System error", "authenticated": False}

# ❌ Bad: Bare except
try:
    result = process_biometric_data(data)
except:
    return False
```

## Release Process

### Version Numbering

We use Semantic Versioning (SemVer):
- `MAJOR.MINOR.PATCH`
- Major: Breaking changes
- Minor: New features (backward compatible)
- Patch: Bug fixes

### Release Checklist

- [ ] All tests pass
- [ ] Security review completed
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version numbers updated
- [ ] Release notes prepared
- [ ] Security audit (for major releases)

## Getting Help

### Resources

- **Documentation**: Check the `docs/` directory
- **Issues**: Search existing GitHub issues
- **Discussions**: Use GitHub Discussions for questions
- **Security**: Email security@project.com for security issues

### Community

- Be respectful and professional
- Help others learn and contribute
- Share knowledge and best practices
- Follow the Code of Conduct

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- Project documentation
- Annual contributor highlights

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

---

**Thank you for contributing to the Sivaji Security System!**

Your contributions help make biometric authentication more secure and accessible for everyone.

---

**Last Updated**: January 2025
**Version**: 1.0