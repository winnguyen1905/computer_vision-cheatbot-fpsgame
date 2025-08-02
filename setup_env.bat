@echo off
echo ========================================
echo Object Detective - Environment Setup
echo ========================================

REM Set project root directory
set PROJECT_ROOT=%~dp0
set PROJECT_ROOT=%PROJECT_ROOT:~0,-1%

echo Setting up environment variables...

REM Python path configuration
set PYTHONPATH=%PROJECT_ROOT%;%PROJECT_ROOT%\src;%PROJECT_ROOT%\utils;%PYTHONPATH%

REM OpenCV environment variables
set OPENCV_LOG_LEVEL=ERROR
set OPENCV_FFMPEG_CAPTURE_OPTIONS=rtbufsize;50M

REM PyAutoGUI safety and configuration
set PYAUTOGUI_FAILSAFE=False
set PYAUTOGUI_PAUSE=0.01

REM Display and graphics settings
set QT_DEVICE_PIXEL_RATIO=auto
set QT_AUTO_SCREEN_SCALE_FACTOR=1

REM Performance settings
set OPENBLAS_NUM_THREADS=4
set MKL_NUM_THREADS=4
set OMP_NUM_THREADS=4

REM Object Detective specific settings
set OBJECT_DETECTIVE_ROOT=%PROJECT_ROOT%
set OBJECT_DETECTIVE_CONFIG=%PROJECT_ROOT%\config.json
set OBJECT_DETECTIVE_TEMPLATES=%PROJECT_ROOT%\templates
set OBJECT_DETECTIVE_EXAMPLES=%PROJECT_ROOT%\examples
set OBJECT_DETECTIVE_LOG_LEVEL=INFO

echo Environment variables set successfully!
echo.
echo Project Root: %PROJECT_ROOT%
echo Config File: %OBJECT_DETECTIVE_CONFIG%
echo Templates Dir: %OBJECT_DETECTIVE_TEMPLATES%
echo.

REM Check if virtual environment exists
if exist ".venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
    echo Virtual environment activated!
) else (
    echo Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo Error: Failed to create virtual environment
        echo Please ensure Python is installed and accessible
        pause
        exit /b 1
    )
    call .venv\Scripts\activate.bat
    echo Virtual environment created and activated!
)

echo.
echo Installing/Upgrading dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if errorlevel 1 (
    echo Warning: Some dependencies may not have installed correctly
    echo You may need to install them manually
)

echo.
echo ========================================
echo Environment Setup Complete!
echo ========================================
echo.
echo Available commands:
echo   python main.py --help                    : Show all options
echo   python main.py --motion-detect           : Motion detection demo
echo   python main.py --color-detect --red-range: Color tracking demo
echo   python examples/enhanced_mouse_demo.py   : Enhanced mouse demo
echo   python examples/unified_detector.py      : Unified interface demo
echo.
echo To test the project:
echo   1. Run: python main.py --test-detection --motion-detect
echo   2. Try: python examples/motion_tracker.py
echo   3. Demo: python examples/enhanced_mouse_demo.py
echo.

REM Test basic imports
echo Testing basic functionality...
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

echo.
echo Press any key to continue...
pause >nul 