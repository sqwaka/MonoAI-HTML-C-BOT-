import openai
from flask import Flask, request, jsonify

# Set up your OpenAI API key
openai.api_key = "###"

# Create a Flask app and set up the message database
app = Flask(__name__)
messages = []

# Define a function to generate a response using OpenAI GPT-3
def generate_response(message):
    prompt = "User: {}\nAI:".format(message)
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

# Define the Flask routes for the chatbot
@app.route('/')
def home():
    return '''
<html>
    <head>
            <title>MonoAI</title>
            <!-- Скрипт на обработку сообщений и получение через бота -->
        <script>
                            function sendMessage() {
                                var message = document.getElementById('message').value;
                                fetch('/send', {
                                    method: 'POST',
                                    body: JSON.stringify({message: message}),
                                    headers: {
                                        'Content-Type': 'application/json'
                                    }
                                }).then(response => response.json())
                                .then(data => {
                                    document.getElementById('message').value = '';
                                    var chatWindow = document.getElementById('chat-window');
                                    chatWindow.innerHTML += '<p>Я: ' + message + '</p>';
                                    chatWindow.innerHTML += '<p>ИИ: ' + data.response + '</p>';
                                });
                            }
        </script>
        <style>

            @import url('https://fonts.googleapis.com/css2?family=Raleway:wght@400;700&display=swap');

            *{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            h1 {
                color: azure;
                margin-bottom: 32px;
            }
            p {
                color: azure;
            }
            body{
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background: #050801;
                font-family: 'Raleway', sans-serif;
            }

            button{
            padding: 25px 30px;
            background-color: #050801;
            color: #03e9f4;
            font-weight: bold;
            border: none;
            border-radius: 5px;
            letter-spacing: 4px;
            overflow: hidden;
            transition: 0.5s;
            cursor: pointer;
            }

            button:hover{
                background: #03e9f4;
                color: #050801;
            }

        </style>
    </head>
        <body>
            <div class="block">
                <h1>Чат-бот</h1>
                <div id="chat-window"></div>
                <input type="text" id="message">
                <button onclick="sendMessage()">Отправить</button>
            </div>
        </body>
</html>
    '''

@app.route('/send', methods=['POST'])
def send():
    data = request.get_json()
    message = data['message']
    messages.append(message)
    # Generate a response using OpenAI GPT-3
    response = generate_response(message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run()
