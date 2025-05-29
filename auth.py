from flask import Blueprint, request, session, jsonify

auth_blueprint = Blueprint('auth', __name__, url_prefix='/auth')

USER_CREDENTIALS = {
    "admin": {"password": "admin123", "role": "admin"},
    "viewer": {"password": "viewer123", "role": "viewer"}
}


@auth_blueprint.route('/login', methods=['POST'])
def api_login():
    data = request.json
    user = USER_CREDENTIALS.get(data['username'])

    if user and user['password'] == data['password']:
        session['user'] = {"username": data['username'], "role": user['role']}
        return jsonify({"message": "Login successful", "role": user['role']})
    return jsonify({"message": "Invalid credentials"}), 401
