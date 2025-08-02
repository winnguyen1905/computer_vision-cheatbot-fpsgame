#!/usr/bin/env python3
"""
Simple Object Tracker Example
Basic template-based object tracking with mouse following
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from src.tracker_system import TrackerSystem
from utils.logger import setup_logger


def main():
    """Simple tracking example"""
    # Setup logging
    logger = setup_logger("SimpleTracker", verbose=True)
    
    try:
        # Initialize tracker with default settings
        tracker = TrackerSystem()
        
        # Load a template (you'll need to create this image)
        template_path = "templates/target_object.png"
        
        if not Path(template_path).exists():
            logger.error(f"Template not found: {template_path}")
            logger.info("Please create a template image in the templates/ folder")
            logger.info("Take a screenshot and crop the object you want to track")
            return 1
        
        # Load the template
        tracker.load_template(template_path)
        logger.info(f"Loaded template: {template_path}")
        
        # Configure tracking settings
        tracker.set_tracking_speed(30)  # 30 FPS
        tracker.set_confidence_threshold(0.8)  # 80% confidence
        
        # Set up callbacks for events
        def on_object_found(detection_result):
            x, y = detection_result.center
            logger.info(f"Object found at ({x}, {y}) - Confidence: {detection_result.confidence:.2f}")
        
        def on_object_lost():
            logger.info("Object lost - continuing search...")
        
        tracker.set_callbacks(on_found=on_object_found, on_lost=on_object_lost)
        
        # Start tracking
        logger.info("Starting object tracking...")
        logger.info("Move the target object around your screen to see the mouse follow it")
        logger.info("Press Ctrl+C to stop tracking")
        
        tracker.start_tracking()
        
        # Keep the main thread alive
        try:
            while tracker.is_tracking:
                import time
                time.sleep(1)
                
                # Print statistics every 10 seconds
                stats = tracker.get_tracking_stats()
                if stats['frames_processed'] > 0 and stats['frames_processed'] % 300 == 0:  # Every ~10 seconds at 30 FPS
                    logger.info(f"Stats - Frames: {stats['frames_processed']}, "
                              f"Detections: {stats['objects_detected']}, "
                              f"Rate: {stats.get('detection_rate', 0):.2%}")
        
        except KeyboardInterrupt:
            logger.info("Stopping tracker...")
            tracker.stop_tracking()
            
            # Print final statistics
            final_stats = tracker.get_tracking_stats()
            logger.info("Final Statistics:")
            logger.info(f"  Total frames processed: {final_stats['frames_processed']}")
            logger.info(f"  Objects detected: {final_stats['objects_detected']}")
            logger.info(f"  Detection rate: {final_stats.get('detection_rate', 0):.2%}")
            logger.info(f"  Average FPS: {final_stats.get('avg_fps', 0):.1f}")
            logger.info(f"  Total runtime: {final_stats.get('elapsed_time', 0):.1f} seconds")
    
    except Exception as e:
        logger.error(f"Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 