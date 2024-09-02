from pydantic import BaseModel
from datetime import date

class WebinarSchema(BaseModel):
    image: str
    title: str
    description: str
    date: date
    start_time: str
    end_time: str
    Tag: str
    active: bool