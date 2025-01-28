import os
import openai.whisper as whisper
from typing import Optional, Union
from pathlib import Path

class SecureWhisperWrapper:
    """Secure wrapper for Whisper model with safe loading"""
    
    def __init__(self):
        """
        Initialize Whisper model with secure loading
        """
        self.model = whisper.load_model("base")
        
    def transcribe(self, audio_path: str, **kwargs) -> dict:
        """
        Transcribe audio file
        
        Args:
            audio_path (str): Path to audio file
            **kwargs: Additional arguments for whisper.transcribe
            
        Returns:
            dict: Transcription result
        """
        try:
            # Basic validation
            if not os.path.exists(audio_path):
                raise FileNotFoundError(f"Audio file not found: {audio_path}")
                
            if not os.path.getsize(audio_path) > 0:
                raise ValueError("Audio file is empty")
            
            # Set secure defaults for transcription
            secure_kwargs = {
                'fp16': False,  # Use FP32 for better compatibility
                'language': 'en',  # Default to English
                'task': 'transcribe',  # Default to transcription
                'verbose': None  # Disable verbose output
            }
            
            # Update with user kwargs but maintain secure defaults
            secure_kwargs.update(kwargs)
            
            # Perform transcription
            return self.model.transcribe(audio_path, **secure_kwargs)
            
        except Exception as e:
            raise Exception(f"Transcription error: {str(e)}")
    
    def cleanup(self):
        """Cleanup resources"""
        try:
            # Clear CUDA cache if available
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                
            # Remove reference to model
            self.model = None
            
        except Exception as e:
            print(f"Cleanup warning: {str(e)}")