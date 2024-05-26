from flask import Blueprint, request, jsonify
from app.models import User, Score
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


@main.route('/users', methods=['GET'])
@auth.login_required
def get_users():
    users = User.get_all_users()
    request_identifier = str(uuid.uuid4())
    return jsonify({
        "request-identifier": request_identifier,
        "message": None,
        "data": users
    }), 200


@main.route('/users/score', methods=['POST'])
@auth.login_required
def upsert_score():
    data = request.json
    if not data or not all(k in data for k in ("user_id", "score")):
        return jsonify({"error": "Invalid data"}), 400

    score = Score.upsert_score(data["user_id"], data["score"])
    request_identifier = str(uuid.uuid4())
    return jsonify({
        "request-identifier" : request_identifier,
        "message" : None,
        "data" : score
    }), 200