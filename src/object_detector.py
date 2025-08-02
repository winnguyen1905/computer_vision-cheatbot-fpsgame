"""
Object Detection Module
Handles template matching, color-based object detection, and motion detection
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
    multiple_objects: Optional[List[Tuple[int, int, int, int]]] = None  # For motion detection
    

class ObjectDetector:
    """Handles object detection using various methods"""
    
    def __init__(self, confidence_threshold: float = 0.8, motion_config: Optional[Dict[str, Any]] = None):
        """
        Initialize object detector
        
        Args:
            confidence_threshold: Minimum confidence for detection
            motion_config: Configuration for motion detection
        """
        self.confidence_threshold = confidence_threshold
        self.template_cache = {}
        
        # Motion detection parameters
        self.motion_config = motion_config or {}
        self.min_area = self.motion_config.get('min_area', 500)
        self.motion_threshold = self.motion_config.get('motion_threshold', 25)
        self.dilate_iterations = self.motion_config.get('dilate_iterations', 2)
        self.blur_kernel_size = self.motion_config.get('blur_kernel_size', 21)
        self.background_history = self.motion_config.get('background_history', 50)
        self.background_threshold = self.motion_config.get('background_threshold', 16)
        
        # Motion detection state
        self.prev_gray = None
        self.background_subtractor = None
        self.motion_method = 'frame_diff'  # 'frame_diff' or 'mog2' or 'knn'
        
        # Initialize background subtractor if configured
        if self.motion_config.get('use_background_subtraction', False):
            self.motion_method = 'mog2'
            self.background_subtractor = cv2.createBackgroundSubtractorMOG2(
                history=self.background_history,
                varThreshold=self.background_threshold,
                detectShadows=True
            )
        
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

    def detect_motion(self, screen_image: np.ndarray) -> DetectionResult:
        """
        Detect motion in the screen image using frame differencing or background subtraction
        
        Args:
            screen_image: Screen capture image
            
        Returns:
            DetectionResult: Detection result with motion areas
        """
        try:
            if self.motion_method == 'frame_diff':
                return self._detect_motion_frame_diff(screen_image)
            elif self.motion_method == 'mog2':
                return self._detect_motion_background_subtraction(screen_image)
            else:
                raise ValueError(f"Unknown motion detection method: {self.motion_method}")
                
        except Exception as e:
            raise RuntimeError(f"Motion detection failed: {e}")
    
    def _detect_motion_frame_diff(self, screen_image: np.ndarray) -> DetectionResult:
        """
        Detect motion using frame differencing
        
        Args:
            screen_image: Current frame
            
        Returns:
            DetectionResult: Motion detection result
        """
        # Convert to grayscale and blur
        gray = cv2.cvtColor(screen_image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (self.blur_kernel_size, self.blur_kernel_size), 0)
        
        # Initialize previous frame
        if self.prev_gray is None:
            self.prev_gray = gray
            return DetectionResult(found=False)
        
        # Compute absolute difference
        delta = cv2.absdiff(self.prev_gray, gray)
        self.prev_gray = gray
        
        # Threshold and dilate to fill holes
        thresh = cv2.threshold(delta, self.motion_threshold, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=self.dilate_iterations)
        
        # Find contours and filter by area
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        motion_boxes = []
        largest_area = 0
        largest_center = None
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area >= self.min_area:
                x, y, w, h = cv2.boundingRect(contour)
                motion_boxes.append((x, y, w, h))
                
                # Track largest motion area for primary center
                if area > largest_area:
                    largest_area = area
                    largest_center = (x + w // 2, y + h // 2)
        
        if motion_boxes:
            # Calculate confidence based on largest motion area
            confidence = min(largest_area / (screen_image.shape[0] * screen_image.shape[1] * 0.1), 1.0)
            
            return DetectionResult(
                found=True,
                center=largest_center,
                confidence=confidence,
                bounding_box=motion_boxes[0] if motion_boxes else None,  # Largest box
                multiple_objects=motion_boxes
            )
        
        return DetectionResult(found=False)
    
    def _detect_motion_background_subtraction(self, screen_image: np.ndarray) -> DetectionResult:
        """
        Detect motion using background subtraction (MOG2)
        
        Args:
            screen_image: Current frame
            
        Returns:
            DetectionResult: Motion detection result
        """
        if self.background_subtractor is None:
            return DetectionResult(found=False)
        
        # Apply background subtraction
        fg_mask = self.background_subtractor.apply(screen_image)
        
        # Clean up the mask
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, kernel)
        fg_mask = cv2.dilate(fg_mask, None, iterations=self.dilate_iterations)
        
        # Find contours
        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        motion_boxes = []
        largest_area = 0
        largest_center = None
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area >= self.min_area:
                x, y, w, h = cv2.boundingRect(contour)
                motion_boxes.append((x, y, w, h))
                
                if area > largest_area:
                    largest_area = area
                    largest_center = (x + w // 2, y + h // 2)
        
        if motion_boxes:
            confidence = min(largest_area / (screen_image.shape[0] * screen_image.shape[1] * 0.1), 1.0)
            
            return DetectionResult(
                found=True,
                center=largest_center,
                confidence=confidence,
                bounding_box=motion_boxes[0] if motion_boxes else None,
                multiple_objects=motion_boxes
            )
        
        return DetectionResult(found=False)
    
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
    
    def set_motion_method(self, method: str):
        """
        Set motion detection method
        
        Args:
            method: 'frame_diff' or 'mog2' or 'knn'
        """
        if method == 'mog2' and self.background_subtractor is None:
            self.background_subtractor = cv2.createBackgroundSubtractorMOG2(
                history=self.background_history,
                varThreshold=self.background_threshold,
                detectShadows=True
            )
        elif method == 'knn' and self.background_subtractor is None:
            self.background_subtractor = cv2.createBackgroundSubtractorKNN(
                history=self.background_history,
                dist2Threshold=400.0,
                detectShadows=True
            )
        
        self.motion_method = method
    
    def reset_motion_detection(self):
        """Reset motion detection state"""
        self.prev_gray = None
        if self.background_subtractor is not None:
            # Recreate background subtractor to reset learning
            if self.motion_method == 'mog2':
                self.background_subtractor = cv2.createBackgroundSubtractorMOG2(
                    history=self.background_history,
                    varThreshold=self.background_threshold,
                    detectShadows=True
                )
            elif self.motion_method == 'knn':
                self.background_subtractor = cv2.createBackgroundSubtractorKNN(
                    history=self.background_history,
                    dist2Threshold=400.0,
                    detectShadows=True
                )
    
    def clear_template_cache(self):
        """Clear the template cache"""
        self.template_cache.clear() 