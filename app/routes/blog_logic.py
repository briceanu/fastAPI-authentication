
from sqlalchemy.orm import Session
from fastapi import status, HTTPException
from sqlalchemy import select, insert, delete, and_, update
from schemas import Blog_Schema_Create, Blog_Schema_Update
from models import Blog
import uuid


def create_blog(user_id:uuid.UUID,
                blog_data:Blog_Schema_Create,
                session:Session,
            ):
    stmt = insert(Blog).values(
        title=blog_data.title,
        content=blog_data.content,
        created_at=blog_data.created_at,
        updated_at=blog_data.updated_at,
        user_id=user_id)
    session.execute(stmt)
    session.commit()

    return {'success':'blog saved'}


 

def remove_blog(user_id:uuid.UUID,blog_id:uuid.UUID,session:Session):
    blog = session.execute(select(Blog).where(Blog.blog_id == blog_id)).scalar_one_or_none()
    if not blog:
        return None

    if blog.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to delete this blog")    

    stmt = delete(Blog).where(Blog.blog_id==blog_id)
    session.execute(stmt)
    session.commit()
    return {'success':'blog removed'}


 
def partial_update(
        user_id:uuid.UUID,
        blog_id:uuid.UUID,
        data:Blog_Schema_Update,
        session:Session,
        ):
    stmt = (select(Blog)
            .where(Blog.blog_id==blog_id))
    
    blog = session.execute(stmt).scalar()
    if not blog:
        return None
    if blog.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to update this blog")    

    stmt = (update(Blog)
            .where(Blog.blog_id==blog.blog_id)
            .values(content=data.content,updated_at=data.updated_at))
    session.execute(stmt)
    session.commit()
    return {'success':'blog updated'}

 

def total_update(
        user_id:uuid.UUID,
        blog_id:uuid.UUID,
        data:Blog_Schema_Create,
        session:Session,
        ):
    stmt = (select(Blog)
            .where(Blog.blog_id==blog_id))
    
    blog = session.execute(stmt).scalar()
    if not blog:
        return None
    if blog.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to update this blog")    

    stmt = (update(Blog)
            .where(Blog.blog_id==blog.blog_id)
            .values(**data.model_dump()))
    session.execute(stmt)
    session.commit()
    return {'success':'blog updated'}

 
