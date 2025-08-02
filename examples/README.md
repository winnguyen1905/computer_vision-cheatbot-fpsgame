# Object Detective Examples

This directory contains example scripts demonstrating different features of the Object Detective system.

## Examples

### 🎯 **motion_tracker.py**
Demonstrates motion detection using frame differencing with statistics and callbacks.

```bash
python examples/motion_tracker.py
```

### 🎨 **color_tracker.py**  
Shows color-based object detection and tracking.

```bash
python examples/color_tracker.py
```

### 🖱️ **simple_tracker.py**
Basic template-based object tracking example.

```bash
python examples/simple_tracker.py
```

### 🎮 **gaming_bot.py**
Game automation example using object detection.

```bash
python examples/gaming_bot.py
```

### 🖥️ **ui_automation.py**
UI automation examples for desktop applications.

```bash
python examples/ui_automation.py
```

### 🔧 **unified_detector.py** *(NEW)*
**Comprehensive example demonstrating the unified detection interface with real-time visual feedback.**

Features:
- Motion detection with live annotations
- Color detection with HSV filtering  
- Config file integration
- Visual OpenCV display with bounding boxes
- Mouse interaction with detected objects
- Performance statistics overlay

```bash
python examples/unified_detector.py
```

#### Interactive Demo Menu:
1. **Motion Detection** - Real-time motion tracking with visual feedback
2. **Color Detection** - Track objects by color with live annotations
3. **Config File** - Load settings from `config.json`
4. **Unified Interface** - Shows the exact pattern requested by user
5. **Test Detection Methods** - Compare different detection algorithms

## 🚀 **New Unified Interface Pattern**

The system now supports a simplified interface matching the requested pattern:

```python
from tracker_system import TrackerSystem
from screen_capture import grab_frame
from utils.config_loader import ConfigLoader

class MyTracker(TrackerSystem):
    def __init__(self, config_path: str):
        cfg = ConfigLoader(config_path).load()
        super().__init__(cfg)
        
        self.region = cfg["capture_region"] 
        self.detector = self.object_detector  # Unified detector
        self.mouse = self.mouse_controller     # Mouse controller

    def run(self):
        print("Starting real-time tracking. Press 'q' to quit.")
        while True:
            # 1) Capture frame
            frame = grab_frame(self.region)
            
            # 2) Detect objects - returns List[(x,y,w,h)]
            boxes = self.detector.detect(frame)
            
            # 3) Process detections
            for (x, y, w, h) in boxes:
                # 3a) Draw rectangle
                cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
                
                # 3b) Mouse interaction
                self.mouse.click_box((x, y, w, h))
            
            # 4) Show annotated frame
            cv2.imshow("Object Detective", frame)
            
            # 5) Exit on 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        cv2.destroyAllWindows()
```

## 🎯 **Detection Methods**

### Motion Detection
```python
config = {
    "detection": {
        "method": "motion",
        "min_area": 1000,
        "motion_threshold": 30
    }
}
tracker = TrackerSystem(config)
tracker.run()  # Visual detection loop
```

### Template Matching
```python
tracker = TrackerSystem(config)
tracker.load_template("template.png")
tracker.run()
```

### Color Detection  
```python
tracker = TrackerSystem(config)
tracker.track_by_color(
    lower_color=(0, 100, 100),    # HSV lower
    upper_color=(10, 255, 255),   # HSV upper
    color_space='HSV'
)
tracker.run()
```

## 🖥️ **Visual Features**

- **Live Bounding Boxes**: Green rectangles around detected objects
- **Statistics Overlay**: Object count and detection info
- **Method Indicator**: Shows current detection algorithm
- **Area Display**: Object size information
- **Mouse Tracking**: Real-time cursor movement to objects
- **OpenCV Display**: Press 'q' to quit, window close detection

## 📊 **Performance Monitoring**

All examples include performance statistics:
- Frames per second (FPS)
- Detection count and rate
- Processing time metrics
- Runtime statistics

## 🛠️ **Configuration**

Examples use `config.json` for settings:

```json
{
  "capture_region": {"left": 100, "top": 100, "width": 800, "height": 600},
  "detection": {"method": "motion", "min_area": 500},
  "mouse": {"auto_click": false}
}
```

## 🎮 **Usage Patterns**

### Visual Detection (with OpenCV display)
```bash
python examples/unified_detector.py  # Interactive menu
```

### Headless Detection (no display)
```python
tracker.run_headless()  # Background processing
```

### Single Frame Testing
```python
result = tracker.test_detection(save_result=True)
```

### Command Line Interface
```bash
python main.py --motion-detect --region 100 100 800 600
``` 