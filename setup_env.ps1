# Object Detective - PowerShell Environment Setup
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Object Detective - Environment Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Set project root directory
$PROJECT_ROOT = $PSScriptRoot

Write-Host "Setting up environment variables..." -ForegroundColor Yellow

# Python path configuration
$env:PYTHONPATH = "$PROJECT_ROOT;$PROJECT_ROOT\src;$PROJECT_ROOT\utils;$env:PYTHONPATH"

# OpenCV environment variables
$env:OPENCV_LOG_LEVEL = "ERROR"
$env:OPENCV_FFMPEG_CAPTURE_OPTIONS = "rtbufsize;50M"

# PyAutoGUI safety and configuration
$env:PYAUTOGUI_FAILSAFE = "False"
$env:PYAUTOGUI_PAUSE = "0.01"

# Display and graphics settings
$env:QT_DEVICE_PIXEL_RATIO = "auto"
$env:QT_AUTO_SCREEN_SCALE_FACTOR = "1"

# Performance settings
$env:OPENBLAS_NUM_THREADS = "4"
$env:MKL_NUM_THREADS = "4"
$env:OMP_NUM_THREADS = "4"

# Object Detective specific settings
$env:OBJECT_DETECTIVE_ROOT = $PROJECT_ROOT
$env:OBJECT_DETECTIVE_CONFIG = "$PROJECT_ROOT\config.json"
$env:OBJECT_DETECTIVE_TEMPLATES = "$PROJECT_ROOT\templates"
$env:OBJECT_DETECTIVE_EXAMPLES = "$PROJECT_ROOT\examples"
$env:OBJECT_DETECTIVE_LOG_LEVEL = "INFO"

# Development settings
$env:PYTHONDONTWRITEBYTECODE = "1"
$env:PYTHONUNBUFFERED = "1"

Write-Host "Environment variables set successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Project Root: $PROJECT_ROOT" -ForegroundColor Gray
Write-Host "Config File: $env:OBJECT_DETECTIVE_CONFIG" -ForegroundColor Gray
Write-Host "Templates Dir: $env:OBJECT_DETECTIVE_TEMPLATES" -ForegroundColor Gray
Write-Host ""

# Check if virtual environment exists
if (Test-Path ".venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & .venv\Scripts\Activate.ps1
    Write-Host "Virtual environment activated!" -ForegroundColor Green
} else {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    try {
        python -m venv .venv
        & .venv\Scripts\Activate.ps1
        Write-Host "Virtual environment created and activated!" -ForegroundColor Green
    } catch {
        Write-Host "Error: Failed to create virtual environment" -ForegroundColor Red
        Write-Host "Please ensure Python is installed and accessible" -ForegroundColor Red
        Read-Host "Press Enter to exit..."
        exit 1
    }
}

Write-Host ""
Write-Host "Installing/Upgrading dependencies..." -ForegroundColor Yellow
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "Warning: Some dependencies may not have installed correctly" -ForegroundColor Yellow
    Write-Host "You may need to install them manually" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Environment Setup Complete!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Available commands:" -ForegroundColor White
Write-Host "  python main.py --help                    : Show all options" -ForegroundColor Gray
Write-Host "  python main.py --motion-detect           : Motion detection demo" -ForegroundColor Gray
Write-Host "  python main.py --color-detect --red-range: Color tracking demo" -ForegroundColor Gray
Write-Host "  python examples/enhanced_mouse_demo.py   : Enhanced mouse demo" -ForegroundColor Gray
Write-Host "  python examples/unified_detector.py      : Unified interface demo" -ForegroundColor Gray
Write-Host ""
Write-Host "To test the project:" -ForegroundColor White
Write-Host "  1. Run: python main.py --test-detection --motion-detect" -ForegroundColor Gray
Write-Host "  2. Try: python examples/motion_tracker.py" -ForegroundColor Gray
Write-Host "  3. Demo: python examples/enhanced_mouse_demo.py" -ForegroundColor Gray
Write-Host ""

# Test basic imports
Write-Host "Testing basic functionality..." -ForegroundColor Yellow
$testScript = @"
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
"@

python -c $testScript

Write-Host ""
Write-Host "Environment setup complete! You can now run Object Detective." -ForegroundColor Green
Write-Host "Press any key to continue..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 