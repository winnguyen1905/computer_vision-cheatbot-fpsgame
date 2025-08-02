"""
Mouse Controller Module
Handles mouse movement and clicking operations
"""

import pyautogui
import time
import math
from typing import Tuple, Optional
import threading
from dataclasses import dataclass


@dataclass
class MouseSettings:
    """Mouse control settings"""
    movement_speed: float = 0.3  # 0.0 to 1.0
    smooth_movement: bool = True
    auto_click: bool = False
    click_delay: float = 0.1
    

class MouseController:
    """Handles mouse movement and clicking operations"""
    
    def __init__(self, settings: Optional[MouseSettings] = None):
        """
        Initialize mouse controller
        
        Args:
            settings: Mouse control settings
        """
        self.settings = settings or MouseSettings()
        
        # Disable pyautogui failsafe for automation
        pyautogui.FAILSAFE = False
        
        # Current mouse position
        self.current_x, self.current_y = pyautogui.position()
        
        # Movement thread control
        self._movement_thread = None
        self._stop_movement = False
        
    def move_to(self, x: int, y: int):
        """
        Move mouse to specific coordinates instantly
        
        Args:
            x: Target x coordinate
            y: Target y coordinate
        """
        try:
            pyautogui.moveTo(x, y)
            self.current_x, self.current_y = x, y
            
        except Exception as e:
            raise RuntimeError(f"Failed to move mouse: {e}")
    
    def smooth_move_to(self, x: int, y: int, duration: Optional[float] = None):
        """
        Move mouse smoothly to target coordinates
        
        Args:
            x: Target x coordinate
            y: Target y coordinate
            duration: Movement duration in seconds
        """
        if not self.settings.smooth_movement:
            self.move_to(x, y)
            return
        
        try:
            # Calculate duration based on distance and speed
            if duration is None:
                distance = math.sqrt((x - self.current_x)**2 + (y - self.current_y)**2)
                duration = (distance / 1000) * (1.0 - self.settings.movement_speed)
                duration = max(0.1, min(duration, 2.0))  # Clamp between 0.1 and 2.0 seconds
            
            # Use pyautogui's smooth movement
            pyautogui.moveTo(x, y, duration=duration, tween=pyautogui.easeOutQuad)
            self.current_x, self.current_y = x, y
            
        except Exception as e:
            raise RuntimeError(f"Failed to smooth move mouse: {e}")
    
    def click_at(self, x: int, y: int, button: str = 'left', clicks: int = 1):
        """
        Click at specific coordinates
        
        Args:
            x: Click x coordinate
            y: Click y coordinate
            button: Mouse button ('left', 'right', 'middle')
            clicks: Number of clicks
        """
        try:
            # Move to position first
            if self.settings.smooth_movement:
                self.smooth_move_to(x, y)
            else:
                self.move_to(x, y)
            
            # Add delay before clicking
            time.sleep(self.settings.click_delay)
            
            # Perform click
            pyautogui.click(x, y, clicks=clicks, button=button)
            
        except Exception as e:
            raise RuntimeError(f"Failed to click at position: {e}")
    
    def double_click_at(self, x: int, y: int):
        """Double click at coordinates"""
        self.click_at(x, y, clicks=2)
    
    def right_click_at(self, x: int, y: int):
        """Right click at coordinates"""
        self.click_at(x, y, button='right')
    
    def drag_to(self, start_x: int, start_y: int, end_x: int, end_y: int, 
                duration: float = 1.0, button: str = 'left'):
        """
        Drag from start position to end position
        
        Args:
            start_x, start_y: Starting coordinates
            end_x, end_y: Ending coordinates
            duration: Drag duration
            button: Mouse button to use for dragging
        """
        try:
            # Move to start position
            self.move_to(start_x, start_y)
            
            # Perform drag
            pyautogui.drag(end_x - start_x, end_y - start_y, 
                          duration=duration, button=button)
            
            self.current_x, self.current_y = end_x, end_y
            
        except Exception as e:
            raise RuntimeError(f"Failed to drag: {e}")
    
    def scroll_at(self, x: int, y: int, clicks: int):
        """
        Scroll at specific coordinates
        
        Args:
            x, y: Scroll position
            clicks: Number of scroll clicks (positive for up, negative for down)
        """
        try:
            # Move to position
            self.move_to(x, y)
            
            # Scroll
            pyautogui.scroll(clicks, x=x, y=y)
            
        except Exception as e:
            raise RuntimeError(f"Failed to scroll: {e}")
    
    def get_current_position(self) -> Tuple[int, int]:
        """
        Get current mouse position
        
        Returns:
            Tuple[int, int]: Current (x, y) coordinates
        """
        return pyautogui.position()
    
    def track_to_position(self, x: int, y: int, auto_click: Optional[bool] = None):
        """
        Move mouse to position with optional auto-click
        
        Args:
            x, y: Target coordinates
            auto_click: Override auto-click setting
        """
        # Move mouse
        if self.settings.smooth_movement:
            self.smooth_move_to(x, y)
        else:
            self.move_to(x, y)
        
        # Auto-click if enabled
        should_click = auto_click if auto_click is not None else self.settings.auto_click
        if should_click:
            time.sleep(self.settings.click_delay)
            pyautogui.click()
    
    def start_continuous_tracking(self, target_position_func, stop_condition_func=None):
        """
        Start continuous mouse tracking in a separate thread
        
        Args:
            target_position_func: Function that returns target (x, y) or None
            stop_condition_func: Function that returns True to stop tracking
        """
        def tracking_loop():
            while not self._stop_movement:
                try:
                    # Check stop condition
                    if stop_condition_func and stop_condition_func():
                        break
                    
                    # Get target position
                    target_pos = target_position_func()
                    
                    if target_pos:
                        x, y = target_pos
                        self.track_to_position(x, y)
                    
                    time.sleep(0.01)  # Small delay to prevent excessive CPU usage
                    
                except Exception as e:
                    print(f"Tracking error: {e}")
                    time.sleep(0.1)
        
        # Stop any existing tracking
        self.stop_continuous_tracking()
        
        # Start new tracking thread
        self._stop_movement = False
        self._movement_thread = threading.Thread(target=tracking_loop, daemon=True)
        self._movement_thread.start()
    
    def stop_continuous_tracking(self):
        """Stop continuous tracking"""
        self._stop_movement = True
        if self._movement_thread and self._movement_thread.is_alive():
            self._movement_thread.join(timeout=1.0)
    
    def update_settings(self, **kwargs):
        """Update mouse settings"""
        for key, value in kwargs.items():
            if hasattr(self.settings, key):
                setattr(self.settings, key, value)
    
    def calibrate_movement_speed(self, target_x: int, target_y: int, 
                                desired_duration: float) -> float:
        """
        Calibrate movement speed based on desired duration
        
        Args:
            target_x, target_y: Target coordinates
            desired_duration: Desired movement duration
            
        Returns:
            float: Calculated movement speed
        """
        start_time = time.time()
        start_x, start_y = self.get_current_position()
        
        # Test movement
        self.smooth_move_to(target_x, target_y, desired_duration)
        
        actual_duration = time.time() - start_time
        distance = math.sqrt((target_x - start_x)**2 + (target_y - start_y)**2)
        
        # Calculate optimal speed
        speed_factor = desired_duration / actual_duration
        new_speed = max(0.1, min(1.0, self.settings.movement_speed * speed_factor))
        
        return new_speed 