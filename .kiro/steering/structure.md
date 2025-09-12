# Project Structure & Architecture

## Directory Organization

```
src/                           # Main source code
├── game.py                    # Core game class with state management
├── constants.py               # Game constants, enums, colors
├── game_story.py              # Story system and narrative
├── states/                    # Game state implementations
│   ├── base_state.py          # Abstract base class for all states
│   ├── menu_state.py          # Main menu
│   ├── world_map_state.py     # Level selection map
│   ├── level_state.py         # Individual level gameplay
│   └── coding_challenge_state.py # Interactive coding challenges
├── challenges/                # Educational challenge implementations
│   ├── base_challenge.py      # Abstract base class for challenges
│   ├── neuron_challenge.py    # Basic neuron concepts
│   ├── bias_challenge.py      # Bias and thresholds
│   ├── perceptron_challenge.py # Complete perceptron implementation
│   └── [other challenges...]
├── character/                 # Character system
│   └── alex_character.py      # Main protagonist
├── ui/                        # User interface components
│   ├── clean_layout.py        # Clean UI layouts
│   ├── modern_ui.py           # Modern UI components
│   └── responsive_layout.py   # Responsive design system
├── visualization/             # Neural network visualization
│   └── neural_viz.py          # Real-time network rendering
└── audio/                     # Audio and speech systems
    └── speech_system.py       # Text-to-speech integration

tests/                         # Test suite
├── unit/                      # Unit tests (isolated components)
├── integration/               # Integration tests (component interaction)
└── e2e/                       # End-to-end tests (full game flow)
```

## Architecture Patterns

### State Pattern
- All game screens inherit from `BaseState`
- State transitions managed by main `Game` class
- Each state handles its own events, updates, and rendering

### Challenge System
- All educational challenges inherit from `BaseChallenge`
- Consistent interface for initialization, event handling, and solution checking
- Modular design allows easy addition of new neural network concepts

### Visualization Architecture
- `NeuralNetworkVisualizer` provides reusable components
- Real-time rendering with animation support
- Separation of visualization logic from game logic

## Naming Conventions

### Files & Directories
- Snake_case for all Python files: `neural_viz.py`
- Descriptive names indicating purpose: `coding_challenge_state.py`
- Group related functionality in directories: `challenges/`, `states/`

### Classes
- PascalCase: `BaseChallenge`, `NeuralNetworkVisualizer`
- Descriptive names ending with type: `MenuState`, `BiasChallenge`

### Constants
- ALL_CAPS in constants.py: `SCREEN_WIDTH`, `NEURON_INPUT_COLOR`
- Grouped by category with clear prefixes

## Code Organization Principles

### Separation of Concerns
- Game logic separate from visualization
- State management isolated in dedicated classes
- Challenge logic independent of UI rendering

### Inheritance Hierarchy
- Base classes provide common interface and shared functionality
- Concrete implementations focus on specific behavior
- Consistent method signatures across similar classes

### Player Progress Tracking
- Centralized in main `Game` class
- Persistent data structure for completed levels, scores, implementations
- Character progression tied to learning achievements