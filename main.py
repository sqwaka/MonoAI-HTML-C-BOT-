import openai
from flask import Flask, request, jsonify

# Set up your OpenAI API key
openai.api_key = "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"

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
                <title>Chatbot</title>
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
                            chatWindow.innerHTML += '<p>You: ' + message + '</p>';
                            chatWindow.innerHTML += '<p>Bot: ' + data.response + '</p>';
                        });
                    }
                </script>
            </head>
            <body>
                <h1>Chatbot</h1>
                <div id="chat-window"></div>
                <input type="text" id="message">
                <button onclick="sendMessage()">Send</button>
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
