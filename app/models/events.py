from models import db
from models.schedule import Schedule 
from models.venue import Venue
from models.admin import admin_event_association


class Event(db.Model):
    __tablename__ = 'events'

    event_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(50),  nullable=False)

    # Foreign Key to Venue
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.venue_id'), nullable=False)
    
    schedule = db.relationship('Schedule', backref='event', uselist=False)

    admins = db.relationship('Admin', secondary=admin_event_association, back_populates='events')
    

    def __repr__(self):
        return f"<Event {self.name}>"
