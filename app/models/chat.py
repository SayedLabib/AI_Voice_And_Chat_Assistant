from pydantic import BaseModel

class Chat(BaseModel):
    user_input: str
    bot_response: str