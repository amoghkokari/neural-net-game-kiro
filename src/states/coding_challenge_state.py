"""
Coding challenge state where players implement neural network concepts
"""

import pygame
import sys
from .base_state import BaseState
from ..constants import GameState
from ..challenges.perceptron_challenge import PerceptronChallenge
from ..challenges.neuron_challenge import NeuronChallenge
from ..challenges.bias_challenge import BiasChallenge
from ..challenges.activation_challenge import ActivationChallenge
from ..challenges.chain_rule_challenge import ChainRuleChallenge
from ..challenges.perceptron_simple import PerceptronSimple
from ..challenges.forward_pass_challenge import ForwardPassChallenge

class CodingChallengeState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font(None, 32)
        self.code_font = pygame.font.Font(None, 24)
        self.current_challenge = None
        
        # Available challenges
        self.challenges = {
            "perceptron_classifier": PerceptronChallenge,
            "neuron_basics": NeuronChallenge,
            "bias_battle": BiasChallenge,
            "activation_functions": ActivationChallenge,
            "chain_rule_mastery": ChainRuleChallenge,
            "perceptron_complete": PerceptronSimple,
            "forward_pass_flow": ForwardPassChallenge
        }
    
    def enter(self):
        """Initialize the current challenge"""
        challenge_name = getattr(self.game, 'current_challenge', None)
        if challenge_name and challenge_name in self.challenges:
            self.current_challenge = self.challenges[challenge_name](self.game)
            self.current_challenge.initialize()
    
    def handle_event(self, event):
        if self.current_challenge:
            result = self.current_challenge.handle_event(event)
            if result == "completed":
                # Mark level as completed and unlock next level
                current_level_name = getattr(self.game, 'current_level_data', {}).get('name', '')
                
                # Find current level index and mark as completed
                world_map_state = self.game.states[GameState.WORLD_MAP]
                for i, level in enumerate(world_map_state.levels):
                    if level['name'] == current_level_name:
                        self.game.player_progress['completed_levels'].add(i)
                        # Unlock next level
                        if i + 1 < len(world_map_state.levels):
                            world_map_state.levels[i + 1]['unlocked'] = True
                        break
                
                # Add experience and skills to character
                if hasattr(self.game, 'character'):
                    self.game.character.gain_experience(100)
                    
                    # Add specific skills based on challenge type
                    challenge_skills = {
                        'neuron_basics': 'neuron_mastery',
                        'bias_battle': 'bias_manipulation', 
                        'activation_functions': 'activation_power',
                        'chain_rule_mastery': 'gradient_flow',
                        'perceptron_complete': 'network_building',
                        'forward_pass_flow': 'weight_control'
                    }
                    
                    skill_name = challenge_skills.get(getattr(self.game, 'current_challenge', ''), 'neuron_mastery')
                    self.game.character.gain_skill(skill_name, 25)
                
                self.game.change_state(GameState.WORLD_MAP)
            elif result == "exit":
                self.game.change_state(GameState.WORLD_MAP)
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.change_state(GameState.WORLD_MAP)
    
    def update(self, dt):
        if self.current_challenge:
            self.current_challenge.update(dt)
    
    def render(self, screen):
        if self.current_challenge:
            self.current_challenge.render(screen)
        else:
            # Fallback if no challenge loaded
            screen.fill((60, 20, 20))
            error_text = self.font.render("Challenge not found!", True, (255, 255, 255))
            error_rect = error_text.get_rect(center=(self.game.width // 2, self.game.height // 2))
            screen.blit(error_text, error_rect)