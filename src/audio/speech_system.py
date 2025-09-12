"""
Speech synthesis system for narration and dialogue
"""

import threading
import queue
import time
try:
    import pyttsx3
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False
    print("⚠️  pyttsx3 not available - speech disabled")

class SpeechSystem:
    def __init__(self):
        self.enabled = SPEECH_AVAILABLE
        self.engine = None
        self.speech_queue = queue.Queue()
        self.is_speaking = False
        self.speech_thread = None
        
        if self.enabled:
            try:
                self.engine = pyttsx3.init()
                # Configure voice settings
                voices = self.engine.getProperty('voices')
                if voices:
                    # Try to find a good voice (prefer female for Tensor)
                    for voice in voices:
                        if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                            self.engine.setProperty('voice', voice.id)
                            break
                
                # Set speech rate and volume
                self.engine.setProperty('rate', 180)  # Slightly faster than default
                self.engine.setProperty('volume', 0.8)
                
                # Start speech thread
                self.speech_thread = threading.Thread(target=self._speech_worker, daemon=True)
                self.speech_thread.start()
                
            except Exception as e:
                print(f"⚠️  Speech engine initialization failed: {e}")
                self.enabled = False
    
    def speak(self, text, character="narrator", priority=False):
        """Add text to speech queue"""
        if not self.enabled or not text.strip():
            return
        
        # Clean text for speech
        clean_text = self._clean_text_for_speech(text, character)
        
        if priority:
            # Clear queue and speak immediately
            with self.speech_queue.mutex:
                self.speech_queue.queue.clear()
        
        self.speech_queue.put((clean_text, character))
    
    def _clean_text_for_speech(self, text, character):
        """Clean text for better speech synthesis"""
        # Remove special characters that don't speak well
        text = text.replace("'", "'")
        text = text.replace(""", '"')
        text = text.replace(""", '"')
        text = text.replace("—", " - ")
        text = text.replace("…", "...")
        
        # Add character-specific modifications
        if character == "tensor":
            # Tensor speaks more formally
            text = text.replace("you're", "you are")
            text = text.replace("we're", "we are")
            text = text.replace("it's", "it is")
        elif character == "alex":
            # Alex speaks more casually - keep contractions
            pass
        
        # Add pauses for better pacing
        text = text.replace("!", "! ")
        text = text.replace(".", ". ")
        text = text.replace("?", "? ")
        
        return text.strip()
    
    def _speech_worker(self):
        """Background thread for speech synthesis"""
        while True:
            try:
                text, character = self.speech_queue.get(timeout=1)
                if text:
                    self.is_speaking = True
                    self.engine.say(text)
                    self.engine.runAndWait()
                    self.is_speaking = False
                    time.sleep(0.2)  # Brief pause between speeches
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Speech error: {e}")
                self.is_speaking = False
    
    def is_currently_speaking(self):
        """Check if speech is currently active"""
        return self.is_speaking
    
    def stop_speech(self):
        """Stop current speech and clear queue"""
        if not self.enabled:
            return
        
        try:
            self.engine.stop()
            with self.speech_queue.mutex:
                self.speech_queue.queue.clear()
            self.is_speaking = False
        except:
            pass
    
    def set_enabled(self, enabled):
        """Enable or disable speech"""
        if enabled and not SPEECH_AVAILABLE:
            return False
        
        self.enabled = enabled
        if not enabled:
            self.stop_speech()
        
        return self.enabled

# Global speech system instance
speech_system = SpeechSystem()