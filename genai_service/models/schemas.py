from typing import Optional
from pydantic import BaseModel

class Interactions(BaseModel):
    username: str
    comment: str

class PostData(BaseModel):
    caption:str 
    likes_count: int
    comment_count: int
    post_url: str
    comments: list[Interactions]
    
class GeneralProfile(BaseModel):
    name: Optional[str]
    username: Optional[str]
    linkedin_url: Optional[str]
    current_role: Optional[str]
    education: Optional[str]
    country: Optional[str]
    email: Optional[str] 
    profile_pic_url: str
    verified: Optional[bool]
    post_data : PostData



    

