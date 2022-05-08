from pydantic import BaseModel


class Post(BaseModel):
    title: str
    content: str
    
    
class PostInDb(Post):
    key: str
    views: int = 0
    likes: int = 0
    created_at: float
    updated_at: float
    
    
class Comment(BaseModel):
    name: str
    email: str
    content: str
    post_key: str
    
    
    
class LoginForm(BaseModel):
    username: str
    password: str
    is_robot: bool = False
    grant_access: bool = False
    
    login_browser: str
    login_user_agent: str
    login_ip: str
    login_country: str
    login_city: str
    login_region: str
    
    
class RegisterForm(BaseModel):
    name: str
    username: str
    email: str
    password: str
    confirm_password: str
    terms: bool
    is_robot: bool = False
    grant_access: bool = False
    

class User(BaseModel):
    name: str
    username: str
    email: str
    password: str
    last_login: float = None
    refresh_token: str = ''
    last_login_ip: str = ''
    last_login_country: str = ''
    last_login_city: str = ''
    last_login_region: str = ''
    created_at: float
    updated_at: float