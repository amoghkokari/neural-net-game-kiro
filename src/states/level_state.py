"""
Individual level state with story and challenges
"""

import pygame
from .base_state import BaseState
from ..constants import GameState
try:
    from ..ui.responsive_layout import ResponsiveLayout
except ImportError:
    from ui.responsive_layout import ResponsiveLayout

class LevelState(BaseState):
    def __init__(self, game):
        super().__init__(game)
        self.layout = ResponsiveLayout(game.width, game.height)
        self.current_dialogue = 0
        self.level_data = None
        
        # Level content database
        self.level_content = {
            "Neuron Academy": {
                "story": [
                    "Welcome to the Neuron Academy, brave learner!",
                    "Here lies the foundation of all neural networks.",
                    "Every AI system starts with understanding a single neuron.",
                    "Master weights, bias, and computation to proceed.",
                    "The Weight Master awaits your challenge!"
                ],
                "challenge": "neuron_basics",
                "concept": "Learn how neurons process information"
            },
            "Bias Battlefield": {
                "story": [
                    "You enter the Bias Battlefield, where thresholds are everything!",
                    "The Bias Baron controls the power of neural activation.",
                    "Without bias, neurons can only activate at zero threshold.",
                    "Master bias to shift decision boundaries at will!",
                    "Prepare for battle against the threshold tyrant!"
                ],
                "challenge": "bias_battle",
                "concept": "Learn how bias shifts activation thresholds"
            },
            "Activation Peaks": {
                "story": [
                    "You ascend the treacherous Activation Peaks!",
                    "Here dwells the Sigmoid Sorcerer, master of non-linear transformations.",
                    "Linear functions are weak - only activation brings true neural power!",
                    "ReLU, Sigmoid, Tanh - each function has its sacred purpose.",
                    "Prove you understand the magic of non-linearity!"
                ],
                "challenge": "activation_functions",
                "concept": "Master activation functions and non-linearity"
            },
            "Chain Rule Caverns": {
                "story": [
                    "Deep in the Chain Rule Caverns lurks the Derivative Dragon!",
                    "This ancient beast guards the secrets of backpropagation.",
                    "The chain rule flows through every gradient calculation.",
                    "∂Loss/∂weight = ∂Loss/∂output × ∂output/∂weight",
                    "Face the dragon and master the mathematics of learning!"
                ],
                "challenge": "chain_rule_mastery",
                "concept": "Learn the chain rule for backpropagation"
            },
            "Perceptron Plains": {
                "story": [
                    "Welcome to the vast Perceptron Plains!",
                    "The Linear Separatrix rules these lands with decision boundaries.",
                    "Here you must build a complete perceptron from scratch.",
                    "Train it, tune it, make it learn the patterns of data!",
                    "Only then can you claim mastery over linear classification!"
                ],
                "challenge": "perceptron_complete",
                "concept": "Build and train complete perceptrons"
            },
            "Forward Pass Forest": {
                "story": [
                    "Enter the mystical Forward Pass Forest!",
                    "The Flow Guardian controls the rivers of information.",
                    "Data must flow from input to output, layer by layer.",
                    "Speed and accuracy both matter in this realm.",
                    "Race against the guardian to prove your mastery!"
                ],
                "challenge": "forward_pass_flow",
                "concept": "Master forward propagation through networks"
            },
            "Perceptron Village": {
                "story": [
                    "Welcome to Perceptron Village, traveler!",
                    "Here, the ancient art of neural computation began.",
                    "A perceptron is the simplest neural network - just one neuron!",
                    "It takes inputs, multiplies by weights, adds bias, and decides.",
                    "Your quest: Help the village elder classify fruits!"
                ],
                "challenge": "perceptron_classifier",
                "concept": "Learn how a single neuron makes binary decisions"
            }
        }
    
    def enter(self):
        """Called when entering the level"""
        print("🔄 Entering level state...")
        self.level_data = getattr(self.game, 'current_level_data', None)
        print(f"📊 Level data: {self.level_data}")
        self.current_dialogue = 0
        self.auto_advance_timer = 0
        self.auto_advance_complete = False
        self.dialogue_speed = 5.0  # seconds per dialogue line (slower)
        self.speech_started = False
        print("✅ Level state initialized successfully")
        
        # Start speech for first line (temporarily disabled to fix crash)
        if self.level_data and self.level_data["name"] in self.level_content:
            story = self.level_content[self.level_data["name"]]["story"]
            if story:
                try:
                    # Temporarily disable speech to fix game freezing
                    # from ..audio.speech_system import speech_system
                    # speech_system.speak(story[0], "tensor")
                    pass
                except Exception as e:
                    print(f"Speech system error (non-critical): {e}")
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.auto_advance_complete:
                    # Start coding challenge
                    if self.level_data and self.level_data["name"] in self.level_content:
                        self.game.current_challenge = self.level_content[self.level_data["name"]]["challenge"]
                        self.game.change_state(GameState.CODING_CHALLENGE)
                else:
                    # Skip to end of current dialogue
                    if self.level_data and self.level_data["name"] in self.level_content:
                        story = self.level_content[self.level_data["name"]]["story"]
                        self.current_dialogue = len(story) - 1
                        self.auto_advance_complete = True
            elif event.key == pygame.K_ESCAPE:
                self.game.change_state(GameState.WORLD_MAP)
    
    def update(self, dt):
        """Update auto-advancing dialogue"""
        if not self.auto_advance_complete and self.level_data and self.level_data["name"] in self.level_content:
            story = self.level_content[self.level_data["name"]]["story"]
            
            # Start speech for first line if not started (temporarily disabled)
            try:
                # Temporarily disable speech to fix game freezing
                # from ..audio.speech_system import speech_system
                # if not self.speech_started:
                #     speech_system.speak(story[self.current_dialogue], "tensor")
                #     self.speech_started = True
                # 
                # # Only advance if speech is not playing and enough time has passed
                # speech_not_playing = not speech_system.is_currently_speaking()
                speech_not_playing = True
                if not self.speech_started:
                    self.speech_started = True
            except Exception as e:
                print(f"Speech system error (non-critical): {e}")
                speech_not_playing = True
                if not self.speech_started:
                    self.speech_started = True
            
            if speech_not_playing:
                self.auto_advance_timer += dt
                
                # Wait 3 seconds after speech finishes before advancing
                if self.auto_advance_timer >= 3.0 and self.current_dialogue < len(story) - 1:
                    self.current_dialogue += 1
                    self.auto_advance_timer = 0
                    
                    # Speak next line (temporarily disabled)
                    try:
                        # Temporarily disable speech to fix game freezing
                        # speech_system.speak(story[self.current_dialogue], "tensor")
                        pass
                    except Exception as e:
                        print(f"Speech system error (non-critical): {e}")
                    
                elif self.current_dialogue >= len(story) - 1:
                    self.auto_advance_complete = True
    
    def render(self, screen):
        if not self.level_data:
            print("⚠️  No level data available for rendering")
            return
        
        try:
            # Dynamic background based on level type
            level_type = self.level_data.get("type", "foundation")
            if level_type == "foundation":
                bg_color = (40, 60, 40)  # Green
            elif level_type == "building":
                bg_color = (60, 40, 60)  # Purple
            elif level_type == "training":
                bg_color = (60, 60, 40)  # Yellow-brown
            elif level_type == "advanced":
                bg_color = (40, 40, 60)  # Blue
            elif level_type == "transformer":
                bg_color = (60, 40, 40)  # Red
            else:
                bg_color = (50, 50, 50)  # Gray
            
            screen.fill(bg_color)
            
            # Create responsive layout areas
            title_rect = self.layout.get_rect(0, 0, 1, 0.15)
            boss_rect = self.layout.get_rect(0, 0.15, 1, 0.08)
            concept_rect = self.layout.get_rect(0, 0.23, 1, 0.08)
            dialogue_rect = self.layout.get_rect(0.1, 0.31, 0.8, 0.45)
            instruction_rect = self.layout.get_rect(0, 0.76, 1, 0.12)
            back_rect = self.layout.get_rect(0, 0.88, 1, 0.12)
            
            # Level title with responsive font
            title_font_size = self.layout.get_font_size(0.06, min_size=24, max_size=48)
            title_font = pygame.font.Font(None, title_font_size)
            
            # Glow effect for title
            for offset in [(2, 2), (-2, -2), (2, -2), (-2, 2)]:
                glow_title = title_font.render(self.level_data["name"], True, (100, 100, 100))
                glow_pos = (title_rect.centerx + offset[0], title_rect.centery + offset[1])
                glow_rect = glow_title.get_rect(center=glow_pos)
                screen.blit(glow_title, glow_rect)
            
            self.layout.render_text_block(screen, self.level_data["name"], title_font, title_rect,
                                        (255, 255, 255), align="center", vertical_align="center")
            
            # Boss name
            boss_name = self.level_data.get("boss", "Unknown Boss")
            boss_font_size = self.layout.get_font_size(0.04, min_size=16, max_size=32)
            boss_font = pygame.font.Font(None, boss_font_size)
            boss_text = f"Boss: {boss_name}"
            self.layout.render_text_block(screen, boss_text, boss_font, boss_rect,
                                        (255, 100, 100), align="center", vertical_align="center")
            
            # Level concept
            concept = self.level_data.get("concept", "")
            if concept:
                concept_font_size = self.layout.get_font_size(0.03, min_size=14, max_size=24)
                concept_font = pygame.font.Font(None, concept_font_size)
                concept_text = f"💡 {concept}"
                self.layout.render_text_block(screen, concept_text, concept_font, concept_rect,
                                            (200, 255, 200), align="center", vertical_align="center")
        
            # Story dialogue with responsive UI
            if self.level_data["name"] in self.level_content:
                story = self.level_content[self.level_data["name"]]["story"]
                if self.current_dialogue < len(story):
                    # Modern dialogue box with responsive design
                    dialogue_surface = pygame.Surface((dialogue_rect.width, dialogue_rect.height), pygame.SRCALPHA)
                    pygame.draw.rect(dialogue_surface, (0, 0, 0, 200), (0, 0, dialogue_rect.width, dialogue_rect.height), border_radius=20)
                    screen.blit(dialogue_surface, dialogue_rect.topleft)
                    
                    # Border with glow
                    pygame.draw.rect(screen, (100, 200, 255), dialogue_rect, 3, border_radius=20)
                    
                    # Character indicator
                    char_font_size = self.layout.get_font_size(0.035, min_size=16, max_size=28)
                    char_font = pygame.font.Font(None, char_font_size)
                    
                    char_y = dialogue_rect.y + 15
                    char_shadow = char_font.render("Tensor:", True, (0, 0, 0))
                    char_text = char_font.render("Tensor:", True, (100, 255, 255))
                    screen.blit(char_shadow, (dialogue_rect.x + 22, char_y + 2))
                    screen.blit(char_text, (dialogue_rect.x + 20, char_y))
                    
                    # Story text with responsive wrapping
                    text = story[self.current_dialogue]
                    text_font_size = self.layout.get_font_size(0.03, min_size=12, max_size=20)
                    text_font = pygame.font.Font(None, text_font_size)
                    
                    text_area = pygame.Rect(dialogue_rect.x + 20, dialogue_rect.y + 50,
                                          dialogue_rect.width - 40, dialogue_rect.height - 80)
                    self.layout.render_text_block(screen, text, text_font, text_area,
                                                (255, 255, 255), align="left", vertical_align="top")
                    
                    # Progress indicator
                    progress = (self.current_dialogue + 1) / len(story)
                    progress_width = int((dialogue_rect.width - 40) * progress)
                    progress_rect = pygame.Rect(dialogue_rect.x + 20, dialogue_rect.bottom - 30, progress_width, 4)
                    pygame.draw.rect(screen, (100, 255, 100), progress_rect, border_radius=2)
                    
                    # Progress text
                    progress_text = f"{self.current_dialogue + 1}/{len(story)}"
                    progress_font_size = self.layout.get_font_size(0.025, min_size=12, max_size=20)
                    progress_font = pygame.font.Font(None, progress_font_size)
                    progress_surface = progress_font.render(progress_text, True, (200, 200, 200))
                    screen.blit(progress_surface, (dialogue_rect.right - 60, dialogue_rect.bottom - 25))
            
            # Instructions with responsive styling
            if self.auto_advance_complete:
                instruction = "🚀 Press SPACE to start your challenge!"
                color = (0, 255, 0)
            else:
                instruction = "📖 Story auto-advancing... Press SPACE to skip"
                color = (255, 255, 100)
            
            inst_font_size = self.layout.get_font_size(0.035, min_size=16, max_size=28)
            inst_font = pygame.font.Font(None, inst_font_size)
            
            # Background for instruction
            inst_bg_rect = instruction_rect.inflate(-20, -10)
            pygame.draw.rect(screen, (0, 0, 0, 150), inst_bg_rect, border_radius=10)
            
            self.layout.render_text_block(screen, instruction, inst_font, instruction_rect,
                                        color, align="center", vertical_align="center")
            
            # Back instruction
            back_font_size = self.layout.get_font_size(0.025, min_size=12, max_size=20)
            back_font = pygame.font.Font(None, back_font_size)
            back_text = "ESC - Return to world map"
            self.layout.render_text_block(screen, back_text, back_font, back_rect,
                                        (150, 150, 150), align="left", vertical_align="top")
        
        except Exception as e:
            print(f"❌ Error in level render: {e}")
            import traceback
            traceback.print_exc()
            # Render error message
            error_font_size = self.layout.get_font_size(0.04, min_size=18, max_size=36)
            error_font = pygame.font.Font(None, error_font_size)
            error_rect = self.layout.get_centered_rect(0.8, 0.2, y_percent=0.5)
            self.layout.render_text_block(screen, "Level rendering error - check console", error_font,
                                        error_rect, (255, 0, 0), align="center", vertical_align="center")
    
    def _render_wrapped_text(self, screen, text, x, y, max_width, color):
        """Render text with word wrapping and shadow for better readability"""
        words = text.split(' ')
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " "
            if self.text_font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                current_line = word + " "
        
        if current_line:
            lines.append(current_line.strip())
        
        # Render lines with shadow for better readability
        line_height = self.text_font.get_height() + 5
        for i, line in enumerate(lines):
            if line:
                # Shadow for better readability
                shadow_surface = self.text_font.render(line, True, (0, 0, 0))
                screen.blit(shadow_surface, (x + 2, y + i * line_height + 2))
                # Main text
                text_surface = self.text_font.render(line, True, color)
                screen.blit(text_surface, (x, y + i * line_height))