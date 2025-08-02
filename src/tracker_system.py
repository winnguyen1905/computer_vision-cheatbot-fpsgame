"""
Tracker System Module
Main coordination system that ties together detection, capture, and mouse control
"""

import time
import threading
import cv2
from typing import Tuple, Optional, Dict, Any, Callable
from pathlib import Path
import logging

from screen_capture import ScreenCapture, grab_frame
from object_detector import ObjectDetector, DetectionResult
from mouse_controller import MouseController, MouseSettings
from keyboard_controller import KeyboardController


class TrackerSystem:
    """Main tracking system that coordinates all components"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None, config_path: Optional[str] = None):
        """
        Initialize tracker system
        
        Args:
            config: Configuration dictionary
            config_path: Path to configuration file (for unified interface)
        """
        # Handle unified initialization pattern
        if config_path is not None:
            from utils.config_loader import ConfigLoader
            config_loader = ConfigLoader(config_path)
            config = config_loader.load()
        
        self.config = config or {}
        
        # Initialize components
        self.screen_capture = ScreenCapture()
        
        # Get detection configuration
        detection_config = self.config.get('detection', {})
        motion_config = {
            'min_area': detection_config.get('min_area', 500),
            'motion_threshold': detection_config.get('motion_threshold', 25),
            'dilate_iterations': detection_config.get('dilate_iterations', 2),
            'blur_kernel_size': detection_config.get('blur_kernel_size', 21),
            'background_history': detection_config.get('background_history', 50),
            'background_threshold': detection_config.get('background_threshold', 16),
            'use_background_subtraction': detection_config.get('method') in ['mog2', 'knn']
        }
        
        self.object_detector = ObjectDetector(
            config=detection_config,
            confidence_threshold=self.config.get('tracking', {}).get('confidence_threshold', 0.8),
            motion_config=motion_config
        )
        
        # Set motion detection method if specified
        detection_method = detection_config.get('method', 'template')
        if detection_method in ['mog2', 'knn']:
            self.object_detector.set_motion_method(detection_method)
        
        # Initialize mouse controller with settings from config
        mouse_config = self.config.get('mouse', {})
        tracking_config = self.config.get('tracking', {})
        
        mouse_settings = MouseSettings(
            movement_speed=tracking_config.get('movement_speed', 0.3),
            smooth_movement=tracking_config.get('smooth_movement', True),
            auto_click=mouse_config.get('auto_click', False),
            click_delay=mouse_config.get('click_delay', 0.1),
            move_duration=mouse_config.get('move_duration', 0.1),
            enable_click=mouse_config.get('enable_click', False)
        )
        
        self.mouse_controller = MouseController(mouse_settings)
        
        # Initialize keyboard controller
        self.keyboard_controller = KeyboardController(self)
        
        # Simplified interface properties
        self.region = self.config.get('capture_region', {})
        self.detector = self.object_detector  # Alias for unified interface
        self.mouse = self.mouse_controller    # Alias for unified interface
        self.keyboard = self.keyboard_controller  # Alias for unified interface
        
        # Capture region configuration
        capture_region_config = self.config.get('capture_region', {})
        self.capture_region = None
        if capture_region_config:
            self.capture_region = (
                capture_region_config.get('left', 0),
                capture_region_config.get('top', 0),
                capture_region_config.get('width', 1920),
                capture_region_config.get('height', 1080)
            )
        
        # Tracking state
        self.is_tracking = False
        self.should_exit = False  # For graceful shutdown via shortcuts
        self.tracking_thread = None
        self.fps = self.config.get('tracking', {}).get('fps', 30)
        
        # Visual display settings (merge with config)
        visual_config_from_config = self.config.get('visual', {})
        self.visual_config = {
            'show_circles': visual_config_from_config.get('show_circles', True),
            'circle_radius': visual_config_from_config.get('circle_radius', 50),
            'detection_circle_color': (0, 255, 255),  # Yellow around objects
            'range_circle_color': (0, 255, 0),        # Green for detection zone
            'circle_thickness': 2,
            'show_detection_range': visual_config_from_config.get('show_detection_range', True),
            'range_circle_radius': visual_config_from_config.get('range_circle_radius', 0),  # Auto-calculate 10%
            'range_percentage': visual_config_from_config.get('range_percentage', 0.10),  # 10% of screen
            'show_crosshair': visual_config_from_config.get('show_crosshair', True),
            'crosshair_color': (0, 0, 255),           # Red
            'crosshair_size': 20,
            'detection_zone_alpha': 0.3               # Transparency for zone
        }
        
        # Detection state
        self.current_template = None
        self.color_detection_params = None
        self.detection_method = detection_config.get('method', 'template')
        
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
        
        # Visual tracking settings
        self.show_visual_feedback = True
        self.window_name = "Object Detective"
        self.auto_click_detections = mouse_config.get('auto_click', False)
    
    def run(self):
        """
        Real-time visual tracking loop with OpenCV display
        This matches the user's requested interface pattern
        """
        print("Starting real-time tracking. Press 'q' to quit or use Ctrl+Shift+Q for global stop.")
        
        # Start keyboard shortcut listener
        try:
            self.keyboard_controller.start_listening()
        except Exception as e:
            print(f"Warning: Keyboard shortcuts not available: {e}")
        
        # Throttling variables for mouse movement
        last_move = 0
        move_interval = 0.2  # seconds between mouse movements
        
        try:
            while True:
                # Check for exit signal from keyboard shortcuts
                if self.should_exit:
                    break
                
                # 1) Capture frame
                frame = grab_frame(self.region)
                
                # 2) Detect objects on this single frame
                # Returns: List of (x, y, w, h) for each detected object
                boxes = self.detector.detect(frame)
                
                # Update statistics
                self.stats['frames_processed'] += 1
                if boxes:
                    self.stats['objects_detected'] += len(boxes)
                    self.stats['last_detection_time'] = time.time()
                
                # 3) Post-process each detection
                for (x, y, w, h) in boxes:
                    # 3a) Draw a rectangle
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    
                    # 3b) Draw detection circle around object center
                    if self.visual_config['show_circles']:
                        center_x = x + w // 2
                        center_y = y + h // 2
                        radius = self.visual_config['circle_radius']
                        color = self.visual_config['detection_circle_color']
                        thickness = self.visual_config['circle_thickness']
                        
                        cv2.circle(frame, (center_x, center_y), radius, color, thickness)
                        
                        # Draw crosshair at center
                        if self.visual_config['show_crosshair']:
                            crosshair_size = self.visual_config['crosshair_size']
                            crosshair_color = self.visual_config['crosshair_color']
                            
                            # Horizontal line
                            cv2.line(frame, 
                                   (center_x - crosshair_size, center_y), 
                                   (center_x + crosshair_size, center_y), 
                                   crosshair_color, 2)
                            # Vertical line
                            cv2.line(frame, 
                                   (center_x, center_y - crosshair_size), 
                                   (center_x, center_y + crosshair_size), 
                                   crosshair_color, 2)
                    
                    # Add confidence and area text if available
                    area = w * h
                    cv2.putText(frame, f"Area: {area}", (x, y - 10), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
                
                # 4) Mouse interaction with throttling
                now = time.time()
                if boxes and now - last_move > move_interval:
                    # Pick the largest box (by area) as the target
                    target_box = max(boxes, key=lambda b: b[2] * b[3])
                    x, y, w, h = target_box
                    
                    # Adjust coordinates if using capture region
                    adj_x = x + self.region.get('left', 0)
                    adj_y = y + self.region.get('top', 0)
                    adjusted_box = (adj_x, adj_y, w, h)
                    
                    # Move mouse to the target box
                    self.mouse.move_to_box(adjusted_box)
                    
                    # Optionally click (based on configuration)
                    if self.mouse.settings.enable_click:
                        self.mouse.click_box(adjusted_box)
                    
                    last_move = now
                
                # Add statistics overlay
                if boxes:
                    status_text = f"Detected: {len(boxes)} objects"
                    cv2.putText(frame, status_text, (10, 30), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                # Add method indicator
                method_text = f"Method: {self.detection_method}"
                cv2.putText(frame, method_text, (10, frame.shape[0] - 10), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                
                # Add throttling status
                time_since_move = now - last_move
                throttle_text = f"Last move: {time_since_move:.1f}s ago"
                cv2.putText(frame, throttle_text, (10, frame.shape[0] - 30), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                
                # Draw detection range circle at screen center
                if self.visual_config['show_detection_range']:
                    center_x = frame.shape[1] // 2
                    center_y = frame.shape[0] // 2
                    range_radius = self.visual_config['range_circle_radius']
                    range_color = self.visual_config['range_circle_color']
                    
                    # Draw main range circle
                    cv2.circle(frame, (center_x, center_y), range_radius, range_color, 1)
                    
                    # Draw smaller inner circles for reference
                    cv2.circle(frame, (center_x, center_y), range_radius // 2, range_color, 1)
                    cv2.circle(frame, (center_x, center_y), range_radius // 4, range_color, 1)
                    
                    # Add range text
                    cv2.putText(frame, f"Range: {range_radius}px", 
                              (center_x - 50, center_y + range_radius + 20), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.5, range_color, 1)
                
                # 5) Show the annotated frame
                cv2.imshow(self.window_name, frame)
                
                # 6) Break on 'q' or window close
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                    
                # Check if window was closed
                if cv2.getWindowProperty(self.window_name, cv2.WND_PROP_VISIBLE) < 1:
                    break
                    
        except KeyboardInterrupt:
            print("Tracking interrupted by user")
        except Exception as e:
            print(f"Tracking error: {e}")
        finally:
            # Stop keyboard listener
            try:
                self.keyboard_controller.stop_listening()
            except:
                pass
                
            cv2.destroyAllWindows()
            print("Visual tracking stopped")
    
    def run_headless(self):
        """
        Run tracking without visual display (headless mode)
        """
        print("Starting headless tracking. Press Ctrl+C or Ctrl+Shift+Q to stop.")
        
        # Start keyboard shortcut listener
        try:
            self.keyboard_controller.start_listening()
        except Exception as e:
            print(f"Warning: Keyboard shortcuts not available: {e}")
        
        try:
            self.start_tracking()
            
            # Keep running until interrupted
            while self.is_tracking and not self.should_exit:
                time.sleep(0.1)
                
                # Print periodic stats
                if self.stats['frames_processed'] % 300 == 0 and self.stats['frames_processed'] > 0:
                    stats = self.get_tracking_stats()
                    print(f"Stats - FPS: {stats.get('avg_fps', 0):.1f}, "
                          f"Detections: {stats.get('objects_detected', 0)}, "
                          f"Rate: {stats.get('detection_rate', 0):.1%}")
                          
        except KeyboardInterrupt:
            print("Headless tracking interrupted")
        finally:
            self.stop_tracking()
            # Stop keyboard listener
            try:
                self.keyboard_controller.stop_listening()
            except:
                pass
    
    def load_template(self, template_path: str):
        """
        Load template for object detection
        
        Args:
            template_path: Path to template image
        """
        if not Path(template_path).exists():
            raise FileNotFoundError(f"Template file not found: {template_path}")
        
        template = self.object_detector.load_template(template_path)
        self.object_detector.set_template(template)
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
        self.object_detector.set_color_detection(lower_color, upper_color, color_space)
        self.detection_method = 'color'
        self.logger.info(f"Configured color tracking: {color_space} range {lower_color} to {upper_color}")

    def track_by_motion(self, motion_method: str = 'frame_diff'):
        """
        Configure motion-based tracking
        
        Args:
            motion_method: Motion detection method ('frame_diff', 'mog2', 'knn')
        """
        self.detection_method = 'motion'
        self.object_detector.set_motion_detection(motion_method)
        self.logger.info(f"Configured motion tracking using {motion_method}")
    
    def start_tracking(self):
        """Start the tracking loop"""
        if self.is_tracking:
            self.logger.warning("Tracking is already running")
            return
        
        if self.detection_method == 'template' and self.current_template is None:
            raise ValueError("No template loaded for tracking")
        
        if self.detection_method == 'color' and self.color_detection_params is None:
            raise ValueError("No color detection parameters configured")
        
        if self.detection_method == 'motion':
            # Reset motion detection state when starting
            self.object_detector.reset_motion_detection()
        
        self.is_tracking = True
        self.stats['tracking_start_time'] = time.time()
        self.stats['frames_processed'] = 0
        self.stats['objects_detected'] = 0
        
        # Start tracking in separate thread
        self.tracking_thread = threading.Thread(target=self._tracking_loop, daemon=True)
        self.tracking_thread.start()
        
        self.logger.info(f"Object tracking started using {self.detection_method} method")
    
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
    
    def shutdown(self):
        """Graceful shutdown via keyboard shortcuts"""
        self.should_exit = True
        self.stop_tracking()
        
        # Stop keyboard listener
        try:
            self.keyboard_controller.stop_listening()
        except:
            pass
    
    def _tracking_loop(self):
        """Main tracking loop running in separate thread"""
        frame_time = 1.0 / self.fps
        last_detection_result = None
        
        try:
            while self.is_tracking:
                start_time = time.time()
                
                # Capture frame (either full screen or region)
                if self.capture_region:
                    frame = self.screen_capture.capture_region(*self.capture_region)
                else:
                    frame = self.screen_capture.capture_screen()
                
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
                        
                        # Adjust coordinates if using capture region
                        if self.capture_region:
                            x += self.capture_region[0]  # Add left offset
                            y += self.capture_region[1]  # Add top offset
                        
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
            
            elif self.detection_method == 'motion':
                return self.object_detector.detect_motion(frame)
            
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
        self.auto_click_detections = enabled
        self.logger.info(f"Auto-click {'enabled' if enabled else 'disabled'}")
    
    def set_confidence_threshold(self, threshold: float):
        """Set detection confidence threshold"""
        self.object_detector.set_confidence_threshold(threshold)
        self.logger.info(f"Confidence threshold set to: {threshold}")

    def set_capture_region(self, left: int, top: int, width: int, height: int):
        """
        Set capture region for focused tracking
        
        Args:
            left, top: Top-left coordinates
            width, height: Region dimensions
        """
        self.capture_region = (left, top, width, height)
        self.region = {'left': left, 'top': top, 'width': width, 'height': height}
        self.logger.info(f"Capture region set to: {left}, {top}, {width}x{height}")
    
    def clear_capture_region(self):
        """Clear capture region to track full screen"""
        self.capture_region = None
        self.region = {}
        self.logger.info("Capture region cleared - tracking full screen")
    
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
    
    def toggle_circle_display(self):
        """Toggle circle display on/off"""
        self.visual_config['show_circles'] = not self.visual_config['show_circles']
        status = "ON" if self.visual_config['show_circles'] else "OFF"
        self.logger.info(f"Circle display: {status}")
        return self.visual_config['show_circles']
    
    def toggle_range_display(self):
        """Toggle detection range display on/off"""
        self.visual_config['show_detection_range'] = not self.visual_config['show_detection_range']
        status = "ON" if self.visual_config['show_detection_range'] else "OFF"
        self.logger.info(f"Range display: {status}")
        return self.visual_config['show_detection_range']
    
    def toggle_crosshair_display(self):
        """Toggle crosshair display on/off"""
        self.visual_config['show_crosshair'] = not self.visual_config['show_crosshair']
        status = "ON" if self.visual_config['show_crosshair'] else "OFF"
        self.logger.info(f"Crosshair display: {status}")
        return self.visual_config['show_crosshair']
    
    def set_circle_radius(self, radius: int):
        """Set detection circle radius"""
        self.visual_config['circle_radius'] = max(10, min(radius, 200))
        self.logger.info(f"Circle radius set to: {self.visual_config['circle_radius']}")
    
    def set_range_radius(self, radius: int):
        """Set detection range radius"""
        self.visual_config['range_circle_radius'] = max(50, min(radius, 500))
        self.logger.info(f"Range radius set to: {self.visual_config['range_circle_radius']}")
    
    def get_visual_config(self) -> Dict[str, Any]:
        """Get current visual configuration"""
        return self.visual_config.copy()
    
    def update_visual_config(self, **kwargs):
        """Update visual configuration"""
        for key, value in kwargs.items():
            if key in self.visual_config:
                self.visual_config[key] = value
                self.logger.debug(f"Visual config updated: {key} = {value}")

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
            
            if self.capture_region:
                self.screen_capture.save_screenshot(save_path, self.capture_region)
            else:
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
            if self.capture_region:
                frame = self.screen_capture.capture_region(*self.capture_region)
            else:
                frame = self.screen_capture.capture_screen()
                
            result = self._detect_object(frame)
            
            if save_result and result.found:
                # Draw detection result on frame and save
                import cv2
                
                # Draw all detected objects for motion detection
                if result.multiple_objects:
                    for box in result.multiple_objects:
                        x, y, w, h = box
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                elif result.bounding_box:
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