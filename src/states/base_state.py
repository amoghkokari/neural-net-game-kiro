"""
Base state class for all game states
"""

class BaseState:
    def __init__(self, game):
        self.game = game
    
    def enter(self):
        """Called when entering this state"""
        pass
    
    def exit(self):
        """Called when leaving this state"""
        pass
    
    def handle_event(self, event):
        """Handle pygame events"""
        pass
    
    def update(self, dt):
        """Update state logic"""
        pass
    
    def render(self, screen):
        """Render state graphics"""
        pass