import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import configparser
import os
import threading
from pathlib import Path
from gui_helpers import create_tooltip, create_validated_entry, ConfigValidator, TOOLTIPS

class ConfigGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Object Detective - Configuration Manager")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Configuration file path
        self.config_path = "config.ini"
        self.config = configparser.ConfigParser()
        
        # Load current configuration
        self.load_config()
        
        # Create GUI elements
        self.create_widgets()
        
        # Center window
        self.center_window()
        
    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def load_config(self):
        """Load configuration from config.ini"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config.read_file(f)
        except FileNotFoundError:
            messagebox.showerror("Error", "config.ini file not found!")
            self.root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load config: {str(e)}")
            
    def save_config(self):
        """Save configuration to config.ini"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                self.config.write(f)
            messagebox.showinfo("Success", "Configuration saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save config: {str(e)}")
            
    def create_widgets(self):
        """Create all GUI widgets"""
        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Create tabs
        self.create_detection_tab()
        self.create_capture_tab()
        self.create_aim_tab()
        self.create_hotkeys_tab()
        self.create_mouse_tab()
        self.create_shooting_tab()
        self.create_arduino_tab()
        self.create_ai_tab()
        self.create_overlay_tab()
        self.create_debug_tab()
        
        # Create bottom buttons
        self.create_buttons(main_frame)
        
    def create_detection_tab(self):
        """Create Detection Window tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Detection Window")
        
        # Detection window settings
        settings_frame = ttk.LabelFrame(frame, text="Detection Window Settings", padding=10)
        settings_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Width
        ttk.Label(settings_frame, text="Detection Window Width:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.detection_width = tk.StringVar(value=self.config.get('Detection window', 'detection_window_width'))
        width_entry = create_validated_entry(settings_frame, "positive_int", textvariable=self.detection_width, width=10)
        width_entry.grid(row=0, column=1, sticky=tk.W, padx=5)
        create_tooltip(width_entry, TOOLTIPS['detection_width'])
        ttk.Label(settings_frame, text="pixels").grid(row=0, column=2, sticky=tk.W)
        
        # Height
        ttk.Label(settings_frame, text="Detection Window Height:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.detection_height = tk.StringVar(value=self.config.get('Detection window', 'detection_window_height'))
        height_entry = create_validated_entry(settings_frame, "positive_int", textvariable=self.detection_height, width=10)
        height_entry.grid(row=1, column=1, sticky=tk.W, padx=5)
        create_tooltip(height_entry, TOOLTIPS['detection_height'])
        ttk.Label(settings_frame, text="pixels").grid(row=1, column=2, sticky=tk.W)
        
        # Circle capture
        self.circle_capture = tk.BooleanVar(value=self.config.getboolean('Detection window', 'circle_capture'))
        ttk.Checkbutton(settings_frame, text="Enable Circle Capture", variable=self.circle_capture).grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=5)
        
        # Add description
        desc_frame = ttk.LabelFrame(frame, text="Description", padding=10)
        desc_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(desc_frame, text="Detection window settings control the size and shape of the area where AI detection occurs.\nSmaller windows improve performance but reduce detection range.").pack(anchor=tk.W)
        
    def create_capture_tab(self):
        """Create Capture Methods tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Capture Methods")
        
        # Global settings
        global_frame = ttk.LabelFrame(frame, text="Global Capture Settings", padding=10)
        global_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(global_frame, text="Capture FPS:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.capture_fps = tk.StringVar(value=self.config.get('Capture Methods', 'capture_fps'))
        ttk.Entry(global_frame, textvariable=self.capture_fps, width=10).grid(row=0, column=1, sticky=tk.W, padx=5)
        ttk.Label(global_frame, text="fps").grid(row=0, column=2, sticky=tk.W)
        
        # Capture methods
        methods_frame = ttk.LabelFrame(frame, text="Capture Methods (Select Only One)", padding=10)
        methods_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Bettercam
        self.bettercam_capture = tk.BooleanVar(value=self.config.getboolean('Capture Methods', 'Bettercam_capture'))
        ttk.Checkbutton(methods_frame, text="Bettercam Capture", variable=self.bettercam_capture).grid(row=0, column=0, sticky=tk.W, pady=2)
        
        ttk.Label(methods_frame, text="Monitor ID:").grid(row=1, column=0, sticky=tk.W, pady=2, padx=20)
        self.bettercam_monitor = tk.StringVar(value=self.config.get('Capture Methods', 'bettercam_monitor_id'))
        ttk.Entry(methods_frame, textvariable=self.bettercam_monitor, width=5).grid(row=1, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(methods_frame, text="GPU ID:").grid(row=2, column=0, sticky=tk.W, pady=2, padx=20)
        self.bettercam_gpu = tk.StringVar(value=self.config.get('Capture Methods', 'bettercam_gpu_id'))
        ttk.Entry(methods_frame, textvariable=self.bettercam_gpu, width=5).grid(row=2, column=1, sticky=tk.W, padx=5)
        
        # OBS
        self.obs_capture = tk.BooleanVar(value=self.config.getboolean('Capture Methods', 'Obs_capture'))
        ttk.Checkbutton(methods_frame, text="OBS Capture", variable=self.obs_capture).grid(row=3, column=0, sticky=tk.W, pady=2)
        
        ttk.Label(methods_frame, text="Camera ID:").grid(row=4, column=0, sticky=tk.W, pady=2, padx=20)
        self.obs_camera = tk.StringVar(value=self.config.get('Capture Methods', 'Obs_camera_id'))
        ttk.Entry(methods_frame, textvariable=self.obs_camera, width=5).grid(row=4, column=1, sticky=tk.W, padx=5)
        
        # MSS
        self.mss_capture = tk.BooleanVar(value=self.config.getboolean('Capture Methods', 'mss_capture'))
        ttk.Checkbutton(methods_frame, text="MSS Capture", variable=self.mss_capture).grid(row=5, column=0, sticky=tk.W, pady=2)
        
    def create_aim_tab(self):
        """Create Aim tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Aim Settings")
        
        # Aim settings
        aim_frame = ttk.LabelFrame(frame, text="Aim Configuration", padding=10)
        aim_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Body Y offset
        ttk.Label(aim_frame, text="Body Y Offset:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.body_y_offset = tk.StringVar(value=self.config.get('Aim', 'body_y_offset'))
        ttk.Entry(aim_frame, textvariable=self.body_y_offset, width=10).grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # Checkboxes
        self.hideout_targets = tk.BooleanVar(value=self.config.getboolean('Aim', 'hideout_targets'))
        ttk.Checkbutton(aim_frame, text="Enable Hideout Targets", variable=self.hideout_targets).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        self.disable_headshot = tk.BooleanVar(value=self.config.getboolean('Aim', 'disable_headshot'))
        ttk.Checkbutton(aim_frame, text="Disable Headshot", variable=self.disable_headshot).grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        self.disable_prediction = tk.BooleanVar(value=self.config.getboolean('Aim', 'disable_prediction'))
        ttk.Checkbutton(aim_frame, text="Disable Prediction", variable=self.disable_prediction).grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=2)
        
        # Prediction interval
        ttk.Label(aim_frame, text="Prediction Interval:").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.prediction_interval = tk.StringVar(value=self.config.get('Aim', 'prediction_interval'))
        ttk.Entry(aim_frame, textvariable=self.prediction_interval, width=10).grid(row=4, column=1, sticky=tk.W, padx=5)
        
        self.third_person = tk.BooleanVar(value=self.config.getboolean('Aim', 'third_person'))
        ttk.Checkbutton(aim_frame, text="Third Person Mode", variable=self.third_person).grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=2)
        
    def create_hotkeys_tab(self):
        """Create Hotkeys tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Hotkeys")
        
        # Hotkeys settings
        hotkeys_frame = ttk.LabelFrame(frame, text="Hotkey Configuration", padding=10)
        hotkeys_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Targeting hotkey
        ttk.Label(hotkeys_frame, text="Targeting Hotkey:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.hotkey_targeting = tk.StringVar(value=self.config.get('Hotkeys', 'hotkey_targeting'))
        ttk.Entry(hotkeys_frame, textvariable=self.hotkey_targeting, width=15).grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # Exit hotkey
        ttk.Label(hotkeys_frame, text="Exit Hotkey:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.hotkey_exit = tk.StringVar(value=self.config.get('Hotkeys', 'hotkey_exit'))
        ttk.Entry(hotkeys_frame, textvariable=self.hotkey_exit, width=15).grid(row=1, column=1, sticky=tk.W, padx=5)
        
        # Pause hotkey
        ttk.Label(hotkeys_frame, text="Pause Hotkey:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.hotkey_pause = tk.StringVar(value=self.config.get('Hotkeys', 'hotkey_pause'))
        ttk.Entry(hotkeys_frame, textvariable=self.hotkey_pause, width=15).grid(row=2, column=1, sticky=tk.W, padx=5)
        
        # Reload config hotkey
        ttk.Label(hotkeys_frame, text="Reload Config Hotkey:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.hotkey_reload_config = tk.StringVar(value=self.config.get('Hotkeys', 'hotkey_reload_config'))
        ttk.Entry(hotkeys_frame, textvariable=self.hotkey_reload_config, width=15).grid(row=3, column=1, sticky=tk.W, padx=5)
        
        # Add hotkey reference
        ref_frame = ttk.LabelFrame(frame, text="Available Keys", padding=10)
        ref_frame.pack(fill=tk.X, padx=5, pady=5)
        reference_text = "Mouse: LeftMouseButton, RightMouseButton, MiddleMouseButton, X1MouseButton, X2MouseButton\n"
        reference_text += "Function Keys: F1-F12\n"
        reference_text += "Letters: A-Z\n"
        reference_text += "Numbers: Key0-Key9\n"
        reference_text += "Special: Space, Enter, Escape, Tab, Shift, Ctrl, Alt"
        ttk.Label(ref_frame, text=reference_text, justify=tk.LEFT).pack(anchor=tk.W)
        
    def create_mouse_tab(self):
        """Create Mouse tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Mouse Settings")
        
        # Mouse basic settings
        basic_frame = ttk.LabelFrame(frame, text="Basic Mouse Settings", padding=10)
        basic_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # DPI
        ttk.Label(basic_frame, text="Mouse DPI:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.mouse_dpi = tk.StringVar(value=self.config.get('Mouse', 'mouse_dpi'))
        ttk.Entry(basic_frame, textvariable=self.mouse_dpi, width=10).grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # Sensitivity
        ttk.Label(basic_frame, text="Mouse Sensitivity:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.mouse_sensitivity = tk.StringVar(value=self.config.get('Mouse', 'mouse_sensitivity'))
        ttk.Entry(basic_frame, textvariable=self.mouse_sensitivity, width=10).grid(row=1, column=1, sticky=tk.W, padx=5)
        
        # FOV settings
        fov_frame = ttk.LabelFrame(frame, text="Field of View Settings", padding=10)
        fov_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(fov_frame, text="FOV Width:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.mouse_fov_width = tk.StringVar(value=self.config.get('Mouse', 'mouse_fov_width'))
        ttk.Entry(fov_frame, textvariable=self.mouse_fov_width, width=10).grid(row=0, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(fov_frame, text="FOV Height:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.mouse_fov_height = tk.StringVar(value=self.config.get('Mouse', 'mouse_fov_height'))
        ttk.Entry(fov_frame, textvariable=self.mouse_fov_height, width=10).grid(row=1, column=1, sticky=tk.W, padx=5)
        
        # Speed settings
        speed_frame = ttk.LabelFrame(frame, text="Speed Settings", padding=10)
        speed_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(speed_frame, text="Min Speed Multiplier:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.mouse_min_speed = tk.StringVar(value=self.config.get('Mouse', 'mouse_min_speed_multiplier'))
        ttk.Entry(speed_frame, textvariable=self.mouse_min_speed, width=10).grid(row=0, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(speed_frame, text="Max Speed Multiplier:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.mouse_max_speed = tk.StringVar(value=self.config.get('Mouse', 'mouse_max_speed_multiplier'))
        ttk.Entry(speed_frame, textvariable=self.mouse_max_speed, width=10).grid(row=1, column=1, sticky=tk.W, padx=5)
        
        # Mouse options
        options_frame = ttk.LabelFrame(frame, text="Mouse Options", padding=10)
        options_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.mouse_lock_target = tk.BooleanVar(value=self.config.getboolean('Mouse', 'mouse_lock_target'))
        ttk.Checkbutton(options_frame, text="Lock Target", variable=self.mouse_lock_target).grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.mouse_auto_aim = tk.BooleanVar(value=self.config.getboolean('Mouse', 'mouse_auto_aim'))
        ttk.Checkbutton(options_frame, text="Auto Aim", variable=self.mouse_auto_aim).grid(row=1, column=0, sticky=tk.W, pady=2)
        
        self.mouse_ghub = tk.BooleanVar(value=self.config.getboolean('Mouse', 'mouse_ghub'))
        ttk.Checkbutton(options_frame, text="Use GHub Driver", variable=self.mouse_ghub).grid(row=2, column=0, sticky=tk.W, pady=2)
        
        self.mouse_rzr = tk.BooleanVar(value=self.config.getboolean('Mouse', 'mouse_rzr'))
        ttk.Checkbutton(options_frame, text="Use Razer Driver", variable=self.mouse_rzr).grid(row=3, column=0, sticky=tk.W, pady=2)
        
    def create_shooting_tab(self):
        """Create Shooting tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Shooting")
        
        # Shooting settings
        shooting_frame = ttk.LabelFrame(frame, text="Shooting Configuration", padding=10)
        shooting_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.auto_shoot = tk.BooleanVar(value=self.config.getboolean('Shooting', 'auto_shoot'))
        ttk.Checkbutton(shooting_frame, text="Auto Shoot", variable=self.auto_shoot).grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.triggerbot = tk.BooleanVar(value=self.config.getboolean('Shooting', 'triggerbot'))
        ttk.Checkbutton(shooting_frame, text="Trigger Bot", variable=self.triggerbot).grid(row=1, column=0, sticky=tk.W, pady=2)
        
        self.force_click = tk.BooleanVar(value=self.config.getboolean('Shooting', 'force_click'))
        ttk.Checkbutton(shooting_frame, text="Force Click", variable=self.force_click).grid(row=2, column=0, sticky=tk.W, pady=2)
        
        ttk.Label(shooting_frame, text="Scope Multiplier:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.bscope_multiplier = tk.StringVar(value=self.config.get('Shooting', 'bScope_multiplier'))
        ttk.Entry(shooting_frame, textvariable=self.bscope_multiplier, width=10).grid(row=3, column=1, sticky=tk.W, padx=5)
        
    def create_arduino_tab(self):
        """Create Arduino tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Arduino")
        
        # Arduino settings
        arduino_frame = ttk.LabelFrame(frame, text="Arduino Configuration", padding=10)
        arduino_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.arduino_move = tk.BooleanVar(value=self.config.getboolean('Arduino', 'arduino_move'))
        ttk.Checkbutton(arduino_frame, text="Arduino Move", variable=self.arduino_move).grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.arduino_shoot = tk.BooleanVar(value=self.config.getboolean('Arduino', 'arduino_shoot'))
        ttk.Checkbutton(arduino_frame, text="Arduino Shoot", variable=self.arduino_shoot).grid(row=1, column=0, sticky=tk.W, pady=2)
        
        ttk.Label(arduino_frame, text="Arduino Port:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.arduino_port = tk.StringVar(value=self.config.get('Arduino', 'arduino_port'))
        ttk.Entry(arduino_frame, textvariable=self.arduino_port, width=10).grid(row=2, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(arduino_frame, text="Baudrate:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.arduino_baudrate = tk.StringVar(value=self.config.get('Arduino', 'arduino_baudrate'))
        ttk.Entry(arduino_frame, textvariable=self.arduino_baudrate, width=10).grid(row=3, column=1, sticky=tk.W, padx=5)
        
        self.arduino_16_bit = tk.BooleanVar(value=self.config.getboolean('Arduino', 'arduino_16_bit_mouse'))
        ttk.Checkbutton(arduino_frame, text="16-bit Mouse", variable=self.arduino_16_bit).grid(row=4, column=0, sticky=tk.W, pady=2)
        
    def create_ai_tab(self):
        """Create AI tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="AI Settings")
        
        # AI model settings
        ai_frame = ttk.LabelFrame(frame, text="AI Model Configuration", padding=10)
        ai_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(ai_frame, text="AI Model Name:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.ai_model_name = tk.StringVar(value=self.config.get('AI', 'AI_model_name'))
        model_frame = ttk.Frame(ai_frame)
        model_frame.grid(row=0, column=1, sticky=tk.W, padx=5)
        ttk.Entry(model_frame, textvariable=self.ai_model_name, width=20).pack(side=tk.LEFT)
        ttk.Button(model_frame, text="Browse", command=self.browse_model).pack(side=tk.LEFT, padx=5)
        
        ttk.Label(ai_frame, text="Image Size:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.ai_image_size = tk.StringVar(value=self.config.get('AI', 'AI_model_image_size'))
        ttk.Entry(ai_frame, textvariable=self.ai_image_size, width=10).grid(row=1, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(ai_frame, text="Confidence:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.ai_conf = tk.StringVar(value=self.config.get('AI', 'AI_conf'))
        ttk.Entry(ai_frame, textvariable=self.ai_conf, width=10).grid(row=2, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(ai_frame, text="Device:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.ai_device = tk.StringVar(value=self.config.get('AI', 'AI_device'))
        ttk.Entry(ai_frame, textvariable=self.ai_device, width=10).grid(row=3, column=1, sticky=tk.W, padx=5)
        
        self.ai_enable_amd = tk.BooleanVar(value=self.config.getboolean('AI', 'AI_enable_AMD'))
        ttk.Checkbutton(ai_frame, text="Enable AMD", variable=self.ai_enable_amd).grid(row=4, column=0, sticky=tk.W, pady=2)
        
        self.disable_tracker = tk.BooleanVar(value=self.config.getboolean('AI', 'disable_tracker'))
        ttk.Checkbutton(ai_frame, text="Disable Tracker", variable=self.disable_tracker).grid(row=5, column=0, sticky=tk.W, pady=2)
        
    def create_overlay_tab(self):
        """Create Overlay tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Overlay")
        
        # Overlay settings
        overlay_frame = ttk.LabelFrame(frame, text="Overlay Configuration", padding=10)
        overlay_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.show_overlay = tk.BooleanVar(value=self.config.getboolean('overlay', 'show_overlay'))
        ttk.Checkbutton(overlay_frame, text="Show Overlay", variable=self.show_overlay).grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.overlay_show_borders = tk.BooleanVar(value=self.config.getboolean('overlay', 'overlay_show_borders'))
        ttk.Checkbutton(overlay_frame, text="Show Borders", variable=self.overlay_show_borders).grid(row=1, column=0, sticky=tk.W, pady=2)
        
        self.overlay_show_boxes = tk.BooleanVar(value=self.config.getboolean('overlay', 'overlay_show_boxes'))
        ttk.Checkbutton(overlay_frame, text="Show Detection Boxes", variable=self.overlay_show_boxes).grid(row=2, column=0, sticky=tk.W, pady=2)
        
        self.overlay_show_target_line = tk.BooleanVar(value=self.config.getboolean('overlay', 'overlay_show_target_line'))
        ttk.Checkbutton(overlay_frame, text="Show Target Line", variable=self.overlay_show_target_line).grid(row=3, column=0, sticky=tk.W, pady=2)
        
        self.overlay_show_prediction_line = tk.BooleanVar(value=self.config.getboolean('overlay', 'overlay_show_target_prediction_line'))
        ttk.Checkbutton(overlay_frame, text="Show Prediction Line", variable=self.overlay_show_prediction_line).grid(row=4, column=0, sticky=tk.W, pady=2)
        
        self.overlay_show_labels = tk.BooleanVar(value=self.config.getboolean('overlay', 'overlay_show_labels'))
        ttk.Checkbutton(overlay_frame, text="Show Labels", variable=self.overlay_show_labels).grid(row=5, column=0, sticky=tk.W, pady=2)
        
        self.overlay_show_conf = tk.BooleanVar(value=self.config.getboolean('overlay', 'overlay_show_conf'))
        ttk.Checkbutton(overlay_frame, text="Show Confidence", variable=self.overlay_show_conf).grid(row=6, column=0, sticky=tk.W, pady=2)
        
    def create_debug_tab(self):
        """Create Debug Window tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="Debug")
        
        # Debug window settings
        debug_frame = ttk.LabelFrame(frame, text="Debug Window Configuration", padding=10)
        debug_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.show_window = tk.BooleanVar(value=self.config.getboolean('Debug window', 'show_window'))
        ttk.Checkbutton(debug_frame, text="Show Debug Window", variable=self.show_window).grid(row=0, column=0, sticky=tk.W, pady=2)
        
        self.show_detection_speed = tk.BooleanVar(value=self.config.getboolean('Debug window', 'show_detection_speed'))
        ttk.Checkbutton(debug_frame, text="Show Detection Speed", variable=self.show_detection_speed).grid(row=1, column=0, sticky=tk.W, pady=2)
        
        self.show_window_fps = tk.BooleanVar(value=self.config.getboolean('Debug window', 'show_window_fps'))
        ttk.Checkbutton(debug_frame, text="Show Window FPS", variable=self.show_window_fps).grid(row=2, column=0, sticky=tk.W, pady=2)
        
        self.show_boxes = tk.BooleanVar(value=self.config.getboolean('Debug window', 'show_boxes'))
        ttk.Checkbutton(debug_frame, text="Show Boxes", variable=self.show_boxes).grid(row=3, column=0, sticky=tk.W, pady=2)
        
        self.show_labels = tk.BooleanVar(value=self.config.getboolean('Debug window', 'show_labels'))
        ttk.Checkbutton(debug_frame, text="Show Labels", variable=self.show_labels).grid(row=4, column=0, sticky=tk.W, pady=2)
        
        self.show_conf = tk.BooleanVar(value=self.config.getboolean('Debug window', 'show_conf'))
        ttk.Checkbutton(debug_frame, text="Show Confidence", variable=self.show_conf).grid(row=5, column=0, sticky=tk.W, pady=2)
        
        # Position settings
        pos_frame = ttk.LabelFrame(frame, text="Window Position", padding=10)
        pos_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(pos_frame, text="Window X:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.spawn_window_x = tk.StringVar(value=self.config.get('Debug window', 'spawn_window_pos_x'))
        ttk.Entry(pos_frame, textvariable=self.spawn_window_x, width=10).grid(row=0, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(pos_frame, text="Window Y:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.spawn_window_y = tk.StringVar(value=self.config.get('Debug window', 'spawn_window_pos_y'))
        ttk.Entry(pos_frame, textvariable=self.spawn_window_y, width=10).grid(row=1, column=1, sticky=tk.W, padx=5)
        
        ttk.Label(pos_frame, text="Scale %:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.debug_scale = tk.StringVar(value=self.config.get('Debug window', 'debug_window_scale_percent'))
        ttk.Entry(pos_frame, textvariable=self.debug_scale, width=10).grid(row=2, column=1, sticky=tk.W, padx=5)
        
    def create_buttons(self, parent):
        """Create bottom buttons"""
        button_frame = ttk.Frame(parent)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Save Configuration", command=self.save_configuration).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Load Configuration", command=self.load_configuration).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Reset to Defaults", command=self.reset_defaults).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", command=self.root.quit).pack(side=tk.RIGHT, padx=5)
        
    def browse_model(self):
        """Browse for AI model file"""
        filename = filedialog.askopenfilename(
            title="Select AI Model",
            filetypes=[("Model files", "*.pt *.onnx *.engine"), ("All files", "*.*")],
            initialdir="models"
        )
        if filename:
            # Get relative path from models directory
            model_name = os.path.basename(filename)
            self.ai_model_name.set(model_name)
            
    def save_configuration(self):
        """Save all settings to config.ini"""
        try:
            # Update config with current values
            self.update_config_values()
            
            # Save to file
            with open(self.config_path, 'w', encoding='utf-8') as f:
                self.config.write(f)
                
            messagebox.showinfo("Success", "Configuration saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {str(e)}")
            
    def load_configuration(self):
        """Reload configuration from file"""
        try:
            self.load_config()
            self.update_gui_values()
            messagebox.showinfo("Success", "Configuration reloaded successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to reload configuration: {str(e)}")
            
    def reset_defaults(self):
        """Reset to default values"""
        if messagebox.askyesno("Confirm", "Are you sure you want to reset all settings to defaults?"):
            # This would need a default config template
            messagebox.showinfo("Info", "Reset functionality would be implemented with default values")
            
    def update_config_values(self):
        """Update config object with current GUI values"""
        # Detection window
        self.config.set('Detection window', 'detection_window_width', self.detection_width.get())
        self.config.set('Detection window', 'detection_window_height', self.detection_height.get())
        self.config.set('Detection window', 'circle_capture', str(self.circle_capture.get()))
        
        # Capture methods
        self.config.set('Capture Methods', 'capture_fps', self.capture_fps.get())
        self.config.set('Capture Methods', 'Bettercam_capture', str(self.bettercam_capture.get()))
        self.config.set('Capture Methods', 'bettercam_monitor_id', self.bettercam_monitor.get())
        self.config.set('Capture Methods', 'bettercam_gpu_id', self.bettercam_gpu.get())
        self.config.set('Capture Methods', 'Obs_capture', str(self.obs_capture.get()))
        self.config.set('Capture Methods', 'Obs_camera_id', self.obs_camera.get())
        self.config.set('Capture Methods', 'mss_capture', str(self.mss_capture.get()))
        
        # Aim
        self.config.set('Aim', 'body_y_offset', self.body_y_offset.get())
        self.config.set('Aim', 'hideout_targets', str(self.hideout_targets.get()))
        self.config.set('Aim', 'disable_headshot', str(self.disable_headshot.get()))
        self.config.set('Aim', 'disable_prediction', str(self.disable_prediction.get()))
        self.config.set('Aim', 'prediction_interval', self.prediction_interval.get())
        self.config.set('Aim', 'third_person', str(self.third_person.get()))
        
        # Hotkeys
        self.config.set('Hotkeys', 'hotkey_targeting', self.hotkey_targeting.get())
        self.config.set('Hotkeys', 'hotkey_exit', self.hotkey_exit.get())
        self.config.set('Hotkeys', 'hotkey_pause', self.hotkey_pause.get())
        self.config.set('Hotkeys', 'hotkey_reload_config', self.hotkey_reload_config.get())
        
        # Mouse
        self.config.set('Mouse', 'mouse_dpi', self.mouse_dpi.get())
        self.config.set('Mouse', 'mouse_sensitivity', self.mouse_sensitivity.get())
        self.config.set('Mouse', 'mouse_fov_width', self.mouse_fov_width.get())
        self.config.set('Mouse', 'mouse_fov_height', self.mouse_fov_height.get())
        self.config.set('Mouse', 'mouse_min_speed_multiplier', self.mouse_min_speed.get())
        self.config.set('Mouse', 'mouse_max_speed_multiplier', self.mouse_max_speed.get())
        self.config.set('Mouse', 'mouse_lock_target', str(self.mouse_lock_target.get()))
        self.config.set('Mouse', 'mouse_auto_aim', str(self.mouse_auto_aim.get()))
        self.config.set('Mouse', 'mouse_ghub', str(self.mouse_ghub.get()))
        self.config.set('Mouse', 'mouse_rzr', str(self.mouse_rzr.get()))
        
        # Shooting
        self.config.set('Shooting', 'auto_shoot', str(self.auto_shoot.get()))
        self.config.set('Shooting', 'triggerbot', str(self.triggerbot.get()))
        self.config.set('Shooting', 'force_click', str(self.force_click.get()))
        self.config.set('Shooting', 'bScope_multiplier', self.bscope_multiplier.get())
        
        # Arduino
        self.config.set('Arduino', 'arduino_move', str(self.arduino_move.get()))
        self.config.set('Arduino', 'arduino_shoot', str(self.arduino_shoot.get()))
        self.config.set('Arduino', 'arduino_port', self.arduino_port.get())
        self.config.set('Arduino', 'arduino_baudrate', self.arduino_baudrate.get())
        self.config.set('Arduino', 'arduino_16_bit_mouse', str(self.arduino_16_bit.get()))
        
        # AI
        self.config.set('AI', 'AI_model_name', self.ai_model_name.get())
        self.config.set('AI', 'AI_model_image_size', self.ai_image_size.get())
        self.config.set('AI', 'AI_conf', self.ai_conf.get())
        self.config.set('AI', 'AI_device', self.ai_device.get())
        self.config.set('AI', 'AI_enable_AMD', str(self.ai_enable_amd.get()))
        self.config.set('AI', 'disable_tracker', str(self.disable_tracker.get()))
        
        # Overlay
        self.config.set('overlay', 'show_overlay', str(self.show_overlay.get()))
        self.config.set('overlay', 'overlay_show_borders', str(self.overlay_show_borders.get()))
        self.config.set('overlay', 'overlay_show_boxes', str(self.overlay_show_boxes.get()))
        self.config.set('overlay', 'overlay_show_target_line', str(self.overlay_show_target_line.get()))
        self.config.set('overlay', 'overlay_show_target_prediction_line', str(self.overlay_show_prediction_line.get()))
        self.config.set('overlay', 'overlay_show_labels', str(self.overlay_show_labels.get()))
        self.config.set('overlay', 'overlay_show_conf', str(self.overlay_show_conf.get()))
        
        # Debug window
        self.config.set('Debug window', 'show_window', str(self.show_window.get()))
        self.config.set('Debug window', 'show_detection_speed', str(self.show_detection_speed.get()))
        self.config.set('Debug window', 'show_window_fps', str(self.show_window_fps.get()))
        self.config.set('Debug window', 'show_boxes', str(self.show_boxes.get()))
        self.config.set('Debug window', 'show_labels', str(self.show_labels.get()))
        self.config.set('Debug window', 'show_conf', str(self.show_conf.get()))
        self.config.set('Debug window', 'spawn_window_pos_x', self.spawn_window_x.get())
        self.config.set('Debug window', 'spawn_window_pos_y', self.spawn_window_y.get())
        self.config.set('Debug window', 'debug_window_scale_percent', self.debug_scale.get())
        
    def update_gui_values(self):
        """Update GUI with current config values"""
        # This would update all GUI elements with current config values
        # Similar to the constructor but for reloading
        pass
        
    def run(self):
        """Start the GUI"""
        self.root.mainloop()

if __name__ == "__main__":
    app = ConfigGUI()
    app.run() 