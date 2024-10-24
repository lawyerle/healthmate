from flask import Flask, render_template, jsonify, request
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
    value = ''
    if 'search' in request.args:
        value = request.args.get('search', type=str)
        print(value)
    if value:
        return render_template('chat.html', query_param=value)
    else:
        return render_template('chat.html')

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

@app.route('/chat/<question>', methods=['GET'])
def chat_massage(question):
   message = chat_with_user(question)

   return jsonify({'message': message})

if __name__ == '__main__':
    prepare()
    app.run(port=8000, debug=True)