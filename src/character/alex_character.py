"""
Alex - The protagonist character with progression system
"""

import pygame
import math
import random

class AlexCharacter:
    def __init__(self):
        # Character stats
        self.level = 1
        self.experience = 0
        self.experience_to_next_level = 100
        
        # Combat stats
        self.hp = 100
        self.max_hp = 100
        self.mp = 50
        self.max_mp = 50
        self.attack_power = 10
        
        # Skills unlocked through progression
        self.skills = {
            'neuron_mastery': 0,      # 0-100
            'weight_control': 0,      # 0-100
            'bias_manipulation': 0,   # 0-100
            'activation_power': 0,    # 0-100
            'gradient_flow': 0,       # 0-100
            'network_building': 0,    # 0-100
        }
        
        # Combat abilities
        self.abilities = {
            'weight_strike': {'mp_cost': 10, 'damage': 15, 'unlocked': True},
            'bias_blast': {'mp_cost': 15, 'damage': 20, 'unlocked': False},
            'activation_surge': {'mp_cost': 20, 'damage': 25, 'unlocked': False},
            'gradient_storm': {'mp_cost': 25, 'damage': 30, 'unlocked': False}
        }
        
        # Visual appearance that changes with level
        self.appearance = {
            'body_color': (100, 150, 255),  # Blue shirt
            'hair_color': (139, 69, 19),    # Brown hair
            'skin_color': (255, 220, 177),  # Skin tone
            'eye_color': (0, 100, 0),       # Green eyes
            'accessories': [],              # Unlocked accessories
            'aura_color': None,             # Special aura when high level
            'size_multiplier': 1.0,         # Gets slightly bigger with level
        }
        
        # Animation state
        self.animation_time = 0
        self.current_animation = 'idle'
        self.animation_frame = 0
        
        # Position and movement
        self.x = 100
        self.y = 300
        self.target_x = 100
        self.target_y = 300
        
        # Particle effects
        self.level_up_particles = []
        self.skill_particles = []
        
    def gain_experience(self, amount):
        """Gain experience and potentially level up"""
        self.experience += amount
        
        # Check for level up
        while self.experience >= self.experience_to_next_level:
            self.level_up()
    
    def level_up(self):
        """Level up the character"""
        self.experience -= self.experience_to_next_level
        self.level += 1
        self.experience_to_next_level = int(self.experience_to_next_level * 1.2)
        
        # Increase stats
        self.max_hp += 20
        self.hp = self.max_hp  # Full heal on level up
        self.max_mp += 10
        self.mp = self.max_mp  # Full MP restore
        self.attack_power += 5
        
        # Unlock abilities
        if self.level >= 3:
            self.abilities['bias_blast']['unlocked'] = True
        if self.level >= 5:
            self.abilities['activation_surge']['unlocked'] = True
        if self.level >= 7:
            self.abilities['gradient_storm']['unlocked'] = True
        
        # Update appearance
        self._update_appearance()
        
        # Create level up particles
        self._create_level_up_particles()
        
        # Play level up animation
        self.current_animation = 'level_up'
        self.animation_frame = 0
    
    def gain_skill(self, skill_name, amount):
        """Gain skill points in a specific area"""
        if skill_name in self.skills:
            old_value = self.skills[skill_name]
            self.skills[skill_name] = min(100, self.skills[skill_name] + amount)
            
            # Create skill particles if significant gain
            if self.skills[skill_name] - old_value >= 10:
                self._create_skill_particles(skill_name)
    
    def use_ability(self, ability_name):
        """Use a combat ability"""
        if ability_name in self.abilities:
            ability = self.abilities[ability_name]
            if ability['unlocked'] and self.mp >= ability['mp_cost']:
                self.mp -= ability['mp_cost']
                return ability['damage']
        return 0
    
    def restore_mp(self, amount):
        """Restore MP"""
        self.mp = min(self.max_mp, self.mp + amount)
    
    def take_damage(self, damage):
        """Take damage"""
        self.hp = max(0, self.hp - damage)
        return self.hp <= 0  # Return True if defeated
    
    def _update_appearance(self):
        """Update character appearance based on level"""
        # Size increases slightly with level
        self.appearance['size_multiplier'] = 1.0 + (self.level - 1) * 0.1
        
        # Unlock accessories at certain levels
        if self.level >= 3 and 'neural_headband' not in self.appearance['accessories']:
            self.appearance['accessories'].append('neural_headband')
        
        if self.level >= 5 and 'gradient_gloves' not in self.appearance['accessories']:
            self.appearance['accessories'].append('gradient_gloves')
        
        if self.level >= 7 and 'activation_cape' not in self.appearance['accessories']:
            self.appearance['accessories'].append('activation_cape')
        
        # High level characters get an aura
        if self.level >= 10:
            self.appearance['aura_color'] = (255, 255, 100, 100)  # Golden aura
        elif self.level >= 5:
            self.appearance['aura_color'] = (100, 255, 100, 80)   # Green aura
    
    def _create_level_up_particles(self):
        """Create particles for level up effect"""
        for _ in range(20):
            particle = {
                'x': self.x + random.randint(-30, 30),
                'y': self.y + random.randint(-30, 30),
                'vx': random.uniform(-50, 50),
                'vy': random.uniform(-100, -20),
                'color': (255, 255, 0),
                'lifetime': random.uniform(1.0, 2.0),
                'max_lifetime': random.uniform(1.0, 2.0),
                'size': random.randint(3, 8)
            }
            self.level_up_particles.append(particle)
    
    def _create_skill_particles(self, skill_name):
        """Create particles for skill gain"""
        skill_colors = {
            'neuron_mastery': (100, 150, 255),
            'weight_control': (255, 100, 100),
            'bias_manipulation': (100, 255, 100),
            'activation_power': (255, 255, 100),
            'gradient_flow': (255, 100, 255),
            'network_building': (100, 255, 255)
        }
        
        color = skill_colors.get(skill_name, (255, 255, 255))
        
        for _ in range(10):
            particle = {
                'x': self.x + random.randint(-20, 20),
                'y': self.y + random.randint(-20, 20),
                'vx': random.uniform(-30, 30),
                'vy': random.uniform(-50, -10),
                'color': color,
                'lifetime': random.uniform(0.5, 1.5),
                'max_lifetime': random.uniform(0.5, 1.5),
                'size': random.randint(2, 5)
            }
            self.skill_particles.append(particle)
    
    def move_to(self, x, y):
        """Move character to a new position"""
        self.target_x = x
        self.target_y = y
        self.current_animation = 'walking'
    
    def update(self, dt):
        """Update character state"""
        self.animation_time += dt
        
        # Move towards target position
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        
        if abs(dx) > 5 or abs(dy) > 5:
            self.x += dx * dt * 3
            self.y += dy * dt * 3
            self.current_animation = 'walking'
        else:
            self.x = self.target_x
            self.y = self.target_y
            if self.current_animation == 'walking':
                self.current_animation = 'idle'
        
        # Update animation frame
        if self.current_animation == 'level_up':
            self.animation_frame += dt * 10
            if self.animation_frame >= 20:  # Level up animation duration
                self.current_animation = 'idle'
                self.animation_frame = 0
        else:
            self.animation_frame += dt * 5
        
        # Update particles
        self._update_particles(dt)
    
    def _update_particles(self, dt):
        """Update all particle effects"""
        # Update level up particles
        for particle in self.level_up_particles[:]:
            particle['x'] += particle['vx'] * dt
            particle['y'] += particle['vy'] * dt
            particle['vy'] += 200 * dt  # Gravity
            particle['lifetime'] -= dt
            
            if particle['lifetime'] <= 0:
                self.level_up_particles.remove(particle)
        
        # Update skill particles
        for particle in self.skill_particles[:]:
            particle['x'] += particle['vx'] * dt
            particle['y'] += particle['vy'] * dt
            particle['vy'] += 150 * dt  # Gravity
            particle['lifetime'] -= dt
            
            if particle['lifetime'] <= 0:
                self.skill_particles.remove(particle)
    
    def render(self, screen):
        """Render the character"""
        size = int(40 * self.appearance['size_multiplier'])
        
        # Draw aura if character has one
        if self.appearance['aura_color']:
            aura_size = size + 20
            aura_pulse = abs(math.sin(self.animation_time * 3)) * 10 + 10
            aura_surface = pygame.Surface((aura_size + aura_pulse, aura_size + aura_pulse), pygame.SRCALPHA)
            pygame.draw.circle(aura_surface, self.appearance['aura_color'], 
                             (aura_size//2 + aura_pulse//2, aura_size//2 + aura_pulse//2), 
                             aura_size//2 + aura_pulse//2)
            screen.blit(aura_surface, (self.x - aura_size//2 - aura_pulse//2, 
                                     self.y - aura_size//2 - aura_pulse//2))
        
        # Animation offset
        bob_offset = 0
        if self.current_animation == 'idle':
            bob_offset = math.sin(self.animation_time * 2) * 3
        elif self.current_animation == 'walking':
            bob_offset = math.sin(self.animation_time * 8) * 5
        elif self.current_animation == 'level_up':
            bob_offset = math.sin(self.animation_frame) * 10
        
        char_y = self.y + bob_offset
        
        # Draw cape (if unlocked)
        if 'activation_cape' in self.appearance['accessories']:
            cape_points = [
                (self.x - size//3, char_y - size//2),
                (self.x - size//2, char_y + size//2),
                (self.x - size//4, char_y + size//3),
                (self.x + size//4, char_y + size//3),
                (self.x + size//2, char_y + size//2),
                (self.x + size//3, char_y - size//2)
            ]
            pygame.draw.polygon(screen, (150, 0, 150), cape_points)
        
        # Draw body (circle for simplicity)
        pygame.draw.circle(screen, self.appearance['body_color'], 
                         (int(self.x), int(char_y)), size//2)
        
        # Draw head
        head_size = size//3
        pygame.draw.circle(screen, self.appearance['skin_color'], 
                         (int(self.x), int(char_y - size//3)), head_size)
        
        # Draw hair
        hair_rect = pygame.Rect(self.x - head_size, char_y - size//2, head_size*2, head_size)
        pygame.draw.ellipse(screen, self.appearance['hair_color'], hair_rect)
        
        # Draw eyes
        eye_size = 3
        left_eye = (int(self.x - head_size//3), int(char_y - size//3 - 3))
        right_eye = (int(self.x + head_size//3), int(char_y - size//3 - 3))
        pygame.draw.circle(screen, self.appearance['eye_color'], left_eye, eye_size)
        pygame.draw.circle(screen, self.appearance['eye_color'], right_eye, eye_size)
        
        # Draw neural headband (if unlocked)
        if 'neural_headband' in self.appearance['accessories']:
            headband_rect = pygame.Rect(self.x - head_size, char_y - size//2 + 5, head_size*2, 8)
            pygame.draw.rect(screen, (0, 255, 255), headband_rect)
            # Neural pattern on headband
            for i in range(3):
                dot_x = self.x - head_size + 10 + i * 15
                pygame.draw.circle(screen, (255, 255, 255), (int(dot_x), int(char_y - size//2 + 9)), 2)
        
        # Draw gradient gloves (if unlocked)
        if 'gradient_gloves' in self.appearance['accessories']:
            # Left glove
            left_hand = (int(self.x - size//2), int(char_y))
            pygame.draw.circle(screen, (255, 100, 0), left_hand, 8)
            # Right glove
            right_hand = (int(self.x + size//2), int(char_y))
            pygame.draw.circle(screen, (255, 100, 0), right_hand, 8)
        
        # Draw level indicator
        level_text = pygame.font.Font(None, 24).render(f"Lv.{self.level}", True, (255, 255, 255))
        level_bg = pygame.Rect(self.x - 20, char_y - size - 20, 40, 20)
        pygame.draw.rect(screen, (0, 0, 0, 150), level_bg)
        screen.blit(level_text, (self.x - 15, char_y - size - 18))
        
        # Render particles
        self._render_particles(screen)
    
    def _render_particles(self, screen):
        """Render all particle effects"""
        # Render level up particles
        for particle in self.level_up_particles:
            try:
                alpha = particle['lifetime'] / particle['max_lifetime']
                # Fix color format - ensure RGB only for pygame.draw.circle
                base_color = particle['color'][:3]  # Take only RGB, ignore alpha
                
                # Ensure color values are valid integers between 0-255
                base_color = tuple(max(0, min(255, int(c))) for c in base_color)
                
                particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
                # Create color with alpha for the surface
                alpha_value = max(0, min(255, int(alpha * 255)))
                color_with_alpha = (*base_color, alpha_value)
                pygame.draw.circle(particle_surface, color_with_alpha, (particle['size'], particle['size']), particle['size'])
                screen.blit(particle_surface, (int(particle['x'] - particle['size']), int(particle['y'] - particle['size'])))
            except (ValueError, TypeError) as e:
                # Skip invalid particles
                continue
        
        # Render skill particles
        for particle in self.skill_particles:
            try:
                alpha = particle['lifetime'] / particle['max_lifetime']
                # Fix color format - ensure RGB only for pygame.draw.circle
                base_color = particle['color'][:3]  # Take only RGB, ignore alpha
                
                # Ensure color values are valid integers between 0-255
                base_color = tuple(max(0, min(255, int(c))) for c in base_color)
                
                particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
                # Create color with alpha for the surface
                alpha_value = max(0, min(255, int(alpha * 255)))
                color_with_alpha = (*base_color, alpha_value)
                pygame.draw.circle(particle_surface, color_with_alpha, (particle['size'], particle['size']), particle['size'])
                screen.blit(particle_surface, (int(particle['x'] - particle['size']), int(particle['y'] - particle['size'])))
            except (ValueError, TypeError) as e:
                # Skip invalid particles
                continue
    
    def render_stats_panel(self, screen, x, y):
        """Render character stats panel with improved layout"""
        panel_width = 240
        panel_height = 220
        
        # Ensure panel fits on screen
        if x + panel_width > screen.get_width():
            x = screen.get_width() - panel_width - 10
        if y + panel_height > screen.get_height():
            y = screen.get_height() - panel_height - 10
        
        # Background with rounded corners effect
        panel_rect = pygame.Rect(x, y, panel_width, panel_height)
        pygame.draw.rect(screen, (20, 25, 40, 240), panel_rect)
        pygame.draw.rect(screen, (100, 150, 255), panel_rect, 2)
        
        # Title - more compact
        title_font = pygame.font.Font(None, 24)
        title = title_font.render("Alex - Neural Warrior", True, (255, 255, 255))
        screen.blit(title, (x + 8, y + 8))
        
        # Level and stats - better spacing
        font = pygame.font.Font(None, 20)
        current_y = y + 35
        
        # Level and Attack on same line
        level_text = font.render(f"Level: {self.level}", True, (255, 255, 255))
        screen.blit(level_text, (x + 8, current_y))
        
        attack_text = font.render(f"Attack: {self.attack_power}", True, (255, 200, 100))
        screen.blit(attack_text, (x + 120, current_y))
        current_y += 25
        
        # HP Bar with better styling
        bar_width = panel_width - 20
        hp_bar_rect = pygame.Rect(x + 10, current_y, bar_width, 18)
        pygame.draw.rect(screen, (40, 0, 0), hp_bar_rect)
        hp_fill_width = int(bar_width * (self.hp / self.max_hp))
        if hp_fill_width > 0:
            hp_fill_rect = pygame.Rect(x + 10, current_y, hp_fill_width, 18)
            pygame.draw.rect(screen, (220, 50, 50), hp_fill_rect)
        pygame.draw.rect(screen, (255, 255, 255), hp_bar_rect, 2)
        
        hp_text = pygame.font.Font(None, 16).render(f"HP: {self.hp}/{self.max_hp}", True, (255, 255, 255))
        screen.blit(hp_text, (x + 12, current_y + 2))
        current_y += 25
        
        # MP Bar with better styling
        mp_bar_rect = pygame.Rect(x + 10, current_y, bar_width, 18)
        pygame.draw.rect(screen, (0, 0, 40), mp_bar_rect)
        mp_fill_width = int(bar_width * (self.mp / self.max_mp))
        if mp_fill_width > 0:
            mp_fill_rect = pygame.Rect(x + 10, current_y, mp_fill_width, 18)
            pygame.draw.rect(screen, (50, 120, 255), mp_fill_rect)
        pygame.draw.rect(screen, (255, 255, 255), mp_bar_rect, 2)
        
        mp_text = pygame.font.Font(None, 16).render(f"MP: {self.mp}/{self.max_mp}", True, (255, 255, 255))
        screen.blit(mp_text, (x + 12, current_y + 2))
        current_y += 25
        
        # Experience bar
        exp_bar_rect = pygame.Rect(x + 10, current_y, bar_width, 15)
        pygame.draw.rect(screen, (40, 40, 0), exp_bar_rect)
        exp_progress = self.experience / self.experience_to_next_level if self.experience_to_next_level > 0 else 0
        exp_fill_width = int(bar_width * exp_progress)
        if exp_fill_width > 0:
            exp_fill_rect = pygame.Rect(x + 10, current_y, exp_fill_width, 15)
            pygame.draw.rect(screen, (255, 220, 50), exp_fill_rect)
        pygame.draw.rect(screen, (255, 255, 255), exp_bar_rect, 2)
        
        exp_text = pygame.font.Font(None, 14).render(f"EXP: {self.experience}/{self.experience_to_next_level}", True, (255, 255, 255))
        screen.blit(exp_text, (x + 12, current_y + 1))
        current_y += 22
        
        # Combat Abilities - more compact
        ability_font = pygame.font.Font(None, 16)
        ability_title = pygame.font.Font(None, 18).render("Combat Abilities:", True, (255, 150, 150))
        screen.blit(ability_title, (x + 8, current_y))
        current_y += 18
        
        unlocked_abilities = [(name, data) for name, data in self.abilities.items() if data['unlocked']]
        for ability_name, ability_data in unlocked_abilities[:2]:  # Show max 2 abilities
            color = (255, 255, 255) if self.mp >= ability_data['mp_cost'] else (120, 120, 120)
            ability_display = f"• {ability_name.replace('_', ' ').title()} (MP:{ability_data['mp_cost']} DMG:{ability_data['damage']})"
            ability_text = ability_font.render(ability_display, True, color)
            screen.blit(ability_text, (x + 12, current_y))
            current_y += 16
        
        # Skills - show only top skills
        skills_with_points = [(name, value) for name, value in self.skills.items() if value > 0]
        if skills_with_points:
            skill_title = pygame.font.Font(None, 18).render("Skills:", True, (150, 255, 150))
            screen.blit(skill_title, (x + 8, current_y))
            current_y += 18
            
            # Show top 2 skills only
            for skill_name, skill_value in skills_with_points[:2]:
                skill_display_name = skill_name.replace('_', ' ').title()
                skill_text = ability_font.render(f"• {skill_display_name}: {skill_value}%", True, (200, 255, 200))
                screen.blit(skill_text, (x + 12, current_y))
                current_y += 16