from pydantic import BaseModel

class BlogSchema(BaseModel):
    title: str
    blog: str
    Tag: str
    
class BlogUpdateSchema(BlogSchema):
    old_blog_title: str