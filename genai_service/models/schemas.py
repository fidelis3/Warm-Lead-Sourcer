from typing import Optional
from pydantic import BaseModel, Field

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

class LeadScoreOutput(BaseModel):
    score: int = Field(description="The calculated Fit Score from 0 to 10.")
    reason: str = Field(description="A brief, one-sentence justification for the assigned score.")

