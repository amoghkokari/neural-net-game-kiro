"""
Modern UI system with engaging visual effects and smooth animations
"""

import pygame
import math
import time
from typing import Tuple, List, Optional

class UIAnimator:
    """Handles smooth UI animations and transitions"""
    
    def __init__(self):
        self.animations = []
    
    def add_animation(self, target, property_name, start_value, end_value, duration, easing="ease_out"):
        """Add a smooth animation"""
        animation = {
            'target': target,
            'property': property_name,
            'start_value': start_value,
            'end_value': end_value,
            'duration': duration,
            'start_time': time.time(),
            'easing': easing
        }
        self.animations.append(animation)
    
    def update(self, dt):
        """Update all animations"""
        current_time = time.time()
        completed = []
        
        for i, anim in enumerate(self.animations):
            elapsed = current_time - anim['start_time']
            progress = min(elapsed / anim['duration'], 1.0)
            
            # Apply easing
            if anim['easing'] == "ease_out":
                progress = 1 - (1 - progress) ** 3
            elif anim['easing'] == "ease_in":
                progress = progress ** 3
            elif anim['easing'] == "bounce":
                progress = self._bounce_ease(progress)
            
            # Calculate current value
            start = anim['start_value']
            end = anim['end_value']
            
            if isinstance(start, (int, float)):
                current_value = start + (end - start) * progress
            elif isinstance(start, tuple):  # Color or position
                current_value = tuple(start[j] + (end[j] - start[j]) * progress for j in range(len(start)))
            
            # Set the property
            setattr(anim['target'], anim['property'], current_value)
            
            if progress >= 1.0:
                completed.append(i)
        
        # Remove completed animations
        for i in reversed(completed):
            self.animations.pop(i)
    
    def _bounce_ease(self, t):
        """Bounce easing function"""
        if t < 1/2.75:
            return 7.5625 * t * t
        elif t < 2/2.75:
            t -= 1.5/2.75
            return 7.5625 * t * t + 0.75
        elif t < 2.5/2.75:
            t -= 2.25/2.75
            return 7.5625 * t * t + 0.9375
        else:
            t -= 2.625/2.75
            return 7.5625 * t * t + 0.984375

class ModernButton:
    """Modern button with hover effects and animations"""
    
    def __init__(self, x, y, width, height, text, font, 
                 bg_color=(70, 130, 180), hover_color=(100, 149, 237), 
                 text_color=(255, 255, 255), border_radius=10):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_radius = border_radius
        
        # Animation properties
        self.current_color = bg_color
        self.scale = 1.0
        self.glow_intensity = 0.0
        
        # State
        self.is_hovered = False
        self.is_pressed = False
        self.enabled = True
    
    def update(self, mouse_pos, mouse_pressed, dt):
        """Update button state and animations"""
        if not self.enabled:
            return False
        
        # Check hover
        was_hovered = self.is_hovered
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        # Animate color
        target_color = self.hover_color if self.is_hovered else self.bg_color
        self.current_color = self._lerp_color(self.current_color, target_color, dt * 8)
        
        # Animate scale
        target_scale = 1.05 if self.is_hovered else 1.0
        self.scale += (target_scale - self.scale) * dt * 10
        
        # Animate glow
        target_glow = 0.3 if self.is_hovered else 0.0
        self.glow_intensity += (target_glow - self.glow_intensity) * dt * 8
        
        # Check click
        if self.is_hovered and mouse_pressed and not self.is_pressed:
            self.is_pressed = True
            return True
        
        if not mouse_pressed:
            self.is_pressed = False
        
        return False
    
    def render(self, screen):
        """Render the button with effects"""
        if not self.enabled:
            return
        
        # Calculate scaled rect
        center = self.rect.center
        scaled_width = int(self.rect.width * self.scale)
        scaled_height = int(self.rect.height * self.scale)
        scaled_rect = pygame.Rect(0, 0, scaled_width, scaled_height)
        scaled_rect.center = center
        
        # Draw glow effect
        if self.glow_intensity > 0:
            glow_color = (*self.hover_color, int(self.glow_intensity * 100))
            glow_rect = scaled_rect.inflate(20, 20)
            self._draw_rounded_rect_with_glow(screen, glow_rect, glow_color, self.border_radius + 10)
        
        # Draw main button
        self._draw_rounded_rect(screen, scaled_rect, self.current_color, self.border_radius)
        
        # Draw text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=center)
        screen.blit(text_surface, text_rect)
    
    def _lerp_color(self, color1, color2, t):
        """Linear interpolation between colors"""
        # Ensure colors are valid tuples with 3 components
        if len(color1) < 3 or len(color2) < 3:
            return (128, 128, 128)  # Default gray
        
        # Clamp t to valid range
        t = max(0.0, min(1.0, t))
        
        # Interpolate and clamp each component
        result = []
        for i in range(3):
            value = color1[i] + (color2[i] - color1[i]) * t
            result.append(max(0, min(255, int(value))))
        
        return tuple(result)
    
    def _draw_rounded_rect(self, screen, rect, color, radius):
        """Draw rounded rectangle"""
        # Validate color
        if not isinstance(color, (tuple, list)) or len(color) < 3:
            color = (128, 128, 128)  # Default gray
        
        # Ensure color values are valid
        color = tuple(max(0, min(255, int(c))) for c in color[:3])
        
        pygame.draw.rect(screen, color, rect, border_radius=radius)
    
    def _draw_rounded_rect_with_glow(self, screen, rect, color, radius):
        """Draw rounded rectangle with glow effect"""
        # Create temporary surface for glow
        glow_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        pygame.draw.rect(glow_surface, color, (0, 0, rect.width, rect.height), border_radius=radius)
        screen.blit(glow_surface, rect.topleft, special_flags=pygame.BLEND_ALPHA_SDL2)

class ProgressBar:
    """Animated progress bar with modern styling"""
    
    def __init__(self, x, y, width, height, max_value=100):
        self.rect = pygame.Rect(x, y, width, height)
        self.max_value = max_value
        self.current_value = 0
        self.display_value = 0  # For smooth animation
        self.bg_color = (40, 40, 40)
        self.fill_color = (0, 255, 100)
        self.border_color = (100, 100, 100)
        self.text_color = (255, 255, 255)
    
    def set_value(self, value):
        """Set progress value (will animate to this value)"""
        self.current_value = max(0, min(value, self.max_value))
    
    def update(self, dt):
        """Update animation"""
        self.display_value += (self.current_value - self.display_value) * dt * 5
    
    def render(self, screen, font=None):
        """Render progress bar"""
        # Background
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=5)
        
        # Fill
        fill_width = int((self.display_value / self.max_value) * self.rect.width)
        if fill_width > 0:
            fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
            pygame.draw.rect(screen, self.fill_color, fill_rect, border_radius=5)
        
        # Border
        pygame.draw.rect(screen, self.border_color, self.rect, 2, border_radius=5)
        
        # Text
        if font:
            percentage = int((self.display_value / self.max_value) * 100)
            text = f"{percentage}%"
            text_surface = font.render(text, True, self.text_color)
            text_rect = text_surface.get_rect(center=self.rect.center)
            screen.blit(text_surface, text_rect)

class DialogueBox:
    """Modern dialogue box with typewriter effect and character portraits"""
    
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.bg_color = (20, 25, 40, 220)  # Semi-transparent
        self.border_color = (100, 150, 255)
        self.text_color = (255, 255, 255)
        self.name_color = (255, 255, 100)
        
        # Typewriter effect
        self.full_text = ""
        self.displayed_text = ""
        self.char_index = 0
        self.type_speed = 50  # Characters per second
        self.last_char_time = 0
        
        # Character info
        self.character_name = ""
        self.character_portrait = None
        
        # Animation
        self.slide_offset = 0
        self.target_offset = 0
    
    def set_dialogue(self, text, character_name="", portrait=None):
        """Set new dialogue text"""
        self.full_text = text
        self.displayed_text = ""
        self.char_index = 0
        self.character_name = character_name
        self.character_portrait = portrait
        self.last_char_time = time.time()
    
    def update(self, dt):
        """Update typewriter effect"""
        current_time = time.time()
        
        # Typewriter effect
        if self.char_index < len(self.full_text):
            chars_to_add = int((current_time - self.last_char_time) * self.type_speed)
            if chars_to_add > 0:
                self.char_index = min(self.char_index + chars_to_add, len(self.full_text))
                self.displayed_text = self.full_text[:self.char_index]
                self.last_char_time = current_time
        
        # Slide animation
        self.slide_offset += (self.target_offset - self.slide_offset) * dt * 8
    
    def render(self, screen, font, name_font=None):
        """Render dialogue box"""
        # Calculate position with slide offset
        render_rect = self.rect.copy()
        render_rect.y += int(self.slide_offset)
        
        # Background with transparency
        bg_surface = pygame.Surface((render_rect.width, render_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(bg_surface, self.bg_color, (0, 0, render_rect.width, render_rect.height), border_radius=15)
        screen.blit(bg_surface, render_rect.topleft)
        
        # Border
        pygame.draw.rect(screen, self.border_color, render_rect, 3, border_radius=15)
        
        # Character name
        if self.character_name and name_font:
            name_surface = name_font.render(self.character_name, True, self.name_color)
            name_rect = pygame.Rect(render_rect.x + 20, render_rect.y + 10, name_surface.get_width(), name_surface.get_height())
            screen.blit(name_surface, name_rect)
            text_start_y = name_rect.bottom + 10
        else:
            text_start_y = render_rect.y + 20
        
        # Text with word wrapping
        self._render_wrapped_text(screen, self.displayed_text, font, 
                                render_rect.x + 20, text_start_y, 
                                render_rect.width - 40, self.text_color)
    
    def _render_wrapped_text(self, screen, text, font, x, y, max_width, color):
        """Render text with word wrapping"""
        words = text.split(' ')
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                    current_line = word + " "
                else:
                    # Single word is too long, force it
                    lines.append(word)
                    current_line = ""
        
        if current_line:
            lines.append(current_line.strip())
        
        # Render lines with better spacing
        line_height = font.get_height() + 3
        available_height = self.rect.height - (y - self.rect.y) - 20  # Leave some bottom padding
        max_lines = max(1, int(available_height / line_height))
        
        for i, line in enumerate(lines[:max_lines]):  # Only render lines that fit
            if line:
                text_surface = font.render(line, True, color)
                screen.blit(text_surface, (x, y + i * line_height))
    
    def is_complete(self):
        """Check if typewriter effect is complete"""
        return self.char_index >= len(self.full_text)
    
    def skip_to_end(self):
        """Skip typewriter effect to show full text"""
        self.char_index = len(self.full_text)
        self.displayed_text = self.full_text
    
    def show(self):
        """Animate dialogue box into view"""
        self.target_offset = 0
    
    def hide(self):
        """Animate dialogue box out of view"""
        self.target_offset = 200

class ParticleSystem:
    """Particle system for visual effects"""
    
    def __init__(self):
        self.particles = []
    
    def add_particle(self, x, y, velocity, color, lifetime, size=3):
        """Add a new particle"""
        particle = {
            'x': x,
            'y': y,
            'vx': velocity[0],
            'vy': velocity[1],
            'color': color,
            'lifetime': lifetime,
            'max_lifetime': lifetime,
            'size': size
        }
        self.particles.append(particle)
    
    def update(self, dt):
        """Update all particles"""
        for particle in self.particles[:]:
            particle['x'] += particle['vx'] * dt
            particle['y'] += particle['vy'] * dt
            particle['lifetime'] -= dt
            
            # Apply gravity
            particle['vy'] += 200 * dt
            
            if particle['lifetime'] <= 0:
                self.particles.remove(particle)
    
    def render(self, screen):
        """Render all particles"""
        for particle in self.particles:
            alpha = particle['lifetime'] / particle['max_lifetime']
            color = (*particle['color'][:3], int(alpha * 255))
            
            # Create surface for alpha blending
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, color, (particle['size'], particle['size']), particle['size'])
            screen.blit(particle_surface, (int(particle['x'] - particle['size']), int(particle['y'] - particle['size'])))
    
    def create_explosion(self, x, y, color, count=20):
        """Create explosion effect"""
        import random
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 200)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            lifetime = random.uniform(0.5, 1.5)
            size = random.randint(2, 5)
            self.add_particle(x, y, (vx, vy), color, lifetime, size)