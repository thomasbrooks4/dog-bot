from message_router import message_response
from flask import Flask, request, redirect

app = Flask(__name__)

@app.route('/sms', methods=['POST'])
def sms_response():
    number = request.form['From']
    body = request.form['Body']

    response = message_response(body)

    return str(response)

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)
