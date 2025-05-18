from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
from fastapi import status



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


@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    for todo in Todos:
        if todo["id"] == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")

@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int):
    for i, todo in enumerate(Todos):
        if todo["id"] == todo_id:
            Todos.pop(i)
            return
    raise HTTPException(status_code=404, detail="Todo not found")

class Todo(BaseModel):
    id:int
    title: str
    completed: bool

@app.put("/todos/{Todos_id}")
def update_todo(todo_id: int, updated_todo: Todo):
    for i, todo in enumerate(Todos):
        if todo["id"]==todo_id:
            Todos[i] = updated_todo.dict()    
            return Todos[i]
    raise HTTPException(status_code=404,details="Todo not found!")    