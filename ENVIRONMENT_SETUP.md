# Object Detective - Environment Setup Guide

This guide will help you set up the environment variables and dependencies needed to run the Object Detective project successfully.

## 🚀 Quick Start

Choose your platform and run the appropriate setup script:

### Windows (Command Prompt)
```cmd
setup_env.bat
```

### Windows (PowerShell)
```powershell
.\setup_env.ps1
```

### Linux/Mac (Bash)
```bash
chmod +x setup_env.sh
./setup_env.sh
```

## 📋 What the Setup Scripts Do

1. **Set Environment Variables** - Configure all necessary environment variables
2. **Create Virtual Environment** - Set up an isolated Python environment
3. **Install Dependencies** - Install all required packages from `requirements.txt`
4. **Test Basic Functionality** - Verify that core modules can be imported
5. **Provide Usage Instructions** - Show you how to test and run the project

## 🔧 Environment Variables Set

| Variable | Purpose | Default Value |
|----------|---------|---------------|
| `OBJECT_DETECTIVE_ROOT` | Project root directory | Current directory |
| `OBJECT_DETECTIVE_CONFIG` | Configuration file path | `./config.json` |
| `OBJECT_DETECTIVE_TEMPLATES` | Templates directory | `./templates` |
| `OBJECT_DETECTIVE_EXAMPLES` | Examples directory | `./examples` |
| `PYTHONPATH` | Python module search path | Includes src/ and utils/ |
| `OPENCV_LOG_LEVEL` | OpenCV logging level | `ERROR` |
| `PYAUTOGUI_FAILSAFE` | PyAutoGUI safety feature | `False` |
| `PYAUTOGUI_PAUSE` | PyAutoGUI delay between actions | `0.01` |

## 🧪 Testing the Environment

After running the setup script, test your environment:

```bash
python test_environment.py
```

This comprehensive test will verify:
- ✅ Environment variables are set correctly
- ✅ Project structure is complete
- ✅ All dependencies are installed
- ✅ Core modules can be imported
- ✅ Task 3 enhancements are working
- ✅ Configuration is valid
- ✅ Example scripts are available

## 🎯 Quick Test Commands

Once setup is complete, try these commands:

### 1. Help and Options
```bash
python main.py --help
```

### 2. Motion Detection Demo
```bash
python main.py --motion-detect --test-detection
```

### 3. Color Tracking Demo
```bash
python main.py --color-detect --red-range --test-detection
```

### 4. Enhanced Mouse Demo (Task 3)
```bash
python examples/enhanced_mouse_demo.py
```

### 5. Interactive Motion Tracker
```bash
python examples/motion_tracker.py
```

## 📦 Dependencies Installed

The setup scripts install these packages:

| Package | Version | Purpose |
|---------|---------|---------|
| `opencv-python` | 4.8.1.78 | Computer vision and image processing |
| `numpy` | 1.24.3 | Numerical computing |
| `pyautogui` | 0.9.54 | Mouse and keyboard automation |
| `pillow` | 10.0.1 | Image processing |

## 🎮 Task 3 Features Tested

The environment setup specifically tests these Task 3 enhancements:

- ✅ **Enhanced Mouse Controller**
  - `move_to_box()` method for smooth cursor movement
  - `click_box()` method for optional clicking
  - New configuration options: `move_duration`, `enable_click`

- ✅ **Throttling System**
  - Prevents excessive mouse movement
  - Configurable movement intervals

- ✅ **Configuration Validation**
  - Validates new mouse settings
  - Ensures proper configuration structure

## 🛠️ Manual Environment Setup

If the automated scripts don't work, you can set up manually:

### 1. Create Virtual Environment
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Set Environment Variables

**Windows (Command Prompt):**
```cmd
set PYTHONPATH=%CD%;%CD%\src;%CD%\utils
set OBJECT_DETECTIVE_ROOT=%CD%
set OBJECT_DETECTIVE_CONFIG=%CD%\config.json
```

**Linux/Mac (Bash):**
```bash
export PYTHONPATH="$(pwd):$(pwd)/src:$(pwd)/utils"
export OBJECT_DETECTIVE_ROOT="$(pwd)"
export OBJECT_DETECTIVE_CONFIG="$(pwd)/config.json"
```

**PowerShell:**
```powershell
$env:PYTHONPATH = "$(pwd);$(pwd)\src;$(pwd)\utils"
$env:OBJECT_DETECTIVE_ROOT = "$(pwd)"
$env:OBJECT_DETECTIVE_CONFIG = "$(pwd)\config.json"
```

## 🔍 Troubleshooting

### Common Issues

1. **"ModuleNotFoundError"**
   - Ensure virtual environment is activated
   - Check that `PYTHONPATH` includes `src/` and `utils/`
   - Reinstall dependencies: `pip install -r requirements.txt`

2. **"OpenCV import error"**
   - Try: `pip uninstall opencv-python && pip install opencv-python`
   - On Linux: `sudo apt-get install libopencv-dev`
   - On Mac: `brew install opencv`

3. **"PyAutoGUI permission error"**
   - On macOS: Grant accessibility permissions to Terminal
   - On Linux: Ensure X11 display is available

4. **"Template not found"**
   - Create template images in the `templates/` directory
   - Use PNG format for best results

### Platform-Specific Notes

**Windows:**
- Use Command Prompt or PowerShell as Administrator if needed
- Ensure Python is in your PATH

**Linux:**
- Install additional packages: `sudo apt-get install python3-tk python3-dev`
- Ensure you have X11 display access

**macOS:**
- Install Homebrew dependencies: `brew install python-tk`
- Grant security permissions for automation

## 📁 Project Structure Verification

After setup, your directory should look like:

```
Object Detective/
├── 📄 setup_env.bat           # Windows batch setup
├── 📄 setup_env.sh            # Linux/Mac setup  
├── 📄 setup_env.ps1           # PowerShell setup
├── 📄 test_environment.py     # Environment test script
├── 📄 env_config.txt          # Environment variables reference
├── 📄 config.json            # Project configuration
├── 📄 main.py                # Main application
├── 📄 requirements.txt       # Python dependencies
├── 📁 .venv/                 # Virtual environment
├── 📁 src/                   # Core source code
├── 📁 utils/                 # Utility modules
├── 📁 examples/              # Example scripts
└── 📁 templates/             # Template images
```

## 🎉 Success!

If all tests pass, you're ready to run Object Detective! Try the enhanced mouse features:

```bash
# Enable auto-clicking in config.json:
# "mouse": { "enable_click": true, "move_duration": 0.1 }

python main.py --motion-detect
```

The cursor will now move to detected objects with proper throttling and safety features! 🎯 