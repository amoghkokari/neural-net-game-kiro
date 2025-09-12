"""
Interactive Perceptron Trainer
Learn how perceptrons work by dragging the decision line!
"""

import pygame
import numpy as np
import random
import math
import time

try:
    from ..challenges.base_challenge import BaseChallenge
    from ..ui.modern_ui import DialogueBox, ParticleSystem
except ImportError:
    from challenges.base_challenge import BaseChallenge
    from ui.modern_ui import DialogueBox, ParticleSystem

class PerceptronSimple(BaseChallenge):
    """
    Interactive perceptron trainer - drag the line to separate the dots!
    """
    
    def __init__(self, game):
        super().__init__(game)
        
        # Screen dimensions
        self.width = game.width
        self.height = game.height
        
        # Colors - modern, clean palette
        self.bg_color = (25, 30, 40)
        self.primary_color = (64, 156, 255)  # Blue
        self.success_color = (46, 204, 113)  # Green
        self.error_color = (231, 76, 60)     # Red
        self.warning_color = (255, 193, 7)   # Yellow
        self.text_color = (255, 255, 255)
        self.secondary_text = (180, 180, 180)
        
        # Fonts - large and readable
        self.title_font = pygame.font.Font(None, 48)
        self.header_font = pygame.font.Font(None, 32)
        self.body_font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)
        
        # Game state
        self.phase = "learn"  # learn -> practice -> complete
        self.score = 0
        self.attempts = 0
        self.max_attempts = 10
        
        # Perceptron parameters (start with obviously wrong line)
        self.line_angle = 45  # degrees
        self.line_position = 0  # -1 to 1, position along perpendicular
        
        # Training data - clearly separable points
        self.points = self._generate_clear_data()
        
        # Interaction
        self.dragging_line = False
        self.mouse_pos = (0, 0)
        
        # Visual elements
        self.particles = ParticleSystem()
        self.feedback_text = ""
        self.feedback_timer = 0
        self.feedback_color = self.text_color
        
        # Animation
        self.pulse_timer = 0
        self.line_glow = 0
        
        # Visualization area
        self.viz_rect = pygame.Rect(self.width // 2 - 200, 120, 400, 400)
        
        # Dialogue
        self.dialogue = DialogueBox(50, self.height - 120, self.width - 100, 80)
        self._start_learning()
    
    def _generate_clear_data(self):
        """Generate clearly separable training data"""
        points = []
        
        # Green points (class 1) - upper right
        for _ in range(8):
            x = random.uniform(0.2, 0.8)
            y = random.uniform(0.2, 0.8)
            points.append({'pos': (x, y), 'label': 1, 'color': self.success_color})
        
        # Red points (class 0) - lower left  
        for _ in range(8):
            x = random.uniform(-0.8, -0.2)
            y = random.uniform(-0.8, -0.2)
            points.append({'pos': (x, y), 'label': 0, 'color': self.error_color})
        
        return points
    
    def _start_learning(self):
        """Start the learning phase"""
        learn_text = "🎯 DRAG the yellow line to separate GREEN and RED dots! Try to get all green dots above the line and red dots below."
        self.dialogue.set_dialogue(learn_text, "Perceptron Trainer")
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                # Check if clicking near the line
                if self._is_near_line(event.pos):
                    self.dragging_line = True
                    self.line_glow = 1.0
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if self.dragging_line:
                    self.dragging_line = False
                    self.line_glow = 0.0
                    self._check_solution()
        
        elif event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
            if self.dragging_line:
                self._update_line_from_mouse(event.pos)
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.phase == "complete":
                    self.completed = True
                    return "completed"
                else:
                    self._check_solution()
            elif event.key == pygame.K_r:
                self._reset_line()
            elif event.key == pygame.K_ESCAPE:
                if self.phase == "complete":
                    self.completed = True
                    return "completed"
        
        return None
    
    def _is_near_line(self, mouse_pos):
        """Check if mouse is near the decision line"""
        if not self.viz_rect.collidepoint(mouse_pos):
            return False
        
        # Convert mouse to visualization coordinates
        rel_x = (mouse_pos[0] - self.viz_rect.x) / self.viz_rect.width - 0.5
        rel_y = 0.5 - (mouse_pos[1] - self.viz_rect.y) / self.viz_rect.height
        
        # Calculate distance to line
        distance = self._point_distance_to_line(rel_x, rel_y)
        return distance < 0.1  # Within 10% of the visualization area
    
    def _point_distance_to_line(self, x, y):
        """Calculate distance from point to the decision line"""
        # Line equation: ax + by + c = 0
        # Convert angle and position to line parameters
        angle_rad = math.radians(self.line_angle)
        a = math.sin(angle_rad)
        b = -math.cos(angle_rad)
        c = self.line_position
        
        # Distance formula: |ax + by + c| / sqrt(a² + b²)
        return abs(a * x + b * y + c) / math.sqrt(a * a + b * b)
    
    def _update_line_from_mouse(self, mouse_pos):
        """Update line parameters based on mouse position"""
        if not self.viz_rect.collidepoint(mouse_pos):
            return
        
        # Convert mouse to visualization coordinates
        rel_x = (mouse_pos[0] - self.viz_rect.x) / self.viz_rect.width - 0.5
        rel_y = 0.5 - (mouse_pos[1] - self.viz_rect.y) / self.viz_rect.height
        
        # Update line angle based on mouse movement
        center_x = 0
        center_y = 0
        
        if abs(rel_x - center_x) > 0.01:  # Avoid division by zero
            angle_rad = math.atan2(rel_y - center_y, rel_x - center_x)
            self.line_angle = math.degrees(angle_rad) + 90  # Perpendicular to mouse direction
        
        # Update line position (distance from center)
        self.line_position = (rel_x * math.sin(math.radians(self.line_angle)) - 
                             rel_y * math.cos(math.radians(self.line_angle))) * 0.5
        
        # Clamp values
        self.line_angle = self.line_angle % 360
        self.line_position = max(-0.8, min(0.8, self.line_position))
    
    def _check_solution(self):
        """Check if the current line correctly separates the points"""
        correct = 0
        total = len(self.points)
        
        for point in self.points:
            x, y = point['pos']
            predicted = self._classify_point(x, y)
            if predicted == point['label']:
                correct += 1
        
        accuracy = (correct / total) * 100
        self.attempts += 1
        
        if accuracy >= 90:
            self.score += 1
            self.feedback_text = f"PERFECT! {accuracy:.0f}% accuracy!"
            self.feedback_color = self.success_color
            self._add_celebration_particles()
            
            if self.score >= 3:
                self.phase = "complete"
                complete_text = "🏆 PERCEPTRON MASTERED! You understand how linear classifiers work! Press SPACE or ESC to continue your journey!"
                self.dialogue.set_dialogue(complete_text, "🎓 Challenge Complete")
            else:
                next_text = f"Great! Score: {self.score}/3. Try another configuration! (R to reset line)"
                self.dialogue.set_dialogue(next_text, "Perceptron Trainer")
                self._generate_new_points()
        
        elif accuracy >= 70:
            self.feedback_text = f"Good! {accuracy:.0f}% - Try adjusting the line"
            self.feedback_color = self.warning_color
            adjust_text = f"Close! {accuracy:.0f}% accuracy. Drag the line to improve separation."
            self.dialogue.set_dialogue(adjust_text, "Perceptron Trainer")
        
        else:
            self.feedback_text = f"Keep trying! {accuracy:.0f}%"
            self.feedback_color = self.error_color
            help_text = f"Only {accuracy:.0f}% correct. Drag the yellow line to separate green and red dots better!"
            self.dialogue.set_dialogue(help_text, "Perceptron Trainer")
        
        self.feedback_timer = 2.0
    
    def _classify_point(self, x, y):
        """Classify a point using the current line"""
        # Line equation: ax + by + c = 0
        angle_rad = math.radians(self.line_angle)
        a = math.sin(angle_rad)
        b = -math.cos(angle_rad)
        c = self.line_position
        
        # Point is above line if ax + by + c > 0
        return 1 if (a * x + b * y + c) > 0 else 0
    
    def _reset_line(self):
        """Reset line to default position"""
        self.line_angle = 45
        self.line_position = 0
        self.feedback_text = "Line reset!"
        self.feedback_color = self.primary_color
        self.feedback_timer = 1.0
    
    def _generate_new_points(self):
        """Generate a new set of points for the next challenge"""
        self.points = self._generate_clear_data()
        self._reset_line()
    
    def _add_celebration_particles(self):
        """Add celebration particles"""
        center_x = self.viz_rect.centerx
        center_y = self.viz_rect.centery
        
        for _ in range(15):
            self.particles.add_particle(
                center_x + random.randint(-50, 50),
                center_y + random.randint(-50, 50),
                (random.uniform(-100, 100), random.uniform(-150, -50)),
                random.choice([self.success_color, self.warning_color, self.primary_color]),
                random.uniform(1.0, 2.0),
                random.randint(6, 12)
            )
    
    def is_completed(self):
        """Check if the challenge is completed"""
        return self.phase == "complete"
    
    def update(self, dt):
        """Update the challenge"""
        self.pulse_timer += dt * 2
        self.particles.update(dt)
        self.dialogue.update(dt)
        
        if self.feedback_timer > 0:
            self.feedback_timer -= dt
        
        if self.line_glow > 0:
            self.line_glow -= dt * 2
    
    def render(self, screen):
        """Render the challenge"""
        # Clear screen
        screen.fill(self.bg_color)
        
        # Render title
        self._render_title(screen)
        
        # Render main training area
        self._render_training_area(screen)
        
        # Render stats
        self._render_stats(screen)
        
        # Render feedback
        if self.feedback_timer > 0:
            self._render_feedback(screen)
        
        # Render particles
        self.particles.render(screen)
        
        # Render dialogue
        self.dialogue.render(screen, self.body_font, self.header_font)
    
    def _render_title(self, screen):
        """Render the title"""
        if self.phase == "complete":
            title_text = "🏆 PERCEPTRON MASTERED! 🏆"
            color = self.success_color
        else:
            title_text = "🧠 Perceptron Training Lab"
            color = self.primary_color
            
        title_surface = self.title_font.render(title_text, True, color)
        title_rect = title_surface.get_rect(center=(self.width // 2, 50))
        screen.blit(title_surface, title_rect)
    
    def _render_training_area(self, screen):
        """Render the interactive training visualization"""
        # Draw background
        pygame.draw.rect(screen, (35, 40, 50), self.viz_rect, border_radius=15)
        pygame.draw.rect(screen, self.primary_color, self.viz_rect, 3, border_radius=15)
        
        # Draw coordinate grid
        self._draw_grid(screen)
        
        # Draw decision line
        self._draw_decision_line(screen)
        
        # Draw training points
        for point in self.points:
            self._draw_point(screen, point)
        
        # Draw instructions
        self._draw_instructions(screen)
    
    def _draw_grid(self, screen):
        """Draw a subtle grid"""
        center_x = self.viz_rect.centerx
        center_y = self.viz_rect.centery
        
        # Draw center lines
        pygame.draw.line(screen, (60, 70, 80), 
                        (self.viz_rect.left + 20, center_y), 
                        (self.viz_rect.right - 20, center_y), 1)
        pygame.draw.line(screen, (60, 70, 80), 
                        (center_x, self.viz_rect.top + 20), 
                        (center_x, self.viz_rect.bottom - 20), 1)
    
    def _draw_decision_line(self, screen):
        """Draw the interactive decision line"""
        # Calculate line endpoints
        angle_rad = math.radians(self.line_angle)
        
        # Line direction vector
        dx = math.cos(angle_rad)
        dy = math.sin(angle_rad)
        
        # Line center point (offset by position)
        offset_x = -self.line_position * math.sin(angle_rad)
        offset_y = self.line_position * math.cos(angle_rad)
        
        center_x = self.viz_rect.centerx + offset_x * self.viz_rect.width * 0.4
        center_y = self.viz_rect.centery + offset_y * self.viz_rect.height * 0.4
        
        # Calculate endpoints
        length = max(self.viz_rect.width, self.viz_rect.height)
        x1 = center_x - dx * length
        y1 = center_y - dy * length
        x2 = center_x + dx * length
        y2 = center_y + dy * length
        
        # Clip to visualization area
        x1 = max(self.viz_rect.left, min(self.viz_rect.right, x1))
        y1 = max(self.viz_rect.top, min(self.viz_rect.bottom, y1))
        x2 = max(self.viz_rect.left, min(self.viz_rect.right, x2))
        y2 = max(self.viz_rect.top, min(self.viz_rect.bottom, y2))
        
        # Draw line with glow effect if being dragged
        line_color = self.warning_color
        line_width = 4
        
        if self.dragging_line or self.line_glow > 0:
            # Draw glow
            glow_width = int(8 + self.line_glow * 4)
            glow_color = tuple(int(c * 0.5) for c in line_color)
            pygame.draw.line(screen, glow_color, (x1, y1), (x2, y2), glow_width)
        
        # Draw main line
        pygame.draw.line(screen, line_color, (x1, y1), (x2, y2), line_width)
        
        # Draw drag handle at center
        handle_size = 8 if not self.dragging_line else 12
        pygame.draw.circle(screen, line_color, (int(center_x), int(center_y)), handle_size)
        pygame.draw.circle(screen, self.text_color, (int(center_x), int(center_y)), handle_size, 2)
    
    def _draw_instructions(self, screen):
        """Draw helpful instructions"""
        # Region labels
        label_font = self.small_font
        
        # Find a good spot for green label (above line)
        green_label = label_font.render("GREEN ZONE", True, self.success_color)
        screen.blit(green_label, (self.viz_rect.left + 10, self.viz_rect.top + 10))
        
        # Red label (below line)
        red_label = label_font.render("RED ZONE", True, self.error_color)
        screen.blit(red_label, (self.viz_rect.left + 10, self.viz_rect.bottom - 30))
        
        # Drag instruction
        if not self.dragging_line and self.attempts < 2:
            drag_text = "👆 DRAG the yellow line!"
            drag_surface = self.body_font.render(drag_text, True, self.warning_color)
            drag_rect = drag_surface.get_rect(center=(self.viz_rect.centerx, self.viz_rect.bottom + 30))
            screen.blit(drag_surface, drag_rect)
    
    def _draw_decision_boundary(self, screen, viz_rect):
        """Draw the perceptron's decision boundary"""
        if abs(self.weights[1]) < 1e-6:  # Avoid division by zero
            return
        
        # Calculate line points: w1*x + w2*y + bias = 0 => y = -(w1*x + bias)/w2
        x_range = 4  # -2 to 2 in data space
        
        # Left edge
        x1_data = -2
        y1_data = -(self.weights[0] * x1_data + self.bias) / self.weights[1]
        
        # Right edge
        x2_data = 2
        y2_data = -(self.weights[0] * x2_data + self.bias) / self.weights[1]
        
        # Convert to screen coordinates
        x1_screen, y1_screen = self._point_to_screen_in_rect(np.array([x1_data, y1_data]), viz_rect)
        x2_screen, y2_screen = self._point_to_screen_in_rect(np.array([x2_data, y2_data]), viz_rect)
        
        # Draw the line
        if (viz_rect.top <= y1_screen <= viz_rect.bottom and 
            viz_rect.top <= y2_screen <= viz_rect.bottom):
            pygame.draw.line(screen, (255, 255, 100), 
                           (x1_screen, y1_screen), (x2_screen, y2_screen), 3)
    
    def _draw_point(self, screen, point_data):
        """Draw a training point"""
        x, y = point_data['pos']
        label = point_data['label']
        color = point_data['color']
        
        # Convert to screen coordinates
        screen_x = self.viz_rect.centerx + x * self.viz_rect.width * 0.4
        screen_y = self.viz_rect.centery - y * self.viz_rect.height * 0.4
        
        # Check if point is correctly classified
        predicted = self._classify_point(x, y)
        is_correct = predicted == label
        
        # Choose visual style
        if is_correct:
            # Correct classification - solid color
            radius = 12
            border_color = self.text_color
            border_width = 2
        else:
            # Wrong classification - pulsing red border
            radius = 12
            pulse = math.sin(self.pulse_timer * 4) * 0.5 + 0.5
            border_color = tuple(int(self.error_color[i] * pulse + self.text_color[i] * (1 - pulse)) for i in range(3))
            border_width = 3
        
        # Draw point
        pygame.draw.circle(screen, color, (int(screen_x), int(screen_y)), radius)
        pygame.draw.circle(screen, border_color, (int(screen_x), int(screen_y)), radius, border_width)
        
        # Draw label
        label_text = "G" if label == 1 else "R"
        label_surface = self.small_font.render(label_text, True, self.text_color)
        label_rect = label_surface.get_rect(center=(int(screen_x), int(screen_y)))
        screen.blit(label_surface, label_rect)
    
    def _point_to_screen_in_rect(self, point, rect):
        """Convert data point to screen coordinates within a rectangle"""
        # Data space is -2 to 2 for both x and y
        data_range = 4
        
        # Convert to 0-1 range
        norm_x = (point[0] + 2) / data_range
        norm_y = (point[1] + 2) / data_range
        
        # Convert to screen coordinates (flip y)
        screen_x = rect.left + norm_x * rect.width
        screen_y = rect.bottom - norm_y * rect.height
        
        return screen_x, screen_y
    
    def _point_to_screen(self, point):
        """Convert data point to screen coordinates"""
        # Simple conversion for particle effects
        screen_x = self.width // 2 + point[0] * 50
        screen_y = self.height // 2 - point[1] * 50
        return screen_x, screen_y
    
    def _render_stats(self, screen):
        """Render statistics and progress"""
        stats_x = 50
        stats_y = 120
        
        # Background
        stats_rect = pygame.Rect(stats_x - 20, stats_y - 10, 280, 100)
        pygame.draw.rect(screen, (35, 40, 50), stats_rect, border_radius=8)
        pygame.draw.rect(screen, self.primary_color, stats_rect, 2, border_radius=8)
        
        # Calculate current accuracy
        correct = sum(1 for point in self.points if self._classify_point(*point['pos']) == point['label'])
        accuracy = (correct / len(self.points)) * 100 if self.points else 0
        
        # Stats text
        stats = [
            f"🎯 Score: {self.score}/3 challenges completed",
            f"📊 Current Accuracy: {accuracy:.0f}% ({correct}/{len(self.points)})",
            f"🔄 Attempts: {self.attempts}",
            "",
            "💡 Drag the yellow line to separate dots!"
        ]
        
        for i, stat in enumerate(stats):
            if stat:  # Skip empty lines
                color = self.text_color if i < 3 else self.secondary_text
                font = self.small_font if i < 3 else self.small_font
                stat_surface = font.render(stat, True, color)
                screen.blit(stat_surface, (stats_x, stats_y + i * 18))
    
    def _render_feedback(self, screen):
        """Render classification feedback"""
        if not self.feedback_text:
            return
        
        # Create pulsing effect
        alpha = min(255, int(self.feedback_timer * 127.5))
        
        feedback_surface = self.header_font.render(self.feedback_text, True, self.feedback_color)
        feedback_rect = feedback_surface.get_rect(center=(self.width // 2, self.height // 2 - 100))
        
        # Add background for better visibility
        bg_rect = feedback_rect.inflate(40, 20)
        bg_surface = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
        bg_surface.fill((*self.bg_color, alpha))
        screen.blit(bg_surface, bg_rect)
        
        screen.blit(feedback_surface, feedback_rect)