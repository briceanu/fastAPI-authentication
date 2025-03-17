from fastapi import APIRouter, Depends, Body, HTTPException, status
from sqlalchemy.orm import Session
from db.db_connection import get_db
from . import user_logic
from schemas import User_Schema_Return, User_Schema_Create, Token
from typing import Annotated
from sqlalchemy.exc import IntegrityError
import uuid
from typing import List
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from models import User
from uuid import UUID

router = APIRouter(prefix='/user',tags=['routes for the users'])


@router.post('/create_account',status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: User_Schema_Create, session: Session = Depends(get_db)) -> dict:
    try:
        user = user_logic.sign_up(user_data, session)
        return user
    except HTTPException:
        raise
    except IntegrityError as e:
        raise HTTPException(status_code=400,
                            detail=f'Integrity error: {str(e.orig)}')
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"An error occurred: {str(e)}")



@router.post('/login',response_model=Token)
async def login(form_data: Annotated[OAuth2PasswordRequestForm,
                                     Depends()],
                session: Session = Depends(get_db)):
    user = user_logic.authenticate_user(form_data.username, form_data.password,
                                        session)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='username or password do not match')

    token = user_logic.create_access_token(user.username,user.user_id,timedelta(minutes=30))
    return {'access_token':token,'token_type':'bearer'}






@router.delete('/delete')
async def remove_user(user_id:uuid.UUID,
                      session:Session=Depends(get_db))-> dict:
    try:
        user = user_logic.remove_user(user_id,session)
        if user is None:
            raise HTTPException(status_code=400, detail=f'no user with the id {user_id}')
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f'an error occured: {str(e)}')


@router.get('/all')
async def get_all_users(session:Session=Depends(get_db))-> List[User_Schema_Return]:
    try:
        users = user_logic.get_all(session)
        return users
    except Exception as e:
        raise HTTPException(status_code=500,detail=f'an error occured: {str(e)}')




@router.get('/number')
async def count_number_of_users(session:Session=Depends(get_db))-> dict:
    try:
        users = user_logic.count_users(session)
        return users
    except Exception as e:
        raise HTTPException(status_code=500,detail=f'an error occured: {str(e)}')




@router.patch('/update_name')
async def update_name(
    new_name:Annotated[str,Body()],
    user_id:User=Depends(user_logic.get_current_user),
    session:Session=Depends(get_db)):

    try:
        converted_user_id=UUID(user_id['id'])
        user = user_logic.update_user_name(new_name,converted_user_id,session)
        if user is None:
            raise HTTPException(status_code=400,detail=f'no user with the id {user_id}')
        return user

    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f'an error occured: {str(e.orig)}')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f'an error occured: {str(e)}')



# this route is protected
@router.get('/oldest_user')
async def get_oldest_user(
        current_user: Annotated[User, Depends(user_logic.get_current_user)],
        session: Session = Depends(get_db)) -> User_Schema_Return:
    try:
        user = user_logic.get_oldest_user(session)
        return user
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"An error occurred: {str(e)}")





@router.put('/update_all')
async def update_user_all(user_id:uuid.UUID,
                      data:Annotated[User_Schema_Create,Body()],
                      session:Session=Depends(get_db)):

    try:
        user = user_logic.update_all(user_id,data,session)
        if user is None:
            raise HTTPException(status_code=400, detail=f'no user with the id {user_id}')
        return user

    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f'an error occured: {str(e.orig)}')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500,detail=f'an error occured: {str(e)}')





# this route is protected
@router.get('/user')
async def get_user(    
        current_user:Annotated[User, Depends(user_logic.get_current_user)],
        session: Session = Depends(get_db),
) -> User_Schema_Return:

    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                              detail='could not validate credentials')

    try:
        user = user_logic.get_user(current_user['username'],session)
        if user is None:
            raise exception
        return user
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"An error occurred: {str(e)}")
