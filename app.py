import os
from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

@app.route('/')
def index():
    return render_template('chat.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json.get('message')
    response = query_groq(user_message)
    return jsonify({'response': response})

def query_groq(user_message):
    headers = {
        'Authorization': f'Bearer {GROQ_API_KEY}',
        'Content-Type': 'application/json',
    }
    
    data = {
        "model": "mixtral-8x7b-32768",  # Replace with your chosen model
        "messages": [{"role": "user", "content": user_message}]
    }
    
    response = requests.post(GROQ_API_ENDPOINT, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json().get('choices')[0]['message']['content']
    else:
        return "Error: " + response.text

if __name__ == "__main__":
    app.run(debug=True)
