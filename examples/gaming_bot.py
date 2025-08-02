#!/usr/bin/env python3
"""
Gaming Bot Example
Automated targeting and clicking for games
"""

import sys
import time
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from src.tracker_system import TrackerSystem
from utils.logger import setup_logger


class GamingBot:
    """Gaming automation bot with targeting and auto-click"""
    
    def __init__(self):
        self.logger = setup_logger("GamingBot", verbose=True)
        self.tracker = TrackerSystem()
        self.targets_hit = 0
        self.start_time = None
        
    def setup_targeting(self, enemy_template_path: str):
        """Setup enemy targeting"""
        if not Path(enemy_template_path).exists():
            raise FileNotFoundError(f"Enemy template not found: {enemy_template_path}")
        
        # Load enemy template
        self.tracker.load_template(enemy_template_path)
        
        # Configure for gaming (fast response)
        self.tracker.set_tracking_speed(60)  # 60 FPS for responsiveness
        self.tracker.set_confidence_threshold(0.75)  # Slightly lower for faster detection
        
        # Enable auto-click when enemy is found
        self.tracker.enable_auto_click(True)
        
        # Update mouse settings for gaming
        self.tracker.update_mouse_settings(
            movement_speed=0.8,  # Fast mouse movement
            smooth_movement=True,  # Smooth for better aim
            click_delay=0.05  # Quick click response
        )
        
        self.logger.info("Gaming bot configured for targeting")
    
    def setup_callbacks(self):
        """Setup event callbacks for targeting"""
        def on_enemy_found(detection_result):
            self.targets_hit += 1
            x, y = detection_result.center
            confidence = detection_result.confidence
            
            self.logger.info(f"🎯 Target acquired at ({x}, {y}) - "
                           f"Confidence: {confidence:.2f} - "
                           f"Targets hit: {self.targets_hit}")
        
        def on_enemy_lost():
            self.logger.info("👁️  Scanning for targets...")
        
        self.tracker.set_callbacks(on_found=on_enemy_found, on_lost=on_enemy_lost)
    
    def start_bot(self):
        """Start the gaming bot"""
        self.start_time = time.time()
        self.targets_hit = 0
        
        self.logger.info("🚀 Gaming bot starting...")
        self.logger.info("🎮 Switch to your game window")
        self.logger.info("🎯 Bot will automatically target and click enemies")
        self.logger.info("⏹️  Press Ctrl+C to stop")
        
        # Give user time to switch to game
        for i in range(5, 0, -1):
            self.logger.info(f"Starting in {i}...")
            time.sleep(1)
        
        self.tracker.start_tracking()
        
        try:
            while self.tracker.is_tracking:
                time.sleep(1)
                
                # Print periodic updates
                elapsed = time.time() - self.start_time
                if int(elapsed) % 30 == 0 and elapsed > 1:  # Every 30 seconds
                    self._print_stats()
        
        except KeyboardInterrupt:
            self.stop_bot()
    
    def stop_bot(self):
        """Stop the gaming bot"""
        self.logger.info("🛑 Stopping gaming bot...")
        self.tracker.stop_tracking()
        self._print_final_stats()
    
    def _print_stats(self):
        """Print current statistics"""
        elapsed = time.time() - self.start_time
        rate = self.targets_hit / elapsed * 60 if elapsed > 0 else 0
        
        self.logger.info(f"📊 Stats - Targets: {self.targets_hit}, "
                        f"Rate: {rate:.1f}/min, "
                        f"Runtime: {elapsed:.0f}s")
    
    def _print_final_stats(self):
        """Print final statistics"""
        if self.start_time:
            elapsed = time.time() - self.start_time
            rate = self.targets_hit / elapsed * 60 if elapsed > 0 else 0
            
            self.logger.info("🏁 Final Gaming Bot Statistics:")
            self.logger.info(f"  Targets hit: {self.targets_hit}")
            self.logger.info(f"  Total runtime: {elapsed:.1f} seconds")
            self.logger.info(f"  Hit rate: {rate:.1f} targets/minute")
            
            # Get tracker stats
            tracker_stats = self.tracker.get_tracking_stats()
            self.logger.info(f"  Detection rate: {tracker_stats.get('detection_rate', 0):.2%}")
            self.logger.info(f"  Average FPS: {tracker_stats.get('avg_fps', 0):.1f}")


def main():
    """Main function"""
    bot = GamingBot()
    
    try:
        # You'll need to create this template by taking a screenshot of an enemy
        enemy_template = "templates/enemy.png"
        
        if not Path(enemy_template).exists():
            bot.logger.error(f"Enemy template not found: {enemy_template}")
            bot.logger.info("To create an enemy template:")
            bot.logger.info("1. Take a screenshot when an enemy is visible")
            bot.logger.info("2. Crop just the enemy image")
            bot.logger.info("3. Save as 'templates/enemy.png'")
            bot.logger.info("4. Make sure the enemy is clearly visible and distinct")
            return 1
        
        # Setup the bot
        bot.setup_targeting(enemy_template)
        bot.setup_callbacks()
        
        # Test detection first
        bot.logger.info("🔍 Testing enemy detection...")
        test_result = bot.tracker.test_detection(save_result=True)
        
        if test_result.found:
            bot.logger.info(f"✅ Enemy detected! Confidence: {test_result.confidence:.2f}")
            bot.logger.info("🎯 Bot ready to start")
        else:
            bot.logger.warning("⚠️  No enemy detected in current screen")
            bot.logger.info("Make sure an enemy is visible and try again")
        
        # Ask user if they want to continue
        input("Press Enter to start the gaming bot (or Ctrl+C to cancel)...")
        
        # Start the bot
        bot.start_bot()
        
    except KeyboardInterrupt:
        bot.logger.info("Gaming bot cancelled by user")
        return 0
    except Exception as e:
        bot.logger.error(f"Gaming bot error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 