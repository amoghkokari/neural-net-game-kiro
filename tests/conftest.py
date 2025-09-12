"""
Pytest configuration and fixtures
"""

import pytest
import pygame
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

@pytest.fixture(scope="session", autouse=True)
def pygame_init():
    """Initialize pygame for all tests"""
    pygame.init()
    # Use a dummy display for headless testing
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    yield
    pygame.quit()

@pytest.fixture
def mock_screen():
    """Create a mock pygame screen for testing"""
    return pygame.Surface((1024, 768))

@pytest.fixture
def sample_game_data():
    """Sample game data for testing"""
    return {
        'completed_levels': {0, 1},
        'current_level': 2,
        'neural_network_knowledge': {'neurons': 85, 'bias': 90},
        'code_implementations': {'perceptron': 'def perceptron(): pass'},
        'boss_defeats': {'Weight Master', 'Bias Baron'},
        'understanding_scores': {'Neuron Academy': 95, 'Bias Battlefield': 88}
    }