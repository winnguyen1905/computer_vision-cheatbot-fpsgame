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
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        
        # Configure modern styling
        self.setup_styles()
        
        # Configuration file path
        self.config_path = "config.ini"
        self.config = configparser.ConfigParser()
        
        # Load current configuration
        self.load_config()
        
        # Create GUI elements
        self.create_widgets()
        
        # Center window
        self.center_window()
        
    def setup_styles(self):
        """Setup modern UI styling"""
        style = ttk.Style()
        
        # Configure notebook style
        style.configure('Custom.TNotebook', background='#f0f0f0')
        style.configure('Custom.TNotebook.Tab', padding=[20, 8])
        
        # Configure frame styles
        style.configure('Title.TLabelframe', foreground='#2c3e50', font=('Arial', 10, 'bold'))
        style.configure('Section.TLabelframe', foreground='#34495e', font=('Arial', 9, 'bold'))
        style.configure('Subsection.TLabelframe', foreground='#7f8c8d', font=('Arial', 8))
        
        # Configure button styles
        style.configure('Action.TButton', font=('Arial', 9, 'bold'))
        style.configure('Primary.TButton', foreground='white')
        
        # Set background
        self.root.configure(bg='#f8f9fa')
        
    def create_header(self):
        """Create application header"""
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        # Title
        title_label = tk.Label(header_frame, text="Object Detective", 
                              font=('Arial', 18, 'bold'), 
                              fg='white', bg='#2c3e50')
        title_label.pack(side=tk.LEFT, padx=20, pady=15)
        
        # Subtitle
        subtitle_label = tk.Label(header_frame, text="Configuration Manager", 
                                 font=('Arial', 11), 
                                 fg='#bdc3c7', bg='#2c3e50')
        subtitle_label.pack(side=tk.LEFT, padx=(0, 20), pady=15)
        
        # Status indicator
        self.status_frame = tk.Frame(header_frame, bg='#2c3e50')
        self.status_frame.pack(side=tk.RIGHT, padx=20, pady=15)
        
        self.status_label = tk.Label(self.status_frame, text="● Configuration Loaded", 
                                    font=('Arial', 9), 
                                    fg='#27ae60', bg='#2c3e50')
        self.status_label.pack()
        
    def create_section_frame(self, parent, title, style='Title.TLabelframe'):
        """Create a styled section frame"""
        frame = ttk.LabelFrame(parent, text=f"  {title}  ", style=style, padding=15)
        frame.pack(fill=tk.X, padx=8, pady=8)
        return frame
        
    def create_subsection_frame(self, parent, title):
        """Create a styled subsection frame"""
        frame = ttk.LabelFrame(parent, text=f"  {title}  ", style='Subsection.TLabelframe', padding=10)
        frame.pack(fill=tk.X, padx=5, pady=5)
        return frame
        
    def add_separator(self, parent):
        """Add a visual separator"""
        separator = ttk.Separator(parent, orient='horizontal')
        separator.pack(fill=tk.X, padx=10, pady=8)
        
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
        # Create header
        self.create_header()
        
        # Create main frame with improved styling
        main_frame = ttk.Frame(self.root, style='Card.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Create notebook for tabs with custom style
        self.notebook = ttk.Notebook(main_frame, style='Custom.TNotebook')
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
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
        self.notebook.add(frame, text="🎯 Detection Window")
        
        # Create scrollable content
        canvas = tk.Canvas(frame, bg='#f8f9fa')
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Detection window settings
        settings_frame = self.create_section_frame(scrollable_frame, "🖼️ Detection Area Configuration")
        
        # Dimensions subsection
        dim_frame = self.create_subsection_frame(settings_frame, "Dimensions")
        
        # Width
        width_row = ttk.Frame(dim_frame)
        width_row.pack(fill=tk.X, pady=3)
        ttk.Label(width_row, text="Width:", font=('Arial', 9, 'bold')).pack(side=tk.LEFT)
        self.detection_width = tk.StringVar(value=self.config.get('Detection window', 'detection_window_width'))
        width_entry = create_validated_entry(width_row, "positive_int", textvariable=self.detection_width, width=8)
        width_entry.pack(side=tk.LEFT, padx=(10, 5))
        create_tooltip(width_entry, TOOLTIPS['detection_width'])
        ttk.Label(width_row, text="pixels", foreground='#7f8c8d').pack(side=tk.LEFT)
        
        # Height
        height_row = ttk.Frame(dim_frame)
        height_row.pack(fill=tk.X, pady=3)
        ttk.Label(height_row, text="Height:", font=('Arial', 9, 'bold')).pack(side=tk.LEFT)
        self.detection_height = tk.StringVar(value=self.config.get('Detection window', 'detection_window_height'))
        height_entry = create_validated_entry(height_row, "positive_int", textvariable=self.detection_height, width=8)
        height_entry.pack(side=tk.LEFT, padx=(10, 5))
        create_tooltip(height_entry, TOOLTIPS['detection_height'])
        ttk.Label(height_row, text="pixels", foreground='#7f8c8d').pack(side=tk.LEFT)
        
        self.add_separator(settings_frame)
        
        # Shape subsection
        shape_frame = self.create_subsection_frame(settings_frame, "Detection Shape")
        self.circle_capture = tk.BooleanVar(value=self.config.getboolean('Detection window', 'circle_capture'))
        circle_cb = ttk.Checkbutton(shape_frame, text="🔵 Enable Circle Capture Mode", 
                                   variable=self.circle_capture, 
                                   style='Accent.TCheckbutton')
        circle_cb.pack(anchor=tk.W, pady=5)
        create_tooltip(circle_cb, TOOLTIPS['circle_capture'])
        
        # Performance tips
        tips_frame = self.create_section_frame(scrollable_frame, "💡 Performance Tips", 'Section.TLabelframe')
        
        tips_text = """• Smaller detection windows improve performance significantly
• Circle capture reduces processing area for better FPS
• Recommended sizes: 300x300 (High Performance) | 400x400 (Balanced) | 500x500 (High Accuracy)
• Monitor your FPS in the debug window when adjusting these settings"""
        
        tips_label = tk.Label(tips_frame, text=tips_text, justify=tk.LEFT, 
                             font=('Arial', 9), fg='#34495e', bg='#f8f9fa',
                             wraplength=600)
        tips_label.pack(anchor=tk.W, padx=10, pady=5)
        
    def create_capture_tab(self):
        """Create Capture Methods tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📹 Capture Methods")
        
        # Create scrollable content
        canvas = tk.Canvas(frame, bg='#f8f9fa')
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Global settings
        global_frame = self.create_section_frame(scrollable_frame, "⚙️ Global Capture Settings")
        
        fps_row = ttk.Frame(global_frame)
        fps_row.pack(fill=tk.X, pady=5)
        ttk.Label(fps_row, text="Capture FPS:", font=('Arial', 9, 'bold')).pack(side=tk.LEFT)
        self.capture_fps = tk.StringVar(value=self.config.get('Capture Methods', 'capture_fps'))
        fps_entry = create_validated_entry(fps_row, "positive_int", textvariable=self.capture_fps, width=8)
        fps_entry.pack(side=tk.LEFT, padx=(10, 5))
        create_tooltip(fps_entry, TOOLTIPS['capture_fps'])
        ttk.Label(fps_row, text="fps", foreground='#7f8c8d').pack(side=tk.LEFT)
        
        # Warning about FPS
        warning_frame = tk.Frame(global_frame, bg='#fff3cd', relief=tk.RAISED, bd=1)
        warning_frame.pack(fill=tk.X, pady=10, padx=5)
        warning_label = tk.Label(warning_frame, text="⚠️ High FPS values (>120) may cause performance issues and aiming instability",
                                font=('Arial', 8), fg='#856404', bg='#fff3cd')
        warning_label.pack(pady=8)
        
        # Capture methods
        methods_frame = self.create_section_frame(scrollable_frame, "🎥 Capture Methods (Select Only One)")
        
        # Bettercam
        bettercam_frame = self.create_subsection_frame(methods_frame, "🚀 Bettercam (Recommended)")
        self.bettercam_capture = tk.BooleanVar(value=self.config.getboolean('Capture Methods', 'Bettercam_capture'))
        bettercam_cb = ttk.Checkbutton(bettercam_frame, text="Enable Bettercam Capture", variable=self.bettercam_capture)
        bettercam_cb.pack(anchor=tk.W, pady=5)
        
        # Bettercam settings
        bettercam_settings = ttk.Frame(bettercam_frame)
        bettercam_settings.pack(fill=tk.X, padx=20, pady=5)
        
        monitor_row = ttk.Frame(bettercam_settings)
        monitor_row.pack(fill=tk.X, pady=2)
        ttk.Label(monitor_row, text="Monitor ID:").pack(side=tk.LEFT)
        self.bettercam_monitor = tk.StringVar(value=self.config.get('Capture Methods', 'bettercam_monitor_id'))
        monitor_entry = create_validated_entry(monitor_row, "positive_int", textvariable=self.bettercam_monitor, width=6)
        monitor_entry.pack(side=tk.LEFT, padx=(10, 5))
        ttk.Label(monitor_row, text="(0 = primary monitor)", foreground='#7f8c8d').pack(side=tk.LEFT)
        
        gpu_row = ttk.Frame(bettercam_settings)
        gpu_row.pack(fill=tk.X, pady=2)
        ttk.Label(gpu_row, text="GPU ID:").pack(side=tk.LEFT)
        self.bettercam_gpu = tk.StringVar(value=self.config.get('Capture Methods', 'bettercam_gpu_id'))
        gpu_entry = create_validated_entry(gpu_row, "positive_int", textvariable=self.bettercam_gpu, width=6)
        gpu_entry.pack(side=tk.LEFT, padx=(10, 5))
        ttk.Label(gpu_row, text="(0 = first GPU)", foreground='#7f8c8d').pack(side=tk.LEFT)
        
        self.add_separator(methods_frame)
        
        # OBS
        obs_frame = self.create_subsection_frame(methods_frame, "📺 OBS Virtual Camera")
        self.obs_capture = tk.BooleanVar(value=self.config.getboolean('Capture Methods', 'Obs_capture'))
        obs_cb = ttk.Checkbutton(obs_frame, text="Enable OBS Capture", variable=self.obs_capture)
        obs_cb.pack(anchor=tk.W, pady=5)
        
        obs_settings = ttk.Frame(obs_frame)
        obs_settings.pack(fill=tk.X, padx=20, pady=5)
        
        camera_row = ttk.Frame(obs_settings)
        camera_row.pack(fill=tk.X, pady=2)
        ttk.Label(camera_row, text="Camera ID:").pack(side=tk.LEFT)
        self.obs_camera = tk.StringVar(value=self.config.get('Capture Methods', 'Obs_camera_id'))
        camera_entry = ttk.Entry(camera_row, textvariable=self.obs_camera, width=8)
        camera_entry.pack(side=tk.LEFT, padx=(10, 5))
        ttk.Label(camera_row, text="('auto' for detection)", foreground='#7f8c8d').pack(side=tk.LEFT)
        
        self.add_separator(methods_frame)
        
        # MSS
        mss_frame = self.create_subsection_frame(methods_frame, "🖥️ MSS Screen Capture")
        self.mss_capture = tk.BooleanVar(value=self.config.getboolean('Capture Methods', 'mss_capture'))
        mss_cb = ttk.Checkbutton(mss_frame, text="Enable MSS Capture (Fallback method)", variable=self.mss_capture)
        mss_cb.pack(anchor=tk.W, pady=5)
        
        # Method comparison
        comparison_frame = self.create_section_frame(scrollable_frame, "📊 Performance Comparison", 'Section.TLabelframe')
        
        comparison_text = """Bettercam: 🟢 Fastest, GPU accelerated, best for gaming
OBS Virtual Camera: 🟡 Good performance, requires OBS setup
MSS: 🔴 Slowest, compatible with all systems, CPU intensive"""
        
        comparison_label = tk.Label(comparison_frame, text=comparison_text, justify=tk.LEFT,
                                   font=('Arial', 9), fg='#34495e', bg='#f8f9fa')
        comparison_label.pack(anchor=tk.W, padx=10, pady=5)
        
    def create_aim_tab(self):
        """Create Aim tab"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🎯 Aim Settings")
        
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
        self.notebook.add(frame, text="⌨️ Hotkeys")
        
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
        self.notebook.add(frame, text="🖱️ Mouse Settings")
        
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
        self.notebook.add(frame, text="🔫 Shooting")
        
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
        self.notebook.add(frame, text="🔌 Arduino")
        
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
        self.notebook.add(frame, text="🧠 AI Settings")
        
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
        self.notebook.add(frame, text="👁️ Overlay")
        
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
        self.notebook.add(frame, text="🛠️ Debug")
        
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
        """Create bottom buttons with improved styling"""
        # Create bottom bar
        bottom_bar = tk.Frame(self.root, bg='#ecf0f1', height=60)
        bottom_bar.pack(fill=tk.X, side=tk.BOTTOM)
        bottom_bar.pack_propagate(False)
        
        button_frame = tk.Frame(bottom_bar, bg='#ecf0f1')
        button_frame.pack(expand=True, pady=15)
        
        # Primary action buttons
        primary_frame = tk.Frame(button_frame, bg='#ecf0f1')
        primary_frame.pack(side=tk.LEFT, padx=20)
        
        save_btn = tk.Button(primary_frame, text="💾 Save Configuration", 
                            command=self.save_configuration,
                            bg='#27ae60', fg='white', font=('Arial', 9, 'bold'),
                            relief=tk.FLAT, padx=20, pady=8,
                            cursor='hand2')
        save_btn.pack(side=tk.LEFT, padx=5)
        
        load_btn = tk.Button(primary_frame, text="🔄 Reload Configuration", 
                            command=self.load_configuration,
                            bg='#3498db', fg='white', font=('Arial', 9, 'bold'),
                            relief=tk.FLAT, padx=20, pady=8,
                            cursor='hand2')
        load_btn.pack(side=tk.LEFT, padx=5)
        
        # Secondary actions
        secondary_frame = tk.Frame(button_frame, bg='#ecf0f1')
        secondary_frame.pack(side=tk.LEFT, padx=20)
        
        reset_btn = tk.Button(secondary_frame, text="⚠️ Reset to Defaults", 
                             command=self.reset_defaults,
                             bg='#e74c3c', fg='white', font=('Arial', 9, 'bold'),
                             relief=tk.FLAT, padx=15, pady=8,
                             cursor='hand2')
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        # Exit button on the right
        exit_frame = tk.Frame(button_frame, bg='#ecf0f1')
        exit_frame.pack(side=tk.RIGHT, padx=20)
        
        exit_btn = tk.Button(exit_frame, text="❌ Exit", 
                            command=self.root.quit,
                            bg='#95a5a6', fg='white', font=('Arial', 9, 'bold'),
                            relief=tk.FLAT, padx=20, pady=8,
                            cursor='hand2')
        exit_btn.pack(side=tk.RIGHT)
        
        # Add hover effects
        self.add_button_hover_effects(save_btn, '#229954', '#27ae60')
        self.add_button_hover_effects(load_btn, '#2980b9', '#3498db')
        self.add_button_hover_effects(reset_btn, '#c0392b', '#e74c3c')
        self.add_button_hover_effects(exit_btn, '#7f8c8d', '#95a5a6')
        
    def add_button_hover_effects(self, button, hover_color, normal_color):
        """Add hover effects to buttons"""
        def on_enter(e):
            button.config(bg=hover_color)
        def on_leave(e):
            button.config(bg=normal_color)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
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
        """Save all settings to config.ini with validation"""
        try:
            # Validate settings before saving
            errors = self.validate_all_settings()
            if errors:
                error_message = "Please fix the following errors:\n\n" + "\n".join(errors)
                messagebox.showerror("Validation Error", error_message)
                return
            
            # Update config with current values
            self.update_config_values()
            
            # Save to file
            with open(self.config_path, 'w', encoding='utf-8') as f:
                self.config.write(f)
                
            # Update status
            self.status_label.config(text="● Configuration Saved", fg='#27ae60')
            self.root.after(3000, lambda: self.status_label.config(text="● Configuration Loaded", fg='#27ae60'))
            
            messagebox.showinfo("Success", "Configuration saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {str(e)}")
            
    def validate_all_settings(self):
        """Validate all configuration settings"""
        errors = []
        
        # Validate detection window
        errors.extend(ConfigValidator.validate_detection_window(
            self.detection_width.get(), self.detection_height.get()))
        
        # Validate capture FPS
        errors.extend(ConfigValidator.validate_capture_fps(self.capture_fps.get()))
        
        # Validate mouse settings
        errors.extend(ConfigValidator.validate_mouse_settings(
            self.mouse_dpi.get(), self.mouse_sensitivity.get(),
            self.mouse_fov_width.get(), self.mouse_fov_height.get()))
        
        # Validate AI settings
        errors.extend(ConfigValidator.validate_ai_settings(
            self.ai_conf.get(), self.ai_image_size.get()))
        
        # Validate capture method selection (only one should be true)
        capture_methods = [
            self.bettercam_capture.get(),
            self.obs_capture.get(),
            self.mss_capture.get()
        ]
        
        if sum(capture_methods) != 1:
            errors.append("Please select exactly one capture method")
            
        # Validate mouse method selection (only one should be true)
        mouse_methods = [
            self.mouse_ghub.get(),
            self.mouse_rzr.get()
        ]
        
        if sum(mouse_methods) > 1:
            errors.append("Please select only one mouse driver method")
        
        return errors
            
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