"""
Neural network visualization components for the game
"""

import pygame
import numpy as np
import math

class NeuralNetworkVisualizer:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.animation_time = 0
        
    def draw_neuron(self, screen, x, y, radius, activation=0.0, label="", is_input=False, is_output=False):
        """Draw a single neuron with activation visualization"""
        # Color based on activation level
        if is_input:
            base_color = (100, 150, 255)  # Blue for inputs
        elif is_output:
            base_color = (255, 150, 100)  # Orange for outputs
        else:
            base_color = (150, 255, 150)  # Green for hidden
        
        # Intensity based on activation
        intensity = min(1.0, abs(activation))
        color = tuple(int(base_color[i] * (0.3 + 0.7 * intensity)) for i in range(3))
        
        # Draw neuron circle
        pygame.draw.circle(screen, color, (int(x), int(y)), radius)
        pygame.draw.circle(screen, (255, 255, 255), (int(x), int(y)), radius, 2)
        
        # Draw activation value
        if abs(activation) > 0.01:
            font = pygame.font.Font(None, 20)
            text = font.render(f"{activation:.2f}", True, (255, 255, 255))
            text_rect = text.get_rect(center=(x, y))
            screen.blit(text, text_rect)
        
        # Draw label
        if label:
            font = pygame.font.Font(None, 24)
            text = font.render(label, True, (255, 255, 255))
            text_rect = text.get_rect(center=(x, y - radius - 20))
            screen.blit(text, text_rect)
    
    def draw_connection(self, screen, start_pos, end_pos, weight, animated=False, start_radius=25, end_radius=25):
        """Draw connection between neurons with weight visualization - avoids overlapping neurons"""
        # Calculate connection points at edge of neurons instead of center
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance == 0:
            return
        
        # Unit vector from start to end
        unit_x = dx / distance
        unit_y = dy / distance
        
        # Connection start and end points (at edge of neurons)
        connection_start = (
            start_pos[0] + unit_x * start_radius,
            start_pos[1] + unit_y * start_radius
        )
        connection_end = (
            end_pos[0] - unit_x * end_radius,
            end_pos[1] - unit_y * end_radius
        )
        
        # Color and thickness based on weight
        thickness = max(2, int(abs(weight) * 4) + 1)
        if weight > 0:
            color = (120, 220, 120)  # Softer green for positive weights
        else:
            color = (220, 120, 120)  # Softer red for negative weights
        
        # Animation effect
        if animated:
            pulse = math.sin(self.animation_time * 5) * 0.3 + 0.7
            color = tuple(int(c * pulse) for c in color)
        
        # Draw connection line
        pygame.draw.line(screen, color, connection_start, connection_end, thickness)
        
        # Draw weight value at midpoint, offset to avoid line overlap
        mid_x = (connection_start[0] + connection_end[0]) // 2
        mid_y = (connection_start[1] + connection_end[1]) // 2
        
        # Offset label perpendicular to line to avoid overlap
        perp_x = -unit_y * 15  # Perpendicular offset
        perp_y = unit_x * 15
        
        label_x = mid_x + perp_x
        label_y = mid_y + perp_y
        
        font = pygame.font.Font(None, 16)
        text = font.render(f"{weight:.2f}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(label_x, label_y))
        
        # Background for readability
        pygame.draw.rect(screen, (40, 50, 70), text_rect.inflate(4, 2))
        pygame.draw.rect(screen, (100, 120, 150), text_rect.inflate(4, 2), 1)
        screen.blit(text, text_rect)
    
    def draw_simple_network(self, screen, x, y, width, height, weights, biases, activations, labels=None):
        """Draw a simple feedforward network"""
        layers = len(activations)
        if layers == 0:
            return
        
        layer_width = width // layers
        positions = []
        
        # Calculate neuron positions
        for layer_idx in range(layers):
            layer_neurons = len(activations[layer_idx])
            layer_x = x + layer_idx * layer_width + layer_width // 2
            
            layer_positions = []
            for neuron_idx in range(layer_neurons):
                neuron_y = y + (neuron_idx + 1) * height // (layer_neurons + 1)
                layer_positions.append((layer_x, neuron_y))
            positions.append(layer_positions)
        
        # Draw connections first (so they appear behind neurons)
        for layer_idx in range(len(positions) - 1):
            for i, start_pos in enumerate(positions[layer_idx]):
                for j, end_pos in enumerate(positions[layer_idx + 1]):
                    if layer_idx < len(weights) and i < len(weights[layer_idx]) and j < len(weights[layer_idx][i]):
                        weight = weights[layer_idx][i][j] if isinstance(weights[layer_idx][i], list) else weights[layer_idx][j]
                        self.draw_connection(screen, start_pos, end_pos, weight, animated=True)
        
        # Draw neurons
        for layer_idx, layer_positions in enumerate(positions):
            for neuron_idx, pos in enumerate(layer_positions):
                activation = activations[layer_idx][neuron_idx] if neuron_idx < len(activations[layer_idx]) else 0
                label = ""
                if labels and layer_idx < len(labels) and neuron_idx < len(labels[layer_idx]):
                    label = labels[layer_idx][neuron_idx]
                
                is_input = layer_idx == 0
                is_output = layer_idx == len(positions) - 1
                
                self.draw_neuron(screen, pos[0], pos[1], 25, activation, label, is_input, is_output)
    
    def draw_activation_function(self, screen, x, y, width, height, func_name, input_val=0):
        """Draw activation function graph with current input highlighted"""
        # Background
        pygame.draw.rect(screen, (40, 40, 40), (x, y, width, height))
        pygame.draw.rect(screen, (255, 255, 255), (x, y, width, height), 2)
        
        # Title
        font = pygame.font.Font(None, 24)
        title = font.render(f"{func_name} Activation", True, (255, 255, 255))
        screen.blit(title, (x + 10, y + 10))
        
        # Draw axes
        center_x = x + width // 2
        center_y = y + height // 2
        pygame.draw.line(screen, (100, 100, 100), (x + 20, center_y), (x + width - 20, center_y), 1)  # X-axis
        pygame.draw.line(screen, (100, 100, 100), (center_x, y + 40), (center_x, y + height - 20), 1)  # Y-axis
        
        # Draw function curve
        points = []
        for i in range(width - 40):
            x_val = (i - (width - 40) // 2) / 20.0  # Scale to reasonable range
            
            if func_name.lower() == "relu":
                y_val = max(0, x_val)
            elif func_name.lower() == "sigmoid":
                y_val = 1 / (1 + math.exp(-x_val))
            elif func_name.lower() == "tanh":
                y_val = math.tanh(x_val)
            else:
                y_val = x_val  # Linear
            
            screen_x = x + 20 + i
            screen_y = center_y - int(y_val * 50)  # Scale for display
            screen_y = max(y + 40, min(y + height - 20, screen_y))  # Clamp to bounds
            
            points.append((screen_x, screen_y))
        
        if len(points) > 1:
            pygame.draw.lines(screen, (0, 255, 255), False, points, 2)
        
        # Highlight current input
        if abs(input_val) < 10:  # Only show if reasonable range
            input_x = center_x + int(input_val * 20)
            if func_name.lower() == "relu":
                output_val = max(0, input_val)
            elif func_name.lower() == "sigmoid":
                output_val = 1 / (1 + math.exp(-input_val))
            elif func_name.lower() == "tanh":
                output_val = math.tanh(input_val)
            else:
                output_val = input_val
            
            output_y = center_y - int(output_val * 50)
            output_y = max(y + 40, min(y + height - 20, output_y))
            
            # Draw point
            pygame.draw.circle(screen, (255, 255, 0), (input_x, output_y), 5)
            
            # Show values
            value_text = font.render(f"f({input_val:.2f}) = {output_val:.2f}", True, (255, 255, 0))
            screen.blit(value_text, (x + 10, y + height - 30))
    
    def draw_gradient_flow(self, screen, x, y, width, height, gradients):
        """Visualize gradient flow during backpropagation"""
        # Background
        pygame.draw.rect(screen, (20, 20, 40), (x, y, width, height))
        pygame.draw.rect(screen, (255, 255, 255), (x, y, width, height), 2)
        
        font = pygame.font.Font(None, 24)
        title = font.render("Gradient Flow", True, (255, 255, 255))
        screen.blit(title, (x + 10, y + 10))
        
        # Draw gradient arrows (simplified visualization)
        if gradients:
            arrow_y = y + 50
            for i, grad in enumerate(gradients[:5]):  # Show first 5 gradients
                arrow_length = min(100, abs(grad) * 50)
                arrow_color = (255, 100, 100) if grad < 0 else (100, 255, 100)
                
                start_x = x + 20
                end_x = start_x + arrow_length
                
                # Draw arrow
                pygame.draw.line(screen, arrow_color, (start_x, arrow_y), (end_x, arrow_y), 3)
                pygame.draw.polygon(screen, arrow_color, [
                    (end_x, arrow_y),
                    (end_x - 10, arrow_y - 5),
                    (end_x - 10, arrow_y + 5)
                ])
                
                # Label
                grad_text = pygame.font.Font(None, 18).render(f"∇{i}: {grad:.3f}", True, (255, 255, 255))
                screen.blit(grad_text, (end_x + 10, arrow_y - 8))
                
                arrow_y += 30
    
    def update_animation(self, dt):
        """Update animation timer"""
        self.animation_time += dt