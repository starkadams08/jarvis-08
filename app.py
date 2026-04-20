from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
from openai import OpenAI
from Luna_assistant import speak # Import the voice function you wrote

load_dotenv()
app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    # 1. AI Brain (fixed the 'mini' typo here)
    response = client.chat.completions.create(
        model="gpt-40-mini",
        messages=[{"role": "system", "content": "You are Rei Bear, a sophisticated AI like JARVIS. Be witty, loyal, and concise."},
                  {"role": "user", "content": user_message}
                  ]
    )

    ai_reply = response.choices[0].message.content
    
    # 2. Voice Output (This makes her talk when the web app replies)
    speak(ai_reply)
    
    return jsonify({"reply": ai_reply})

if __name__ == "__main__":
      app.run(debug=True)
    
