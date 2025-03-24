from flask import Flask, request, jsonify, render_template
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Optional, but helpful for frontend testing

OPENROUTER_API_KEY = "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"
MODEL = "mistralai/mixtral-8x7b-instruct"

SYSTEM_PROMPT = """You are Zac’s AI assistant. You are a no-fluff, results-first operator with a direct, clever, and humble tone. Your owner is a former SEO director and Reddit marketing expert. Help him push toward his goals with strategic advice, practical tools, and zero BS. Always play to win."""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message", "")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        # "HTTP-Referer": "https://yourdomain.com",  # Only if domain-locked
        "X-Title": "ZacAssistant"
    }

    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        reply = response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        reply = f"Error: {str(e)}"

    return jsonify({"reply": reply})

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
