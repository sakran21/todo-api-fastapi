# Task Manager API

A simple, extensible to-do list API built with Python and FastAPI.

This project serves as both a portfolio demonstration and a foundation for a potential full-stack productivity app. It includes basic CRUD functionality and is structured for easy expansion into more advanced use cases.

---

## Features

- `GET /todos` – Retrieve all todos  
- `POST /todos` – Create a new todo  
- Input validation with Pydantic  
- Interactive API documentation at `/docs` (Swagger UI)
This is the skeleton of a full productivity system — or maybe just a to-do list.  
Depends how far the madness goes.


---



## Tech Stack

- Python 3.x  
- FastAPI  
- Uvicorn  
- Pydantic  

---

## Setup Instructions

1. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

4. Visit:
   - `http://127.0.0.1:8000` — API root  
   - `http://127.0.0.1:8000/docs` — interactive API docs

---

## License

This project is currently licensed under the MIT License.  
Note: This may be updated in the future if the project evolves toward commercial distribution.

---

## Author

Created and maintained by Moham.alsakran 
GitHub: [https://github.com/sakran21](https://github.com/sakran21)

##  Notes to Future Me

- Remember to update the LICENSE if you ever take this commercial  