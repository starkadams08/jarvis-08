from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import os
from openai import OpenAI
import Luna_assistant # Import your assistant logic file
from Luna_assistant import speak # Import the voice function you wrote

load_dotenv()
app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("message")
    # This calls your assistant logic 
    response_text = Luna_assistant.generate_response(user_input)
    
    # We send the text back to the browser
    return jsonify({"status": "success", "response": response_text})
    
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
    
