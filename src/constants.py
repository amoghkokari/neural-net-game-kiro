"""
Game constants and enums
"""

from enum import Enum

class GameState(Enum):
    MENU = "menu"
    WORLD_MAP = "world_map"
    LEVEL = "level"
    CODING_CHALLENGE = "coding_challenge"

# Game settings
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)

# Neural network visualization colors
NEURON_INPUT_COLOR = (100, 150, 255)
NEURON_HIDDEN_COLOR = (150, 255, 150)
NEURON_OUTPUT_COLOR = (255, 150, 100)
POSITIVE_WEIGHT_COLOR = (0, 255, 0)
NEGATIVE_WEIGHT_COLOR = (255, 0, 0)