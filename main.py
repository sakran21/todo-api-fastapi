from fastapi import FastAPI
from pydantic import BaseModel


class Todo(BaseModel):
    title: str
    completed:bool = False

app = FastAPI()
@app.get("/")       #visit decorators at a later time to learn more
def read_root():
    return {"message": "Live!"} 


Todos = [
    {"id": 1, "title": "Buy groceries", "completed": False},
    {"id": 2, "title": "Clean the house", "completed": True},
] 

@app.get ("/todos")
def get_todos():
    return Todos


@app.post("/todos", status_code=201)
def create_todo(todo: Todo):
    new_todo = {
        "id": len(Todos) + 1,
        "title": todo.title,
        "completed": todo.completed
    }
    Todos.append(new_todo)
    return new_todo