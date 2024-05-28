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
    | ID | METHOD | API                     | Description                     |
    | -- | ------ | ----------------------- | ------------------------------- |
    | 1  | POST   | /api/v1/users           | Add Fake User                   |
    | 2  | DELETE | /api/v1/users/{user_id} | Delete User                     |
    | 3  | GET    | /api/v1/users           | Get paginated users, Defulat 20 |
    | 4  | POST   | /api/v1/users/score     | Add scores                      |
    | 5  | GET    | /api/v1/users/aggregate | Get users grouped by score      |

7. API contracts

    #### 1. Add Fake User 

    <summary><code>POST</code> <code>/api/v1/users</code></summary>

    ##### Parameters

    > | name      |  type     | data type               | description                                                           |
    > |-----------|-----------|-------------------------|-----------------------------------------------------------------------|
    > | None      |  -        | -                       | Adds fake user to database                                            |


    ##### Responses

    > | http code     | content-type                      | response                                                            |
    > |---------------|-----------------------------------|---------------------------------------------------------------------|
    > | `201`         | `application/json`                | `{"data"{}, "message":"User created successfully","request-identifier": ""}`                                |
    > | `400`         | `application/json`                | `{"code":"400","message":"Bad Request"}`                            |
        