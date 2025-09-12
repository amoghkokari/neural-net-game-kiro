"""
World map state showing different neural network realms
"""

import pygame
import math
from .base_state import BaseState
from ..constants import GameState
try:
    from ..ui.responsive_layout import ResponsiveLayout
except ImportError:
    from ui.responsive_layout import ResponsiveLayout

class WorldMapState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.layout = ResponsiveLayout(game.width, game.height)
        
        # Define the learning path with positions - redesigned progression
        self.levels = [
            # Foundation Arc - Understanding the Basics
            {"name": "Neuron Academy", "pos": (150, 650), "unlocked": True, "concept": "Neurons & Weights", "boss": "The Weight Master", "type": "foundation"},
            {"name": "Bias Battlefield", "pos": (300, 600), "unlocked": False, "concept": "Bias & Thresholds", "boss": "Bias Baron", "type": "foundation"},
            {"name": "Activation Peaks", "pos": (450, 550), "unlocked": False, "concept": "Activation Functions", "boss": "Sigmoid Sorcerer", "type": "foundation"},
            {"name": "Chain Rule Caverns", "pos": (600, 500), "unlocked": False, "concept": "Chain Rule & Derivatives", "boss": "Derivative Dragon", "type": "foundation"},
            
            # Building Arc - Constructing Networks
            {"name": "Perceptron Plains", "pos": (750, 450), "unlocked": False, "concept": "Building Perceptrons", "boss": "Linear Separatrix", "type": "building"},
            {"name": "Forward Pass Forest", "pos": (850, 350), "unlocked": False, "concept": "Forward Propagation", "boss": "Flow Guardian", "type": "building"},
            {"name": "Backprop Badlands", "pos": (750, 250), "unlocked": False, "concept": "Backpropagation", "boss": "Gradient Golem", "type": "building"},
            
            # Training Arc - Real World Application
            {"name": "Training Grounds", "pos": (600, 150), "unlocked": False, "concept": "Train/Test/Validate", "boss": "Overfitting Ogre", "type": "training"},
            {"name": "Data Dungeons", "pos": (450, 100), "unlocked": False, "concept": "Real Dataset Training", "boss": "Noise Nightmare", "type": "training"},
            
            # Advanced Arc - Specialized Architectures
            {"name": "RNN Realm", "pos": (300, 150), "unlocked": False, "concept": "Recurrent Networks", "boss": "Memory Monarch", "type": "advanced"},
            {"name": "CNN Castle", "pos": (150, 200), "unlocked": False, "concept": "Convolutional Networks", "boss": "Feature Phantom", "type": "advanced"},
            {"name": "LSTM Labyrinth", "pos": (100, 350), "unlocked": False, "concept": "Long Short-Term Memory", "boss": "Vanishing Gradient Vampire", "type": "advanced"},
            {"name": "GRU Gardens", "pos": (150, 500), "unlocked": False, "concept": "Gated Recurrent Units", "boss": "Gate Keeper", "type": "advanced"},
            
            # Transformer Arc - Modern AI
            {"name": "Word2Vec Wasteland", "pos": (250, 400), "unlocked": False, "concept": "Word Embeddings", "boss": "Semantic Spider", "type": "transformer"},
            {"name": "Attention Archipelago", "pos": (400, 300), "unlocked": False, "concept": "Attention Mechanism", "boss": "Focus Fiend", "type": "transformer"},
            {"name": "Transformer Temple", "pos": (550, 200), "unlocked": False, "concept": "Full Transformer", "boss": "Multi-Head Hydra", "type": "transformer"},
            
            # Final Boss
            {"name": "GPT Citadel", "pos": (700, 100), "unlocked": False, "concept": "Generative AI", "boss": "GPT Overlord", "type": "final"}
        ]
        
        self.selected_level = 0
        self.camera_x = 0
        self.camera_y = 0
        
        # Debug mode for level selection
        self.debug_mode = False
        self.cheat_sequence = ""
        self.target_cheats = ["unlock", "debugmode"]  # Type "unlock" or "debugmode" to unlock all levels
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                # Find previous level (unlocked or debug mode)
                for i in range(self.selected_level - 1, -1, -1):
                    if self.levels[i]["unlocked"] or self.debug_mode:
                        self.selected_level = i
                        break
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                # Find next level (unlocked or debug mode)
                for i in range(self.selected_level + 1, len(self.levels)):
                    if self.levels[i]["unlocked"] or self.debug_mode:
                        self.selected_level = i
                        break
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                # Navigate up in the level grid
                current_pos = self.levels[self.selected_level]["pos"]
                best_level = self.selected_level
                best_distance = float('inf')
                
                for i, level in enumerate(self.levels):
                    if (level["unlocked"] or self.debug_mode) and level["pos"][1] < current_pos[1]:
                        distance = ((level["pos"][0] - current_pos[0])**2 + (level["pos"][1] - current_pos[1])**2)**0.5
                        if distance < best_distance:
                            best_distance = distance
                            best_level = i
                
                if best_level != self.selected_level:
                    self.selected_level = best_level
                    
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                # Navigate down in the level grid
                current_pos = self.levels[self.selected_level]["pos"]
                best_level = self.selected_level
                best_distance = float('inf')
                
                for i, level in enumerate(self.levels):
                    if (level["unlocked"] or self.debug_mode) and level["pos"][1] > current_pos[1]:
                        distance = ((level["pos"][0] - current_pos[0])**2 + (level["pos"][1] - current_pos[1])**2)**0.5
                        if distance < best_distance:
                            best_distance = distance
                            best_level = i
                
                if best_level != self.selected_level:
                    self.selected_level = best_level
                    
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                # Prevent entering levels beyond 6 (in development)
                if self.selected_level >= 6:
                    print("🚧 This level is still in development! Coming soon...")
                    return
                
                if self.levels[self.selected_level]["unlocked"] or self.debug_mode:
                    self.game.current_level_data = self.levels[self.selected_level]
                    self.game.change_state(GameState.LEVEL)
            elif event.key == pygame.K_ESCAPE:
                self.game.change_state(GameState.MENU)
            elif event.key == pygame.K_F1:  # Simple F1 key to toggle debug mode
                self.debug_mode = not self.debug_mode
                print(f"F1 Debug mode toggled: {self.debug_mode}")
                
                # Unlock all levels in debug mode, lock them back otherwise
                for level in self.levels:
                    level["unlocked"] = self.debug_mode or level == self.levels[0]
            else:
                # Cheat code detection
                if event.unicode.isalpha():
                    self.cheat_sequence += event.unicode.lower()
                    
                    # Keep only the last 9 characters (length of longest cheat code)
                    if len(self.cheat_sequence) > 9:
                        self.cheat_sequence = self.cheat_sequence[-9:]
                    
                    # Check if any cheat code matches
                    for cheat in self.target_cheats:
                        if self.cheat_sequence.endswith(cheat):
                            self.debug_mode = not self.debug_mode
                            print(f"Cheat '{cheat}' activated! Debug mode: {self.debug_mode}")
                            self.cheat_sequence = ""  # Reset
                            
                            # Unlock all levels in debug mode, lock them back otherwise
                            for level in self.levels:
                                level["unlocked"] = self.debug_mode or level == self.levels[0]
                            break
    
    def update(self, dt):
        # Update camera to follow selected level
        target_x = self.levels[self.selected_level]["pos"][0] - self.game.width // 2
        target_y = self.levels[self.selected_level]["pos"][1] - self.game.height // 2
        
        self.camera_x += (target_x - self.camera_x) * dt * 2
        self.camera_y += (target_y - self.camera_y) * dt * 2
    
    def render(self, screen):
        # Draw gradient background
        for y in range(self.game.height):
            color_intensity = int(20 + (y / self.game.height) * 40)
            color = (color_intensity, color_intensity + 10, color_intensity + 30)
            pygame.draw.line(screen, color, (0, y), (self.game.width, y))
        
        # Draw connections between levels with better visibility
        for i in range(len(self.levels) - 1):
            start_pos = (self.levels[i]["pos"][0] - self.camera_x, self.levels[i]["pos"][1] - self.camera_y)
            end_pos = (self.levels[i + 1]["pos"][0] - self.camera_x, self.levels[i + 1]["pos"][1] - self.camera_y)
            
            if self.levels[i + 1]["unlocked"]:
                color = (150, 255, 150)  # Bright green for unlocked paths
                thickness = 4
            else:
                color = (80, 80, 80)  # Dark gray for locked paths
                thickness = 2
            
            pygame.draw.line(screen, color, start_pos, end_pos, thickness)
        
        # Draw level nodes with improved graphics
        for i, level in enumerate(self.levels):
            x = level["pos"][0] - self.camera_x
            y = level["pos"][1] - self.camera_y
            
            # Skip if off screen
            if x < -150 or x > self.game.width + 150 or y < -150 or y > self.game.height + 150:
                continue
            
            # Determine colors and effects
            is_accessible = level["unlocked"] or self.debug_mode
            
            if is_accessible:
                if i == self.selected_level:
                    # Selected level - pulsing yellow
                    pulse = abs(math.sin(pygame.time.get_ticks() * 0.005)) * 20 + 235
                    color = (255, 255, int(pulse))
                    radius = 40
                    # Draw selection ring
                    ring_color = (255, 100, 100) if self.debug_mode and not level["unlocked"] else (255, 255, 255)
                    pygame.draw.circle(screen, ring_color, (int(x), int(y)), radius + 8, 3)
                elif i in self.game.player_progress['completed_levels']:
                    color = (100, 255, 100)  # Bright green for completed
                    radius = 35
                elif level["unlocked"]:
                    color = (100, 200, 255)  # Blue for naturally available
                    radius = 32
                else:
                    # Debug mode accessible but not naturally unlocked
                    color = (255, 150, 100)  # Orange for debug-accessible
                    radius = 30
            else:
                color = (60, 60, 60)  # Dark gray for locked
                radius = 25
            
            # Draw level circle with glow effect
            if is_accessible:
                # Glow effect
                glow_surface = pygame.Surface((radius * 3, radius * 3), pygame.SRCALPHA)
                glow_color = (*color[:3], 50)
                pygame.draw.circle(glow_surface, glow_color, (radius * 3 // 2, radius * 3 // 2), radius + 10)
                screen.blit(glow_surface, (int(x - radius * 1.5), int(y - radius * 1.5)))
            
            # Main circle
            pygame.draw.circle(screen, color, (int(x), int(y)), radius)
            pygame.draw.circle(screen, (255, 255, 255), (int(x), int(y)), radius, 3)
            
            # Level number
            level_num = str(i + 1)
            num_font = pygame.font.Font(None, 32)
            
            # Text color based on accessibility
            if is_accessible:
                text_color = (0, 0, 0)
            else:
                text_color = (150, 150, 150)
                
            # Add debug indicator for debug-accessible levels
            if self.debug_mode and not level["unlocked"] and is_accessible:
                level_num = f"🔧{i + 1}"
                
            num_text = num_font.render(level_num, True, text_color)
            num_rect = num_text.get_rect(center=(x, y))
            screen.blit(num_text, num_rect)
            
            # Completion indicator
            if i in self.game.player_progress['completed_levels']:
                check_font = pygame.font.Font(None, 24)
                check_text = check_font.render("✓", True, (255, 255, 255))
                check_rect = check_text.get_rect(center=(x + radius - 10, y - radius + 10))
                pygame.draw.circle(screen, (0, 200, 0), (int(x + radius - 10), int(y - radius + 10)), 12)
                screen.blit(check_text, check_rect)
            
            # Level name with better positioning
            name_font = pygame.font.Font(None, 24)
            
            # Show "In Development" for levels beyond 6
            if i >= 6:
                level_name = "🚧 In Development"
                name_color = (255, 200, 100)
            else:
                level_name = level["name"]
                name_color = (255, 255, 255)
            
            name_text = name_font.render(level_name, True, name_color)
            name_rect = name_text.get_rect(center=(x, y - radius - 25))
            
            # Background for text readability
            text_bg = name_rect.inflate(10, 4)
            pygame.draw.rect(screen, (0, 0, 0, 150), text_bg)
            screen.blit(name_text, name_rect)
            
            # Boss name
            if "boss" in level:
                boss_font = pygame.font.Font(None, 18)
                boss_text = boss_font.render(f"Boss: {level['boss']}", True, (255, 200, 200))
                boss_rect = boss_text.get_rect(center=(x, y + radius + 15))
                boss_bg = boss_rect.inflate(8, 2)
                pygame.draw.rect(screen, (0, 0, 0, 120), boss_bg)
                screen.blit(boss_text, boss_rect)
            
            # Concept description
            concept_font = pygame.font.Font(None, 16)
            concept_text = concept_font.render(level["concept"], True, (200, 200, 200))
            concept_rect = concept_text.get_rect(center=(x, y + radius + 35))
            concept_bg = concept_rect.inflate(6, 2)
            pygame.draw.rect(screen, (0, 0, 0, 100), concept_bg)
            screen.blit(concept_text, concept_rect)
        
        # Draw character at selected level position
        selected_level = self.levels[self.selected_level]
        char_x = selected_level["pos"][0] - self.camera_x
        char_y = selected_level["pos"][1] - self.camera_y + 80
        
        # Update character position
        self.game.character.move_to(char_x, char_y)
        self.game.character.render(screen)
        
        # Draw UI with better styling
        # Title
        title_font = pygame.font.Font(None, 48)
        title = title_font.render("Neural Network World", True, (255, 255, 255))
        title_shadow = title_font.render("Neural Network World", True, (0, 0, 0))
        screen.blit(title_shadow, (22, 22))
        screen.blit(title, (20, 20))
        
        # Character stats panel - ensure it fits on screen
        panel_width = 250
        stats_x = max(10, self.game.width - panel_width - 10)  # Ensure it doesn't go off-screen
        self.game.character.render_stats_panel(screen, stats_x, 20)
        
        # Progress indicator
        completed_count = len(self.game.player_progress['completed_levels'])
        total_unlocked = len([l for l in self.levels if l["unlocked"]])
        progress_text = f"Progress: {completed_count}/{total_unlocked} levels completed"
        progress_font = pygame.font.Font(None, 24)
        progress_surface = progress_font.render(progress_text, True, (255, 255, 100))
        screen.blit(progress_surface, (20, 80))
        
        # Instructions with better formatting
        instructions = [
            "🎮 Controls:",
            "WASD/Arrow Keys - Navigate",
            "Enter/Space - Enter Level",
            "Esc - Main Menu",
            "",
            "💡 F1 or type 'unlock' to unlock all levels for testing"
        ]
        
        inst_font = pygame.font.Font(None, 20)
        for i, instruction in enumerate(instructions):
            color = (255, 255, 100) if i == 0 else (200, 200, 200)
            inst_text = inst_font.render(instruction, True, color)
            screen.blit(inst_text, (20, self.game.height - 100 + i * 22))
        
        # Selected level info
        if self.selected_level < len(self.levels):
            selected = self.levels[self.selected_level]
            info_font = pygame.font.Font(None, 28)
            info_text = f"Selected: {selected['name']}"
            info_surface = info_font.render(info_text, True, (255, 255, 0))
            info_bg = pygame.Rect(self.game.width // 2 - 150, self.game.height - 50, 300, 30)
            pygame.draw.rect(screen, (0, 0, 0, 180), info_bg)
            pygame.draw.rect(screen, (255, 255, 0), info_bg, 2)
            screen.blit(info_surface, (self.game.width // 2 - 140, self.game.height - 45))
        
        # Debug mode indicator
        if self.debug_mode:
            debug_font = pygame.font.Font(None, 32)
            debug_text = "🔧 DEBUG MODE - All Levels Unlocked"
            debug_surface = debug_font.render(debug_text, True, (255, 100, 100))
            debug_bg = pygame.Rect(self.game.width // 2 - 200, 20, 400, 35)
            pygame.draw.rect(screen, (50, 0, 0, 200), debug_bg)
            pygame.draw.rect(screen, (255, 100, 100), debug_bg, 2)
            screen.blit(debug_surface, (self.game.width // 2 - 190, 25))
            
            # Instructions for debug mode
            debug_inst = "Type 'unlock' again or press F1 to disable"
            debug_inst_surface = pygame.font.Font(None, 20).render(debug_inst, True, (255, 150, 150))
            screen.blit(debug_inst_surface, (self.game.width // 2 - 120, 60))
    
    def _unlock_next_levels(self):
        """Unlock next levels based on progress"""
        # Unlock the immediate next level
        if self.selected_level + 1 < len(self.levels):
            self.levels[self.selected_level + 1]["unlocked"] = True
        
        # Special unlocking logic for different arcs
        completed_count = len(self.game.player_progress['completed_levels'])
        
        # Unlock multiple levels at certain milestones
        if completed_count >= 2:  # After completing 2 levels, unlock next 2
            for i in range(min(4, len(self.levels))):
                self.levels[i]["unlocked"] = True
        
        if completed_count >= 4:  # After completing 4 levels, unlock next arc
            for i in range(min(6, len(self.levels))):
                self.levels[i]["unlocked"] = True