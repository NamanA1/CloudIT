from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Dict

app = FastAPI()

# ✅ User model
class User(BaseModel):
    name: str
    email: EmailStr

class UserOut(User):
    id: int

# ✅ In-memory store
users: Dict[int, User] = {}
user_id_counter = 1

# ✅ Create new user
@app.post("/users", response_model=UserOut, status_code=201)
def create_user(user: User):
    global user_id_counter
    new_user = user.dict()
    users[user_id_counter] = User(**new_user)
    response = UserOut(id=user_id_counter, **new_user)
    user_id_counter += 1
    return response

# ✅ Get user by ID
@app.get("/users/{id}", response_model=UserOut)
def get_user(id: int):
    if id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut(id=id, **users[id].dict())

# ✅ Update user
@app.put("/users/{id}", response_model=UserOut)
def update_user(id: int, updated_user: User):
    if id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    users[id] = updated_user
    return UserOut(id=id, **updated_user.dict())

# ✅ Delete user
@app.delete("/users/{id}", status_code=204)
def delete_user(id: int):
    if id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    del users[id]
