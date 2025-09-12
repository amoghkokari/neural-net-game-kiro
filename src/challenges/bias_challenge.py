"""
Bias Challenge: Understanding how bias affects neural network decisions
"""

import pygame
import numpy as np
import math
from .base_challenge import BaseChallenge
from ..visualization.neural_viz import NeuralNetworkVisualizer
from ..game_story import GameStory

class BiasChallenge(BaseChallenge):
    def __init__(self, game):
        super().__init__(game)
        self.story = GameStory()
        self.visualizer = NeuralNetworkVisualizer(game.width, game.height)
        
        # Challenge phases
        self.phase = "story"  # story -> demo -> practice -> boss -> victory
        self.story_index = 0
        
        # Interactive bias demonstration
        self.demo_inputs = [0.0, 0.0]  # Start with zero inputs
        self.demo_weights = [0.5, 0.5]
        self.demo_bias = 0.0
        self.bias_slider = 0.0  # -2 to 2
        
        # Boss battle
        self.boss_hp = 100
        self.boss_max_hp = 100
        self.boss_phase = 0  # Different attack patterns
        
        # Bias scenarios for boss battle
        self.scenarios = [
            {
                "description": "Make this neuron activate with zero inputs",
                "inputs": [0.0, 0.0],
                "weights": [0.3, 0.7],
                "target_output": 1.0,
                "solution_bias": 0.5,  # Needs positive bias
                "hint": "You need to shift the threshold down!"
            },
            {
                "description": "Prevent activation even with strong positive inputs",
                "inputs": [1.0, 1.0],
                "weights": [0.8, 0.6],
                "target_output": 0.0,
                "solution_bias": -2.0,  # Needs strong negative bias
                "hint": "Make the threshold very high!"
            },
            {
                "description": "Fine-tune for precise threshold",
                "inputs": [0.3, 0.7],
                "weights": [0.4, 0.6],
                "target_output": 1.0,
                "solution_bias": 0.2,
                "hint": "Small adjustments can make big differences!"
            }
        ]
        self.current_scenario = 0
        self.player_bias = 0.0
        
    def initialize(self):
        self.phase = "story"
        self.story_index = 0
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.phase == "story":
                if event.key == pygame.K_SPACE:
                    story_lines = self.story.get_level_intro("Bias Battlefield", "Bias Baron")
                    if self.story_index < len(story_lines) - 1:
                        self.story_index += 1
                    else:
                        self.phase = "demo"
                        
            elif self.phase == "demo":
                if event.key == pygame.K_LEFT:
                    self.bias_slider = max(-2.0, self.bias_slider - 0.1)
                elif event.key == pygame.K_RIGHT:
                    self.bias_slider = min(2.0, self.bias_slider + 0.1)
                elif event.key == pygame.K_SPACE:
                    self.phase = "practice"
                    
            elif self.phase == "practice":
                if event.key == pygame.K_LEFT:
                    self.player_bias = max(-3.0, self.player_bias - 0.1)
                elif event.key == pygame.K_RIGHT:
                    self.player_bias = min(3.0, self.player_bias + 0.1)
                elif event.key == pygame.K_RETURN:
                    if self._check_scenario_solution():
                        self._damage_boss()
                elif event.key == pygame.K_SPACE and self.boss_hp <= 0:
                    self.phase = "victory"
                    
            elif self.phase == "victory":
                if event.key == pygame.K_SPACE:
                    return "completed"
                    
            if event.key == pygame.K_ESCAPE:
                return "exit"
                
        return None
    
    def _step_function(self, x):
        """Step activation function"""
        return 1.0 if x > 0 else 0.0
    
    def _compute_output(self, inputs, weights, bias):
        """Compute neuron output"""
        weighted_sum = sum(w * x for w, x in zip(weights, inputs)) + bias
        return self._step_function(weighted_sum)
    
    def _check_scenario_solution(self):
        """Check if current bias setting solves the scenario"""
        scenario = self.scenarios[self.current_scenario]
        output = self._compute_output(scenario["inputs"], scenario["weights"], self.player_bias)
        tolerance = 0.1
        
        return abs(output - scenario["target_output"]) < tolerance
    
    def _damage_boss(self):
        """Damage boss when scenario is solved correctly"""
        damage = 35
        self.boss_hp -= damage
        
        if self.boss_hp > 0:
            self.current_scenario = (self.current_scenario + 1) % len(self.scenarios)
            self.player_bias = 0.0  # Reset for next scenario
    
    def update(self, dt):
        self.visualizer.update_animation(dt)
        self.demo_bias = self.bias_slider  # Sync demo bias with slider
    
    def render(self, screen):
        screen.fill((25, 35, 55))  # Clean dark blue background like first level
        
        if self.phase == "story":
            self._render_story(screen)
        elif self.phase == "demo":
            self._render_demo(screen)
        elif self.phase == "practice":
            self._render_practice(screen)
        elif self.phase == "victory":
            self._render_victory(screen)
    
    def _render_story(self, screen):
        """Render story introduction"""
        title = self.font.render("Chapter 2: The Bias Battlefield", True, (255, 100, 255))
        title_rect = title.get_rect(center=(self.game.width // 2, 100))
        screen.blit(title, title_rect)
        
        # Story dialogue
        story_lines = self.story.get_level_intro("Bias Battlefield", "Bias Baron")
        if self.story_index < len(story_lines):
            dialogue_rect = pygame.Rect(100, 200, self.game.width - 200, 300)
            pygame.draw.rect(screen, (0, 0, 0, 180), dialogue_rect)
            pygame.draw.rect(screen, (255, 100, 255), dialogue_rect, 2)
            
            text = story_lines[self.story_index]
            self._render_wrapped_text(screen, text, dialogue_rect, (255, 255, 255))
        
        # Continue instruction
        inst = pygame.font.Font(None, 24).render("Press SPACE to continue...", True, (255, 255, 0))
        inst_rect = inst.get_rect(center=(self.game.width // 2, self.game.height - 50))
        screen.blit(inst, inst_rect)
    
    def _render_demo(self, screen):
        """Render interactive bias demonstration"""
        title = self.font.render("Understanding Bias", True, (255, 255, 255))
        screen.blit(title, (50, 50))
        
        # Explanation
        explanation = [
            "Bias shifts the activation threshold of a neuron.",
            "With zero inputs, only bias determines if the neuron fires.",
            "Positive bias makes activation easier, negative makes it harder.",
            "",
            "Experiment with the bias slider below:"
        ]
        
        for i, line in enumerate(explanation):
            text = pygame.font.Font(None, 24).render(line, True, (255, 255, 255))
            screen.blit(text, (50, 100 + i * 30))
        
        # Interactive neuron with zero inputs
        neuron_x, neuron_y = 400, 350
        
        # Input nodes (showing zero)
        input_positions = [(200, 300), (200, 400)]
        for i, pos in enumerate(input_positions):
            self.visualizer.draw_neuron(screen, pos[0], pos[1], 20, 0.0, f"0.0", is_input=True)
            self.visualizer.draw_connection(screen, pos, (neuron_x, neuron_y), self.demo_weights[i], False, 20, 30)
        
        # Main neuron with bias
        output = self._compute_output(self.demo_inputs, self.demo_weights, self.demo_bias)
        self.visualizer.draw_neuron(screen, neuron_x, neuron_y, 30, output, f"bias={self.demo_bias:.1f}")
        
        # Output
        self.visualizer.draw_neuron(screen, 600, 350, 25, output, f"{output:.1f}", is_output=True)
        self.visualizer.draw_connection(screen, (neuron_x, neuron_y), (600, 350), 1.0, False, 30, 25)
        
        # Bias slider
        slider_rect = pygame.Rect(200, 500, 400, 20)
        pygame.draw.rect(screen, (100, 100, 100), slider_rect)
        
        # Slider handle
        handle_x = slider_rect.x + int((self.bias_slider + 2) / 4 * slider_rect.width)
        handle_rect = pygame.Rect(handle_x - 10, slider_rect.y - 5, 20, 30)
        pygame.draw.rect(screen, (255, 255, 0), handle_rect)
        
        # Slider labels
        pygame.font.Font(None, 20).render("-2", True, (255, 255, 255))
        screen.blit(pygame.font.Font(None, 20).render("-2", True, (255, 255, 255)), (180, 525))
        screen.blit(pygame.font.Font(None, 20).render("0", True, (255, 255, 255)), (395, 525))
        screen.blit(pygame.font.Font(None, 20).render("+2", True, (255, 255, 255)), (605, 525))
        
        # Current values
        values_text = [
            f"Weighted Sum: {sum(w * x for w, x in zip(self.demo_weights, self.demo_inputs)):.2f}",
            f"Bias: {self.demo_bias:.2f}",
            f"Total: {sum(w * x for w, x in zip(self.demo_weights, self.demo_inputs)) + self.demo_bias:.2f}",
            f"Output: {output:.1f} ({'ACTIVE' if output > 0.5 else 'INACTIVE'})"
        ]
        
        for i, text in enumerate(values_text):
            color = (0, 255, 0) if output > 0.5 and i == 3 else (255, 255, 255)
            rendered = pygame.font.Font(None, 24).render(text, True, color)
            screen.blit(rendered, (50, 550 + i * 30))
        
        # Instructions
        inst = pygame.font.Font(None, 24).render("Use LEFT/RIGHT arrows to adjust bias. Press SPACE when ready for battle!", True, (255, 255, 0))
        screen.blit(inst, (50, self.game.height - 50))
    
    def _render_practice(self, screen):
        """Render boss battle practice"""
        # Boss
        boss_rect = pygame.Rect(self.game.width // 2 - 100, 50, 200, 100)
        pygame.draw.rect(screen, (100, 0, 100), boss_rect)
        pygame.draw.rect(screen, (255, 100, 255), boss_rect, 3)
        
        boss_text = self.font.render("Bias Baron", True, (255, 255, 255))
        boss_text_rect = boss_text.get_rect(center=(boss_rect.centerx, boss_rect.centery))
        screen.blit(boss_text, boss_text_rect)
        
        # Boss HP
        hp_width = 300
        hp_filled = int(hp_width * self.boss_hp / self.boss_max_hp)
        hp_rect = pygame.Rect(self.game.width // 2 - 150, 170, hp_width, 20)
        pygame.draw.rect(screen, (100, 0, 0), hp_rect)
        pygame.draw.rect(screen, (255, 0, 0), (hp_rect.x, hp_rect.y, hp_filled, hp_rect.height))
        pygame.draw.rect(screen, (255, 255, 255), hp_rect, 2)
        
        # Current scenario
        if self.current_scenario < len(self.scenarios):
            scenario = self.scenarios[self.current_scenario]
            
            # Scenario description
            desc_text = pygame.font.Font(None, 28).render(scenario["description"], True, (255, 255, 255))
            desc_rect = desc_text.get_rect(center=(self.game.width // 2, 220))
            screen.blit(desc_text, desc_rect)
            
            # Neuron visualization
            neuron_x, neuron_y = 400, 320
            
            # Inputs
            input_positions = [(250, 280), (250, 360)]
            for i, pos in enumerate(input_positions):
                input_val = scenario["inputs"][i]
                self.visualizer.draw_neuron(screen, pos[0], pos[1], 20, input_val, f"{input_val:.1f}", is_input=True)
                self.visualizer.draw_connection(screen, pos, (neuron_x, neuron_y), scenario["weights"][i], False, 20, 30)
            
            # Main neuron
            current_output = self._compute_output(scenario["inputs"], scenario["weights"], self.player_bias)
            self.visualizer.draw_neuron(screen, neuron_x, neuron_y, 30, current_output, f"bias={self.player_bias:.1f}")
            
            # Target vs actual
            target_text = pygame.font.Font(None, 24).render(f"Target Output: {scenario['target_output']:.1f}", True, (255, 255, 0))
            actual_text = pygame.font.Font(None, 24).render(f"Current Output: {current_output:.1f}", True, (255, 255, 255))
            screen.blit(target_text, (550, 280))
            screen.blit(actual_text, (550, 310))
            
            # Bias control
            bias_text = pygame.font.Font(None, 24).render(f"Your Bias: {self.player_bias:.2f}", True, (255, 255, 255))
            screen.blit(bias_text, (50, 400))
            
            # Hint if struggling
            hint_text = pygame.font.Font(None, 20).render(f"Hint: {scenario['hint']}", True, (100, 255, 100))
            screen.blit(hint_text, (50, 430))
            
            # Instructions
            instructions = [
                "LEFT/RIGHT arrows: Adjust bias",
                "ENTER: Submit answer",
                f"Scenario {self.current_scenario + 1} of {len(self.scenarios)}"
            ]
            
            for i, instruction in enumerate(instructions):
                text = pygame.font.Font(None, 20).render(instruction, True, (200, 200, 200))
                screen.blit(text, (50, self.game.height - 100 + i * 25))
        
        if self.boss_hp <= 0:
            victory_text = self.font.render("BIAS BARON DEFEATED!", True, (0, 255, 0))
            victory_rect = victory_text.get_rect(center=(self.game.width // 2, 500))
            screen.blit(victory_text, victory_rect)
            
            continue_text = pygame.font.Font(None, 24).render("Press SPACE to continue!", True, (255, 255, 0))
            continue_rect = continue_text.get_rect(center=(self.game.width // 2, 540))
            screen.blit(continue_text, continue_rect)
    
    def _render_victory(self, screen):
        """Render victory screen"""
        victory_text = self.font.render("VICTORY!", True, (255, 255, 0))
        victory_rect = victory_text.get_rect(center=(self.game.width // 2, 200))
        screen.blit(victory_text, victory_rect)
        
        victory_lines = self.story.get_victory_message("Bias Battlefield", "Bias Baron")
        for i, line in enumerate(victory_lines):
            text = pygame.font.Font(None, 28).render(line, True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.game.width // 2, 300 + i * 40))
            screen.blit(text, text_rect)
        
        inst = pygame.font.Font(None, 24).render("Press SPACE to continue your journey!", True, (255, 255, 0))
        inst_rect = inst.get_rect(center=(self.game.width // 2, self.game.height - 50))
        screen.blit(inst, inst_rect)
    
    def _render_wrapped_text(self, screen, text, rect, color):
        """Helper to render wrapped text"""
        words = text.split(' ')
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            if pygame.font.Font(None, 28).size(test_line)[0] < rect.width - 40:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "
        lines.append(current_line.strip())
        
        for i, line in enumerate(lines):
            text_surface = pygame.font.Font(None, 28).render(line, True, color)
            screen.blit(text_surface, (rect.x + 20, rect.y + 20 + i * 35))