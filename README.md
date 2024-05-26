# Leaderboard Assignment Setup and Run Instructions
TODO add details

## Prerequisites
Tech Stack Used:
1. Python
2. Flask
3. MongoDB

## Steps to Set Up and Run the Project

1. Clone the Repository

    Clone the repository from your version control system:
    ```
    git clone https://github.com/vivekdbit/leaderboard.git
    cd your-flask-api-project
    ```
2. Create a Virtual Environment 
    
    Create a virtual environment to manage your project dependencies:
    ```
    python3 -m venv venv
    source venv/bin/activate
    ```
3. Install Dependencies
    
    Install the necessary Python packages using pip:
    ```
    pip install -r requirements.txt
    ```
4. Set Up Environment Variables
    
    Rename .env.sample to .env file:

    Add the following details to the .env file, replacing the placeholders with your actual MongoDB connection details:
    ```
    FLASK_APP=run.py
    FLASK_ENV=development
    MONGO_URI=mongodb://{connection_uri}
    ```
5. Run the Flask Application

    Start the Flask application using the following command:
    ```
    flask run
    ```
    Your Flask API should now be running at http://127.0.0.1:5000

6. API Endpoints
    
    | Sr | API                         | Description   |
    |----|-----------------------------|---------------|
    | 1  | GET /api/users              | Get all users |
    | 2  | DELETE /api/users/{user_id} | Delete user   |
    | 3  | POST /api/users             | Add user      |
    | 4  | POST /api/users/score       | Add score     |

    TODO
    add API contracts
    