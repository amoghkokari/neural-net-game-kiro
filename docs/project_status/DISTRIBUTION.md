# Neural Network Adventure RPG - Distribution Guide

## Building Executables for Multiple Platforms

This guide explains how to create one-click executables for macOS (Silicon), Windows, and Linux.

### Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install pyinstaller
   ```

2. **Build for Your Platform**:
   ```bash
   python build_executable.py
   ```

3. **Find Your Executable**:
   - Check the `dist/` folder for your platform-specific build

### Platform-Specific Instructions

#### macOS (Silicon/Intel)
```bash
# Use the dedicated script
./build_macos.sh

# Or manually
python build_executable.py
```
**Output**: `Neural Network Adventure.app` bundle

#### Windows
```batch
# Use the dedicated script
build_windows.bat

# Or manually
python build_executable.py
```
**Output**: `NeuralNetworkAdventure.exe`

#### Linux
```bash
# Use the dedicated script
./build_linux.sh

# Or manually
python build_executable.py
```
**Output**: `NeuralNetworkAdventure` binary

### Cross-Platform Building

To build for multiple platforms, you'll need to run the build process on each target platform:

1. **macOS builds** require macOS (for app signing and bundling)
2. **Windows builds** require Windows (for proper .exe generation)
3. **Linux builds** work on Linux (various distributions supported)

### Distribution Structure

Each build creates a folder with:
```
dist/neural-network-adventure-{platform}/
├── NeuralNetworkAdventure[.exe/.app]
├── README.txt
└── [platform-specific files]
```

### File Sizes

Approximate executable sizes:
- **macOS**: ~150-200MB (app bundle)
- **Windows**: ~100-150MB (.exe)
- **Linux**: ~100-150MB (binary)

### Dependencies Included

The executable includes all required dependencies:
- Python runtime
- Pygame 2.5.2
- NumPy 1.24.3
- Matplotlib 3.7.2
- pygame-gui 0.6.9
- pyttsx3 2.90 (text-to-speech)

### Troubleshooting

#### Build Fails
- Ensure Python 3.8+ is installed
- Install PyInstaller: `pip install pyinstaller`
- Check that all source files are present

#### Executable Won't Run
- **macOS**: Allow in Security & Privacy settings
- **Windows**: Click "More info" → "Run anyway" in Windows Defender
- **Linux**: Make executable with `chmod +x`

#### Missing Source Files
- Ensure all game source files are in the `src/` directory
- Check that `requirements.txt` is present

### Advanced Configuration

#### Custom Icons
Icons can be added to build configuration:
- `icon.ico` for Windows builds
- `icon.icns` for macOS builds

#### Build Options
Edit `neural_network_adventure.spec` to customize:
- Hidden imports
- Data files
- Build options
- App metadata

### Testing Builds

Before distribution, test on clean systems:
1. Copy executable to a machine without Python/dependencies
2. Run the executable
3. Verify all game features work
4. Test on different OS versions

### Distribution Checklist

- [ ] Build tested on target platform
- [ ] README.txt included
- [ ] File permissions set correctly
- [ ] Virus scan completed (Windows)
- [ ] Code signing (macOS, optional)
- [ ] Installer created (optional)

### Performance Notes

- First launch may be slower (extracting bundled files)
- Subsequent launches are faster
- Executable size includes full Python runtime
- No internet connection required to run

---

**Ready to share your Neural Network Adventure!** 🎮🧠