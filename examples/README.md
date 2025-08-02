# Example Scripts

This folder contains ready-to-use example scripts demonstrating different use cases for the Real-Time Object Tracker.

## 📁 Available Examples

### 1. `simple_tracker.py` - Basic Object Tracking
**Purpose**: Simple template-based object tracking with mouse following
**Use Case**: Learning the basics, testing templates

```bash
python examples/simple_tracker.py
```

**Features**:
- Template-based detection
- Real-time mouse tracking
- Event callbacks for found/lost objects
- Performance statistics
- Verbose logging

**Requirements**:
- Create `templates/target_object.png` template

---

### 2. `gaming_bot.py` - Gaming Automation
**Purpose**: Automated targeting and clicking for games
**Use Case**: Game automation, auto-aim assistance

```bash
python examples/gaming_bot.py
```

**Features**:
- High-performance tracking (60 FPS)
- Auto-click on target detection
- Gaming-optimized mouse settings
- Target hit statistics
- 5-second startup delay

**Requirements**:
- Create `templates/enemy.png` template

---

### 3. `ui_automation.py` - UI Testing & Automation
**Purpose**: Automated UI interaction and testing
**Use Case**: Application testing, workflow automation

```bash
python examples/ui_automation.py
```

**Features**:
- Multi-step automation sequences
- Various click actions (click, double-click, right-click)
- Template validation testing
- Retry logic with configurable attempts
- Loop automation support

**Requirements**:
- Create UI element templates (buttons, icons, etc.)

---

### 4. `color_tracker.py` - Color-Based Tracking
**Purpose**: Track objects by color range instead of templates
**Use Case**: Tracking colored objects, markers, highlights

```bash
python examples/color_tracker.py
```

**Features**:
- HSV color space detection
- 10+ predefined color presets
- Custom color range support
- Color-optimized settings
- Interactive color selection

**Requirements**:
- Colored objects on screen (no templates needed)

---

## 🚀 Quick Start Guide

### Step 1: Choose Your Use Case
- **Learning/Testing**: Start with `simple_tracker.py`
- **Gaming**: Use `gaming_bot.py`
- **UI Automation**: Try `ui_automation.py`
- **Color Tracking**: Use `color_tracker.py`

### Step 2: Prepare Templates (if needed)
For template-based examples:
1. Take a screenshot of your target object
2. Crop the image to show only the object
3. Save as PNG in the `templates/` folder
4. Use descriptive names

### Step 3: Run the Example
```bash
# Navigate to project root
cd /path/to/realtime_object_tracker

# Run an example
python examples/simple_tracker.py
```

### Step 4: Customize for Your Needs
- Modify tracking settings (FPS, confidence, etc.)
- Add custom callbacks
- Adjust mouse behavior
- Create automation sequences

---

## 🛠️ Customization Examples

### Basic Template Tracking
```python
from src.tracker_system import TrackerSystem

tracker = TrackerSystem()
tracker.load_template("my_template.png")
tracker.set_tracking_speed(30)
tracker.start_tracking()
```

### Color-Based Tracking
```python
tracker = TrackerSystem()
tracker.track_by_color(
    lower_color=(0, 100, 100),    # Lower HSV bound
    upper_color=(10, 255, 255),   # Upper HSV bound
    color_space='HSV'
)
tracker.start_tracking()
```

### Gaming Configuration
```python
tracker = TrackerSystem()
tracker.load_template("enemy.png")
tracker.set_tracking_speed(60)
tracker.enable_auto_click(True)
tracker.update_mouse_settings(
    movement_speed=0.9,
    smooth_movement=True
)
tracker.start_tracking()
```

### UI Automation Sequence
```python
from examples.ui_automation import UIAutomation

automation = UIAutomation()
automation.add_step("templates/login_button.png", "click", wait_time=2.0)
automation.add_step("templates/username_field.png", "click", wait_time=1.0)
automation.add_step("templates/submit_button.png", "click", wait_time=3.0)
automation.execute_automation(loop=False)
```

---

## 📊 Performance Tips

### For Gaming (High Performance)
- Use 60+ FPS tracking
- Lower confidence threshold (0.7-0.8)
- Fast mouse movement (0.8+)
- Small, distinct templates

### For UI Automation (Reliability)
- Use 10-30 FPS tracking
- Higher confidence threshold (0.85+)
- Slower mouse movement (0.3-0.5)
- Clear, high-contrast templates

### For Color Tracking (Accuracy)
- Use 30 FPS tracking
- Lower confidence threshold (0.3-0.5)
- Adjust HSV ranges for lighting conditions
- Test different color spaces if needed

---

## 🐛 Troubleshooting

### Template Not Detected
1. Check template quality and contrast
2. Adjust confidence threshold
3. Use `--verbose` flag for debugging
4. Test with `test_detection()` method

### Mouse Not Moving Smoothly
1. Adjust `movement_speed` setting
2. Enable/disable `smooth_movement`
3. Check system permissions
4. Reduce tracking FPS if CPU usage is high

### Color Detection Issues
1. Test different HSV ranges
2. Check lighting conditions
3. Use color picker tools for accurate ranges
4. Try different color spaces (HSV, RGB, BGR)

### Performance Problems
1. Lower tracking FPS
2. Reduce screen capture region
3. Close unnecessary applications
4. Use template caching for multiple detections

---

## 🎯 Next Steps

1. **Modify Examples**: Customize existing examples for your specific needs
2. **Create New Scripts**: Combine features from different examples
3. **Add Features**: Extend the core system with new capabilities
4. **Share Templates**: Create and share template libraries
5. **Optimize Performance**: Fine-tune settings for your hardware

---

## 📖 Further Reading

- Check `../README.md` for full project documentation
- Review `../src/` modules for API details
- See `../templates/README.md` for template creation guide
- Visit configuration docs in `../config.json` 