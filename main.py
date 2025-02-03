import json
import time
import os
import openai
from src.speech_to_text.recorder import AudioRecorder
from src.speech_to_text.transcriber import Transcriber
from src.nlp_processing.intent_classifier import IntentClassifier
from src.response_gen.response_generator import ResponseGenerator
from src.text_to_speech.tts_generator import TTSGenerator
from src.database.db_manager import DatabaseManager
import logging

logging.basicConfig(level=logging.INFO, filename='app.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s')

class VoiceBot:
    def __init__(self):
        print("Initializing Voice Bot...")
        self.recorder = AudioRecorder()
        self.transcriber = Transcriber()
        self.intent_classifier = IntentClassifier()
        self.response_generator = ResponseGenerator()
        self.tts_generator = TTSGenerator()
        self.db = DatabaseManager()
        self.user_id = None
        self.username= None
        # In main.py, update the commands dictionary in __init__
        # In main.py, update the commands dictionary in __init__
        self.commands = {
            'change user': self.change_user,
            'this is':self.find_current_user,
            'balance': self.check_balance,
            'transaction': self.check_transactions,
            'help': self.show_help,
            'deposit': self.make_deposit,
            'withdraw': self.make_withdrawal,
            'create': self.create_new_user,
            'transfer': self.transfer_money,
            'send': self.transfer_money  # Alias for transfer
        }



    def create_new_user(self, text):
        """Handle user creation command"""
        try:
            # Extract username from command
            import re
            match = re.search(r'create (?:user|account)(?: for)? ([a-zA-Z]+)', text.lower())
            if match:
                username = match.group(1)
                user_id = self.db.create_user(username)
                if user_id:
                    return f"Successfully created account for {username}"
                else:
                    return f"Failed to create account for {username}"
            return "Please specify a valid username"
        except Exception as e:
            return f"Error creating user: {str(e)}"



    
    def transfer_money(self, text):
        """Handle money transfer command using OpenAI extraction"""
        if self.user_id is None:
            return (f"Please tell the name of user like 'This is user name' ")
        try:
            # Define the prompt to extract amount and username
            prompt = f"Extract the amount and recipient username from this text: '{text}'. Return a valid JSON in this format: {{\"username\": \"<recipient>\", \"amount\": <amount>}}. make sure nothing extra is sent in response apart from json "
            
            logging.info("Extracting data using OpenAI...")

            # Call OpenAI API (Updated for latest version)
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ]
            )

            logging.info(f"API Response: {response}")

            # Extract response content
            extracted_text = response.choices[0].message.content.strip()
            logging.info(f"extracted_text {extracted_text}")
            # Convert extracted response to JSON
            extracted_data = json.loads(extracted_text)
            logging.info(f"username {extracted_text}")
            logging.info(f"amount {extracted_data}")
            # Get extracted username and amount
            to_username = extracted_data.get("username", "").strip().lower()
            amount = float(extracted_data.get("amount", 0))
            from_username=self.username
            # Validate extracted data
            if to_username and amount > 0:
                return self.db.transfer_money(from_username, to_username.lower(), amount)

            return "Invalid input. Please specify both amount and recipient."

        except json.JSONDecodeError:
            return "Error extracting data. Ensure the input is correctly formatted."
        except Exception as e:
            return f"Error processing transfer: {str(e)}"

    
    def check_balance(self, text):
        if self.user_id is None:
            return (f"Please tell the name of user like 'This is user name' ")
        logging.info(f"this is the text {text}")
        balance = self.db.get_balance(self.user_id)
        return f"Your current balance is ${balance:.2f}"

    def check_transactions(self, text):
        if self.user_id is None:
            return (f"Please tell the name of user like 'This is user name' ")
        transactions = self.db.get_transactions(self.user_id, limit=5)
        if not transactions:
            return "You have no recent transactions."
        
        response = "Here are your recent transactions:\n"
        for trans in transactions:
            response += f"- {trans[0]}: ${trans[1]:.2f} on {trans[2]}\n"
        return response

    def make_deposit(self, text):
        if self.user_id is None:
            return (f"Please tell the name of user like 'This is user name' ")
        try:
            # Try to extract amount from text
            import re
            amounts = re.findall(r'\$?(\d+(?:\.\d{2})?)', text)
            if amounts:
                amount = float(amounts[0])
                if self.db.add_transaction(self.user_id, 'deposit', amount):
                    return f"Successfully deposited ${amount:.2f}"
            return "Please specify the amount to deposit."
        except Exception as e:
            return "Error processing deposit. Please try again."

    def make_withdrawal(self, text):
        if self.user_id is None:
            return (f"Please tell the name of user like 'This is user name' ")
        try:
            import re
            amounts = re.findall(r'\$?(\d+(?:\.\d{2})?)', text)
            if amounts:
                amount = float(amounts[0])
                if self.db.add_transaction(self.user_id, 'withdrawal', amount):
                    return f"Successfully withdrew ${amount:.2f}"
            return "Please specify the amount to withdraw."
        except Exception as e:
            return "Error processing withdrawal. Please try again."

    def change_user(self, text):
        try:
            # OpenAI GPT model to identify the username
                
            prompt = f"Extract the changed username from this text :'{text}' i just need username make sure not to give anything else except that just give one word and that should be username"
            logging.info("im here ")
            # Call OpenAI API to generate a response (updated for new API interface)
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",  # Use an appropriate model
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
            )
            logging.info(f"response {response}")
            
            # Parse the response
            extracted_username = response.choices[0].message.content.strip().lower()
            logging.info(f"username {extracted_username}")
            # If we found a valid username, retrieve user details
            if extracted_username:
                user_details = self.db.get_user_by_username(extracted_username)
                if user_details:
                    self.user_id=user_details['user_id']
                    self.username=extracted_username
                    return f"Current user: {extracted_username} (ID: {user_details['user_id']})"
                else:
                    return "User not found."
            return "No valid username detected in the input."
        
        except Exception as e:
            return f"Error processing the current user. Details: {str(e)}"

    def find_current_user(self, text):
        try:
            # OpenAI GPT model to identify the username
                
            prompt = f"Extract the username from this text :'{text}' i just need username make sure not to give anything else except that just give one word and that should be username"
            logging.info("im here ")
            # Call OpenAI API to generate a response (updated for new API interface)
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",  # Use an appropriate model
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
            )
            logging.info(f"response {response}")
            
            # Parse the response
            extracted_username = response.choices[0].message.content.strip().lower()
            logging.info(f"username {extracted_username}")
            # If we found a valid username, retrieve user details
            if extracted_username:
                user_details = self.db.get_user_by_username(extracted_username)
                if user_details:
                    self.user_id=user_details['user_id']
                    self.username=extracted_username
                    return f"Current user: {extracted_username} (ID: {user_details['user_id']})"
                else:
                    return "User not found."
            return "No valid username detected in the input."
        
        except Exception as e:
            return f"Error processing the current user. Details: {str(e)}"

    def show_help(self, text):
        return """
    Available commands:
    - Check balance: "What's my balance?"
    - Recent transactions: "Show my transactions"
    - Make deposit: "Deposit $100"
    - Make withdrawal: "Withdraw $50"
    - Create user: "Create user John"
    - Transfer money: "Transfer $100 to John" or "Send $100 to John"
    - Help: "Show help"
        """



    def process_user_input(self):
        try:
            # 1. Record audio
            print("\nListening... (Speaking for 5 seconds)")
            self.recorder.start_recording()
            time.sleep(5)
            self.recorder.stop_recording()
            
            # Save audio to file
            audio_file = f"temp_recording_{int(time.time())}.wav"
            self.recorder.save_audio(audio_file)
            
            # 2. Convert speech to text
            text = self.transcriber.transcribe_audio(audio_file)
            if not text:
                return "I couldn't understand the audio. Please try again."
            print(f"You said: {text}")
            
            # 3. Classify intent and handle commands
            intent_data = self.intent_classifier.classify_intent(text)
            intent = intent_data['intent']
            confidence = intent_data['confidence']
            print(f"Detected intent: {intent} (confidence: {confidence:.2f})")
            
            # 4. Generate response based on intent
            response = None
            text_lower = text.lower()
            
            # Check for specific commands
            for cmd, handler in self.commands.items():
                if cmd in text_lower:
                    response = handler(text)
                    break
            
            # If no command matched, use general response generator
            if not response:
                response = self.response_generator.generate_response(text, intent, confidence)
            
            print(f"Bot response: {response}")
            
            # 5. Log conversation
            self.db.log_conversation(
                self.user_id,
                text,
                response,
                intent,
                confidence
            )
            
            # 6. Convert response to speech
            self.tts_generator.speak_text(response)
            
            # 7. Cleanup temporary audio file
            if os.path.exists(audio_file):
                os.remove(audio_file)
            
            return response
            
        except Exception as e:
            print(f"Error in processing: {str(e)}")
            return "I encountered an error. Please try again."

    def run(self):
        print("\nVoice Bot is ready! Press Ctrl+C to exit.")
        print("Type 'help' or say 'show help' for available commands.")
        try:
            while True:
                input("\nPress Enter to start speaking...")
                response = self.process_user_input()
                
        except KeyboardInterrupt:
            print("\nShutting down Voice Bot...")
        finally:
            self.cleanup()

    def cleanup(self):
        """Cleanup resources"""
        self.db.close()
        # Clean up any remaining temporary files
        for file in os.listdir():
            if file.startswith("temp_recording_") and file.endswith(".wav"):
                try:
                    os.remove(file)
                except:
                    pass


def main():
    print("=== Banking Voice Bot ===")
    bot = VoiceBot()
    bot.run()

if __name__ == "__main__":
    main()
