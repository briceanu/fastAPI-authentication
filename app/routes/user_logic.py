from jose import jwt, JWTError

from sqlalchemy.orm import Session, selectinload,joinedload
from sqlalchemy import select, insert,update, func
from schemas import User_Schema_Create
from models import User
import uuid
from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
from fastapi.security import  OAuth2PasswordBearer
from typing import Annotated
from fastapi import Depends, HTTPException,status



SECRET_KEY = '120NOJ092NOINaowdi90230ifsoie0932nf2039fn203'
ALGORITHM = 'HS256'
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/user/login/")



def sign_up(user_data:User_Schema_Create,session:Session):
    stmt = insert(User).values(
        username=user_data.username,
        email=user_data.email,
        date_of_birth=user_data.date_of_birth,
        password = bcrypt_context.hash(user_data.password))
    session.execute(stmt)
    session.commit()
    return {'success': 'your account has been created'}


 
def authenticate_user(username:str,password:str,session:Session):
    stmt = select(User).where(User.username == username)
    user = session.execute(stmt).scalar()
    if not user:
        return False
    if not bcrypt_context.verify(password,user.password):
        return False
    return user


def create_access_token(username: str, user_id: uuid.UUID,expires_delta: timedelta):
    encode = {'sub': username, 'id': str(user_id)}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)




async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id :uuid.UUID = payload.get('id')

        if username is None or user_id is None:
            raise credentials_exception
        return {'username':username,'id':user_id}

    except JWTError:
        raise credentials_exception



def remove_user(user_id:uuid.UUID,session:Session):
    user = session.get(User,user_id)
    if user is None:
        return
    session.delete(user)
    session.commit()
    return {'success':'your account has been removed'}



def get_all(session:Session):

    stmt = (select(User)
            .options(selectinload(User.blogs))
            )
    users = session.execute(stmt).scalars().all()
    return users




def count_users(session:Session):
    stmt = select(func.count(User.user_id))
    user_number = session.execute(stmt).scalar()
    return {'number_of_users':user_number}




def get_oldest_user(session:Session):
    stmt = select(User,func.min(User.date_of_birth).options(selectinload(User.blogs)))
    user = session.execute(stmt).scalar_one()
    return user


# this is the one
def update_user_name(new_name:str,
                    user_id:uuid.UUID,
                    session:Session):

    stmt = update(User).where(User.user_id == user_id).values(username=new_name)
    result = session.execute(stmt)
    if result.rowcount == 0:
        return 
    session.commit()


    return {'success': 'Username updated successfully'}






def update_all(user_id:uuid.UUID,
               user_data:User_Schema_Create,
               session:Session):
    stmt = (update(User)
            .where(User.user_id == user_id)
            .values(**user_data.model_dump())
         )
    result = session.execute(stmt)
    if result.rowcount == 0:
        return
    session.commit()
    return {'success':'user successfully updated'}



def get_user(user:str,session:Session):
    stmt = (select(User)
            .where(User.username==user)
            .options(joinedload(User.blogs))
        )
    user = session.execute(stmt).scalar()
    if user is None:
        return False
    return user
