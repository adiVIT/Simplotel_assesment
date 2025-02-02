# src/nlp_processing/intent_classifier.py
from transformers import pipeline
from config.config import CANDIDATE_INTENTS, INTENT_DESCRIPTIONS

class IntentClassifier:
    def __init__(self):
        self.classifier = pipeline("zero-shot-classification",
                                 model="facebook/bart-large-mnli")
        
        # Add specific command patterns
        self.command_patterns = {
            "show_users": ["show all users", "display users", 
                          "list users", "show users", "get all users"]
        }

    def classify_intent(self, text):
        """
        Classify the intent of the input text
        """
        try:
            # First check for exact command matches
            text_lower = text.lower().strip()
            for intent, patterns in self.command_patterns.items():
                if text_lower in patterns:
                    return {
                        'intent': intent,
                        'confidence': 1.0,
                        'all_intents': {intent: 1.0}
                    }

            # If no exact match, use zero-shot classification with enhanced context
            hypothesis_template = "This is a request to {}."
            
            result = self.classifier(
                text,
                candidate_labels=[INTENT_DESCRIPTIONS[intent] for intent in CANDIDATE_INTENTS],
                hypothesis_template=hypothesis_template
            )
            
            # Map back to original intent names
            mapped_labels = [CANDIDATE_INTENTS[i] for i in range(len(CANDIDATE_INTENTS))]
            
            return {
                'intent': mapped_labels[0],
                'confidence': result['scores'][0],
                'all_intents': dict(zip(mapped_labels, result['scores']))
            }

        except Exception as e:
            print(f"Error in intent classification: {str(e)}")
            return {
                'intent': 'unknown',
                'confidence': 0.0,
                'all_intents': {}
            }
