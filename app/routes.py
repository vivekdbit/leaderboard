from flask import Blueprint, request, jsonify
from app.users_models import User
from app.scores_models import Score
from app.auth import auth
import uuid

request_identifier = str(uuid.uuid4())
main = Blueprint('main', __name__)

@main.route('/api/v1/users', methods=['POST'])
@auth.login_required
def add_user():
    try:
        user = User.create_user()
        return jsonify({
            "request-identifier": request_identifier,
            "message": "User created successfully",
            "data": user
        }), 201
    except Exception as e:
        # Log the error
        print(f"An error occurred while adding a user: {e}")
        # Return an error response
        return jsonify({
            "request-identifier": request_identifier,
            "message": "An error occurred while processing the request.",
            "data": None
        }), 500


@main.route('/api/v1/users/<user_id>', methods=['DELETE'])
@auth.login_required
def delete_user(user_id):
    try:
        success = User.delete_user(user_id)
        if success:
            return jsonify({"request-identifier" : request_identifier, "message": "User deleted", "data": None}), 200
        else:
            return jsonify({"request-identifier" : request_identifier, "message": "User not found" , "data": None}), 404
    except Exception as e:
        # Log the error
        print(f"An error occurred while delete a user: {e}")
        # Return an error response
        return jsonify({
            "request-identifier": request_identifier,
            "message": "An error occurred while processing the request.",
            "data": None
        }), 500


@main.route('/api/v1/users', methods=['GET'])
@auth.login_required
def get_users():
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))
        users = User.get_all_users(page, page_size)
        return jsonify({
            "request-identifier": request_identifier,
            "message": None,
            "data": users
        }), 200
    except Exception as e:
        # Log the error
        print(f"An error occurred while getting a user: {e}")
        # Return an error response
        return jsonify({
            "request-identifier": request_identifier,
            "message": "An error occurred while processing the request.",
            "data": None
        }), 500


@main.route('/api/v1/users/score', methods=['POST'])
@auth.login_required
def upsert_score():
    try:
        data = request.json
        if not data or not all(k in data for k in ("user_id", "score")):
            return jsonify({"error": "Invalid data"}), 400

        score = Score.upsert_score(data["user_id"], data["score"])
        return jsonify({
            "request-identifier" : request_identifier,
            "message" : None,
            "data" : score
        }), 200
    except Exception as e:
        # Log the error
        print(f"An error occurred while adding a score: {e}")
        # Return an error response
        return jsonify({
            "request-identifier": request_identifier,
            "message": "An error occurred while processing the request.",
            "data": None
        }), 500


@main.route('/api/v1/users/aggregate', methods=['GET'])
@auth.login_required
def get_users_grouped_by_score():
    try:
        users = User.get_users_grouped_by_score()
        return jsonify({
            "request-identifier": request_identifier,
            "message": None,
            "data": users
        }), 200
    except Exception as e:
        # Log the error
        print(f"An error occurred while aggregating a score: {e}")
        # Return an error response
        return jsonify({
            "request-identifier": request_identifier,
            "message": "An error occurred while processing the request.",
            "data": None
        }), 500


@main.route('/api/v1/users/calculate_winner', methods=['GET'])
@auth.login_required
def calculate_winner():
    winner = Score.calculate_winner()
    request_identifier = str(uuid.uuid4())
    if winner:
        # Return the winner as JSON
        return jsonify({
            "request-identifier" : request_identifier,
            "message" : None,
            "data" : winner
        }), 200
    else:
        return jsonify({"message": "No users found."}), 404