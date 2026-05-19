from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
from fastapi import status
from fastapi import Depends
from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import List
from datetime import datetime, timezone
import pandas as pd
import random
from contextlib import asynccontextmanager

from datetime import timedelta
from sklearn.linear_model import LogisticRegression
from fastapi.responses import StreamingResponse
import io
import csv




class Todo(BaseModel):


    title: str
    completed:bool = False

sqlite_url ="sqlite:///todos.db"
engine = create_engine(sqlite_url, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

class TodoDB (SQLModel, table=True):
        id: int | None = Field(default=None, primary_key=True)
        title: str
        created_at: datetime = Field(default_factory= lambda:datetime.now(timezone.utc))
        completed_at: datetime | None=None
        completed: bool= False

Todos = [
    { 
      "id": 1,
      "title": "Buy groceries",
      "created_at": datetime(2026, 4, 1, 10, 0, 0, tzinfo=timezone.utc),
      "completed_at": None,
      "completed": False
    },
    {
        "id": 2,
        "title": "Clean the house",
        "created_at": datetime(2026, 4, 2, 9, 0, 0, tzinfo=timezone.utc),
        "completed_at": datetime(2026, 4, 2, 12, 0, 0, tzinfo=timezone.utc),
        "completed": True
    },
    ]

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/")       #visit decorators at a later time to learn more
def read_root():
    return {"message": "Task Manager API", "endpoints":[
        "/todos", "/todos/{id}", "/analytics/summary"
    ]} 




model=None

now = datetime.now((timezone.utc))

@app.post("/ml/train")
def train_model():
    global model
    x=[]
    y=[]
    now = datetime.now(timezone.utc)

    for todo in Todos:
        if "created_at" not in todo:
            continue
        created_at =todo["created_at"]

        if created_at is None:
            continue

        age=(now-created_at).total_seconds()

        x.append([age])
        y.append(1 if todo["completed"] else 0)

    if len(x)<5:
        return {"error": "not enough data"}

    model = LogisticRegression()
    model.fit(x,y)

    return {
        "message": "model trained",
        "samples": len(x)
    }    

for todo in Todos:
    if "created_at" not in todo:
        todo["created_at"]=now
    if "completed_at" not in todo:
        if todo["completed"]: todo["completed_at"]=now
        else: todo["completed_at"]=None 


@app.get ("/todos")
def get_todos(session: Session = Depends(get_session)):
    todos= session.exec(select(TodoDB)).all()
    return todos


@app.post("/todos", status_code=201)
def create_todo(todo: Todo, session: Session = Depends(get_session)):
    now = datetime.now((timezone.utc))
    new_todo = TodoDB(
        title=todo.title,
        created_at=now,
        completed_at=now if todo.completed else None,
        completed=todo.completed
    )
    session.add(new_todo)
    session.commit()
    session.refresh(new_todo)
    return new_todo


@app.get("/todos/{todo_id}")
def get_todo(todo_id: int, session: Session=Depends(get_session)):
    todo=session.get(TodoDB,todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, session: Session=Depends(get_session)):
    todo = session.get(TodoDB, todo_id)
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    session.delete(todo)
    session.commit()
    return{"message": "Todo deleted"}


@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: Todo, session: Session=Depends(get_session)):
    todo=session.get(TodoDB,todo_id)
    if todo is None:
        raise HTTPException(status_code=404,detail="Todo not found!")    
    
    todo.title=updated_todo.title
    todo.completed=updated_todo.completed
    if updated_todo.completed:
        todo.completed_at=datetime.now(timezone.utc)
    else:
        todo.completed_at=None
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo        

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

@app.post("/ml/generate")
def generatedata(n: int = 100):
    now = datetime.now(timezone.utc)

    for _ in range(n):
        task_type = random.choices(
            ["routine", "periodic", "milestone"],
            weights=[70, 25, 5],
            k=1
        )[0]

        created_at = now - timedelta(days=random.randint(0, 365))

        if task_type == "routine":
            duration = timedelta(hours=random.randint(1, 12))
        elif task_type == "periodic":
            duration = timedelta(days=random.randint(1, 7))
        else:
            duration = timedelta(days=random.randint(90, 270))

        expected_finish = created_at + duration

        if expected_finish > now:
            completed = False
            completed_at = None
        else:
            completed = random.random() < 0.85
            completed_at = expected_finish if completed else None

        new_todo = {
            "id": len(Todos) + 1,
            "title": f"{task_type} task {len(Todos) + 1}",
            "created_at": created_at,
            "completed_at": completed_at,
            "completed": completed
        }

        Todos.append(new_todo)

    return {"message": f"{n} todos generated", "total": len(Todos)}



@app.post("/ml/predict")
def predict_completion(age_seconds: float):
    global model

    if model is None:
        return {"error": "model not trained"}
    
    prediction =model.predict([[age_seconds]])[0]
    probability = model.predict_proba([[age_seconds]])[0][1]

    return {
        "predicted_completed": bool(prediction),"completion_probability":round(float(probability),3)
    }

@app.get("/export/csv")
def export_csv():
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["id","title","created_at","completed_at","completed"])
    writer.writeheader()

    for todo in Todos:
        writer.writerow(todo)

    output.seek(0)
    return StreamingResponse(output, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=todos.csv"})
