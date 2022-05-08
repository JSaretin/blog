from fastapi import APIRouter, Depends, status, HTTPException

from main.router.admin.utils import get_now

from .models import LoginForm, Post, PostInDb, RegisterForm, User
from main.utils.db import get_connection
from bcrypt import checkpw, hashpw, gensalt
from jose import jwt

from .utils import get_current_user, secret_key


router = APIRouter(prefix="/auth", tags=["auth"], dependencies=[Depends(get_current_user)])



@router.post("/login")
async def login(login_form: LoginForm):
    db_connection = get_connection('blog_authors')
    if login_form.is_robot or login_form.grant_access:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login")
    author = db_connection.get(login_form.username)
    if not author:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login")
    if not checkpw(login_form.password.encode('utf-8'), author['password'].encode('utf-8')):
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login")
        
    payload = {
        'user_id': author['key'],
        'created_at': get_now(),
        'expire_at': get_now() + 60 * 60 * 24,
    }
    new_token = jwt.encode(payload, secret_key, algorithm='HS256')
    
    return {
        'message': 'Login successful',
        'token': f'Bearer {new_token}',
    }
    
    
@router.post("/register")
async def register(register_form: RegisterForm):
    if register_form.is_robot or register_form.grant_access or register_form.terms:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid registration")
    db_connection = get_connection('blog_authors')
    user = db_connection.fetch([{'username':register_form.username}, {'email':register_form.email}])
    if user.count:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User already exists")
    password = hashpw(register_form.password.encode('utf-8'), gensalt())
    now = get_now()
    new_user = User(username=register_form.username, email=register_form.email, password=password, created_at=now, updated_at=now).dict()
    
    db_connection.put(new_user)
    
    return {
        'message': 'Registration successful',
    }
    