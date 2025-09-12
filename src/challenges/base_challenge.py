"""
Base class for all coding challenges
"""

import pygame

class BaseChallenge:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 28)
        self.code_font = pygame.font.Font(None, 20)
        self.completed = False
        
    def initialize(self):
        """Initialize challenge-specific data"""
        pass
    
    def handle_event(self, event):
        """Handle events, return 'completed', 'exit', or None"""
        pass
    
    def update(self, dt):
        """Update challenge logic"""
        pass
    
    def render(self, screen):
        """Render challenge interface"""
        pass
    
    def check_solution(self, code):
        """Check if the provided code solves the challenge"""
        return False