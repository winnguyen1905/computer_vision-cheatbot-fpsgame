#!/usr/bin/env python3
"""
Unified Object Detection Example
Demonstrates the simplified interface for real-time object detection with visual feedback
"""

import sys
import os
from pathlib import Path

# Add parent src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from tracker_system import TrackerSystem
from utils.config_loader import ConfigLoader
from utils.logger import setup_logger

def demo_motion_detection():
    """Demo motion detection with visual feedback"""
    print("=== Motion Detection Demo ===")
    
    # Configuration for motion detection
    config = {
        "capture_region": {
            "top": 100,
            "left": 100, 
            "width": 800,
            "height": 600
        },
        "detection": {
            "method": "motion",
            "min_area": 1000,
            "motion_threshold": 30,
            "dilate_iterations": 3,
            "blur_kernel_size": 15
        },
        "mouse": {
            "auto_click": False,
            "click_delay": 0.1
        }
    }
    
    # Create tracker using unified interface
    tracker = TrackerSystem(config)
    
    # Run visual detection loop
    tracker.run()

def demo_color_detection():
    """Demo color detection with visual feedback"""
    print("=== Color Detection Demo ===")
    
    config = {
        "capture_region": {
            "top": 0,
            "left": 0,
            "width": 1920,
            "height": 1080
        },
        "detection": {
            "method": "color"
        },
        "mouse": {
            "auto_click": False
        }
    }
    
    tracker = TrackerSystem(config)
    
    # Configure to track red objects
    tracker.track_by_color(
        lower_color=(0, 100, 100),
        upper_color=(10, 255, 255),
        color_space='HSV'
    )
    
    # Run visual detection loop
    tracker.run()

def demo_config_file():
    """Demo loading from config file"""
    print("=== Config File Demo ===")
    
    # Create tracker from config file
    tracker = TrackerSystem(config_path='config.json')
    
    # Run visual detection loop (uses config method)
    tracker.run()

def demo_unified_interface():
    """Demo the exact interface pattern requested by user"""
    print("=== Unified Interface Demo ===")
    
    # This matches the user's exact requested pattern:
    class SimpleTracker(TrackerSystem):
        def __init__(self, config_path: str):
            # Load config using config loader
            cfg = ConfigLoader(config_path).load()
            
            super().__init__(cfg)
            
            # Set up unified interface properties
            self.region = cfg["capture_region"]
            self.detector = self.object_detector  # Already set in parent
            self.mouse = self.mouse_controller     # Already set in parent
    
    # Create simple tracker
    tracker = SimpleTracker('config.json')
    
    print("Starting real-time tracking. Press 'q' to quit.")
    
    # The run() method is inherited and provides the exact interface:
    # - grab_frame(self.region)
    # - self.detector.detect(frame)  
    # - self.mouse.click_box(box)
    # - cv2.imshow with annotations
    
    tracker.run()

def test_detection_methods():
    """Test different detection methods"""
    logger = setup_logger(verbose=True)
    
    config = {
        "capture_region": {"top": 100, "left": 100, "width": 800, "height": 600},
        "detection": {"method": "motion", "min_area": 500},
        "mouse": {"auto_click": False}
    }
    
    tracker = TrackerSystem(config)
    
    print("Testing motion detection...")
    result = tracker.test_detection(save_result=True)
    if result.found:
        print(f"Motion detected! Confidence: {result.confidence:.3f}")
    else:
        print("No motion detected")
    
    # Switch to different method
    tracker.track_by_color(
        lower_color=(100, 100, 100),  # Blue range
        upper_color=(130, 255, 255),
        color_space='HSV'
    )
    
    print("Testing color detection...")
    result = tracker.test_detection(save_result=True) 
    if result.found:
        print(f"Blue object detected! Confidence: {result.confidence:.3f}")
    else:
        print("No blue objects detected")

def main():
    """Main demo selector"""
    print("Unified Object Detection Demo")
    print("Choose a demo:")
    print("1. Motion Detection")
    print("2. Color Detection") 
    print("3. Config File")
    print("4. Unified Interface")
    print("5. Test Detection Methods")
    print("0. Exit")
    
    try:
        choice = input("Enter choice (0-5): ").strip()
        
        if choice == '1':
            demo_motion_detection()
        elif choice == '2':
            demo_color_detection()
        elif choice == '3':
            demo_config_file()
        elif choice == '4':
            demo_unified_interface()
        elif choice == '5':
            test_detection_methods()
        elif choice == '0':
            print("Goodbye!")
        else:
            print("Invalid choice")
            
    except KeyboardInterrupt:
        print("\nDemo interrupted")
    except Exception as e:
        print(f"Demo error: {e}")

if __name__ == "__main__":
    main() 