# Object Detective

A real-time object detection and tracking system with advanced AI-powered detection capabilities, designed for gaming applications with customizable configuration options.

## 🎯 Overview

Object Detective is a sophisticated computer vision application that uses YOLO (You Only Look Once) models for real-time object detection. The system features:

- **Real-time AI Detection**: Powered by YOLO models for accurate object detection
- **Multiple Capture Methods**: Support for Bettercam, OBS Virtual Camera, and MSS screen capture
- **Advanced Mouse Control**: Multiple input methods including Arduino, GHub, and Razer drivers
- **Customizable Configuration**: Comprehensive GUI-based configuration manager
- **Performance Optimization**: Circle capture mode and configurable detection windows
- **Anti-Detection Features**: Arduino-based input methods for enhanced stealth

## 🚀 Features

### Core Detection
- **AI-Powered Detection**: Uses YOLO models for real-time object detection
- **Multi-Class Detection**: Detects players, bots, weapons, heads, and other game objects
- **Tracking Support**: Optional ByteTrack integration for object tracking
- **Circle Capture Mode**: Circular detection area for improved focus and performance

### Capture Methods
- **Bettercam**: GPU-accelerated screen capture (Recommended)
- **OBS Virtual Camera**: Integration with OBS Studio
- **MSS**: Python-based screen capture (Fallback method)

### Input Methods
- **Arduino**: Hardware-based mouse control for anti-detection
- **Logitech G HUB**: GHub driver integration
- **Razer**: Razer driver integration
- **Standard**: Win32 API mouse control

### Configuration
- **GUI Configuration Manager**: User-friendly interface for all settings
- **Real-time Validation**: Input validation and error checking
- **Hotkey Support**: Customizable hotkeys for all functions
- **Performance Monitoring**: Built-in debug window with performance metrics

## 📋 Requirements

### System Requirements
- **OS**: Windows 10/11
- **Python**: 3.8 or higher
- **CUDA**: 12.1 or higher (for GPU acceleration)
- **RAM**: 8GB minimum, 16GB recommended
- **GPU**: NVIDIA GPU with CUDA support (recommended)

### Hardware Requirements
- **Mouse**: Any mouse with configurable DPI
- **Arduino**: Optional - for hardware-based input (recommended for anti-detection)

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Object-Detective
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install CUDA (Required for GPU Acceleration)
1. Download and install CUDA Toolkit 12.1 or higher from [NVIDIA's website](https://developer.nvidia.com/cuda-downloads)
2. Install PyTorch with CUDA support:
```bash
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

### 4. Download AI Models
Place your YOLO models in the `models/` directory:
- `windz-1.1.pt` (included)
- `sunxds_0.5.6.pt` (included)
- Or use your own custom models

## ⚙️ Configuration

### GUI Configuration Manager
Launch the configuration GUI:
```bash
python run.py --gui
```

### Manual Configuration
Edit `config.ini` directly for advanced users.

### Key Configuration Sections

#### Detection Window
```ini
[Detection window]
detection_window_width = 300
detection_window_height = 300
circle_capture = True
```

#### Capture Methods
```ini
[Capture Methods]
capture_fps = 60
Bettercam_capture = False
Obs_capture = False
mss_capture = True
```

#### AI Settings
```ini
[AI]
AI_model_name = windz-1.1.pt
AI_model_image_size = 640
AI_conf = 0.2
AI_device = 0
```

#### Mouse Settings
```ini
[Mouse]
mouse_dpi = 1000
mouse_sensitivity = 2.0
mouse_fov_width = 40
mouse_fov_height = 40
```

## 🎮 Usage

### Basic Usage
1. **Configure Settings**: Run `python run.py --gui` to configure
2. **Start Detection**: Run `python run.py` to start detection
3. **Use Hotkeys**:
   - `RightMouseButton`: Enable aiming assistance
   - `F2`: Exit application
   - `F3`: Pause/resume detection
   - `F4`: Reload configuration

### Advanced Usage

#### Arduino Setup (Recommended)
1. Connect Arduino with USB Host Shield
2. Upload Arduino code (see Arduino documentation)
3. Enable Arduino options in configuration
4. Set port to 'auto' for automatic detection

#### OBS Virtual Camera Setup
1. Install OBS Studio
2. Add Virtual Camera source
3. Enable OBS capture in configuration
4. Set camera ID to 'auto' for automatic detection

#### Performance Optimization
- Use smaller detection windows (300x300) for better performance
- Enable circle capture mode
- Use Bettercam capture method
- Adjust AI confidence threshold based on needs

## 🔧 Configuration Options

### Detection Settings
- **Window Size**: 100-1920 pixels width/height
- **Circle Capture**: Circular detection area
- **FPS**: 1-240 capture frame rate

### AI Settings
- **Model**: Choose from available YOLO models
- **Image Size**: 320, 640, or 1280 pixels
- **Confidence**: 0.1-1.0 detection threshold
- **Device**: CPU or GPU device selection

### Mouse Settings
- **DPI**: Your actual mouse DPI setting
- **Sensitivity**: In-game sensitivity multiplier
- **FOV**: Field of view for detection area
- **Speed Multipliers**: Min/max movement speed

### Capture Methods
- **Bettercam**: Fastest, GPU-accelerated
- **OBS**: Good performance, requires OBS setup
- **MSS**: Slowest but most compatible

## 🎯 Supported Object Classes

The system detects the following object classes:
- **Player**: Human players
- **Bot**: AI-controlled entities
- **Weapon**: Weapons and equipment
- **Head**: Head targets for precision
- **Dead Body**: Fallen players
- **Hideout Targets**: Training targets
- **Smoke/Fire**: Environmental effects
- **Third Person**: Third-person view indicators

## 🔒 Anti-Detection Features

### Arduino Integration
- Hardware-based mouse control
- Bypasses software detection
- Configurable baud rate and port settings
- 16-bit mouse support

### Driver Options
- **GHub**: Logitech G HUB driver
- **Razer**: Razer driver
- **Standard**: Win32 API (fallback)

### Stealth Features
- Random window names
- Configurable hotkeys
- Minimal resource usage
- Background operation

## 🐛 Troubleshooting

### Common Issues

#### CUDA Not Available
```bash
# Uninstall existing PyTorch
pip uninstall torch torchvision torchaudio

# Install CUDA version
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

#### Model Loading Error
- Ensure model file exists in `models/` directory
- Check model format compatibility
- Verify CUDA installation

#### Capture Issues
- Try different capture methods
- Check monitor configuration
- Verify GPU drivers

#### Arduino Connection
- Check USB connection
- Verify Arduino IDE is closed
- Install USB Host Shield library
- Disable debugging in settings.h

### Performance Issues
- Reduce detection window size
- Lower capture FPS
- Use circle capture mode
- Enable GPU acceleration
- Close unnecessary applications

## 📁 Project Structure

```
Object Detective/
├── config.ini              # Main configuration file
├── gui_config.py           # GUI configuration manager
├── gui_helpers.py          # GUI helper functions
├── run.py                  # Main application entry point
├── requirements.txt        # Python dependencies
├── logic/                  # Core application logic
│   ├── arduino.py         # Arduino integration
│   ├── buttons.py         # Key code definitions
│   ├── capture.py         # Screen capture methods
│   ├── checks.py          # System validation
│   ├── config_watcher.py  # Configuration management
│   ├── frame_parser.py    # Detection result parsing
│   ├── ghub.py           # Logitech G HUB integration
│   ├── hotkeys_watcher.py # Hotkey monitoring
│   ├── logger.py         # Logging functionality
│   ├── mouse.py          # Mouse control logic
│   ├── overlay.py        # Visual overlay system
│   ├── rzctl.py         # Razer driver integration
│   ├── shooting.py       # Shooting mechanics
│   ├── visual.py        # Debug window and visuals
│   ├── game.yaml        # YOLO model configuration
│   └── tracker.yaml     # Tracking configuration
├── models/                # AI model directory
│   ├── windz-1.1.pt     # Primary detection model
│   └── sunxds_0.5.6.pt  # Alternative model
└── run_*.bat            # Windows batch files
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is for educational and research purposes only. Users are responsible for complying with local laws and regulations.

## ⚠️ Disclaimer

This software is provided "as is" without warranty. The authors are not responsible for any misuse or damage caused by this software. Users are responsible for:

- Complying with local laws and regulations
- Using the software responsibly
- Understanding the implications of automated detection systems
- Respecting terms of service for target applications

## 🔗 Links

- **Documentation**: See inline code comments and configuration files
- **Models**: Find improved models at [Boosty](https://boosty.to/sunone) and [Patreon](https://www.patreon.com/sunone)
- **Issues**: Report bugs and feature requests through GitHub issues

## 📞 Support

For support and questions:
- Check the troubleshooting section
- Review configuration options
- Test with different settings
- Ensure all requirements are met

---

**Note**: This software is designed for educational purposes and legitimate use cases. Users must ensure compliance with applicable laws and regulations in their jurisdiction. 