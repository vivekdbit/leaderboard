import os

class Config:
    MONGO_URI = os.getenv('MONGO_URI')
    KINESIS_STREAM_NAME = os.getenv('KINESIS_STREAM_NAME')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.getenv('AWS_REGION')