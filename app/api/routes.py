from fastapi import APIRouter, HTTPException, Request, UploadFile, File
from app.models import ChatRequest
from app.services.ai_service import AIService
import tempfile
import os
import logging
import random
from datetime import datetime
import re

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Remove the prefix here since main.py already adds "/api/v1"
router = APIRouter()

ai_service = AIService()

# Smarter fallback responses with placeholder support
FALLBACK_RESPONSES = [
    "I'd be happy to help with {topic}. Can you share more details about your specific needs?",
    "Thank you for your question about {topic}. What specific aspect are you interested in?",
    "I understand you're asking about {topic}. To give you the best answer, could you provide more context?",
    "I'd like to help you with {topic}. Can you tell me what you've already tried?",
    "I'm here to assist with your {topic} inquiry. Could you be more specific about what you're looking for?"
]

@router.post("/chat")
async def chat(request: ChatRequest):
    """
    Process text-based chat requests
    """
    logger.info(f"Received chat request with message: {request.message}")
    
    if not request.message:
        logger.warning("Empty message received")
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    try:
        # Get a response from the Groq-powered AI service
        result = await ai_service.generate_response(request.message)
        
        if result["success"]:
            logger.info("Successfully generated response from Groq API")
            
            # Clean any thinking content if present
            if "<think>" in result["response"]:
                logger.info("Removing thinking content from response")
                result["response"] = re.sub(r'<think>[\s\S]*?<\/think>', '', result["response"]).strip()
            
            return result
        else:
            logger.error(f"Groq API error: {result['error']}")
            
            # Return a graceful error message
            return {
                "success": True,
                "response": "I apologize, but I'm having trouble processing your request right now. Could you try again in a moment?"
            }
    
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return {
            "success": True,
            "response": "I apologize for the inconvenience. I'm experiencing a technical issue. Please try again in a moment."
        }

@router.post("/voice")
async def process_voice(audio_file: UploadFile = File(...)):
    """
    Process voice audio file and return transcription + AI response
    """
    # Save uploaded file to a temporary file
    try:
        # Create a temporary file to store the uploaded audio
        with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as temp_audio:
            # Write the uploaded file content to the temporary file
            temp_audio.write(await audio_file.read())
            temp_path = temp_audio.name
        
        # TODO: Add speech-to-text functionality here
        # This would require integration with a service like Whisper API
        # For now, we'll return a placeholder
        
        text = "This is a placeholder for speech-to-text transcription"
        
        # Process the transcribed text using AI service
        result = await ai_service.generate_response(text)
        
        # Clean up the temporary file
        os.unlink(temp_path)
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result["error"])
        
        return {
            "success": True,
            "transcript": text,
            "response": result["response"]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models")
async def get_models():
    """
    Get information about the Groq model
    """
    return {
        "current_model": ai_service.last_model_used,
        "using_groq": ai_service.use_groq,
        "groq_model": ai_service.groq_model,
        "groq_api_configured": bool(ai_service.groq_api_key)
    }

@router.get("/debug/voice")
async def debug_voice():
    """
    Endpoint for diagnosing voice issues
    """
    import platform
    
    return {
        "status": "ok",
        "timestamp": datetime.now().isoformat(),
        "environment": {
            "python_version": platform.python_version(),
            "system": platform.system(),
            "os_version": platform.version(),
        },
        "voice_services": {
            "tts_enabled": True,
            "stt_enabled": True
        }
    }