# Object Detective - GUI Configuration Manager

This GUI application provides an easy-to-use interface for configuring all Object Detective settings without manually editing the `config.ini` file.

## Features

- **User-friendly Interface**: Organized tabs for different setting categories
- **Input Validation**: Real-time validation prevents invalid configurations
- **Tooltips**: Hover over fields to get helpful explanations
- **Configuration Backup**: Save and load different configurations
- **Error Prevention**: Validates settings before saving

## How to Use

### Starting the GUI

There are several ways to launch the configuration manager:

1. **Using the batch file**: Double-click `run_gui.bat`
2. **From command line**: `python gui_config.py`
3. **From main application**: `python run.py --gui`

### Configuration Tabs

#### 1. Detection Window
- **Detection Window Width/Height**: Set the size of the detection area
- **Circle Capture**: Enable circular detection mask for better focus
- *Tip: Smaller detection windows improve performance*

#### 2. Capture Methods
- **Capture FPS**: Frame rate for screen capture
- **Capture Methods**: Choose between Bettercam, OBS, or MSS
- *Warning: Only select one capture method at a time*

#### 3. Aim Settings
- **Body Y Offset**: Vertical aim adjustment for body shots
- **Headshot Options**: Enable/disable headshot targeting
- **Prediction**: Movement prediction settings
- **Third Person**: Enable for third-person games

#### 4. Hotkeys
- **Targeting Hotkey**: Key to activate aiming (default: RightMouseButton)
- **Exit Hotkey**: Key to exit the application (default: F2)
- **Pause Hotkey**: Key to pause/unpause (default: F3)
- **Reload Config**: Key to reload configuration (default: F4)

#### 5. Mouse Settings
- **Mouse DPI**: Your actual mouse DPI setting
- **Sensitivity**: In-game sensitivity multiplier
- **FOV Settings**: Field of view dimensions for targeting
- **Speed Multipliers**: Min/max movement speed settings
- **Driver Options**: Choose mouse input method

#### 6. Shooting
- **Auto Shoot**: Automatically fire when target is in crosshair
- **Trigger Bot**: Enhanced auto-shooting with trigger detection
- **Force Click**: Force mouse click behavior
- **Scope Multiplier**: Sensitivity adjustment when scoped

#### 7. Arduino
- **Arduino Move**: Use Arduino for mouse movement
- **Arduino Shoot**: Use Arduino for shooting
- **Port Settings**: Configure Arduino connection
- *Note: Arduino provides better anti-cheat bypass*

#### 8. AI Settings
- **Model Name**: AI model file to use (browse for .pt, .onnx, .engine files)
- **Image Size**: Detection resolution (320, 640, or 1280)
- **Confidence**: Detection confidence threshold (0.1-1.0)
- **Device**: GPU device to use (0 for first GPU, cpu for CPU)

#### 9. Overlay
- **Show Overlay**: Display detection overlay on screen
- **Visual Elements**: Choose what to display (boxes, lines, labels, etc.)
- *Note: Overlays may impact performance*

#### 10. Debug
- **Debug Window**: Show detection information window
- **Window Position**: Set debug window location
- **Display Options**: Choose what debug info to show

## Important Settings

### Performance Settings
- **Detection Window Size**: Smaller = better performance
- **Capture FPS**: Lower = better performance
- **AI Image Size**: Smaller = better performance
- **Show Overlay/Debug**: Disabled = better performance

### Anti-Cheat Bypass
- **Arduino Options**: Recommended for better anti-cheat evasion
- **Mouse Drivers**: GHub/Razer drivers may be detected
- **Standard Libraries**: Win32 API may trigger detection

### Recommended Configurations

#### High Performance
- Detection Window: 300x300
- Capture FPS: 60
- AI Image Size: 640
- Overlays: Disabled

#### High Accuracy
- Detection Window: 400x400
- Capture FPS: 120
- AI Image Size: 1280
- AI Confidence: 0.3

#### Stealth Mode
- Arduino Move: Enabled
- Arduino Shoot: Enabled
- Mouse Drivers: Disabled
- Overlays: Disabled

## Validation and Error Checking

The GUI includes comprehensive validation:

- **Range Checking**: Values must be within acceptable ranges
- **Type Validation**: Ensures correct data types (integers, floats)
- **Logic Validation**: Prevents conflicting settings
- **Hardware Checks**: Validates device/port settings

## Configuration Management

### Saving Settings
1. Make your changes in the GUI
2. Click "Save Configuration"
3. Settings are validated before saving
4. Any errors will be displayed with instructions

### Loading Settings
- Click "Load Configuration" to reload from `config.ini`
- Useful if you manually edited the file or want to discard changes

### Backup Configurations
- The original `config.ini` is your backup
- Consider copying `config.ini` to `config_backup.ini` before major changes

## Troubleshooting

### Common Issues

**GUI won't start**
- Ensure Python has tkinter installed
- Check that `config.ini` exists
- Run from command line to see error messages

**Settings not saving**
- Check file permissions for `config.ini`
- Ensure no other applications are using the file
- Fix any validation errors shown

**Invalid settings**
- Use tooltips for guidance on acceptable values
- Check that only one capture method is selected
- Ensure hotkeys use valid key names

### Validation Errors

Common validation errors and fixes:

- **"Width should be between 100 and 1920"**: Adjust detection window size
- **"Only one capture method allowed"**: Uncheck other capture options
- **"DPI should be between 100 and 10000"**: Check your actual mouse DPI
- **"Confidence should be between 0.1 and 1.0"**: Use decimal values

## Advanced Usage

### Command Line Integration
```bash
# Start main application with GUI option
python run.py --gui

# Start just the configuration GUI
python gui_config.py
```

### Hotkey Reference
Available keys for hotkey configuration:
- **Mouse**: LeftMouseButton, RightMouseButton, MiddleMouseButton, X1MouseButton, X2MouseButton
- **Function**: F1-F12
- **Letters**: A-Z
- **Numbers**: Key0-Key9
- **Special**: Space, Enter, Escape, Tab, Shift, Ctrl, Alt

### Model Files
Supported AI model formats:
- **.pt**: PyTorch models (slower but compatible)
- **.onnx**: ONNX models (faster, may need conversion)
- **.engine**: TensorRT engines (fastest, best performance)

## Getting Help

If you encounter issues:
1. Check this README for common solutions
2. Verify your settings against recommended configurations
3. Enable debug window to see detection information
4. Check console output for error messages

## Memory Based on User Preferences

Based on your memory [[memory:5044934]], the project only uses Camera Tracking Mode with circle draw functionality modifiable via the GUI, and no longer uses mouse pointer movement.

The GUI has been configured accordingly:
- Circle capture is enabled in the Detection Window tab
- Mouse movement settings are present but can be disabled if not needed
- The interface focuses on camera-based tracking configuration 