from datetime import datetime
from typing import Optional
from ninja import Schema
from pydantic import EmailStr

# Create user response
class CreateUser(Schema):
    firstName: str
    lastName: str
    email: EmailStr
    password: str

# Retrieve user response
class RetrieveUser(Schema):
    firstName: str
    lastName: str
    email: EmailStr
    weight: int # Stored in pounds
    height: int # Stored in inches
    birthDate: datetime

# Update user response
class UpdateUser(Schema):
    firstName: Optional[str]
    lastName: Optional[str]
    email: Optional[EmailStr]
    weight: Optional[int] # Stored in pounds.
    height: Optional[int] # Stored in inches
    birthDate: Optional[datetime]


# Error response
class Error(Schema):
    status: str = "error"
    code: int
    message: str


# Success response
class Success(Schema):
    status: str = "success"
    code: int
    message: Optional[str] = None
