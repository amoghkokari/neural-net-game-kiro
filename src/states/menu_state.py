"""
Main menu state
"""

import pygame
from .base_state import BaseState
from ..constants import GameState

class MenuState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.selected_option = 0
        self.menu_options = ["Start Adventure", "Continue", "Quit"]
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
            elif event.key == pygame.K_RETURN:
                if self.selected_option == 0:  # Start Adventure
                    self.game.change_state(GameState.WORLD_MAP)
                elif self.selected_option == 1:  # Continue
                    self.game.change_state(GameState.WORLD_MAP)
                elif self.selected_option == 2:  # Quit
                    pygame.quit()
                    import sys
                    sys.exit()
    
    def render(self, screen):
        # Title
        title = self.font_large.render("Neural Network Adventure", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.game.width // 2, 200))
        screen.blit(title, title_rect)
        
        # Subtitle
        subtitle = self.font_medium.render("Learn AI by Building It", True, (200, 200, 200))
        subtitle_rect = subtitle.get_rect(center=(self.game.width // 2, 260))
        screen.blit(subtitle, subtitle_rect)
        
        # Menu options
        for i, option in enumerate(self.menu_options):
            color = (255, 255, 0) if i == self.selected_option else (255, 255, 255)
            text = self.font_medium.render(option, True, color)
            text_rect = text.get_rect(center=(self.game.width // 2, 400 + i * 60))
            screen.blit(text, text_rect)
        
        # Instructions
        instructions = pygame.font.Font(None, 24).render("Use arrow keys and Enter to navigate", True, (150, 150, 150))
        instructions_rect = instructions.get_rect(center=(self.game.width // 2, self.game.height - 50))
        screen.blit(instructions, instructions_rect)