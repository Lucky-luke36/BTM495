from app.extentions import db

class Speaker(db.Model):
    __tablename__ = 'speakers'

    speaker_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    expertise = db.Column(db.String(100), nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'speaker'
    }

    def __repr__(self):
        return f"<Speaker {self.name}>"
