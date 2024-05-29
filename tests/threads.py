import threading
import requests
import json
import time

# Define the number of concurrent requests
NUM_THREADS = 100

# Define the user ID and score increment
USER_ID = '66558ae7ddd1c223539217cf'  
SCORE_INCREMENT = 5

# Define the API endpoint
API_URL = 'http://127.0.0.1:5000/api/v1/users/score'

# Define the payload
payload = {
    'user_id': USER_ID,
    'score': SCORE_INCREMENT
}

# Define the headers
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Basic YWRtaW46cGFzc3dvcmQ='
}

# Function to send a request to the API
def send_request():
    requests.post(API_URL, headers=headers, data=json.dumps(payload))

# List to hold threads
threads = []

# Start time
start_time = time.time()

# Create and start threads
threads = [threading.Thread(target=send_request) for _ in range(NUM_THREADS)]

# Start all threads
for thread in threads:
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

# End time
end_time = time.time()

print(f"Completed {NUM_THREADS} requests in {end_time - start_time} seconds")