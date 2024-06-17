from fastapi import FastAPI, Form, Request
from typing import Annotated
import re
from typing import List
from database import User
from database import SessionLocal, engine
from fastapi.responses import HTMLResponse,  RedirectResponse
from helpers.helpers import get_db
from pydantic import BaseModel
from helpers.models import UserCreate, UserResponse
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from dotenv import load_dotenv , find_dotenv
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pickle
from helpers.reccomender import books_recommendation, load_pivot
# load the enviornment variables
load_dotenv(find_dotenv())

book_pivot = load_pivot()



with open("nearest_neighbors_model.pkl", "rb") as file:
    model = pickle.load(file)






# instantiate FastAPI
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
# this goes
@app.get("/", response_class=HTMLResponse)
def home(requests: Request):
    return templates.TemplateResponse("home.html", {"request": requests})


# the request gets processed and thrown around...
@app.post("/users/", response_class=HTMLResponse)
def create_user(request: Request, name: str = Form(...), email: str = Form(...), active: bool = Form(True), db: Session = Depends(get_db)):
    # Check if the user already exists if he does raise an error
    db_user = db.query(User).filter(User.email == email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create a new user
    new_user = User(name=name, email=email, is_active=active)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Ensure the email is correctly passed in the URL
    return RedirectResponse(url=f"/user_home?email={new_user.email}", status_code=303)


# to here 
@app.get("/user_home", response_class=HTMLResponse)
def user_home(request: Request, email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    return templates.TemplateResponse("user_home.html", {"request": request, "user": user})

# submit the book to show reccomendations
@app.post("/submit_books/", response_class=HTMLResponse)
def submit(request: Request, books: str = Form(...)):
    user_liked_books = re.split(r',\s*(?=[^)]*(?:\(|$))', books)
    user_liked_books = [book.strip().lower() for book in user_liked_books]
    suggested_books = books_recommendation(user_liked_books, model, book_pivot, 9)
    suggested_books = [' '.join(word.title() for word in book.split()) for book in suggested_books]
    return RedirectResponse(url=f"/show_books/?suggested_books={','.join(suggested_books)}", status_code=303)



@app.get("/show_books/", response_class=HTMLResponse)
def show_books(request: Request, suggested_books: str):
    suggested_books_list = suggested_books.split(',')

    return templates.TemplateResponse("show_books.html", {"request": request, "suggested_books": suggested_books_list})



@app.get("/book/{book_name}", response_class=HTMLResponse)
def book_detail(request: Request, book_name: str):
    return templates.TemplateResponse("book_detail.html", {"request": request, "book": book_name})
    




# http://127.0.0.1:8000/user_home?email=jared.peck@uconn.edu




'''
#--------------------------
# get all the users
@app.get("/users/", response_model=List[UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    # go into the db and query it. 
    users = db.query(User).offset(skip).limit(limit).all()
    return users


# get user by id use the Response class because we are getting the User 
@app.get("/users/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    # return none if no user found
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user



# delete a user 
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}


# update user
@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_data: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    for field, value in user_data.model_dump(exclude_unset=True).items():
        setattr(db_user, field, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
'''

