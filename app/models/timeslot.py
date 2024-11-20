from models import db

# Association Table for TimeSlot and Speaker (many-to-many relationship)
time_slot_speakers = db.Table('time_slot_speakers',
    db.Column('slot_id', db.Integer, db.ForeignKey('time_slots.slot_id'), primary_key=True),
    db.Column('speaker_id', db.Integer, db.ForeignKey('speakers.speaker_id'), primary_key=True)
)

class TimeSlot(db.Model):
    __tablename__ = 'time_slots'

    slot_id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Time, nullable=False)  # Start of the time slot (e.g., 08:00:00)
    end_time = db.Column(db.Time, nullable=False)    # End of the time slot (e.g., 09:00:00)
    schedule_id = db.Column(db.Integer, db.ForeignKey('schedules.schedule_id'), nullable=False)

    # Many-to-many relationship with speakers
    speakers = db.relationship('Speaker', secondary='time_slot_speakers', backref='time_slots')

    def __repr__(self):
        return f"<TimeSlot: {self.start_time} - {self.end_time}>"
