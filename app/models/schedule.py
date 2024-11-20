from app.extentions import db
from app.models.timeslot import TimeSlot

class Schedule(db.Model):
    __tablename__ = 'schedules'

    schedule_id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Time, nullable=False)  # Example: 08:00:00
    end_time = db.Column(db.Time, nullable=False)    # Example: 17:00:00
    event_id = db.Column(db.Integer, db.ForeignKey('events.event_id'), nullable=False)

    # One-to-many relationship with time slots
    time_slots = db.relationship('TimeSlot', backref='schedule', lazy=True)

    def __repr__(self):
        return f"<Schedule for Event {self.event_id}: {self.start_time} - {self.end_time}>"
