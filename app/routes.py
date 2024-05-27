from flask import Blueprint, request, jsonify
from app.models import User, Score
from app.auth import auth
from dotenv import load_dotenv
import uuid
import boto3
import json
import os
import datetime

load_dotenv()

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
    request_identifier = str(uuid.uuid4())
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    users = User.get_all_users(page, page_size)
    return jsonify({
        "request-identifier": request_identifier,
        "message": None,
        "data": users
    }), 200


@main.route('/users/score', methods=['POST'])
@auth.login_required
def upsert_score():
    request_identifier = str(uuid.uuid4())
    data = request.json
    if not data or not all(k in data for k in ("user_id", "score")):
        return jsonify({
            "request-identifier" : request_identifier,
            "message" : "Invalid data",
            "data" : None
        }), 400

    # Initialize Boto3 client for Kinesis
    kinesis_client = boto3.client(
        'kinesis',
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
        region_name=os.environ.get('AWS_REGION')
    )

    # Environment variable for Kinesis stream name
    KINESIS_STREAM_NAME = os.environ.get('KINESIS_STREAM_NAME')

    # Kinesis payload
    kinesis_data = {
        "request_identifier": request_identifier,
        "user_id": data["user_id"],
        "score": data["score"],
        "event_time": datetime.datetime.utcnow().isoformat()
    }

    # Put record to Kinesis stream
    try:
        kinesis_client.put_record(
            StreamName=KINESIS_STREAM_NAME,
            Data=json.dumps(kinesis_data),
            PartitionKey=data["user_id"]
        )
    except Exception as e:
        print(f"Failed to send data to Kinesis: {str(e)}")
        return jsonify({
            "request-identifier": request_identifier, 
            "message": "Failed to send data to Kinesis",
            "data": None
        }), 500

    return jsonify({
        "request-identifier": request_identifier,
        "message": None,
        "data": None
    }), 200


@main.route('/users/calculate_winner', methods=['GET'])
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