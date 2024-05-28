def test_kinesis(user_id, score):
    request_identifier = str(uuid.uuid4())
    data = request.json
    if not data or not all(k in data for k in ("user_id", "score")):
        return jsonify({
            "request-identifier" : request_identifier,
            "message" : "Invalid data",
            "data" : None
        }), 400
    
    # TODO - validation
    # Check if user_id is a valid ObjectId, if not, convert it
        # if not ObjectId.is_valid(user_id):
        #     raise ValueError("Invalid user_id")

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
            "event_time": datetime.datetime.utcnow().isoformat()
        }
        kinesis_client.put_record(
            StreamName=os.environ.get('KINESIS_STREAM_NAME'),
            Data=json.dumps(kinesis_data),
            PartitionKey=data["user_id"]
        )
        return jsonify({
            "request-identifier": request_identifier,
            "message": None,
            "data": None
        }), 200
    except Exception as e:
        print(f"Failed to send data to Kinesis: {str(e)}")
        return jsonify({
            "request-identifier": request_identifier, 
            "message": "Failed to send data to Kinesis",
            "data": None
        }), 500