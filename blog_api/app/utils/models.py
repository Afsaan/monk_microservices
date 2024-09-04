from pydantic import BaseModel
from datetime import time

class BlogSchema(BaseModel):
    blog_img: str
    blog_title: str
    blog_user: str
    blog_time: time
    blog: str
    Tag: str

class BlogUpdateSchema(BlogSchema):
    old_blog_title: str