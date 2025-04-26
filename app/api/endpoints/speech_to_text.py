from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.speech_recognition import SpeechRecognitionService

router = APIRouter()

class SpeechToTextEndpoint:
    def __init__(self):
        self.stt_service = SpeechRecognitionService()
        
    @router.post("/speech-to-text/")
    async def convert_speech_to_text(self, audio: UploadFile = File(...)):
        """Convert uploaded audio to text"""
        if not audio:
            raise HTTPException(status_code=400, detail="Audio file is required")
            
        # Read audio file
        audio_bytes = await audio.read()
        
        if not audio_bytes:
            raise HTTPException(status_code=400, detail="Audio file is empty")
            
        # Process audio with Whisper
        result = await self.stt_service.transcribe(audio_bytes)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result.get("error", "Failed to transcribe audio"))
            
        return {"text": result["text"], "language": result.get("language", "en")}