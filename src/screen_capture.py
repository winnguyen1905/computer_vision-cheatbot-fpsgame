"""
Screen Capture Module
Handles real-time screen capturing and region-based captures
"""

import cv2
import numpy as np
import pyautogui
from typing import Tuple, Optional
import time


class ScreenCapture:
    """Handles screen capturing operations"""
    
    def __init__(self):
        """Initialize screen capture system"""
        self.screen_width, self.screen_height = pyautogui.size()
        # Disable pyautogui failsafe for automation
        pyautogui.FAILSAFE = False
        
    def capture_screen(self) -> np.ndarray:
        """
        Capture the entire screen
        
        Returns:
            np.ndarray: Screen image in BGR format
        """
        try:
            # Capture screenshot using pyautogui
            screenshot = pyautogui.screenshot()
            
            # Convert PIL image to numpy array
            frame = np.array(screenshot)
            
            # Convert RGB to BGR for OpenCV
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            return frame
            
        except Exception as e:
            raise RuntimeError(f"Failed to capture screen: {e}")
    
    def capture_region(self, x: int, y: int, width: int, height: int) -> np.ndarray:
        """
        Capture a specific region of the screen
        
        Args:
            x: Left coordinate
            y: Top coordinate  
            width: Region width
            height: Region height
            
        Returns:
            np.ndarray: Region image in BGR format
        """
        try:
            # Validate region bounds
            x = max(0, min(x, self.screen_width - 1))
            y = max(0, min(y, self.screen_height - 1))
            width = min(width, self.screen_width - x)
            height = min(height, self.screen_height - y)
            
            # Capture region
            screenshot = pyautogui.screenshot(region=(x, y, width, height))
            
            # Convert to numpy array and BGR
            frame = np.array(screenshot)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            return frame
            
        except Exception as e:
            raise RuntimeError(f"Failed to capture region: {e}")
    
    def get_screen_size(self) -> Tuple[int, int]:
        """
        Get screen dimensions
        
        Returns:
            Tuple[int, int]: (width, height)
        """
        return self.screen_width, self.screen_height
    
    def capture_continuous(self, fps: int = 30):
        """
        Generator for continuous screen capture
        
        Args:
            fps: Frames per second for capture rate
            
        Yields:
            np.ndarray: Screen frames
        """
        frame_time = 1.0 / fps
        last_time = time.time()
        
        while True:
            current_time = time.time()
            
            # Maintain FPS timing
            if current_time - last_time >= frame_time:
                yield self.capture_screen()
                last_time = current_time
            else:
                time.sleep(0.001)  # Small sleep to prevent excessive CPU usage
    
    def capture_region_continuous(self, x: int, y: int, width: int, height: int, fps: int = 30):
        """
        Generator for continuous region capture
        
        Args:
            x, y, width, height: Region coordinates
            fps: Frames per second
            
        Yields:
            np.ndarray: Region frames
        """
        frame_time = 1.0 / fps
        last_time = time.time()
        
        while True:
            current_time = time.time()
            
            if current_time - last_time >= frame_time:
                yield self.capture_region(x, y, width, height)
                last_time = current_time
            else:
                time.sleep(0.001)
    
    def save_screenshot(self, filepath: str, region: Optional[Tuple[int, int, int, int]] = None):
        """
        Save a screenshot to file
        
        Args:
            filepath: Path to save image
            region: Optional region tuple (x, y, width, height)
        """
        try:
            if region:
                frame = self.capture_region(*region)
            else:
                frame = self.capture_screen()
                
            cv2.imwrite(filepath, frame)
            
        except Exception as e:
            raise RuntimeError(f"Failed to save screenshot: {e}")
    
    def get_pixel_color(self, x: int, y: int) -> Tuple[int, int, int]:
        """
        Get the color of a specific pixel
        
        Args:
            x, y: Pixel coordinates
            
        Returns:
            Tuple[int, int, int]: BGR color values
        """
        try:
            # Get single pixel region
            pixel = self.capture_region(x, y, 1, 1)
            color = pixel[0, 0]  # Get the single pixel
            
            return tuple(color.astype(int))
            
        except Exception as e:
            raise RuntimeError(f"Failed to get pixel color: {e}") 