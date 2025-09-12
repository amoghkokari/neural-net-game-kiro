"""
Perceptron implementation challenge
"""

import pygame
import numpy as np
from .base_challenge import BaseChallenge

class PerceptronChallenge(BaseChallenge):
    def __init__(self, game):
        super().__init__(game)
        self.step = 0  # 0: explanation, 1: coding, 2: testing, 3: completed
        self.user_code = ""
        self.cursor_pos = 0
        self.test_results = []
        
        # Sample data for testing
        self.training_data = np.array([
            [0, 0], [0, 1], [1, 0], [1, 1]
        ])
        self.training_labels = np.array([0, 0, 0, 1])  # AND gate
        
        self.template_code = '''import numpy as np

class Perceptron:
    def __init__(self):
        # Initialize weights and bias
        self.weights = np.random.randn(2) * 0.1
        self.bias = 0.0
        self.learning_rate = 0.1
    
    def forward(self, x):
        # TODO: Implement forward pass
        # Hint: output = sum(weights * inputs) + bias
        # Then apply step function (1 if > 0, else 0)
        pass
    
    def train(self, X, y, epochs=100):
        # TODO: Implement training loop
        # For each epoch and each sample:
        # 1. Get prediction
        # 2. Calculate error
        # 3. Update weights and bias
        pass

# Test your implementation
perceptron = Perceptron()
# Training data will be provided automatically'''
    
    def initialize(self):
        self.user_code = self.template_code
        self.step = 0
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.step == 0:  # Explanation phase
                if event.key == pygame.K_SPACE:
                    self.step = 1
            elif self.step == 1:  # Coding phase
                if event.key == pygame.K_F5:  # Run code
                    self.test_code()
                    self.step = 2
                elif event.key == pygame.K_BACKSPACE:
                    if self.cursor_pos > 0:
                        self.user_code = self.user_code[:self.cursor_pos-1] + self.user_code[self.cursor_pos:]
                        self.cursor_pos -= 1
                elif event.key == pygame.K_RETURN:
                    self.user_code = self.user_code[:self.cursor_pos] + '\n' + self.user_code[self.cursor_pos:]
                    self.cursor_pos += 1
                elif event.unicode and event.unicode.isprintable():
                    self.user_code = self.user_code[:self.cursor_pos] + event.unicode + self.user_code[self.cursor_pos:]
                    self.cursor_pos += 1
            elif self.step == 2:  # Testing phase
                if event.key == pygame.K_SPACE:
                    if self.completed:
                        return "completed"
                    else:
                        self.step = 1  # Back to coding
            
            if event.key == pygame.K_ESCAPE:
                return "exit"
        
        return None
    
    def test_code(self):
        """Test the user's perceptron implementation"""
        try:
            # Create a safe execution environment
            exec_globals = {
                'np': np,
                '__builtins__': {'print': print, 'len': len, 'range': range}
            }
            
            # Execute user code
            exec(self.user_code, exec_globals)
            
            # Test the implementation
            if 'Perceptron' in exec_globals:
                perceptron = exec_globals['Perceptron']()
                
                # Train the perceptron
                perceptron.train(self.training_data, self.training_labels)
                
                # Test predictions
                correct = 0
                self.test_results = []
                for i, (x, expected) in enumerate(zip(self.training_data, self.training_labels)):
                    prediction = perceptron.forward(x)
                    is_correct = abs(prediction - expected) < 0.5
                    if is_correct:
                        correct += 1
                    self.test_results.append({
                        'input': x,
                        'expected': expected,
                        'predicted': prediction,
                        'correct': is_correct
                    })
                
                if correct >= 3:  # Allow some tolerance
                    self.completed = True
                    self.test_results.append({'message': 'SUCCESS! Your perceptron learned the AND gate!'})
                else:
                    self.test_results.append({'message': f'Not quite right. Got {correct}/4 correct.'})
            else:
                self.test_results = [{'message': 'Error: Perceptron class not found'}]
                
        except Exception as e:
            self.test_results = [{'message': f'Error: {str(e)}'}]
    
    def render(self, screen):
        screen.fill((25, 35, 55))  # Clean dark blue background
        
        if self.step == 0:  # Explanation
            title = self.font.render("Perceptron Challenge", True, (255, 255, 255))
            screen.blit(title, (50, 50))
            
            explanation = [
                "The perceptron is the building block of neural networks!",
                "",
                "It works like this:",
                "1. Takes inputs (x1, x2, ...)",
                "2. Multiplies each by a weight (w1, w2, ...)",
                "3. Adds them up with a bias: sum(wi * xi) + bias",
                "4. Applies step function: output 1 if sum > 0, else 0",
                "",
                "Your mission: Implement a perceptron that learns the AND gate!",
                "",
                "Press SPACE to start coding..."
            ]
            
            for i, line in enumerate(explanation):
                text = pygame.font.Font(None, 24).render(line, True, (255, 255, 255))
                screen.blit(text, (50, 100 + i * 30))
        
        elif self.step == 1:  # Coding
            title = self.font.render("Code Your Perceptron", True, (255, 255, 255))
            screen.blit(title, (50, 20))
            
            # Instructions
            inst = pygame.font.Font(None, 20).render("Fill in the TODO sections. Press F5 to test your code.", True, (200, 200, 200))
            screen.blit(inst, (50, 50))
            
            # Code editor (simplified)
            code_lines = self.user_code.split('\n')
            for i, line in enumerate(code_lines[:25]):  # Show first 25 lines
                color = (255, 255, 255) if not line.strip().startswith('#') else (100, 255, 100)
                text = self.code_font.render(line[:80], True, color)  # Truncate long lines
                screen.blit(text, (50, 80 + i * 20))
        
        elif self.step == 2:  # Testing
            title = self.font.render("Test Results", True, (255, 255, 255))
            screen.blit(title, (50, 50))
            
            y_offset = 100
            for result in self.test_results:
                if 'message' in result:
                    color = (0, 255, 0) if 'SUCCESS' in result['message'] else (255, 100, 100)
                    text = self.font.render(result['message'], True, color)
                    screen.blit(text, (50, y_offset))
                    y_offset += 40
                else:
                    # Show test case
                    input_str = f"Input: {result['input']}"
                    expected_str = f"Expected: {result['expected']}"
                    predicted_str = f"Got: {result['predicted']:.1f}"
                    status = "✓" if result['correct'] else "✗"
                    
                    color = (0, 255, 0) if result['correct'] else (255, 100, 100)
                    
                    text = pygame.font.Font(None, 24).render(f"{status} {input_str} → {expected_str}, {predicted_str}", True, color)
                    screen.blit(text, (50, y_offset))
                    y_offset += 30
            
            if self.completed:
                next_text = "Press SPACE to continue to next level!"
            else:
                next_text = "Press SPACE to go back and fix your code"
            
            inst = pygame.font.Font(None, 24).render(next_text, True, (255, 255, 0))
            screen.blit(inst, (50, self.game.height - 100))
        
        # Always show escape instruction
        esc_text = pygame.font.Font(None, 20).render("Press ESC to return to world map", True, (150, 150, 150))
        screen.blit(esc_text, (50, self.game.height - 30))