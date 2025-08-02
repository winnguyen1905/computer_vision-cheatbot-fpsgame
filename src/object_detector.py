"""
Object Detection Module
Handles template matching and color-based object detection
"""

import cv2
import numpy as np
from typing import Tuple, Optional, List, Dict, Any
from dataclasses import dataclass


@dataclass
class DetectionResult:
    """Result of object detection"""
    found: bool
    center: Optional[Tuple[int, int]] = None
    confidence: float = 0.0
    bounding_box: Optional[Tuple[int, int, int, int]] = None  # (x, y, width, height)
    

class ObjectDetector:
    """Handles object detection using various methods"""
    
    def __init__(self, confidence_threshold: float = 0.8):
        """
        Initialize object detector
        
        Args:
            confidence_threshold: Minimum confidence for detection
        """
        self.confidence_threshold = confidence_threshold
        self.template_cache = {}
        
    def detect_object(self, screen_image: np.ndarray, template: np.ndarray, 
                     method: int = cv2.TM_CCOEFF_NORMED) -> DetectionResult:
        """
        Detect object using template matching
        
        Args:
            screen_image: Screen capture image
            template: Template image to find
            method: OpenCV template matching method
            
        Returns:
            DetectionResult: Detection result with location and confidence
        """
        try:
            # Convert to grayscale for better matching
            screen_gray = cv2.cvtColor(screen_image, cv2.COLOR_BGR2GRAY)
            template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            
            # Perform template matching
            result = cv2.matchTemplate(screen_gray, template_gray, method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            # Get template dimensions
            template_height, template_width = template_gray.shape
            
            # Determine if object was found based on confidence
            confidence = max_val if method in [cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR_NORMED] else 1 - min_val
            found = confidence >= self.confidence_threshold
            
            if found:
                # Calculate center point
                top_left = max_loc if method in [cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR_NORMED] else min_loc
                center_x = top_left[0] + template_width // 2
                center_y = top_left[1] + template_height // 2
                
                # Bounding box coordinates
                bounding_box = (top_left[0], top_left[1], template_width, template_height)
                
                return DetectionResult(
                    found=True,
                    center=(center_x, center_y),
                    confidence=confidence,
                    bounding_box=bounding_box
                )
            else:
                return DetectionResult(found=False, confidence=confidence)
                
        except Exception as e:
            raise RuntimeError(f"Template matching failed: {e}")
    
    def find_by_color(self, screen_image: np.ndarray, lower_color: Tuple[int, int, int], 
                     upper_color: Tuple[int, int, int], color_space: str = 'HSV') -> DetectionResult:
        """
        Find object by color range
        
        Args:
            screen_image: Screen capture image
            lower_color: Lower bound of color range
            upper_color: Upper bound of color range
            color_space: Color space ('HSV', 'RGB', 'BGR')
            
        Returns:
            DetectionResult: Detection result with location
        """
        try:
            # Convert color space if needed
            if color_space == 'HSV':
                image = cv2.cvtColor(screen_image, cv2.COLOR_BGR2HSV)
            elif color_space == 'RGB':
                image = cv2.cvtColor(screen_image, cv2.COLOR_BGR2RGB)
            else:
                image = screen_image.copy()
            
            # Create color mask
            mask = cv2.inRange(image, np.array(lower_color), np.array(upper_color))
            
            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                # Find largest contour
                largest_contour = max(contours, key=cv2.contourArea)
                area = cv2.contourArea(largest_contour)
                
                # Calculate confidence based on area
                total_pixels = screen_image.shape[0] * screen_image.shape[1]
                confidence = min(area / (total_pixels * 0.01), 1.0)  # Normalize to area percentage
                
                if confidence >= self.confidence_threshold:
                    # Get center of mass
                    moments = cv2.moments(largest_contour)
                    if moments['m00'] != 0:
                        center_x = int(moments['m10'] / moments['m00'])
                        center_y = int(moments['m01'] / moments['m00'])
                        
                        # Get bounding box
                        x, y, w, h = cv2.boundingRect(largest_contour)
                        
                        return DetectionResult(
                            found=True,
                            center=(center_x, center_y),
                            confidence=confidence,
                            bounding_box=(x, y, w, h)
                        )
            
            return DetectionResult(found=False)
            
        except Exception as e:
            raise RuntimeError(f"Color detection failed: {e}")
    
    def get_object_center(self, detection_result: DetectionResult) -> Optional[Tuple[int, int]]:
        """
        Get center coordinates from detection result
        
        Args:
            detection_result: Result from detection method
            
        Returns:
            Optional[Tuple[int, int]]: Center coordinates or None
        """
        return detection_result.center if detection_result.found else None
    
    def load_template(self, template_path: str) -> np.ndarray:
        """
        Load and cache template image
        
        Args:
            template_path: Path to template image
            
        Returns:
            np.ndarray: Loaded template image
        """
        if template_path in self.template_cache:
            return self.template_cache[template_path]
        
        try:
            template = cv2.imread(template_path)
            if template is None:
                raise FileNotFoundError(f"Could not load template: {template_path}")
            
            self.template_cache[template_path] = template
            return template
            
        except Exception as e:
            raise RuntimeError(f"Failed to load template: {e}")
    
    def detect_multiple_objects(self, screen_image: np.ndarray, template: np.ndarray,
                               threshold: Optional[float] = None) -> List[DetectionResult]:
        """
        Detect multiple instances of an object
        
        Args:
            screen_image: Screen capture image
            template: Template image to find
            threshold: Custom threshold for this detection
            
        Returns:
            List[DetectionResult]: List of all detected objects
        """
        threshold = threshold or self.confidence_threshold
        
        try:
            screen_gray = cv2.cvtColor(screen_image, cv2.COLOR_BGR2GRAY)
            template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            
            result = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF_NORMED)
            
            # Find all locations above threshold
            locations = np.where(result >= threshold)
            template_height, template_width = template_gray.shape
            
            detections = []
            
            for pt in zip(*locations[::-1]):  # Switch x and y
                center_x = pt[0] + template_width // 2
                center_y = pt[1] + template_height // 2
                confidence = result[pt[1], pt[0]]
                bounding_box = (pt[0], pt[1], template_width, template_height)
                
                detections.append(DetectionResult(
                    found=True,
                    center=(center_x, center_y),
                    confidence=confidence,
                    bounding_box=bounding_box
                ))
            
            return detections
            
        except Exception as e:
            raise RuntimeError(f"Multiple object detection failed: {e}")
    
    def set_confidence_threshold(self, threshold: float):
        """Set new confidence threshold"""
        self.confidence_threshold = max(0.0, min(1.0, threshold))
    
    def clear_template_cache(self):
        """Clear the template cache"""
        self.template_cache.clear() 