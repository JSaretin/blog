from fastapi import APIRouter, status, HTTPException, BackgroundTasks

from main.utils.db import get_connection


router = APIRouter(prefix="/posts", tags=["posts"])


async def update_views(post_key: str):
    pass


@router.get("/")
async def get_all_post():
    posts = []
    return {"posts": posts}


@router.get("/{post_id}")
async def get_post(post_key: str, background_tasks: BackgroundTasks):
    db_connection = get_connection('blog')
    post = db_connection.get(post_key)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
    background_tasks.add_task(update_views, post_key)
    return {
        'post': post
    }
