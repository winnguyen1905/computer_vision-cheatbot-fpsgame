"""
Tracker System Module
Main coordination system that ties together detection, capture, and mouse control
"""

import time
import threading
from typing import Tuple, Optional, Dict, Any, Callable
from pathlib import Path
import logging

from .screen_capture import ScreenCapture
from .object_detector import ObjectDetector, DetectionResult
from .mouse_controller import MouseController, MouseSettings


class TrackerSystem:
    """Main tracking system that coordinates all components"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize tracker system
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        
        # Initialize components
        self.screen_capture = ScreenCapture()
        self.object_detector = ObjectDetector(
            confidence_threshold=self.config.get('tracking', {}).get('confidence_threshold', 0.8)
        )
        
        # Initialize mouse controller with settings from config
        mouse_config = self.config.get('mouse', {})
        tracking_config = self.config.get('tracking', {})
        
        mouse_settings = MouseSettings(
            movement_speed=tracking_config.get('movement_speed', 0.3),
            smooth_movement=tracking_config.get('smooth_movement', True),
            auto_click=mouse_config.get('auto_click', False),
            click_delay=mouse_config.get('click_delay', 0.1)
        )
        
        self.mouse_controller = MouseController(mouse_settings)
        
        # Tracking state
        self.is_tracking = False
        self.tracking_thread = None
        self.fps = self.config.get('tracking', {}).get('fps', 30)
        
        # Detection state
        self.current_template = None
        self.color_detection_params = None
        self.detection_method = 'template'  # 'template' or 'color'
        
        # Callbacks
        self.on_object_found: Optional[Callable[[DetectionResult], None]] = None
        self.on_object_lost: Optional[Callable] = None
        
        # Statistics
        self.stats = {
            'frames_processed': 0,
            'objects_detected': 0,
            'tracking_start_time': None,
            'last_detection_time': None
        }
        
        # Logger
        self.logger = logging.getLogger(__name__)
    
    def load_template(self, template_path: str):
        """
        Load template for object detection
        
        Args:
            template_path: Path to template image
        """
        if not Path(template_path).exists():
            raise FileNotFoundError(f"Template file not found: {template_path}")
        
        self.current_template = self.object_detector.load_template(template_path)
        self.detection_method = 'template'
        self.logger.info(f"Loaded template: {template_path}")
    
    def track_by_color(self, lower_color: Tuple[int, int, int], upper_color: Tuple[int, int, int],
                      color_space: str = 'HSV'):
        """
        Configure color-based tracking
        
        Args:
            lower_color: Lower bound of color range
            upper_color: Upper bound of color range
            color_space: Color space for detection
        """
        self.color_detection_params = {
            'lower_color': lower_color,
            'upper_color': upper_color,
            'color_space': color_space
        }
        self.detection_method = 'color'
        self.logger.info(f"Configured color tracking: {color_space} range {lower_color} to {upper_color}")
    
    def start_tracking(self):
        """Start the tracking loop"""
        if self.is_tracking:
            self.logger.warning("Tracking is already running")
            return
        
        if self.detection_method == 'template' and self.current_template is None:
            raise ValueError("No template loaded for tracking")
        
        if self.detection_method == 'color' and self.color_detection_params is None:
            raise ValueError("No color detection parameters configured")
        
        self.is_tracking = True
        self.stats['tracking_start_time'] = time.time()
        self.stats['frames_processed'] = 0
        self.stats['objects_detected'] = 0
        
        # Start tracking in separate thread
        self.tracking_thread = threading.Thread(target=self._tracking_loop, daemon=True)
        self.tracking_thread.start()
        
        self.logger.info("Object tracking started")
    
    def stop_tracking(self):
        """Stop the tracking loop"""
        if not self.is_tracking:
            return
        
        self.is_tracking = False
        
        # Stop mouse tracking
        self.mouse_controller.stop_continuous_tracking()
        
        # Wait for tracking thread to finish
        if self.tracking_thread and self.tracking_thread.is_alive():
            self.tracking_thread.join(timeout=2.0)
        
        self.logger.info("Object tracking stopped")
    
    def _tracking_loop(self):
        """Main tracking loop running in separate thread"""
        frame_time = 1.0 / self.fps
        last_detection_result = None
        
        try:
            for frame in self.screen_capture.capture_continuous(self.fps):
                if not self.is_tracking:
                    break
                
                start_time = time.time()
                
                # Perform detection
                detection_result = self._detect_object(frame)
                
                # Update statistics
                self.stats['frames_processed'] += 1
                
                if detection_result.found:
                    self.stats['objects_detected'] += 1
                    self.stats['last_detection_time'] = time.time()
                    
                    # Move mouse to detected object
                    if detection_result.center:
                        x, y = detection_result.center
                        self.mouse_controller.track_to_position(x, y)
                    
                    # Trigger callback
                    if self.on_object_found:
                        self.on_object_found(detection_result)
                    
                    last_detection_result = detection_result
                
                elif last_detection_result and last_detection_result.found:
                    # Object was lost
                    if self.on_object_lost:
                        self.on_object_lost()
                    last_detection_result = None
                
                # Maintain FPS
                elapsed_time = time.time() - start_time
                sleep_time = max(0, frame_time - elapsed_time)
                if sleep_time > 0:
                    time.sleep(sleep_time)
                    
        except Exception as e:
            self.logger.error(f"Tracking loop error: {e}")
            self.is_tracking = False
    
    def _detect_object(self, frame) -> DetectionResult:
        """
        Detect object in frame using current detection method
        
        Args:
            frame: Screen capture frame
            
        Returns:
            DetectionResult: Detection result
        """
        try:
            if self.detection_method == 'template' and self.current_template is not None:
                return self.object_detector.detect_object(frame, self.current_template)
            
            elif self.detection_method == 'color' and self.color_detection_params:
                return self.object_detector.find_by_color(
                    frame,
                    self.color_detection_params['lower_color'],
                    self.color_detection_params['upper_color'],
                    self.color_detection_params['color_space']
                )
            
            else:
                return DetectionResult(found=False)
                
        except Exception as e:
            self.logger.error(f"Detection error: {e}")
            return DetectionResult(found=False)
    
    def set_tracking_speed(self, fps: int):
        """
        Set tracking FPS
        
        Args:
            fps: Frames per second for tracking
        """
        self.fps = max(1, min(fps, 120))  # Clamp between 1 and 120 FPS
        self.logger.info(f"Tracking FPS set to: {self.fps}")
    
    def enable_auto_click(self, enabled: bool = True):
        """Enable or disable auto-clicking when object is found"""
        self.mouse_controller.settings.auto_click = enabled
        self.logger.info(f"Auto-click {'enabled' if enabled else 'disabled'}")
    
    def set_confidence_threshold(self, threshold: float):
        """Set detection confidence threshold"""
        self.object_detector.set_confidence_threshold(threshold)
        self.logger.info(f"Confidence threshold set to: {threshold}")
    
    def get_tracking_stats(self) -> Dict[str, Any]:
        """
        Get tracking statistics
        
        Returns:
            Dict containing tracking statistics
        """
        stats = self.stats.copy()
        
        if stats['tracking_start_time']:
            elapsed_time = time.time() - stats['tracking_start_time']
            stats['elapsed_time'] = elapsed_time
            stats['avg_fps'] = stats['frames_processed'] / elapsed_time if elapsed_time > 0 else 0
            stats['detection_rate'] = stats['objects_detected'] / stats['frames_processed'] if stats['frames_processed'] > 0 else 0
        
        return stats
    
    def capture_current_screen(self, save_path: Optional[str] = None) -> Optional[str]:
        """
        Capture current screen for debugging
        
        Args:
            save_path: Optional path to save screenshot
            
        Returns:
            Path where screenshot was saved
        """
        try:
            if save_path is None:
                save_path = f"debug_screenshot_{int(time.time())}.png"
            
            self.screen_capture.save_screenshot(save_path)
            self.logger.info(f"Screenshot saved: {save_path}")
            return save_path
            
        except Exception as e:
            self.logger.error(f"Failed to capture screenshot: {e}")
            return None
    
    def test_detection(self, save_result: bool = False) -> DetectionResult:
        """
        Test current detection settings on a single frame
        
        Args:
            save_result: Whether to save the detection result image
            
        Returns:
            DetectionResult: Test detection result
        """
        try:
            frame = self.screen_capture.capture_screen()
            result = self._detect_object(frame)
            
            if save_result and result.found:
                # Draw detection result on frame and save
                import cv2
                if result.bounding_box:
                    x, y, w, h = result.bounding_box
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                if result.center:
                    cv2.circle(frame, result.center, 10, (0, 0, 255), -1)
                
                save_path = f"test_detection_{int(time.time())}.png"
                cv2.imwrite(save_path, frame)
                self.logger.info(f"Detection test result saved: {save_path}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Detection test failed: {e}")
            return DetectionResult(found=False)
    
    def set_callbacks(self, on_found: Optional[Callable[[DetectionResult], None]] = None,
                     on_lost: Optional[Callable] = None):
        """
        Set event callbacks
        
        Args:
            on_found: Callback when object is found
            on_lost: Callback when object is lost
        """
        self.on_object_found = on_found
        self.on_object_lost = on_lost
    
    def update_mouse_settings(self, **kwargs):
        """Update mouse control settings"""
        self.mouse_controller.update_settings(**kwargs)
        
    def is_object_currently_detected(self) -> bool:
        """Check if object was recently detected"""
        if not self.stats['last_detection_time']:
            return False
        
        time_since_detection = time.time() - self.stats['last_detection_time']
        return time_since_detection < 1.0  # Consider detected if found within last second 