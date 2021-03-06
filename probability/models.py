import random
import string
from datetime import datetime

from flask import flash
from flask_login import UserMixin
from werkzeug import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash

from probability import app, db, login


def id_generator(size=32, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
