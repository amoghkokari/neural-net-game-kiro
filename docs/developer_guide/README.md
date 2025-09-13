# 🛠️ Neural Network Adventure RPG - Developer Guide

Welcome to the developer guide! This comprehensive guide will help you understand, modify, and extend the Neural Network Adventure RPG.

## 📋 Table of Contents
- [Quick Start](#quick-start)
- [Project Architecture](#project-architecture)
- [Development Setup](#development-setup)
- [Code Organization](#code-organization)
- [Adding New Content](#adding-new-content)
- [Testing Guide](#testing-guide)
- [Build & Distribution](#build--distribution)
- [API Reference](#api-reference)

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+**
- **Git**
- **Virtual environment** (recommended)

### Setup in 3 Steps
```bash
# 1. Clone and enter directory
git clone https://github.com/your-username/neural-network-adventure.git
cd neural-network-adventure

# 2. Run automated setup
python scripts/setup_dev.py

# 3. Start developing!
source navenv/bin/activate  # On Windows: navenv\Scripts\activate
python main.py
```

### Development Commands
```bash
# Run the game
python main.py

# Run tests
python scripts/run_tests.py all

# Format code
python scripts/dev.py format

# Build executable
python scripts/build_executable.py
```

## 🏗️ Project Architecture

### High-Level Overview
```
Neural Network Adventure RPG
├── Game Engine (Pygame-based)
├── State Management (Menu, World Map, Levels)
├── Challenge System (Educational content)
├── Visualization Engine (Neural network rendering)
├── Character System (Progression and stats)
└── Audio System (Text-to-speech narration)
```

### Core Design Patterns

#### 1. State Pattern
All game screens inherit from `BaseState`:
```python
class BaseState:
    def handle_event(self, event): pass
    def update(self, dt): pass
    def render(self, screen): pass

class MenuState(BaseState):
    # Implement menu-specific behavior
```

#### 2. Challenge System
Educational content uses a plugin-like architecture:
```python
class BaseChallenge:
    def initialize(self): pass
    def handle_event(self, event): pass
    def check_solution(self): pass
    def get_hint(self): pass

class NeuronChallenge(BaseChallenge):
    # Implement neuron-specific learning content
```

#### 3. Component-Based UI
Reusable UI components for consistent design:
```python
class ModernButton:
    def __init__(self, text, position, callback): pass
    def render(self, screen): pass
    def handle_click(self, pos): pass
```

### Directory Structure
```
neural-network-adventure/
├── src/                    # Main source code
│   ├── game.py            # Core game class
│   ├── constants.py       # Game constants
│   ├── states/            # Game state management
│   ├── challenges/        # Educational challenges
│   ├── ui/               # User interface components
│   ├── visualization/    # Neural network rendering
│   ├── character/        # Character progression
│   └── audio/            # Speech and sound
├── tests/                # Test suite
├── scripts/              # Development tools
├── docs/                 # Documentation

└── config/               # Configuration files
```

## 🛠️ Development Setup

### Automated Setup (Recommended)
```bash
python scripts/setup_dev.py
```

This script will:
- ✅ Create virtual environment
- ✅ Install all dependencies
- ✅ Set up pre-commit hooks
- ✅ Configure VS Code settings
- ✅ Run initial tests

### Manual Setup
```bash
# Create virtual environment
python -m venv navenv
source navenv/bin/activate  # Windows: navenv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt

# Set up pre-commit hooks
pre-commit install

# Run tests to verify setup
python scripts/run_tests.py all
```

### Development Dependencies
- **Runtime**: pygame, numpy, matplotlib, pygame-gui, pyttsx3
- **Testing**: pytest, pytest-cov, pytest-mock
- **Code Quality**: black, isort, flake8, mypy
- **Documentation**: sphinx, sphinx-rtd-theme
- **Build**: pyinstaller, build, wheel

## 📁 Code Organization

### Source Code Structure

#### Core Game (`src/`)
```python
# game.py - Main game class
class Game:
    def __init__(self, screen, width, height):
        self.states = {}  # State management
        self.current_state = None
        self.player_progress = {}
    
    def handle_event(self, event): pass
    def update(self, dt): pass
    def render(self): pass
```

#### Game States (`src/states/`)
```python
# base_state.py - Abstract base class
class BaseState(ABC):
    @abstractmethod
    def handle_event(self, event): pass
    
    @abstractmethod
    def update(self, dt): pass
    
    @abstractmethod
    def render(self, screen): pass

# Concrete implementations
class MenuState(BaseState): pass
class WorldMapState(BaseState): pass
class LevelState(BaseState): pass
```

#### Challenge System (`src/challenges/`)
```python
# base_challenge.py - Challenge interface
class BaseChallenge(ABC):
    def __init__(self):
        self.completed = False
        self.score = 0
        self.understanding_level = 0
    
    @abstractmethod
    def initialize(self): pass
    
    @abstractmethod
    def check_solution(self): pass
    
    @abstractmethod
    def get_hint(self): pass
```

#### UI Components (`src/ui/`)
```python
# modern_ui.py - Reusable UI components
class ModernButton:
    def __init__(self, text, rect, callback):
        self.text = text
        self.rect = rect
        self.callback = callback
        self.hovered = False
    
    def render(self, screen): pass
    def handle_event(self, event): pass
```

### Configuration Management
```python
# config/game_config.py
class GameConfig:
    # Display settings
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800
    FPS = 60
    
    # Game settings
    DIFFICULTY_LEVELS = ['easy', 'medium', 'hard']
    SAVE_FILE = 'neural_adventure_save.json'
    
    # Educational settings
    HINT_DELAY = 30  # seconds before hints available
    UNDERSTANDING_THRESHOLD = 0.8
```

## 🎓 Adding New Content

### Creating a New Challenge

#### 1. Create Challenge Class
```python
# src/challenges/my_new_challenge.py
from .base_challenge import BaseChallenge
import pygame
import numpy as np

class MyNewChallenge(BaseChallenge):
    """
    Challenge teaching [specific concept].
    
    Learning Objectives:
    - Understand [concept 1]
    - Apply [concept 2]
    - Implement [concept 3]
    """
    
    def __init__(self):
        super().__init__()
        self.concept_name = "My New Concept"
        self.difficulty = "intermediate"
        
    def initialize(self):
        """Set up challenge parameters and UI"""
        self.parameters = {
            'learning_rate': 0.01,
            'epochs': 100,
            'batch_size': 32
        }
        self.current_parameter = 'learning_rate'
        
    def handle_event(self, event):
        """Handle user input and interactions"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self._select_previous_parameter()
            elif event.key == pygame.K_RIGHT:
                self._select_next_parameter()
            elif event.key == pygame.K_UP:
                self._increase_parameter()
            elif event.key == pygame.K_DOWN:
                self._decrease_parameter()
            elif event.key == pygame.K_f:
                self._execute_forward_pass()
                
    def update(self, dt):
        """Update challenge state and animations"""
        # Update visualizations, animations, etc.
        pass
        
    def render(self, screen):
        """Render challenge visualization"""
        # Render neural network, parameters, UI, etc.
        self._render_network(screen)
        self._render_parameters(screen)
        self._render_instructions(screen)
        
    def check_solution(self):
        """Validate user's solution"""
        # Check if parameters achieve learning objective
        accuracy = self._calculate_accuracy()
        if accuracy > 0.9:
            self.completed = True
            self.score = int(accuracy * 1000)
            return True
        return False
        
    def get_hint(self):
        """Provide contextual help"""
        hints = {
            'learning_rate': "Try a smaller learning rate for more stable training",
            'epochs': "More epochs allow more learning, but watch for overfitting",
            'batch_size': "Larger batches are more stable, smaller batches more noisy"
        }
        return hints.get(self.current_parameter, "Experiment with different values!")
```

#### 2. Register Challenge
```python
# src/challenges/__init__.py
from .my_new_challenge import MyNewChallenge

AVAILABLE_CHALLENGES = {
    'neuron': NeuronChallenge,
    'bias': BiasChallenge,
    'my_new_concept': MyNewChallenge,  # Add your challenge
}
```

#### 3. Add to Level
```python
# src/states/level_state.py
def _load_level_challenges(self, level_name):
    challenge_map = {
        'Neuron Academy': ['neuron'],
        'Bias Battlefield': ['bias'],
        'My New Level': ['my_new_concept'],  # Add your level
    }
    return challenge_map.get(level_name, [])
```

### Creating a New Boss Battle

#### 1. Define Boss Questions
```python
# src/challenges/boss_battles.py
MY_NEW_BOSS_QUESTIONS = [
    {
        'question': 'What is the primary purpose of [concept]?',
        'options': [
            'Option A - Correct answer',
            'Option B - Incorrect',
            'Option C - Incorrect',
            'Option D - Incorrect'
        ],
        'correct': 0,
        'explanation': 'Detailed explanation of why A is correct...',
        'difficulty': 'medium'
    },
    # Add more questions...
]

BOSS_QUESTIONS = {
    'My New Boss': MY_NEW_BOSS_QUESTIONS,
}
```

#### 2. Add Boss to Level Data
```python
# src/constants.py
LEVEL_DATA = {
    'My New Level': {
        'name': 'My New Level',
        'pos': (400, 500),
        'unlocked': False,
        'concept': 'My New Concept',
        'boss': 'My New Boss',
        'type': 'advanced'
    },
}
```

### Adding New UI Components

#### 1. Create Component Class
```python
# src/ui/my_component.py
import pygame
from .modern_ui import UIComponent

class MyCustomComponent(UIComponent):
    def __init__(self, rect, **kwargs):
        super().__init__(rect)
        self.custom_property = kwargs.get('custom_property', 'default')
        
    def render(self, screen):
        # Custom rendering logic
        pygame.draw.rect(screen, self.color, self.rect)
        
    def handle_event(self, event):
        # Custom event handling
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.on_click()
```

#### 2. Use in Game States
```python
# In any game state
from src.ui.my_component import MyCustomComponent

class MyGameState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.my_component = MyCustomComponent(
            rect=pygame.Rect(100, 100, 200, 50),
            custom_property='special_value'
        )
```

## 🧪 Testing Guide

### Test Structure
```
tests/
├── unit/                  # Unit tests (isolated components)
│   ├── test_game.py
│   ├── test_challenges.py
│   └── test_ui.py
├── integration/           # Integration tests (component interaction)
│   ├── test_state_transitions.py
│   └── test_challenge_system.py
└── e2e/                  # End-to-end tests (full workflows)
    ├── test_game_flow.py
    └── test_level_progression.py
```

### Writing Tests

#### Unit Test Example
```python
# tests/unit/test_my_challenge.py
import pytest
from unittest.mock import Mock, patch
from src.challenges.my_new_challenge import MyNewChallenge

class TestMyNewChallenge:
    def setup_method(self):
        """Set up test fixtures"""
        self.challenge = MyNewChallenge()
        self.challenge.initialize()
    
    def test_initialization(self):
        """Test that challenge initializes correctly"""
        assert self.challenge.concept_name == "My New Concept"
        assert self.challenge.difficulty == "intermediate"
        assert not self.challenge.completed
    
    def test_parameter_adjustment(self):
        """Test parameter adjustment functionality"""
        initial_lr = self.challenge.parameters['learning_rate']
        self.challenge._increase_parameter()
        assert self.challenge.parameters['learning_rate'] > initial_lr
    
    @patch('pygame.event.get')
    def test_event_handling(self, mock_events):
        """Test event handling with mocked pygame events"""
        mock_event = Mock()
        mock_event.type = pygame.KEYDOWN
        mock_event.key = pygame.K_UP
        mock_events.return_value = [mock_event]
        
        initial_value = self.challenge.parameters[self.challenge.current_parameter]
        self.challenge.handle_event(mock_event)
        final_value = self.challenge.parameters[self.challenge.current_parameter]
        
        assert final_value > initial_value
    
    def test_solution_checking(self):
        """Test solution validation"""
        # Set up parameters for a correct solution
        self.challenge.parameters['learning_rate'] = 0.001
        self.challenge.parameters['epochs'] = 200
        
        # Mock the accuracy calculation to return high accuracy
        with patch.object(self.challenge, '_calculate_accuracy', return_value=0.95):
            result = self.challenge.check_solution()
            assert result is True
            assert self.challenge.completed is True
            assert self.challenge.score > 0
```

#### Integration Test Example
```python
# tests/integration/test_challenge_integration.py
import pytest
from unittest.mock import Mock
from src.game import Game
from src.states.level_state import LevelState

class TestChallengeIntegration:
    def setup_method(self):
        """Set up integration test environment"""
        self.mock_screen = Mock()
        self.game = Game(self.mock_screen, 1200, 800)
        
    def test_level_challenge_loading(self):
        """Test that levels load challenges correctly"""
        level_state = LevelState(self.game)
        level_data = {
            'name': 'Test Level',
            'concept': 'Test Concept',
            'boss': 'Test Boss'
        }
        
        level_state.initialize_level(level_data)
        assert level_state.current_challenge is not None
        assert level_state.level_data == level_data
    
    def test_challenge_completion_progression(self):
        """Test that completing challenges unlocks progression"""
        level_state = LevelState(self.game)
        level_state.initialize_level({'name': 'Test Level'})
        
        # Simulate challenge completion
        level_state.current_challenge.completed = True
        level_state.current_challenge.score = 1000
        
        level_state._handle_challenge_completion()
        
        # Check that progress was recorded
        assert self.game.player_progress['Test Level']['completed'] is True
        assert self.game.player_progress['Test Level']['score'] == 1000
```

### Running Tests
```bash
# All tests
python scripts/run_tests.py all

# Quick unit tests only
python scripts/run_tests.py quick

# Specific test file
python scripts/run_tests.py tests/unit/test_my_challenge.py

# With coverage report
python scripts/run_tests.py coverage

# Code quality checks
python scripts/run_tests.py quality
```

### Test Coverage Goals
- **Overall Coverage**: 80%+
- **Core Game Logic**: 100%
- **Challenge System**: 90%+
- **UI Components**: 70%+
- **Integration Points**: 85%+

## 🚀 Build & Distribution

### Building Executables

#### For Current Platform
```bash
python scripts/build_executable.py
```

#### Platform-Specific Builds
```bash
# macOS (run on macOS)
./scripts/build_macos.sh

# Windows (run on Windows)
scripts\build_windows.bat

# Linux (run on Linux)
./scripts/build_linux.sh
```

### Build Configuration
```python
# scripts/build_executable.py configuration
PYINSTALLER_OPTIONS = {
    'name': 'NeuralNetworkAdventure',
    'onefile': True,
    'windowed': True,  # No console window
    'icon': 'assets/icon.ico',
    'add_data': [
        ('src', 'src'),
        ('assets', 'assets'),
    ],
    'hidden_imports': [
        'pygame',
        'numpy',
        'matplotlib',
        'pygame_gui',
        'pyttsx3',
    ],
}
```

### Distribution Checklist
- [ ] All tests pass
- [ ] Code quality checks pass
- [ ] Documentation updated
- [ ] Version numbers bumped
- [ ] Cross-platform builds tested
- [ ] Performance benchmarks maintained
- [ ] Security review completed

## 📚 API Reference

### Core Classes

#### Game Class
```python
class Game:
    """Main game class managing states and player progress"""
    
    def __init__(self, screen, width, height):
        """Initialize game with display surface and dimensions"""
        
    def change_state(self, state_name, **kwargs):
        """Change to a different game state"""
        
    def handle_event(self, event):
        """Handle pygame events and delegate to current state"""
        
    def update(self, dt):
        """Update game logic with delta time"""
        
    def render(self):
        """Render current game state"""
```

#### BaseState Class
```python
class BaseState(ABC):
    """Abstract base class for all game states"""
    
    @abstractmethod
    def handle_event(self, event):
        """Handle pygame events"""
        
    @abstractmethod
    def update(self, dt):
        """Update state logic with delta time"""
        
    @abstractmethod
    def render(self, screen):
        """Render state to screen"""
```

#### BaseChallenge Class
```python
class BaseChallenge(ABC):
    """Abstract base class for educational challenges"""
    
    def __init__(self):
        """Initialize challenge with default values"""
        
    @abstractmethod
    def initialize(self):
        """Set up challenge-specific parameters and UI"""
        
    @abstractmethod
    def handle_event(self, event):
        """Handle user input and interactions"""
        
    @abstractmethod
    def update(self, dt):
        """Update challenge state and animations"""
        
    @abstractmethod
    def render(self, screen):
        """Render challenge visualization"""
        
    @abstractmethod
    def check_solution(self):
        """Validate user's solution and return success"""
        
    @abstractmethod
    def get_hint(self):
        """Provide contextual help for current situation"""
```

### Utility Functions

#### Neural Network Utilities
```python
# src/utils/neural_utils.py
def sigmoid(x):
    """Sigmoid activation function"""
    
def relu(x):
    """ReLU activation function"""
    
def forward_pass(inputs, weights, bias, activation='sigmoid'):
    """Execute forward pass through single layer"""
    
def calculate_gradient(output, target, inputs):
    """Calculate gradient for backpropagation"""
```

#### UI Utilities
```python
# src/ui/ui_utils.py
def draw_rounded_rect(surface, color, rect, radius):
    """Draw rectangle with rounded corners"""
    
def render_text_with_shadow(surface, text, font, color, shadow_color, pos):
    """Render text with drop shadow effect"""
    
def create_gradient_surface(size, start_color, end_color, vertical=True):
    """Create surface with gradient fill"""
```

### Event System
```python
# Custom events for game communication
CHALLENGE_COMPLETED = pygame.USEREVENT + 1
BOSS_DEFEATED = pygame.USEREVENT + 2
LEVEL_UNLOCKED = pygame.USEREVENT + 3
PARAMETER_CHANGED = pygame.USEREVENT + 4

# Event data structure
event_data = {
    'type': CHALLENGE_COMPLETED,
    'challenge_name': 'neuron_challenge',
    'score': 1000,
    'understanding_level': 0.85
}
```

## 🔧 Advanced Topics

### Performance Optimization

#### Rendering Optimization
```python
# Use dirty rectangle updates
class OptimizedRenderer:
    def __init__(self):
        self.dirty_rects = []
        
    def mark_dirty(self, rect):
        """Mark area as needing redraw"""
        self.dirty_rects.append(rect)
        
    def render_dirty_areas(self, screen):
        """Only redraw marked areas"""
        for rect in self.dirty_rects:
            # Redraw only this area
            pass
        self.dirty_rects.clear()
```

#### Memory Management
```python
# Object pooling for frequently created objects
class ObjectPool:
    def __init__(self, object_class, initial_size=10):
        self.object_class = object_class
        self.available = [object_class() for _ in range(initial_size)]
        self.in_use = []
        
    def get_object(self):
        """Get object from pool"""
        if self.available:
            obj = self.available.pop()
            self.in_use.append(obj)
            return obj
        else:
            # Create new if pool empty
            obj = self.object_class()
            self.in_use.append(obj)
            return obj
            
    def return_object(self, obj):
        """Return object to pool"""
        if obj in self.in_use:
            self.in_use.remove(obj)
            obj.reset()  # Reset object state
            self.available.append(obj)
```

### Custom Visualization

#### Neural Network Renderer
```python
class NeuralNetworkRenderer:
    """Advanced neural network visualization"""
    
    def __init__(self, network_structure):
        self.layers = network_structure
        self.neuron_positions = self._calculate_positions()
        self.connection_weights = {}
        
    def render_network(self, screen, weights, activations):
        """Render complete network with weights and activations"""
        self._render_connections(screen, weights)
        self._render_neurons(screen, activations)
        self._render_data_flow(screen)
        
    def animate_forward_pass(self, screen, data_flow):
        """Animate data flowing through network"""
        for layer_idx, layer_data in enumerate(data_flow):
            self._animate_layer_activation(screen, layer_idx, layer_data)
```

### Plugin System

#### Challenge Plugin Interface
```python
class ChallengePlugin:
    """Interface for challenge plugins"""
    
    @property
    def name(self):
        """Plugin name"""
        return "My Challenge Plugin"
        
    @property
    def version(self):
        """Plugin version"""
        return "1.0.0"
        
    def get_challenges(self):
        """Return list of challenges provided by this plugin"""
        return [MyCustomChallenge, AnotherChallenge]
        
    def initialize(self, game):
        """Initialize plugin with game instance"""
        pass
```

## 🤝 Contributing Guidelines

### Code Style
- **Follow PEP 8**: Python style guidelines
- **Use Type Hints**: For better code clarity
- **Write Docstrings**: Document all public functions and classes
- **Line Length**: Maximum 88 characters (Black formatter)

### Git Workflow
```bash
# Create feature branch
git checkout -b feature/my-new-feature

# Make changes and commit
git add .
git commit -m "feat: add new neural network challenge"

# Push and create pull request
git push origin feature/my-new-feature
```

### Pull Request Checklist
- [ ] Tests pass locally
- [ ] Code formatted with Black
- [ ] Type hints added
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)

---

## 🎉 You're Ready to Develop!

This guide covers the essentials of developing for Neural Network Adventure RPG. For more specific information:

- **Architecture Details**: See [PROJECT_ARCHITECTURE.md](../../PROJECT_ARCHITECTURE.md)
- **Contributing**: See [docs/CONTRIBUTING.md](../CONTRIBUTING.md)
- **API Documentation**: Generated docs in `docs/api/`
- **User Guide**: See [docs/user_guide/README.md](../user_guide/README.md)

**Happy coding, and welcome to the Neural Network Adventure development team!** 🧠💻✨

---

<div align="center">

**[⬆️ Back to Top](#-neural-network-adventure-rpg---developer-guide)** | **[🏠 Main README](../../README.md)** | **[🎮 User Guide](../user_guide/README.md)**

</div>