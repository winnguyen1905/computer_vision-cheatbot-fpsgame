#!/bin/bash

echo "========================================"
echo "Object Detective - Environment Setup"
echo "========================================"

# Set project root directory
export PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Setting up environment variables..."

# Python path configuration
export PYTHONPATH="${PROJECT_ROOT}:${PROJECT_ROOT}/src:${PROJECT_ROOT}/utils:${PYTHONPATH}"

# OpenCV environment variables
export OPENCV_LOG_LEVEL=ERROR
export OPENCV_FFMPEG_CAPTURE_OPTIONS="rtbufsize:50M"

# PyAutoGUI safety and configuration
export PYAUTOGUI_FAILSAFE=False
export PYAUTOGUI_PAUSE=0.01

# Display and graphics settings (especially for Linux)
export DISPLAY=${DISPLAY:-:0}
export QT_DEVICE_PIXEL_RATIO=auto
export QT_AUTO_SCREEN_SCALE_FACTOR=1

# Performance settings
export OPENBLAS_NUM_THREADS=4
export MKL_NUM_THREADS=4
export OMP_NUM_THREADS=4

# Object Detective specific settings
export OBJECT_DETECTIVE_ROOT="${PROJECT_ROOT}"
export OBJECT_DETECTIVE_CONFIG="${PROJECT_ROOT}/config.json"
export OBJECT_DETECTIVE_TEMPLATES="${PROJECT_ROOT}/templates"
export OBJECT_DETECTIVE_EXAMPLES="${PROJECT_ROOT}/examples"
export OBJECT_DETECTIVE_LOG_LEVEL=INFO

# Linux specific settings for GUI applications
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    export QT_X11_NO_MITSHM=1
    export XAUTHORITY=${XAUTHORITY:-$HOME/.Xauthority}
fi

echo "Environment variables set successfully!"
echo ""
echo "Project Root: ${PROJECT_ROOT}"
echo "Config File: ${OBJECT_DETECTIVE_CONFIG}"
echo "Templates Dir: ${OBJECT_DETECTIVE_TEMPLATES}"
echo ""

# Check if virtual environment exists
if [[ -f ".venv/bin/activate" ]]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
    echo "Virtual environment activated!"
else
    echo "Creating virtual environment..."
    python3 -m venv .venv
    if [[ $? -ne 0 ]]; then
        echo "Error: Failed to create virtual environment"
        echo "Please ensure Python 3 is installed and accessible"
        exit 1
    fi
    source .venv/bin/activate
    echo "Virtual environment created and activated!"
fi

echo ""
echo "Installing/Upgrading dependencies..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if [[ $? -ne 0 ]]; then
    echo "Warning: Some dependencies may not have installed correctly"
    echo "You may need to install them manually"
    echo ""
    echo "For Ubuntu/Debian, you might need:"
    echo "  sudo apt-get install python3-tk python3-dev libopencv-dev"
    echo ""
    echo "For macOS, you might need:"
    echo "  brew install python-tk opencv"
fi

echo ""
echo "========================================"
echo "Environment Setup Complete!"
echo "========================================"
echo ""
echo "Available commands:"
echo "  python main.py --help                    : Show all options"
echo "  python main.py --motion-detect           : Motion detection demo"
echo "  python main.py --color-detect --red-range: Color tracking demo"
echo "  python examples/enhanced_mouse_demo.py   : Enhanced mouse demo"
echo "  python examples/unified_detector.py      : Unified interface demo"
echo ""
echo "To test the project:"
echo "  1. Run: python main.py --test-detection --motion-detect"
echo "  2. Try: python examples/motion_tracker.py"
echo "  3. Demo: python examples/enhanced_mouse_demo.py"
echo ""

# Test basic imports
echo "Testing basic functionality..."
python -c "
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))
sys.path.insert(0, os.path.join(os.getcwd(), 'utils'))

try:
    print('Testing imports...')
    from config_loader import ConfigLoader
    print('✓ ConfigLoader imported successfully')
    
    config_loader = ConfigLoader('config.json')
    config = config_loader.load()
    print('✓ Configuration loaded successfully')
    
    # Test without heavy dependencies
    print('✓ Basic functionality test passed')
    print('Ready to run Object Detective!')
    
except Exception as e:
    print(f'✗ Import test failed: {e}')
    print('Some dependencies may be missing')
"

echo ""
echo "Environment setup complete! You can now run Object Detective."
echo "To activate this environment in future sessions, run:"
echo "  source .venv/bin/activate  # (then export the environment variables above)" 