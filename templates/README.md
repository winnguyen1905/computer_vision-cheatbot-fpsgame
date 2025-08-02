# Template Images

This folder contains template images used for object detection. Templates are used to find specific objects on your screen using template matching.

## How to Create Templates

1. **Take a Screenshot**: Capture your screen when the target object is visible
2. **Crop the Object**: Use an image editor to crop just the object you want to track
3. **Save as PNG**: Save the cropped image as a PNG file in this folder
4. **Use Clear Images**: Ensure the template is clear and distinct from the background

## Template Guidelines

### Good Templates:
- ✅ High contrast with background
- ✅ Unique visual features
- ✅ Consistent size and appearance
- ✅ Clear, sharp edges
- ✅ PNG format with transparency if needed

### Avoid:
- ❌ Templates with changing content (text, numbers)
- ❌ Very small objects (< 20x20 pixels)
- ❌ Objects that blend with background
- ❌ Screenshots with compression artifacts
- ❌ Templates with inconsistent appearance

## Example Templates

Create templates for common use cases:

- **target_object.png** - Main target to track
- **button.png** - UI button to click
- **icon.png** - Application icon or symbol
- **enemy.png** - Game enemy or target
- **item.png** - Inventory item or resource

## Usage in Code

```python
from src.tracker_system import TrackerSystem

# Load and use template
tracker = TrackerSystem()
tracker.load_template("templates/button.png")
tracker.start_tracking()
```

## Template Testing

Use the test detection feature to verify your templates:

```bash
# Test template detection
python main.py --template templates/your_template.png --verbose
```

## Tips for Better Detection

1. **Multiple Templates**: Create different templates for the same object at different scales
2. **Confidence Threshold**: Adjust the confidence threshold in config.json if needed
3. **Regular Updates**: Update templates if the UI or game graphics change
4. **Backup Templates**: Keep backup templates for different scenarios

## Template Naming Convention

Use descriptive names for your templates:
- `game_enemy_red.png`
- `ui_close_button.png`
- `app_search_icon.png`
- `dialog_ok_button.png` 