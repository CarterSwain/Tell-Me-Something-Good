from . import db

class PushToken(db.Model):
    __tablename__ = 'push_tokens'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return f"<PushToken {self.token}>"
