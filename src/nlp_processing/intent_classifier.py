# src/nlp_processing/intent_classifier.py
from transformers import pipeline
from config.config import CANDIDATE_INTENTS

class IntentClassifier:
    def __init__(self):
        # Initialize the zero-shot classification pipeline
        self.classifier = pipeline("zero-shot-classification",
                                 model="facebook/bart-large-mnli")

    def classify_intent(self, text):
        """
        Classify the intent of the input text
        """
        try:
            result = self.classifier(text, 
                                   candidate_labels=CANDIDATE_INTENTS,
                                   hypothesis_template="This is {}.")
            
            return {
                'intent': result['labels'][0],
                'confidence': result['scores'][0],
                'all_intents': dict(zip(result['labels'], result['scores']))
            }
        except Exception as e:
            print(f"Error in intent classification: {str(e)}")
            return {
                'intent': 'unknown',
                'confidence': 0.0,
                'all_intents': {}
            }
