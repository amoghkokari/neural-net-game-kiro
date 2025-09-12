# 🧠🎮 Neural Network Adventure RPG

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Pygame 2.5.2](https://img.shields.io/badge/pygame-2.5.2-green.svg)](https://www.pygame.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/tests-in%20development-yellow.svg)](tests/)
[![Game Status](https://img.shields.io/badge/game-playable-brightgreen.svg)](main.py)

> **Learn neural networks through epic RPG adventures!** 🚀

An educational RPG game that teaches neural network concepts through interactive challenges and visualizations. Learn fundamental neural network concepts including neurons, weights, bias, activation functions, and forward propagation through hands-on gameplay.

![Game Screenshot](docs/images/gameplay-preview.png)

## 🎯 What You'll Learn

### 📚 Neural Network Fundamentals
- **Foundation Concepts**: Neurons, weights, bias, activation functions
- **Network Building**: Perceptrons and forward propagation
- **Interactive Learning**: Real-time parameter adjustment and visualization
- **Progressive Difficulty**: 6 levels covering core concepts

### 🎮 Interactive Learning Features
- **Real-Time Visualization**: Watch neural networks compute as you adjust parameters
- **Educational Challenges**: Step-by-step learning with immediate feedback
- **Progressive Levels**: 6 levels from basic neurons to forward propagation
- **Visual Feedback**: See how changes affect network behavior instantly

## 🚀 Quick Start

### Option 1: macOS Executable (Recommended)
Download the pre-built macOS executable:

- **macOS**: `builds/Neural-Network-Adventure-macOS-Complete.zip` (20MB native executable)
- **Requirements**: macOS 10.14+ (Mojave or later)
- **Status**: Complete and tested

### Option 2: Run from Source
```bash
# Set up virtual environment (if not already done)
python -m venv navenv
source navenv/bin/activate  # On Windows: navenv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the game
python main.py
```



## 🎮 Game Features

### ✨ What Makes It Special
- **🧠 Educational Excellence**: Learn by doing, not just reading
- **🎨 Modern UI/UX**: Professional game design and polish
- **🔊 Audio Narration**: Text-to-speech brings characters to life
- **📊 Real-Time Visualization**: Watch neural networks compute
- **⚡ 60 FPS Gameplay**: Smooth, responsive experience
- **🔄 Instant Retry**: No frustration, just learning

### � Aovailable Levels
Currently implemented levels with interactive challenges:
- **Neuron Academy** - Basic neurons and computation
- **Bias Battlefield** - Bias and activation thresholds  
- **Activation Peaks** - Activation functions (Sigmoid, ReLU, etc.)
- **Chain Rule Caverns** - Derivatives and chain rule
- **Perceptron Plains** - Multi-layer perceptron networks
- **Forward Pass Forest** - Forward propagation mastery

### 🎯 Learning Progression
```
Level 1: Neuron Academy     → Basic neurons and weights
Level 2: Bias Battlefield   → Thresholds and activation
Level 3: Activation Peaks   → Activation functions
Level 4: Chain Rule Caverns → Derivatives and chain rule
Level 5: Perceptron Plains  → Multi-layer perceptrons
Level 6: Forward Pass Forest → Forward propagation
```

## 🎮 Controls

### 🕹️ Navigation
- **Arrow Keys / WASD**: Navigate menus and world map
- **SPACE / ENTER**: Select options and advance dialogue
- **ESC**: Return to previous screen or exit

### 🎮 Interactive Challenges
- **Arrow Keys**: Navigate through challenge options
- **SPACE**: Confirm selections and advance
- **R**: Reset parameters to try different values

### 🔧 Challenges
- **Left/Right**: Select parameter to adjust
- **Up/Down**: Increase/decrease values
- **R**: Reset to random values
- **SPACE**: Continue/confirm actions

## 🛠️ For Developers

### 🏗️ Clean Project Structure
```
neural-network-adventure/
├── 📄 main.py                    # 🎮 Game entry point
├── 📄 README.md                  # 📖 Project overview (this file)
├── 📄 LICENSE                    # ⚖️ MIT license
├── 📄 CHANGELOG.md               # 📝 Version history
├── 📄 STRUCTURE.md               # 📁 Detailed project organization
├── 📄 requirements*.txt          # 📦 Dependencies
│
├── 📁 src/                       # 💻 Main source code
├── 📁 tests/                     # 🧪 Comprehensive test suite  
├── 📁 docs/                      # 📚 Documentation
├── 📁 scripts/                   # 🔧 Development tools
├── 📁 assets/                    # 🎨 Game assets
└── 📁 config/                    # ⚙️ Configuration files
```

**📁 [See STRUCTURE.md](STRUCTURE.md) for complete directory details**

### 🧪 Testing
```bash
# Test framework is set up but requires pytest installation
pip install pytest pytest-cov pytest-mock

# Run tests (when pytest is installed)
python scripts/run_tests.py quick
```

### 📦 Building Executables
```bash
# macOS executable already available in builds/
# For other platforms, PyInstaller can be used:
pip install pyinstaller
pyinstaller main.py --onefile --name NeuralNetworkAdventure
```

### 🤝 Contributing
We welcome contributions! Please see:
- [Contributing Guidelines](docs/CONTRIBUTING.md)
- [Code of Conduct](docs/CODE_OF_CONDUCT.md)
- [Game Design](docs/GAME_DESIGN.md)

## 📋 System Requirements

### Minimum Requirements
- **OS**: macOS 10.14+, Windows 10+, or Linux (Ubuntu 18.04+)
- **Python**: 3.8+ (for source code)
- **Memory**: 4GB RAM
- **Storage**: 500MB free space
- **Graphics**: OpenGL 2.1 support

### Recommended
- **Memory**: 8GB RAM for smooth experience
- **Graphics**: Dedicated GPU for best performance
- **Audio**: Speakers or headphones for narration

## 🎓 Educational Impact

### 🎯 Learning Outcomes
By playing this game, players will:
- ✅ Understand fundamental neural network concepts (neurons, weights, bias)
- ✅ Learn about activation functions and their effects
- ✅ Grasp forward propagation in neural networks
- ✅ See real-time visualization of network behavior
- ✅ Build intuition for how neural networks compute

### 👥 Target Audience
- **Students**: Learning AI/ML in computer science courses
- **Developers**: Wanting to understand neural networks deeply
- **Educators**: Teaching AI concepts through interactive methods
- **Professionals**: Transitioning into AI/ML careers

### 📊 Educational Approach
- **Interactive Learning**: Learn by doing rather than just reading
- **Visual Feedback**: See immediate results of parameter changes
- **Progressive Difficulty**: Build understanding step by step
- **Hands-On Experience**: Direct manipulation of neural network parameters

## 📈 Roadmap

### 🚀 Version 1.0 (Current)
- ✅ 6 interactive learning levels
- ✅ Real-time neural network visualization
- ✅ Educational challenges with immediate feedback
- ✅ macOS executable available

### 🔮 Future Development
- 🔄 Additional neural network concepts (backpropagation, training)
- 🔄 More interactive challenges and visualizations
- 🔄 Cross-platform executables (Windows, Linux)
- 🔄 Enhanced educational content and progression

## 🤝 Community

### 💬 Get Involved
- **GitHub Issues**: Report bugs and suggest features
- **Discussions**: Share feedback and ideas

### 🐛 Report Issues
Found a bug or have a suggestion? Please:
1. Check existing issues in the repository
2. Create a new issue with details
3. Include your OS, Python version, and steps to reproduce

### 💝 Support the Project
- ⭐ **Star this repository** to show your support
- 🐦 **Share on social media** to help others discover it
- 💰 **Sponsor development** for faster feature releases
- 🤝 **Contribute code** to make it even better

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

### 🎨 Inspiration
- **3Blue1Brown**: For making neural networks visually intuitive
- **Pygame Community**: For the amazing game development framework
- **Educational Game Developers**: For proving learning can be fun

### 🛠️ Built With
- [Pygame](https://www.pygame.org/) - Game development framework
- [NumPy](https://numpy.org/) - Numerical computations
- [Matplotlib](https://matplotlib.org/) - Visualization components
- [pygame-gui](https://pygame-gui.readthedocs.io/) - Modern UI elements
- [pyttsx3](https://pyttsx3.readthedocs.io/) - Text-to-speech narration

### 👥 Contributors
- Initial development and game design
- Community contributors welcome!

---

## 🚀 Ready to Start Your Neural Network Adventure?

```bash
# Run the game
python main.py
```

**Transform your understanding of neural networks through the power of play!** 🧠🎮✨

---

<div align="center">

**[⬆️ Back to Top](#-neural-network-adventure-rpg)** | **[� Doocumentation](docs/)** | **[🤝 Contribute](docs/CONTRIBUTING.md)**

Made with ❤️ for the AI learning community

</div>