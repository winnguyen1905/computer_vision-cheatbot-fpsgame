# Real-Time Object Tracker

🎯 **Detect objects on screen in real-time and move mouse to their location**

A modern Python application that uses computer vision to detect objects on your screen and automatically move your mouse cursor to their location. Perfect for gaming automation, UI testing, and accessibility tools.

## ✨ Features

- **Real-time object detection** using template matching or color detection
- **Smooth mouse movement** with configurable speed and easing
- **Multiple detection methods**: Template matching, color-based detection
- **Gaming automation** with auto-click functionality
- **Configurable tracking** with JSON configuration files
- **Modern architecture** with clean, modular code

## 🚀 Quick Start

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd realtime_object_tracker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run basic tracking**
   ```bash
   # Track using a template image
   python main.py --template templates/target_object.png
   
   # Track red objects on screen
   python main.py --color-detect --red-range
   ```

## 📖 Usage Examples

### Template-Based Detection
```bash
# Track a specific UI element
python main.py --template templates/button.png

# Track with auto-click enabled
python main.py --template templates/target.png --auto-click
```

### Color-Based Detection
```bash
# Track red objects
python main.py --color-detect --red-range

# Track blue objects with custom FPS
python main.py --color-detect --blue-range --fps 60
```

### Advanced Usage
```bash
# Use custom configuration file
python main.py --config my_config.json --template my_target.png

# Verbose logging for debugging
python main.py --template target.png --verbose
```

## 🛠️ Configuration

Edit `config.json` to customize tracking behavior:

```json
{
  "tracking": {
    "fps": 30,
    "confidence_threshold": 0.8,
    "smooth_movement": true,
    "movement_speed": 0.3
  },
  "detection": {
    "method": "template",
    "template_path": "templates/target_object.png"
  },
  "mouse": {
    "auto_click": false,
    "click_delay": 0.1
  }
}
```

## 📁 Project Structure

```
realtime_object_tracker/
├── main.py              # Main application entry point
├── requirements.txt     # Required Python packages
├── config.json         # Configuration file
├── src/                # Core source code
│   ├── object_detector.py    # Object detection logic
│   ├── screen_capture.py     # Screen capturing
│   ├── mouse_controller.py   # Mouse movement control
│   └── tracker_system.py     # Main coordination system
├── templates/          # Template images for detection
├── examples/           # Ready-to-use examples
└── utils/             # Helper utilities
```

## 🎮 Use Cases

- **Gaming Automation**: Auto-aim, target tracking, resource collection
- **UI Testing**: Automated clicking, form filling, app testing
- **Accessibility**: Eye-tracking alternatives, assistive technology
- **Productivity**: Automated workflows, repetitive task automation

## 🔧 Development

### Adding New Detection Methods

1. Extend `ObjectDetector` class in `src/object_detector.py`
2. Update `TrackerSystem` to support new method
3. Add configuration options in `config.json`

### Creating Custom Templates

1. Take a screenshot of the object you want to track
2. Crop to show only the target object
3. Save as PNG in the `templates/` folder
4. Reference in your configuration or command line

## 📝 Requirements

- Python 3.7+
- OpenCV 4.8+
- NumPy 1.24+
- PyAutoGUI 0.9+
- Pillow 10.0+

## ⚠️ Important Notes

- **Screen Resolution**: Works best with consistent screen resolution
- **Template Quality**: Use high-quality, distinct template images
- **Performance**: Higher FPS requires more CPU resources
- **Permissions**: May require accessibility permissions on some systems

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

1. **"Template not found"**: Ensure template file exists and path is correct
2. **"No objects detected"**: Adjust confidence threshold or try different template
3. **Mouse not moving**: Check system permissions for mouse control
4. **Performance issues**: Lower FPS or reduce tracking region

### Getting Help

- Check the `examples/` folder for working implementations
- Review configuration options in `config.json`
- Enable verbose logging with `--verbose` flag 