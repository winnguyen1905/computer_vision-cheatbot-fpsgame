#!/usr/bin/env python3
"""
UI Automation Example
Automated UI interaction and testing
"""

import sys
import time
from pathlib import Path
from typing import List, Dict, Any

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from src.tracker_system import TrackerSystem
from utils.logger import setup_logger


class UIAutomation:
    """UI automation system for clicking buttons and interacting with interfaces"""
    
    def __init__(self):
        self.logger = setup_logger("UIAutomation", verbose=True)
        self.tracker = TrackerSystem()
        self.automation_steps = []
        self.current_step = 0
        
    def add_step(self, template_path: str, action: str = "click", 
                 wait_time: float = 1.0, max_attempts: int = 10):
        """
        Add an automation step
        
        Args:
            template_path: Path to template image
            action: Action to perform ('click', 'move', 'wait')
            wait_time: Time to wait after action
            max_attempts: Maximum attempts to find the element
        """
        step = {
            'template_path': template_path,
            'action': action,
            'wait_time': wait_time,
            'max_attempts': max_attempts
        }
        self.automation_steps.append(step)
        self.logger.info(f"Added step {len(self.automation_steps)}: {action} on {template_path}")
    
    def execute_automation(self, loop: bool = False):
        """
        Execute the automation sequence
        
        Args:
            loop: Whether to loop the automation sequence
        """
        if not self.automation_steps:
            self.logger.error("No automation steps defined")
            return False
        
        self.logger.info(f"🤖 Starting UI automation with {len(self.automation_steps)} steps")
        
        try:
            while True:
                success = self._execute_sequence()
                
                if not success:
                    self.logger.error("❌ Automation sequence failed")
                    return False
                
                if not loop:
                    self.logger.info("✅ Automation sequence completed successfully")
                    break
                
                self.logger.info("🔄 Looping automation sequence...")
                time.sleep(2)  # Brief pause between loops
                
        except KeyboardInterrupt:
            self.logger.info("🛑 Automation stopped by user")
        
        return True
    
    def _execute_sequence(self) -> bool:
        """Execute a single automation sequence"""
        for step_num, step in enumerate(self.automation_steps, 1):
            self.logger.info(f"📍 Step {step_num}/{len(self.automation_steps)}: "
                           f"{step['action']} on {Path(step['template_path']).name}")
            
            if not self._execute_step(step):
                self.logger.error(f"❌ Step {step_num} failed")
                return False
            
            # Wait between steps
            if step['wait_time'] > 0:
                time.sleep(step['wait_time'])
        
        return True
    
    def _execute_step(self, step: Dict[str, Any]) -> bool:
        """Execute a single automation step"""
        template_path = step['template_path']
        action = step['action']
        max_attempts = step['max_attempts']
        
        # Verify template exists
        if not Path(template_path).exists():
            self.logger.error(f"Template not found: {template_path}")
            return False
        
        # Load template
        self.tracker.load_template(template_path)
        
        # Configure for UI automation
        self.tracker.set_tracking_speed(10)  # Slower for UI stability
        self.tracker.set_confidence_threshold(0.85)  # Higher confidence for UI elements
        
        # Attempt to find and interact with element
        for attempt in range(max_attempts):
            self.logger.info(f"🔍 Attempt {attempt + 1}/{max_attempts} - Looking for element...")
            
            # Test detection
            result = self.tracker.test_detection()
            
            if result.found:
                x, y = result.center
                self.logger.info(f"✅ Element found at ({x}, {y}) - Confidence: {result.confidence:.2f}")
                
                # Perform action
                if action == "click":
                    self.tracker.mouse_controller.click_at(x, y)
                    self.logger.info("🖱️  Clicked element")
                
                elif action == "double_click":
                    self.tracker.mouse_controller.double_click_at(x, y)
                    self.logger.info("🖱️  Double-clicked element")
                
                elif action == "right_click":
                    self.tracker.mouse_controller.right_click_at(x, y)
                    self.logger.info("🖱️  Right-clicked element")
                
                elif action == "move":
                    self.tracker.mouse_controller.smooth_move_to(x, y)
                    self.logger.info("🖱️  Moved to element")
                
                elif action == "wait":
                    self.logger.info("⏳ Waiting...")
                
                return True
            
            else:
                self.logger.warning(f"⚠️  Element not found, waiting 2 seconds...")
                time.sleep(2)
        
        self.logger.error(f"❌ Failed to find element after {max_attempts} attempts")
        return False
    
    def test_all_templates(self):
        """Test detection for all templates in the automation sequence"""
        self.logger.info("🧪 Testing all templates...")
        
        for i, step in enumerate(self.automation_steps, 1):
            template_path = step['template_path']
            
            if not Path(template_path).exists():
                self.logger.error(f"❌ Step {i}: Template not found - {template_path}")
                continue
            
            self.tracker.load_template(template_path)
            result = self.tracker.test_detection(save_result=True)
            
            if result.found:
                self.logger.info(f"✅ Step {i}: Template detected - {Path(template_path).name} "
                               f"(Confidence: {result.confidence:.2f})")
            else:
                self.logger.warning(f"⚠️  Step {i}: Template not detected - {Path(template_path).name}")


def create_sample_automation() -> UIAutomation:
    """Create a sample UI automation sequence"""
    automation = UIAutomation()
    
    # Example automation sequence for a typical application
    automation.add_step("templates/button.png", "click", wait_time=1.0)
    automation.add_step("templates/icon.png", "double_click", wait_time=2.0)
    automation.add_step("templates/close_button.png", "click", wait_time=1.0)
    
    return automation


def main():
    """Main function"""
    automation = UIAutomation()
    
    try:
        print("🤖 UI Automation Example")
        print("=" * 40)
        print("1. Create template images for UI elements you want to interact with")
        print("2. Place them in the templates/ folder")
        print("3. Modify this script to add your automation steps")
        print()
        
        # Check if sample templates exist
        sample_templates = ["templates/button.png", "templates/icon.png"]
        missing_templates = [t for t in sample_templates if not Path(t).exists()]
        
        if missing_templates:
            automation.logger.info("📝 To use this example, create the following templates:")
            for template in missing_templates:
                automation.logger.info(f"  - {template}")
            automation.logger.info("")
            automation.logger.info("How to create templates:")
            automation.logger.info("1. Take a screenshot of the UI element")
            automation.logger.info("2. Crop just the button/icon you want to click")
            automation.logger.info("3. Save as PNG in the templates/ folder")
            return 1
        
        # Create sample automation
        automation = create_sample_automation()
        
        # Test templates first
        automation.test_all_templates()
        
        # Ask user what to do
        print("\nOptions:")
        print("1. Test templates only (already done)")
        print("2. Run automation once")
        print("3. Run automation in loop")
        print("4. Exit")
        
        choice = input("Choose an option (1-4): ").strip()
        
        if choice == "2":
            automation.execute_automation(loop=False)
        elif choice == "3":
            automation.execute_automation(loop=True)
        elif choice in ["1", "4"]:
            automation.logger.info("Exiting...")
        else:
            automation.logger.warning("Invalid choice")
            return 1
    
    except KeyboardInterrupt:
        automation.logger.info("UI automation cancelled by user")
        return 0
    except Exception as e:
        automation.logger.error(f"UI automation error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 