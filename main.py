from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import List

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Temporary storage for todos (in-memory)
todos: List[str] = []

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos, "users": users})

@app.post("/create-todo")
def create_todo(item: str = Form(...)):
    todos.append(item)
    return RedirectResponse("/", status_code=303)

# Temporary storage for todos (in-memory)
users: List[str] = []
@app.post('/create-user')
def create_todo_user(user: str= Form(...)):
    users.append(user)
    return RedirectResponse("/", status_code=303)

# @app.post('/user-post')
# def user_post():
    

# @app.get('get-todo')
# def get_todo():
#     return
