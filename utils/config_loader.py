"""
Configuration Loader Module
Handles loading and validation of configuration files
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
import logging


class ConfigLoader:
    """Handles loading and validation of configuration files"""
    
    def __init__(self, config_path: str = "config.json"):
        """
        Initialize config loader
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = Path(config_path)
        self.logger = logging.getLogger(__name__)
        
        # Default configuration
        self.default_config = {
            "capture_region": {
                "top": 0,
                "left": 0,
                "width": 1920,
                "height": 1080
            },
            "tracking": {
                "fps": 30,
                "confidence_threshold": 0.8,
                "smooth_movement": True,
                "movement_speed": 0.3
            },
            "detection": {
                "method": "template",
                "template_path": "templates/target_object.png",
                "min_area": 500,
                "background_history": 50,
                "background_threshold": 16,
                "motion_threshold": 25,
                "dilate_iterations": 2,
                "blur_kernel_size": 21
            },
            "mouse": {
                "auto_click": False,
                "click_delay": 0.1,
                "move_duration": 0.1,
                "enable_click": False
            }
        }
    
    def load(self) -> Dict[str, Any]:
        """
        Load configuration from file with fallback to defaults
        
        Returns:
            Dict containing configuration
        """
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                
                # Merge with defaults
                config = self._merge_config(self.default_config.copy(), user_config)
                
                # Validate configuration
                self._validate_config(config)
                
                self.logger.info(f"Configuration loaded from: {self.config_path}")
                return config
            
            else:
                self.logger.warning(f"Config file not found: {self.config_path}, using defaults")
                return self.default_config.copy()
                
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in config file: {e}")
            self.logger.info("Using default configuration")
            return self.default_config.copy()
            
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            self.logger.info("Using default configuration")
            return self.default_config.copy()
    
    def save(self, config: Dict[str, Any], config_path: Optional[str] = None):
        """
        Save configuration to file
        
        Args:
            config: Configuration dictionary to save
            config_path: Optional path override
        """
        try:
            save_path = Path(config_path) if config_path else self.config_path
            
            # Create directory if it doesn't exist
            save_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Validate before saving
            self._validate_config(config)
            
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Configuration saved to: {save_path}")
            
        except Exception as e:
            self.logger.error(f"Error saving config: {e}")
            raise
    
    def _merge_config(self, default: Dict[str, Any], user: Dict[str, Any]) -> Dict[str, Any]:
        """
        Recursively merge user config with defaults
        
        Args:
            default: Default configuration
            user: User configuration
            
        Returns:
            Merged configuration
        """
        for key, value in user.items():
            if key in default:
                if isinstance(default[key], dict) and isinstance(value, dict):
                    default[key] = self._merge_config(default[key], value)
                else:
                    default[key] = value
            else:
                # Log unknown configuration keys
                self.logger.warning(f"Unknown configuration key: {key}")
                default[key] = value
        
        return default
    
    def _validate_config(self, config: Dict[str, Any]):
        """
        Validate configuration values
        
        Args:
            config: Configuration to validate
            
        Raises:
            ValueError: If configuration is invalid
        """
        try:
            # Validate capture region section
            capture_region = config.get('capture_region', {})
            
            for dimension in ['top', 'left', 'width', 'height']:
                value = capture_region.get(dimension, 0)
                if not isinstance(value, int) or value < 0:
                    raise ValueError(f"Invalid capture region {dimension}: {value} (must be non-negative integer)")
            
            # Validate tracking section
            tracking = config.get('tracking', {})
            
            fps = tracking.get('fps', 30)
            if not isinstance(fps, int) or fps < 1 or fps > 120:
                raise ValueError(f"Invalid FPS value: {fps} (must be 1-120)")
            
            confidence = tracking.get('confidence_threshold', 0.8)
            if not isinstance(confidence, (int, float)) or confidence < 0 or confidence > 1:
                raise ValueError(f"Invalid confidence threshold: {confidence} (must be 0.0-1.0)")
            
            movement_speed = tracking.get('movement_speed', 0.3)
            if not isinstance(movement_speed, (int, float)) or movement_speed < 0 or movement_speed > 1:
                raise ValueError(f"Invalid movement speed: {movement_speed} (must be 0.0-1.0)")
            
            # Validate detection section
            detection = config.get('detection', {})
            
            method = detection.get('method', 'template')
            valid_methods = ['template', 'color', 'motion', 'mog2', 'knn', 'frame_diff']
            if method not in valid_methods:
                raise ValueError(f"Invalid detection method: {method} (must be one of {valid_methods})")
            
            # Validate motion detection parameters
            if method in ['motion', 'mog2', 'knn', 'frame_diff']:
                min_area = detection.get('min_area', 500)
                if not isinstance(min_area, int) or min_area < 0:
                    raise ValueError(f"Invalid min_area: {min_area} (must be non-negative integer)")
                
                motion_threshold = detection.get('motion_threshold', 25)
                if not isinstance(motion_threshold, int) or motion_threshold < 0 or motion_threshold > 255:
                    raise ValueError(f"Invalid motion_threshold: {motion_threshold} (must be 0-255)")
                
                dilate_iterations = detection.get('dilate_iterations', 2)
                if not isinstance(dilate_iterations, int) or dilate_iterations < 0:
                    raise ValueError(f"Invalid dilate_iterations: {dilate_iterations} (must be non-negative integer)")
                
                blur_kernel_size = detection.get('blur_kernel_size', 21)
                if not isinstance(blur_kernel_size, int) or blur_kernel_size < 1 or blur_kernel_size % 2 == 0:
                    raise ValueError(f"Invalid blur_kernel_size: {blur_kernel_size} (must be positive odd integer)")
                
                if method in ['mog2', 'knn']:
                    background_history = detection.get('background_history', 50)
                    if not isinstance(background_history, int) or background_history < 1:
                        raise ValueError(f"Invalid background_history: {background_history} (must be positive integer)")
                    
                    background_threshold = detection.get('background_threshold', 16)
                    if not isinstance(background_threshold, (int, float)) or background_threshold < 0:
                        raise ValueError(f"Invalid background_threshold: {background_threshold} (must be non-negative)")
            
            # Validate mouse section
            mouse = config.get('mouse', {})
            
            click_delay = mouse.get('click_delay', 0.1)
            if not isinstance(click_delay, (int, float)) or click_delay < 0:
                raise ValueError(f"Invalid click delay: {click_delay} (must be >= 0)")
            
            move_duration = mouse.get('move_duration', 0.1)
            if not isinstance(move_duration, (int, float)) or move_duration < 0:
                raise ValueError(f"Invalid move duration: {move_duration} (must be >= 0)")
            
            enable_click = mouse.get('enable_click', False)
            if not isinstance(enable_click, bool):
                raise ValueError(f"Invalid enable_click: {enable_click} (must be boolean)")
            
        except Exception as e:
            raise ValueError(f"Configuration validation failed: {e}")
    
    def get_template_path(self, config: Dict[str, Any]) -> str:
        """
        Get absolute template path from configuration
        
        Args:
            config: Configuration dictionary
            
        Returns:
            Absolute path to template file
        """
        template_path = config.get('detection', {}).get('template_path', '')
        
        if not template_path:
            return ''
        
        # Convert to absolute path if relative
        path = Path(template_path)
        if not path.is_absolute():
            # Resolve relative to config file directory
            path = self.config_path.parent / path
        
        return str(path)
    
    def create_default_config(self, force: bool = False):
        """
        Create default configuration file
        
        Args:
            force: Overwrite existing config file
        """
        if self.config_path.exists() and not force:
            self.logger.warning(f"Config file already exists: {self.config_path}")
            return
        
        self.save(self.default_config)
        self.logger.info(f"Default configuration created: {self.config_path}")
    
    def update_config(self, updates: Dict[str, Any]):
        """
        Update configuration file with new values
        
        Args:
            updates: Dictionary of updates to apply
        """
        # Load current config
        current_config = self.load()
        
        # Apply updates
        updated_config = self._merge_config(current_config, updates)
        
        # Save updated config
        self.save(updated_config)
    
    def get_config_value(self, key_path: str, default: Any = None) -> Any:
        """
        Get configuration value using dot notation
        
        Args:
            key_path: Dot-separated key path (e.g., 'tracking.fps')
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        config = self.load()
        
        try:
            keys = key_path.split('.')
            value = config
            
            for key in keys:
                value = value[key]
            
            return value
            
        except (KeyError, TypeError):
            return default 