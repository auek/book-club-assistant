from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Book:
    title: str
    author: str
    rating: str
    date_display: str
    date_obj: Optional[datetime]
    link: str

    def to_dict(self):
        return {
            'title': self.title,
            'author': self.author,
            'rating': self.rating,
            'date_display': self.date_display,
            'date_obj': self.date_obj,
            'link': self.link
        }
