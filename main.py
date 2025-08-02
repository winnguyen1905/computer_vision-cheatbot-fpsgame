#!/usr/bin/env python3
"""
Real-Time Object Tracker - Main Entry Point
Detect objects on screen in real-time and move mouse to their location
"""

import argparse
import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from tracker_system import TrackerSystem
from utils.logger import setup_logger
from utils.config_loader import ConfigLoader

def main():
    """Main application entry point"""
    parser = argparse.ArgumentParser(description="Real-Time Object Tracker")
    
    # Detection method arguments
    parser.add_argument('--template', type=str, help='Path to template image for detection')
    parser.add_argument('--color-detect', action='store_true', help='Use color-based detection')
    parser.add_argument('--motion-detect', action='store_true', help='Use motion-based detection')
    parser.add_argument('--red-range', action='store_true', help='Track red objects')
    parser.add_argument('--blue-range', action='store_true', help='Track blue objects')
    parser.add_argument('--green-range', action='store_true', help='Track green objects')
    
    # Motion detection arguments
    parser.add_argument('--motion-method', type=str, choices=['frame_diff', 'mog2', 'knn'], 
                       default='frame_diff', help='Motion detection method')
    parser.add_argument('--min-area', type=int, help='Minimum area for motion detection')
    parser.add_argument('--motion-threshold', type=int, help='Motion detection threshold (0-255)')
    
    # Capture region arguments
    parser.add_argument('--region', nargs=4, type=int, metavar=('LEFT', 'TOP', 'WIDTH', 'HEIGHT'),
                       help='Capture region (left top width height)')
    parser.add_argument('--full-screen', action='store_true', help='Use full screen capture (default)')
    
    # Configuration arguments
    parser.add_argument('--config', type=str, default='config.json', help='Configuration file path')
    parser.add_argument('--fps', type=int, help='Tracking FPS (overrides config)')
    parser.add_argument('--auto-click', action='store_true', help='Auto-click when object found')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose logging')
    
    # Test and debug arguments
    parser.add_argument('--test-detection', action='store_true', help='Test detection on single frame and exit')
    parser.add_argument('--save-test', action='store_true', help='Save test detection result image')
    
    args = parser.parse_args()
    
    # Setup logging
    logger = setup_logger(verbose=args.verbose)
    logger.info("Starting Real-Time Object Tracker")
    
    try:
        # Load configuration
        config_loader = ConfigLoader(args.config)
        config = config_loader.load()
        
        # Override config with command line arguments
        if args.fps:
            config['tracking']['fps'] = args.fps
        if args.auto_click:
            config['mouse']['auto_click'] = True
        if args.min_area:
            config['detection']['min_area'] = args.min_area
        if args.motion_threshold:
            config['detection']['motion_threshold'] = args.motion_threshold
            
        # Handle capture region
        if args.region:
            config['capture_region'] = {
                'left': args.region[0],
                'top': args.region[1], 
                'width': args.region[2],
                'height': args.region[3]
            }
            logger.info(f"Using capture region: {args.region[0]}, {args.region[1]}, {args.region[2]}x{args.region[3]}")
        elif args.full_screen:
            config['capture_region'] = {}  # Clear capture region for full screen
            logger.info("Using full screen capture")
            
        # Initialize tracker system
        tracker = TrackerSystem(config)
        
        # Configure detection method
        if args.template:
            if not Path(args.template).exists():
                logger.error(f"Template file not found: {args.template}")
                return 1
            tracker.load_template(args.template)
            logger.info(f"Loaded template: {args.template}")
            
        elif args.motion_detect:
            tracker.track_by_motion(args.motion_method)
            logger.info(f"Configured motion detection using {args.motion_method}")
            
        elif args.color_detect:
            if args.red_range:
                tracker.track_by_color(
                    lower_color=(0, 100, 100),
                    upper_color=(10, 255, 255),
                    color_space='HSV'
                )
                logger.info("Tracking red objects")
            elif args.blue_range:
                tracker.track_by_color(
                    lower_color=(100, 100, 100),
                    upper_color=(130, 255, 255),
                    color_space='HSV'
                )
                logger.info("Tracking blue objects")
            elif args.green_range:
                tracker.track_by_color(
                    lower_color=(40, 100, 100),
                    upper_color=(80, 255, 255),
                    color_space='HSV'
                )
                logger.info("Tracking green objects")
            else:
                logger.error("Please specify a color range (--red-range, --blue-range, --green-range)")
                return 1
        else:
            # Use default detection method from config
            detection_method = config.get('detection', {}).get('method', 'template')
            
            if detection_method == 'motion':
                motion_method = args.motion_method if hasattr(args, 'motion_method') else 'frame_diff'
                tracker.track_by_motion(motion_method)
                logger.info(f"Using default motion detection: {motion_method}")
                
            elif detection_method == 'template':
                template_path = config['detection']['template_path']
                if Path(template_path).exists():
                    tracker.load_template(template_path)
                    logger.info(f"Using default template: {template_path}")
                else:
                    logger.error("No detection method specified and default template not found")
                    logger.info("Use --template <path>, --motion-detect, or --color-detect with color range")
                    return 1
            else:
                logger.error(f"Unsupported default detection method: {detection_method}")
                return 1
        
        # Test detection if requested
        if args.test_detection:
            logger.info("Testing detection on single frame...")
            result = tracker.test_detection(save_result=args.save_test)
            
            if result.found:
                logger.info(f"Detection successful! Center: {result.center}, Confidence: {result.confidence:.3f}")
                if result.multiple_objects:
                    logger.info(f"Detected {len(result.multiple_objects)} objects")
            else:
                logger.info("No objects detected in test frame")
            
            return 0
        
        # Start tracking
        logger.info("Starting object tracking... Press Ctrl+C to stop")
        tracker.start_tracking()
        
        # Keep main thread alive
        try:
            while tracker.is_tracking:
                import time
                time.sleep(0.1)
                
                # Print periodic stats
                stats = tracker.get_tracking_stats()
                if stats.get('frames_processed', 0) % 300 == 0 and stats['frames_processed'] > 0:  # Every 10 seconds at 30fps
                    logger.info(f"Stats - FPS: {stats.get('avg_fps', 0):.1f}, "
                              f"Detections: {stats.get('objects_detected', 0)}, "
                              f"Rate: {stats.get('detection_rate', 0):.1%}")
                              
        except KeyboardInterrupt:
            logger.info("Stopping tracking...")
            tracker.stop_tracking()
        
    except KeyboardInterrupt:
        logger.info("Tracking stopped by user")
    except Exception as e:
        logger.error(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 