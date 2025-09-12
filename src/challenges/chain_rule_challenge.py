"""
Chain Rule Challenge - Level 4: The Derivative Dragon
"""

import pygame
import numpy as np
import math
import random
from .base_challenge import BaseChallenge
from ..visualization.neural_viz import NeuralNetworkVisualizer
from ..game_story import GameStory
# Audio removed for better performance
from ..ui.modern_ui import ModernButton, ProgressBar, DialogueBox, ParticleSystem

class ChainRuleChallenge(BaseChallenge):
    def __init__(self, game):
        super().__init__(game)
        self.story = GameStory()
        self.visualizer = NeuralNetworkVisualizer(game.width, game.height)
        self.particles = ParticleSystem()
        
        # Challenge phases
        self.phase = "intro"
        self.dialogue_box = DialogueBox(50, game.height - 200, game.width - 100, 150)
        
        # Chain rule visualization
        self.network_layers = [
            {"name": "Input", "value": 2.0, "derivative": 1.0},
            {"name": "Hidden 1", "value": 0.0, "derivative": 0.0, "weight": 0.5, "activation": "sigmoid"},
            {"name": "Hidden 2", "value": 0.0, "derivative": 0.0, "weight": 0.8, "activation": "relu"},
            {"name": "Output", "value": 0.0, "derivative": 0.0, "weight": 0.3, "activation": "linear"}
        ]
        
        # Boss battle - Chain rule calculation challenges
        self.boss_hp = 100
        self.boss_max_hp = 100
        self.current_challenge = 0
        self.selected_answer = 0
        
        # Chain rule challenges
        self.challenges = [
            {
                "description": "Calculate ∂L/∂w₁ for a 2-layer network",
                "network": "Input → w₁ → Sigmoid → w₂ → Output → Loss",
                "given": "∂L/∂output = 0.5, output = 0.8, sigmoid_input = 1.2",
                "answer": "0.0768",  # 0.5 * 1.0 * sigmoid'(1.2) * input
                "explanation": "∂L/∂w₁ = ∂L/∂output × ∂output/∂w₂ × ∂w₂/∂sigmoid × ∂sigmoid/∂w₁"
            },
            {
                "description": "Find gradient through ReLU activation",
                "network": "x = 2.0 → w = 0.5 → ReLU → Loss",
                "given": "∂L/∂output = -0.3, ReLU_input = 1.0",
                "answer": "-0.6",  # -0.3 * 1.0 * 2.0 (ReLU derivative is 1 for positive input)
                "explanation": "ReLU derivative is 1 for positive inputs, 0 for negative"
            },
            {
                "description": "Chain through multiple layers",
                "network": "Input → Layer1 → Layer2 → Layer3 → Loss",
                "given": "All derivatives = 0.5, input = 1.0",
                "answer": "0.125",  # 0.5^3 * 1.0
                "explanation": "Multiply all partial derivatives: 0.5 × 0.5 × 0.5 × 1.0"
            }
        ]
        
        # UI elements
        self.understanding_bar = ProgressBar(50, 50, 300, 25, 100)
        self.gradient_flow_animation = 0
        
        # Animation effects
        self.dragon_breath_particles = []
        self.victory_celebration = False
        
    def initialize(self):
        self.phase = "intro"
        self._start_intro()
    
    def _start_intro(self):
        """Start dramatic introduction"""
        intro_text = "Beware, mortal! I am the Derivative Dragon, keeper of the sacred Chain Rule! Without me, backpropagation is impossible!"
        self.dialogue_box.set_dialogue(intro_text, "Derivative Dragon")
        # Audio removed
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.phase == "intro":
                if event.key == pygame.K_SPACE and self.dialogue_box.is_complete():
                    self._advance_intro()
            elif self.phase == "theory":
                if event.key == pygame.K_SPACE:
                    self.phase = "practice"
                    self._start_practice()
            elif self.phase == "practice":
                if event.key == pygame.K_SPACE and self.understanding_bar.current_value >= 80:
                    self.phase = "boss"
                    self._start_boss_battle()
                elif event.key == pygame.K_f or event.key == pygame.K_RIGHT:  # F for Forward or RIGHT arrow
                    self._update_network_forward()
                    self._randomize_network()  # Add new values after each pass
                    self.understanding_bar.set_value(min(100, self.understanding_bar.current_value + 3))
                elif event.key == pygame.K_b or event.key == pygame.K_LEFT:  # B for Backward or LEFT arrow
                    self._update_network_backward()
                    self._add_noise_to_gradients()  # Add some variation to gradients
                    self.understanding_bar.set_value(min(100, self.understanding_bar.current_value + 5))
                elif event.key == pygame.K_r:  # R to reset/randomize
                    self._randomize_network()
                    self.understanding_bar.set_value(min(100, self.understanding_bar.current_value + 1))
                elif event.key == pygame.K_UP:  # Add weight adjustment
                    self._adjust_weights(0.1)
                elif event.key == pygame.K_DOWN:  # Add weight adjustment
                    self._adjust_weights(-0.1)
            elif self.phase == "boss":
                # Simplified boss battle - just demonstrate understanding
                if event.key == pygame.K_LEFT:
                    self.selected_answer = (self.selected_answer - 1) % 3
                elif event.key == pygame.K_RIGHT:
                    self.selected_answer = (self.selected_answer + 1) % 3
                elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    self._check_boss_answer()
            elif self.phase == "victory":
                if event.key == pygame.K_SPACE:
                    return "completed"
            
            if event.key == pygame.K_ESCAPE:
                return "exit"
        
        return None
    
    def _advance_intro(self):
        """Advance through introduction"""
        intros = [
            "The chain rule is the heart of backpropagation! It lets us compute gradients through complex networks.",
            "∂Loss/∂weight = ∂Loss/∂output × ∂output/∂activation × ∂activation/∂weight",
            "Each layer passes gradients backward, multiplying partial derivatives.",
            "Master this, and you control the flow of learning itself!"
        ]
        
        if not hasattr(self, 'intro_step'):
            self.intro_step = 0
        
        self.intro_step += 1
        
        if self.intro_step < len(intros):
            self.dialogue_box.set_dialogue(intros[self.intro_step], "Derivative Dragon")
            # Audio removed
        else:
            self.phase = "theory"
            self._start_theory()
    
    def _start_theory(self):
        """Start theory phase"""
        theory_text = "Observe how gradients flow backward through the network. Each layer multiplies the gradient by its local derivative."
        self.dialogue_box.set_dialogue(theory_text, "Tensor")
        # Audio removed
    
    def _start_practice(self):
        """Start practice phase"""
        practice_text = "Practice time! Press F/RIGHT for forward pass, B/LEFT for backward pass. Watch the gradients flow!"
        self.dialogue_box.set_dialogue(practice_text, "Tensor")
        # Audio removed
    
    def _start_boss_battle(self):
        """Start boss battle"""
        challenge = self.challenges[self.current_challenge]
        battle_text = f"Face my challenge! {challenge['description']}"
        self.dialogue_box.set_dialogue(battle_text, "Derivative Dragon")
        # Audio removed
    
    def _update_network_forward(self):
        """Update network forward pass"""
        if len(self.network_layers) <= 1:
            return
            
        for i in range(1, len(self.network_layers)):
            if i >= len(self.network_layers) or i-1 < 0:
                continue
                
            layer = self.network_layers[i]
            prev_layer = self.network_layers[i-1]
            
            # Safety checks
            if "value" not in prev_layer or "weight" not in layer:
                continue
            
            try:
                # Compute forward pass
                weighted_input = prev_layer["value"] * layer["weight"]
                # Clamp input to prevent numerical issues
                weighted_input = max(-50, min(50, weighted_input))
                
                if layer.get("activation") == "sigmoid":
                    layer["value"] = 1 / (1 + math.exp(-weighted_input))
                elif layer.get("activation") == "relu":
                    layer["value"] = max(0, weighted_input)
                else:  # linear
                    layer["value"] = weighted_input
                    
                # Clamp output values
                layer["value"] = max(-10.0, min(10.0, layer["value"]))
            except (OverflowError, ValueError, TypeError):
                layer["value"] = 0.0
    
    def _update_network_backward(self):
        """Update network backward pass (chain rule)"""
        if len(self.network_layers) == 0:
            return
            
        # Start from output with gradient of 1.0
        self.network_layers[-1]["derivative"] = 1.0
        
        # Propagate backward
        for i in range(len(self.network_layers) - 2, -1, -1):
            if i < 0 or i >= len(self.network_layers):
                continue
                
            current_layer = self.network_layers[i]
            next_layer = self.network_layers[i + 1]
            
            # Safety check
            if "value" not in next_layer or "weight" not in next_layer:
                continue
            
            # Compute local derivative based on activation
            try:
                if next_layer.get("activation") == "sigmoid":
                    sigmoid_val = next_layer["value"]
                    # Clamp sigmoid value to prevent numerical issues
                    sigmoid_val = max(0.001, min(0.999, sigmoid_val))
                    local_derivative = sigmoid_val * (1 - sigmoid_val)
                elif next_layer.get("activation") == "relu":
                    local_derivative = 1.0 if next_layer["value"] > 0 else 0.0
                else:  # linear
                    local_derivative = 1.0
                
                # Chain rule: multiply by weight and local derivative
                derivative_value = next_layer.get("derivative", 0.0) * next_layer["weight"] * local_derivative
                # Clamp to prevent numerical explosion
                current_layer["derivative"] = max(-10.0, min(10.0, derivative_value))
            except (KeyError, TypeError, ValueError):
                current_layer["derivative"] = 0.0
    
    def _randomize_network(self):
        """Randomize network values for practice"""
        try:
            for layer in self.network_layers:
                layer["value"] = random.uniform(-2, 2)
                if "weight" in layer:  # Only randomize weight if it exists
                    layer["weight"] = random.uniform(0.1, 1.0)
                layer["derivative"] = 0.0
        except (KeyError, TypeError):
            # Reset to safe defaults if there's an issue
            self.network_layers = [
                {"name": "Input", "value": 2.0, "derivative": 1.0},
                {"name": "Hidden 1", "value": 0.0, "derivative": 0.0, "weight": 0.5, "activation": "sigmoid"},
                {"name": "Hidden 2", "value": 0.0, "derivative": 0.0, "weight": 0.8, "activation": "relu"},
                {"name": "Output", "value": 0.0, "derivative": 0.0, "weight": 0.3, "activation": "linear"}
            ]
    
    def _add_noise_to_gradients(self):
        """Add small variations to gradients for more dynamic display"""
        for layer in self.network_layers:
            if layer["derivative"] != 0:
                noise = random.uniform(-0.1, 0.1)
                layer["derivative"] += noise
    
    def _adjust_weights(self, delta):
        """Allow manual weight adjustment"""
        for layer in self.network_layers:
            if "weight" in layer:  # Only adjust layers that have weights
                layer["weight"] = max(0.1, min(2.0, layer["weight"] + delta))
        # Recalculate forward pass with new weights
        self._update_network_forward()
    
    def _check_boss_answer(self):
        """Check boss battle answer - simplified multiple choice"""
        # Simple questions about chain rule concepts
        questions = [
            {
                "question": "What does chain rule calculate?",
                "options": ["Weights", "Gradients", "Activations"],
                "correct": 1
            },
            {
                "question": "Gradients flow which direction?",
                "options": ["Forward", "Backward", "Both ways"],
                "correct": 1
            },
            {
                "question": "Chain rule multiplies what?",
                "options": ["Weights", "Derivatives", "Inputs"],
                "correct": 1
            }
        ]
        
        if self.current_challenge < len(questions):
            question = questions[self.current_challenge]
            if self.selected_answer == question["correct"]:
                # Correct!
                self.boss_hp -= 35
                
                # Dragon takes damage - create fire particles
                for _ in range(20):
                    self.particles.add_particle(
                        random.randint(300, 700),
                        random.randint(100, 200),
                        (random.uniform(-100, 100), random.uniform(-50, 50)),
                        (255, random.randint(100, 200), 0),
                        random.uniform(1.0, 2.0),
                        random.randint(3, 8)
                    )
                
                response = "Correct! The chain rule helps us compute derivatives of composite functions!"
                self.dialogue_box.set_dialogue(response, "Tensor")
                # Audio removed
                
                if self.boss_hp <= 0:
                    self.phase = "victory"
                    self.victory_celebration = True
                    victory_text = "The Derivative Dragon is defeated! You have mastered the chain rule!"
                    self.dialogue_box.set_dialogue(victory_text, "Tensor")
                    # Audio removed
                else:
                    self.current_challenge = (self.current_challenge + 1) % len(questions)
            else:
                # Wrong answer
                response = "Not quite! Think about what the chain rule helps us calculate."
                self.dialogue_box.set_dialogue(response, "Derivative Dragon")
                # Audio removed
    
    def update(self, dt):
        self.visualizer.update_animation(dt)
        self.dialogue_box.update(dt)
        self.understanding_bar.update(dt)
        self.particles.update(dt)
        
        # Gradient flow animation
        self.gradient_flow_animation += dt * 2
        
        # Dragon breath effect
        if self.phase == "boss" and random.random() < 0.1:
            self.particles.add_particle(
                random.randint(400, 600),
                random.randint(80, 120),
                (random.uniform(-30, 30), random.uniform(20, 60)),
                (255, random.randint(50, 150), 0),
                random.uniform(0.5, 1.5),
                random.randint(3, 8)
            )
        
        # Victory celebration particles
        if self.victory_celebration:
            if random.random() < 0.3:
                self.particles.create_explosion(
                    random.randint(100, self.game.width - 100),
                    random.randint(100, 300),
                    (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)),
                    15
                )
    
    def render(self, screen):
        # Gradient background
        for y in range(self.game.height):
            intensity = int(30 + (y / self.game.height) * 30)
            color = (intensity, intensity + 10, intensity + 30)
            pygame.draw.line(screen, color, (0, y), (self.game.width, y))
        
        if self.phase in ["intro", "theory"]:
            self._render_intro_theory(screen)
        elif self.phase == "practice":
            self._render_practice(screen)
        elif self.phase == "boss":
            self._render_boss_battle(screen)
        elif self.phase == "victory":
            self._render_victory(screen)
        
        # Render dialogue only when not overlapping with instructions
        if self.phase != "practice":
            self.dialogue_box.render(screen, pygame.font.Font(None, 28), pygame.font.Font(None, 32))
        self.particles.render(screen)
    
    def _render_intro_theory(self, screen):
        """Render intro and theory phases"""
        # Title
        title_font = pygame.font.Font(None, 48)
        title = title_font.render("The Chain Rule", True, (255, 100, 100))
        title_rect = title.get_rect(center=(self.game.width // 2, 80))
        screen.blit(title, title_rect)
        
        # Dragon
        dragon_rect = pygame.Rect(self.game.width // 2 - 150, 120, 300, 120)
        pygame.draw.rect(screen, (200, 50, 50), dragon_rect, border_radius=20)
        
        dragon_font = pygame.font.Font(None, 36)
        dragon_text = dragon_font.render("🐉 Derivative Dragon", True, (255, 255, 255))
        dragon_text_rect = dragon_text.get_rect(center=dragon_rect.center)
        screen.blit(dragon_text, dragon_text_rect)
        
        if self.phase == "theory":
            self._render_chain_rule_diagram(screen, 100, 280, 800, 200)
    
    def _render_practice(self, screen):
        """Render practice phase"""
        # Understanding bar
        self.understanding_bar.render(screen, pygame.font.Font(None, 24))
        
        # Network visualization
        self._render_network_with_gradients(screen, 100, 100, 800, 400)
        
        # Instructions with better positioning to avoid overlap
        inst_rect = pygame.Rect(50, 420, 700, 80)
        pygame.draw.rect(screen, (40, 50, 70), inst_rect)
        pygame.draw.rect(screen, (100, 150, 200), inst_rect, 2)
        
        font = pygame.font.Font(None, 20)
        instructions = [
            "Controls: F/RIGHT = Forward Pass, B/LEFT = Backward Pass, R = Reset",
            "UP/DOWN = Adjust Weights, Watch gradients flow backward!",
            f"Understanding: {int(self.understanding_bar.current_value)}% - Values change each pass!"
        ]
        
        for i, instruction in enumerate(instructions):
            color = (255, 255, 100) if i == 0 else (255, 255, 255) if i == 1 else (100, 255, 100)
            text = font.render(instruction, True, color)
            screen.blit(text, (60, 430 + i * 22))
        
        if self.understanding_bar.current_value >= 80:
            ready_text = "Ready for Dragon Battle! Press SPACE"
            ready_surface = pygame.font.Font(None, 32).render(ready_text, True, (255, 255, 0))
            ready_rect = ready_surface.get_rect(center=(self.game.width // 2, 650))
            screen.blit(ready_surface, ready_rect)
    
    def _render_boss_battle(self, screen):
        """Render simplified boss battle"""
        # Dragon with HP
        dragon_rect = pygame.Rect(self.game.width // 2 - 150, 50, 300, 100)
        pygame.draw.rect(screen, (200, 50, 50), dragon_rect, border_radius=20)
        
        dragon_font = pygame.font.Font(None, 36)
        dragon_text = dragon_font.render("🐉 Derivative Dragon", True, (255, 255, 255))
        dragon_text_rect = dragon_text.get_rect(center=dragon_rect.center)
        screen.blit(dragon_text, dragon_text_rect)
        
        # HP bar
        hp_width = 300
        hp_filled = int(hp_width * self.boss_hp / self.boss_max_hp)
        hp_rect = pygame.Rect(self.game.width // 2 - 150, 170, hp_width, 20)
        pygame.draw.rect(screen, (100, 0, 0), hp_rect)
        pygame.draw.rect(screen, (255, 0, 0), (hp_rect.x, hp_rect.y, hp_filled, hp_rect.height))
        pygame.draw.rect(screen, (255, 255, 255), hp_rect, 2)
        
        # Simple questions about chain rule concepts
        questions = [
            {
                "question": "What does chain rule calculate?",
                "options": ["Weights", "Gradients", "Activations"],
                "correct": 1
            },
            {
                "question": "Gradients flow which direction?",
                "options": ["Forward", "Backward", "Both ways"],
                "correct": 1
            },
            {
                "question": "Chain rule multiplies what?",
                "options": ["Weights", "Derivatives", "Inputs"],
                "correct": 1
            }
        ]
        
        if self.current_challenge < len(questions):
            question = questions[self.current_challenge]
            
            # Question
            font = pygame.font.Font(None, 28)
            question_text = font.render(question["question"], True, (255, 255, 100))
            screen.blit(question_text, (50, 220))
            
            # Options
            option_font = pygame.font.Font(None, 24)
            for i, option in enumerate(question["options"]):
                y_pos = 270 + i * 40
                
                # Highlight selected option
                if i == self.selected_answer:
                    bg_color = (100, 150, 200)
                    text_color = (255, 255, 255)
                    border_width = 3
                else:
                    bg_color = (60, 80, 120)
                    text_color = (200, 200, 200)
                    border_width = 1
                
                # Draw option button
                option_rect = pygame.Rect(50, y_pos, 300, 35)
                pygame.draw.rect(screen, bg_color, option_rect, border_radius=8)
                pygame.draw.rect(screen, (150, 180, 220), option_rect, border_width, border_radius=8)
                
                # Draw option text
                option_text = option_font.render(f"{i+1}. {option}", True, text_color)
                text_rect = option_text.get_rect(center=option_rect.center)
                screen.blit(option_text, text_rect)
            
            # Instructions
            inst_rect = pygame.Rect(50, 420, 600, 50)
            pygame.draw.rect(screen, (40, 50, 70), inst_rect)
            pygame.draw.rect(screen, (100, 150, 200), inst_rect, 2)
            
            inst_font = pygame.font.Font(None, 20)
            inst_text = inst_font.render("Use LEFT/RIGHT arrows to select, SPACE to confirm", True, (255, 255, 100))
            screen.blit(inst_text, (60, 435))
    
    def _render_victory(self, screen):
        """Render victory screen"""
        # Animated victory title
        victory_font = pygame.font.Font(None, 72)
        glow_intensity = abs(math.sin(self.gradient_flow_animation)) * 50 + 205
        
        victory_text = victory_font.render("CHAIN RULE MASTERED!", True, (255, int(glow_intensity), 0))
        victory_rect = victory_text.get_rect(center=(self.game.width // 2, 200))
        screen.blit(victory_text, victory_rect)
        
        # Achievement
        achievement_text = "🏆 Derivative Dragon Defeated!"
        achievement_surface = pygame.font.Font(None, 36).render(achievement_text, True, (255, 255, 100))
        achievement_rect = achievement_surface.get_rect(center=(self.game.width // 2, 300))
        screen.blit(achievement_surface, achievement_rect)
    
    def _render_chain_rule_diagram(self, screen, x, y, width, height):
        """Render chain rule explanation diagram"""
        # Background
        pygame.draw.rect(screen, (40, 40, 60), (x, y, width, height), border_radius=10)
        
        # Chain rule formula
        formula_font = pygame.font.Font(None, 32)
        formula_text = "∂L/∂w = ∂L/∂y × ∂y/∂z × ∂z/∂w"
        formula_surface = formula_font.render(formula_text, True, (255, 255, 100))
        formula_rect = formula_surface.get_rect(center=(x + width // 2, y + 30))
        screen.blit(formula_surface, formula_rect)
        
        # Visual chain
        chain_y = y + 80
        box_width = 120
        box_height = 60
        spacing = 50
        
        chain_elements = ["Loss", "Output", "Hidden", "Weight"]
        colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255), (255, 255, 100)]
        
        for i, (element, color) in enumerate(zip(chain_elements, colors)):
            box_x = x + 50 + i * (box_width + spacing)
            box_rect = pygame.Rect(box_x, chain_y, box_width, box_height)
            
            pygame.draw.rect(screen, color, box_rect, border_radius=10)
            
            text = pygame.font.Font(None, 24).render(element, True, (0, 0, 0))
            text_rect = text.get_rect(center=box_rect.center)
            screen.blit(text, text_rect)
            
            # Arrow
            if i < len(chain_elements) - 1:
                arrow_start = (box_x + box_width, chain_y + box_height // 2)
                arrow_end = (box_x + box_width + spacing, chain_y + box_height // 2)
                pygame.draw.line(screen, (255, 255, 255), arrow_start, arrow_end, 3)
                
                # Arrow head
                pygame.draw.polygon(screen, (255, 255, 255), [
                    arrow_end,
                    (arrow_end[0] - 10, arrow_end[1] - 5),
                    (arrow_end[0] - 10, arrow_end[1] + 5)
                ])
    
    def _render_network_with_gradients(self, screen, x, y, width, height):
        """Render network with gradient visualization"""
        # Background
        pygame.draw.rect(screen, (30, 30, 50), (x, y, width, height), border_radius=15)
        
        # Network nodes
        node_radius = 30
        layer_spacing = width // (len(self.network_layers) + 1)
        
        for i, layer in enumerate(self.network_layers):
            node_x = x + (i + 1) * layer_spacing
            node_y = y + height // 2
            
            # Node color based on value
            intensity = min(255, int(abs(layer["value"]) * 100 + 50))
            node_color = (intensity, intensity, 255)
            
            # Draw node
            pygame.draw.circle(screen, node_color, (node_x, node_y), node_radius)
            pygame.draw.circle(screen, (255, 255, 255), (node_x, node_y), node_radius, 2)
            
            # Value text
            value_text = f"{layer['value']:.2f}"
            value_surface = pygame.font.Font(None, 20).render(value_text, True, (255, 255, 255))
            value_rect = value_surface.get_rect(center=(node_x, node_y - 5))
            screen.blit(value_surface, value_rect)
            
            # Gradient text
            grad_text = f"∇{layer['derivative']:.3f}"
            grad_surface = pygame.font.Font(None, 16).render(grad_text, True, (255, 255, 100))
            grad_rect = grad_surface.get_rect(center=(node_x, node_y + 10))
            screen.blit(grad_surface, grad_rect)
            
            # Layer name
            name_surface = pygame.font.Font(None, 18).render(layer["name"], True, (200, 200, 200))
            name_rect = name_surface.get_rect(center=(node_x, node_y - 50))
            screen.blit(name_surface, name_rect)
            
            # Connection to next layer
            if i < len(self.network_layers) - 1:
                next_x = x + (i + 2) * layer_spacing
                
                # Gradient flow animation
                flow_offset = int(math.sin(self.gradient_flow_animation + i) * 10)
                
                # Connection line
                pygame.draw.line(screen, (100, 255, 100), 
                               (node_x + node_radius, node_y), 
                               (next_x - node_radius, node_y), 3)
                
                # Weight label
                if "weight" in self.network_layers[i + 1]:
                    weight = self.network_layers[i + 1]["weight"]
                    weight_text = f"w={weight:.1f}"
                    weight_surface = pygame.font.Font(None, 18).render(weight_text, True, (255, 255, 255))
                    weight_x = (node_x + next_x) // 2
                    weight_y = node_y - 20 + flow_offset
                    weight_rect = weight_surface.get_rect(center=(weight_x, weight_y))
                    screen.blit(weight_surface, weight_rect)