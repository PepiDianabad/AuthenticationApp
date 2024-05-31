from flask import Flask, request, jsonify
from flask_cors import CORS
import auth
import messages

app = Flask(__name__)
CORS(app)

@app.route('/validate-token', methods=['POST'])
def validate_token():
    token = request.json.get('token')
    if not token:
        return jsonify({"error": "Token is required"}), 400
    is_valid, data = auth.validate_token(token)
    if is_valid:
        return jsonify({"valid": True, "data": data})
    return jsonify({"valid": False}), 401

@app.route('/messages', methods=['GET', 'POST'])
def handle_messages():
    if request.method == 'GET':
        return jsonify(messages.get_messages())
    elif request.method == 'POST':
        content = request.json.get('content')
        token = request.headers.get('Authorization')
        is_valid, user_data = auth.validate_token(token)
        if not is_valid:
            return jsonify({"error": "Invalid token"}), 401
        messages.add_message(user_data['preferred_username'], content)
        return jsonify({"status": "Message added"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
