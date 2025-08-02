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
    parser.add_argument('--red-range', action='store_true', help='Track red objects')
    parser.add_argument('--blue-range', action='store_true', help='Track blue objects')
    parser.add_argument('--green-range', action='store_true', help='Track green objects')
    
    # Configuration arguments
    parser.add_argument('--config', type=str, default='config.json', help='Configuration file path')
    parser.add_argument('--fps', type=int, help='Tracking FPS (overrides config)')
    parser.add_argument('--auto-click', action='store_true', help='Auto-click when object found')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose logging')
    
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
            
        # Initialize tracker system
        tracker = TrackerSystem(config)
        
        # Configure detection method
        if args.template:
            if not Path(args.template).exists():
                logger.error(f"Template file not found: {args.template}")
                return 1
            tracker.load_template(args.template)
            logger.info(f"Loaded template: {args.template}")
            
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
            # Use default template from config
            template_path = config['detection']['template_path']
            if Path(template_path).exists():
                tracker.load_template(template_path)
                logger.info(f"Using default template: {template_path}")
            else:
                logger.error("No detection method specified and default template not found")
                logger.info("Use --template <path> or --color-detect with color range")
                return 1
        
        # Start tracking
        logger.info("Starting object tracking... Press Ctrl+C to stop")
        tracker.start_tracking()
        
    except KeyboardInterrupt:
        logger.info("Tracking stopped by user")
    except Exception as e:
        logger.error(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 