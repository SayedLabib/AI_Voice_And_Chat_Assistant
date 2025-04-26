import os
from dotenv import load_dotenv
import httpx
import logging
import json
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class AIService:
    def __init__(self):
        # Groq API settings - only use Groq
        self.use_groq = True
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.groq_model = os.getenv("GROQ_MODEL", "deepseek-r1-distill-llama-70b")
        
        # Remove all other model options and fallbacks
        self.use_openrouter = False
        self.use_mock = False
        self.last_model_used = self.groq_model
        self.rate_limited = False
        
        # Log configuration
        logger.info(f"Initialized AIService with Groq model: {self.groq_model}")
        if not self.groq_api_key:
            logger.warning("GROQ_API_KEY environment variable is not set")
    
    async def _call_groq_api(self, user_input, system_prompt):
        """Call the Groq API with deepseek-r1-distill-llama-70b model"""
        try:
            # Groq API endpoint
            url = "https://api.groq.com/openai/v1/chat/completions"
            
            # Request headers for Groq API
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.groq_api_key}"
            }
            
            # Request body for Groq API
            data = {
                "model": self.groq_model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                "max_tokens": 800,
                "temperature": 0.7,
                "top_p": 0.9
            }
            
            logger.info(f"Sending request to Groq API with model: {self.groq_model}")
            
            # Make API call
            start_time = datetime.now()
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, json=data, headers=headers)
                
                elapsed = (datetime.now() - start_time).total_seconds()
                logger.info(f"Groq API response received in {elapsed:.2f}s with status code: {response.status_code}")
                
                if response.status_code == 200:
                    response_data = response.json()
                    
                    # Extract the message content safely
                    try:
                        ai_response = response_data["choices"][0]["message"]["content"]
                        return {"success": True, "response": ai_response}
                    except (KeyError, IndexError) as e:
                        logger.error(f"Error extracting message from Groq response: {e}")
                        return {"success": False, "error": f"Error extracting message from Groq response: {e}"}
                else:
                    error_message = f"Groq API error: {response.status_code}, {response.text}"
                    logger.error(error_message)
                    return {"success": False, "error": error_message}
                    
        except Exception as e:
            logger.error(f"Error calling Groq API: {e}")
            return {"success": False, "error": f"Error calling Groq API: {e}"}
    
    async def generate_response(self, user_input):
        """Generate a response using Groq API only"""
        # Customer support system prompt optimized for the DeepSeek Llama 70B model
        system_prompt = """
        You are an AI customer support assistant for a technology company. Your role is to provide helpful, clear, and accurate responses to customer inquiries.
        
        Follow these guidelines:
        - Be friendly and professional in your responses
        - Provide clear and concise information
        - If you don't know the answer, say so honestly
        - Offer step-by-step troubleshooting when appropriate
        - Personalize your responses based on the customer's question
        - Focus on solutions rather than explanations
        - Use simple language and avoid technical jargon when possible
        - DO NOT include your thinking process or use <think> tags in your response
        - DO NOT explain your reasoning or include internal thoughts
        - Just provide direct, helpful responses to the user's queries
        
        Remember to be patient and understanding with customer concerns.
        """
        
        # Use Groq API exclusively
        if self.groq_api_key:
            self.last_model_used = self.groq_model
            result = await self._call_groq_api(user_input, system_prompt)
            
            # If successful, also clean any potential thinking tags from the response
            if result["success"] and "<think>" in result["response"]:
                result["response"] = self._clean_thinking_content(result["response"])
                
            return result
        else:
            error_message = "Groq API key not configured"
            logger.error(error_message)
            return {"success": False, "error": error_message}
            
    def _clean_thinking_content(self, text):
        """Remove content between <think> tags"""
        import re
        cleaned_text = re.sub(r'<think>[\s\S]*?<\/think>', '', text).strip()
        return cleaned_text