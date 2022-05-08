from fastapi import APIRouter, Depends, status, HTTPException

from main.router.admin.utils import get_current_user

from .models import Post, PostInDb
from main.utils.db import get_connection


router = APIRouter(prefix="/posts", dependencies=[Depends(get_current_user)])


@router.post("/")
async def create_post(post: Post):
    new_post = PostInDb(**post.dict()).dict()
    new_post.pop('key')
    
    db_connection = get_connection('blog')
    
    saved_post = db_connection.put(new_post)
    return {
        'post': saved_post
    }
    

@router.put("/{post_key}")
async def update_post(post_key: str, post: Post):
    db_connection = get_connection('blog')
    saved_post = db_connection.get(post_key)
    
    if not saved_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    updated_post = saved_post.update(**post.dict())
    
    key = updated_post.pop('key')
    db_connection.update(updated_post, key)
    
    return {
        'message': 'Post updated',
    }
    

@router.delete("/{post_key}")
async def delete_post(post_key: str):
    db_connection = get_connection('blog')
    saved_post = db_connection.get(post_key)
    if not saved_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    db_connection.delete(post_key)
    return {
        'message': 'Post deleted',
    }
