from models import db
from models.speaker import Speaker
from models.admin import Admin
from models.venue import Venue
from models.events import Event
from models.schedule import Schedule
from models.admin import admin_event_association
from werkzeug.security import generate_password_hash
from datetime import datetime

def populate_db():
    # Create mock data for Speakers
    speaker1 = Speaker(name="John Doe", email="johndoe@example.com", expertise="Cybersecurity")
    speaker2 = Speaker(name="Jane Smith", email="janesmith@example.com", expertise="Cloud Computing")
    speaker3 = Speaker(name="Michael Johnson", email="mjohnson@example.com", expertise="AI and Machine Learning")

    # Create mock data for Admins
    admin1 = Admin(name="Alice Admin", email="aliceadmin@example.com", username="alice", password_hash=generate_password_hash("password1"))
    admin2 = Admin(name="Bob Manager", email="bobmanager@example.com", username="bob", password_hash=generate_password_hash("password2"))
    
    # Create mock data for Venues
    venue1 = Venue(name="Tech Convention Center", location="New York, NY", capacity=500)
    venue2 = Venue(name="Innovation Hub", location="San Francisco, CA", capacity=300)

    # Create mock data for Events
    event1 = Event(name="Tech Conference 2024", date=datetime(2024, 3, 15), venue_id=1)
    event2 = Event(name="Marketing Summit 2024", date=datetime(2024, 5, 10), venue_id=2)
    
    # Create schedules for the events
    schedule1 = Schedule(start_time=datetime.strptime("08:00", "%H:%M").time(), end_time=datetime.strptime("17:00", "%H:%M").time(), event_id=1)
    schedule2 = Schedule(start_time=datetime.strptime("09:00", "%H:%M").time(), end_time=datetime.strptime("18:00", "%H:%M").time(), event_id=2)

    # Add the speakers, admins, venues, and events to the database session
    db.session.add_all([speaker1, speaker2, speaker3, admin1, admin2, venue1, venue2, event1, event2, schedule1, schedule2])

    # Commit the initial data to the database
    db.session.commit()

    # Associate admins with events using the admin_event_association table
    event1.admins.append(admin1)  # Associate Alice with event1
    event2.admins.append(admin2)  # Associate Bob with event2

    # Commit the admin to event association
    db.session.commit()

    print("Database populated with mock data successfully!")

if __name__ == '__main__':
    from app import app  # Ensure that Flask app context is loaded
    
    with app.app_context():
        populate_db()
