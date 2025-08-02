"""
Real-Time Object Tracker - Core Package
"""

__version__ = "1.0.0"
__author__ = "Object Detective Team"
__description__ = "Real-time object detection and mouse tracking system"

from .tracker_system import TrackerSystem
from .object_detector import ObjectDetector
from .screen_capture import ScreenCapture
from .mouse_controller import MouseController

__all__ = [
    'TrackerSystem',
    'ObjectDetector', 
    'ScreenCapture',
    'MouseController'
] 