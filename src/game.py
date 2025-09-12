"""
Main game class that manages game states and flow
"""

import pygame
from .constants import GameState
from .states.menu_state import MenuState
from .states.world_map_state import WorldMapState
from .states.level_state import LevelState
from .states.coding_challenge_state import CodingChallengeState

class Game:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        self.current_state = GameState.MENU
        
        # Player progress tracking
        self.player_progress = {
            'completed_levels': set(),
            'current_level': 0,
            'neural_network_knowledge': {},
            'code_implementations': {},
            'boss_defeats': set(),
            'understanding_scores': {}
        }
        
        # Initialize character
        from .character.alex_character import AlexCharacter
        self.character = AlexCharacter()
        
        # Initialize game states
        self.states = {
            GameState.MENU: MenuState(self),
            GameState.WORLD_MAP: WorldMapState(self),
            GameState.LEVEL: LevelState(self),
            GameState.CODING_CHALLENGE: CodingChallengeState(self)
        }
        

    
    def change_state(self, new_state):
        """Change the current game state"""
        if new_state in self.states:
            self.current_state = new_state
            self.states[new_state].enter()
    
    def handle_event(self, event):
        """Handle pygame events"""
        self.states[self.current_state].handle_event(event)
    
    def update(self, dt):
        """Update current state"""
        self.states[self.current_state].update(dt)
        # Update character
        self.character.update(dt)
    
    def render(self):
        """Render current state"""
        self.screen.fill((0, 0, 0))  # Clear screen
        self.states[self.current_state].render(self.screen)