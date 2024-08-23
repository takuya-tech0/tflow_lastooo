# /Users/takuya/Documents/talent-flow1.1/fastapi-backend/schemas.py
from pydantic import BaseModel

class EmployeeCreate(BaseModel):
    username: str
    password: str

class Employee(BaseModel):
    username: str

    class Config:
        orm_mode = True
