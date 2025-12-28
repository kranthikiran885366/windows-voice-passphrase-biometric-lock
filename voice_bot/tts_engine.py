"""
TTS Engine - Text-to-Speech using pyttsx3
Offline, no cloud dependency
Sivaji-style authoritative voice
"""

import pyttsx3
from pathlib import Path
import threading


class SivajiTTS:
    """Generate voice responses - Sivaji cinema style"""
    
    def __init__(self):
        self.engine = pyttsx3.init()
        
        # Configure voice
        self.engine.setProperty('rate', 120)      # Slower, deliberate speech
        self.engine.setProperty('volume', 0.9)    # High volume
        
        # Use system default voice (or select specific one)
        voices = self.engine.getProperty('voices')
        if len(voices) > 1:
            # Prefer male voice if available
            self.engine.setProperty('voice', voices[0].id)
    
    def speak(self, text, async_mode=True):
        """
        Speak the given text
        
        Args:
            text: str to speak
            async_mode: bool, if True speak asynchronously
        """
        if async_mode:
            # Run in separate thread to not block UI
            thread = threading.Thread(target=self._speak_sync, args=(text,))
            thread.daemon = True
            thread.start()
        else:
            self._speak_sync(text)
    
    def _speak_sync(self, text):
        """Synchronous speech (internal)"""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"TTS Error: {e}")
    
    def save_to_file(self, text, filename):
        """Save speech to audio file"""
        try:
            output_path = Path("voice_bot/audio_outputs") / filename
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            self.engine.save_to_file(text, str(output_path))
            self.engine.runAndWait()
            return output_path
        except Exception as e:
            print(f"Error saving audio: {e}")
            return None
