from app import db
from models.helpers import userDegrees

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True,)
    name = db.Column(db.String())
    grade = db.Column(db.String())
    address = db.Column(db.String())
    country = db.Column(db.String())
    posts = db.relationship('Post', lazy='dynamic', backref=db.backref('user', lazy=True, uselist= False))  #if one-to-one relation than uselist=False
    degrees = db.relationship('Degree', secondary=userDegrees, lazy=True,backref=db.backref('users', lazy=True))  # if one-to-one relation than uselist=False

    def __init__(self, name, grade, address,country):
        self.name = name
        self.grade = grade
        self.address = address
        self.country = country

    def __repr__(self):
        return f"<User {self.name}>"

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'grade': self.grade,
            'address': self.address,
            'country': self.country
        }