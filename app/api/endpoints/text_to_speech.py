from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import io
from app.services.text_to_speech import TextToSpeechService

router = APIRouter()

class TextToSpeechRequest(BaseModel):
    text: str
    voice_id: str = "en"  # Default voice

class TextToSpeechEndpoint:
    def __init__(self):
        self.tts_service = TextToSpeechService()
        
    async def convert_text_to_speech(self, request: TextToSpeechRequest):
        """Convert text to speech audio"""
        if not request.text:
            raise HTTPException(status_code=400, detail="Text cannot be empty")
            
        # Generate speech
        result = await self.tts_service.synthesize(request.text, request.voice_id)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result.get("error", "Failed to synthesize speech"))
            
        # Return audio as streaming response
        audio_bytes = io.BytesIO(result["audio_data"])
        audio_bytes.seek(0)
        
        return StreamingResponse(
            audio_bytes, 
            media_type="audio/wav",
            headers={"Content-Disposition": "attachment; filename=speech.wav"}
        )

text_to_speech_endpoint = TextToSpeechEndpoint()

@router.post("/text-to-speech")
async def convert_text_to_speech(request: TextToSpeechRequest):
    return await text_to_speech_endpoint.convert_text_to_speech(request)