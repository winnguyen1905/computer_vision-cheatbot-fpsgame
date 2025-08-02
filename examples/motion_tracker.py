#!/usr/bin/env python3
"""
Motion Detection Example
Demonstrates real-time motion detection and mouse tracking
"""

import sys
import os
import time
from pathlib import Path

# Add parent src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from tracker_system import TrackerSystem
from utils.logger import setup_logger

def main():
    """Demonstrate motion detection tracking"""
    
    # Setup logging
    logger = setup_logger(verbose=True)
    logger.info("Motion Detection Example")
    
    # Configuration for motion detection
    config = {
        "capture_region": {
            "top": 100,
            "left": 100,
            "width": 800,
            "height": 600
        },
        "tracking": {
            "fps": 30,
            "confidence_threshold": 0.3,  # Lower threshold for motion
            "smooth_movement": True,
            "movement_speed": 0.5
        },
        "detection": {
            "method": "motion",
            "min_area": 1000,      # Minimum area for motion detection
            "motion_threshold": 30, # Sensitivity to motion
            "dilate_iterations": 3,
            "blur_kernel_size": 15
        },
        "mouse": {
            "auto_click": False,
            "click_delay": 0.1
        }
    }
    
    # Initialize tracker
    tracker = TrackerSystem(config)
    
    # Configure motion detection
    tracker.track_by_motion('frame_diff')  # Use frame differencing
    
    # Set up callbacks for motion events
    def on_motion_found(result):
        logger.info(f"Motion detected! Center: {result.center}, "
                   f"Confidence: {result.confidence:.3f}, "
                   f"Objects: {len(result.multiple_objects) if result.multiple_objects else 0}")
    
    def on_motion_lost():
        logger.info("Motion stopped")
    
    tracker.set_callbacks(on_found=on_motion_found, on_lost=on_motion_lost)
    
    try:
        # Test detection first
        logger.info("Testing motion detection on current frame...")
        result = tracker.test_detection(save_result=True)
        
        if result.found:
            logger.info(f"Initial motion detected: {result.center}")
        else:
            logger.info("No initial motion detected - move something in the capture region")
        
        # Start tracking
        logger.info("Starting motion tracking...")
        logger.info("Move objects in the capture region to see tracking in action")
        logger.info("Press Ctrl+C to stop")
        
        tracker.start_tracking()
        
        # Monitor for 30 seconds with statistics
        start_time = time.time()
        last_stats_time = start_time
        
        while tracker.is_tracking and (time.time() - start_time) < 30:
            time.sleep(0.5)
            
            # Print stats every 5 seconds
            if time.time() - last_stats_time >= 5:
                stats = tracker.get_tracking_stats()
                logger.info(f"Performance - Avg FPS: {stats.get('avg_fps', 0):.1f}, "
                           f"Total Detections: {stats.get('objects_detected', 0)}, "
                           f"Detection Rate: {stats.get('detection_rate', 0):.1%}")
                last_stats_time = time.time()
        
        # Stop tracking
        tracker.stop_tracking()
        
        # Final statistics
        final_stats = tracker.get_tracking_stats()
        logger.info("\n=== Final Statistics ===")
        logger.info(f"Frames Processed: {final_stats.get('frames_processed', 0)}")
        logger.info(f"Motion Events: {final_stats.get('objects_detected', 0)}")
        logger.info(f"Average FPS: {final_stats.get('avg_fps', 0):.2f}")
        logger.info(f"Detection Rate: {final_stats.get('detection_rate', 0):.1%}")
        logger.info(f"Total Runtime: {final_stats.get('elapsed_time', 0):.1f} seconds")
        
    except KeyboardInterrupt:
        logger.info("\nMotion tracking stopped by user")
        tracker.stop_tracking()
    
    except Exception as e:
        logger.error(f"Error during motion tracking: {e}")
        return 1
    
    logger.info("Motion detection example completed")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 