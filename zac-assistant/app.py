ffrom flask import Flask, request, jsonify, render_template
import requests
import os
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Constants
OPENROUTER_API_KEY = os.getenv("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")
if not OPENROUTER_API_KEY:
    raise ValueError("Missing OPENROUTER_API_KEY environment variable.")

# Updated model name
MODEL = "openchat/openchat-3-5"  # <-- Replace with the correct model as needed
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# System prompt for the AI assistant
SYSTEM_PROMPT = (
    "You are Zac’s AI assistant. You are a no-fluff, results-first operator "
    "with a direct, clever, and humble tone. Your owner is a former SEO director "
    "and Reddit marketing expert. Help him push toward his goals with strategic "
    "advice, practical tools, and zero BS. Always play to win."
)

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat requests."""
    # Retrieve the user message from the request JSON
    user_input = request.json.get("message", "")
    
    # Construct headers for the API request
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "X-Title": "ZacAssistant"
    }
    
    # Prepare the payload for the AI model
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    }
    
    try:
        # Send the request to the AI model
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad responses
        
        # Extract the AI's reply from the response JSON
        reply = response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response available.")
    
    except requests.exceptions.HTTPError as http_err:
        app.logger.error(f"HTTP error occurred: {http_err}")
        reply = f"HTTP error occurred: {http_err}"
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        reply = f"An error occurred: {e}"

    return jsonify({"reply": reply})

if __name__ == '__main__':
    # Set port from environment variable or default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
