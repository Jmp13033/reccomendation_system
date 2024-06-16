from pydantic import BaseModel


# takes user input 
class UserCreate(BaseModel):
    name: str
    email: str
    is_active: bool = True

# is for representing user data in API responses
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool

    class Config:
        from_attributes = True