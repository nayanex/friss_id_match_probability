from dataclasses import dataclass
from datetime import datetime


@dataclass
class Person:
    def __post_init__(self):
        if self.birth_date:
            self.birth_date = datetime.strptime(self.birth_date, "%d-%m-%Y")

    first_name: str
    last_name: str
    birth_date: datetime
    bsn: str

    def to_json(self):
        json_post = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "birth_date": self.birth_date,
            "bsn": self.bsn,
        }
        return json_post

    @staticmethod
    def from_json(json_post):
        first_name = json_post.get("first_name")
        last_name = json_post.get("last_name")
        birth_date = json_post.get("birth_date")
        bsn = json_post.get("bsn")
        if first_name is None or first_name == "":
            raise ValidationError("person does not have a first name.")
        return Person(
            first_name=first_name, last_name=last_name, birth_date=birth_date, bsn=bsn
        )
