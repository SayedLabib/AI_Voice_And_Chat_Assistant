class ChatService:
    def __init__(self, ai_service):
        self.ai_service = ai_service
        self.chat_sessions = {}

    def start_chat_session(self, user_id):
        self.chat_sessions[user_id] = []

    def process_chat(self, user_id, user_input):
        if user_id not in self.chat_sessions:
            self.start_chat_session(user_id)

        response = self.ai_service.get_response(user_input)
        self.chat_sessions[user_id].append({'user': user_input, 'bot': response})
        return response

    def get_chat_history(self, user_id):
        return self.chat_sessions.get(user_id, [])