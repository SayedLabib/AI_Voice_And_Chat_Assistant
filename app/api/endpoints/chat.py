from fastapi import HTTPException
from pydantic import BaseModel
from app.services.ai_service import AIService

class ChatRequest(BaseModel):
    message: str

class ChatEndpoint:
    def __init__(self):
        # Create AIService with no arguments - it will use defaults or env vars
        self.ai_service = AIService()
        
    async def process_chat(self, request: ChatRequest):
        """Process a chat message and return AI response"""
        if not request.message:
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        response = await self.ai_service.generate_response(request.message)
        
        if not response["success"]:
            raise HTTPException(status_code=500, detail=response.get("error", "Failed to generate response"))
            
        return {"response": response["response"]}