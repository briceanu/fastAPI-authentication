from fastapi import APIRouter, Depends, Body, HTTPException, status 
from sqlalchemy.orm import Session
from db.db_connection import get_db
from . import blog_logic
from schemas import  Blog_Schema_Create, Blog_Schema_Update
from models import User
from . import user_logic
from typing import Annotated
router = APIRouter(prefix='/blogs',tags=['routes for the blogs'])
import uuid
from sqlalchemy.exc import IntegrityError


@router.post('/create')
async def get_blog(
    user:Annotated[User,Depends(user_logic.get_current_user)],
    blog_data:Annotated[Blog_Schema_Create,Body()],
    session:Session=Depends(get_db),
    ) -> dict:
    valid_user = uuid.UUID(user['id'])
    data = blog_logic.create_blog(valid_user,blog_data,session)
    return data

@router.delete('/delete')
async def remove_blog(
    user_id:Annotated[User,Depends(user_logic.get_current_user)],
    blog_id:Annotated[uuid.UUID,Body()],
    session:Session=Depends(get_db))->dict:
    try:
        valid_user_id = uuid.UUID(user_id['id'])
        result = blog_logic.remove_blog(valid_user_id,blog_id,session)
        if result is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'no blog with the id {blog_id}found ')
        return result
    
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'an error occured {str(e)}')
    



@router.patch('/partial_update')
async def update_blog(
    user_id:Annotated[User,Depends(user_logic.get_current_user)],
    blog_id:Annotated[uuid.UUID,Body()],
    data:Annotated[Blog_Schema_Update,Body()],
    session:Session=Depends(get_db),
    ) -> dict:
    try:
        valid_user_id = uuid.UUID(user_id['id'])
        result = blog_logic.partial_update(valid_user_id,blog_id,data,session)
        if result is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'no blog with the id {blog_id} found')
        return result
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f'an error occured: {str(e.orig)}')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'an error occured {str(e)}')
    




@router.put('/total_update')
async def total_update_blog(
    user_id:Annotated[User,Depends(user_logic.get_current_user)],
    blog_id:Annotated[uuid.UUID,Body()],
    update_data:Annotated[Blog_Schema_Create,Body()],
    session:Session=Depends(get_db),
    ) -> dict:
    try:
        valid_user_id = uuid.UUID(user_id['id'])
        result = blog_logic.total_update(valid_user_id,blog_id,update_data,session)
        if result is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                detail=f'no blog with the id {blog_id} found')
        return result
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f'an error occured: {str(e.orig)}')
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'an error occured {str(e)}')