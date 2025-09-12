"""
Activation Functions Challenge - Level 3: The Sigmoid Sorcerer
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

class ActivationChallenge(BaseChallenge):
    def __init__(self, game):
        super().__init__(game)
        self.story = GameStory()
        self.visualizer = NeuralNetworkVisualizer(game.width, game.height)
        self.particles = ParticleSystem()
        
        # Challenge phases
        self.phase = "intro"  # intro -> theory -> practice -> boss -> victory
        self.dialogue_box = DialogueBox(50, game.height - 200, game.width - 100, 150)
        
        # Interactive function playground
        self.selected_function = 0
        self.functions = ["ReLU", "Sigmoid", "Tanh", "Leaky ReLU", "Swish"]
        self.input_value = 0.0
        self.input_slider_pos = game.width // 2
        
        # Boss battle - Function Matching Game
        self.boss_hp = 100
        self.boss_max_hp = 100
        self.player_score = 0
        self.current_scenario = 0
        self.show_hint = False  # For collapsible hint system
        
        # Simplified scenarios with visual examples
        self.scenarios = [
            {
                "problem": "Output Layer for Yes/No Questions",
                "description": "You're building a spam detector. It should output 0 for 'not spam' and 1 for 'spam'.",
                "visual_input": 2.5,
                "correct_function": "Sigmoid",
                "explanation": "Sigmoid converts any number to 0-1 range, perfect for yes/no answers!",
                "wrong_explanation": "This function doesn't give you probabilities between 0 and 1."
            },
            {
                "problem": "Hidden Layer in Deep Network",
                "description": "You have a 10-layer network. You want fast training without gradient problems.",
                "visual_input": -1.5,
                "correct_function": "ReLU",
                "explanation": "ReLU is simple and fast - negative becomes 0, positive stays the same!",
                "wrong_explanation": "This function can slow down training in deep networks."
            },
            {
                "problem": "Some Neurons Stopped Working",
                "description": "In your ReLU network, many neurons always output 0 and stopped learning.",
                "visual_input": -2.0,
                "correct_function": "Leaky ReLU",
                "explanation": "Leaky ReLU gives tiny outputs for negatives, keeping neurons alive!",
                "wrong_explanation": "This won't fix neurons that have completely stopped learning."
            }
        ]
        
        # UI elements
        self.understanding_bar = ProgressBar(50, 50, 300, 25, 100)
        self.function_buttons = []
        self._create_function_buttons()
        
        # Animation and effects
        self.boss_shake = 0
        self.victory_particles_timer = 0
        
    def _create_function_buttons(self):
        """Create buttons for function selection"""
        button_width = 120
        button_height = 40
        start_x = 50
        start_y = 400
        
        for i, func_name in enumerate(self.functions):
            x = start_x + (i % 3) * (button_width + 20)
            y = start_y + (i // 3) * (button_height + 15)
            
            button = ModernButton(
                x, y, button_width, button_height,
                func_name, pygame.font.Font(None, 24),
                bg_color=(60, 100, 140),
                hover_color=(80, 120, 180)
            )
            self.function_buttons.append(button)
    
    def initialize(self):
        self.phase = "intro"
        self._start_intro()
    
    def _start_intro(self):
        """Start the introduction with speech"""
        intro_text = "Welcome to the Activation Peaks, brave neural architect! I am the Sigmoid Sorcerer, guardian of non-linear transformations!"
        self.dialogue_box.set_dialogue(intro_text, "Sigmoid Sorcerer")
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
                if event.key == pygame.K_LEFT:
                    self.selected_function = (self.selected_function - 1) % len(self.functions)
                elif event.key == pygame.K_RIGHT:
                    self.selected_function = (self.selected_function + 1) % len(self.functions)
                elif event.key == pygame.K_UP:
                    self.input_value = min(5.0, self.input_value + 0.2)
                    self.understanding_bar.set_value(min(100, self.understanding_bar.current_value + 2))
                elif event.key == pygame.K_DOWN:
                    self.input_value = max(-5.0, self.input_value - 0.2)
                    self.understanding_bar.set_value(min(100, self.understanding_bar.current_value + 2))
                elif event.key == pygame.K_SPACE and self.understanding_bar.current_value >= 80:
                    self.phase = "boss"
                    self._start_boss_battle()
            elif self.phase == "boss":
                # Only use LEFT/RIGHT for function selection (more intuitive)
                if event.key == pygame.K_LEFT:
                    # Map to main functions only
                    main_functions = ["ReLU", "Sigmoid", "Leaky ReLU"]
                    current_main_idx = 0
                    for i, func in enumerate(main_functions):
                        if self.selected_function == self.functions.index(func):
                            current_main_idx = i
                            break
                    current_main_idx = (current_main_idx - 1) % len(main_functions)
                    self.selected_function = self.functions.index(main_functions[current_main_idx])
                elif event.key == pygame.K_RIGHT:
                    # Map to main functions only
                    main_functions = ["ReLU", "Sigmoid", "Leaky ReLU"]
                    current_main_idx = 0
                    for i, func in enumerate(main_functions):
                        if self.selected_function == self.functions.index(func):
                            current_main_idx = i
                            break
                    current_main_idx = (current_main_idx + 1) % len(main_functions)
                    self.selected_function = self.functions.index(main_functions[current_main_idx])
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    self._check_boss_answer()
                elif event.key == pygame.K_h:  # H key to toggle hint
                    self.show_hint = not self.show_hint
            elif self.phase == "victory":
                if event.key == pygame.K_SPACE:
                    return "completed"
            
            if event.key == pygame.K_ESCAPE:
                return "exit"
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.phase == "practice":
                mouse_pos = pygame.mouse.get_pos()
                for i, button in enumerate(self.function_buttons):
                    if button.update(mouse_pos, True, 0.016):
                        self.selected_function = i
                        self.understanding_bar.set_value(min(100, self.understanding_bar.current_value + 5))
        
        return None
    
    def _advance_intro(self):
        """Advance through introduction dialogue"""
        intros = [
            "Linear functions are weak! They cannot solve complex problems like XOR.",
            "But with activation functions, we add the power of non-linearity!",
            "Each function has its purpose: ReLU for deep networks, Sigmoid for probabilities, Tanh for zero-centered outputs.",
            "Master them all, and you shall pass! Let's begin your training..."
        ]
        
        if not hasattr(self, 'intro_step'):
            self.intro_step = 0
        
        self.intro_step += 1
        
        if self.intro_step < len(intros):
            self.dialogue_box.set_dialogue(intros[self.intro_step], "Sigmoid Sorcerer")
            # Audio removed
        else:
            self.phase = "theory"
            self._start_theory()
    
    def _start_theory(self):
        """Start theory explanation"""
        theory_text = "Observe how each activation function transforms inputs. Experiment with different values!"
        self.dialogue_box.set_dialogue(theory_text, "Tensor")
        # Audio removed
    
    def _start_practice(self):
        """Start practice phase"""
        practice_text = "Now experiment! Use arrow keys to change input values and see how each function responds."
        self.dialogue_box.set_dialogue(practice_text, "Tensor")
        # Audio removed
    
    def _start_boss_battle(self):
        """Start boss battle"""
        battle_text = f"Excellent! Now face my challenge: {self.scenarios[self.current_scenario]['problem']}"
        self.dialogue_box.set_dialogue(battle_text, "Sigmoid Sorcerer")
        # Audio removed
    
    def _check_boss_answer(self):
        """Check boss battle answer"""
        scenario = self.scenarios[self.current_scenario]
        selected_func = self.functions[self.selected_function]
        
        if selected_func == scenario["correct_function"]:
            # Correct answer!
            self.boss_hp -= 20
            self.player_score += 20
            self.boss_shake = 10
            
            # Victory particles
            for _ in range(15):
                self.particles.add_particle(
                    random.randint(100, self.game.width - 100),
                    random.randint(100, 300),
                    (random.uniform(-50, 50), random.uniform(-100, -50)),
                    (0, 255, 100),
                    random.uniform(1.0, 2.0)
                )
            
            response = f"Correct! {scenario['explanation']}"
            self.dialogue_box.set_dialogue(response, "Tensor")
            # Audio removed
            
            if self.boss_hp <= 0:
                self.phase = "victory"
                victory_text = "The Sigmoid Sorcerer is defeated! You have mastered activation functions!"
                self.dialogue_box.set_dialogue(victory_text, "Tensor")
                # Audio removed
            else:
                self.current_scenario = (self.current_scenario + 1) % len(self.scenarios)
        else:
            # Wrong answer
            response = f"Not quite! {scenario['wrong_explanation']} Try again!"
            self.dialogue_box.set_dialogue(response, "Sigmoid Sorcerer")
            # Audio removed
    
    def _compute_activation(self, x, function_name):
        """Compute activation function output"""
        if function_name == "ReLU":
            return max(0, x)
        elif function_name == "Sigmoid":
            return 1 / (1 + math.exp(-x))
        elif function_name == "Tanh":
            return math.tanh(x)
        elif function_name == "Leaky ReLU":
            return x if x > 0 else 0.01 * x
        elif function_name == "Swish":
            return x / (1 + math.exp(-x))
        return x
    
    def update(self, dt):
        self.visualizer.update_animation(dt)
        self.dialogue_box.update(dt)
        self.understanding_bar.update(dt)
        self.particles.update(dt)
        
        # Update UI elements
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        
        for button in self.function_buttons:
            button.update(mouse_pos, mouse_pressed, dt)
        
        # Boss shake effect
        if self.boss_shake > 0:
            self.boss_shake -= dt * 30
        
        # Victory particles
        if self.phase == "victory":
            self.victory_particles_timer += dt
            if self.victory_particles_timer > 0.1:
                self.victory_particles_timer = 0
                self.particles.create_explosion(
                    random.randint(100, self.game.width - 100),
                    random.randint(100, 300),
                    (random.randint(100, 255), random.randint(100, 255), 0)
                )
    
    def render(self, screen):
        # Background gradient
        for y in range(self.game.height):
            color_intensity = int(20 + (y / self.game.height) * 40)
            color = (color_intensity, color_intensity + 10, color_intensity + 20)
            pygame.draw.line(screen, color, (0, y), (self.game.width, y))
        
        if self.phase in ["intro", "theory"]:
            self._render_intro_theory(screen)
        elif self.phase == "practice":
            self._render_practice(screen)
        elif self.phase == "boss":
            self._render_boss_battle(screen)
        elif self.phase == "victory":
            self._render_victory(screen)
        
        # Always render dialogue box and particles
        self.dialogue_box.render(screen, pygame.font.Font(None, 28), pygame.font.Font(None, 32))
        self.particles.render(screen)
    
    def _render_intro_theory(self, screen):
        """Render introduction and theory phase"""
        # Title
        title_font = pygame.font.Font(None, 48)
        title = title_font.render("Activation Functions", True, (255, 255, 100))
        title_rect = title.get_rect(center=(self.game.width // 2, 100))
        screen.blit(title, title_rect)
        
        # Boss character (Sigmoid Sorcerer)
        boss_rect = pygame.Rect(self.game.width // 2 - 100, 150, 200, 150)
        pygame.draw.rect(screen, (150, 50, 200), boss_rect, border_radius=20)
        
        boss_font = pygame.font.Font(None, 36)
        boss_text = boss_font.render("Sigmoid Sorcerer", True, (255, 255, 255))
        boss_text_rect = boss_text.get_rect(center=boss_rect.center)
        screen.blit(boss_text, boss_text_rect)
        
        # Show function preview
        if self.phase == "theory":
            self._render_function_preview(screen, 400, 350, 400, 200)
    
    def _render_practice(self, screen):
        """Render practice phase"""
        # Understanding progress
        self.understanding_bar.render(screen, pygame.font.Font(None, 24))
        
        progress_text = f"Understanding: {int(self.understanding_bar.current_value)}%"
        font = pygame.font.Font(None, 28)
        text = font.render(progress_text, True, (255, 255, 255))
        screen.blit(text, (360, 55))
        
        # Function buttons
        for i, button in enumerate(self.function_buttons):
            if i == self.selected_function:
                button.bg_color = (100, 150, 200)
            else:
                button.bg_color = (60, 100, 140)
            button.render(screen)
        
        # Interactive function graph
        self._render_interactive_graph(screen, 450, 100, 500, 300)
        
        # Input value display
        input_text = f"Input: {self.input_value:.2f}"
        output_value = self._compute_activation(self.input_value, self.functions[self.selected_function])
        output_text = f"Output: {output_value:.3f}"
        
        font = pygame.font.Font(None, 32)
        input_surface = font.render(input_text, True, (255, 255, 100))
        output_surface = font.render(output_text, True, (100, 255, 100))
        
        screen.blit(input_surface, (50, 300))
        screen.blit(output_surface, (50, 330))
        
        # Function formula and explanation
        self._render_function_info(screen, 50, 370, self.functions[self.selected_function])
        
        # Instructions
        if self.understanding_bar.current_value >= 80:
            ready_text = "Ready for boss battle! Press SPACE"
            ready_surface = font.render(ready_text, True, (0, 255, 0))
            ready_rect = ready_surface.get_rect(center=(self.game.width // 2, self.game.height - 250))
            screen.blit(ready_surface, ready_rect)
    
    def _render_boss_battle(self, screen):
        """Render boss battle phase with visual examples"""
        # Boss with shake effect
        boss_x = self.game.width // 2 - 150 + random.randint(-int(self.boss_shake), int(self.boss_shake))
        boss_y = 50
        boss_rect = pygame.Rect(boss_x, boss_y, 300, 100)
        pygame.draw.rect(screen, (150, 50, 200), boss_rect, border_radius=15)
        
        # Boss HP bar
        hp_bar_rect = pygame.Rect(boss_x, boss_y - 30, 300, 20)
        pygame.draw.rect(screen, (100, 0, 0), hp_bar_rect)
        hp_fill_width = int((self.boss_hp / self.boss_max_hp) * 300)
        hp_fill_rect = pygame.Rect(boss_x, boss_y - 30, hp_fill_width, 20)
        pygame.draw.rect(screen, (255, 0, 0), hp_fill_rect)
        
        # Current scenario
        scenario = self.scenarios[self.current_scenario]
        
        # Problem description with better text wrapping
        problem_font = pygame.font.Font(None, 28)
        problem_text = problem_font.render(f"Challenge: {scenario['problem']}", True, (255, 255, 100))
        screen.blit(problem_text, (50, 180))
        
        # Description with wrapping
        desc_rect = pygame.Rect(50, 210, 700, 40)
        self._render_wrapped_text(screen, scenario['description'], desc_rect, (255, 255, 255), 20)
        
        # Visual example - show what happens with the input
        visual_x = 50
        visual_y = 260
        visual_width = 300
        visual_height = 80
        
        pygame.draw.rect(screen, (40, 50, 70), (visual_x, visual_y, visual_width, visual_height))
        pygame.draw.rect(screen, (100, 150, 200), (visual_x, visual_y, visual_width, visual_height), 2)
        
        # Show input and what each function would output
        input_val = scenario['visual_input']
        example_font = pygame.font.Font(None, 18)
        
        example_title = pygame.font.Font(None, 20).render(f"Example: Input = {input_val}", True, (255, 255, 100))
        screen.blit(example_title, (visual_x + 10, visual_y + 5))
        
        # Show outputs for each function
        y_offset = 25
        for func_name in ["ReLU", "Sigmoid", "Tanh"]:
            output = self._compute_activation(input_val, func_name)
            color = (100, 255, 100) if func_name == scenario['correct_function'] else (200, 200, 200)
            output_text = example_font.render(f"{func_name}: {output:.2f}", True, color)
            screen.blit(output_text, (visual_x + 10, visual_y + y_offset))
            y_offset += 18
        
        # Function selection
        selection_text = pygame.font.Font(None, 24).render("Choose the best function:", True, (255, 255, 255))
        screen.blit(selection_text, (50, 360))
        
        # Draw function options in a grid - only show the 3 main ones for simplicity
        main_functions = ["ReLU", "Sigmoid", "Leaky ReLU"]
        button_width = 120
        button_height = 40
        start_x = 50
        start_y = 390
        
        for i, func_name in enumerate(main_functions):
            x = start_x + i * (button_width + 20)
            y = start_y
            
            # Highlight selected function
            if self.selected_function == self.functions.index(func_name):
                bg_color = (255, 100, 100)
                border_color = (255, 255, 255)
                border_width = 3
            else:
                bg_color = (60, 100, 140)
                border_color = (100, 150, 200)
                border_width = 1
            
            # Draw button
            button_rect = pygame.Rect(x, y, button_width, button_height)
            pygame.draw.rect(screen, bg_color, button_rect, border_radius=8)
            pygame.draw.rect(screen, border_color, button_rect, border_width, border_radius=8)
            
            # Draw text
            font = pygame.font.Font(None, 20)
            text = font.render(func_name, True, (255, 255, 255))
            text_rect = text.get_rect(center=button_rect.center)
            screen.blit(text, text_rect)
        
        # Instructions with hint toggle
        inst_y = 450 if not self.show_hint else 580
        inst_rect = pygame.Rect(50, inst_y, 700, 60)
        pygame.draw.rect(screen, (40, 50, 70), inst_rect)
        pygame.draw.rect(screen, (100, 150, 200), inst_rect, 2)
        
        inst_font = pygame.font.Font(None, 18)
        inst_text = inst_font.render("Controls: LEFT/RIGHT to select, SPACE to confirm, H for hint", True, (255, 255, 100))
        screen.blit(inst_text, (60, inst_y + 10))
        
        hint_text = inst_font.render("Hint: Look at the example outputs above to see which works best!", True, (200, 255, 200))
        screen.blit(hint_text, (60, inst_y + 30))
        
        # Collapsible hint with activation function diagrams
        if self.show_hint:
            hint_rect = pygame.Rect(50, 450, 700, 120)
            pygame.draw.rect(screen, (25, 35, 50), hint_rect)
            pygame.draw.rect(screen, (150, 200, 255), hint_rect, 2)
            
            # Title
            hint_title = pygame.font.Font(None, 22).render("Activation Function Reference (Press H to hide)", True, (255, 255, 100))
            screen.blit(hint_title, (60, 460))
            
            # Draw mini diagrams for each function
            diagram_width = 200
            diagram_height = 80
            main_functions = ["ReLU", "Sigmoid", "Leaky ReLU"]
            
            for i, func_name in enumerate(main_functions):
                diagram_x = 60 + i * (diagram_width + 20)
                diagram_y = 480
                self._render_activation_diagram(screen, diagram_x, diagram_y, diagram_width, diagram_height, func_name)
    
    def _render_victory(self, screen):
        """Render victory screen"""
        # Victory title with glow effect
        victory_font = pygame.font.Font(None, 72)
        victory_text = victory_font.render("VICTORY!", True, (255, 255, 0))
        
        # Glow effect
        for offset in [(2, 2), (-2, -2), (2, -2), (-2, 2)]:
            glow_text = victory_font.render("VICTORY!", True, (255, 200, 0))
            glow_rect = glow_text.get_rect(center=(self.game.width // 2 + offset[0], 200 + offset[1]))
            screen.blit(glow_text, glow_rect)
        
        victory_rect = victory_text.get_rect(center=(self.game.width // 2, 200))
        screen.blit(victory_text, victory_rect)
        
        # Score
        score_text = f"Final Score: {self.player_score}/100"
        score_surface = pygame.font.Font(None, 36).render(score_text, True, (100, 255, 100))
        score_rect = score_surface.get_rect(center=(self.game.width // 2, 300))
        screen.blit(score_surface, score_rect)
    
    def _render_function_preview(self, screen, x, y, width, height):
        """Render function preview graph"""
        # Background
        pygame.draw.rect(screen, (40, 40, 60), (x, y, width, height), border_radius=10)
        
        # Draw all activation functions
        colors = [(255, 100, 100), (100, 255, 100), (100, 100, 255), (255, 255, 100), (255, 100, 255)]
        
        for i, func_name in enumerate(self.functions):
            points = []
            for px in range(width):
                input_val = (px / width) * 10 - 5  # Range from -5 to 5
                output_val = self._compute_activation(input_val, func_name)
                
                # Scale output to fit in graph
                py = y + height - int((output_val + 2) / 4 * height)  # Assuming output range roughly -2 to 2
                py = max(y, min(y + height, py))
                
                points.append((x + px, py))
            
            if len(points) > 1:
                pygame.draw.lines(screen, colors[i], False, points, 2)
        
        # Legend
        legend_y = y + 10
        for i, func_name in enumerate(self.functions):
            legend_text = pygame.font.Font(None, 20).render(func_name, True, colors[i])
            screen.blit(legend_text, (x + 10, legend_y + i * 25))
    
    def _render_interactive_graph(self, screen, x, y, width, height):
        """Render interactive function graph"""
        # Background
        pygame.draw.rect(screen, (30, 30, 50), (x, y, width, height), border_radius=10)
        pygame.draw.rect(screen, (100, 100, 100), (x, y, width, height), 2, border_radius=10)
        
        # Axes
        center_x = x + width // 2
        center_y = y + height // 2
        pygame.draw.line(screen, (150, 150, 150), (x + 20, center_y), (x + width - 20, center_y), 1)
        pygame.draw.line(screen, (150, 150, 150), (center_x, y + 20), (center_x, y + height - 20), 1)
        
        # Current function curve
        func_name = self.functions[self.selected_function]
        points = []
        
        for px in range(width - 40):
            input_val = (px / (width - 40)) * 10 - 5  # Range from -5 to 5
            output_val = self._compute_activation(input_val, func_name)
            
            # Scale to graph
            graph_x = x + 20 + px
            graph_y = center_y - int(output_val * 50)  # Scale output
            graph_y = max(y + 20, min(y + height - 20, graph_y))
            
            points.append((graph_x, graph_y))
        
        if len(points) > 1:
            pygame.draw.lines(screen, (0, 255, 255), False, points, 3)
        
        # Current input/output point
        input_x = center_x + int(self.input_value * 50)
        output_val = self._compute_activation(self.input_value, func_name)
        output_y = center_y - int(output_val * 50)
        
        # Clamp to graph bounds
        input_x = max(x + 20, min(x + width - 20, input_x))
        output_y = max(y + 20, min(y + height - 20, output_y))
        
        # Draw current point
        pygame.draw.circle(screen, (255, 255, 0), (input_x, output_y), 8)
        pygame.draw.circle(screen, (255, 255, 255), (input_x, output_y), 8, 2)
        
        # Function name
        title = pygame.font.Font(None, 32).render(func_name, True, (255, 255, 255))
        screen.blit(title, (x + 10, y + 10))
        
        # Add axis labels and values
        axis_font = pygame.font.Font(None, 18)
        
        # X-axis labels (input values)
        x_values = [-4, -2, 0, 2, 4]
        for val in x_values:
            label_x = center_x + int(val * 50)
            if x + 20 <= label_x <= x + width - 20:
                # Tick mark
                pygame.draw.line(screen, (150, 150, 150), (label_x, center_y - 5), (label_x, center_y + 5), 1)
                # Label
                label_text = axis_font.render(str(val), True, (200, 200, 200))
                label_rect = label_text.get_rect(center=(label_x, center_y + 15))
                screen.blit(label_text, label_rect)
        
        # Y-axis labels (output values)
        y_values = [-2, -1, 0, 1, 2]
        for val in y_values:
            label_y = center_y - int(val * 50)
            if y + 20 <= label_y <= y + height - 20:
                # Tick mark
                pygame.draw.line(screen, (150, 150, 150), (center_x - 5, label_y), (center_x + 5, label_y), 1)
                # Label
                label_text = axis_font.render(str(val), True, (200, 200, 200))
                label_rect = label_text.get_rect(center=(center_x - 15, label_y))
                screen.blit(label_text, label_rect)
        
        # Axis titles
        x_axis_title = pygame.font.Font(None, 20).render("Input (x)", True, (255, 255, 255))
        x_title_rect = x_axis_title.get_rect(center=(center_x, y + height - 5))
        screen.blit(x_axis_title, x_title_rect)
        
        # Y-axis title (rotated)
        y_axis_title = pygame.font.Font(None, 20).render("Output f(x)", True, (255, 255, 255))
        # Rotate and position y-axis title
        rotated_y_title = pygame.transform.rotate(y_axis_title, 90)
        y_title_rect = rotated_y_title.get_rect(center=(x + 10, center_y))
        screen.blit(rotated_y_title, y_title_rect)
    
    def _render_activation_diagram(self, screen, x, y, width, height, function_name):
        """Render a small diagram showing how the activation function works"""
        # Background
        pygame.draw.rect(screen, (30, 40, 60), (x, y, width, height))
        pygame.draw.rect(screen, (100, 150, 200), (x, y, width, height), 2)
        
        # Title
        title_font = pygame.font.Font(None, 20)
        title = title_font.render(f"{function_name} Function", True, (255, 255, 100))
        screen.blit(title, (x + 10, y + 5))
        
        # Draw simple graph
        graph_x = x + 10
        graph_y = y + 30
        graph_w = width - 20
        graph_h = height - 60
        
        # Axes
        center_x = graph_x + graph_w // 2
        center_y = graph_y + graph_h // 2
        pygame.draw.line(screen, (150, 150, 150), (graph_x, center_y), (graph_x + graph_w, center_y), 1)  # X-axis
        pygame.draw.line(screen, (150, 150, 150), (center_x, graph_y), (center_x, graph_y + graph_h), 1)  # Y-axis
        
        # Draw function curve
        points = []
        for i in range(graph_w):
            input_val = (i - graph_w // 2) / 20.0  # Scale input
            output_val = self._compute_activation(input_val, function_name)
            
            # Scale output to fit graph
            screen_x = graph_x + i
            screen_y = center_y - int(output_val * 20)  # Scale output
            screen_y = max(graph_y, min(graph_y + graph_h, screen_y))  # Clamp
            
            points.append((screen_x, screen_y))
        
        if len(points) > 1:
            pygame.draw.lines(screen, (0, 255, 255), False, points, 2)
        
        # Add key points and labels
        key_font = pygame.font.Font(None, 16)
        if function_name == "ReLU":
            key_text = key_font.render("f(x) = max(0, x)", True, (255, 255, 255))
            screen.blit(key_text, (x + 10, y + height - 20))
        elif function_name == "Sigmoid":
            key_text = key_font.render("f(x) = 1/(1+e^-x)", True, (255, 255, 255))
            screen.blit(key_text, (x + 10, y + height - 20))
        elif function_name == "Leaky ReLU":
            key_text = key_font.render("f(x) = max(0.01x, x)", True, (255, 255, 255))
            screen.blit(key_text, (x + 10, y + height - 20))

    def _render_wrapped_text(self, screen, text, rect, color, font_size=18):
        """Render text with proper wrapping inside a rectangle"""
        font = pygame.font.Font(None, font_size)
        words = text.split(' ')
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            if font.size(test_line)[0] <= rect.width - 20:  # Leave 10px margin on each side
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        # Render lines
        y_offset = 0
        for line in lines:
            if y_offset + font_size > rect.height - 10:  # Stop if we exceed the box
                break
            text_surface = font.render(line, True, color)
            screen.blit(text_surface, (rect.x + 10, rect.y + y_offset + 5))
            y_offset += font_size + 2

    def _render_function_info(self, screen, x, y, function_name):
        """Render function formula and explanation with proper text wrapping"""
        # Simplified function info for better learning
        function_info = {
            "ReLU": {
                "formula": "f(x) = max(0, x)",
                "simple_explanation": "ReLU is like a gate - it lets positive values through unchanged, but blocks negative values (sets them to 0). Great for deep networks!",
                "use_case": "Best for: Hidden layers in deep networks"
            },
            "Sigmoid": {
                "formula": "f(x) = 1 / (1 + e^(-x))",
                "simple_explanation": "Sigmoid squashes any input to a value between 0 and 1. Perfect when you need probabilities!",
                "use_case": "Best for: Binary classification output"
            },
            "Tanh": {
                "formula": "f(x) = tanh(x)",
                "simple_explanation": "Tanh is like sigmoid but outputs between -1 and 1. The zero-centered output helps with training.",
                "use_case": "Best for: Hidden layers when you want zero-centered outputs"
            },
            "Leaky ReLU": {
                "formula": "f(x) = max(0.01x, x)",
                "simple_explanation": "Like ReLU but allows tiny negative values (0.01x). Prevents neurons from 'dying' completely.",
                "use_case": "Best for: When regular ReLU neurons stop learning"
            },
            "Swish": {
                "formula": "f(x) = x * sigmoid(x)",
                "simple_explanation": "A smooth, modern activation that often works better than ReLU. Self-gating means it can control its own output.",
                "use_case": "Best for: Modern deep networks, often outperforms ReLU"
            }
        }
        
        if function_name not in function_info:
            return
        
        info = function_info[function_name]
        
        # Background for info panel - make it larger for better text fit
        panel_width = 400
        panel_height = 180
        panel_rect = pygame.Rect(x, y, panel_width, panel_height)
        pygame.draw.rect(screen, (25, 35, 50), panel_rect)
        pygame.draw.rect(screen, (100, 150, 200), panel_rect, 2)
        
        # Formula section
        formula_title = pygame.font.Font(None, 22).render("Formula:", True, (255, 255, 100))
        screen.blit(formula_title, (x + 10, y + 10))
        
        # Render formula with better formatting
        formula_font = pygame.font.Font(None, 20)
        formula_text = formula_font.render(info["formula"], True, (255, 255, 255))
        screen.blit(formula_text, (x + 10, y + 30))
        
        # Explanation section
        explanation_title = pygame.font.Font(None, 22).render("What it does:", True, (255, 200, 100))
        screen.blit(explanation_title, (x + 10, y + 60))
        
        # Render wrapped explanation
        explanation_rect = pygame.Rect(x, y + 80, panel_width, 60)
        self._render_wrapped_text(screen, info["simple_explanation"], explanation_rect, (220, 220, 220), 16)
        
        # Use case
        use_case_title = pygame.font.Font(None, 20).render(info["use_case"], True, (100, 255, 150))
        screen.blit(use_case_title, (x + 10, y + 150))