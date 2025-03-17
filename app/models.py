from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    validates
    )
import uuid
from sqlalchemy import func, DateTime,Date, ForeignKey, String
from datetime import date
from typing import List
import re

class Base(DeclarativeBase):
    pass

class Blog(Base):
    __tablename__ = 'blog'
    blog_id : Mapped[uuid.UUID] = mapped_column(primary_key=True,default=lambda:uuid.uuid4(), unique=True)
    title : Mapped[str] = mapped_column(String(60))
    content : Mapped[str] = mapped_column()
    created_at :Mapped[date] = mapped_column(DateTime,default=func.now())
    updated_at: Mapped[date | None] = mapped_column(DateTime, nullable=True, default=None)
    user_id:Mapped[uuid.UUID] = mapped_column(ForeignKey('user.user_id'))
    user :Mapped['User'] = relationship(back_populates='blogs',uselist=False)


class User(Base):
    __tablename__ = 'user'
    user_id: Mapped[uuid.UUID] = mapped_column(primary_key=True,
                                               default=lambda: uuid.uuid4(),
                                               unique=True)
    username: Mapped[str] = mapped_column(String(60), unique=True)
    password: Mapped[str] =mapped_column(String)
    email: Mapped[str] = mapped_column(String(100),
                                       nullable=False,
                                       unique=True)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    blogs: Mapped[List['Blog']] = relationship(back_populates='user')

    @validates
    def validate_date_of_birth(self, key, value):
        min_date = date(1930, 1, 1)
        if value < min_date:
            raise ValueError("Date of birth cannot be earlier than 01-01-1930")
        return value

    @validates
    def validate_password(self,key,value):
        if len(value) < 6:
            raise ValueError('Password must be at least 6 characters long')

        if not re.search(r'[A-Za-z]', value):  # Check for at least one letter
            raise ValueError('Password must include at least one letter')

        if not re.search(r'\d', value):  # Check for at least one number
            raise ValueError('Password must include at least one number')
        
        return value










