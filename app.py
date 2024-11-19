import os
from flask import Flask, render_template, request, redirect, url_for, g, session
from models.speaker import Speaker
from models.events import Event
from models.schedule import Schedule
from models.timeslot import TimeSlot
from models.venue import Venue
from models.admin import Admin
from models import db 
from datetime import datetime
from flask import jsonify


app = Flask(__name__)

# Set a secret key for session management
app.config['SECRET_KEY'] = os.urandom(24)  # Generates a random 24-byte key

# Get the absolute path of the current directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Update the database URI to use the current directory for storing the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crm.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Bind the app with SQLAlchemy (initialize db with app)
db.init_app(app)

# Checking if the app context is working
with app.app_context():
    print("App context is active. Creating database...")
    db.create_all()
    print("Database created successfully.")


######### Login Page ##################

@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.admin = None
    else:
        g.admin = Admin.query.get(user_id)  # Assuming session stores user_id


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.check_password(password):
            session['user_id'] = admin.admin_id  # Store the admin ID in the session
            return redirect(url_for('dashboard'))
        else:
            error_message = "Invalid username or password"
            return render_template('index.html', error_message=error_message)
    
    return render_template('index.html')




####### Speakers Page #################

# Defining route to display speakers
@app.route('/speakers')
def list_speakers():
    speakers = Speaker.query.all()
    return render_template('speakers.html', speakers=speakers)

# Route to handle form submission to add a speaker
@app.route('/add_speaker', methods=['POST'])
def add_speaker():
    # Print form data for debugging
    print("Form submitted")

    # Check if the form has data
    if 'name' in request.form and 'email' in request.form and 'expertise' in request.form:
        # Get the form data
        name = request.form['name']
        email = request.form['email']
        expertise = request.form['expertise']

        # Debug print to verify form data
        print(f"Received data - Name: {name}, Email: {email}, Expertise: {expertise}")

        # Create a new speaker instance and save it to the database
        new_speaker = Speaker(name=name, email=email, expertise=expertise)
        db.session.add(new_speaker)
        db.session.commit()

        # Redirect back to the speakers list
        return redirect(url_for('list_speakers'))
    
    else:
        # If form data is missing, print an error message for debugging
        print("Form data missing")
        return redirect(url_for('list_speakers'))  # Redirect to speakers list even if something is wrong


@app.before_request
def override_method():
    if request.method == 'POST' and '_method' in request.form:
        method = request.form['_method']
        if method.upper() in ['DELETE']:
            request.environ['REQUEST_METHOD'] = method.upper()

@app.route('/delete_speaker/<int:speaker_id>', methods=['POST'])
def delete_speaker(speaker_id):
    # Query the speaker by ID
    speaker_to_delete = Speaker.query.get_or_404(speaker_id)

    try:
        # Delete the speaker from the database
        db.session.delete(speaker_to_delete)
        db.session.commit()
        return redirect(url_for('list_speakers'))
    except Exception as e:
        # Handle any exceptions
        print(f"Error occurred: {e}")
        return redirect(url_for('list_speakers'))

@app.route('/update_speaker', methods=['POST'])
def update_speaker():
    speaker_id = request.form.get('speaker_id')
    name = request.form.get('name')
    email = request.form.get('email')
    expertise = request.form.get('expertise')

    # Fetch the speaker from the database
    speaker = Speaker.query.get_or_404(speaker_id)
    speaker.name = name
    speaker.email = email
    speaker.expertise = expertise

    # Save the changes to the database
    db.session.commit()
    return redirect(url_for('list_speakers'))




####### Events Page #################

# Defining route to display events
@app.route('/events', methods=['GET'])
def list_events():
    event = Event.query.all()
    venues = Venue.query.all()    
    return render_template('events.html', events=event, venues=venues)

# Route to handle form submission to add an event
@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        # Handle the form submission (POST request)
        name = request.form.get('name')
        date = request.form.get('date')
        venue_id = request.form.get('venue_id')
        
        if not name or not date or not venue_id:
            print("Form data missing")
            return redirect(url_for('list_speakers'))  # Or handle with a flash message or error
        
        # Debug print to verify form data
        print(f"Received data - Name: {name}, Date: {date}, Venue ID: {venue_id}")

        # Create a new event instance and save it to the database
        new_event = Event(name=name, date=date, venue_id=venue_id)
        db.session.add(new_event)
        db.session.commit()

        # Automatically create a default schedule (from 8am to 5pm) for the new event
        default_start_time = datetime.strptime("08:00:00", "%H:%M:%S").time()
        default_end_time = datetime.strptime("17:00:00", "%H:%M:%S").time()

        default_schedule = Schedule(start_time=default_start_time, end_time=default_end_time, event_id=new_event.event_id)
        db.session.add(default_schedule)
        db.session.commit()

        # Redirect after adding the event and schedule
        return redirect(url_for('list_events'))

    # Render the form with venues list
    return render_template('list_events')



@app.before_request
def override_method():
    if request.method == 'POST' and '_method' in request.form:
        method = request.form['_method']
        if method.upper() in ['DELETE']:
            request.environ['REQUEST_METHOD'] = method.upper()

@app.route('/delete_event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    # Query the speaker by ID
    event_to_delete = Event.query.get_or_404(event_id)

    try:
        # Delete the speaker from the database
        db.session.delete(event_to_delete)
        db.session.commit()
        return redirect(url_for('list_events'))
    except Exception as e:
        # Handle any exceptions
        print(f"Error occurred: {e}")
        return redirect(url_for('list_events'))

@app.route('/update_event', methods=['POST'])
def update_event():
    event_id = request.form.get('event_id')
    name = request.form.get('name')
    date = request.form.get('date')
    venue_id = request.form.get('venue_id')

    # Fetch the event to update
    event = Event.query.get_or_404(event_id)
    if event:
        # Update the event details
        event.name = name
        event.date = date
        event.venue_id = venue_id
        db.session.commit()

    return redirect(url_for('list_events'))


######### Manager Page ##################



# Route to render the manager page
@app.route('/manager')
def dashboard():
    speakers = Speaker.query.all()
    events = Event.query.all()
    admins = Admin.query.all() 
    return render_template('manager.html', speakers=speakers, events=events, admins=admins)

@app.route('/event_details/<int:event_id>')
def event_details(event_id):
    # Fetch the event details based on the selected event_id
    event = Event.query.get_or_404(event_id)
    schedule = event.schedule

    # Get the time slots associated with the schedule
    time_slots = schedule.time_slots if schedule else []

    # Render the event details as a partial HTML snippet
    return render_template('partials/event_details.html', event=event, schedule=schedule, time_slots=time_slots)




from flask import jsonify

@app.route('/add_time_slot', methods=['POST'])
def add_time_slot():
    speaker_id = request.form['speaker_id']
    event_id = request.form['event_id']
    start_time_str = request.form['start_time']
    end_time_str = request.form['end_time']

    # Convert the time strings to Python time objects
    start_time = datetime.strptime(start_time_str, "%H:%M").time()
    end_time = datetime.strptime(end_time_str, "%H:%M").time()

    event = Event.query.get_or_404(event_id)
    schedule = event.schedule

    # Validation: Check if the time slot is within the schedule's start and end time
    if start_time < schedule.start_time or end_time > schedule.end_time:
        return jsonify(success=False, message="Time slot must be within the schedule timeframe!")
    
    # Validation: Check if the start time is earlier than the end time
    if start_time >= end_time:
        return jsonify(success=False, message="Start time must be earlier than end time!")

    # Create new time slot
    new_time_slot = TimeSlot(start_time=start_time, end_time=end_time, schedule_id=schedule.schedule_id)
    speaker = Speaker.query.get_or_404(speaker_id)
    new_time_slot.speakers.append(speaker)

    db.session.add(new_time_slot)
    db.session.commit()

    return jsonify(success=True)


@app.route('/delete_time_slot/<int:slot_id>', methods=['POST'])
def delete_time_slot(slot_id):
    # Find the time slot by ID
    time_slot = TimeSlot.query.get_or_404(slot_id)
    
    try:
        # Delete the time slot from the database
        db.session.delete(time_slot)
        db.session.commit()
        
        return jsonify(success=True)
    except Exception as e:
        # If there's an error, return an error message
        return jsonify(success=False, message=str(e))


####### Venues Page ################

@app.route('/venues')
def list_venues():
    venues = Venue.query.all()
    return render_template('venues.html', venues=venues)

# Route to handle form submission to add an event
@app.route('/add_venue', methods=['POST'])
def add_venue():
    # Print form data for debugging
    print("Form submitted")

    # Check if the form has data
    if 'name' in request.form and 'location' in request.form and 'capacity' in request.form :
        # Get the form data
        name = request.form['name']
        location = request.form['location']
        capacity = request.form['capacity']


        # Debug print to verify form data
        print(f"Received data - Name: {name}")

        # Create a new event instance and save it to the database
        new_venue = Venue(name=name, location=location ,capacity=capacity)
        db.session.add(new_venue)
        db.session.commit()

        # Redirect back to the speakers list
        return redirect(url_for('list_venues'))
    
    else:
        # If form data is missing, print an error message for debugging
        print("Form data missing")
        return redirect(url_for('list_venues'))  # Redirect to speakers list even if something is wrong

@app.route('/delete_venue/<int:venue_id>', methods=['POST'])
def delete_venue(venue_id):
    # Query the speaker by ID
    venue_to_delete = Venue.query.get_or_404(venue_id)

    try:
        # Delete the speaker from the database
        db.session.delete(venue_to_delete)
        db.session.commit()
        return redirect(url_for('list_venues'))
    except Exception as e:
        # Handle any exceptions
        print(f"Error occurred: {e}")
        return redirect(url_for('list_venues'))

if __name__ == '__main__':
    app.run(debug=True)