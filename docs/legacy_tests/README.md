# 🧪 Legacy Test Files

This directory contains legacy test files and debugging scripts from the development process.

## 📁 Contents

### Test Files
- **test_distribution.py** - Distribution testing script
- **test_enhanced_game.py** - Enhanced game features testing
- **test_full_interaction.py** - Full interaction testing
- **test_game_manual.py** - Manual testing procedures
- **test_game_visual.py** - Visual testing scripts
- **test_level_crash.py** - Level crash debugging
- **test_perceptron_challenge.py** - Perceptron challenge testing
- **test_perceptron.py** - Basic perceptron testing

### Debug Scripts
- **debug_crash.py** - Crash debugging utilities
- **temp_practice_method.py** - Temporary practice implementations

## ⚠️ Important Note

These files are kept for historical reference but are **not part of the main test suite**. 

For current testing, use:
```bash
# Run the official test suite
python scripts/run_tests.py all

# Run specific test categories
python scripts/run_tests.py unit
python scripts/run_tests.py integration
python scripts/run_tests.py e2e
```

## 🔗 Current Testing

- **Main Test Suite**: `tests/` directory
- **Test Runner**: `scripts/run_tests.py`
- **Test Configuration**: `pytest.ini`
- **Coverage Reports**: `htmlcov/` directory

---

*These legacy files represent the iterative development and testing process used to build the Neural Network Adventure RPG.*