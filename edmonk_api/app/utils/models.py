from pydantic import BaseModel
from datetime import date, time

class eventSummaryList(BaseModel):
    listTitle: str

class speakers(BaseModel):
    name: str
    post: str

class WebinarSchema(BaseModel):
    eventImg: str
    eventTitle: str
    eventSummary: str
    eventSummaryList: list[eventSummaryList]
    speakers: list[speakers]
    eventMonth: date
    eventDate: date
    start_time: time
    end_time: time
    Tag: str
    active: bool