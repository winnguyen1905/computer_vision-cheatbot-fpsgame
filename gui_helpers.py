import tkinter as tk
from tkinter import ttk
import re

class ToolTip:
    """Create a tooltip for a given widget"""
    def __init__(self, widget, text='Widget info'):
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.tipwindow = None

    def enter(self, event=None):
        self.showtip()

    def leave(self, event=None):
        self.hidetip()

    def showtip(self):
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + cy + self.widget.winfo_rooty() + 25
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                        background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                        font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

class ValidatedEntry(ttk.Entry):
    """Entry widget with input validation"""
    def __init__(self, parent, validation_type="any", **kwargs):
        super().__init__(parent, **kwargs)
        self.validation_type = validation_type
        self.setup_validation()
        
    def setup_validation(self):
        """Setup input validation based on type"""
        if self.validation_type == "int":
            vcmd = (self.register(self.validate_int), '%P')
            self.config(validate='key', validatecommand=vcmd)
        elif self.validation_type == "float":
            vcmd = (self.register(self.validate_float), '%P')
            self.config(validate='key', validatecommand=vcmd)
        elif self.validation_type == "positive_int":
            vcmd = (self.register(self.validate_positive_int), '%P')
            self.config(validate='key', validatecommand=vcmd)
        elif self.validation_type == "positive_float":
            vcmd = (self.register(self.validate_positive_float), '%P')
            self.config(validate='key', validatecommand=vcmd)
            
    def validate_int(self, value):
        """Validate integer input"""
        if value == "" or value == "-":
            return True
        try:
            int(value)
            return True
        except ValueError:
            return False
            
    def validate_float(self, value):
        """Validate float input"""
        if value == "" or value == "-" or value == ".":
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False
            
    def validate_positive_int(self, value):
        """Validate positive integer input"""
        if value == "":
            return True
        try:
            val = int(value)
            return val >= 0
        except ValueError:
            return False
            
    def validate_positive_float(self, value):
        """Validate positive float input"""
        if value == "" or value == ".":
            return True
        try:
            val = float(value)
            return val >= 0
        except ValueError:
            return False

class ConfigValidator:
    """Validate configuration values"""
    
    @staticmethod
    def validate_detection_window(width, height):
        """Validate detection window dimensions"""
        errors = []
        try:
            w, h = int(width), int(height)
            if w < 100 or w > 1920:
                errors.append("Width should be between 100 and 1920 pixels")
            if h < 100 or h > 1080:
                errors.append("Height should be between 100 and 1080 pixels")
        except ValueError:
            errors.append("Width and height must be valid integers")
        return errors
        
    @staticmethod
    def validate_capture_fps(fps):
        """Validate capture FPS"""
        errors = []
        try:
            f = int(fps)
            if f < 1 or f > 240:
                errors.append("FPS should be between 1 and 240")
        except ValueError:
            errors.append("FPS must be a valid integer")
        return errors
        
    @staticmethod
    def validate_mouse_settings(dpi, sensitivity, fov_w, fov_h):
        """Validate mouse settings"""
        errors = []
        try:
            dpi_val = int(dpi)
            if dpi_val < 100 or dpi_val > 10000:
                errors.append("DPI should be between 100 and 10000")
        except ValueError:
            errors.append("DPI must be a valid integer")
            
        try:
            sens = float(sensitivity)
            if sens < 0.1 or sens > 10.0:
                errors.append("Sensitivity should be between 0.1 and 10.0")
        except ValueError:
            errors.append("Sensitivity must be a valid number")
            
        try:
            fw, fh = int(fov_w), int(fov_h)
            if fw < 10 or fw > 200:
                errors.append("FOV Width should be between 10 and 200")
            if fh < 10 or fh > 200:
                errors.append("FOV Height should be between 10 and 200")
        except ValueError:
            errors.append("FOV values must be valid integers")
            
        return errors
        
    @staticmethod
    def validate_ai_settings(confidence, image_size):
        """Validate AI settings"""
        errors = []
        try:
            conf = float(confidence)
            if conf < 0.1 or conf > 1.0:
                errors.append("Confidence should be between 0.1 and 1.0")
        except ValueError:
            errors.append("Confidence must be a valid number")
            
        try:
            size = int(image_size)
            valid_sizes = [320, 640, 1280]
            if size not in valid_sizes:
                errors.append(f"Image size should be one of: {valid_sizes}")
        except ValueError:
            errors.append("Image size must be a valid integer")
            
        return errors

def create_tooltip(widget, text):
    """Helper function to create tooltips"""
    return ToolTip(widget, text)

def create_validated_entry(parent, validation_type="any", **kwargs):
    """Helper function to create validated entry"""
    return ValidatedEntry(parent, validation_type, **kwargs)

# Tooltip texts for different settings
TOOLTIPS = {
    'detection_width': "Width of the detection area in pixels. Smaller values improve performance.",
    'detection_height': "Height of the detection area in pixels. Smaller values improve performance.",
    'circle_capture': "Apply circular mask to detection area for better focus.",
    'capture_fps': "Frame rate for screen capture. Higher values may cause performance issues.",
    'mouse_dpi': "Your mouse DPI setting. Check your mouse software for this value.",
    'mouse_sensitivity': "In-game mouse sensitivity multiplier.",
    'ai_confidence': "AI detection confidence threshold. Lower values detect more but may include false positives.",
    'hotkey_targeting': "Key to hold for aiming assistance. Use mouse buttons or keyboard keys.",
    'auto_shoot': "Automatically shoot when target is detected and in crosshair.",
    'arduino_move': "Use Arduino for mouse movement to bypass game detection.",
    'show_overlay': "Display detection overlay on screen.",
    'show_debug': "Show debug window with detection information."
} 