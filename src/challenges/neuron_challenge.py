"""
First challenge: Understanding neurons, weights, and basic computation
"""

import pygame
import numpy as np
import math
from .base_challenge import BaseChallenge
from ..visualization.neural_viz import NeuralNetworkVisualizer
from ..game_story import GameStory
try:
    from ..ui.responsive_layout import ResponsiveLayout, ResponsiveButton, ResponsiveSlider
except ImportError:
    from ui.responsive_layout import ResponsiveLayout, ResponsiveButton, ResponsiveSlider

class NeuronChallenge(BaseChallenge):
    def __init__(self, game):
        super().__init__(game)
        self.layout = ResponsiveLayout(game.width, game.height)
        self.story = GameStory()
        self.visualizer = NeuralNetworkVisualizer(game.width, game.height)
        
        # Challenge state
        self.phase = "story"  # story -> theory -> practice -> boss -> victory
        self.story_index = 0
        self.boss_hp = 100
        self.boss_max_hp = 100
        self.player_understanding = 0
        
        # Interactive neuron simulation
        self.input_values = [0.5, -0.3, 0.8]
        self.weights = [0.2, 0.7, -0.4]
        self.bias = 0.1
        self.selected_param = 0  # 0-2: weights, 3: bias, 4-6: inputs
        
        # Initialize all attributes first
        self.parameter_sliders = {}
        self.hints_shown = []
        self.hint_timer = 0.0
        
        self.boss_questions = [
            {
                "question": "What happens when you increase a positive weight?",
                "options": ["Output decreases", "Output increases", "No change", "Becomes negative"],
                "correct": 1,
                "explanation": "Positive weights amplify their inputs - higher weight means stronger influence!"
            },
            {
                "question": "What is the role of bias in a neuron?",
                "options": ["Multiplies inputs", "Shifts the threshold", "Activates the neuron", "Stores memory"],
                "correct": 1,
                "explanation": "Bias shifts the activation threshold, allowing neurons to fire even with zero input!"
            },
            {
                "question": "If all weights are zero, what determines the output?",
                "options": ["Random value", "Input values", "Only the bias", "Always zero"],
                "correct": 2,
                "explanation": "With zero weights, inputs are ignored - only bias affects the output!"
            }
        ]
        self.current_question = 0
        self.selected_answer = 0
        
        # Create responsive UI elements
        self._setup_responsive_ui()
        
    def _setup_responsive_ui(self):
        """Setup responsive UI elements"""
        # Create layout areas
        self.areas = self.layout.create_layout_areas(self.phase)
        
        # Create responsive sliders for weights and bias
        if self.phase in ["practice", "boss"]:
            self._create_parameter_sliders()
    
    def _create_parameter_sliders(self):
        """Create sliders for adjusting neuron parameters"""
        # Create sliders for weights and bias
        slider_rects = self.layout.distribute_horizontally(
            count=4,  # 3 weights + 1 bias
            width_percent=0.2,
            y_percent=0.7,
            height_percent=0.04,
            spacing_percent=0.02
        )
        
        labels = ["Weight 1", "Weight 2", "Weight 3", "Bias"]
        values = [self.weights[0], self.weights[1], self.weights[2], self.bias]
        
        for i, (label, value) in enumerate(zip(labels, values)):
            if i < len(slider_rects):
                self.parameter_sliders[f"param_{i}"] = ResponsiveSlider(
                    self.layout, slider_rects[i], label, -1.0, 1.0, value
                )
        
    def initialize(self):
        self.phase = "story"
        self.story_index = 0
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.phase == "story":
                if event.key == pygame.K_SPACE:
                    story_lines = self.story.get_level_intro("Neuron Academy", "Weight Master")
                    if self.story_index < len(story_lines) - 1:
                        self.story_index += 1
                    else:
                        self.phase = "theory"
                        
            elif self.phase == "theory":
                if event.key == pygame.K_SPACE:
                    self.phase = "practice"
                    
            elif self.phase == "practice":
                if event.key == pygame.K_LEFT:
                    self.selected_param = (self.selected_param - 1) % 7
                elif event.key == pygame.K_RIGHT:
                    self.selected_param = (self.selected_param + 1) % 7
                elif event.key == pygame.K_UP:
                    self._adjust_parameter(0.1)
                elif event.key == pygame.K_DOWN:
                    self._adjust_parameter(-0.1)
                elif event.key == pygame.K_SPACE:
                    if self.player_understanding >= 80:
                        self.phase = "boss"
                        
            elif self.phase == "boss":
                if event.key == pygame.K_UP:
                    self.selected_answer = (self.selected_answer - 1) % 4
                elif event.key == pygame.K_DOWN:
                    self.selected_answer = (self.selected_answer + 1) % 4
                elif event.key == pygame.K_RETURN:
                    self._answer_boss_question()
                    
            elif self.phase == "victory":
                if event.key == pygame.K_SPACE:
                    return "completed"
                    
            if event.key == pygame.K_ESCAPE:
                return "exit"
                
        return None
    
    def _adjust_parameter(self, delta):
        """Adjust the selected parameter and update understanding"""
        if self.selected_param < 3:  # Weights
            self.weights[self.selected_param] += delta
            self.weights[self.selected_param] = max(-2, min(2, self.weights[self.selected_param]))
        elif self.selected_param == 3:  # Bias
            self.bias += delta
            self.bias = max(-2, min(2, self.bias))
        else:  # Inputs
            input_idx = self.selected_param - 4
            self.input_values[input_idx] += delta
            self.input_values[input_idx] = max(-2, min(2, self.input_values[input_idx]))
        
        # Update understanding based on experimentation
        self.player_understanding = min(100, self.player_understanding + 2)
    
    def _answer_boss_question(self):
        """Handle boss battle question answering"""
        question = self.boss_questions[self.current_question]
        if self.selected_answer == question["correct"]:
            # Correct answer - damage boss
            damage = 35
            self.boss_hp -= damage
            if self.boss_hp <= 0:
                self.phase = "victory"
        else:
            # Wrong answer - show explanation and continue
            pass
        
        self.current_question += 1
        if self.current_question >= len(self.boss_questions) and self.boss_hp > 0:
            # Reset questions if boss still alive
            self.current_question = 0
        
        self.selected_answer = 0
    
    def _compute_neuron_output(self):
        """Compute the current neuron output"""
        weighted_sum = sum(w * x for w, x in zip(self.weights, self.input_values)) + self.bias
        return weighted_sum
    
    def update(self, dt):
        self.visualizer.update_animation(dt)
        self.hint_timer += dt
        
        # Show hints during practice phase
        if self.phase == "practice" and self.hint_timer > 10 and len(self.hints_shown) < 3:
            hints = self.story.get_hint_system("Neuron Academy")
            if len(self.hints_shown) < len(hints):
                self.hints_shown.append(hints[len(self.hints_shown)])
                self.hint_timer = 0
    
    def render(self, screen):
        # Pleasant gradient background
        for y in range(self.layout.screen_height):
            color_intensity = int(15 + (y / self.layout.screen_height) * 25)
            color = (color_intensity, color_intensity + 8, color_intensity + 30)
            pygame.draw.line(screen, color, (0, y), (self.layout.screen_width, y))
        
        # Update layout for current phase
        self.areas = self.layout.create_layout_areas(self.phase)
        
        if self.phase == "story":
            self._render_story(screen)
        elif self.phase == "theory":
            self._render_theory(screen)
        elif self.phase == "practice":
            self._render_practice(screen)
        elif self.phase == "boss":
            self._render_boss_battle(screen)
        elif self.phase == "victory":
            self._render_victory(screen)
    
    def _render_story(self, screen):
        """Render story introduction with responsive layout"""
        # Title
        title_rect = self.layout.get_rect(0, 0, 1, 0.15)
        title_font_size = self.layout.get_font_size(0.05, min_size=20, max_size=40)
        title_font = pygame.font.Font(None, title_font_size)
        self.layout.render_text_block(screen, "Chapter 1: The Neuron Academy", title_font, title_rect,
                                    (255, 255, 0), align="center", vertical_align="center")
        
        # Story dialogue
        story_lines = self.story.get_level_intro("Neuron Academy", "Weight Master")
        if self.story_index < len(story_lines):
            dialogue_rect = self.layout.get_rect(0.1, 0.2, 0.8, 0.5)
            
            # Background
            pygame.draw.rect(screen, (0, 0, 0, 180), dialogue_rect)
            pygame.draw.rect(screen, (255, 255, 255), dialogue_rect, 2)
            
            # Render current dialogue with responsive text
            text = story_lines[self.story_index]
            text_font_size = self.layout.get_font_size(0.03, min_size=14, max_size=24)
            text_font = pygame.font.Font(None, text_font_size)
            
            text_area = pygame.Rect(dialogue_rect.x + 20, dialogue_rect.y + 20,
                                  dialogue_rect.width - 40, dialogue_rect.height - 40)
            self.layout.render_text_block(screen, text, text_font, text_area,
                                        (255, 255, 255), align="left", vertical_align="top")
        
        # Continue instruction
        inst_rect = self.layout.get_rect(0, 0.8, 1, 0.1)
        inst_font_size = self.layout.get_font_size(0.03, min_size=16, max_size=24)
        inst_font = pygame.font.Font(None, inst_font_size)
        self.layout.render_text_block(screen, "Press SPACE to continue...", inst_font, inst_rect,
                                    (255, 255, 0), align="center", vertical_align="center")
    
    def _render_theory(self, screen):
        """Render theory explanation with improved visualization"""
        screen.fill((25, 35, 55))  # Clean dark blue background
        
        # Title with better positioning
        title = self.font.render("Understanding Neurons", True, (220, 240, 255))
        title_rect = title.get_rect(center=(self.game.width // 2, 30))
        screen.blit(title, title_rect)
        
        # Create a proper neural network diagram with better spacing
        diagram_area = pygame.Rect(50, 70, 600, 280)
        
        # Input layer positions (left side) - better spacing
        input_x = diagram_area.x + 60
        input_positions = [
            (input_x, diagram_area.y + 50),   # x₁
            (input_x, diagram_area.y + 140),  # x₂  
            (input_x, diagram_area.y + 230)   # x₃
        ]
        input_labels = ["x₁", "x₂", "x₃"]
        
        # Main neuron (center) - adjusted position
        neuron_x = diagram_area.x + 300
        neuron_y = diagram_area.y + 140
        
        # Output (right side)
        output_x = diagram_area.x + 540
        output_y = neuron_y
        
        # Calculate output
        output = self._compute_neuron_output()
        
        # Draw connections first (behind neurons) with better positioning
        for i, pos in enumerate(input_positions):
            weight = self.weights[i]
            thickness = max(2, min(6, int(abs(weight) * 4) + 2))
            color = (120, 220, 120) if weight > 0 else (220, 120, 120)
            
            # Draw connection line with proper endpoints to avoid overlap
            start_x = pos[0] + 28  # Start from edge of input neuron
            start_y = pos[1]
            end_x = neuron_x - 38   # End at edge of main neuron
            end_y = neuron_y
            
            pygame.draw.line(screen, color, (start_x, start_y), (end_x, end_y), thickness)
            
            # Weight label positioned better to avoid overlap
            mid_x = (start_x + end_x) // 2
            mid_y = (start_y + end_y) // 2
            
            # Offset label to avoid line overlap
            if i == 0:  # Top connection
                mid_y -= 20
            elif i == 2:  # Bottom connection  
                mid_y += 20
            
            # Background for weight text
            weight_font = pygame.font.Font(None, 18)
            weight_text = weight_font.render(f"w{i+1}={weight:.2f}", True, (255, 255, 255))
            weight_rect = weight_text.get_rect(center=(mid_x, mid_y))
            pygame.draw.rect(screen, (40, 50, 70), weight_rect.inflate(6, 4))
            pygame.draw.rect(screen, (100, 120, 150), weight_rect.inflate(6, 4), 1)
            screen.blit(weight_text, weight_rect)
        
        # Connection from neuron to output (avoid overlap)
        pygame.draw.line(screen, (150, 180, 255), (neuron_x + 38, neuron_y), (output_x - 28, output_y), 4)
        
        # Draw input neurons with better spacing
        for i, (pos, label) in enumerate(zip(input_positions, input_labels)):
            input_val = self.input_values[i]
            intensity = min(1.0, abs(input_val))
            base_color = (100, 150, 255)
            color = tuple(int(base_color[j] * (0.4 + 0.6 * intensity)) for j in range(3))
            
            # Draw input neuron
            pygame.draw.circle(screen, color, pos, 25)
            pygame.draw.circle(screen, (200, 220, 255), pos, 25, 3)
            
            # Input value inside circle
            val_text = pygame.font.Font(None, 16).render(f"{input_val:.1f}", True, (255, 255, 255))
            val_rect = val_text.get_rect(center=pos)
            screen.blit(val_text, val_rect)
            
            # Input label above circle (no overlap)
            label_text = pygame.font.Font(None, 22).render(label, True, (200, 220, 255))
            label_rect = label_text.get_rect(center=(pos[0], pos[1] - 35))
            screen.blit(label_text, label_rect)
        
        # Draw main neuron with bias
        neuron_intensity = min(1.0, abs(output) / 2.0)
        neuron_color = (150, 255, 150) if output > 0 else (255, 150, 150)
        neuron_color = tuple(int(neuron_color[i] * (0.4 + 0.6 * neuron_intensity)) for i in range(3))
        
        pygame.draw.circle(screen, neuron_color, (neuron_x, neuron_y), 35)
        pygame.draw.circle(screen, (220, 255, 220), (neuron_x, neuron_y), 35, 4)
        
        # Neuron label and bias
        neuron_label = pygame.font.Font(None, 20).render("Neuron", True, (255, 255, 255))
        neuron_label_rect = neuron_label.get_rect(center=(neuron_x, neuron_y - 50))
        screen.blit(neuron_label, neuron_label_rect)
        
        # Bias display below neuron
        bias_text = pygame.font.Font(None, 18).render(f"bias={self.bias:.2f}", True, (255, 255, 100))
        bias_rect = bias_text.get_rect(center=(neuron_x, neuron_y + 50))
        pygame.draw.rect(screen, (40, 50, 70), bias_rect.inflate(6, 4))
        pygame.draw.rect(screen, (100, 120, 150), bias_rect.inflate(6, 4), 1)
        screen.blit(bias_text, bias_rect)
        
        # Draw output neuron
        output_intensity = min(1.0, abs(output) / 2.0)
        output_color = (255, 200, 100)
        output_color = tuple(int(output_color[i] * (0.4 + 0.6 * output_intensity)) for i in range(3))
        
        pygame.draw.circle(screen, output_color, (output_x, output_y), 25)
        pygame.draw.circle(screen, (255, 220, 180), (output_x, output_y), 25, 3)
        
        # Output value
        out_text = pygame.font.Font(None, 16).render(f"{output:.2f}", True, (255, 255, 255))
        out_rect = out_text.get_rect(center=(output_x, output_y))
        screen.blit(out_text, out_rect)
        
        # Output label
        out_label = pygame.font.Font(None, 22).render("Output", True, (255, 220, 180))
        out_label_rect = out_label.get_rect(center=(output_x, output_y - 35))
        screen.blit(out_label, out_label_rect)
        
        # Mathematical formula and explanation section
        formula_y = 380
        
        # Formula title
        formula_title = pygame.font.Font(None, 28).render("Neuron Formula:", True, (255, 255, 100))
        screen.blit(formula_title, (50, formula_y))
        
        # Main formula with better formatting
        formula_font = pygame.font.Font(None, 24)
        formula_lines = [
            "output = Σ(input × weight) + bias",
            f"output = (x₁ × w₁) + (x₂ × w₂) + (x₃ × w₃) + bias",
            f"output = ({self.input_values[0]:.1f} × {self.weights[0]:.1f}) + ({self.input_values[1]:.1f} × {self.weights[1]:.1f}) + ({self.input_values[2]:.1f} × {self.weights[2]:.1f}) + {self.bias:.1f}",
            f"output = {output:.3f}"
        ]
        
        for i, line in enumerate(formula_lines):
            color = (255, 255, 100) if i == 0 else (200, 255, 200) if i == len(formula_lines)-1 else (255, 255, 255)
            text = formula_font.render(line, True, color)
            screen.blit(text, (50, formula_y + 30 + i * 25))
        
        # Explanation section
        explanation_x = 50
        explanation_y = formula_y + 160
        
        explanation_title = pygame.font.Font(None, 26).render("How it works:", True, (255, 200, 100))
        screen.blit(explanation_title, (explanation_x, explanation_y))
        
        explanation_font = pygame.font.Font(None, 20)
        explanations = [
            "• Each input (x₁, x₂, x₃) represents a feature or data point",
            "• Weights (w₁, w₂, w₃) control how much each input influences the output",
            "• Positive weights amplify inputs, negative weights diminish them",
            "• Bias shifts the activation threshold - helps neuron fire even with zero input",
            "• The neuron sums all weighted inputs plus bias to produce final output",
            "• This output can then be passed through an activation function"
        ]
        
        for i, explanation in enumerate(explanations):
            text = explanation_font.render(explanation, True, (220, 220, 220))
            screen.blit(text, (explanation_x, explanation_y + 30 + i * 22))
        output_text = pygame.font.Font(None, 20).render(f"{output:.2f}", True, (255, 255, 255))
        output_rect = output_text.get_rect(center=(neuron_x, neuron_y))
        screen.blit(output_text, output_rect)
        
        # Bias indicator
        bias_text = pygame.font.Font(None, 18).render(f"bias={self.bias:.2f}", True, (255, 255, 180))
        bias_rect = bias_text.get_rect(center=(neuron_x, neuron_y + 50))
        pygame.draw.rect(screen, (60, 70, 90, 200), bias_rect.inflate(8, 4))
        screen.blit(bias_text, bias_rect)
        
        # Neuron label
        neuron_label = pygame.font.Font(None, 24).render("Neuron", True, (200, 255, 200))
        neuron_label_rect = neuron_label.get_rect(center=(neuron_x, neuron_y - 55))
        screen.blit(neuron_label, neuron_label_rect)
        
        # Draw output node
        output_color = (255, 180, 100)
        pygame.draw.circle(screen, output_color, (output_x, output_y), 25)
        pygame.draw.circle(screen, (255, 220, 180), (output_x, output_y), 25, 3)
        
        # Output value
        out_text = pygame.font.Font(None, 18).render(f"{output:.2f}", True, (255, 255, 255))
        out_rect = out_text.get_rect(center=(output_x, output_y))
        screen.blit(out_text, out_rect)
        
        # Output label
        out_label = pygame.font.Font(None, 24).render("Output", True, (255, 200, 150))
        out_label_rect = out_label.get_rect(center=(output_x, output_y - 40))
        screen.blit(out_label, out_label_rect)
        
        # Formula section with better layout
        formula_area = pygame.Rect(50, 400, self.game.width - 100, 150)
        pygame.draw.rect(screen, (30, 40, 60, 200), formula_area, border_radius=10)
        pygame.draw.rect(screen, (100, 150, 200), formula_area, 2, border_radius=10)
        
        formula_text = [
            "Neuron Computation Formula:",
            f"output = Σ(input × weight) + bias",
            f"output = ({self.input_values[0]:.1f}×{self.weights[0]:.1f}) + ({self.input_values[1]:.1f}×{self.weights[1]:.1f}) + ({self.input_values[2]:.1f}×{self.weights[2]:.1f}) + {self.bias:.1f}",
            f"output = {output:.2f}"
        ]
        
        for i, line in enumerate(formula_text):
            if i == 0:
                color = (255, 220, 100)  # Golden for title
                font_size = 26
            elif i == len(formula_text) - 1:
                color = (150, 255, 150)  # Green for result
                font_size = 24
            else:
                color = (200, 220, 255)  # Light blue for formula
                font_size = 22
            
            text = pygame.font.Font(None, font_size).render(line, True, color)
            text_rect = text.get_rect(center=(formula_area.centerx, formula_area.y + 30 + i * 30))
            screen.blit(text, text_rect)
        
        # Continue instruction with better styling
        inst_text = "Press SPACE to start practicing!"
        inst_surface = pygame.font.Font(None, 28).render(inst_text, True, (255, 255, 100))
        inst_rect = inst_surface.get_rect(center=(self.game.width // 2, self.game.height - 40))
        
        # Background for instruction
        inst_bg = inst_rect.inflate(20, 10)
        pygame.draw.rect(screen, (50, 70, 100, 200), inst_bg, border_radius=8)
        pygame.draw.rect(screen, (255, 255, 100), inst_bg, 2, border_radius=8)
        screen.blit(inst_surface, inst_rect)
    
    def _render_practice(self, screen):
        """Render interactive practice mode with improved layout"""
        # Pleasant gradient background
        for y in range(self.game.height):
            color_intensity = int(20 + (y / self.game.height) * 20)
            color = (color_intensity, color_intensity + 8, color_intensity + 25)
            pygame.draw.line(screen, color, (0, y), (self.game.width, y))
        
        # Title
        title = self.font.render("Interactive Neural Network Lab", True, (220, 240, 255))
        title_rect = title.get_rect(center=(self.game.width // 2, 30))
        screen.blit(title, title_rect)
        
        # Understanding meter with better styling
        meter_x, meter_y = 50, 70
        meter_width, meter_height = 300, 25
        
        # Background
        pygame.draw.rect(screen, (40, 50, 70), (meter_x, meter_y, meter_width, meter_height), border_radius=12)
        
        # Fill
        understanding_filled = int(meter_width * self.player_understanding / 100)
        if understanding_filled > 0:
            fill_color = (100, 255, 150) if self.player_understanding >= 80 else (255, 200, 100)
            pygame.draw.rect(screen, fill_color, (meter_x, meter_y, understanding_filled, meter_height), border_radius=12)
        
        # Border
        pygame.draw.rect(screen, (150, 180, 220), (meter_x, meter_y, meter_width, meter_height), 3, border_radius=12)
        
        # Text
        understanding_text = pygame.font.Font(None, 24).render(f"Understanding: {self.player_understanding}%", True, (220, 240, 255))
        screen.blit(understanding_text, (meter_x + meter_width + 20, meter_y + 3))
        
        # Split screen: visualization on left, controls on right
        viz_area = pygame.Rect(20, 110, self.game.width * 0.65, 350)
        control_area = pygame.Rect(self.game.width * 0.68, 110, self.game.width * 0.3, 350)
        
        # Render neural network in visualization area
        self._render_interactive_network(screen, viz_area)
        
        # Parameter controls panel
        pygame.draw.rect(screen, (30, 40, 60, 220), control_area, border_radius=10)
        pygame.draw.rect(screen, (100, 150, 200), control_area, 2, border_radius=10)
        
        # Controls title
        controls_title = pygame.font.Font(None, 26).render("Parameters", True, (200, 220, 255))
        screen.blit(controls_title, (control_area.x + 10, control_area.y + 10))
        
        # Parameter controls with better layout
        param_names = ["Weight 1", "Weight 2", "Weight 3", "Bias", "Input 1", "Input 2", "Input 3"]
        param_values = self.weights + [self.bias] + self.input_values
        param_colors = [(120, 220, 120)] * 3 + [(255, 200, 100)] + [(100, 150, 255)] * 3
        
        for i, (name, value, base_color) in enumerate(zip(param_names, param_values, param_colors)):
            y_pos = control_area.y + 50 + i * 40
            
            # Highlight selected parameter
            if i == self.selected_param:
                highlight_rect = pygame.Rect(control_area.x + 5, y_pos - 5, control_area.width - 10, 35)
                pygame.draw.rect(screen, (80, 100, 140, 150), highlight_rect, border_radius=5)
                pygame.draw.rect(screen, (255, 255, 100), highlight_rect, 2, border_radius=5)
                text_color = (255, 255, 150)
            else:
                text_color = base_color
            
            # Parameter name and value
            param_text = pygame.font.Font(None, 22).render(f"{name}:", True, text_color)
            screen.blit(param_text, (control_area.x + 10, y_pos))
            
            value_text = pygame.font.Font(None, 22).render(f"{value:.2f}", True, text_color)
            value_rect = value_text.get_rect(right=control_area.right - 10, y=y_pos)
            screen.blit(value_text, value_rect)
            
            # Visual bar for parameter value
            bar_width = 80
            bar_x = control_area.x + 10
            bar_y = y_pos + 20
            bar_value = max(-2, min(2, value))  # Clamp to display range
            bar_fill = int((bar_value + 2) / 4 * bar_width)  # Map -2 to 2 -> 0 to bar_width
            
            # Bar background
            pygame.draw.rect(screen, (50, 60, 80), (bar_x, bar_y, bar_width, 8), border_radius=4)
            
            # Bar fill
            if bar_fill > bar_width // 2:
                # Positive values - green
                pygame.draw.rect(screen, (100, 255, 100), (bar_x + bar_width // 2, bar_y, bar_fill - bar_width // 2, 8), border_radius=4)
            else:
                # Negative values - red
                pygame.draw.rect(screen, (255, 100, 100), (bar_x + bar_fill, bar_y, bar_width // 2 - bar_fill, 8), border_radius=4)
            
            # Center line
            pygame.draw.line(screen, (200, 200, 200), (bar_x + bar_width // 2, bar_y), (bar_x + bar_width // 2, bar_y + 8), 1)
        
        # Instructions with better styling
        inst_area = pygame.Rect(50, self.game.height - 120, self.game.width - 100, 80)
        pygame.draw.rect(screen, (25, 35, 55, 200), inst_area, border_radius=8)
        pygame.draw.rect(screen, (100, 150, 200), inst_area, 2, border_radius=8)
        
        instructions = [
            "🎮 Controls: LEFT/RIGHT - Select parameter, UP/DOWN - Adjust value",
            "🧠 Experiment with different values to see how they affect the output!",
            "📈 Watch the connections change color and thickness based on weights"
        ]
        
        for i, instruction in enumerate(instructions):
            text = pygame.font.Font(None, 20).render(instruction, True, (200, 220, 255))
            screen.blit(text, (inst_area.x + 10, inst_area.y + 10 + i * 22))
        
        # Boss battle ready indicator
        if self.player_understanding >= 80:
            ready_area = pygame.Rect(self.game.width // 2 - 200, self.game.height - 50, 400, 35)
            pygame.draw.rect(screen, (50, 150, 50, 200), ready_area, border_radius=8)
            pygame.draw.rect(screen, (100, 255, 100), ready_area, 3, border_radius=8)
            
            ready_text = pygame.font.Font(None, 28).render("🎯 Ready for Challenge! Press SPACE", True, (150, 255, 150))
            ready_rect = ready_text.get_rect(center=ready_area.center)
            screen.blit(ready_text, ready_rect)
    
    def _render_interactive_network(self, screen, area):
        """Render the interactive neural network in the given area"""
        # Network positions within the area
        input_x = area.x + 60
        neuron_x = area.centerx
        output_x = area.right - 60
        
        input_positions = [
            (input_x, area.y + 80),
            (input_x, area.centery),
            (input_x, area.bottom - 80)
        ]
        
        neuron_pos = (neuron_x, area.centery)
        output_pos = (output_x, area.centery)
        
        # Compute output
        output = self._compute_neuron_output()
        
        # Draw connections with animated flow
        for i, pos in enumerate(input_positions):
            weight = self.weights[i]
            
            # Connection styling based on weight
            thickness = max(2, min(10, int(abs(weight) * 4)))
            if weight > 0:
                color = (120, 255, 120, 200)
            else:
                color = (255, 120, 120, 200)
            
            # Draw connection line
            pygame.draw.line(screen, color[:3], pos, neuron_pos, thickness)
            
            # Animated data flow (small moving circles)
            flow_progress = (pygame.time.get_ticks() / 1000.0 + i * 0.3) % 1.0
            flow_x = pos[0] + (neuron_pos[0] - pos[0]) * flow_progress
            flow_y = pos[1] + (neuron_pos[1] - pos[1]) * flow_progress
            
            flow_color = (255, 255, 150) if abs(self.input_values[i]) > 0.1 else (100, 100, 100)
            pygame.draw.circle(screen, flow_color, (int(flow_x), int(flow_y)), 4)
            
            # Weight label with background
            mid_x = (pos[0] + neuron_pos[0]) // 2
            mid_y = (pos[1] + neuron_pos[1]) // 2 - 20
            
            weight_text = pygame.font.Font(None, 18).render(f"w{i+1}={weight:.2f}", True, (255, 255, 255))
            weight_rect = weight_text.get_rect(center=(mid_x, mid_y))
            pygame.draw.rect(screen, (40, 50, 70, 200), weight_rect.inflate(6, 4), border_radius=3)
            screen.blit(weight_text, weight_rect)
        
        # Output connection
        pygame.draw.line(screen, (150, 180, 255), neuron_pos, output_pos, 5)
        
        # Draw neurons with enhanced visuals
        for i, (pos, label) in enumerate(zip(input_positions, ["x₁", "x₂", "x₃"])):
            input_val = self.input_values[i]
            
            # Pulsing effect based on value
            pulse = abs(math.sin(pygame.time.get_ticks() / 500.0)) * 0.3 + 0.7
            intensity = min(1.0, abs(input_val)) * pulse
            
            base_color = (100, 150, 255)
            color = tuple(int(base_color[j] * (0.3 + 0.7 * intensity)) for j in range(3))
            
            # Highlight if selected
            radius = 28 if self.selected_param == i + 4 else 25
            
            pygame.draw.circle(screen, color, pos, radius)
            pygame.draw.circle(screen, (200, 220, 255), pos, radius, 3)
            
            # Value display
            val_text = pygame.font.Font(None, 16).render(f"{input_val:.1f}", True, (255, 255, 255))
            val_rect = val_text.get_rect(center=pos)
            screen.blit(val_text, val_rect)
            
            # Label
            label_text = pygame.font.Font(None, 22).render(label, True, (200, 220, 255))
            label_rect = label_text.get_rect(center=(pos[0], pos[1] - 45))
            screen.blit(label_text, label_rect)
        
        # Main neuron with bias visualization
        neuron_intensity = min(1.0, abs(output) / 3.0)
        pulse = abs(math.sin(pygame.time.get_ticks() / 300.0)) * 0.2 + 0.8
        
        if output > 0:
            neuron_color = (150, 255, 150)
        else:
            neuron_color = (255, 150, 150)
        
        neuron_color = tuple(int(neuron_color[i] * (0.4 + 0.6 * neuron_intensity * pulse)) for i in range(3))
        
        # Highlight if bias is selected
        radius = 40 if self.selected_param == 3 else 35
        
        pygame.draw.circle(screen, neuron_color, neuron_pos, radius)
        pygame.draw.circle(screen, (220, 255, 220), neuron_pos, radius, 4)
        
        # Output value
        output_text = pygame.font.Font(None, 18).render(f"{output:.2f}", True, (255, 255, 255))
        output_rect = output_text.get_rect(center=neuron_pos)
        screen.blit(output_text, output_rect)
        
        # Bias indicator
        bias_text = pygame.font.Font(None, 16).render(f"b={self.bias:.2f}", True, (255, 255, 180))
        bias_rect = bias_text.get_rect(center=(neuron_pos[0], neuron_pos[1] + 55))
        pygame.draw.rect(screen, (60, 70, 90, 200), bias_rect.inflate(6, 4), border_radius=3)
        screen.blit(bias_text, bias_rect)
        
        # Neuron label
        neuron_label = pygame.font.Font(None, 22).render("Neuron", True, (200, 255, 200))
        neuron_label_rect = neuron_label.get_rect(center=(neuron_pos[0], neuron_pos[1] - 55))
        screen.blit(neuron_label, neuron_label_rect)
        
        # Output node
        output_color = (255, 180, 100)
        pygame.draw.circle(screen, output_color, output_pos, 25)
        pygame.draw.circle(screen, (255, 220, 180), output_pos, 25, 3)
        
        # Output value
        out_text = pygame.font.Font(None, 16).render(f"{output:.2f}", True, (255, 255, 255))
        out_rect = out_text.get_rect(center=output_pos)
        screen.blit(out_text, out_rect)
        
        # Output label
        out_label = pygame.font.Font(None, 22).render("Output", True, (255, 200, 150))
        out_label_rect = out_label.get_rect(center=(output_pos[0], output_pos[1] - 45))
        screen.blit(out_label, out_label_rect)
    
    def _render_boss_battle(self, screen):
        """Render boss battle interface"""
        # Boss
        boss_rect = pygame.Rect(self.game.width // 2 - 100, 100, 200, 150)
        pygame.draw.rect(screen, (100, 0, 0), boss_rect)
        pygame.draw.rect(screen, (255, 255, 255), boss_rect, 3)
        
        boss_text = self.font.render("Weight Master", True, (255, 255, 255))
        boss_text_rect = boss_text.get_rect(center=(boss_rect.centerx, boss_rect.centery))
        screen.blit(boss_text, boss_text_rect)
        
        # Boss HP bar
        hp_width = 300
        hp_filled = int(hp_width * self.boss_hp / self.boss_max_hp)
        pygame.draw.rect(screen, (100, 0, 0), (self.game.width // 2 - 150, 270, hp_width, 20))
        pygame.draw.rect(screen, (255, 0, 0), (self.game.width // 2 - 150, 270, hp_filled, 20))
        pygame.draw.rect(screen, (255, 255, 255), (self.game.width // 2 - 150, 270, hp_width, 20), 2)
        
        hp_text = pygame.font.Font(None, 24).render(f"Boss HP: {self.boss_hp}/{self.boss_max_hp}", True, (255, 255, 255))
        screen.blit(hp_text, (self.game.width // 2 - 60, 300))
        
        # Current question
        if self.current_question < len(self.boss_questions):
            question = self.boss_questions[self.current_question]
            
            # Question text
            q_text = pygame.font.Font(None, 28).render(question["question"], True, (255, 255, 255))
            q_rect = q_text.get_rect(center=(self.game.width // 2, 350))
            screen.blit(q_text, q_rect)
            
            # Answer options
            for i, option in enumerate(question["options"]):
                color = (255, 255, 0) if i == self.selected_answer else (255, 255, 255)
                option_text = pygame.font.Font(None, 24).render(f"{i+1}. {option}", True, color)
                screen.blit(option_text, (self.game.width // 2 - 200, 400 + i * 40))
        
        # Instructions
        inst = pygame.font.Font(None, 24).render("Use UP/DOWN to select, ENTER to answer", True, (200, 200, 200))
        inst_rect = inst.get_rect(center=(self.game.width // 2, self.game.height - 50))
        screen.blit(inst, inst_rect)
    
    def _render_victory(self, screen):
        """Render victory screen"""
        # Victory message
        victory_text = self.font.render("VICTORY!", True, (255, 255, 0))
        victory_rect = victory_text.get_rect(center=(self.game.width // 2, 200))
        screen.blit(victory_text, victory_rect)
        
        # Story conclusion
        victory_lines = self.story.get_victory_message("Neuron Academy", "Weight Master")
        for i, line in enumerate(victory_lines):
            text = pygame.font.Font(None, 28).render(line, True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.game.width // 2, 300 + i * 40))
            screen.blit(text, text_rect)
        
        # Continue instruction
        inst = pygame.font.Font(None, 24).render("Press SPACE to continue your journey!", True, (255, 255, 0))
        inst_rect = inst.get_rect(center=(self.game.width // 2, self.game.height - 50))
        screen.blit(inst, inst_rect)