from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    MONGO_URI = os.getenv('MONGO_URI')
    API_AUTH_USERNAME = os.getenv('API_AUTH_USERNAME')
    API_AUTH_PASSWORD = os.getenv('API_AUTH_PASSWORD')
    KINESIS_STREAM_NAME = os.getenv('KINESIS_STREAM_NAME')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = os.getenv('AWS_REGION')