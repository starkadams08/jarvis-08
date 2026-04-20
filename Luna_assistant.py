from flask import Flask
import json
import pyttsx3
import speech_recognition as sr
from dotenv import load_dotenv 
import os 

app = Flask(__name__)

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(text):
    print(f"Luna: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='en-in')
        print(f"user said: {query}\n")
        return query.lower()
    except Exception:
        return "none"

MEMORY_FILE = "memory.json"

def load_memory():
    try:
     with open("memory.json", "r") as f:
        return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"tasks": [], "compeleted_tasks": []}
    
def save_memory(data):
    with open("memory.json", "w") as f:
        json.dump(data, f, indent=4)
        
# Use it in your chat logic:
memory = load_memory()

def add_task(task_text):
    data = load_memory()
    data["tasks"].append({
        "task": task_text,
        "done": False
    })
    save_memory(data)

def list_tasks():
    data = load_memory()
    tasks = data["tasks"]

    if not tasks:
        return "You have no tasks right now"
    
    response = "Here are your tasks:\n"
    for idx, task in enumerate(tasks, start=1):
        status = "✓" if task["done"] else "✗"
        response += f"{idx}. [{status}] {task['task']}\n"

    return response.strip()

def complete_task(index):
    data = load_memory()
    tasks = data["tasks"]

    if index < 1 or index > len(tasks):
        return "That task number doesn't exist in your list."
    
    tasks[index - 1]["done"] = True
    save_memory(data)
    return f"Task {index} marked as done."

def list_pending_tasks():
    data = load_memory()
    tasks = data["tasks"]
    pending = [task for task in tasks if not task["done"]]

    if not pending:
        return "You have no pending tasks"
    
    response = "Here are your pending tasks:\n"
    for idx, task in enumerate(pending, start=1):
        response += f"{idx}. {task['task']}\n"

    return response.strip()

def list_completed_tasks():
    data = load_memory()
    tasks = data["tasks"]
    completed = [task for task in tasks if task["done"]]

    if not completed:
        return "You have no completed tasks"
    
    response = "Here are your completed tasks:\n"
    for idx, task in enumerate(completed, start=1):
        response += f"{idx}. {task['task']}\n"

    return response.strip()

def get_reply(message):
    message = message.strip()

    # Add task
    if message.lower().startswith("add task:"):
        task = message[9:].strip()
        if task:
            add_task(task)
            reply = f"Task added successfully: {task}"
        else:
            reply = "Please tell me what task to add."
    
    # Show tasks 
    elif message.lower() == "show tasks":
        reply = list_tasks()

    elif message.lower() == "show pending":
        reply = list_pending_tasks()

    elif message.lower() == "show completed":
        reply = list_completed_tasks()

    # Complete task
    elif message.lower().startswith("done task:"):
        try:
            index = int(message.split(":")[1].strip())
            reply = complete_task(index)
        except (ValueError, IndexError):
            reply = "Please use: done task: number"

    # Friendly chat (with optional AI context)
    else:
        message = [
            {
                "role": "system",
                "content": "You are Rei Bear, a highly advanced, witty, and efficient AI assistant similar to JARVIS. Be concise, slightly formal but loyal, and always ready to assist with 'sir Gohan' or 'Ma'am Rukia' if appropriate. Focus on task management and technical precision."
            },
            {"role": "user", "content": message}
        ]
        msg = message.lower()

        if "hello" in msg or "hi" in msg:
            reply = "I'm listening. You can chat with me or manage your tasks."
        elif "how are you" in msg:
            reply = "I'm feeling calm and ready to help you"
        elif "thank" in msg:
            reply = "you're always welcome"
        elif "bye" in msg:
            reply = "Goodbye, I'll be right here when you reply."
        else:
            reply = "I'm listening. You can chat with me or manage your tasks."

    return reply

# ... your speak and listen functions ...

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
    speak("Systems online. How can I help you, Sir?")
    
    while True:
        command = listen()
        
        if "luna" in command:
            # Here you would call your chat logic
            response = "I am processing your request now."
            speak(response)
            
        elif "go to sleep" in command:
            speak("Powering down. Goodbye.")
            break
 