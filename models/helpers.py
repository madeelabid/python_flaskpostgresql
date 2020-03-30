from app import db

userDegrees = db.Table('user_degrees',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('degree_id', db.Integer, db.ForeignKey('degrees.id'), primary_key=True)
)
