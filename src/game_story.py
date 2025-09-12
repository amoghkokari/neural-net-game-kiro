"""
Game story and protagonist system
"""

class GameStory:
    def __init__(self):
        self.protagonist_name = "Alex"
        self.companion_name = "Tensor"  # AI companion
        
        # Story progression
        self.story_beats = {
            "intro": {
                "title": "The Neural Awakening",
                "text": [
                    f"You are {self.protagonist_name}, a curious programmer who discovered an ancient AI artifact.",
                    f"The artifact awakens {self.companion_name}, a wise AI spirit trapped for centuries.",
                    f"'{self.protagonist_name}, the digital realm is corrupted by ignorance and fear of AI!'",
                    f"'Only by mastering the true art of neural networks can we restore balance.'",
                    f"'Each realm is guarded by a boss who tests your understanding.'",
                    f"'Defeat them all, and you'll have the power to build any AI from scratch!'"
                ]
            },
            
            "foundation_complete": {
                "title": "Foundation Mastered",
                "text": [
                    f"'{self.protagonist_name}, you've grasped the fundamentals!'",
                    f"'Neurons, weights, bias, activation - the building blocks are yours.'",
                    f"'But knowledge without application is like a sword without a wielder.'",
                    f"'Now we must learn to forge these pieces into true neural networks!'"
                ]
            },
            
            "building_complete": {
                "title": "The Builder's Path",
                "text": [
                    f"'Incredible! You can now build and train neural networks from scratch!'",
                    f"'Forward pass, backpropagation - the ancient arts flow through you.'",
                    f"'But the real world awaits. Data is messy, chaotic, unforgiving.'",
                    f"'Are you ready to face the challenges of practical AI?'"
                ]
            },
            
            "training_complete": {
                "title": "Battle-Tested Warrior",
                "text": [
                    f"'You've survived the data wars, {self.protagonist_name}!'",
                    f"'Overfitting, noise, validation - nothing can stop you now.'",
                    f"'But greater challenges await in the advanced realms.'",
                    f"'Specialized architectures that bend reality itself!'"
                ]
            },
            
            "advanced_complete": {
                "title": "Master of Architectures",
                "text": [
                    f"'RNNs, CNNs, LSTMs, GRUs - you command them all!'",
                    f"'Time, space, memory - all bow to your neural mastery.'",
                    f"'But the ultimate test approaches...'",
                    f"'The Transformer realm, where attention is everything!'"
                ]
            },
            
            "transformer_complete": {
                "title": "The Attention Master",
                "text": [
                    f"'The power of attention flows through you!'",
                    f"'Word embeddings, multi-head attention, transformers - all mastered!'",
                    f"'Now face the final challenge...'",
                    f"'The GPT Overlord awaits in the Citadel of Generation!'"
                ]
            },
            
            "final_victory": {
                "title": "Neural Network Grandmaster",
                "text": [
                    f"'You did it, {self.protagonist_name}! The GPT Overlord is defeated!'",
                    f"'You now possess the ultimate knowledge - the ability to create any AI!'",
                    f"'From simple perceptrons to mighty language models.'",
                    f"'The digital realm is restored, and you are its guardian!'",
                    f"'Go forth and build the future with your neural network mastery!'"
                ]
            }
        }
    
    def get_level_intro(self, level_name, boss_name):
        """Get dramatic intro for each level"""
        intros = {
            "Neuron Academy": [
                f"'{self.protagonist_name}, behold the Neuron Academy!'",
                f"'Here, the Weight Master hoards the secrets of neural connections.'",
                f"'Defeat him to learn how neurons process information!'",
                f"'Remember: Every neuron is a simple function - inputs × weights = output!'"
            ],
            
            "Bias Battlefield": [
                f"'The Bias Baron controls the threshold of decision!'",
                f"'Without bias, neurons cannot shift their boundaries.'",
                f"'Show him you understand how bias shapes neural behavior!'",
                f"'Bias is the key that unlocks non-zero thresholds!'"
            ],
            
            "Activation Peaks": [
                f"'The Sigmoid Sorcerer guards the peaks of non-linearity!'",
                f"'Linear functions are weak - activation brings true power!'",
                f"'Master ReLU, Sigmoid, Tanh - each has its purpose!'",
                f"'Without activation functions, neural networks are just linear algebra!'"
            ],
            
            "Chain Rule Caverns": [
                f"'Deep in these caverns lurks the Derivative Dragon!'",
                f"'The chain rule is the heart of backpropagation!'",
                f"'Learn to chain derivatives together like a master!'",
                f"'∂Loss/∂weight = ∂Loss/∂output × ∂output/∂weight - remember this!'"
            ],
            
            "GPT Citadel": [
                f"'This is it, {self.protagonist_name}. The final battle!'",
                f"'The GPT Overlord commands billions of parameters!'",
                f"'But you have something he lacks - true understanding!'",
                f"'Show him that knowledge beats raw computational power!'"
            ]
        }
        
        return intros.get(level_name, [
            f"'Another challenge awaits, {self.protagonist_name}!'",
            f"'The {boss_name} guards the secrets of {level_name}!'",
            f"'Prove your worth and claim the knowledge within!'"
        ])
    
    def get_victory_message(self, level_name, boss_name):
        """Get victory message after beating a boss"""
        return [
            f"'Well done, {self.protagonist_name}!'",
            f"'The {boss_name} has been defeated!'",
            f"'You have mastered the secrets of {level_name}!'",
            f"'Your neural network powers grow stronger!'"
        ]
    
    def get_hint_system(self, level_name):
        """Reinforcement learning hints for each level"""
        hints = {
            "Neuron Academy": [
                "💡 A neuron is just: output = sum(input × weight) + bias",
                "💡 Think of weights as importance - higher weight = more important input",
                "💡 Try different weight values and see how output changes!",
                "💡 Neurons are the building blocks - master this and you master AI!"
            ],
            
            "Bias Battlefield": [
                "💡 Bias shifts the activation threshold - like adjusting sensitivity",
                "💡 Without bias, your neuron can only activate when inputs sum to 0",
                "💡 Positive bias makes activation easier, negative makes it harder",
                "💡 Bias is learned just like weights during training!"
            ],
            
            "Activation Peaks": [
                "💡 Linear functions can't solve complex problems - you need curves!",
                "💡 ReLU: max(0, x) - simple but powerful for deep networks",
                "💡 Sigmoid: 1/(1+e^-x) - smooth curve, good for probabilities",
                "💡 Each activation function has strengths - choose wisely!"
            ]
        }
        
        return hints.get(level_name, ["💡 Think step by step!", "💡 Break the problem down!", "💡 You've got this!"])