# Technology Stack

## Core Technologies

- **Game Engine**: Pygame 2.5.2 for 60fps interactive gameplay
- **Mathematics**: NumPy 1.24.3 for neural network computations
- **Visualization**: Matplotlib 3.7.2 + custom rendering system
- **UI Framework**: pygame-gui 0.6.9 for modern UI components
- **Audio**: pyttsx3 2.90 for text-to-speech narration
- **Python**: 3.x (modern Python features expected)

## Testing Framework

- **Test Runner**: pytest 7.4.3 with custom run_tests.py script
- **Coverage**: pytest-cov 4.1.0 with 80% minimum coverage requirement
- **Mocking**: pytest-mock 3.12.0 for isolated unit tests
- **Test Types**: Unit, integration, and end-to-end tests in separate directories

## Common Commands

### Development
```bash
# Start the game (with virtual environment)
source navenv/bin/activate && python main.py

# Install dependencies
pip install -r requirements.txt

# Package for distribution
python build_executable.py
```

### Testing
```bash
# Quick unit tests
python run_tests.py quick

# All tests with coverage
python run_tests.py all

# Specific test types
python run_tests.py unit
python run_tests.py integration
python run_tests.py e2e

# Generate coverage report (creates htmlcov/index.html)
python run_tests.py coverage

# Code quality checks
python run_tests.py quality
```

### Environment Setup
```bash
# For headless testing (CI/automated environments)
export SDL_VIDEODRIVER=dummy
```

## Code Quality Standards

- **Coverage Target**: 80%+ required (enforced by pytest configuration)
- **Code Style**: PEP 8 compliant
- **Type Hints**: Encouraged for new code
- **Documentation**: Comprehensive docstrings required
- **Testing**: All new features must include unit tests