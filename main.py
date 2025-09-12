#!/usr/bin/env python3
"""
Neural Network Adventure RPG
Main game entry point
"""

import pygame
import sys
from src.game import Game
from src.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS

def main():
    """Initialize and run the game"""
    pygame.init()
    
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Neural Network Adventure")
    clock = pygame.time.Clock()
    
    # Initialize game
    game = Game(screen, SCREEN_WIDTH, SCREEN_HEIGHT)
    
    # Game loop
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # Delta time in seconds
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                game.handle_event(event)
        
        game.update(dt)
        game.render()
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()