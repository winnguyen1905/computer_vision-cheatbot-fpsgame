# Object Detective - Environment Setup Guide

## Quick Setup (Recommended)

### Windows
```bash
# Method 1: Use the automated setup script
setup_env.bat

# Method 2: Manual setup
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### Linux/macOS
```bash
# Use the automated setup script
./setup_env.sh

# Or manual setup
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

## Troubleshooting Common Issues

### 1. ModuleNotFoundError: No module named 'cv2'

**Problem**: OpenCV is not installed in your Python environment.

**Solution**:
```bash
# Update pip and install build dependencies
pip install --upgrade pip setuptools wheel

# Install dependencies from requirements.txt
pip install -r requirements.txt

# Verify installation
python -c "import cv2; print('OpenCV version:', cv2.__version__)"
```

### 2. Numpy Build Errors

**Problem**: Build dependencies missing for numpy compilation.

**Solution**:
```bash
# Install build tools first
pip install setuptools wheel

# Use updated requirements with flexible versions
pip install -r requirements.txt
```

### 3. Virtual Environment Issues

**Problem**: Dependencies installed in wrong environment.

**Solution**:
```bash
# Create and activate virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Dependency Versions

Current compatible versions:
- opencv-python >= 4.8.0
- numpy >= 1.24.0
- pyautogui >= 0.9.54
- pillow >= 10.0.0

## Verification

Test your setup:
```bash
# Test basic functionality
python main.py --help

# Test environment
python test_environment.py

# Test detection
python main.py --test-detection --motion-detect
```

## Environment Variables (Optional)

For advanced usage, set these environment variables:
```bash
export OBJECT_DETECTIVE_ROOT=/path/to/project
export OBJECT_DETECTIVE_CONFIG=/path/to/config.json
export PYTHONPATH=$PYTHONPATH:/path/to/project/src:/path/to/project/utils
```

## Python Version Compatibility

- **Recommended**: Python 3.9 - 3.13
- **Minimum**: Python 3.8
- **Tested on**: Python 3.13.3

## Platform Support

- ✅ Windows 10/11
- ✅ Linux (Ubuntu 20.04+)
- ✅ macOS (10.15+)

## Performance Optimization

For better performance:
```bash
# Set environment variables
export OPENCV_LOG_LEVEL=ERROR
export PYAUTOGUI_PAUSE=0.01
export OMP_NUM_THREADS=4
``` 