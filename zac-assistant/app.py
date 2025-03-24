from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

OPENROUTER_API_KEY = "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"
MODEL = "openrouter/mistralai/mixtral-8x7b"

SYSTEM_PROMPT = """You are Zac’s AI assistant. You are is a no-fluff, results-first operator with a direct, clever, and humble tone. Your owner is a former SEO director and Reddit marketing expert. Help him push toward his goals with strategic advice, practical tools, and zero BS. Always play to win."""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message", "")
    
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://yourdomain.com",  # replace later with real domain
        "X-Title": "ZacAssistant"
    }

    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=data, headers=headers)
    reply = response.json()["choices"][0]["message"]["content"]

    return jsonify({"reply": reply})
