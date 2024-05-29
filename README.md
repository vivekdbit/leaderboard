# Leaderboard Assignment Setup and Run Instructions

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
    cd leaderboard
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

6. Running Tests with pytest
    
    Execute the pytest command to run all tests in your project.
   ```
   pytest
    ```
    Alternatively, to run tests in a specific file:
    ```
    pytest test/test_users.py
    ```

6. API Endpoints
    | ID | METHOD | API                     | Description                     |
    | -- | ------ | ----------------------- | ------------------------------- |
    | 1  | POST   | /api/v1/users           | Add Fake User                   |
    | 2  | DELETE | /api/v1/users/{user_id} | Delete User                     |
    | 3  | GET    | /api/v1/users           | Get paginated users, Defulat 20 |
    | 4  | POST   | /api/v1/users/score     | Add scores                      |
    | 5  | GET    | /api/v1/users/aggregate | Get users grouped by score      |

7. API contracts: https://documenter.getpostman.com/view/30759648/2sA3QsAs2E#0b82d441-98f7-4a62-ae85-7ad7d10055f3


## Out of Scope
1. Logger
2. Time Zone
