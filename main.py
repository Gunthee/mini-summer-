from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import List
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# --- Models and in-memory stores ---

class Todo(BaseModel):
    item: str
    owner: str

users: List[str] = []
todos: List[Todo] = []

# --- Routes ---

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "users": users,
        "todos": todos,
    })

@app.post("/create-user")
def create_user(user: str = Form(...)):
    if user not in users:
        users.append(user)
    return RedirectResponse("/", status_code=303)

@app.post("/create-todo")
def create_todo(username: str = Form(...), item: str = Form(...)):
    # 1. Only allow if the user exists
    if username not in users:
        raise HTTPException(status_code=400, detail="Username not registered")
    # 2. Create a Todo with owner set
    todos.append(Todo(item=item, owner=username))
    return RedirectResponse("/", status_code=303)

@app.get("/todos", response_model=List[Todo])
def get_all_todos():
    """2. Return the full list of todos, each with its owner."""
    return todos

@app.get("/todos/{username}", response_model=List[Todo])
def get_user_todos(username: str):
    """2. Return only the todos owned by `username`."""
    return [t for t in todos if t.owner == username]

@app.post("/delete-todo")
def delete_todo(username: str = Form(...), index: int = Form(...)):
    # 3. Enforce that you can delete only your own todos by filtering
    user_list = [t for t in todos if t.owner == username]
    if index < 0 or index >= len(user_list):
        raise HTTPException(status_code=400, detail="Invalid index or not your todo")
    # Remove from the global list
    todos.remove(user_list[index])
    return RedirectResponse("/", status_code=303)
