from flask import Blueprint, request, jsonify
from app.models import User
from app.auth import auth
import uuid

request_identifier = str(uuid.uuid4())
main = Blueprint('main', __name__)

@main.route('/users', methods=['POST'])
@auth.login_required
def add_user():
    data = request.json
    user = User.create_user()
    
    return jsonify({
        "request-identifier" : request_identifier,
        "message" : "User created successfully",
        "data" : user
    }), 201

@main.route('/users/<user_id>', methods=['DELETE'])
@auth.login_required
def delete_user(user_id):
    success = User.delete_user(user_id)
    if success:
        return jsonify({"request-identifier" : request_identifier, "message": "User deleted", "data": None}), 200
    else:
        return jsonify({"request-identifier" : request_identifier, "message": "User not found" , "data": None}), 404
