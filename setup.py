import requests

class ConvaiAI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.convai.com/v1/"
        self.contexts = {}

    def _request(self, endpoint, payload):
        """Internal method to handle requests to the Convai API."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(f"{self.base_url}{endpoint}", json=payload, headers=headers)
        response.raise_for_status()
        return response.json()

    # Dialogue Management
    def start_dialogue(self, user_id, initial_message):
        """Initialize a dialogue with a user by storing their context."""
        self.contexts[user_id] = initial_message
        return f"Dialogue started with user {user_id}."

    def continue_dialogue(self, user_id, message):
        """Continue an existing dialogue with context tracking."""
        if user_id not in self.contexts:
            return "Dialogue not started. Please start a dialogue first."
        
        payload = {
            "user_id": user_id,
            "message": message,
            "context": self.contexts[user_id]
        }
        response = self._request("generate-response", payload)
        self.contexts[user_id] = response.get("message")
        return response.get("message", "No response generated.")

    # Sentiment Analysis
    def analyze_sentiment(self, text):
        """Analyze the sentiment of the given text."""
        payload = {"text": text}
        response = self._request("analyze-sentiment", payload)
        return response.get("sentiment", "Sentiment analysis failed.")

    # Intent Recognition
    def recognize_intent(self, text):
        """Identify the intent behind the given text."""
        payload = {"text": text}
        response = self._request("detect-intent", payload)
        return response.get("intent", "Intent recognition failed.")

    # Response Generation
    def generate_response(self, user_id, message):
        """Generate a conversational response for the provided message."""
        payload = {
            "user_id": user_id,
            "message": message
        }
        response = self._request("generate-response", payload)
        return response.get("message", "Failed to generate response.")


# Example Usage
if __name__ == "__main__":
    api_key = "YOUR_CONVAI_API_KEY"  # Replace with your actual Convai API key
    convai = ConvaiAI(api_key)

    # Start a dialogue with a user
    user_id = "user123"
    print(convai.start_dialogue(user_id, "Hello! I'm excited to use Convai."))

    # Continue dialogue
    print(convai.continue_dialogue(user_id, "Can you tell me a joke?"))

    # Analyze sentiment
    sentiment = convai.analyze_sentiment("I love using this AI service!")
    print(f"Sentiment: {sentiment}")

    # Recognize intent
    intent = convai.recognize_intent("I want to book a flight to New York.")
    print(f"Intent: {intent}")

    # Generate response
    response = convai.generate_response(user_id, "What is the weather like?")
    print(f"Generated Response: {response}")
