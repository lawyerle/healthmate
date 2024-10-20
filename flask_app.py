from flask import Flask, render_template, jsonify
from main import chat_with_user, make_chain, init_api

app = Flask(__name__)

def prepare():
    init_api()
    make_chain()
    
# @app.route('/static/<path:filename>')
# def serve_static(filename):
#     return send_from_directory('static', filename)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/chatui', methods=['GET'])
def chatui():
    return render_template('chat.html')

@app.route('/onboarding', methods=['GET'])
def onboarding():
    return render_template('onboarding.html')

@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/chat/<question>', methods=['GET'])
def chat_massage(question):
   message = chat_with_user(question)

   return jsonify({'message': message})

if __name__ == '__main__':
    prepare()
    app.run(port=8000, debug=True)