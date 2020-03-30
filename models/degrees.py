from app import db


class Degree(db.Model):
    __tablename__ = 'degrees'

    id = db.Column(db.Integer, primary_key=True,)
    degreeName = db.Column(db.String(), nullable=False)

    def __init__(self, degreeName):
        self.degreeName = degreeName

    def __repr__(self):
        return f"<Degree {self.id}>"

    def serialize(self):
        return {
            'id': self.id,
            'tagName': self.degreeName,
        }