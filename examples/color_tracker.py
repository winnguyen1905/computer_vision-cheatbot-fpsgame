#!/usr/bin/env python3
"""
Color-Based Tracker Example
Track objects by color range instead of template matching
"""

import sys
import time
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from src.tracker_system import TrackerSystem
from utils.logger import setup_logger


class ColorTracker:
    """Color-based object tracking system"""
    
    def __init__(self):
        self.logger = setup_logger("ColorTracker", verbose=True)
        self.tracker = TrackerSystem()
        
        # Predefined color ranges (HSV format)
        self.color_ranges = {
            'red': {
                'lower': (0, 100, 100),
                'upper': (10, 255, 255),
                'description': 'Red objects (like red buttons, markers)'
            },
            'red2': {  # Second red range (wraps around HSV)
                'lower': (170, 100, 100),
                'upper': (180, 255, 255),
                'description': 'Red objects (upper HSV range)'
            },
            'green': {
                'lower': (40, 100, 100),
                'upper': (80, 255, 255),
                'description': 'Green objects (like green buttons, nature)'
            },
            'blue': {
                'lower': (100, 100, 100),
                'upper': (130, 255, 255),
                'description': 'Blue objects (like blue buttons, water)'
            },
            'yellow': {
                'lower': (20, 100, 100),
                'upper': (30, 255, 255),
                'description': 'Yellow objects (like yellow markers, highlights)'
            },
            'orange': {
                'lower': (10, 100, 100),
                'upper': (20, 255, 255),
                'description': 'Orange objects (like orange buttons, warnings)'
            },
            'purple': {
                'lower': (130, 100, 100),
                'upper': (160, 255, 255),
                'description': 'Purple objects (like purple UI elements)'
            },
            'cyan': {
                'lower': (80, 100, 100),
                'upper': (100, 255, 255),
                'description': 'Cyan objects (like cyan highlights)'
            },
            'bright_green': {
                'lower': (60, 200, 200),
                'upper': (80, 255, 255),
                'description': 'Bright green objects (high saturation)'
            },
            'dark_red': {
                'lower': (0, 50, 50),
                'upper': (10, 200, 200),
                'description': 'Dark red objects (low saturation)'
            }
        }
    
    def list_available_colors(self):
        """List all available color presets"""
        self.logger.info("Available color presets:")
        for color_name, color_info in self.color_ranges.items():
            lower = color_info['lower']
            upper = color_info['upper']
            desc = color_info['description']
            self.logger.info(f"  {color_name}: {desc}")
            self.logger.info(f"    HSV Range: {lower} to {upper}")
    
    def track_color(self, color_name: str):
        """
        Start tracking objects of the specified color
        
        Args:
            color_name: Name of the color preset to track
        """
        if color_name not in self.color_ranges:
            self.logger.error(f"Unknown color: {color_name}")
            self.list_available_colors()
            return False
        
        color_info = self.color_ranges[color_name]
        lower_color = color_info['lower']
        upper_color = color_info['upper']
        description = color_info['description']
        
        self.logger.info(f"Setting up color tracking for: {description}")
        self.logger.info(f"HSV Range: {lower_color} to {upper_color}")
        
        # Configure color tracking
        self.tracker.track_by_color(lower_color, upper_color, 'HSV')
        
        # Configure tracking settings
        self.tracker.set_tracking_speed(30)  # 30 FPS
        self.tracker.set_confidence_threshold(0.3)  # Lower threshold for color detection
        
        # Setup callbacks
        self.setup_callbacks(color_name)
        
        return True
    
    def track_custom_color(self, lower_hsv: tuple, upper_hsv: tuple):
        """
        Track objects using custom HSV color range
        
        Args:
            lower_hsv: Lower HSV bound (h, s, v)
            upper_hsv: Upper HSV bound (h, s, v)
        """
        self.logger.info(f"Setting up custom color tracking")
        self.logger.info(f"HSV Range: {lower_hsv} to {upper_hsv}")
        
        # Configure color tracking
        self.tracker.track_by_color(lower_hsv, upper_hsv, 'HSV')
        
        # Configure tracking settings
        self.tracker.set_tracking_speed(30)
        self.tracker.set_confidence_threshold(0.3)
        
        # Setup callbacks
        self.setup_callbacks("custom")
    
    def setup_callbacks(self, color_name: str):
        """Setup event callbacks for color tracking"""
        detections = 0
        
        def on_color_found(detection_result):
            nonlocal detections
            detections += 1
            x, y = detection_result.center
            confidence = detection_result.confidence
            
            self.logger.info(f"🎨 {color_name.title()} object found at ({x}, {y}) - "
                           f"Confidence: {confidence:.2f} - "
                           f"Detections: {detections}")
        
        def on_color_lost():
            self.logger.info(f"👀 Searching for {color_name} objects...")
        
        self.tracker.set_callbacks(on_found=on_color_found, on_lost=on_color_lost)
    
    def start_tracking(self):
        """Start the color tracking"""
        self.logger.info("🚀 Starting color tracking...")
        self.logger.info("🎨 Move colored objects around your screen")
        self.logger.info("🖱️  Mouse will follow the detected objects")
        self.logger.info("⏹️  Press Ctrl+C to stop")
        
        # Test detection first
        test_result = self.tracker.test_detection(save_result=True)
        if test_result.found:
            self.logger.info(f"✅ Color detected! Confidence: {test_result.confidence:.2f}")
        else:
            self.logger.warning("⚠️  No matching color detected in current screen")
            self.logger.info("Try adjusting the color range or ensure target objects are visible")
        
        self.tracker.start_tracking()
        
        try:
            start_time = time.time()
            while self.tracker.is_tracking:
                time.sleep(1)
                
                # Print statistics every 30 seconds
                elapsed = time.time() - start_time
                if int(elapsed) % 30 == 0 and elapsed > 1:
                    stats = self.tracker.get_tracking_stats()
                    self.logger.info(f"📊 Stats - Frames: {stats['frames_processed']}, "
                                   f"Detections: {stats['objects_detected']}, "
                                   f"Rate: {stats.get('detection_rate', 0):.2%}")
        
        except KeyboardInterrupt:
            self.logger.info("🛑 Stopping color tracking...")
            self.tracker.stop_tracking()
            
            # Print final statistics
            final_stats = self.tracker.get_tracking_stats()
            self.logger.info("📊 Final Statistics:")
            self.logger.info(f"  Total frames: {final_stats['frames_processed']}")
            self.logger.info(f"  Color detections: {final_stats['objects_detected']}")
            self.logger.info(f"  Detection rate: {final_stats.get('detection_rate', 0):.2%}")


def main():
    """Main function"""
    tracker = ColorTracker()
    
    print("🎨 Color-Based Object Tracker")
    print("=" * 40)
    
    # Show available colors
    tracker.list_available_colors()
    print()
    
    try:
        # Ask user to choose a color
        print("Options:")
        print("1. Use predefined color")
        print("2. Use custom HSV range")
        print("3. Quick test with red objects")
        
        choice = input("Choose an option (1-3): ").strip()
        
        if choice == "1":
            color_name = input("Enter color name from the list above: ").strip().lower()
            if tracker.track_color(color_name):
                tracker.start_tracking()
        
        elif choice == "2":
            print("Enter HSV color range (0-179 for H, 0-255 for S and V):")
            try:
                h_min = int(input("  Lower H (hue): "))
                s_min = int(input("  Lower S (saturation): "))
                v_min = int(input("  Lower V (value): "))
                h_max = int(input("  Upper H (hue): "))
                s_max = int(input("  Upper S (saturation): "))
                v_max = int(input("  Upper V (value): "))
                
                lower_hsv = (h_min, s_min, v_min)
                upper_hsv = (h_max, s_max, v_max)
                
                tracker.track_custom_color(lower_hsv, upper_hsv)
                tracker.start_tracking()
                
            except ValueError:
                tracker.logger.error("Invalid input. Please enter numbers only.")
                return 1
        
        elif choice == "3":
            tracker.logger.info("🔴 Quick test: Tracking red objects")
            if tracker.track_color("red"):
                tracker.start_tracking()
        
        else:
            tracker.logger.warning("Invalid choice")
            return 1
    
    except KeyboardInterrupt:
        tracker.logger.info("Color tracking cancelled by user")
        return 0
    except Exception as e:
        tracker.logger.error(f"Color tracking error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 