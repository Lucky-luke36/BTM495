from models import db

class Venue(db.Model):
    __tablename__ = 'venues'

    venue_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=True)
    capacity = db.Column(db.Integer, nullable=True)

    # Relationship: A venue can have many events
    events = db.relationship('Event', backref='venue', lazy=True)

    def __repr__(self):
        return f"<Venue {self.name}>"