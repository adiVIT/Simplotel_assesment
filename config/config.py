# config/config.py
# Add these lines to existing config
import os
from dotenv import load_dotenv
load_dotenv()



# Database Configuration
DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'banking.db')

# Path for saving audio files
AUDIO_OUTPUT_DIR = "output/audio"



OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Response templates for different intents
RESPONSE_TEMPLATES = {
    "greeting": "Hello! How can I assist you today?",
    "balance_inquiry": "Let me check your balance for you.",
    "transaction_history": "I'll fetch your recent transactions.",
    "goodbye": "Goodbye! Have a great day!",
    "unknown": "I'm not sure I understand. Could you please rephrase that?",
    "help": "I can help you with checking your balance, viewing transactions, and more."
}
# config/config.py
CANDIDATE_INTENTS = [
    "greeting",
    "balance_inquiry",
    "transaction_history",
    "goodbye",
    "help"
]

INTENT_EXAMPLES = {
    "greeting": ["hello", "hi", "hey", "good morning", "good evening"],
    "balance_inquiry": ["what's my balance", "show balance", "account balance"],
    "transaction_history": ["show transactions", "recent transactions", "transaction history"],
    "goodbye": ["bye", "goodbye", "see you", "exit"],
    "help": ["help", "support", "assist", "what can you do"]
}
from google.cloud import texttospeech

# TTS Configuration
TTS_LANGUAGE_CODE = "en-US"
TTS_VOICE = {
    "name": "en-US-Standard-A",
    "language_code": "en-US",
    "ssml_gender": texttospeech.SsmlVoiceGender.FEMALE
}
TTS_AUDIO_CONFIG = {
    "audio_encoding": texttospeech.AudioEncoding.MP3,
    "speaking_rate": 1.0,
    "pitch": 0.0
}