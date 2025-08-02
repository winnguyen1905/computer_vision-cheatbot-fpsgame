"""
Keyboard Controller Module
Handles global keyboard shortcuts for controlling the Object Detective
"""

import time
import logging
from typing import Dict, Callable, Optional, Any
from threading import Event, Lock
from pynput import keyboard
from pynput.keyboard import Key, KeyCode


class KeyboardController:
    """Handles global keyboard shortcuts for the tracking system"""
    
    def __init__(self, tracker_system=None):
        """
        Initialize keyboard controller
        
        Args:
            tracker_system: Reference to the TrackerSystem instance
        """
        self.tracker_system = tracker_system
        self.logger = logging.getLogger(__name__)
        
        # Shortcut handlers
        self.shortcuts: Dict[tuple, Callable] = {}
        self.pressed_keys = set()
        self.listener = None
        self.is_active = False
        
        # Thread-safe events
        self._lock = Lock()
        self._stop_event = Event()
        
        # System state
        self.is_paused = False
        self.current_method_index = 0
        self.available_methods = ['template', 'motion', 'color']
        
        # Register default shortcuts
        self._register_default_shortcuts()
        
        # Display help on initialization
        self.show_shortcuts_help()
    
    def _register_default_shortcuts(self):
        """Register default keyboard shortcuts"""
        
        # Ctrl+Shift+Q: Stop tracking (main stop command)
        self.register_shortcut(
            (Key.ctrl_l, Key.shift, KeyCode.from_char('q')),
            self._stop_tracking,
            "Stop tracking and exit"
        )
        
        # Alternative: Ctrl+Shift+X (backup stop)
        self.register_shortcut(
            (Key.ctrl_l, Key.shift, KeyCode.from_char('x')),
            self._stop_tracking,
            "Stop tracking (alternative)"
        )
        
        # Ctrl+Shift+P: Pause/Resume tracking
        self.register_shortcut(
            (Key.ctrl_l, Key.shift, KeyCode.from_char('p')),
            self._toggle_pause,
            "Pause/Resume tracking"
        )
        
        # Ctrl+Shift+S: Take screenshot
        self.register_shortcut(
            (Key.ctrl_l, Key.shift, KeyCode.from_char('s')),
            self._take_screenshot,
            "Take screenshot"
        )
        
        # Ctrl+Shift+C: Toggle auto-click
        self.register_shortcut(
            (Key.ctrl_l, Key.shift, KeyCode.from_char('c')),
            self._toggle_auto_click,
            "Toggle auto-click"
        )
        
        # Ctrl+Shift+M: Cycle detection methods
        self.register_shortcut(
            (Key.ctrl_l, Key.shift, KeyCode.from_char('m')),
            self._cycle_detection_method,
            "Cycle detection methods"
        )
        
        # Ctrl+Shift+R: Reset detection state
        self.register_shortcut(
            (Key.ctrl_l, Key.shift, KeyCode.from_char('r')),
            self._reset_detection,
            "Reset detection state"
        )
        
        # Ctrl+Shift+H: Show help
        self.register_shortcut(
            (Key.ctrl_l, Key.shift, KeyCode.from_char('h')),
            self._show_help,
            "Show shortcuts help"
        )
        
        # Ctrl+Shift+F: Toggle FPS display
        self.register_shortcut(
            (Key.ctrl_l, Key.shift, KeyCode.from_char('f')),
            self._toggle_fps_display,
            "Toggle FPS statistics display"
        )
        
        # Ctrl+Shift+T: Test detection on current frame
        self.register_shortcut(
            (Key.ctrl_l, Key.shift, KeyCode.from_char('t')),
            self._test_detection,
            "Test detection on current frame"
        )
        
        # Visual display shortcuts
        # Ctrl+Shift+V: Toggle circle display
        self.register_shortcut(
            (Key.ctrl_l, Key.shift, KeyCode.from_char('v')),
            self._toggle_circles,
            "Toggle detection circles"
        )
        
        # Ctrl+Shift+B: Toggle range display
        self.register_shortcut(
            (Key.ctrl_l, Key.shift, KeyCode.from_char('b')),
            self._toggle_range,
            "Toggle detection range"
        )
        
        # Ctrl+Shift+N: Toggle crosshair
        self.register_shortcut(
            (Key.ctrl_l, Key.shift, KeyCode.from_char('n')),
            self._toggle_crosshair,
            "Toggle crosshair display"
        )
        
        # Ctrl+Shift+Plus: Increase circle size
        self.register_shortcut(
            (Key.ctrl_l, Key.shift, KeyCode.from_char('=')),
            self._increase_circle_size,
            "Increase circle size"
        )
        
        # Ctrl+Shift+Minus: Decrease circle size  
        self.register_shortcut(
            (Key.ctrl_l, Key.shift, KeyCode.from_char('-')),
            self._decrease_circle_size,
            "Decrease circle size"
        )
    
    def register_shortcut(self, key_combination: tuple, handler: Callable, description: str = ""):
        """
        Register a keyboard shortcut
        
        Args:
            key_combination: Tuple of keys that must be pressed together
            handler: Function to call when shortcut is activated
            description: Human-readable description of the shortcut
        """
        with self._lock:
            self.shortcuts[key_combination] = {
                'handler': handler,
                'description': description
            }
            
        self.logger.debug(f"Registered shortcut: {self._format_key_combination(key_combination)} - {description}")
    
    def start_listening(self):
        """Start listening for keyboard shortcuts"""
        if self.is_active:
            self.logger.warning("Keyboard listener already active")
            return
        
        try:
            self.listener = keyboard.Listener(
                on_press=self._on_key_press,
                on_release=self._on_key_release
            )
            self.listener.start()
            self.is_active = True
            self.logger.info("Keyboard shortcut listener started")
            
        except Exception as e:
            self.logger.error(f"Failed to start keyboard listener: {e}")
    
    def stop_listening(self):
        """Stop listening for keyboard shortcuts"""
        if not self.is_active:
            return
        
        try:
            self.is_active = False
            if self.listener:
                self.listener.stop()
                self.listener = None
            
            self._stop_event.set()
            self.logger.info("Keyboard shortcut listener stopped")
            
        except Exception as e:
            self.logger.error(f"Error stopping keyboard listener: {e}")
    
    def _on_key_press(self, key):
        """Handle key press events"""
        try:
            with self._lock:
                self.pressed_keys.add(key)
                
                # Check if any registered shortcuts match current key combination
                for shortcut_keys, shortcut_info in self.shortcuts.items():
                    if self._keys_match(shortcut_keys, self.pressed_keys):
                        self.logger.info(f"Shortcut activated: {self._format_key_combination(shortcut_keys)}")
                        
                        # Execute handler in try-catch to prevent crashes
                        try:
                            shortcut_info['handler']()
                        except Exception as e:
                            self.logger.error(f"Error executing shortcut handler: {e}")
                        
                        # Clear pressed keys after successful shortcut
                        self.pressed_keys.clear()
                        break
                        
        except Exception as e:
            self.logger.error(f"Error in key press handler: {e}")
    
    def _on_key_release(self, key):
        """Handle key release events"""
        try:
            with self._lock:
                self.pressed_keys.discard(key)
        except Exception as e:
            self.logger.error(f"Error in key release handler: {e}")
    
    def _keys_match(self, target_keys: tuple, pressed_keys: set) -> bool:
        """Check if the pressed keys match the target key combination"""
        target_set = set(target_keys)
        
        # Handle modifier key variations (left/right ctrl, shift, alt)
        normalized_pressed = set()
        for key in pressed_keys:
            if key in [Key.ctrl_l, Key.ctrl_r]:
                normalized_pressed.add(Key.ctrl_l)  # Normalize to left ctrl
            elif key in [Key.shift_l, Key.shift_r]:
                normalized_pressed.add(Key.shift)   # Normalize to shift
            elif key in [Key.alt_l, Key.alt_r]:
                normalized_pressed.add(Key.alt_l)   # Normalize to left alt
            else:
                normalized_pressed.add(key)
        
        return target_set.issubset(normalized_pressed)
    
    def _format_key_combination(self, keys: tuple) -> str:
        """Format key combination for display"""
        key_names = []
        for key in keys:
            if key == Key.ctrl_l:
                key_names.append("Ctrl")
            elif key == Key.shift:
                key_names.append("Shift")
            elif key == Key.alt_l:
                key_names.append("Alt")
            elif isinstance(key, KeyCode):
                key_names.append(key.char.upper() if key.char else str(key))
            else:
                key_names.append(str(key).replace('Key.', '').title())
        
        return "+".join(key_names)
    
    # Shortcut handler methods
    def _stop_tracking(self):
        """Stop tracking completely"""
        print("\n🛑 STOP SHORTCUT ACTIVATED - Stopping Object Detective...")
        
        if self.tracker_system:
            # Use the shutdown method for graceful exit
            self.tracker_system.shutdown()
        else:
            # Stop keyboard listener if no tracker system
            self.stop_listening()
            
        print("✅ Shutdown complete")
    
    def _toggle_pause(self):
        """Toggle pause/resume tracking"""
        if not self.tracker_system:
            return
            
        self.is_paused = not self.is_paused
        
        if self.is_paused:
            print("⏸️  Tracking PAUSED (Ctrl+Shift+P to resume)")
            if hasattr(self.tracker_system, 'is_tracking'):
                self.tracker_system.is_tracking = False
        else:
            print("▶️  Tracking RESUMED")
            if hasattr(self.tracker_system, 'start_tracking'):
                self.tracker_system.start_tracking()
    
    def _take_screenshot(self):
        """Take a screenshot"""
        if not self.tracker_system:
            return
            
        try:
            timestamp = int(time.time())
            filename = f"screenshot_{timestamp}.png"
            
            if hasattr(self.tracker_system, 'capture_current_screen'):
                saved_path = self.tracker_system.capture_current_screen(filename)
                if saved_path:
                    print(f"📸 Screenshot saved: {saved_path}")
                else:
                    print("❌ Failed to save screenshot")
            else:
                print("❌ Screenshot function not available")
                
        except Exception as e:
            print(f"❌ Screenshot error: {e}")
    
    def _toggle_auto_click(self):
        """Toggle auto-click functionality"""
        if not self.tracker_system or not hasattr(self.tracker_system, 'mouse_controller'):
            print("❌ Auto-click control not available")
            return
            
        try:
            current_state = self.tracker_system.mouse_controller.settings.auto_click
            new_state = not current_state
            
            self.tracker_system.mouse_controller.settings.auto_click = new_state
            self.tracker_system.mouse_controller.settings.enable_click = new_state
            
            status = "ON" if new_state else "OFF"
            emoji = "🖱️" if new_state else "👆"
            print(f"{emoji} Auto-click: {status}")
            
        except Exception as e:
            print(f"❌ Auto-click toggle error: {e}")
    
    def _cycle_detection_method(self):
        """Cycle through available detection methods"""
        if not self.tracker_system:
            return
            
        try:
            self.current_method_index = (self.current_method_index + 1) % len(self.available_methods)
            new_method = self.available_methods[self.current_method_index]
            
            # Apply the new detection method
            if new_method == 'motion':
                self.tracker_system.track_by_motion()
            elif new_method == 'color':
                # Use default red color detection as example
                self.tracker_system.track_by_color(
                    lower_color=(0, 100, 100),
                    upper_color=(10, 255, 255),
                    color_space='HSV'
                )
            # template method requires a template file, so we skip it in cycling
            
            print(f"🔄 Detection method: {new_method.upper()}")
            
        except Exception as e:
            print(f"❌ Method cycle error: {e}")
    
    def _reset_detection(self):
        """Reset detection state"""
        if not self.tracker_system:
            return
            
        try:
            if hasattr(self.tracker_system, 'object_detector'):
                self.tracker_system.object_detector.reset_motion_detection()
                print("🔄 Detection state reset")
            else:
                print("❌ Detection reset not available")
                
        except Exception as e:
            print(f"❌ Detection reset error: {e}")
    
    def _show_help(self):
        """Display shortcuts help"""
        self.show_shortcuts_help()
    
    def _toggle_fps_display(self):
        """Toggle FPS statistics display"""
        if not self.tracker_system:
            return
            
        try:
            # Get current stats
            stats = self.tracker_system.get_tracking_stats()
            fps = stats.get('avg_fps', 0)
            detections = stats.get('objects_detected', 0)
            rate = stats.get('detection_rate', 0)
            
            print(f"📊 STATS - FPS: {fps:.1f} | Detections: {detections} | Rate: {rate:.1%}")
            
        except Exception as e:
            print(f"❌ Stats display error: {e}")
    
    def _test_detection(self):
        """Test detection on current frame"""
        if not self.tracker_system:
            return
            
        try:
            if hasattr(self.tracker_system, 'test_detection'):
                result = self.tracker_system.test_detection(save_result=True)
                
                if result.found:
                    print(f"✅ Detection test: SUCCESS (confidence: {result.confidence:.3f})")
                else:
                    print("❌ Detection test: No objects found")
            else:
                print("❌ Detection test not available")
                
        except Exception as e:
            print(f"❌ Detection test error: {e}")
    
    def _toggle_circles(self):
        """Toggle detection circles display"""
        if not self.tracker_system:
            return
            
        try:
            if hasattr(self.tracker_system, 'toggle_circle_display'):
                enabled = self.tracker_system.toggle_circle_display()
                status = "ON" if enabled else "OFF"
                emoji = "🟢" if enabled else "⭕"
                print(f"{emoji} Detection circles: {status}")
            else:
                print("❌ Circle display not available")
                
        except Exception as e:
            print(f"❌ Circle toggle error: {e}")
    
    def _toggle_range(self):
        """Toggle detection range display"""
        if not self.tracker_system:
            return
            
        try:
            if hasattr(self.tracker_system, 'toggle_range_display'):
                enabled = self.tracker_system.toggle_range_display()
                status = "ON" if enabled else "OFF"
                emoji = "🎯" if enabled else "⭕"
                print(f"{emoji} Detection range: {status}")
            else:
                print("❌ Range display not available")
                
        except Exception as e:
            print(f"❌ Range toggle error: {e}")
    
    def _toggle_crosshair(self):
        """Toggle crosshair display"""
        if not self.tracker_system:
            return
            
        try:
            if hasattr(self.tracker_system, 'toggle_crosshair_display'):
                enabled = self.tracker_system.toggle_crosshair_display()
                status = "ON" if enabled else "OFF"
                emoji = "➕" if enabled else "⭕"
                print(f"{emoji} Crosshair: {status}")
            else:
                print("❌ Crosshair display not available")
                
        except Exception as e:
            print(f"❌ Crosshair toggle error: {e}")
    
    def _increase_circle_size(self):
        """Increase detection circle size"""
        if not self.tracker_system:
            return
            
        try:
            if hasattr(self.tracker_system, 'visual_config'):
                current_radius = self.tracker_system.visual_config['circle_radius']
                new_radius = min(current_radius + 10, 200)
                self.tracker_system.set_circle_radius(new_radius)
                print(f"🔵 Circle radius: {new_radius}px")
            else:
                print("❌ Circle size control not available")
                
        except Exception as e:
            print(f"❌ Circle size error: {e}")
    
    def _decrease_circle_size(self):
        """Decrease detection circle size"""
        if not self.tracker_system:
            return
            
        try:
            if hasattr(self.tracker_system, 'visual_config'):
                current_radius = self.tracker_system.visual_config['circle_radius']
                new_radius = max(current_radius - 10, 10)
                self.tracker_system.set_circle_radius(new_radius)
                print(f"🔵 Circle radius: {new_radius}px")
            else:
                print("❌ Circle size control not available")
                
        except Exception as e:
            print(f"❌ Circle size error: {e}")
    
    def show_shortcuts_help(self):
        """Display all available shortcuts"""
        print("\n" + "="*60)
        print("🎮 OBJECT DETECTIVE - KEYBOARD SHORTCUTS")
        print("="*60)
        
        for key_combo, shortcut_info in self.shortcuts.items():
            key_str = self._format_key_combination(key_combo)
            description = shortcut_info['description']
            print(f"  {key_str:<20} - {description}")
        
        print("="*60)
        print("💡 Note: Shortcuts work globally (even when window is not focused)")
        print("🛑 Primary stop command: Ctrl+Shift+Q")
        print("="*60 + "\n")
    
    def set_tracker_system(self, tracker_system):
        """Set or update the tracker system reference"""
        self.tracker_system = tracker_system
    
    def is_listening(self) -> bool:
        """Check if the keyboard listener is active"""
        return self.is_active 