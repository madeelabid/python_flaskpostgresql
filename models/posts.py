from app import db


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True,)
    userId = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    content = db.Column(db.String(), nullable=False)


    def __init__(self, userId, content):
        self.userId = userId
        self.content = content

    def __repr__(self):
        return f"<Post {self.id}>"

    def serialize(self):
        return {
            'id': self.id,
            'userId': self.userId,
            'content': self.content
        }