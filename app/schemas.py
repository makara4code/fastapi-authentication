from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str
    
    
class CreateUserRequest(BaseModel):
    username: str
    passowrd: str