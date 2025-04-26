from typing import Any
import torch
import numpy as np
from io import BytesIO
from faster_whisper import WhisperModel

class SpeechRecognitionService:
    def __init__(self):
        # Initialize Whisper model (using faster-whisper for better performance)
        # Choose model size based on your hardware capabilities: tiny, base, small, medium, large-v2
        self.model = WhisperModel("small", device="cuda" if torch.cuda.is_available() else "cpu")
        
    async def transcribe(self, audio_bytes):
        """Convert speech to text using Whisper"""
        try:
            # Convert bytes to numpy array (assuming 16kHz mono PCM)
            audio_np = np.frombuffer(audio_bytes, dtype=np.float32)
            
            # Transcribe with Whisper
            segments, info = self.model.transcribe(audio_np, beam_size=5)
            
            # Combine all segments
            transcript = " ".join([segment.text for segment in segments])
            
            return {"success": True, "text": transcript, "language": info.language}
            
        except Exception as e:
            return {"success": False, "error": str(e)}