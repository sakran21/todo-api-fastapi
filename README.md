# Task Manager API (FastAPI)

A lightweight RESTful API built with FastAPI for managing tasks, complete with automated testing.
 This project aims to refine backend development skills, explore structured API design, and establish a foundation for future full-stack enhancements.

-----------------------------------

## Tech Stack

- **FastAPI** – Modern Python web framework
- **Pydantic** – Data validation and management
- **pytest** – Testing framework
- **TestClient** – HTTP request simulation for testing
- **Uvicorn** – ASGI web server for running the API

-----------------------------------

## Running Locally

**1. Clone the repository**

```bash
git clone https://github.com/sakran21/task_manager_api.git
cd task_manager_api


**2. Activate the virtual environment
source venv/bin/activate

**3. Install required packages
pip install -r requirements.txt

**4.Launch the development server
uvicorn main:app --reload

 
**5Access the interactive API documentation**
Swagger UI: http://127.0.0.1:8000/docs
ReDoc UI: http://127.0.0.1:8000/redoc

Method      Endpoint         Description             
GET        `/todos`          Retrieve all todos      
GET        `/todos/{id}`     Retrieve a todo by ID   
POST       `/todos`          Create a new todo       
PUT        `/todos/{id}`     Update an existing todo 
DELETE     `/todos/{id}`     Delete a todo by ID     

-----------------------------------
Example: Create a new todo:

POST /todos
{
  "title": "Take out trash",
  "completed": false
}
-----------------------------------
Example: Update a todo

PUT /todos/3
{
  "id": 3,
  "title": "Recycle plastics",
  "completed": true
}
-----------------------------------

Test Coverage: 

run automated tests with: 
 python -m pytest

Included tests:

Coverage for all CRUD endpoints (GET, POST, PUT, DELETE)

Valid and invalid scenarios

6 test cases in total using TestClient
------------------------------------
Future Improvements
Integration of persistent storage (SQLite, PostgreSQL)

User authentication and authorization

Frontend implementation (React or similar frameworks)

Docker containerization for easier deployment

Advanced task management features (tags, deadlines, priority)






-----------------------------------

## License

This project is currently licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
Note: This may be updated in the future if the project evolves toward commercial distribution.

---

## Author

Created and maintained by Moham.alsakran 
GitHub: [https://github.com/sakran21](https://github.com/sakran21)

##  Notes to Future Me

- Remember to update the LICENSE if you ever take this commercial  