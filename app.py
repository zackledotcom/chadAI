from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    api_key = os.environ.get("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")

    if not api_key:
        return jsonify({"reply": "Server error: missing API key."}), 500

    headers = {
        "Authorization": f"Bearer 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",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openrouter/mistral-7b",
        "messages": [
            {"role": "user", "content": user_message}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    
    if response.status_code == 200:
        reply = response.json()["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})
    else:
        return jsonify({"reply": "Error: Something went wrong talking to OpenRouter."}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(debug=False, host="0.0.0.0", port=port)
