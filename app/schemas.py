from pydantic import BaseModel, EmailStr, field_validator
import uuid
from datetime import datetime,date
import uuid
from typing import List
import re

class Blog_Schema_Create(BaseModel):
    title:str
    content:str
    created_at: datetime
    updated_at:datetime | None

    class Config:
        extra = 'forbid'



class Blog_Schema_Return(Blog_Schema_Create):
    blog_id:uuid.UUID
 

class Blog_Schema_Update(BaseModel):
    content:str
    updated_at:datetime 



class User_Schema_Create(BaseModel):
    username:str
    password:str
    email:EmailStr
    date_of_birth: date

    @field_validator('date_of_birth')
    @classmethod
    def validate_date_of_birth(cls,value):
        min_date = date(1930,1,1)
        if value < min_date:
            raise ValueError("Date of birth cannot be earlier than 01-01-1930")
        return value

    @field_validator('password')
    @classmethod
    def validate_password(cls,value):
        if len(value) < 6:
            raise ValueError('Password must be at least 6 characters long')

        if not re.search(r'[A-Za-z]', value):  # Check for at least one letter
            raise ValueError('Password must include at least one letter')

        if not re.search(r'\d', value):  # Check for at least one number
            raise ValueError('Password must include at least one number')

        return value





    class Config:
        extra = 'forbid'



class User_Schema_Return(User_Schema_Create):
    user_id:uuid.UUID
    blogs:List['Blog_Schema_Return']


class Token(BaseModel):
    access_token:str
    token_type:str


class User_Data_Login(BaseModel):
    username:str
    password:str
 