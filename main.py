from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
from fastapi import status
from typing import List
from datetime import datetime, timezone
import pandas as pd




class Todo(BaseModel):
    title: str
    completed:bool = False

app = FastAPI()
@app.get("/")       #visit decorators at a later time to learn more
def read_root():
    return {"message": "Task Manager API", "endpoints":[
        "/todos", "/todos/{id}", "/analytics/summary"
    ]} 


Todos = [
    {"id": 1, "title": "Buy groceries", "completed": False},
    {"id": 2, "title": "Clean the house", "completed": True},
] 

now = datetime.now((timezone.utc))

for todo in Todos:
    if "created_at" not in todo:
        todo["created_at"]=now
    if "completed_at" not in todo:
        if todo["completed"]: todo["completed_at"]=now
        else: todo["completed_at"]=None 


@app.get ("/todos")
def get_todos():
    return Todos


@app.post("/todos", status_code=201)
def create_todo(todo: Todo):
    now = datetime.now((timezone.utc))
    new_todo = {
        "id": len(Todos) + 1,
        "title": todo.title,
        "created_at": now,
        "completed_at": now if todo.completed else None,
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


@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: Todo):
    for i, todo in enumerate(Todos):
        if todo["id"]==todo_id:
            todo["title"] = updated_todo.title
            todo["completed"] = updated_todo.completed
            if updated_todo.completed:
                todo["completed_at"]= datetime.now(timezone.utc)   
            else:todo["completed_at"] = None    
            return todo
    raise HTTPException(status_code=404,detail="Todo not found!")    

@app.get("/analytics/summary")
def analytics_summary():
    if not Todos:
        return {
        "total":0,
        "completed":0,
        "completed_rate":0.0,
        "avg_completion_seconds":None,
    }


    
    df = pd.DataFrame(Todos)

    needed_cols = ["completed", "created_at","completed_at"]

    for col in needed_cols:
        if col not in df.columns:
            df[col]=None

    df["completed"] = df["completed"].fillna(False).astype(bool)        

    total = int(len(df))
    completed = int(df["completed"].sum())

    completion_rate= float(completed/total)
    completion_rate= round(completion_rate,3)



    completed_df = df[df["completed"]==True].copy()

    if len(completed_df)==0:
        avg_seconds = None
    else:
        completed_df["created_at"]=pd.to_datetime(completed_df["created_at"],utc=True, errors="coerce")
        completed_df["completed_at"]=pd.to_datetime(completed_df["completed_at"], utc = True, errors="coerce")
        
        completed_df = completed_df.dropna(subset=["created_at","completed_at"])
        if len(completed_df)==0:
            avg_seconds=None
        else:
             
             durations=(completed_df["completed_at"]- completed_df["created_at"]).dt.total_seconds()
             avg_seconds=float(durations.mean())
             avg_seconds=round(avg_seconds,2)
                
    return{"total":total,
           "completed":completed,
           "completion_rate": completion_rate,
           "avg_completion_seconds": avg_seconds,
           }    
