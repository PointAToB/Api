from datetime import datetime
from typing import Optional, Union
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
    weight: Union[int, None] # Stored in pounds
    height: Union[int, None] # Stored in inches
    birthDate: Union[datetime, None]

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
    status: Optional[str] = "error"
    message: str
