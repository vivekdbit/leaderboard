import os
import datetime
import json
import boto3
import uuid

def test_kinesis(data):
    request_identifier = str(uuid.uuid4())
    
    # Initialize Boto3 client for Kinesis
    kinesis_client = boto3.client(
        'kinesis',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name=os.getenv('AWS_REGION')
    )

    # Put record to Kinesis stream
    try:
        # Kinesis payload
        kinesis_data = {
            "request_identifier": request_identifier,
            "user_id": data["user_id"],
            "score": data["score"],
            "event_time": datetime.datetime.utcnow()
        }
        kinesis_client.put_record(
            StreamName=os.environ.get('KINESIS_STREAM_NAME'),
            Data=json.dumps(kinesis_data),
            PartitionKey=data["user_id"]
        )

    except Exception as e:
        print(f"Failed to send data to Kinesis: {str(e)}")
        return None