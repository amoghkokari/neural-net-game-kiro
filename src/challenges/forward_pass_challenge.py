"""
Forward Pass Challenge - Level 6: The Flow Guardian
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
try:
    from ..ui.responsive_layout import ResponsiveLayout, ResponsiveButton, ResponsiveSlider
except ImportError:
    from ui.responsive_layout import ResponsiveLayout, ResponsiveButton, ResponsiveSlider

class ForwardPassChallenge(BaseChallenge):
    def __init__(self, game):
        super().__init__(game)
        self.layout = ResponsiveLayout(game.width, game.height)
        self.story = GameStory()
        self.visualizer = NeuralNetworkVisualizer(game.width, game.height)
        self.particles = ParticleSystem()
        
        # Challenge phases
        self.phase = "intro"
        
        # Create responsive dialogue box - positioned at bottom to avoid overlap with questions
        dialogue_rect = self.layout.get_rect(0.05, 0.82, 0.9, 0.16)
        self.dialogue_box = DialogueBox(dialogue_rect.x, dialogue_rect.y, dialogue_rect.width, dialogue_rect.height)
        
        # Question system
        self.current_question = None
        self.feedback_text = ""
        self.feedback_timer = 0
        self.questions = [
            {
                'question': 'What happens in the first step of forward propagation?',
                'options': [
                    'Apply activation function',
                    'Multiply inputs by weights',
                    'Add bias terms',
                    'Calculate gradients'
                ],
                'correct': 2
            },
            {
                'question': 'What is the purpose of the bias term?',
                'options': [
                    'Speed up training',
                    'Shift the activation function',
                    'Reduce overfitting',
                    'Normalize inputs'
                ],
                'correct': 2
            },
            {
                'question': 'Which activation function outputs values between 0 and 1?',
                'options': [
                    'ReLU',
                    'Sigmoid',
                    'Tanh',
                    'Linear'
                ],
                'correct': 2
            },
            {
                'question': 'What does softmax do in the output layer?',
                'options': [
                    'Speeds up computation',
                    'Prevents overfitting',
                    'Creates probability distribution',
                    'Reduces dimensions'
                ],
                'correct': 3
            }
        ]
        self.question_index = 0
        
        # Multi-layer network
        self.network = {
            'layers': [
                {'size': 3, 'name': 'Input', 'activations': [1.0, 0.5, -0.3]},
                {'size': 4, 'name': 'Hidden 1', 'activations': [0.0, 0.0, 0.0, 0.0], 'activation_func': 'relu'},
                {'size': 3, 'name': 'Hidden 2', 'activations': [0.0, 0.0, 0.0], 'activation_func': 'sigmoid'},
                {'size': 2, 'name': 'Output', 'activations': [0.0, 0.0], 'activation_func': 'softmax'}
            ],
            'weights': [
                np.random.randn(3, 4) * 0.5,  # Input to Hidden 1
                np.random.randn(4, 3) * 0.5,  # Hidden 1 to Hidden 2
                np.random.randn(3, 2) * 0.5   # Hidden 2 to Output
            ],
            'biases': [
                np.random.randn(4) * 0.1,
                np.random.randn(3) * 0.1,
                np.random.randn(2) * 0.1
            ]
        }
        
        # Animation and flow visualization
        self.data_flow_particles = []
        self.flow_speed = 2.0
        self.current_layer_processing = -1
        self.processing_timer = 0
        
        # Boss battle - Forward pass race
        self.boss_hp = 100
        self.boss_max_hp = 100
        self.player_speed = 1.0
        self.boss_speed = 0.8
        self.race_progress = 0
        self.boss_progress = 0
        
        # Interactive elements
        self.selected_weight = None
        self.selected_connection = None
        self.weight_adjustment_mode = False
        self.dragging = False
        self.drag_start_pos = None
        
        # UI elements
        self.understanding_bar = ProgressBar(50, 50, 300, 25, 100)
        self.speed_bar = ProgressBar(400, 50, 200, 25, 100)
        
        # Game mechanics
        self.perfect_passes = 0
        self.total_passes = 0
        self.accuracy_bonus = 1.0
        
        # Forward propagation understanding challenge
        self.current_step = 0  # Which step of forward pass we're on
        self.max_steps = 4  # Input -> Hidden1 -> Hidden2 -> Output
        self.step_names = ["Input Layer", "Hidden Layer 1", "Hidden Layer 2", "Output Layer"]
        self.auto_advance = False
        self.step_timer = 0.0
        self.step_duration = 2.0
        
        # Challenge mechanics - focus on understanding, not precision
        self.understanding_points = 0
        self.max_understanding = 100
        self.questions_asked = 0
        self.correct_answers = 0
        
        # Interactive prediction game
        self.prediction_mode = False
        self.predicted_values = {}
        self.show_predictions = False
        self.target_output = [0.8, 0.2]  # Target values for training
        
        # Step-by-step calculation display
        self.show_calculations = True
        self.current_calculation = ""
        
        # Hint system
        self.show_hint = False
        
        # Time pressure mechanics
        self.time_pressure = False
        self.current_time = 0.0
        self.time_limit = 3.0
        self.question_start_time = 0.0
        self.question_timed_out = False
        
    def initialize(self):
        self.phase = "intro"
        self._start_intro()
    
    def _start_intro(self):
        """Epic Flow Guardian introduction"""
        intro_text = "I am the Flow Guardian! Master of information flow through neural networks! Can you match my speed in forward propagation?"
        self.dialogue_box.set_dialogue(intro_text, "Flow Guardian")
        # Audio removed
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.phase == "intro":
                if event.key == pygame.K_f and self.dialogue_box.is_complete():
                    self._advance_intro()
            elif self.phase == "theory":
                if event.key == pygame.K_f:
                    self.phase = "practice"
                    self._start_practice()
            elif self.phase == "practice":
                if event.key == pygame.K_f:
                    if self.understanding_points >= 80:
                        self.phase = "boss"
                        self._start_boss_battle()
                    else:
                        self._step_forward_pass()
                elif event.key == pygame.K_r:
                    self._reset_forward_pass()
                elif event.key == pygame.K_p:
                    self._start_prediction_game()
                elif event.key == pygame.K_c:
                    self.show_calculations = not self.show_calculations
                elif event.key == pygame.K_a:
                    self.auto_advance = not self.auto_advance
                elif event.key == pygame.K_1:
                    self._answer_question(1)
                elif event.key == pygame.K_2:
                    self._answer_question(2)
                elif event.key == pygame.K_3:
                    self._answer_question(3)
                elif event.key == pygame.K_4:
                    self._answer_question(4)
            elif self.phase == "boss":
                if event.key == pygame.K_f:
                    self._boss_forward_pass()
                elif event.key == pygame.K_h:
                    self.show_hint = not self.show_hint
                elif event.key == pygame.K_1:
                    self._answer_boss_question(1)
                elif event.key == pygame.K_2:
                    self._answer_boss_question(2)
                elif event.key == pygame.K_3:
                    self._answer_boss_question(3)
                elif event.key == pygame.K_4:
                    self._answer_boss_question(4)
            elif self.phase == "victory":
                if event.key == pygame.K_f:
                    return "completed"
                elif event.key == pygame.K_ESCAPE:
                    return "exit"
            elif self.phase == "defeat":
                if event.key == pygame.K_r:
                    self._retry_boss_battle()
                elif event.key == pygame.K_ESCAPE:
                    return "exit"
            
            if event.key == pygame.K_ESCAPE:
                return "exit"
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.phase in ["practice", "boss"]:
                self._handle_mouse_down(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.phase in ["practice", "boss"]:
                self._handle_mouse_up(event.pos)
        elif event.type == pygame.MOUSEMOTION:
            if self.phase in ["practice", "boss"]:
                self._handle_mouse_motion(event.pos)
        
        return None
    
    def _advance_intro(self):
        """Advance through introduction"""
        intros = [
            "Forward propagation is the heartbeat of neural networks! Data flows from input to output.",
            "Each layer transforms the data: z = Wx + b, then a = activation(z)",
            "Layer by layer, simple inputs become complex representations!",
            "But speed matters! In real networks, millions of forward passes happen per second!"
        ]
        
        if not hasattr(self, 'intro_step'):
            self.intro_step = 0
        
        self.intro_step += 1
        
        if self.intro_step < len(intros):
            self.dialogue_box.set_dialogue(intros[self.intro_step], "Flow Guardian")
            # Audio removed
        else:
            self.phase = "theory"
            self._start_theory()
    
    def _start_theory(self):
        """Start theory explanation"""
        theory_text = "Watch the data flow! Each neuron receives inputs, applies weights, adds bias, then activates."
        self.dialogue_box.set_dialogue(theory_text, "Tensor")
        # Audio removed
    
    def _start_practice(self):
        """Start practice phase"""
        practice_text = "Practice time! Press F for forward pass, R to randomize inputs, W to adjust weights!"
        self.dialogue_box.set_dialogue(practice_text, "Tensor")
        # Audio removed
    
    def _start_boss_battle(self):
        """Start boss battle"""
        battle_text = "Now we race! Execute forward passes faster than me to win! This is about speed and understanding the flow of data through the network!"
        self.dialogue_box.set_dialogue(battle_text, "Flow Guardian")
        # Audio removed
    
    def _step_forward_pass(self):
        """Execute one step of forward pass for educational purposes"""
        if self.current_step >= self.max_steps:
            self._reset_forward_pass()
            return
        
        self.total_passes += 1
        
        if self.current_step == 0:
            # Starting fresh - clear previous calculations
            self.data_flow_particles = []
            self.current_calculation = "Starting forward pass with input values"
            self._ask_layer_question()
        else:
            # Execute calculation for current step
            layer_idx = self.current_step - 1
            self._calculate_layer_step(layer_idx)
        
        self.current_step += 1
        self.current_layer_processing = self.current_step - 1
        
        # Create flow particles for this step
        self._create_step_particles()
        
        # Award understanding points for completing steps
        self.understanding_points += 5
        self.understanding_bar.set_value(min(100, self.understanding_points))
    
    def _calculate_layer_step(self, layer_idx):
        """Calculate one layer step and show the math"""
        if layer_idx >= len(self.network['weights']):
            return
        
        # Get current layer activations
        current_activations = np.array(self.network['layers'][layer_idx]['activations'])
        
        # Get weights and biases
        weights = self.network['weights'][layer_idx]
        biases = self.network['biases'][layer_idx]
        
        # Show the calculation step by step
        layer_name = self.network['layers'][layer_idx]['name']
        next_layer_name = self.network['layers'][layer_idx + 1]['name']
        
        self.current_calculation = f"Computing {layer_name} → {next_layer_name}:"
        
        # Compute weighted sum
        z = np.dot(current_activations, weights) + biases
        
        # Apply activation function
        next_layer = self.network['layers'][layer_idx + 1]
        if next_layer['activation_func'] == 'relu':
            activations = np.maximum(0, z)
            self.current_calculation += f"\nz = Wx + b, then ReLU(z) = max(0, z)"
        elif next_layer['activation_func'] == 'sigmoid':
            activations = 1 / (1 + np.exp(-np.clip(z, -500, 500)))
            self.current_calculation += f"\nz = Wx + b, then σ(z) = 1/(1+e^(-z))"
        elif next_layer['activation_func'] == 'softmax':
            exp_z = np.exp(z - np.max(z))
            activations = exp_z / np.sum(exp_z)
            self.current_calculation += f"\nz = Wx + b, then softmax(z) = e^z / Σe^z"
        else:
            activations = z
            self.current_calculation += f"\nz = Wx + b (linear activation)"
        
        # Update layer activations
        next_layer['activations'] = activations.tolist()
    
    def _execute_forward_pass(self):
        """Execute a complete forward pass through the network"""
        # Perform forward propagation through all layers
        for layer_idx in range(len(self.network['weights'])):
            # Get current layer activations
            current_activations = np.array(self.network['layers'][layer_idx]['activations'])
            
            # Matrix multiplication with weights and add bias
            weighted_sum = np.dot(current_activations, self.network['weights'][layer_idx]) + self.network['biases'][layer_idx]
            
            # Apply activation function
            next_layer = self.network['layers'][layer_idx + 1]
            if next_layer['activation_func'] == 'relu':
                activations = np.maximum(0, weighted_sum)
            elif next_layer['activation_func'] == 'sigmoid':
                activations = 1 / (1 + np.exp(-np.clip(weighted_sum, -500, 500)))
            elif next_layer['activation_func'] == 'softmax':
                exp_vals = np.exp(weighted_sum - np.max(weighted_sum))
                activations = exp_vals / np.sum(exp_vals)
            else:
                activations = weighted_sum
            
            # Update next layer activations
            self.network['layers'][layer_idx + 1]['activations'] = activations.tolist()
        
        # Update stats
        self.total_passes += 1
        
        # Calculate accuracy (simple check against target)
        output_activations = self.network['layers'][-1]['activations']
        if len(output_activations) >= 2 and len(self.target_output) >= 2:
            error = sum((a - t)**2 for a, t in zip(output_activations, self.target_output))
            if error < 0.1:  # Close enough to target
                self.perfect_passes += 1
                self.accuracy_bonus = min(2.0, self.accuracy_bonus + 0.1)
        
        # Reset current time for time pressure
        self.current_time = 0.0
    
    def _reset_forward_pass(self):
        """Reset to beginning of forward pass"""
        self.current_step = 0
        self.current_layer_processing = -1
        
        # Reset to original input values
        self.network['layers'][0]['activations'] = [1.0, 0.5, -0.3]
        
        # Clear other layers
        for layer in self.network['layers'][1:]:
            layer['activations'] = [0.0] * layer['size']
        
        self.current_calculation = "Ready to start forward pass"
        self.data_flow_particles = []
    
    def _start_prediction_game(self):
        """Start prediction mini-game"""
        self.prediction_mode = not self.prediction_mode
        if self.prediction_mode:
            self._reset_forward_pass()
            self.current_calculation = "Prediction Mode: Try to predict the next layer's values!"
    
    def _ask_layer_question(self):
        """Ask a question about the current layer"""
        # Show next question if available and no current question
        if not self.current_question and self.question_index < len(self.questions):
            self._show_next_question()
    
    def _answer_question(self, answer_num):
        """Handle question answers"""
        if not self.current_question:
            return
        
        self.questions_asked += 1
        
        # Check if answer is correct
        if answer_num == self.current_question['correct']:
            self.correct_answers += 1
            self.understanding_points += 15
            feedback = "✅ Correct!"
        else:
            self.understanding_points += 5  # Small points for trying
            correct_answer = self.current_question['options'][self.current_question['correct'] - 1]
            feedback = f"❌ Wrong. Correct answer: {correct_answer}"
        
        # Update progress bar
        self.understanding_bar.set_value(min(100, self.understanding_points))
        
        # Show feedback briefly
        self.feedback_text = feedback
        self.feedback_timer = 2.0
        
        # Clear current question
        self.current_question = None
    
    def _show_next_question(self):
        """Show the next question"""
        if self.question_index < len(self.questions):
            self.current_question = self.questions[self.question_index]
            self.question_index += 1
    
    def _create_flow_particles(self):
        """Create particles to visualize data flow"""
        layer_positions = self._get_layer_positions()
        
        for layer_idx in range(len(layer_positions) - 1):
            start_positions = layer_positions[layer_idx]
            end_positions = layer_positions[layer_idx + 1]
            
            for start_pos in start_positions:
                for end_pos in end_positions:
                    # Create particle
                    particle = {
                        'start_pos': start_pos,
                        'end_pos': end_pos,
                        'current_pos': list(start_pos),
                        'progress': 0.0,
                        'layer': layer_idx,
                        'lifetime': 1.0,
                        'max_lifetime': 1.0
                    }
                    self.data_flow_particles.append(particle)
    
    def _get_layer_positions(self):
        """Get screen positions for each layer's neurons"""
        positions = []
        layer_spacing = 180
        start_x = 150
        
        for layer_idx, layer in enumerate(self.network['layers']):
            layer_x = start_x + layer_idx * layer_spacing
            layer_positions = []
            
            # Adjust vertical spacing based on layer size - more compact
            neuron_spacing = min(45, 180 // max(1, layer['size']))
            start_y = 220 - (layer['size'] - 1) * neuron_spacing // 2
            
            for neuron_idx in range(layer['size']):
                neuron_y = start_y + neuron_idx * neuron_spacing
                layer_positions.append((layer_x, neuron_y))
            
            positions.append(layer_positions)
        
        return positions
    
    def _create_step_particles(self):
        """Create particles for the current step"""
        if self.current_step <= 0 or self.current_step > len(self.network['layers']):
            return
        
        layer_positions = self._get_layer_positions()
        
        # Create particles from previous layer to current layer
        if self.current_step > 1:
            start_positions = layer_positions[self.current_step - 2]
            end_positions = layer_positions[self.current_step - 1]
            
            for start_pos in start_positions:
                for end_pos in end_positions:
                    particle = {
                        'start_pos': start_pos,
                        'end_pos': end_pos,
                        'current_pos': list(start_pos),
                        'progress': 0.0,
                        'layer': self.current_step - 2,
                        'lifetime': 2.0,
                        'max_lifetime': 2.0
                    }
                    self.data_flow_particles.append(particle)
    
    def _increase_difficulty(self):
        """Increase challenge difficulty"""
        self.noise_level = min(0.3, self.noise_level + 0.05)
        self.weight_decay = min(0.02, self.weight_decay + 0.005)
        self.output_tolerance = max(0.1, self.output_tolerance - 0.02)
        
        # Enable time pressure after some difficulty increases
        if self.noise_level > 0.1:
            self.time_pressure = True
            self.time_limit = max(1.5, self.time_limit - 0.2)
        
        # Randomize target occasionally
        if random.random() < 0.3:
            self.target_output = [random.uniform(0.2, 0.8), random.uniform(0.2, 0.8)]
            # Normalize to sum to 1 for softmax
            total = sum(self.target_output)
            self.target_output = [x / total for x in self.target_output]
    
    def _randomize_inputs(self):
        """Randomize input values"""
        for i in range(len(self.network['layers'][0]['activations'])):
            self.network['layers'][0]['activations'][i] = random.uniform(-2, 2)
    
    def _handle_mouse_down(self, pos):
        """Handle mouse down for weight selection and dragging"""
        self.selected_connection = self._find_connection_at_pos(pos)
        if self.selected_connection:
            self.dragging = True
            self.drag_start_pos = pos
    
    def _handle_mouse_up(self, pos):
        """Handle mouse up"""
        self.dragging = False
        self.drag_start_pos = None
    
    def _handle_mouse_motion(self, pos):
        """Handle mouse motion for weight adjustment"""
        if self.dragging and self.selected_connection and self.drag_start_pos:
            # Calculate weight change based on vertical mouse movement
            delta_y = pos[1] - self.drag_start_pos[1]
            weight_change = -delta_y * 0.01  # Negative because up should increase weight
            
            layer_idx, from_idx, to_idx = self.selected_connection
            self.network['weights'][layer_idx][from_idx][to_idx] += weight_change
            self.network['weights'][layer_idx][from_idx][to_idx] = np.clip(
                self.network['weights'][layer_idx][from_idx][to_idx], -3, 3
            )
            
            self.drag_start_pos = pos
    
    def _find_connection_at_pos(self, pos):
        """Find which connection is at the given position"""
        layer_positions = self._get_layer_positions()
        
        for layer_idx in range(len(self.network['weights'])):
            start_positions = layer_positions[layer_idx]
            end_positions = layer_positions[layer_idx + 1]
            
            for from_idx, start_pos in enumerate(start_positions):
                for to_idx, end_pos in enumerate(end_positions):
                    # Check if mouse is near this connection line
                    if self._point_near_line(pos, start_pos, end_pos, 15):
                        return (layer_idx, from_idx, to_idx)
        return None
    
    def _point_near_line(self, point, line_start, line_end, threshold):
        """Check if a point is near a line within threshold distance"""
        x0, y0 = point
        x1, y1 = line_start
        x2, y2 = line_end
        
        # Calculate distance from point to line
        A = x0 - x1
        B = y0 - y1
        C = x2 - x1
        D = y2 - y1
        
        dot = A * C + B * D
        len_sq = C * C + D * D
        
        if len_sq == 0:
            return False
        
        param = dot / len_sq
        
        if param < 0:
            xx, yy = x1, y1
        elif param > 1:
            xx, yy = x2, y2
        else:
            xx = x1 + param * C
            yy = y1 + param * D
        
        dx = x0 - xx
        dy = y0 - yy
        distance = math.sqrt(dx * dx + dy * dy)
        
        return distance <= threshold
    
    def _adjust_selected_weight(self, delta):
        """Adjust selected weight"""
        if self.selected_connection:
            layer_idx, from_idx, to_idx = self.selected_connection
            self.network['weights'][layer_idx][from_idx][to_idx] += delta
            self.network['weights'][layer_idx][from_idx][to_idx] = np.clip(
                self.network['weights'][layer_idx][from_idx][to_idx], -3, 3
            )
    
    def _render_current_question(self, screen):
        """Render the current question with options"""
        if not hasattr(self, 'current_question') or not self.current_question:
            return
        
        # Question area - positioned between network and stats to avoid overlap
        question_rect = self.layout.get_rect(0.05, 0.72, 0.9, 0.18)
        
        # Background with strong visibility
        pygame.draw.rect(screen, (20, 25, 40), question_rect, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 100), question_rect, 4, border_radius=12)
        
        # Question text with responsive sizing
        question_font_size = self.layout.get_font_size(0.025, min_size=18, max_size=28)
        question_font = pygame.font.Font(None, question_font_size)
        
        # Question title
        question_title = question_font.render("❓ Question:", True, (255, 255, 100))
        screen.blit(question_title, (question_rect.x + 15, question_rect.y + 10))
        
        # Question text - wrap if too long
        question_text = self.current_question.get('question', '')
        if len(question_text) > 60:  # If text is too long, wrap it
            words = question_text.split()
            line1 = ' '.join(words[:len(words)//2])
            line2 = ' '.join(words[len(words)//2:])
            
            question_surface1 = question_font.render(line1, True, (255, 255, 255))
            question_surface2 = question_font.render(line2, True, (255, 255, 255))
            screen.blit(question_surface1, (question_rect.x + 15, question_rect.y + 35))
            screen.blit(question_surface2, (question_rect.x + 15, question_rect.y + 55))
            options_start_y = question_rect.y + 80
        else:
            question_surface = question_font.render(question_text, True, (255, 255, 255))
            screen.blit(question_surface, (question_rect.x + 15, question_rect.y + 35))
            options_start_y = question_rect.y + 60
        
        # Options with better spacing
        options = self.current_question.get('options', [])
        option_font_size = self.layout.get_font_size(0.02, min_size=16, max_size=22)
        option_font = pygame.font.Font(None, option_font_size)
        
        for i, option in enumerate(options):
            option_text = f"{i+1}. {option}"
            option_surface = option_font.render(option_text, True, (200, 220, 255))
            screen.blit(option_surface, (question_rect.x + 30, options_start_y + i * 22))
    
    def _render_feedback(self, screen):
        """Render answer feedback"""
        if not self.feedback_text:
            return
        
        # Feedback area - center of screen
        feedback_font_size = self.layout.get_font_size(0.04, min_size=24, max_size=48)
        feedback_font = pygame.font.Font(None, feedback_font_size)
        
        # Determine color based on feedback
        if "✅" in self.feedback_text:
            color = (100, 255, 100)
        else:
            color = (255, 100, 100)
        
        feedback_surface = feedback_font.render(self.feedback_text, True, color)
        feedback_rect = feedback_surface.get_rect(center=(self.game.width // 2, self.game.height // 2))
        
        # Background for visibility
        bg_rect = feedback_rect.inflate(40, 20)
        pygame.draw.rect(screen, (40, 40, 60), bg_rect, border_radius=10)
        pygame.draw.rect(screen, color, bg_rect, 3, border_radius=10)
        
        screen.blit(feedback_surface, feedback_rect)
    
    def _render_practice_header(self, screen, header_rect):
        """Render the practice phase header"""
        header_font_size = self.layout.get_font_size(0.04, min_size=20, max_size=36)
        header_font = pygame.font.Font(None, header_font_size)
        
        # Title
        title_text = "🎯 Forward Propagation Practice"
        title_surface = header_font.render(title_text, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(header_rect.centerx, header_rect.y + 20))
        screen.blit(title_surface, title_rect)
        
        # Step indicator
        step_font_size = self.layout.get_font_size(0.025, min_size=14, max_size=24)
        step_font = pygame.font.Font(None, step_font_size)
        step_text = f"Step {self.current_step}/{self.max_steps}: {self.step_names[min(self.current_step, len(self.step_names)-1)]}"
        step_surface = step_font.render(step_text, True, (255, 255, 100))
        step_rect = step_surface.get_rect(center=(header_rect.centerx, header_rect.y + 50))
        screen.blit(step_surface, step_rect)
    
    def _render_practice_stats(self, screen, stats_rect):
        """Render practice stats in designated area"""
        # Background
        pygame.draw.rect(screen, (25, 30, 40), stats_rect, border_radius=8)
        pygame.draw.rect(screen, (100, 150, 200), stats_rect, 2, border_radius=8)
        
        # Stats font
        stats_font_size = self.layout.get_font_size(0.02, min_size=14, max_size=20)
        stats_font = pygame.font.Font(None, stats_font_size)
        
        # Compact stats in horizontal layout
        stats_text = f"Understanding: {self.understanding_points}/100 | Steps: {max(0, self.current_step-1)}/{self.max_steps-1} | Q&A: {self.correct_answers}/{self.questions_asked} | Layer: {self.step_names[min(self.current_step, len(self.step_names)-1)]}"
        
        # Split into two lines if too long
        if len(stats_text) > 80:
            line1 = f"Understanding: {self.understanding_points}/100 | Steps: {max(0, self.current_step-1)}/{self.max_steps-1}"
            line2 = f"Q&A: {self.correct_answers}/{self.questions_asked} | Layer: {self.step_names[min(self.current_step, len(self.step_names)-1)]}"
            
            line1_surface = stats_font.render(line1, True, (255, 255, 255))
            line2_surface = stats_font.render(line2, True, (200, 200, 200))
            
            screen.blit(line1_surface, (stats_rect.x + 10, stats_rect.y + 10))
            screen.blit(line2_surface, (stats_rect.x + 10, stats_rect.y + 35))
        else:
            stats_surface = stats_font.render(stats_text, True, (255, 255, 255))
            screen.blit(stats_surface, (stats_rect.x + 10, stats_rect.centery - 10))
    
    def _render_current_question_compact(self, screen, question_rect):
        """Render question in compact format within designated area"""
        if not hasattr(self, 'current_question') or not self.current_question:
            return
        
        # Background with strong visibility
        pygame.draw.rect(screen, (20, 25, 40), question_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 100), question_rect, 3, border_radius=10)
        
        # Compact font sizes
        question_font_size = self.layout.get_font_size(0.02, min_size=16, max_size=22)
        question_font = pygame.font.Font(None, question_font_size)
        option_font_size = self.layout.get_font_size(0.018, min_size=14, max_size=18)
        option_font = pygame.font.Font(None, option_font_size)
        
        # Question text - single line, truncated if needed
        question_text = self.current_question.get('question', '')
        if len(question_text) > 70:
            question_text = question_text[:67] + "..."
        
        question_surface = question_font.render(f"❓ {question_text}", True, (255, 255, 255))
        screen.blit(question_surface, (question_rect.x + 10, question_rect.y + 8))
        
        # Options in horizontal layout
        options = self.current_question.get('options', [])
        options_per_row = 2
        option_width = (question_rect.width - 30) // options_per_row
        
        for i, option in enumerate(options):
            row = i // options_per_row
            col = i % options_per_row
            
            # Truncate option if too long
            if len(option) > 25:
                option = option[:22] + "..."
            
            option_text = f"{i+1}. {option}"
            option_surface = option_font.render(option_text, True, (200, 220, 255))
            
            x = question_rect.x + 15 + col * option_width
            y = question_rect.y + 35 + row * 25
            screen.blit(option_surface, (x, y))
    
    def _render_practice_instructions(self, screen, instruction_rect):
        """Render practice instructions in designated area"""
        instruction_font_size = self.layout.get_font_size(0.025, min_size=16, max_size=24)
        instruction_font = pygame.font.Font(None, instruction_font_size)
        
        if self.understanding_points >= 80:
            instruction_text = "🎉 Ready for boss battle! Press F to face the Flow Guardian!"
            color = (100, 255, 100)
        else:
            instruction_text = "Press F to execute forward pass • Press 1-4 to answer questions"
            color = (255, 255, 100)
        
        # Background for visibility
        instruction_surface = instruction_font.render(instruction_text, True, color)
        instruction_surface_rect = instruction_surface.get_rect(center=instruction_rect.center)
        
        bg_rect = instruction_surface_rect.inflate(20, 10)
        pygame.draw.rect(screen, (40, 40, 60), bg_rect, border_radius=8)
        pygame.draw.rect(screen, color, bg_rect, 2, border_radius=8)
        
        screen.blit(instruction_surface, instruction_surface_rect)
    
    def _render_ultra_compact_question(self, screen, question_rect):
        """Render question in ultra-compact single-line format"""
        if not hasattr(self, 'current_question') or not self.current_question:
            return
        
        # Background
        pygame.draw.rect(screen, (20, 25, 40), question_rect, border_radius=5)
        pygame.draw.rect(screen, (255, 255, 100), question_rect, 2, border_radius=5)
        
        # Single line format: "Q: [question] | 1.[opt1] 2.[opt2] 3.[opt3] 4.[opt4]"
        font = pygame.font.Font(None, 16)
        
        question_text = self.current_question.get('question', '')
        if len(question_text) > 40:
            question_text = question_text[:37] + "..."
        
        options = self.current_question.get('options', [])
        options_text = " | ".join([f"{i+1}.{opt[:15]}" for i, opt in enumerate(options)])
        
        full_text = f"❓ {question_text} | {options_text}"
        
        # Truncate if still too long
        if len(full_text) > 120:
            full_text = full_text[:117] + "..."
        
        text_surface = font.render(full_text, True, (255, 255, 255))
        screen.blit(text_surface, (question_rect.x + 10, question_rect.y + 20))
    

    
    def _render_compact_question(self, screen, start_y):
        """Render question in a compact format"""
        if not hasattr(self, 'current_question') or not self.current_question:
            return
        
        question_rect = pygame.Rect(50, start_y, self.game.width - 100, 80)
        
        # Background
        pygame.draw.rect(screen, (35, 40, 55), question_rect, border_radius=8)
        pygame.draw.rect(screen, (255, 255, 100), question_rect, 2, border_radius=8)
        
        # Question text
        question_font = pygame.font.Font(None, 18)
        question_text = self.current_question.get('question', '')
        question_surface = question_font.render(f"❓ {question_text}", True, (255, 255, 255))
        screen.blit(question_surface, (question_rect.x + 10, question_rect.y + 8))
        
        # Options in horizontal layout
        option_font = pygame.font.Font(None, 16)
        options = self.current_question.get('options', [])
        
        for i, option in enumerate(options):
            option_text = f"{i+1}. {option[:20]}{'...' if len(option) > 20 else ''}"
            option_surface = option_font.render(option_text, True, (200, 220, 255))
            
            col = i % 2
            row = i // 2
            x = question_rect.x + 15 + col * 400
            y = question_rect.y + 35 + row * 18
            
            screen.blit(option_surface, (x, y))
    
    def _render_center_feedback(self, screen):
        """Render feedback in center of screen"""
        if not self.feedback_text:
            return
        
        # Center overlay
        feedback_rect = pygame.Rect(200, 250, 600, 100)
        pygame.draw.rect(screen, (40, 45, 60), feedback_rect, border_radius=10)
        
        # Border color based on feedback type
        border_color = (100, 255, 100) if "✅" in self.feedback_text else (255, 100, 100)
        pygame.draw.rect(screen, border_color, feedback_rect, 3, border_radius=10)
        
        # Text
        font = pygame.font.Font(None, 24)
        text_surface = font.render(self.feedback_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=feedback_rect.center)
        screen.blit(text_surface, text_rect)
    
    def _render_feedback_positioned(self, screen, feedback_rect):
        """Render feedback in a specific position to avoid overlaps"""
        if not self.feedback_text:
            return
        
        # Background
        pygame.draw.rect(screen, (40, 40, 60), feedback_rect, border_radius=8)
        
        # Border color based on feedback type
        border_color = (100, 255, 100) if "Correct" in self.feedback_text else (255, 100, 100)
        pygame.draw.rect(screen, border_color, feedback_rect, 2, border_radius=8)
        
        # Text - single line
        font = pygame.font.Font(None, 20)
        text_surface = font.render(self.feedback_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=feedback_rect.center)
        screen.blit(text_surface, text_rect)
    
    def _is_perfect_pass(self):
        """Check if the forward pass was executed correctly (always true for forward prop)"""
        # Forward propagation is about understanding the process, not hitting targets
        # A "perfect pass" means the player executed it (which they did by pressing F)
        return True
    
    def _boss_forward_pass(self):
        """Quiz-based boss battle - answer questions quickly to beat the boss"""
        if not hasattr(self, 'boss_questions'):
            self._initialize_boss_questions()
        
        # If no current question, show next one
        if not self.current_question and self.boss_question_index < len(self.boss_questions):
            self._show_boss_question()
            self._start_question_timer()
        elif not self.current_question:
            # No more questions, determine winner
            if self.race_progress >= self.boss_progress:
                self.phase = "victory"
                self._handle_victory()
            else:
                self.phase = "defeat"
                self._handle_defeat()
    
    def _initialize_boss_questions(self):
        """Initialize boss battle questions"""
        self.boss_questions = [
            {
                'question': 'In forward propagation, what happens FIRST?',
                'options': [
                    'Apply activation function',
                    'Multiply inputs by weights', 
                    'Add bias terms',
                    'Calculate gradients'
                ],
                'correct': 2,
                'time_limit': 5.0
            },
            {
                'question': 'What does the bias term do?',
                'options': [
                    'Speeds up training',
                    'Shifts the activation threshold',
                    'Prevents overfitting', 
                    'Normalizes inputs'
                ],
                'correct': 2,
                'time_limit': 4.5
            },
            {
                'question': 'Which activation keeps only positive values?',
                'options': [
                    'Sigmoid',
                    'ReLU',
                    'Tanh',
                    'Softmax'
                ],
                'correct': 2,
                'time_limit': 4.0
            },
            {
                'question': 'What does softmax output sum to?',
                'options': [
                    '0',
                    '1', 
                    'Infinity',
                    'Depends on input'
                ],
                'correct': 2,
                'time_limit': 3.5
            },
            {
                'question': 'In z = Wx + b, what is W?',
                'options': [
                    'Weights matrix',
                    'Bias vector',
                    'Input vector',
                    'Output vector'
                ],
                'correct': 1,
                'time_limit': 3.0
            }
        ]
        self.boss_question_index = 0
        self.question_start_time = 0
        self.current_time_limit = 5.0
    
    def _show_boss_question(self):
        """Show the next boss question"""
        if self.boss_question_index < len(self.boss_questions):
            self.current_question = self.boss_questions[self.boss_question_index]
            self.current_time_limit = self.current_question['time_limit']
            self.boss_question_index += 1
            self.question_timed_out = False  # Reset timeout flag
    
    def _start_question_timer(self):
        """Start timer for current question"""
        self.question_start_time = pygame.time.get_ticks() / 1000.0
    
    def _answer_boss_question(self, answer_num):
        """Handle boss question answers with time pressure"""
        if not self.current_question:
            return
        
        current_time = pygame.time.get_ticks() / 1000.0
        time_taken = current_time - getattr(self, 'question_start_time', current_time)
        
        # Check if answer is correct
        if answer_num == self.current_question['correct']:
            # Correct answer - calculate progress based on speed
            if time_taken <= 2.0:
                progress = 25  # Very fast
                self.feedback_text = "⚡ LIGHTNING FAST! +25%"
            elif time_taken <= 3.0:
                progress = 20  # Fast
                self.feedback_text = "🚀 FAST! +20%"
            elif time_taken <= 4.0:
                progress = 15  # Good
                self.feedback_text = "✅ Good! +15%"
            else:
                progress = 10  # Slow but correct
                self.feedback_text = "✅ Correct but slow +10%"
            
            self.race_progress += progress
        else:
            # Wrong answer - small penalty
            progress = 5
            self.race_progress += progress
            correct_answer = self.current_question['options'][self.current_question['correct'] - 1]
            self.feedback_text = f"❌ Wrong! Correct: {correct_answer} +5%"
        
        # Boss progresses based on time taken (faster boss response if player is slow)
        if time_taken <= 2.0:
            boss_progress = 8   # Player was very fast, boss gets less
        elif time_taken <= 3.0:
            boss_progress = 12  # Normal boss progress
        elif time_taken <= 4.0:
            boss_progress = 16  # Player was slow, boss gets more
        else:
            boss_progress = 20  # Player was very slow, boss gets much more
        
        self.boss_progress += boss_progress
        
        # Show feedback timer
        self.feedback_timer = 2.0
        
        # Clear current question
        self.current_question = None
        
        # Check win/lose conditions
        if self.race_progress >= 100:
            self.phase = "victory"
            self._handle_victory()
        elif self.boss_progress >= 100:
            self.phase = "defeat"
            self._handle_defeat()
        else:
            # Update dialogue with progress
            progress_text = f"Race Progress - You: {self.race_progress}% | Boss: {self.boss_progress}%"
            self.dialogue_box.set_dialogue(progress_text, "System")
    
    def _handle_victory(self):
        """Handle victory in boss battle"""
        self.boss_hp = 0
        victory_text = "🎉 Victory! You've mastered forward propagation speed and understanding!"
        self.dialogue_box.set_dialogue(victory_text, "System")
        # Audio removed
    
    def _handle_defeat(self):
        """Handle defeat in boss battle"""
        self.phase = "defeat"
        defeat_text = "💀 Defeat! The Flow Guardian was too fast! Press R to retry or ESC to exit"
        self.dialogue_box.set_dialogue(defeat_text, "System")
    
    def _retry_boss_battle(self):
        """Reset and retry the boss battle"""
        # Reset all boss battle state
        self.race_progress = 0
        self.boss_progress = 0
        self.boss_question_index = 0
        self.current_question = None
        self.question_timed_out = False
        self.feedback_text = ""
        self.feedback_timer = 0
        
        # Reset boss questions if they exist
        if hasattr(self, 'boss_questions'):
            delattr(self, 'boss_questions')
        
        # Go back to boss phase
        self.phase = "boss"
        retry_text = "🔄 Retry! Show the Flow Guardian your true speed and knowledge!"
        self.dialogue_box.set_dialogue(retry_text, "System")
    
    def _handle_question_timeout(self):
        """Handle when a question times out"""
        if not self.current_question:
            return
        
        # Player gets no points for timeout
        player_progress = 0
        
        # Boss gets maximum points for player timeout
        boss_progress = 25
        
        self.race_progress += player_progress
        self.boss_progress += boss_progress
        
        # Show timeout feedback
        self.feedback_text = "⏰ TIME OUT! Boss gains advantage!"
        self.feedback_timer = 2.0
        
        # Clear current question and reset timeout flag
        self.current_question = None
        self.question_timed_out = False
        
        # Check win/lose conditions
        if self.race_progress >= 100:
            self.phase = "victory"
            self._handle_victory()
        elif self.boss_progress >= 100:
            self.phase = "defeat"
            self._handle_defeat()
        else:
            # Update dialogue with progress
            progress_text = f"Race Progress - You: {self.race_progress}% | Boss: {self.boss_progress}%"
            self.dialogue_box.set_dialogue(progress_text, "System")
    
    def update(self, dt):
        self.visualizer.update_animation(dt)
        self.dialogue_box.update(dt)
        self.understanding_bar.update(dt)
        self.speed_bar.set_value(self.accuracy_bonus * 40)
        self.speed_bar.update(dt)
        self.particles.update(dt)
        
        # Update feedback timer
        if self.feedback_timer > 0:
            self.feedback_timer -= dt
        
        # Update time pressure
        if self.time_pressure and self.phase == "practice":
            self.current_time += dt
            if self.current_time > self.time_limit:
                # Auto-execute if time runs out
                self._execute_forward_pass()
        
        # Update flow particles
        for particle in self.data_flow_particles[:]:
            particle['progress'] += dt * self.flow_speed
            
            if particle['progress'] >= 1.0:
                particle['current_pos'] = list(particle['end_pos'])
                particle['lifetime'] -= dt
                if particle['lifetime'] <= 0:
                    self.data_flow_particles.remove(particle)
            else:
                # Interpolate position
                start = particle['start_pos']
                end = particle['end_pos']
                progress = particle['progress']
                
                particle['current_pos'][0] = start[0] + (end[0] - start[0]) * progress
                particle['current_pos'][1] = start[1] + (end[1] - start[1]) * progress
        
        # Update processing animation
        if self.current_layer_processing >= 0:
            self.processing_timer += dt
            if self.processing_timer > 0.5:
                self.current_layer_processing += 1
                self.processing_timer = 0
                if self.current_layer_processing >= len(self.network['layers']):
                    self.current_layer_processing = -1
    
    def render(self, screen):
        # Dynamic background based on network activity
        activity_level = sum(sum(abs(a) for a in layer['activations']) for layer in self.network['layers'])
        bg_intensity = int(20 + min(30, activity_level * 2))
        
        for y in range(self.game.height):
            intensity = bg_intensity + int((y / self.game.height) * 20)
            color = (intensity, intensity + 5, intensity + 15)
            pygame.draw.line(screen, color, (0, y), (self.game.width, y))
        
        if self.phase in ["intro", "theory"]:
            self._render_intro_theory(screen)
        elif self.phase == "practice":
            self._render_practice(screen)
        elif self.phase == "boss":
            self._render_boss_battle(screen)
        elif self.phase == "victory":
            self._render_victory(screen)
        elif self.phase == "defeat":
            self._render_defeat(screen)
        
        # Always render dialogue and particles
        self.dialogue_box.render(screen, pygame.font.Font(None, 28), pygame.font.Font(None, 32))
        self.particles.render(screen)
    
    def _render_intro_theory(self, screen):
        """Render introduction and theory with responsive layout"""
        # Get responsive areas
        title_rect = self.layout.get_rect(0, 0, 1, 0.15)
        boss_rect = self.layout.get_rect(0.2, 0.15, 0.6, 0.12)
        network_rect = self.layout.get_rect(0.05, 0.3, 0.9, 0.4)
        instruction_rect = self.layout.get_rect(0, 0.7, 1, 0.06)
        
        # Title with responsive font
        title_font_size = self.layout.get_font_size(0.06, min_size=32, max_size=64)
        title_font = pygame.font.Font(None, title_font_size)
        title = title_font.render("🌊 Forward Propagation", True, (100, 255, 255))
        title_rect_center = title.get_rect(center=title_rect.center)
        screen.blit(title, title_rect_center)
        
        # Boss with responsive design
        pygame.draw.rect(screen, (100, 150, 255), boss_rect, border_radius=15)
        pygame.draw.rect(screen, (150, 200, 255), boss_rect, 3, border_radius=15)
        
        boss_font_size = self.layout.get_font_size(0.04, min_size=20, max_size=40)
        boss_font = pygame.font.Font(None, boss_font_size)
        boss_text = boss_font.render("⚡ Flow Guardian", True, (255, 255, 255))
        boss_text_rect = boss_text.get_rect(center=boss_rect.center)
        screen.blit(boss_text, boss_text_rect)
        
        # Clear instructions with background for visibility
        instruction_font_size = self.layout.get_font_size(0.025, min_size=16, max_size=28)
        instruction_font = pygame.font.Font(None, instruction_font_size)
        
        if self.phase == "intro":
            if self.dialogue_box.is_complete():
                instruction_text = "Press F to continue learning about forward propagation!"
            else:
                instruction_text = "Read the dialogue below, then press F to continue"
        else:  # theory phase
            instruction_text = "Press F to start practicing forward propagation!"
        
        # Add background for better visibility
        instruction_surface = instruction_font.render(instruction_text, True, (255, 255, 100))
        instruction_surface_rect = instruction_surface.get_rect(center=instruction_rect.center)
        
        # Draw background rectangle
        bg_rect = instruction_surface_rect.inflate(20, 10)
        pygame.draw.rect(screen, (40, 40, 60), bg_rect, border_radius=8)
        pygame.draw.rect(screen, (255, 255, 100), bg_rect, 2, border_radius=8)
        
        screen.blit(instruction_surface, instruction_surface_rect)
        
        if self.phase == "theory":
            self._render_network_diagram(screen, network_rect.x, network_rect.y, network_rect.width, network_rect.height)
    
    def _render_practice(self, screen):
        """Render practice phase with clean, non-overlapping layout"""
        
        # Header section (top 15%)
        header_y = 20
        header_font = pygame.font.Font(None, 32)
        title_text = "🎯 Forward Propagation Practice"
        title_surface = header_font.render(title_text, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(self.game.width // 2, header_y))
        screen.blit(title_surface, title_rect)
        
        # Step and progress (next 10%)
        step_y = header_y + 40
        step_font = pygame.font.Font(None, 20)
        step_text = f"Step {self.current_step}/{self.max_steps}: {self.step_names[min(self.current_step, len(self.step_names)-1)]}"
        step_surface = step_font.render(step_text, True, (255, 255, 100))
        step_rect = step_surface.get_rect(center=(self.game.width // 2, step_y))
        screen.blit(step_surface, step_rect)
        
        # Progress bar
        progress_y = step_y + 30
        progress_rect = pygame.Rect(150, progress_y, 700, 20)
        self.understanding_bar.rect = progress_rect
        self.understanding_bar.render(screen, pygame.font.Font(None, 16))
        
        # Network visualization (middle 40%)
        network_y = progress_y + 40
        network_height = 200
        self._render_educational_network(screen, 50, network_y, 900, network_height)
        
        # Stats line (compact)
        stats_y = network_y + network_height + 20
        stats_font = pygame.font.Font(None, 16)
        stats_text = f"Understanding: {self.understanding_points}/100 | Q&A: {self.correct_answers}/{self.questions_asked}"
        stats_surface = stats_font.render(stats_text, True, (180, 180, 180))
        stats_rect = stats_surface.get_rect(center=(self.game.width // 2, stats_y))
        screen.blit(stats_surface, stats_rect)
        
        # Instructions (compact)
        inst_y = stats_y + 30
        inst_font = pygame.font.Font(None, 18)
        if self.understanding_points >= 80:
            inst_text = "🎉 Ready for boss battle! Press F to face the Flow Guardian!"
            color = (100, 255, 100)
        else:
            inst_text = "Press F to execute forward pass • Press 1-4 to answer questions"
            color = (255, 255, 100)
        
        inst_surface = inst_font.render(inst_text, True, color)
        inst_rect = inst_surface.get_rect(center=(self.game.width // 2, inst_y))
        
        # Background for instructions
        bg_rect = inst_rect.inflate(20, 8)
        pygame.draw.rect(screen, (40, 45, 60), bg_rect, border_radius=5)
        pygame.draw.rect(screen, color, bg_rect, 1, border_radius=5)
        screen.blit(inst_surface, inst_rect)
        
        # Question area - positioned in remaining space
        if hasattr(self, 'current_question') and self.current_question:
            question_y = inst_y + 50
            self._render_compact_question(screen, question_y)
        
        # Feedback overlay
        if self.feedback_timer > 0:
            self._render_center_feedback(screen)
    
    def _render_boss_battle(self, screen):
        """Render clean boss battle layout"""
        # Boss title at top
        boss_rect = pygame.Rect(200, 20, 600, 50)
        pygame.draw.rect(screen, (100, 150, 255), boss_rect, border_radius=15)
        pygame.draw.rect(screen, (150, 200, 255), boss_rect, 3, border_radius=15)
        
        boss_font = pygame.font.Font(None, 32)
        boss_text = boss_font.render("⚡ Flow Guardian", True, (255, 255, 255))
        boss_text_rect = boss_text.get_rect(center=boss_rect.center)
        screen.blit(boss_text, boss_text_rect)
        
        # Progress bars section - positioned as overlays on the network area
        bar_width = 400
        bar_height = 20
        
        # Player progress bar - top left overlay
        player_bar_rect = pygame.Rect(60, 90, bar_width, bar_height)
        pygame.draw.rect(screen, (40, 40, 40), player_bar_rect, border_radius=5)
        
        player_fill_width = int((self.race_progress / 100) * bar_width)
        player_fill_rect = pygame.Rect(player_bar_rect.x, player_bar_rect.y, player_fill_width, bar_height)
        pygame.draw.rect(screen, (0, 255, 100), player_fill_rect, border_radius=5)
        pygame.draw.rect(screen, (255, 255, 255), player_bar_rect, 2, border_radius=5)
        
        # Player label
        label_font = pygame.font.Font(None, 18)
        player_text = label_font.render(f"You: {self.race_progress:.0f}%", True, (255, 255, 255))
        screen.blit(player_text, (player_bar_rect.x, player_bar_rect.y - 20))
        
        # Boss progress bar - below player bar
        boss_bar_rect = pygame.Rect(60, 130, bar_width, bar_height)
        pygame.draw.rect(screen, (40, 40, 40), boss_bar_rect, border_radius=5)
        
        boss_fill_width = int((self.boss_progress / 100) * bar_width)
        boss_fill_rect = pygame.Rect(boss_bar_rect.x, boss_bar_rect.y, boss_fill_width, bar_height)
        pygame.draw.rect(screen, (255, 100, 100), boss_fill_rect, border_radius=5)
        pygame.draw.rect(screen, (255, 255, 255), boss_bar_rect, 2, border_radius=5)
        
        # Boss label
        boss_text = label_font.render(f"Boss: {self.boss_progress:.0f}%", True, (255, 255, 255))
        screen.blit(boss_text, (boss_bar_rect.x, boss_bar_rect.y - 20))
        
        # Network visualization - starts right after boss title
        network_y = 80
        network_height = 300  # Full height for better visibility
        self._render_interactive_network(screen, 50, network_y, 900, network_height)
        
        # Quiz question area - positioned above dialogue area
        question_y = network_y + network_height + 10
        if hasattr(self, 'current_question') and self.current_question is not None:
            self._render_boss_question_with_timer(screen, question_y)
        
        # Instructions at bottom - positioned above dialogue area
        inst_y = question_y + (120 if self.current_question else 0)
        inst_font = pygame.font.Font(None, 20)
        
        if self.race_progress >= 100:
            instruction_text = "🏆 Victory! Press F to complete the challenge!"
            color = (100, 255, 100)
        elif self.boss_progress >= 100:
            instruction_text = "💀 Boss won! Press R to retry or ESC to exit"
            color = (255, 100, 100)
        elif hasattr(self, 'current_question') and self.current_question is not None:
            instruction_text = "Answer quickly! Press 1-4 to select your answer"
            color = (255, 255, 100)
        else:
            instruction_text = "Press F to start quiz battle • Press H for hints"
            color = (255, 255, 100)
        
        instruction_surface = inst_font.render(instruction_text, True, color)
        instruction_surface_rect = instruction_surface.get_rect(center=(self.game.width // 2, inst_y))
        
        # Background for visibility
        bg_rect = instruction_surface_rect.inflate(20, 10)
        pygame.draw.rect(screen, (20, 20, 40), bg_rect, border_radius=5)
        pygame.draw.rect(screen, color, bg_rect, 2, border_radius=5)
        screen.blit(instruction_surface, instruction_surface_rect)
        
        # Show hints if requested
        if self.show_hint:
            self._render_boss_hints(screen)
        
        # Show feedback if available
        if self.feedback_text and self.feedback_timer > 0:
            self._render_center_feedback(screen)
    
    def _render_boss_question_with_timer(self, screen, start_y):
        """Render boss question with countdown timer"""
        if not hasattr(self, 'current_question') or not self.current_question:
            return
        
        # Question background
        question_rect = pygame.Rect(50, start_y, self.game.width - 100, 100)
        pygame.draw.rect(screen, (20, 25, 40), question_rect, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 100), question_rect, 4, border_radius=12)
        
        # Timer bar at top of question
        if hasattr(self, 'question_start_time') and hasattr(self, 'current_time_limit'):
            current_time = pygame.time.get_ticks() / 1000.0
            time_elapsed = current_time - self.question_start_time
            time_remaining = max(0, self.current_time_limit - time_elapsed)
            timer_progress = time_remaining / self.current_time_limit
            
            timer_rect = pygame.Rect(question_rect.x + 10, question_rect.y + 5, question_rect.width - 20, 8)
            pygame.draw.rect(screen, (60, 60, 60), timer_rect, border_radius=4)
            
            timer_fill_width = int(timer_progress * timer_rect.width)
            timer_fill_rect = pygame.Rect(timer_rect.x, timer_rect.y, timer_fill_width, timer_rect.height)
            
            # Color changes based on time remaining
            if timer_progress > 0.6:
                timer_color = (100, 255, 100)  # Green
            elif timer_progress > 0.3:
                timer_color = (255, 255, 100)  # Yellow
            else:
                timer_color = (255, 100, 100)  # Red
            
            pygame.draw.rect(screen, timer_color, timer_fill_rect, border_radius=4)
            
            # Time remaining text
            time_font = pygame.font.Font(None, 16)
            time_text = time_font.render(f"{time_remaining:.1f}s", True, (255, 255, 255))
            screen.blit(time_text, (timer_rect.right - 40, timer_rect.y - 2))
            
            # Auto-timeout if time runs out
            if time_remaining <= 0 and not hasattr(self, 'question_timed_out'):
                self.question_timed_out = True
                self._handle_question_timeout()
        
        # Question text
        question_font = pygame.font.Font(None, 24)
        question_text = self.current_question.get('question', '')
        question_surface = question_font.render(question_text, True, (255, 255, 255))
        screen.blit(question_surface, (question_rect.x + 15, question_rect.y + 20))
        
        # Options in two columns
        options = self.current_question.get('options', [])
        option_font = pygame.font.Font(None, 20)
        
        for i, option in enumerate(options):
            col = i % 2
            row = i // 2
            x = question_rect.x + 20 + col * 400
            y = question_rect.y + 50 + row * 25
            
            option_text = f"{i+1}. {option}"
            option_surface = option_font.render(option_text, True, (200, 220, 255))
            screen.blit(option_surface, (x, y))
        
        # Show feedback if active
        if self.feedback_timer > 0:
            self._render_center_feedback(screen)
        
        # Temporarily override dialogue position for boss battle
        if hasattr(self.dialogue_box, 'rect'):
            # Move dialogue to bottom of screen
            self.dialogue_box.rect.y = self.game.height - 120
    
    def _render_boss_hints(self, screen):
        """Render hints for boss battle"""
        hint_rect = pygame.Rect(500, 90, 450, 180)
        pygame.draw.rect(screen, (40, 40, 60), hint_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 100), hint_rect, 2, border_radius=10)
        
        hint_font = pygame.font.Font(None, 18)
        hints = [
            "💡 SPEED CHALLENGE HINTS:",
            "",
            "🏃 Execute forward passes quickly!",
            "⚡ Each pass gives +25% progress",
            "🎲 30% chance for speed bonus (+10%)",
            "🤖 Boss processes at steady pace",
            "🏆 First to 100% wins!",
            "",
            "Just keep pressing F!"
        ]
        
        for i, hint in enumerate(hints):
            color = (255, 255, 100) if "💡" in hint else (255, 255, 255)
            hint_surface = hint_font.render(hint, True, color)
            screen.blit(hint_surface, (hint_rect.x + 10, hint_rect.y + 10 + i * 20))
    
    def _render_victory(self, screen):
        """Render victory screen"""
        # Animated victory title
        victory_font = pygame.font.Font(None, 64)
        flow_effect = abs(math.sin(pygame.time.get_ticks() * 0.01)) * 100 + 155
        
        victory_text = victory_font.render("FLOW MASTERED!", True, (100, 255, int(flow_effect)))
        victory_rect = victory_text.get_rect(center=(self.game.width // 2, 200))
        screen.blit(victory_text, victory_rect)
        
        # Victory message
        victory_message = "🏆 Flow Guardian Defeated!"
        message_font = pygame.font.Font(None, 36)
        message_text = message_font.render(victory_message, True, (255, 255, 100))
        message_rect = message_text.get_rect(center=(self.game.width // 2, 320))
        screen.blit(message_text, message_rect)
        
        # Completion instructions
        instruction_font = pygame.font.Font(None, 28)
        instruction_text = "Press F to continue • Press ESC to exit"
        instruction_surface = instruction_font.render(instruction_text, True, (255, 255, 255))
        instruction_rect = instruction_surface.get_rect(center=(self.game.width // 2, 380))
        screen.blit(instruction_surface, instruction_rect)
    
    def _render_defeat(self, screen):
        """Render defeat screen with retry option"""
        # Dark overlay
        overlay = pygame.Surface((self.game.width, self.game.height))
        overlay.set_alpha(180)
        overlay.fill((40, 20, 20))
        screen.blit(overlay, (0, 0))
        
        # Defeat title
        defeat_font = pygame.font.Font(None, 72)
        defeat_text = defeat_font.render("💀 DEFEAT", True, (255, 100, 100))
        defeat_rect = defeat_text.get_rect(center=(self.game.width // 2, self.game.height // 2 - 100))
        screen.blit(defeat_text, defeat_rect)
        
        # Boss won message
        message_font = pygame.font.Font(None, 36)
        message_text = message_font.render("The Flow Guardian was too fast!", True, (255, 200, 200))
        message_rect = message_text.get_rect(center=(self.game.width // 2, self.game.height // 2 - 40))
        screen.blit(message_text, message_rect)
        
        # Progress summary
        summary_font = pygame.font.Font(None, 28)
        summary_text = f"Final Score - You: {self.race_progress}% | Boss: {self.boss_progress}%"
        summary_surface = summary_font.render(summary_text, True, (255, 255, 255))
        summary_rect = summary_surface.get_rect(center=(self.game.width // 2, self.game.height // 2 + 20))
        screen.blit(summary_surface, summary_rect)
        
        # Retry instructions
        retry_font = pygame.font.Font(None, 32)
        retry_text = retry_font.render("Press R to Retry • Press ESC to Exit", True, (255, 255, 100))
        retry_rect = retry_text.get_rect(center=(self.game.width // 2, self.game.height // 2 + 80))
        screen.blit(retry_text, retry_rect)
    
    def _render_network_diagram(self, screen, x, y, width, height):
        """Render responsive network architecture diagram"""
        # Background
        pygame.draw.rect(screen, (30, 30, 50), (x, y, width, height), border_radius=15)
        pygame.draw.rect(screen, (100, 150, 255), (x, y, width, height), 2, border_radius=15)
        
        # Responsive font size
        equation_font_size = max(16, min(28, int(width * 0.025)))
        equation_font = pygame.font.Font(None, equation_font_size)
        
        # Forward pass equations
        equations = [
            "🔄 Forward Pass: z = Wx + b",
            "⚡ Activation: a = f(z)", 
            "🌊 Flow: Input → Hidden → Output"
        ]
        
        equation_y_start = y + int(height * 0.1)
        equation_spacing = max(25, int(height * 0.08))
        
        for i, eq in enumerate(equations):
            eq_surface = equation_font.render(eq, True, (255, 255, 100))
            eq_rect = eq_surface.get_rect(center=(x + width // 2, equation_y_start + i * equation_spacing))
            screen.blit(eq_surface, eq_rect)
        
        # Network diagram area
        diagram_y = equation_y_start + len(equations) * equation_spacing + 20
        diagram_height = height - (diagram_y - y) - 20
        self._render_simple_network_diagram(screen, x + 20, diagram_y, width - 40, diagram_height)
    
    def _render_simple_network_diagram(self, screen, x, y, width, height):
        """Render responsive simplified network diagram"""
        layer_sizes = [3, 4, 3, 2]
        layer_names = ["Input", "Hidden 1 (relu)", "Hidden 2 (sigmoid)", "Output (softmax)"]
        
        # Calculate responsive positions
        layer_spacing = width // (len(layer_sizes) + 1)
        layer_x_positions = [x + layer_spacing * (i + 1) for i in range(len(layer_sizes))]
        
        # Responsive neuron size and spacing
        neuron_radius = max(8, min(20, int(height * 0.08)))
        max_neurons = max(layer_sizes)
        neuron_spacing = min(height * 0.8 / max_neurons, neuron_radius * 3)
        
        # Draw connections first (behind neurons)
        for layer_idx in range(len(layer_x_positions) - 1):
            start_x = layer_x_positions[layer_idx]
            end_x = layer_x_positions[layer_idx + 1]
            
            for i in range(layer_sizes[layer_idx]):
                start_y = y + height // 2 - (layer_sizes[layer_idx] - 1) * neuron_spacing // 2 + i * neuron_spacing
                for j in range(layer_sizes[layer_idx + 1]):
                    end_y = y + height // 2 - (layer_sizes[layer_idx + 1] - 1) * neuron_spacing // 2 + j * neuron_spacing
                    pygame.draw.line(screen, (80, 80, 120), (start_x + neuron_radius, start_y), (end_x - neuron_radius, end_y), 1)
        
        # Draw neurons and labels
        label_font_size = max(12, min(20, int(width * 0.02)))
        label_font = pygame.font.Font(None, label_font_size)
        
        for layer_idx, (layer_x, size) in enumerate(zip(layer_x_positions, layer_sizes)):
            # Layer label
            label_surface = label_font.render(layer_names[layer_idx], True, (255, 255, 255))
            label_rect = label_surface.get_rect(center=(layer_x, y - 10))
            screen.blit(label_surface, label_rect)
            
            # Neurons
            for neuron_idx in range(size):
                neuron_y = y + height // 2 - (size - 1) * neuron_spacing // 2 + neuron_idx * neuron_spacing
                
                if layer_idx == 0:
                    color = (100, 150, 255)  # Input - blue
                elif layer_idx == len(layer_x_positions) - 1:
                    color = (255, 150, 100)  # Output - orange
                else:
                    color = (150, 255, 150)  # Hidden - green
                
                pygame.draw.circle(screen, color, (layer_x, neuron_y), neuron_radius)
                pygame.draw.circle(screen, (255, 255, 255), (layer_x, neuron_y), neuron_radius, 2)
                
                pygame.draw.circle(screen, color, (layer_x, neuron_y), 15)
                pygame.draw.circle(screen, (255, 255, 255), (layer_x, neuron_y), 15, 2)
    
    def _render_interactive_network(self, screen, x, y, width, height):
        """Render interactive network with real-time values - MUCH CLEARER"""
        # Background
        pygame.draw.rect(screen, (20, 25, 35), (x, y, width, height), border_radius=15)
        pygame.draw.rect(screen, (100, 150, 200), (x, y, width, height), 3, border_radius=15)
        
        layer_positions = self._get_layer_positions()
        
        # Draw connections with weights - MUCH MORE VISIBLE
        for layer_idx in range(len(self.network['weights'])):
            start_positions = layer_positions[layer_idx]
            end_positions = layer_positions[layer_idx + 1]
            weights = self.network['weights'][layer_idx]
            
            for i, start_pos in enumerate(start_positions):
                for j, end_pos in enumerate(end_positions):
                    weight = weights[i][j]
                    
                    # Much more visible connection colors and thickness
                    if weight > 0:
                        color = (0, int(100 + 155 * min(1, abs(weight) / 2)), 0)
                    else:
                        color = (int(100 + 155 * min(1, abs(weight) / 2)), 0, 0)
                    
                    thickness = max(2, int(abs(weight) * 4 + 1))
                    
                    # Highlight selected connection
                    if (self.selected_connection and 
                        self.selected_connection == (layer_idx, i, j)):
                        color = (255, 255, 0)  # Yellow for selected
                        thickness += 2
                    
                    pygame.draw.line(screen, color, start_pos, end_pos, thickness)
                    
                    # Draw weight value on connection
                    mid_x = (start_pos[0] + end_pos[0]) // 2
                    mid_y = (start_pos[1] + end_pos[1]) // 2
                    
                    weight_text = f"{weight:.2f}"
                    weight_font = pygame.font.Font(None, 14)
                    weight_surface = weight_font.render(weight_text, True, (255, 255, 255))
                    
                    # Background for weight text
                    text_rect = weight_surface.get_rect(center=(mid_x, mid_y))
                    bg_rect = text_rect.inflate(4, 2)
                    pygame.draw.rect(screen, (0, 0, 0, 180), bg_rect)
                    screen.blit(weight_surface, text_rect)
        
        # Draw flow particles - MORE VISIBLE
        for particle in self.data_flow_particles:
            pos = particle['current_pos']
            alpha = particle['lifetime'] / particle['max_lifetime']
            
            # Brighter particle colors
            colors = [(255, 150, 150), (150, 255, 150), (150, 150, 255)]
            color = colors[particle['layer'] % len(colors)]
            
            # Larger, more visible particles
            particle_surface = pygame.Surface((12, 12), pygame.SRCALPHA)
            particle_color = (*color, int(alpha * 255))
            pygame.draw.circle(particle_surface, particle_color, (6, 6), 6)
            screen.blit(particle_surface, (int(pos[0] - 6), int(pos[1] - 6)))
        
        # Draw neurons with activations - MUCH CLEARER
        for layer_idx, (layer, positions) in enumerate(zip(self.network['layers'], layer_positions)):
            for neuron_idx, pos in enumerate(positions):
                activation = layer['activations'][neuron_idx]
                
                # Much more distinct neuron colors
                if layer_idx == 0:
                    base_color = (50, 100, 255)  # Blue for input
                elif layer_idx == len(self.network['layers']) - 1:
                    base_color = (255, 100, 50)  # Orange for output
                else:
                    base_color = (100, 255, 100)  # Green for hidden
                
                # Activation-based intensity
                intensity = min(1.0, abs(activation) / 1.5)
                color = tuple(int(base_color[i] * (0.4 + 0.6 * intensity)) for i in range(3))
                
                # Larger neurons
                radius = 28 if layer_idx == self.current_layer_processing else 24
                
                # Neuron with glow effect
                glow_surface = pygame.Surface((radius * 3, radius * 3), pygame.SRCALPHA)
                glow_color = (*color, 80)
                pygame.draw.circle(glow_surface, glow_color, (radius * 3 // 2, radius * 3 // 2), radius + 8)
                screen.blit(glow_surface, (int(pos[0] - radius * 1.5), int(pos[1] - radius * 1.5)))
                
                pygame.draw.circle(screen, color, (int(pos[0]), int(pos[1])), radius)
                pygame.draw.circle(screen, (255, 255, 255), (int(pos[0]), int(pos[1])), radius, 3)
                
                # Large, clear activation value
                act_text = f"{activation:.3f}"
                act_font = pygame.font.Font(None, 18)
                act_surface = act_font.render(act_text, True, (255, 255, 255))
                act_rect = act_surface.get_rect(center=(pos[0], pos[1]))
                
                # Black background for text readability
                bg_rect = act_rect.inflate(4, 2)
                pygame.draw.rect(screen, (0, 0, 0), bg_rect)
                screen.blit(act_surface, act_rect)
            
            # Layer labels with better positioning
            if positions:
                label_pos = (positions[0][0], positions[0][1] - 60)
                layer_name = layer['name']
                if layer_idx > 0:
                    layer_name += f" ({layer.get('activation_func', 'linear')})"
                
                label_font = pygame.font.Font(None, 20)
                label_text = label_font.render(layer_name, True, (255, 255, 200))
                label_rect = label_text.get_rect(center=label_pos)
                
                # Background for label
                bg_rect = label_rect.inflate(8, 4)
                pygame.draw.rect(screen, (0, 0, 0, 150), bg_rect)
                screen.blit(label_text, label_rect)
        
        # Show current target output prominently
        if len(self.network['layers']) > 0:
            output_positions = layer_positions[-1]
            for i, (pos, target) in enumerate(zip(output_positions, self.target_output)):
                target_text = f"Target: {target:.3f}"
                target_font = pygame.font.Font(None, 16)
                target_surface = target_font.render(target_text, True, (255, 255, 100))
                target_rect = target_surface.get_rect(center=(pos[0], pos[1] + 40))
                
                bg_rect = target_rect.inflate(6, 3)
                pygame.draw.rect(screen, (50, 50, 0), bg_rect)
                screen.blit(target_surface, target_rect)
        
        # Instructions overlay
        inst_text = "Watch the data flow from left to right, layer by layer"
        inst_font = pygame.font.Font(None, 16)
        inst_surface = inst_font.render(inst_text, True, (200, 255, 200))
        inst_rect = pygame.Rect(x + 10, y + height - 25, width - 20, 20)
        pygame.draw.rect(screen, (0, 50, 0), inst_rect)
        screen.blit(inst_surface, (x + 15, y + height - 22))
    
    def _render_educational_network(self, screen, x, y, width, height):
        """Render network focused on education, not interaction"""
        # Background
        pygame.draw.rect(screen, (15, 20, 30), (x, y, width, height), border_radius=15)
        pygame.draw.rect(screen, (100, 150, 200), (x, y, width, height), 3, border_radius=15)
        
        layer_positions = self._get_layer_positions()
        
        # Draw connections - highlight current step
        for layer_idx in range(len(self.network['weights'])):
            start_positions = layer_positions[layer_idx]
            end_positions = layer_positions[layer_idx + 1]
            weights = self.network['weights'][layer_idx]
            
            # Highlight connections for current step
            is_current_step = (layer_idx == self.current_step - 1)
            
            for i, start_pos in enumerate(start_positions):
                for j, end_pos in enumerate(end_positions):
                    weight = weights[i][j]
                    
                    if is_current_step:
                        # Bright colors for current step
                        if weight > 0:
                            color = (0, 255, 100)
                        else:
                            color = (255, 100, 0)
                        thickness = 4
                    else:
                        # Dimmed colors for other steps
                        if weight > 0:
                            color = (0, 100, 50)
                        else:
                            color = (100, 50, 0)
                        thickness = 2
                    
                    pygame.draw.line(screen, color, start_pos, end_pos, thickness)
                    
                    # Show weight values for current step
                    if is_current_step:
                        mid_x = (start_pos[0] + end_pos[0]) // 2
                        mid_y = (start_pos[1] + end_pos[1]) // 2
                        
                        weight_text = f"{weight:.2f}"
                        weight_font = pygame.font.Font(None, 12)
                        weight_surface = weight_font.render(weight_text, True, (255, 255, 255))
                        
                        # Background for weight text
                        text_rect = weight_surface.get_rect(center=(mid_x, mid_y))
                        bg_rect = text_rect.inflate(4, 2)
                        pygame.draw.rect(screen, (0, 0, 0), bg_rect)
                        screen.blit(weight_surface, text_rect)
        
        # Draw enhanced flow particles
        for particle in self.data_flow_particles:
            pos = particle['current_pos']
            alpha = particle['lifetime'] / particle['max_lifetime']
            
            # Larger, more visible particles
            colors = [(255, 200, 100), (100, 255, 200), (200, 100, 255)]
            color = colors[particle['layer'] % len(colors)]
            
            particle_surface = pygame.Surface((16, 16), pygame.SRCALPHA)
            particle_color = (*color, int(alpha * 255))
            pygame.draw.circle(particle_surface, particle_color, (8, 8), 8)
            screen.blit(particle_surface, (int(pos[0] - 8), int(pos[1] - 8)))
        
        # Draw neurons with step highlighting
        for layer_idx, (layer, positions) in enumerate(zip(self.network['layers'], layer_positions)):
            is_current_layer = (layer_idx == self.current_step)
            
            for neuron_idx, pos in enumerate(positions):
                activation = layer['activations'][neuron_idx]
                
                # Enhanced neuron colors
                if layer_idx == 0:
                    base_color = (50, 100, 255)  # Blue for input
                elif layer_idx == len(self.network['layers']) - 1:
                    base_color = (255, 100, 50)  # Orange for output
                else:
                    base_color = (100, 255, 100)  # Green for hidden
                
                # Highlight current layer
                if is_current_layer:
                    base_color = tuple(min(255, c + 100) for c in base_color)
                
                # Activation-based intensity
                intensity = min(1.0, abs(activation) / 1.5) if activation != 0 else 0.3
                color = tuple(int(base_color[i] * (0.4 + 0.6 * intensity)) for i in range(3))
                
                # Larger neurons for current layer
                radius = 32 if is_current_layer else 26
                
                # Glow effect for current layer
                if is_current_layer:
                    glow_surface = pygame.Surface((radius * 3, radius * 3), pygame.SRCALPHA)
                    glow_color = (*color, 100)
                    pygame.draw.circle(glow_surface, glow_color, (radius * 3 // 2, radius * 3 // 2), radius + 12)
                    screen.blit(glow_surface, (int(pos[0] - radius * 1.5), int(pos[1] - radius * 1.5)))
                
                pygame.draw.circle(screen, color, (int(pos[0]), int(pos[1])), radius)
                pygame.draw.circle(screen, (255, 255, 255), (int(pos[0]), int(pos[1])), radius, 3)
                
                # Activation value - larger for current layer
                font_size = 20 if is_current_layer else 16
                act_text = f"{activation:.3f}"
                act_font = pygame.font.Font(None, font_size)
                act_surface = act_font.render(act_text, True, (255, 255, 255))
                act_rect = act_surface.get_rect(center=(pos[0], pos[1]))
                
                # Black background for text readability
                bg_rect = act_rect.inflate(6, 4)
                pygame.draw.rect(screen, (0, 0, 0), bg_rect)
                screen.blit(act_surface, act_rect)
            
            # Enhanced layer labels
            if positions:
                label_pos = (positions[0][0], positions[0][1] - 70)
                layer_name = layer['name']
                if layer_idx > 0:
                    layer_name += f" ({layer.get('activation_func', 'linear')})"
                
                # Highlight current layer label
                if is_current_layer:
                    layer_name = f">>> {layer_name} <<<"
                
                label_font = pygame.font.Font(None, 22 if is_current_layer else 18)
                label_color = (255, 255, 100) if is_current_layer else (200, 200, 255)
                label_text = label_font.render(layer_name, True, label_color)
                label_rect = label_text.get_rect(center=label_pos)
                
                # Background for label
                bg_rect = label_rect.inflate(10, 6)
                bg_color = (50, 50, 0) if is_current_layer else (0, 0, 50)
                pygame.draw.rect(screen, bg_color, bg_rect)
                screen.blit(label_text, label_rect)
        
        # Step progress indicator
        step_progress_y = y + height - 50
        step_width = width // self.max_steps
        
        for i in range(self.max_steps):
            step_x = x + i * step_width
            step_rect = pygame.Rect(step_x, step_progress_y, step_width - 5, 20)
            
            if i < self.current_step:
                color = (0, 255, 100)  # Completed
            elif i == self.current_step:
                color = (255, 255, 100)  # Current
            else:
                color = (100, 100, 100)  # Not yet
            
            pygame.draw.rect(screen, color, step_rect)
            pygame.draw.rect(screen, (255, 255, 255), step_rect, 2)
            
            # Step label
            step_label = f"Step {i+1}"
            step_font = pygame.font.Font(None, 14)
            step_surface = step_font.render(step_label, True, (0, 0, 0))
            step_text_rect = step_surface.get_rect(center=step_rect.center)
            screen.blit(step_surface, step_text_rect)