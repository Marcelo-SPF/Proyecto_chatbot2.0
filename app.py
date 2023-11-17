from flask import Flask, render_template, request, jsonify
import json
from difflib import get_close_matches

app = Flask(__name__)

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> str|None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def check_banned_words(user_input: str, banned_words: list[str]) -> bool:
    for word in banned_words:
        if word in user_input:
            return True
    return False

def get_answer_for_question(question: str, knowledge_base: dict) -> str|None:
    for q in knowledge_base["question"]:
        if q["question"] == question:
            return q["answer"]

knowledge_base: dict = load_knowledge_base('knowledge_base.json')
banned_words = ["messi", "perro", "tonto", "odio", "amor", "negro"]
warning_count = 0
chat_disabled = False

@app.route('/')
def index():
    return render_template('index.html', chat_disabled=chat_disabled)

@app.route('/ask', methods=['POST'])
def ask():
    global knowledge_base
    global warning_count
    global chat_disabled

    user_input = request.json.get('user_input', '')
    response = {'response': '', 'chat_disabled': False}

    if user_input.lower() == 'quit':
        response['response'] = '¡Adiós!'
    elif check_banned_words(user_input, banned_words):
        warning_count += 1
        if warning_count < 4:
            response['response'] = f'¡Cuidado! Has usado una palabra advertida. Esto es tu {warning_count}ª advertencia.'
        else:
            response['response'] = 'Última advertencia. ¡Palabra baneada! Adiós.'
            chat_disabled = True
    else:
        best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["question"]])
        if best_match:
            response['response'] = get_answer_for_question(best_match, knowledge_base) or 'No sé la respuesta.'
        else:
            response['response'] = 'No sé la respuesta. ¿Puede enseñarme?'
            new_answer = request.json.get('new_answer', '').lower()
            if new_answer != 'skip':
                knowledge_base["question"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                response['response'] = '¡Gracias! ¡He aprendido algo nuevo!'

    return jsonify(response)

@app.route('/reset_chat', methods=['POST'])
def reset_chat():
    global warning_count
    global chat_disabled
    global banned_words
    global knowledge_base

    warning_count = 0
    chat_disabled = False
    banned_words = ["messi", "perro", "tonto", "odio", "amor", "negro"]
    knowledge_base = load_knowledge_base('knowledge_base.json')

    return jsonify({'reset_successful': True})

if __name__ == '__main__':
    app.run(debug=True)