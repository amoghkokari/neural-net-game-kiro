# 🤝 Contributing to Neural Network Adventure RPG

Thank you for your interest in contributing to Neural Network Adventure! This document provides guidelines and information for contributors.

## 📋 Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Development Workflow](#development-workflow)

## 📜 Code of Conduct

This project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## 🚀 Getting Started

### Ways to Contribute
- 🐛 **Bug Reports**: Help us identify and fix issues
- 💡 **Feature Requests**: Suggest new educational content or game features
- 📝 **Documentation**: Improve guides, tutorials, and API docs
- 🎨 **Visual Improvements**: Enhance UI design and visual effects
- 🧪 **Testing**: Write tests or test on different platforms
- 💻 **Code**: Implement new features or fix bugs
- 🎓 **Educational Content**: Design new neural network challenges

### What We're Looking For
- **Educational Challenges**: New neural network concepts to teach
- **Game Features**: UI improvements, accessibility features
- **Performance Optimizations**: Better rendering, memory usage
- **Cross-Platform Support**: Testing and fixes for different OS
- **Documentation**: User guides, developer docs, tutorials
- **Testing**: Unit tests, integration tests, manual testing

## 🛠️ Development Setup

### Prerequisites
- **Python 3.8+**
- **Git**
- **Virtual environment** (recommended)

### Setup Steps
```bash
# 1. Fork the repository on GitHub
# 2. Clone your fork
git clone https://github.com/YOUR-USERNAME/neural-network-adventure.git
cd neural-network-adventure

# 3. Set up virtual environment
python -m venv navenv
source navenv/bin/activate  # On Windows: navenv\Scripts\activate

# 4. Install development dependencies
pip install -r requirements-dev.txt

# 5. Install pre-commit hooks (optional but recommended)
pre-commit install

# 6. Run tests to ensure everything works
python scripts/run_tests.py all

# 7. Start the game to test
python main.py
```

### Development Dependencies
```bash
# Runtime dependencies
pip install -r requirements.txt

# Development dependencies (testing, linting, etc.)
pip install -r requirements-dev.txt

# Build dependencies (for creating executables)
pip install -r requirements-build.txt
```

## 📏 Contributing Guidelines

### Code Style
- **Follow PEP 8**: Python style guidelines
- **Use Type Hints**: For better code clarity
- **Write Docstrings**: Document all public functions and classes
- **Line Length**: Maximum 88 characters (Black formatter)
- **Import Organization**: Use isort for consistent imports

### Code Quality Tools
```bash
# Format code
black src/ tests/

# Sort imports
isort src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/

# Run all quality checks
python scripts/run_tests.py quality
```

### Testing Requirements
- **Write Tests**: All new features must include tests
- **Maintain Coverage**: Aim for 80%+ test coverage
- **Test Types**: Unit tests for logic, integration tests for components
- **Mock External Dependencies**: Use pytest fixtures for pygame, file I/O

### Documentation Standards
- **Docstrings**: Use Google-style docstrings
- **Type Annotations**: All public APIs must have type hints
- **Examples**: Include usage examples in docstrings
- **README Updates**: Update documentation for new features

## 🔄 Development Workflow

### Branch Naming
```bash
# Feature branches
feature/new-challenge-system
feature/improved-ui-layout

# Bug fix branches
bugfix/level-progression-issue
bugfix/audio-crash-fix

# Documentation branches
docs/contributing-guide
docs/api-documentation
```

### Commit Messages
Use conventional commit format:
```bash
# Feature commits
feat: add RNN challenge with LSTM visualization
feat(ui): implement responsive layout system

# Bug fix commits
fix: resolve level progression blocking issue
fix(audio): prevent crash when speech engine unavailable

# Documentation commits
docs: add contributing guidelines
docs(api): document challenge system API

# Test commits
test: add unit tests for neuron challenge
test(integration): add state transition tests
```

### Development Process
1. **Create Issue**: Discuss feature/bug before coding
2. **Create Branch**: Use descriptive branch names
3. **Write Code**: Follow style guidelines and write tests
4. **Test Locally**: Run full test suite
5. **Update Documentation**: Update relevant docs
6. **Create Pull Request**: Use PR template
7. **Code Review**: Address feedback from maintainers
8. **Merge**: Squash and merge when approved

## 📝 Pull Request Process

### Before Submitting
- [ ] **Tests Pass**: All tests pass locally
- [ ] **Code Quality**: Linting and formatting checks pass
- [ ] **Documentation**: Updated for new features
- [ ] **Coverage**: Test coverage maintained or improved
- [ ] **Manual Testing**: Feature works as expected

### PR Template
```markdown
## Description
Brief description of changes and motivation.

## Type of Change
- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] Manual testing completed
- [ ] All tests pass

## Screenshots (if applicable)
Add screenshots for UI changes.

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added for new functionality
```

### Review Process
1. **Automated Checks**: CI/CD runs tests and quality checks
2. **Code Review**: Maintainers review code and provide feedback
3. **Discussion**: Address questions and suggestions
4. **Approval**: At least one maintainer approval required
5. **Merge**: Squash and merge to main branch

## 🐛 Issue Reporting

### Bug Reports
Use the bug report template:
```markdown
**Describe the Bug**
Clear description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected Behavior**
What you expected to happen.

**Screenshots**
If applicable, add screenshots.

**Environment:**
- OS: [e.g. macOS 12.0, Windows 11, Ubuntu 20.04]
- Python Version: [e.g. 3.9.7]
- Game Version: [e.g. 1.0.0]

**Additional Context**
Any other context about the problem.
```

### Feature Requests
Use the feature request template:
```markdown
**Is your feature request related to a problem?**
Clear description of the problem.

**Describe the solution you'd like**
Clear description of what you want to happen.

**Describe alternatives you've considered**
Alternative solutions or features you've considered.

**Educational Value**
How would this feature improve the learning experience?

**Additional Context**
Any other context, mockups, or examples.
```

## 🎓 Educational Content Guidelines

### Creating New Challenges
When adding new neural network challenges:

1. **Educational Goal**: Clear learning objective
2. **Progressive Difficulty**: Builds on previous concepts
3. **Interactive Elements**: Hands-on parameter adjustment
4. **Visual Feedback**: Real-time visualization of concepts
5. **Immediate Validation**: Instant feedback on user actions
6. **Hint System**: Contextual help when users struggle

### Challenge Structure
```python
class NewChallenge(BaseChallenge):
    """
    Challenge teaching [specific concept].
    
    Learning Objectives:
    - Understand [concept 1]
    - Apply [concept 2]
    - Implement [concept 3]
    """
    
    def initialize(self):
        """Set up challenge parameters and UI"""
        
    def handle_event(self, event):
        """Handle user input and interactions"""
        
    def update(self, dt):
        """Update challenge state and animations"""
        
    def render(self, screen):
        """Render challenge visualization"""
        
    def check_solution(self):
        """Validate user's solution"""
        
    def get_hint(self):
        """Provide contextual help"""
```

## 🏗️ Architecture Guidelines

### Adding New Game States
```python
class NewState(BaseState):
    """New game state for [purpose]"""
    
    def __init__(self, game):
        super().__init__(game)
        # Initialize state-specific data
        
    def handle_event(self, event):
        # Handle state-specific events
        
    def update(self, dt):
        # Update state logic
        
    def render(self, screen):
        # Render state visuals
```

### UI Component Guidelines
- **Consistent Styling**: Use existing color schemes and fonts
- **Responsive Design**: Support different screen sizes
- **Accessibility**: Keyboard navigation and clear visual feedback
- **Performance**: Efficient rendering and minimal memory usage

## 🧪 Testing Guidelines

### Test Structure
```python
# tests/unit/test_new_feature.py
import pytest
from unittest.mock import Mock, patch
from src.new_feature import NewFeature

class TestNewFeature:
    """Test suite for NewFeature class"""
    
    def test_initialization(self):
        """Test that NewFeature initializes correctly"""
        feature = NewFeature()
        assert feature.initialized is True
        
    def test_specific_functionality(self):
        """Test specific feature behavior"""
        # Test implementation
        
    @patch('pygame.display')
    def test_with_mocked_pygame(self, mock_display):
        """Test with mocked pygame dependencies"""
        # Test implementation
```

### Testing Best Practices
- **Descriptive Names**: Test names should describe what they test
- **Single Responsibility**: One test per behavior
- **Arrange-Act-Assert**: Clear test structure
- **Mock External Dependencies**: Don't test pygame, file system, etc.
- **Edge Cases**: Test boundary conditions and error cases

## 🎨 Visual Design Guidelines

### UI/UX Design
- **Style Consistency**: Follow existing design patterns
- **Color Scheme**: Use established color constants
- **Typography**: Consistent font usage throughout
- **Responsive Design**: Support different screen sizes

### Visual Effects
- **Performance**: Maintain 60 FPS with all effects
- **Accessibility**: Ensure good contrast and readability
- **Animation**: Smooth transitions and feedback
- **Modern Design**: Clean, professional appearance

## 📊 Performance Guidelines

### Code Performance
- **60 FPS Target**: Maintain smooth gameplay
- **Memory Efficiency**: Minimize object creation in game loop
- **Resource Management**: Efficient memory usage and caching
- **Profiling**: Use cProfile for performance analysis

### Optimization Techniques
- **Object Pooling**: Reuse game objects
- **Dirty Rectangle Updates**: Only redraw changed areas
- **Level-of-Detail**: Reduce complexity for distant objects
- **Batch Operations**: Group similar rendering calls

## 🌍 Internationalization

### Text Guidelines
- **Externalize Strings**: Use configuration files for text
- **Unicode Support**: Handle international characters
- **Context**: Provide context for translators
- **Placeholder Support**: Use format strings for dynamic content

## 🚀 Release Process

### Version Numbering
- **Semantic Versioning**: MAJOR.MINOR.PATCH
- **Major**: Breaking changes or major new features
- **Minor**: New features, backward compatible
- **Patch**: Bug fixes, backward compatible

### Release Checklist
- [ ] All tests pass
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Version numbers bumped
- [ ] Cross-platform builds tested
- [ ] Release notes prepared

## 🤝 Community

### Communication Channels
- **GitHub Issues**: Bug reports and feature requests
- **GitHub Discussions**: General questions and ideas
- **Discord**: Real-time chat and community support
- **Email**: Direct contact for sensitive issues

### Getting Help
- **Documentation**: Check existing docs first
- **Search Issues**: Look for similar problems
- **Ask Questions**: Use GitHub Discussions
- **Join Discord**: Get help from the community

## 🙏 Recognition

### Contributors
All contributors are recognized in:
- **README.md**: Contributors section
- **CHANGELOG.md**: Release notes
- **About Screen**: In-game credits
- **GitHub**: Contributor graphs and statistics

### Types of Recognition
- **Code Contributors**: GitHub commit history
- **Issue Reporters**: Mentioned in fix commits
- **Documentation**: Bylines on major docs
- **Community Support**: Special Discord roles

---

## 🎉 Thank You!

Your contributions make Neural Network Adventure better for everyone. Whether you're fixing a typo, adding a feature, or helping other users, every contribution matters.

**Happy coding, and welcome to the Neural Network Adventure community!** 🧠🎮✨

---

<div align="center">

**[⬆️ Back to Top](#-contributing-to-neural-network-adventure-rpg)** | **[🏠 Main README](../README.md)** | **[📋 Code of Conduct](CODE_OF_CONDUCT.md)**

</div>