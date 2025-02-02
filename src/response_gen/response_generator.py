from openai import OpenAI
from config.config import OPENAI_API_KEY, RESPONSE_TEMPLATES

class ResponseGenerator:
    def __init__(self):
        self.client = OpenAI()
        self.conversation_history = []

    def generate_response(self, user_input, intent, confidence):
        try:
            # If confidence is low, use template response
            if confidence < 0.7:
                return RESPONSE_TEMPLATES.get(intent, RESPONSE_TEMPLATES["unknown"])

            # Update conversation history
            self.conversation_history.append({"role": "user", "content": user_input})

            # Generate response using OpenAI
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self._get_system_message(intent)},
                    *self.conversation_history
                ],
                max_tokens=150,
                temperature=0.7
            )

            # Extract and store response
            bot_response = response.choices[0].message.content.strip()
            self.conversation_history.append({"role": "assistant", "content": bot_response})

            # Maintain conversation history length
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]

            return bot_response

        except Exception as e:
            print(f"Error generating response: {str(e)}")
            return RESPONSE_TEMPLATES.get(intent, RESPONSE_TEMPLATES["unknown"])

    # src/response_generator.py
    def _get_system_message(self, intent):
        """Returns appropriate system message based on intent"""
        system_messages = {
            "show_users": "You are a banking assistant. Show the list of all users in the system.",
            "greeting": "You are a friendly banking assistant. Keep responses brief and welcoming.",
            "balance_inquiry": "You are a banking assistant. Explain that you'll check their balance.",
            "transaction_history": "You are a banking assistant. Explain that you'll retrieve their transactions.",
            "help": "You are a helpful banking assistant. List available services clearly.",
            "goodbye": "You are a friendly banking assistant. Keep farewell messages brief and polite.",
            "unknown": "You are a helpful banking assistant. Ask for clarification politely."
        }
        return system_messages.get(intent, "You are a helpful banking assistant.")

    def reset_conversation(self):
        """Clears the conversation history"""
        self.conversation_history = []
