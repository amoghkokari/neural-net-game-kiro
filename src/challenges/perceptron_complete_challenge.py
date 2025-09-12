"""
Neural Detective Agency - Perceptron Challenge
Learn how perceptrons work by solving mysteries as a neural detective!
"""

import pygame
import numpy as np
import math
import random
try:
    from .base_challenge import BaseChallenge
except ImportError:
    # Fallback for testing
    from base_challenge import BaseChallenge
try:
    from ..ui.modern_ui import ModernButton, ProgressBar, DialogueBox, ParticleSystem
    from ..ui.responsive_layout import ResponsiveLayout, ResponsiveButton, ResponsiveSlider
    from ..ui.clean_layout import CleanLayout
except ImportError:
    # Fallback for testing
    from ui.modern_ui import ModernButton, ProgressBar, DialogueBox, ParticleSystem
    from ui.responsive_layout import ResponsiveLayout, ResponsiveButton, ResponsiveSlider
    from ui.clean_layout import CleanLayout

class PerceptronCompleteChallenge(BaseChallenge):
    def __init__(self, game):
        super().__init__(game)
        
        # Initialize layout systems
        self.layout = ResponsiveLayout(game.width, game.height)
        self.clean_layout = CleanLayout(game.width, game.height)
        
        # Game Theme: Neural Detective Agency
        self.case_number = 1
        self.detective_rank = "Rookie Detective"
        self.evidence_analyzed = 0
        self.correct_classifications = 0
        self.case_solved = False
        
        # Game Mechanics
        self.phase = "briefing"  # briefing -> investigating -> boss_fight -> victory
        self.briefing_timer = 0
        self.investigation_timer = 0
        self.max_investigation_time = 45.0
        self.evidence_spawn_interval = 3.0
        self.last_spawn_time = 0
        
        # Perceptron - The "Neural Scanner"
        self.weights = np.array([0.1, 0.1])  # Detective's initial intuition
        self.bias = 0.0
        self.learning_rate = 0.3
        
        # Evidence Database (Training Data)
        self.current_case = self.generate_case()
        self.evidence_queue = []
        self.classified_evidence = []
        self.current_evidence = None
        self.evidence_timer = 0
        
        # Boss Fight: The Linear Separatrix
        self.boss_hp = 100
        self.boss_max_hp = 100
        self.boss_phase = 1  # 1: Basic separation, 2: Noise attack, 3: Non-linear challenge
        self.boss_attacks = []
        self.player_score = 0
        self.boss_data_points = []
        self.boss_challenge_active = False
        
        # Visual Effects
        self.scanner_active = False
        self.scanner_pulse = 0
        self.classification_feedback = None
        self.feedback_timer = 0
        self.particles = ParticleSystem()
        
        # Tutorial
        self.show_tutorial = True
        self.tutorial_messages = [
            "Welcome to the Neural Detective Agency!",
            "Your job: Train your neural scanner to classify evidence",
            "Drag the sliders to adjust your scanner's sensitivity",
            "Green evidence = Innocent, Red evidence = Guilty",
            "Learn from mistakes to improve accuracy!"
        ]
        self.tutorial_index = 0
        
        # Initialize responsive UI elements
        self._setup_responsive_ui()
    
    def _setup_responsive_ui(self):
        """Setup all responsive UI elements"""
        # Create layout areas for current phase
        self.areas = self.layout.create_layout_areas(self.phase)
        
        # Progress bars (will be positioned dynamically)
        self.accuracy_bar = None
        self.case_progress_bar = None
        
        # Weight sliders (will be created dynamically)
        self.weight_sliders = {}
        
        # Dialogue box (responsive)
        if "dialogue" in self.areas:
            dialogue_rect = self.areas["dialogue"]
            self.dialogue_box = DialogueBox(dialogue_rect.x, dialogue_rect.y, 
                                          dialogue_rect.width, dialogue_rect.height)
        else:
            # Fallback positioning
            dialogue_rect = self.layout.get_rect(0, 0.75, 1, 0.25)
            self.dialogue_box = DialogueBox(dialogue_rect.x, dialogue_rect.y, 
                                          dialogue_rect.width, dialogue_rect.height)
    
    def _update_layout_for_phase(self):
        """Update layout when phase changes"""
        # Use clean layout for better readability
        self.areas = self.clean_layout.create_simple_layout()
        
        # Update dialogue box position
        if "dialogue" in self.areas:
            dialogue_rect = self.areas["dialogue"]
            self.dialogue_box.rect = pygame.Rect(dialogue_rect.x, dialogue_rect.y, 
                                               dialogue_rect.width, dialogue_rect.height)
        
        # Recreate sliders for new layout
        if self.phase in ["investigating", "boss_fight"]:
            self._create_weight_sliders()
    
    def _create_weight_sliders(self):
        """Create responsive weight sliders"""
        if "controls" not in self.areas:
            return
            
        controls_rect = self.areas["controls"]
        
        # Create three sliders horizontally distributed
        slider_height = max(20, int(controls_rect.height * 0.4))
        slider_area = pygame.Rect(controls_rect.x, controls_rect.y, controls_rect.width, slider_height)
        slider_rects = self.layout.distribute_horizontally(slider_area, 3)
        
        slider_configs = [
            ("w1", "Suspicion Level", self.weights[0]),
            ("w2", "Evidence Weight", self.weights[1]),
            ("bias", "Gut Feeling", self.bias)
        ]
        
        self.weight_sliders = {}
        for i, (name, label, value) in enumerate(slider_configs):
            if i < len(slider_rects):
                self.weight_sliders[name] = ResponsiveSlider(
                    self.layout, slider_rects[i], label, -1.0, 1.0, value
                )
    
    def _create_progress_bars(self):
        """Create responsive progress bars"""
        if "progress" not in self.areas:
            return
            
        progress_rect = self.areas["progress"]
        
        # Create two progress bars side by side
        bar_width = int(progress_rect.width * 0.35)
        bar_height = int(progress_rect.height * 0.4)
        
        # Accuracy bar (left)
        acc_x = progress_rect.x + int(progress_rect.width * 0.1)
        acc_y = progress_rect.y + (progress_rect.height - bar_height) // 2
        self.accuracy_bar = ProgressBar(acc_x, acc_y, bar_width, bar_height, 100)
        
        # Case progress bar (right)
        case_x = progress_rect.x + int(progress_rect.width * 0.55)
        case_y = progress_rect.y + (progress_rect.height - bar_height) // 2
        self.case_progress_bar = ProgressBar(case_x, case_y, bar_width, bar_height, 100)
    
    def _calculate_layout(self):
        """Calculate responsive layout dimensions with proper spacing"""
        # Define layout regions as percentages of screen with better spacing
        if self.phase == "boss_fight":
            # Special layout for boss fight to prevent overlapping
            self.layout = {
                'title_area': {'y': 0, 'height': 0.08},
                'progress_area': {'y': 0.08, 'height': 0.06},
                'boss_header': {'y': 0.14, 'height': 0.12},
                'main_content': {'y': 0.26, 'height': 0.35},
                'controls_area': {'y': 0.61, 'height': 0.12},
                'dialogue_area': {'y': 0.73, 'height': 0.27}
            }
        else:
            # Standard layout for other phases
            self.layout = {
                'title_area': {'y': 0, 'height': 0.1},
                'progress_area': {'y': 0.1, 'height': 0.08},
                'main_area': {'y': 0.18, 'height': 0.45},
                'controls_area': {'y': 0.63, 'height': 0.15},
                'dialogue_area': {'y': 0.78, 'height': 0.22}
            }
        
        # Calculate actual pixel values with minimum sizes
        for area_name, area in self.layout.items():
            area['y_px'] = int(area['y'] * self.screen_height)
            area['height_px'] = max(50, int(area['height'] * self.screen_height))  # Minimum 50px height
            
        # Ensure no overlapping by adjusting if needed
        self._adjust_layout_for_overlaps()
    
    def _adjust_layout_for_overlaps(self):
        """Adjust layout to prevent overlapping elements"""
        areas = list(self.layout.keys())
        for i in range(len(areas) - 1):
            current_area = self.layout[areas[i]]
            next_area = self.layout[areas[i + 1]]
            
            current_bottom = current_area['y_px'] + current_area['height_px']
            if current_bottom > next_area['y_px']:
                # Overlap detected, adjust next area
                next_area['y_px'] = current_bottom + 5  # 5px spacing
                # Recalculate height if needed
                if i + 2 < len(areas):
                    following_area = self.layout[areas[i + 2]]
                    max_height = following_area['y_px'] - next_area['y_px'] - 5
                    next_area['height_px'] = min(next_area['height_px'], max_height)
    
    def _setup_responsive_elements(self):
        """Setup all UI elements with responsive positioning"""
        # Main content area dimensions
        main_area = self.layout['main_area']
        main_y = main_area['y_px']
        main_height = main_area['height_px']
        
        # Scanner (center of main area)
        scanner_width = min(int(self.screen_width * 0.25), 250)
        scanner_height = min(int(main_height * 0.6), 180)
        scanner_x = int(self.screen_width * 0.375)  # Center horizontally
        scanner_y = main_y + int(main_height * 0.2)
        self.scanner_rect = pygame.Rect(scanner_x, scanner_y, scanner_width, scanner_height)
        
        # Evidence display (left side)
        evidence_width = min(int(self.screen_width * 0.2), 200)
        evidence_height = scanner_height
        evidence_x = int(self.screen_width * 0.05)
        evidence_y = scanner_y
        self.evidence_rect = pygame.Rect(evidence_x, evidence_y, evidence_width, evidence_height)
        
        # Stats display (right side)
        stats_width = min(int(self.screen_width * 0.25), 250)
        stats_height = scanner_height
        stats_x = int(self.screen_width * 0.7)
        stats_y = scanner_y
        self.stats_rect = pygame.Rect(stats_x, stats_y, stats_width, stats_height)
        
        # Weight sliders (controls area)
        controls_area = self.layout['controls_area']
        controls_y = controls_area['y_px']
        
        slider_width = min(int(self.screen_width * 0.2), 200)
        slider_height = max(25, int(self.screen_height * 0.04))
        slider_spacing = int(self.screen_width * 0.25)
        
        self.weight_sliders = {
            'w1': {
                'rect': pygame.Rect(int(self.screen_width * 0.1), controls_y + 20, slider_width, slider_height),
                'value': 0.1, 'dragging': False, 'label': 'Suspicion Level'
            },
            'w2': {
                'rect': pygame.Rect(int(self.screen_width * 0.4), controls_y + 20, slider_width, slider_height),
                'value': 0.1, 'dragging': False, 'label': 'Evidence Weight'
            },
            'bias': {
                'rect': pygame.Rect(int(self.screen_width * 0.7), controls_y + 20, slider_width, slider_height),
                'value': 0.0, 'dragging': False, 'label': 'Gut Feeling'
            }
        }
        
    def generate_case(self):
        """Generate a new mystery case with evidence"""
        cases = [
            {
                "title": "The Missing Diamond Case",
                "description": "A valuable diamond has been stolen. Classify suspects based on their alibis and motives.",
                "evidence_types": ["Alibi Strength", "Motive Level"],
                "innocent_region": [(0.1, 0.8), (0.8, 0.1)],  # High alibi, low motive
                "guilty_region": [(0.8, 0.8), (0.9, 0.9)]     # Low alibi, high motive
            },
            {
                "title": "The Cyber Fraud Investigation", 
                "description": "Digital transactions need classification. Separate legitimate from fraudulent.",
                "evidence_types": ["Transaction Amount", "User Behavior Score"],
                "innocent_region": [(0.1, 0.1), (0.4, 0.4)],  # Low amount, normal behavior
                "guilty_region": [(0.7, 0.7), (0.9, 0.9)]     # High amount, suspicious behavior
            }
        ]
        return cases[self.case_number - 1] if self.case_number <= len(cases) else cases[0]
    
    def initialize(self):
        self.phase = "briefing"
        self._start_briefing()
        
    def _start_briefing(self):
        """Start case briefing"""
        case = self.current_case
        briefing_text = f"Case #{self.case_number}: {case['title']}. {case['description']}"
        self.dialogue_box.set_dialogue(briefing_text, "Chief Detective")
        
    def handle_event(self, event):
        # Handle slider events first
        if self.weight_sliders:
            for name, slider in self.weight_sliders.items():
                if slider.handle_event(event):
                    # Update perceptron weights when slider changes
                    if name == "w1":
                        self.weights[0] = slider.value
                    elif name == "w2":
                        self.weights[1] = slider.value
                    elif name == "bias":
                        self.bias = slider.value
        
        if event.type == pygame.KEYDOWN:
            if self.phase == "briefing":
                if event.key == pygame.K_SPACE:
                    self.phase = "investigating"
                    self._start_investigation()
            elif self.phase == "investigating":
                if event.key == pygame.K_SPACE and self.current_evidence:
                    self._classify_current_evidence()
                elif event.key == pygame.K_t:  # Train on current evidence
                    self._train_on_evidence()
                elif event.key == pygame.K_n:  # Next evidence
                    self._spawn_evidence()
                elif event.key == pygame.K_b and self.evidence_analyzed >= 10:  # Boss fight
                    self.phase = "boss_fight"
                    self._start_boss_fight()
            elif self.phase == "boss_fight":
                if event.key == pygame.K_SPACE:
                    self._boss_attack()
                elif event.key == pygame.K_t:  # Train during boss fight
                    self._boss_train()
                elif event.key == pygame.K_r:  # Reset perceptron
                    self._reset_perceptron()
            elif self.phase == "victory":
                if event.key == pygame.K_SPACE:
                    return "completed"
                        
            if event.key == pygame.K_ESCAPE:
                return "exit"
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_down(event.pos)
            
        return None
    
    def _handle_mouse_down(self, pos):
        """Handle mouse button down events"""
        # Check evidence classification
        if self.phase == "investigating" and self.current_evidence:
            # Check if clicking in scanner area
            if "main_content" in self.areas:
                main_rect = self.areas["main_content"]
                col_width = main_rect.width // 3
                scanner_rect = pygame.Rect(main_rect.x + col_width, main_rect.y + 10, col_width, main_rect.height - 20)
                if scanner_rect.collidepoint(pos):
                    self._classify_current_evidence()
    
    def _start_investigation(self):
        """Start the investigation phase"""
        investigation_text = "Investigation begins! Use your neural scanner to classify evidence. Press SPACE to classify or T to train the scanner."
        self.dialogue_box.set_dialogue(investigation_text, "Detective AI")
        self._spawn_evidence()
        
    def _spawn_evidence(self):
        """Spawn new evidence for classification"""
        case = self.current_case
        
        # Generate evidence based on case type
        if random.random() < 0.5:  # Innocent evidence
            region = case["innocent_region"]
            evidence_class = 0
            evidence_color = (100, 255, 100)  # Green
        else:  # Guilty evidence
            region = case["guilty_region"] 
            evidence_class = 1
            evidence_color = (255, 100, 100)  # Red
            
        # Generate random point in the region
        x = random.uniform(region[0][0], region[1][0])
        y = random.uniform(region[0][1], region[1][1])
        
        self.current_evidence = {
            'features': np.array([x, y]),
            'true_class': evidence_class,
            'color': evidence_color,
            'description': self._generate_evidence_description(x, y, evidence_class)
        }
        
        # Add some visual feedback
        self.scanner_pulse = 1.0
        
    def _generate_evidence_description(self, x, y, evidence_class):
        """Generate descriptive text for evidence"""
        case = self.current_case
        feature1_name = case["evidence_types"][0]
        feature2_name = case["evidence_types"][1]
        
        feature1_level = "High" if x > 0.5 else "Low"
        feature2_level = "High" if y > 0.5 else "Low"
        
        return f"{feature1_name}: {feature1_level}, {feature2_name}: {feature2_level}"
    
    def _classify_current_evidence(self):
        """Classify the current evidence using the perceptron"""
        if not self.current_evidence:
            return
            
        features = self.current_evidence['features']
        true_class = self.current_evidence['true_class']
        
        # Perceptron prediction
        activation = np.dot(self.weights, features) + self.bias
        predicted_class = 1 if activation > 0 else 0
        
        # Check if correct
        is_correct = predicted_class == true_class
        
        # Update stats
        self.evidence_analyzed += 1
        if is_correct:
            self.correct_classifications += 1
            
        # Visual feedback
        if is_correct:
            self.classification_feedback = "CORRECT! ✓"
            feedback_color = (0, 255, 0)
            # Add success particles at screen center
            center_x = self.screen_width // 2
            center_y = self.screen_height // 2
            for _ in range(10):
                self.particles.add_particle(
                    center_x + random.randint(-50, 50),
                    center_y + random.randint(-50, 50),
                    (random.uniform(-30, 30), random.uniform(-50, -10)),
                    (0, 255, 0),
                    random.uniform(0.5, 1.0),
                    random.randint(3, 6)
                )
        else:
            self.classification_feedback = "WRONG! ✗"
            feedback_color = (255, 0, 0)
            
        self.feedback_timer = 2.0  # Show feedback for 2 seconds
        
        # Update progress
        accuracy = self.correct_classifications / max(1, self.evidence_analyzed)
        if self.accuracy_bar:
            self.accuracy_bar.set_value(accuracy * 100)
        if self.case_progress_bar:
            self.case_progress_bar.set_value((self.evidence_analyzed / 20) * 100)  # Need 20 evidence pieces
        
        # Check if ready for boss fight
        if self.evidence_analyzed >= 10:
            boss_ready_text = "🔥 BOSS READY! Press B to face the Linear Separatrix!"
            self.dialogue_box.set_dialogue(boss_ready_text, "Detective AI")
        else:
            # Spawn next evidence after delay
            pygame.time.set_timer(pygame.USEREVENT + 1, 1500)  # 1.5 second delay
            
    def _train_on_evidence(self):
        """Train the perceptron on current evidence"""
        if not self.current_evidence:
            return
            
        features = self.current_evidence['features']
        true_class = self.current_evidence['true_class']
        
        # Perceptron learning rule
        activation = np.dot(self.weights, features) + self.bias
        predicted_class = 1 if activation > 0 else 0
        
        if predicted_class != true_class:
            # Update weights
            error = true_class - predicted_class
            self.weights += self.learning_rate * error * features
            self.bias += self.learning_rate * error
            
            # Update sliders to reflect new weights
            self.weight_sliders['w1']['value'] = self.weights[0]
            self.weight_sliders['w2']['value'] = self.weights[1] 
            self.weight_sliders['bias']['value'] = self.bias
            
            # Visual feedback for training
            training_text = "Neural scanner updated! Weights adjusted based on evidence."
            self.dialogue_box.set_dialogue(training_text, "Detective AI")
            
    def _start_analysis(self):
        """Start case analysis phase"""
        accuracy = self.correct_classifications / max(1, self.evidence_analyzed)
        
        if accuracy >= 0.8:
            analysis_text = f"Excellent work! {accuracy:.1%} accuracy. The neural scanner is well-trained."
        elif accuracy >= 0.6:
            analysis_text = f"Good progress. {accuracy:.1%} accuracy. More training could improve results."
        else:
            analysis_text = f"Needs improvement. {accuracy:.1%} accuracy. Consider adjusting the scanner parameters."
            
        self.dialogue_box.set_dialogue(analysis_text, "Chief Detective")
        
    def _show_verdict(self):
        """Show final case verdict"""
        accuracy = self.correct_classifications / max(1, self.evidence_analyzed)
        
        if accuracy >= 0.8:
            self.case_solved = True
            self.detective_rank = "Expert Detective"
            verdict_text = "Case SOLVED! Your neural scanner successfully classified the evidence. Promotion earned!"
        else:
            verdict_text = "Case needs more work. Train your scanner better and try again."
            
        self.dialogue_box.set_dialogue(verdict_text, "Judge")
        
    def _start_boss_fight(self):
        """Start the epic boss fight against Linear Separatrix"""
        self.boss_hp = 100
        self.boss_phase = 1
        self.player_score = 0
        self.boss_challenge_active = True
        
        boss_intro = "I am the Linear Separatrix! Master of decision boundaries! Your perceptron cannot defeat my linearly separable challenges!"
        self.dialogue_box.set_dialogue(boss_intro, "Linear Separatrix")
        
        # Generate boss's first challenge - perfectly separable data
        self._generate_boss_challenge()
        
    def _generate_boss_challenge(self):
        """Generate boss challenge data based on current phase"""
        self.boss_data_points = []
        
        if self.boss_phase == 1:
            # Phase 1: Perfect linear separation
            # Class 0: bottom-left region
            for _ in range(8):
                x = random.uniform(0.1, 0.4)
                y = random.uniform(0.1, 0.4)
                self.boss_data_points.append({'pos': [x, y], 'class': 0, 'color': (100, 255, 100)})
            
            # Class 1: top-right region  
            for _ in range(8):
                x = random.uniform(0.6, 0.9)
                y = random.uniform(0.6, 0.9)
                self.boss_data_points.append({'pos': [x, y], 'class': 1, 'color': (255, 100, 100)})
                
        elif self.boss_phase == 2:
            # Phase 2: Add noise to make it harder
            for _ in range(6):
                x = random.uniform(0.1, 0.4) + random.uniform(-0.1, 0.1)
                y = random.uniform(0.1, 0.4) + random.uniform(-0.1, 0.1)
                self.boss_data_points.append({'pos': [max(0, min(1, x)), max(0, min(1, y))], 'class': 0, 'color': (100, 255, 100)})
            
            for _ in range(6):
                x = random.uniform(0.6, 0.9) + random.uniform(-0.1, 0.1)
                y = random.uniform(0.6, 0.9) + random.uniform(-0.1, 0.1)
                self.boss_data_points.append({'pos': [max(0, min(1, x)), max(0, min(1, y))], 'class': 1, 'color': (255, 100, 100)})
                
            # Add some tricky points near the boundary
            for _ in range(4):
                x = random.uniform(0.4, 0.6)
                y = random.uniform(0.4, 0.6)
                true_class = 1 if x + y > 1.0 else 0
                color = (255, 100, 100) if true_class == 1 else (100, 255, 100)
                self.boss_data_points.append({'pos': [x, y], 'class': true_class, 'color': color})
                
        elif self.boss_phase == 3:
            # Phase 3: Nearly non-linear (still solvable by perceptron but very challenging)
            for _ in range(12):
                x = random.uniform(0.0, 1.0)
                y = random.uniform(0.0, 1.0)
                # Complex but still linear boundary: x + 2*y > 1.2
                true_class = 1 if x + 2*y > 1.2 else 0
                color = (255, 100, 100) if true_class == 1 else (100, 255, 100)
                self.boss_data_points.append({'pos': [x, y], 'class': true_class, 'color': color})
    
    def _boss_attack(self):
        """Player attempts to classify boss's challenge data"""
        if not self.boss_data_points:
            return
            
        correct_count = 0
        total_count = len(self.boss_data_points)
        
        # Test perceptron on all boss data points
        for point in self.boss_data_points:
            features = np.array(point['pos'])
            true_class = point['class']
            
            # Perceptron prediction
            activation = np.dot(self.weights, features) + self.bias
            predicted_class = 1 if activation > 0 else 0
            
            if predicted_class == true_class:
                correct_count += 1
                
        accuracy = correct_count / total_count
        
        # Calculate damage based on accuracy
        if accuracy >= 0.9:
            damage = 25
            feedback = f"CRITICAL HIT! {accuracy:.1%} accuracy! Perfect separation!"
            feedback_color = (255, 255, 0)
        elif accuracy >= 0.75:
            damage = 15
            feedback = f"GOOD HIT! {accuracy:.1%} accuracy! Strong boundary!"
            feedback_color = (0, 255, 0)
        elif accuracy >= 0.6:
            damage = 8
            feedback = f"Weak hit. {accuracy:.1%} accuracy. Boundary needs work."
            feedback_color = (255, 200, 0)
        else:
            damage = 0
            feedback = f"MISS! {accuracy:.1%} accuracy. Your perceptron is confused!"
            feedback_color = (255, 0, 0)
            
        self.boss_hp -= damage
        self.player_score += damage
        
        # Boss counter-attack based on phase
        if damage == 0:
            self._boss_counter_attack()
            
        self.dialogue_box.set_dialogue(feedback, "Battle System")
        
        # Check phase transitions
        if self.boss_hp <= 66 and self.boss_phase == 1:
            self.boss_phase = 2
            self._boss_phase_transition()
        elif self.boss_hp <= 33 and self.boss_phase == 2:
            self.boss_phase = 3
            self._boss_phase_transition()
        elif self.boss_hp <= 0:
            self.phase = "victory"
            self._boss_victory()
            
    def _boss_train(self):
        """Train perceptron on boss's challenge data"""
        if not self.boss_data_points:
            return
            
        # Train on a random subset of boss data
        training_points = random.sample(self.boss_data_points, min(4, len(self.boss_data_points)))
        
        for point in training_points:
            features = np.array(point['pos'])
            true_class = point['class']
            
            # Perceptron learning rule
            activation = np.dot(self.weights, features) + self.bias
            predicted_class = 1 if activation > 0 else 0
            
            if predicted_class != true_class:
                error = true_class - predicted_class
                self.weights += self.learning_rate * error * features
                self.bias += self.learning_rate * error
                
        # Update sliders
        self.weight_sliders['w1']['value'] = np.clip(self.weights[0], -1, 1)
        self.weight_sliders['w2']['value'] = np.clip(self.weights[1], -1, 1)
        self.weight_sliders['bias']['value'] = np.clip(self.bias, -1, 1)
        
        train_feedback = "Perceptron trained on boss data! Weights updated!"
        self.dialogue_box.set_dialogue(train_feedback, "Detective AI")
        
    def _boss_counter_attack(self):
        """Boss counter-attacks by corrupting the perceptron"""
        attack_type = random.choice(['weight_corruption', 'bias_shift', 'data_poison'])
        
        if attack_type == 'weight_corruption':
            self.weights += np.random.normal(0, 0.1, 2)
            attack_msg = "Weight Corruption Attack! Your perceptron's weights are scrambled!"
        elif attack_type == 'bias_shift':
            self.bias += random.uniform(-0.2, 0.2)
            attack_msg = "Bias Shift Attack! Your decision threshold is moved!"
        else:  # data_poison
            # Add misleading data points
            for _ in range(2):
                x, y = random.uniform(0, 1), random.uniform(0, 1)
                wrong_class = random.choice([0, 1])
                color = (255, 100, 100) if wrong_class == 1 else (100, 255, 100)
                self.boss_data_points.append({'pos': [x, y], 'class': wrong_class, 'color': color})
            attack_msg = "Data Poisoning Attack! Fake evidence added to confuse you!"
            
        self.dialogue_box.set_dialogue(attack_msg, "Linear Separatrix")
        
    def _boss_phase_transition(self):
        """Handle boss phase transitions"""
        if self.boss_phase == 2:
            transition_msg = "Phase 2: Noise Corruption! I'm adding noise to make separation harder!"
        elif self.boss_phase == 3:
            transition_msg = "Final Phase: Complex Boundary! Can your linear perceptron handle this?!"
            
        self.dialogue_box.set_dialogue(transition_msg, "Linear Separatrix")
        self._generate_boss_challenge()
        
    def _boss_victory(self):
        """Handle boss victory"""
        victory_msg = f"Victory! You mastered the perceptron! Final score: {self.player_score}/100"
        self.dialogue_box.set_dialogue(victory_msg, "Detective AI")
        self.case_solved = True
        
    def _reset_perceptron(self):
        """Reset perceptron to random weights"""
        self.weights = np.random.uniform(-0.5, 0.5, 2)
        self.bias = np.random.uniform(-0.5, 0.5)
        
        # Update sliders
        self.weight_sliders['w1']['value'] = self.weights[0]
        self.weight_sliders['w2']['value'] = self.weights[1]
        self.weight_sliders['bias']['value'] = self.bias
        
        reset_msg = "Perceptron reset! New random weights assigned."
        self.dialogue_box.set_dialogue(reset_msg, "Detective AI")
        
    def update(self, dt):
        """Update game state"""
        self.dialogue_box.update(dt)
        if self.accuracy_bar:
            self.accuracy_bar.update(dt)
        if self.case_progress_bar:
            self.case_progress_bar.update(dt)
        self.particles.update(dt)
        
        # Update scanner pulse effect
        if self.scanner_pulse > 0:
            self.scanner_pulse -= dt * 2
            
        # Update feedback timer
        if self.feedback_timer > 0:
            self.feedback_timer -= dt
            
        # Handle evidence spawn timer
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT + 1:
                self._spawn_evidence()
                pygame.time.set_timer(pygame.USEREVENT + 1, 0)  # Cancel timer
                
    def render(self, screen):
        """Render the game with fully responsive layout"""
        # Update layout for current phase
        self._update_layout_for_phase()
        
        # Background gradient
        for y in range(self.layout.screen_height):
            intensity = int(20 + (y / self.layout.screen_height) * 40)
            color = (intensity, intensity + 10, intensity + 30)
            pygame.draw.line(screen, color, (0, y), (self.layout.screen_width, y))
        
        # Render title
        self._render_title(screen)
        
        # Render progress bars (if not boss fight)
        if self.phase != "boss_fight" and "progress" in self.areas:
            self._render_progress_bars(screen)
        
        # Render phase-specific content
        if self.phase == "briefing":
            self._render_briefing(screen)
        elif self.phase == "investigating":
            self._render_investigation(screen)
        elif self.phase == "boss_fight":
            self._render_boss_fight(screen)
        elif self.phase == "victory":
            self._render_victory(screen)
        
        # Always render dialogue
        self._render_dialogue(screen)
        
        # Render particles
        self.particles.render(screen)
    
    def _render_title(self, screen):
        """Render clean title"""
        if "title" not in self.areas:
            return
            
        title_rect = self.areas["title"]
        self.clean_layout.render_text(screen, "🕵️ Neural Detective Agency", title_rect,
                                    self.clean_layout.title_size, (255, 255, 100))
    
    def _render_progress_bars(self, screen):
        """Render responsive progress bars"""
        if not self.accuracy_bar or not self.case_progress_bar:
            self._create_progress_bars()
        
        progress_rect = self.areas["progress"]
        font_size = self.layout.get_font_size(0.02, min_size=10, max_size=16)
        font = pygame.font.Font(None, font_size)
        
        # Accuracy bar
        acc_label = font.render("Accuracy", True, (255, 255, 255))
        screen.blit(acc_label, (self.accuracy_bar.rect.x, self.accuracy_bar.rect.y - 20))
        self.accuracy_bar.render(screen, font)
        
        # Case progress bar
        case_label = font.render("Case Progress", True, (255, 255, 255))
        screen.blit(case_label, (self.case_progress_bar.rect.x, self.case_progress_bar.rect.y - 20))
        self.case_progress_bar.render(screen, font)
    
    def _render_dialogue(self, screen):
        """Render clean dialogue"""
        if "dialogue" not in self.areas:
            return
            
        dialogue_rect = self.areas["dialogue"]
        
        # Draw dialogue panel
        self.clean_layout.draw_panel(screen, dialogue_rect, (20, 30, 50), (100, 150, 200))
        
        # Render dialogue text
        if hasattr(self.dialogue_box, 'displayed_text') and self.dialogue_box.displayed_text:
            # Character name
            if hasattr(self.dialogue_box, 'character_name') and self.dialogue_box.character_name:
                name_rect = pygame.Rect(dialogue_rect.x + 20, dialogue_rect.y + 10, dialogue_rect.width - 40, 30)
                self.clean_layout.render_text(screen, self.dialogue_box.character_name, name_rect,
                                            self.clean_layout.header_size, (255, 255, 100), "left")
                text_y = dialogue_rect.y + 50
            else:
                text_y = dialogue_rect.y + 20
            
            # Dialogue text
            text_rect = pygame.Rect(dialogue_rect.x + 20, text_y, dialogue_rect.width - 40, dialogue_rect.height - (text_y - dialogue_rect.y) - 20)
            self.clean_layout.render_text(screen, self.dialogue_box.displayed_text, text_rect,
                                        self.clean_layout.body_size, (255, 255, 255), "left")
    
    def _render_sliders(self, screen):
        """Render weight sliders with responsive layout"""
        slider_font_size = max(12, int(self.screen_height * 0.02))
        slider_font = pygame.font.Font(None, slider_font_size)
        
        for slider_name, slider in self.weight_sliders.items():
            rect = slider['rect']
            value = slider['value']
            label = slider['label']
            
            # Slider background
            pygame.draw.rect(screen, (60, 60, 60), rect, border_radius=5)
            
            # Slider fill (based on value from -1 to 1)
            fill_width = int(((value + 1) / 2) * rect.width)
            if fill_width > 0:
                fill_rect = pygame.Rect(rect.x, rect.y, fill_width, rect.height)
                color = (100, 255, 100) if value >= 0 else (255, 100, 100)
                pygame.draw.rect(screen, color, fill_rect, border_radius=5)
            
            # Slider border
            pygame.draw.rect(screen, (200, 200, 200), rect, 2, border_radius=5)
            
            # Slider handle
            handle_x = rect.x + int(((value + 1) / 2) * rect.width) - 5
            handle_rect = pygame.Rect(handle_x, rect.y - 2, 10, rect.height + 4)
            pygame.draw.rect(screen, (255, 255, 255), handle_rect, border_radius=3)
            
            # Label above slider
            label_surface = slider_font.render(label, True, (255, 255, 255))
            screen.blit(label_surface, (rect.x, rect.y - 25))
            
            # Value below slider
            value_text = f"{value:.2f}"
            value_surface = slider_font.render(value_text, True, (200, 200, 200))
            value_rect = value_surface.get_rect(center=(rect.centerx, rect.bottom + 15))
            screen.blit(value_surface, value_rect)
        
    def _render_briefing(self, screen):
        """Render case briefing with fully responsive layout"""
        if "main_content" not in self.areas:
            return
            
        case = self.current_case
        main_rect = self.areas["main_content"]
        
        # Case file (centered in main content area)
        case_rect = self.layout.get_centered_rect(0.7, 0.8, y_percent=0.4)
        
        # Background
        pygame.draw.rect(screen, (50, 50, 70), case_rect, border_radius=10)
        pygame.draw.rect(screen, (200, 200, 200), case_rect, 3, border_radius=10)
        
        # Case title
        title_font_size = self.layout.get_font_size(0.04, min_size=16, max_size=28)
        title_font = pygame.font.Font(None, title_font_size)
        
        title_rect = pygame.Rect(case_rect.x, case_rect.y + 10, case_rect.width, int(case_rect.height * 0.15))
        self.layout.render_text_block(screen, case["title"], title_font, title_rect,
                                    (255, 255, 100), align="center", vertical_align="center")
        
        # Case description
        desc_font_size = self.layout.get_font_size(0.025, min_size=12, max_size=18)
        desc_font = pygame.font.Font(None, desc_font_size)
        
        desc_rect = pygame.Rect(case_rect.x + 20, case_rect.y + int(case_rect.height * 0.2),
                               case_rect.width - 40, int(case_rect.height * 0.6))
        self.layout.render_text_block(screen, case["description"], desc_font, desc_rect,
                                    (255, 255, 255), align="left", vertical_align="top")
        
        # Evidence types
        evidence_font_size = self.layout.get_font_size(0.02, min_size=10, max_size=16)
        evidence_font = pygame.font.Font(None, evidence_font_size)
        evidence_text = f"Evidence Types: {', '.join(case['evidence_types'])}"
        
        evidence_rect = pygame.Rect(case_rect.x + 20, case_rect.y + int(case_rect.height * 0.85),
                                   case_rect.width - 40, int(case_rect.height * 0.1))
        self.layout.render_text_block(screen, evidence_text, evidence_font, evidence_rect,
                                    (200, 255, 200), align="left", vertical_align="center")
        
        # Instructions
        instruction_font_size = self.layout.get_font_size(0.03, min_size=14, max_size=20)
        instruction_font = pygame.font.Font(None, instruction_font_size)
        instruction_text = "Press SPACE to begin investigation"
        
        instruction_rect = pygame.Rect(main_rect.x, case_rect.bottom + 20,
                                     main_rect.width, 40)
        self.layout.render_text_block(screen, instruction_text, instruction_font, instruction_rect,
                                    (255, 255, 0), align="center", vertical_align="center")
        
    def _render_investigation(self, screen):
        """Render investigation phase with clean, readable layout"""
        if "main" not in self.areas:
            return
            
        main_rect = self.areas["main"]
        
        # Create 3-column layout with clean spacing
        columns = self.clean_layout.split_horizontal(main_rect, 3)
        
        # Render evidence display
        self._render_clean_evidence(screen, columns[0])
        
        # Render neural scanner
        self._render_clean_scanner(screen, columns[1])
        
        # Render stats display
        self._render_clean_stats(screen, columns[2])
        
        # Render controls
        if "controls" in self.areas:
            self._render_clean_controls(screen)
    
    def _render_evidence_display(self, screen, rect):
        """Render evidence display area"""
        if not self.current_evidence:
            # Empty state
            pygame.draw.rect(screen, (40, 40, 50), rect, border_radius=8)
            pygame.draw.rect(screen, (100, 100, 120), rect, 2, border_radius=8)
            
            font_size = self.layout.get_font_size(0.025, min_size=12, max_size=18)
            font = pygame.font.Font(None, font_size)
            self.layout.render_text_block(screen, "No Evidence\nPress N for next", font, rect,
                                        (150, 150, 150), align="center", vertical_align="center")
            return
        
        # Draw evidence background
        pygame.draw.rect(screen, self.current_evidence['color'], rect, border_radius=8)
        pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=8)
        
        # Title
        title_font_size = self.layout.get_font_size(0.02, min_size=10, max_size=16)
        title_font = pygame.font.Font(None, title_font_size)
        title_rect = pygame.Rect(rect.x, rect.y - 25, rect.width, 20)
        title_surface = title_font.render("Current Evidence", True, (255, 255, 255))
        screen.blit(title_surface, (title_rect.x, title_rect.y))
        
        # Evidence description
        desc_font_size = self.layout.get_font_size(0.018, min_size=9, max_size=14)
        desc_font = pygame.font.Font(None, desc_font_size)
        
        content_rect = pygame.Rect(rect.x + 10, rect.y + 10, rect.width - 20, rect.height - 20)
        self.layout.render_text_block(screen, self.current_evidence['description'], desc_font,
                                    content_rect, (0, 0, 0), align="left", vertical_align="top")
    
    def _render_neural_scanner(self, screen, rect):
        """Render neural scanner area"""
        # Scanner color with pulse effect
        scanner_color = (100, 150, 255)
        if self.scanner_pulse > 0:
            pulse_intensity = int(self.scanner_pulse * 100)
            scanner_color = (100 + pulse_intensity, 150 + pulse_intensity, 255)
        
        pygame.draw.rect(screen, scanner_color, rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), rect, 3, border_radius=10)
        
        # Title
        title_font_size = self.layout.get_font_size(0.025, min_size=12, max_size=18)
        title_font = pygame.font.Font(None, title_font_size)
        title_rect = pygame.Rect(rect.x, rect.y - 25, rect.width, 20)
        title_surface = title_font.render("🔍 Neural Scanner", True, (255, 255, 255))
        title_text_rect = title_surface.get_rect(center=(title_rect.centerx, title_rect.centery))
        screen.blit(title_surface, title_text_rect)
        
        # Scanner content
        if self.current_evidence:
            content_font_size = self.layout.get_font_size(0.04, min_size=16, max_size=24)
            content_font = pygame.font.Font(None, content_font_size)
            
            instructions = "Click to Classify\nor press SPACE"
            self.layout.render_text_block(screen, instructions, content_font, rect,
                                        (255, 255, 255), align="center", vertical_align="center")
        else:
            content_font_size = self.layout.get_font_size(0.035, min_size=14, max_size=20)
            content_font = pygame.font.Font(None, content_font_size)
            
            self.layout.render_text_block(screen, "Scanner Ready\nWaiting for evidence", content_font, rect,
                                        (200, 200, 200), align="center", vertical_align="center")
        
        # Classification feedback
        if self.feedback_timer > 0 and self.classification_feedback:
            feedback_font_size = self.layout.get_font_size(0.03, min_size=14, max_size=20)
            feedback_font = pygame.font.Font(None, feedback_font_size)
            feedback_color = (100, 255, 100) if "CORRECT" in self.classification_feedback else (255, 100, 100)
            
            feedback_rect = pygame.Rect(rect.x, rect.bottom + 10, rect.width, 30)
            feedback_surface = feedback_font.render(self.classification_feedback, True, feedback_color)
            feedback_text_rect = feedback_surface.get_rect(center=feedback_rect.center)
            screen.blit(feedback_surface, feedback_text_rect)
    
    def _render_stats_display(self, screen, rect):
        """Render stats display area"""
        # Background
        pygame.draw.rect(screen, (30, 40, 60), rect, border_radius=8)
        pygame.draw.rect(screen, (100, 150, 200), rect, 2, border_radius=8)
        
        # Title
        title_font_size = self.layout.get_font_size(0.02, min_size=10, max_size=16)
        title_font = pygame.font.Font(None, title_font_size)
        title_rect = pygame.Rect(rect.x, rect.y - 25, rect.width, 20)
        title_surface = title_font.render("Detective Stats", True, (255, 255, 100))
        screen.blit(title_surface, (title_rect.x, title_rect.y))
        
        # Stats content
        accuracy = self.correct_classifications / max(1, self.evidence_analyzed) if self.evidence_analyzed > 0 else 0
        
        stats_text = f"""Evidence: {self.evidence_analyzed}
Correct: {self.correct_classifications}
Accuracy: {accuracy:.1%}
Rank: {self.detective_rank}

Weights:
W1: {self.weights[0]:.2f}
W2: {self.weights[1]:.2f}
Bias: {self.bias:.2f}"""
        
        content_font_size = self.layout.get_font_size(0.035, min_size=14, max_size=20)
        content_font = pygame.font.Font(None, content_font_size)
        
        content_rect = pygame.Rect(rect.x + 10, rect.y + 10, rect.width - 20, rect.height - 20)
        
        # Render with special color for accuracy
        lines = stats_text.split('\n')
        line_height = content_font.get_height() + 2
        
        for i, line in enumerate(lines):
            if line.strip():
                y_pos = content_rect.y + i * line_height
                if y_pos + line_height > content_rect.bottom:
                    break
                
                color = (100, 255, 100) if "Accuracy" in line and accuracy >= 0.8 else (255, 255, 255)
                line_surface = content_font.render(line, True, color)
                screen.blit(line_surface, (content_rect.x, y_pos))
    
    def _render_investigation_controls(self, screen):
        """Render investigation controls with responsive layout"""
        if not self.weight_sliders:
            self._create_weight_sliders()
        
        if "controls" not in self.areas:
            return
            
        controls_rect = self.areas["controls"]
        
        # Create responsive layout for sliders and instructions
        slider_height = max(25, int(controls_rect.height * 0.5))
        instruction_height = controls_rect.height - slider_height - self.layout.min_spacing
        
        # Slider area
        slider_area = pygame.Rect(controls_rect.x, controls_rect.y, controls_rect.width, slider_height)
        
        # Distribute sliders horizontally
        slider_rects = self.layout.distribute_horizontally(slider_area, len(self.weight_sliders))
        
        # Update and render sliders
        for i, (name, slider) in enumerate(self.weight_sliders.items()):
            if i < len(slider_rects):
                # Update slider position
                slider.rect = slider_rects[i]
                slider.render(screen)
        
        # Instructions area
        instruction_area = pygame.Rect(controls_rect.x, controls_rect.y + slider_height + self.layout.min_spacing,
                                     controls_rect.width, instruction_height)
        
        if instruction_height > 15:
            instruction_font_size = self.layout.get_font_size(0.03, min_size=16, max_size=22)
            instruction_font = pygame.font.Font(None, instruction_font_size)
            
            if self.evidence_analyzed >= 10:
                instructions = "SPACE: Classify | T: Train | B: BOSS FIGHT! | Drag sliders to adjust parameters"
            else:
                instructions = "SPACE: Classify | T: Train | Drag sliders to adjust neural scanner parameters"
            
            self.layout.render_text_block(screen, instructions, instruction_font, instruction_area,
                                        (200, 200, 200), align="center", vertical_align="center")
        
        # Classification feedback (overlay on main content area)
        if self.feedback_timer > 0 and self.classification_feedback:
            feedback_font_size = self.layout.get_font_size(0.03, min_size=16, max_size=32)
            feedback_font = pygame.font.Font(None, feedback_font_size)
            feedback_color = (0, 255, 0) if "CORRECT" in self.classification_feedback else (255, 0, 0)
            feedback_surface = feedback_font.render(self.classification_feedback, True, feedback_color)
            feedback_rect = feedback_surface.get_rect(center=(self.layout.screen_width // 2, self.layout.screen_height // 3))
            screen.blit(feedback_surface, feedback_rect)
        
    def _render_sliders(self, screen):
        """Render interactive weight sliders"""
        for slider_name, slider in self.weight_sliders.items():
            # Slider track
            pygame.draw.rect(screen, (100, 100, 100), slider['rect'])
            pygame.draw.rect(screen, (255, 255, 255), slider['rect'], 2)
            
            # Slider handle
            handle_x = slider['rect'].x + (slider['value'] + 1) / 2 * slider['rect'].width
            handle_rect = pygame.Rect(handle_x - 5, slider['rect'].y - 5, 10, slider['rect'].height + 10)
            pygame.draw.rect(screen, (255, 200, 0), handle_rect)
            
            # Label and value
            label_font = pygame.font.Font(None, 16)
            label_text = f"{slider['label']}: {slider['value']:.2f}"
            label_surface = label_font.render(label_text, True, (255, 255, 255))
            screen.blit(label_surface, (slider['rect'].x, slider['rect'].y - 20))
            
    def _render_analysis(self, screen):
        """Render case analysis"""
        analysis_rect = pygame.Rect(150, 200, 500, 200)
        pygame.draw.rect(screen, (40, 60, 80), analysis_rect)
        pygame.draw.rect(screen, (200, 200, 200), analysis_rect, 3)
        
        # Analysis title
        title_font = pygame.font.Font(None, 32)
        title = title_font.render("📊 Case Analysis", True, (255, 255, 100))
        title_rect = title.get_rect(center=(analysis_rect.centerx, analysis_rect.y + 30))
        screen.blit(title, title_rect)
        
        # Results
        accuracy = self.correct_classifications / max(1, self.evidence_analyzed)
        results_font = pygame.font.Font(None, 24)
        
        results_lines = [
            f"Evidence Pieces Analyzed: {self.evidence_analyzed}",
            f"Correct Classifications: {self.correct_classifications}",
            f"Final Accuracy: {accuracy:.1%}",
            "",
            "Press SPACE to see verdict"
        ]
        
        for i, line in enumerate(results_lines):
            if line:
                color = (0, 255, 0) if accuracy >= 0.8 and "Accuracy" in line else (255, 255, 255)
                line_surface = results_font.render(line, True, color)
                line_rect = line_surface.get_rect(center=(analysis_rect.centerx, analysis_rect.y + 80 + i * 30))
                screen.blit(line_surface, line_rect)
                
    def _render_verdict(self, screen):
        """Render final verdict"""
        verdict_rect = pygame.Rect(100, 180, 600, 250)
        
        if self.case_solved:
            pygame.draw.rect(screen, (0, 80, 0), verdict_rect)
            pygame.draw.rect(screen, (0, 255, 0), verdict_rect, 4)
            verdict_color = (0, 255, 0)
            verdict_text = "🎉 CASE SOLVED! 🎉"
        else:
            pygame.draw.rect(screen, (80, 40, 0), verdict_rect)
            pygame.draw.rect(screen, (255, 100, 0), verdict_rect, 4)
            verdict_color = (255, 100, 0)
            verdict_text = "📋 CASE REVIEW NEEDED"
            
        # Verdict title
        title_font = pygame.font.Font(None, 36)
        title = title_font.render(verdict_text, True, verdict_color)
        title_rect = title.get_rect(center=(verdict_rect.centerx, verdict_rect.y + 40))
        screen.blit(title, title_rect)
        
        # Final stats
        accuracy = self.correct_classifications / max(1, self.evidence_analyzed)
        stats_font = pygame.font.Font(None, 20)
        
        stats_lines = [
            f"Detective Rank: {self.detective_rank}",
            f"Final Accuracy: {accuracy:.1%}",
            f"Evidence Analyzed: {self.evidence_analyzed}",
            "",
            "Press SPACE to continue" if self.case_solved else "Press SPACE to retry"
        ]
        
        for i, line in enumerate(stats_lines):
            if line:
                line_surface = stats_font.render(line, True, (255, 255, 255))
                line_rect = line_surface.get_rect(center=(verdict_rect.centerx, verdict_rect.y + 100 + i * 25))
                screen.blit(line_surface, line_rect)
                
    def _render_boss_fight(self, screen):
        """Render boss fight with fully responsive layout"""
        # Boss header
        if "boss_header" in self.areas:
            self._render_boss_header(screen)
        
        # Main content area
        if "main_content" in self.areas:
            self._render_boss_main_content(screen)
        
        # Controls area
        if "controls" in self.areas:
            self._render_boss_controls(screen)
    
    def _render_boss_header(self, screen):
        """Render responsive boss header"""
        boss_rect = self.areas["boss_header"]
        
        # Phase-based boss appearance
        if self.boss_phase == 1:
            boss_color = (100, 200, 100)
            phase_name = "Linear Separation"
        elif self.boss_phase == 2:
            boss_color = (200, 200, 100)
            phase_name = "Noise Corruption"
        else:
            boss_color = (200, 100, 100)
            phase_name = "Complex Boundary"
        
        # Draw boss background
        pygame.draw.rect(screen, boss_color, boss_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), boss_rect, 3, border_radius=10)
        
        # Boss title
        title_font_size = self.layout.get_font_size(0.03, min_size=14, max_size=24)
        title_font = pygame.font.Font(None, title_font_size)
        title_text = f"⚔️ Linear Separatrix - Phase {self.boss_phase}: {phase_name}"
        
        # Title area (top 40% of boss header)
        title_rect = pygame.Rect(boss_rect.x, boss_rect.y, boss_rect.width, int(boss_rect.height * 0.4))
        self.layout.render_text_block(screen, title_text, title_font, title_rect, 
                                    (255, 255, 255), align="center", vertical_align="center")
        
        # HP bar area (bottom 60% of boss header)
        hp_area = pygame.Rect(boss_rect.x, boss_rect.y + int(boss_rect.height * 0.4), 
                             boss_rect.width, int(boss_rect.height * 0.6))
        
        # HP bar
        hp_margin = int(hp_area.width * 0.15)
        hp_bar_height = max(12, int(hp_area.height * 0.4))
        hp_bar_rect = pygame.Rect(hp_area.x + hp_margin, 
                                 hp_area.y + (hp_area.height - hp_bar_height) // 2,
                                 hp_area.width - 2 * hp_margin, hp_bar_height)
        
        # Draw HP bar
        pygame.draw.rect(screen, (60, 0, 0), hp_bar_rect, border_radius=3)
        
        hp_ratio = self.boss_hp / self.boss_max_hp
        hp_width = int(hp_bar_rect.width * hp_ratio)
        if hp_width > 0:
            current_hp_rect = pygame.Rect(hp_bar_rect.x, hp_bar_rect.y, hp_width, hp_bar_rect.height)
            pygame.draw.rect(screen, (255, 50, 50), current_hp_rect, border_radius=3)
        
        pygame.draw.rect(screen, (255, 255, 255), hp_bar_rect, 2, border_radius=3)
        
        # HP text
        hp_font_size = self.layout.get_font_size(0.02, min_size=10, max_size=16)
        hp_font = pygame.font.Font(None, hp_font_size)
        hp_text = f"HP: {self.boss_hp}/{self.boss_max_hp}"
        hp_text_surface = hp_font.render(hp_text, True, (255, 255, 255))
        hp_text_rect = hp_text_surface.get_rect(center=(hp_bar_rect.centerx, hp_bar_rect.bottom + 15))
        screen.blit(hp_text_surface, hp_text_rect)
    
    def _render_boss_main_content(self, screen):
        """Render boss fight main content area"""
        main_rect = self.areas["main_content"]
        
        # Create responsive 2-column layout: Visualization (60%) | Stats (40%)
        columns = self.layout.distribute_horizontally(main_rect, 2)
        viz_rect = columns[0]
        stats_rect = columns[1]
        
        # Render visualization area
        self._render_boss_visualization(screen, viz_rect)
        
        # Render stats area
        self._render_boss_stats(screen, stats_rect)
    
    def _render_boss_visualization(self, screen, viz_rect):
        """Render boss data visualization"""
        # Make visualization square and centered
        size = min(viz_rect.width, viz_rect.height) - 20
        viz_x = viz_rect.x + (viz_rect.width - size) // 2
        viz_y = viz_rect.y + 10
        viz_area = pygame.Rect(viz_x, viz_y, size, size)
        
        # Background
        pygame.draw.rect(screen, (25, 30, 45), viz_area, border_radius=8)
        pygame.draw.rect(screen, (100, 150, 200), viz_area, 2, border_radius=8)
        
        # Title
        title_font_size = self.layout.get_font_size(0.025, min_size=12, max_size=18)
        title_font = pygame.font.Font(None, title_font_size)
        title_rect = pygame.Rect(viz_area.x, viz_area.y, viz_area.width, 25)
        self.layout.render_text_block(screen, "Boss Challenge Data", title_font, title_rect,
                                    (255, 255, 100), align="center", vertical_align="center")
        
        # Data area
        data_margin = max(10, int(size * 0.05))
        data_area = pygame.Rect(viz_area.x + data_margin, viz_area.y + 30,
                               viz_area.width - 2 * data_margin, viz_area.height - 40)
        
        # Draw grid
        grid_color = (60, 70, 90)
        for i in range(1, 4):
            x = data_area.x + i * data_area.width // 4
            y = data_area.y + i * data_area.height // 4
            pygame.draw.line(screen, grid_color, (x, data_area.y), (x, data_area.bottom), 1)
            pygame.draw.line(screen, grid_color, (data_area.x, y), (data_area.right, y), 1)
        
        # Draw data points
        point_size = max(3, int(size * 0.01))
        for point in self.boss_data_points:
            x, y = point['pos']
            screen_x = data_area.x + x * data_area.width
            screen_y = data_area.y + (1 - y) * data_area.height
            
            pygame.draw.circle(screen, point['color'], (int(screen_x), int(screen_y)), point_size + 1)
            pygame.draw.circle(screen, (255, 255, 255), (int(screen_x), int(screen_y)), point_size + 1, 1)
        
        # Draw decision boundary
        self._draw_decision_boundary(screen, data_area)
    
    def _render_boss_stats(self, screen, stats_rect):
        """Render boss battle stats"""
        # Background
        pygame.draw.rect(screen, (20, 25, 35), stats_rect, border_radius=8)
        pygame.draw.rect(screen, (100, 150, 200), stats_rect, 2, border_radius=8)
        
        # Title
        title_font_size = self.layout.get_font_size(0.025, min_size=12, max_size=18)
        title_font = pygame.font.Font(None, title_font_size)
        title_rect = pygame.Rect(stats_rect.x, stats_rect.y, stats_rect.width, 30)
        self.layout.render_text_block(screen, "Battle Stats", title_font, title_rect,
                                    (255, 255, 100), align="center", vertical_align="center")
        
        # Calculate accuracy
        boss_accuracy = 0
        if self.boss_data_points:
            correct = 0
            for point in self.boss_data_points:
                features = np.array(point['pos'])
                activation = np.dot(self.weights, features) + self.bias
                predicted = 1 if activation > 0 else 0
                if predicted == point['class']:
                    correct += 1
            boss_accuracy = correct / len(self.boss_data_points)
        
        # Stats content
        stats_font_size = self.layout.get_font_size(0.02, min_size=10, max_size=14)
        stats_font = pygame.font.Font(None, stats_font_size)
        
        stats_text = f"""Accuracy: {boss_accuracy:.1%}
Score: {self.player_score}
Phase: {self.boss_phase}/3
Data Points: {len(self.boss_data_points)}

Weights:
W1: {self.weights[0]:.2f}
W2: {self.weights[1]:.2f}
Bias: {self.bias:.2f}"""
        
        content_rect = pygame.Rect(stats_rect.x + 10, stats_rect.y + 35,
                                 stats_rect.width - 20, stats_rect.height - 45)
        
        # Color accuracy line green if good
        lines = stats_text.split('\n')
        line_height = stats_font.get_height() + 2
        
        for i, line in enumerate(lines):
            if line.strip():
                y_pos = content_rect.y + i * line_height
                if y_pos + line_height > content_rect.bottom:
                    break
                
                color = (100, 255, 100) if "Accuracy" in line and boss_accuracy >= 0.9 else (255, 255, 255)
                line_surface = stats_font.render(line, True, color)
                screen.blit(line_surface, (content_rect.x, y_pos))
    
    def _render_boss_controls(self, screen):
        """Render boss fight controls"""
        if not self.weight_sliders:
            self._create_weight_sliders()
        
        # Render sliders
        for slider in self.weight_sliders.values():
            slider.render(screen)
        
        # Instructions
        controls_rect = self.areas["controls"]
        
        # Find space below sliders for instructions
        slider_bottom = max(slider.rect.bottom + 25 for slider in self.weight_sliders.values())
        instruction_area = pygame.Rect(controls_rect.x, slider_bottom,
                                     controls_rect.width, controls_rect.bottom - slider_bottom)
        
        if instruction_area.height > 20:
            instruction_font_size = self.layout.get_font_size(0.018, min_size=10, max_size=14)
            instruction_font = pygame.font.Font(None, instruction_font_size)
            
            instructions = "SPACE: Attack Boss | T: Train | R: Reset | Drag sliders to adjust weights"
            self.layout.render_text_block(screen, instructions, instruction_font, instruction_area,
                                        (200, 200, 200), align="center", vertical_align="top")
            
            # Phase objective
            if instruction_area.height > 50:
                objective_area = pygame.Rect(instruction_area.x, instruction_area.y + 25,
                                           instruction_area.width, instruction_area.height - 25)
                
                if self.boss_phase == 1:
                    objective = "🎯 Achieve 90%+ accuracy to damage the boss!"
                elif self.boss_phase == 2:
                    objective = "⚡ Adapt to noise! Maintain high accuracy!"
                else:
                    objective = "🔥 Final Phase: Master the complex boundary!"
                
                self.layout.render_text_block(screen, objective, instruction_font, objective_area,
                                            (255, 255, 100), align="center", vertical_align="top")
        
    def _draw_decision_boundary(self, screen, rect):
        """Draw the perceptron's decision boundary"""
        if abs(self.weights[1]) < 0.001:  # Avoid division by zero
            return
            
        boundary_points = []
        
        # Calculate boundary line: w1*x + w2*y + bias = 0
        # Solve for y: y = -(w1*x + bias) / w2
        for x in np.linspace(0, 1, 50):
            y = -(self.weights[0] * x + self.bias) / self.weights[1]
            if 0 <= y <= 1:  # Only draw within bounds
                screen_x = rect.x + x * rect.width
                screen_y = rect.y + (1 - y) * rect.height
                boundary_points.append((screen_x, screen_y))
                
        # Draw the boundary line
        if len(boundary_points) >= 2:
            line_width = max(2, int(self.screen_height * 0.004))
            pygame.draw.lines(screen, (255, 255, 0), False, boundary_points, line_width)
            
    def _render_victory(self, screen):
        """Render victory screen with fully responsive layout"""
        if "main_content" not in self.areas:
            return
            
        main_rect = self.areas["main_content"]
        
        # Victory background (centered in main content)
        victory_rect = self.layout.get_centered_rect(0.8, 0.9, y_percent=0.4)
        
        pygame.draw.rect(screen, (0, 100, 0), victory_rect, border_radius=15)
        pygame.draw.rect(screen, (0, 255, 0), victory_rect, 5, border_radius=15)
        
        # Victory title
        title_font_size = self.layout.get_font_size(0.05, min_size=20, max_size=36)
        title_font = pygame.font.Font(None, title_font_size)
        
        title_rect = pygame.Rect(victory_rect.x, victory_rect.y + 10, 
                               victory_rect.width, int(victory_rect.height * 0.2))
        self.layout.render_text_block(screen, "🎉 PERCEPTRON MASTER! 🎉", title_font, title_rect,
                                    (255, 255, 0), align="center", vertical_align="center")
        
        # Victory stats
        stats_font_size = self.layout.get_font_size(0.025, min_size=14, max_size=20)
        stats_font = pygame.font.Font(None, stats_font_size)
        
        accuracy = self.correct_classifications / max(1, self.evidence_analyzed)
        stats_text = f"""You defeated the Linear Separatrix!

Final Score: {self.player_score}/100
Evidence Analyzed: {self.evidence_analyzed}
Final Accuracy: {accuracy:.1%}

You mastered perceptron concepts!

Press SPACE to continue your neural journey"""
        
        stats_rect = pygame.Rect(victory_rect.x + 20, victory_rect.y + int(victory_rect.height * 0.25),
                               victory_rect.width - 40, int(victory_rect.height * 0.7))
        
        # Render with special color for instruction
        lines = stats_text.split('\n')
        line_height = stats_font.get_height() + 5
        
        for i, line in enumerate(lines):
            if line.strip():
                y_pos = stats_rect.y + i * line_height
                if y_pos + line_height > stats_rect.bottom:
                    break
                
                color = (255, 255, 0) if "SPACE" in line else (255, 255, 255)
                line_surface = stats_font.render(line, True, color)
                line_rect = line_surface.get_rect(center=(victory_rect.centerx, y_pos))
                screen.blit(line_surface, line_rect)
    
    def _wrap_text(self, text, font, max_width):
        """Wrap text to fit within max_width"""
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if font.size(test_line)[0] <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
                
        if current_line:
            lines.append(' '.join(current_line))
            
        return lines
    
    def _render_clean_evidence(self, screen, rect):
        """Render evidence panel with clean, large text"""
        # Draw panel background
        self.clean_layout.draw_panel(screen, rect, (40, 60, 40), (100, 200, 100))
        
        # Title
        title_rect = pygame.Rect(rect.x, rect.y + 10, rect.width, 40)
        self.clean_layout.render_text(screen, "Current Evidence", title_rect, 
                                    self.clean_layout.header_size, (255, 255, 255))
        
        # Evidence content
        if self.current_evidence:
            content_rect = pygame.Rect(rect.x + 10, rect.y + 60, rect.width - 20, rect.height - 70)
            evidence_text = self._format_evidence_simple(self.current_evidence)
            self.clean_layout.render_text(screen, evidence_text, content_rect,
                                        self.clean_layout.body_size, (255, 255, 255), "left")
        else:
            content_rect = pygame.Rect(rect.x + 10, rect.y + 60, rect.width - 20, rect.height - 70)
            self.clean_layout.render_text(screen, "No evidence to analyze", content_rect,
                                        self.clean_layout.body_size, (150, 150, 150))
    
    def _render_clean_scanner(self, screen, rect):
        """Render scanner panel with clean, large text"""
        # Draw panel background
        self.clean_layout.draw_panel(screen, rect, (40, 40, 80), (100, 100, 200))
        
        # Title
        title_rect = pygame.Rect(rect.x, rect.y + 10, rect.width, 40)
        self.clean_layout.render_text(screen, "Neural Scanner", title_rect,
                                    self.clean_layout.header_size, (255, 255, 255))
        
        # Scanner content
        content_rect = pygame.Rect(rect.x + 10, rect.y + 60, rect.width - 20, rect.height - 70)
        if self.current_evidence:
            scanner_text = "Click to Classify\nor press SPACE"
        else:
            scanner_text = "Waiting for evidence..."
        
        self.clean_layout.render_text(screen, scanner_text, content_rect,
                                    self.clean_layout.body_size, (255, 255, 255))
        
        # Classification feedback
        if self.feedback_timer > 0 and self.classification_feedback:
            feedback_color = (0, 255, 0) if "CORRECT" in self.classification_feedback else (255, 0, 0)
            feedback_rect = pygame.Rect(rect.x, rect.y + rect.height - 50, rect.width, 40)
            self.clean_layout.render_text(screen, self.classification_feedback, feedback_rect,
                                        self.clean_layout.header_size, feedback_color)
    
    def _render_clean_stats(self, screen, rect):
        """Render stats panel with clean, large text"""
        # Draw panel background
        self.clean_layout.draw_panel(screen, rect, (60, 40, 40), (200, 100, 100))
        
        # Title
        title_rect = pygame.Rect(rect.x, rect.y + 10, rect.width, 40)
        self.clean_layout.render_text(screen, "Detective Stats", title_rect,
                                    self.clean_layout.header_size, (255, 255, 255))
        
        # Stats content
        content_rect = pygame.Rect(rect.x + 10, rect.y + 60, rect.width - 20, rect.height - 70)
        
        accuracy = (self.correct_classifications / max(1, self.evidence_analyzed)) * 100
        stats_text = f"""Evidence: {self.evidence_analyzed}
Correct: {self.correct_classifications}
Accuracy: {accuracy:.0f}%
Rank: {self.detective_rank}

Weights:
W1: {self.weights[0]:.2f}
W2: {self.weights[1]:.2f}
Bias: {self.bias:.2f}"""
        
        self.clean_layout.render_text(screen, stats_text, content_rect,
                                    self.clean_layout.small_size, (255, 255, 255), "left")
    
    def _render_clean_controls(self, screen):
        """Render controls with clean, large text"""
        if "controls" not in self.areas:
            return
            
        controls_rect = self.areas["controls"]
        
        # Draw panel background
        self.clean_layout.draw_panel(screen, controls_rect, (30, 30, 30), (150, 150, 150))
        
        # Controls text
        if self.evidence_analyzed >= 10:
            controls_text = "SPACE: Classify | T: Train | B: BOSS FIGHT!"
        else:
            controls_text = "SPACE: Classify Evidence | T: Train Scanner"
        
        self.clean_layout.render_text(screen, controls_text, controls_rect,
                                    self.clean_layout.body_size, (255, 255, 255))
    
    def _format_evidence_simple(self, evidence):
        """Format evidence in a simple, readable way"""
        case = self.current_case
        features = evidence['features']
        
        feature1_name = case["evidence_types"][0]
        feature2_name = case["evidence_types"][1]
        
        feature1_level = "High" if features[0] > 0.5 else "Low"
        feature2_level = "High" if features[1] > 0.5 else "Low"
        
        return f"{feature1_name}: {feature1_level}\n{feature2_name}: {feature2_level}"