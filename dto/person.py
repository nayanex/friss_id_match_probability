from dataclasses import dataclass
from datetime import datetime
import marshmallow_dataclass


@dataclass
class Person:
    def __post_init__(self):
        self.birth_date = datetime.strptime(self.birth_date, "%d-%m-%Y")
    first_name: str
    last_name: str
    birth_date: datetime
    bsn: str

PersonSchema = marshmallow_dataclass.class_schema(Person)
