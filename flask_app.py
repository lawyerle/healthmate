from flask import Flask, render_template, jsonify, request
from main import chat_with_user, make_chain, init_api

app = Flask(__name__)

# 전역 변수로 chain 선언
chain = None

def prepare():
    global chain
    init_api()
    chain = make_chain()  # chain 객체를 전역 변수로 설정
    if chain is None:
        print("Error: Chain is not initialized properly.")

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/2', methods=['GET'])
def onboarding1():
    return render_template('2.html')

@app.route('/3', methods=['GET'])
def onboarding2():
    return render_template('3.html')

@app.route('/4', methods=['GET'])
def onboarding3():
    return render_template('4.html')

@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/chatui', methods=['GET'])
def chatui():
    value = ''
    if 'search' in request.args:
        value = request.args.get('search', type=str)
        print(value)
    if value:
        return render_template('chat.html', query_param=value)
    else:
        return render_template('chat.html')


@app.route('/chat/<question>', methods=['GET'])
def chat_massage(question):
    global chain
    if chain is None:
        return jsonify({'error': 'Chain is not initialized'}), 500
    try:
        message = chat_with_user(question)
        return jsonify({'message': message})
    except Exception as e:
        print(f"Error in chat_with_user: {e}")
        return jsonify({'error': 'Error processing message'}), 500

if __name__ == '__main__':
    prepare()
    # app.run(host='0.0.0.0', port=8000, debug=True)
    app.run(port=8000, debug=True)