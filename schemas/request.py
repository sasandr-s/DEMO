from pydantic import BaseModel
from datetime import datetime

class Request_add(BaseModel):
    location: str
    pay: str
    date: datetime
