#!/usr/bin/env python3
"""
Enhanced Mouse Controller Demo - Task 3
Demonstrates the new mouse interaction features with throttling and safety
"""

import sys
import os
import time
from pathlib import Path

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

from tracker_system import TrackerSystem
from utils.config_loader import ConfigLoader

def demo_enhanced_mouse_tracking():
    """
    Demo of enhanced mouse tracking with new features:
    - move_to_box() method for smooth cursor movement
    - click_box() method for optional clicking
    - Throttling to prevent excessive movement
    - Target selection (largest box by area)
    """
    
    print("🎯 Enhanced Mouse Controller Demo - Task 3")
    print("=" * 50)
    
    # Load configuration
    config_loader = ConfigLoader('config.json')
    config = config_loader.load()
    
    # Display current mouse configuration
    mouse_config = config.get('mouse', {})
    print("Current mouse configuration:")
    for key, value in mouse_config.items():
        print(f"  {key}: {value}")
    print()
    
    # Initialize tracker system
    tracker = TrackerSystem(config)
    
    print("New Features Implemented:")
    print("✓ move_to_box() - Smoothly moves cursor to box center")
    print("✓ click_box() - Moves to box and optionally clicks")
    print("✓ Throttling - Prevents excessive mouse movement (0.2s interval)")
    print("✓ Target Selection - Chooses largest detection by area")
    print("✓ Coordinate Adjustment - Handles capture regions correctly")
    print()
    
    print("Configuration Options:")
    print(f"• move_duration: {mouse_config.get('move_duration', 0.1)}s - Time to move cursor")
    print(f"• enable_click: {mouse_config.get('enable_click', False)} - Auto-click on detections")
    print(f"• click_delay: {mouse_config.get('click_delay', 0.1)}s - Pause after clicking")
    print()
    
    # Configure for motion detection (safest for demo)
    tracker.track_by_motion('frame_diff')
    
    print("To test the enhanced mouse features:")
    print("1. Set enable_click: true in config.json for auto-clicking")
    print("2. Adjust move_duration for faster/slower mouse movement")
    print("3. Run: python main.py --motion-detect")
    print()
    
    print("Safety Features:")
    print("• Throttling prevents excessive CPU/mouse usage")
    print("• Only targets largest detection to avoid jittery movement")
    print("• Graceful error handling for mouse operations")
    print("• Configurable click delays for system compatibility")
    print()
    
    # Example of programmatic usage
    print("Example Usage in Code:")
    print("""
    # Create tracker with enhanced mouse features
    tracker = TrackerSystem(config)
    
    # Enable motion detection
    tracker.track_by_motion('frame_diff')
    
    # Start visual tracking with mouse interaction
    tracker.run()  # Now includes throttled mouse movement!
    
    # Or use mouse controller directly
    box = (100, 100, 50, 50)  # x, y, width, height
    tracker.mouse.move_to_box(box)      # Move to box center
    tracker.mouse.click_box(box)        # Move and optionally click
    """)

if __name__ == "__main__":
    try:
        demo_enhanced_mouse_tracking()
    except KeyboardInterrupt:
        print("\\nDemo interrupted by user")
    except Exception as e:
        print(f"Demo error: {e}") 